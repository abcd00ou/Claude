"""
Price Intelligence Pipeline — 메인 진입점

사용법:
  python run_pipeline.py                          # 기본 (US, amazon+manufacturer)
  python run_pipeline.py --country US KR          # 국가 지정
  python run_pipeline.py --source amazon          # 소스 지정
  python run_pipeline.py --sku sam_t9_2tb         # 특정 SKU만
  python run_pipeline.py --init-db                # DB 스키마 초기화
  python run_pipeline.py --init-catalog           # 카탈로그 DB 동기화만
  python run_pipeline.py --dry-run                # 실제 크롤링 없이 테스트

실행 순서 (DAG):
  1. CatalogValidation  — SKU↔URL 매핑 검증
  2. FetchRaw           — Playwright 크롤링
  3. ParseExtract       — HTML → 가격 구조화
  4. Normalize          — 통화/숫자 정규화
  5. QualityGate        — accept / quarantine
  6. HITLTriage         — HITL 큐 생성
  7. LoadDB             — PostgreSQL 적재
  8. Report             — 실행 결과 요약
"""
import argparse
import asyncio
import json
import logging
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

from config import (
    CATALOG_DIR, DB_URL, LOGS_DIR,
    DEFAULT_COUNTRIES, SUPPORTED_COUNTRIES,
)
from agents import fetch_raw, parse_extract, normalizer, quality_gate, hitl_triage, load_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("pipeline")


# ── 1. 카탈로그 로드 ─────────────────────────────────────────

def load_catalog_targets(countries: list[str], sources_filter: list[str], sku_filter: list[str]) -> list[dict]:
    """catalog/*.json → 크롤링 대상 목록 생성."""
    targets = []
    for fname in ["samsung.json", "competitors.json"]:
        path = CATALOG_DIR / fname
        if not path.exists():
            logger.warning(f"Catalog not found: {path}")
            continue
        with open(path, encoding="utf-8") as f:
            cat = json.load(f)

        urls = cat["urls"]
        for sku_id, country_map in urls.items():
            if sku_filter and sku_id not in sku_filter:
                continue
            for country, source_map in country_map.items():
                if country not in countries:
                    continue
                for source, url in source_map.items():
                    if sources_filter and source not in sources_filter:
                        continue
                    targets.append({
                        "sku_id":  sku_id,
                        "country": country,
                        "source":  source,
                        "url":     url,
                    })
    return targets


# ── 2. 카탈로그 검증 ─────────────────────────────────────────

def validate_catalog(targets: list[dict]) -> dict:
    """기본 유효성 검사."""
    missing_url = [t for t in targets if not t.get("url")]
    sku_set     = {t["sku_id"] for t in targets}
    return {
        "total":       len(targets),
        "missing_url": missing_url,
        "sku_count":   len(sku_set),
        "ready":       len(missing_url) == 0,
    }


# ── 3. 드라이런 모의 스냅샷 ──────────────────────────────────

def _make_dry_run_snapshots(targets: list[dict], run_date: str) -> list[dict]:
    """실제 크롤링 없이 더미 스냅샷 생성 (구조 테스트용)."""
    return [
        {
            "sku_id":      t["sku_id"],
            "country":     t["country"],
            "source":      t["source"],
            "url":         t["url"],
            "observed_at": datetime.now(timezone.utc).isoformat(),
            "http_status": 200,
            "final_url":   t["url"],
            "content_hash": None,
            "raw_path":    None,
            "fetch_notes": "dry_run",
        }
        for t in targets
    ]


# ── 메인 파이프라인 ──────────────────────────────────────────

async def run_pipeline(args):
    run_id   = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    run_date = datetime.now().strftime("%Y-%m-%d")
    started  = datetime.now(timezone.utc)

    logger.info(f"▶ Pipeline start | run_id={run_id}")
    logger.info(f"  countries={args.country} | sources={args.source or 'all'} | dry_run={args.dry_run}")

    # DB 연결
    try:
        conn = load_db.get_conn()
    except Exception as e:
        logger.error(f"DB 연결 실패: {e}")
        logger.error(f"  → DB_URL: {DB_URL}")
        logger.error("  → PostgreSQL이 실행 중인지 확인하세요: brew services start postgresql")
        sys.exit(1)

    # DB 초기화
    if args.init_db:
        schema_path = Path(__file__).parent / "db" / "schema.sql"
        with open(schema_path) as f:
            conn.cursor().execute(f.read())
        conn.commit()
        logger.info("DB 스키마 초기화 완료.")

    # 카탈로그 DB 동기화
    load_db.init_catalog(conn)
    logger.info("Catalog sync 완료.")

    if args.init_catalog:
        logger.info("--init-catalog: 카탈로그 동기화만 수행 후 종료.")
        conn.close()
        return

    # ── Step 1: 카탈로그 → 타겟 ──────────────────────────────
    targets = load_catalog_targets(
        countries=args.country,
        sources_filter=args.source or [],
        sku_filter=args.sku or [],
    )

    validation = validate_catalog(targets)
    logger.info(f"[1/8] CatalogValidation — {validation['sku_count']} SKUs, {validation['total']} targets")

    if not validation["ready"]:
        logger.warning(f"  Missing URL targets: {validation['missing_url'][:5]}")

    if not targets:
        logger.warning("타겟 없음. catalog/*.json을 확인하세요.")
        conn.close()
        return

    # ── Step 2: FetchRaw ─────────────────────────────────────
    logger.info(f"[2/8] FetchRaw — {len(targets)} URLs 크롤링 시작…")

    if args.dry_run:
        snapshots = _make_dry_run_snapshots(targets, run_date)
        logger.info("  dry-run: 실제 크롤링 생략.")
    else:
        snapshots = await fetch_raw.fetch_all(targets, run_date)

    fetched_ok = sum(1 for s in snapshots if s.get("raw_path") or args.dry_run)
    logger.info(f"  완료: {fetched_ok}/{len(snapshots)} 성공")

    # ── Step 3: ParseExtract ─────────────────────────────────
    logger.info("[3/8] ParseExtract — 가격 추출 중…")
    records = parse_extract.extract_all(snapshots)
    for rec in records:
        rec["run_id"] = run_id
    logger.info(f"  추출 완료: {len(records)}건")

    # ── Step 4: Normalize ────────────────────────────────────
    logger.info("[4/8] Normalize — 통화/숫자 정규화 중…")
    observations, norm_warnings = normalizer.normalize_all(records)
    if norm_warnings:
        logger.warning(f"  정규화 경고 {len(norm_warnings)}건: {norm_warnings[:3]}")

    # ── Step 5: QualityGate ──────────────────────────────────
    logger.info("[5/8] QualityGate — 품질 검사 중…")
    last_prices = load_db.fetch_last_prices(conn)
    gate_result = quality_gate.gate(observations, last_prices)
    summary     = gate_result["summary"]
    logger.info(
        f"  accepted={summary['accepted']} | "
        f"quarantined={summary['quarantined']} | "
        f"anomalies={summary['anomalies']}"
    )

    # ── Step 6: HITLTriage ───────────────────────────────────
    logger.info("[6/8] HITLTriage — HITL 큐 생성 중…")
    hitl_items = hitl_triage.build_hitl_queue(
        run_id,
        gate_result["quarantined"],
        gate_result["anomalies"],
    )
    p_summary = hitl_triage.priority_summary(hitl_items)
    logger.info(f"  HITL: {p_summary['total']}건 (P0={p_summary['P0']}, P1={p_summary['P1']})")
    if p_summary["P0_skus"]:
        logger.warning(f"  P0 항목: {p_summary['P0_skus']}")

    # ── Step 7: LoadDB ───────────────────────────────────────
    logger.info("[7/8] LoadDB — PostgreSQL 적재 중…")
    db_result = load_db.insert_observations(conn, gate_result["accepted"])
    logger.info(
        f"  inserted={db_result['inserted']} | skipped={db_result['skipped']} | failed={len(db_result['failed'])}"
    )

    if hitl_items:
        hitl_count = load_db.insert_hitl_queue(conn, hitl_items)
        logger.info(f"  HITL 큐 {hitl_count}건 등록.")

    # run_log 기록
    completed = datetime.now(timezone.utc)
    load_db.log_run(conn, run_id, {
        "started_at":       started.isoformat(),
        "completed_at":     completed.isoformat(),
        "total_targets":    len(targets),
        "success_count":    db_result["inserted"],
        "quarantine_count": summary["quarantined"],
        "hitl_count":       len(hitl_items),
        "status":           "completed" if not db_result["failed"] else "partial",
    })

    # ── Step 8: Report ───────────────────────────────────────
    elapsed = (completed - started).total_seconds()
    report = {
        "run_id":           run_id,
        "elapsed_sec":      round(elapsed, 1),
        "total_targets":    len(targets),
        "fetch_ok":         fetched_ok,
        "accepted":         summary["accepted"],
        "quarantined":      summary["quarantined"],
        "anomalies":        summary["anomalies"],
        "hitl_total":       len(hitl_items),
        "hitl_P0":          p_summary["P0"],
        "db_inserted":      db_result["inserted"],
        "db_failed":        len(db_result["failed"]),
    }

    log_path = LOGS_DIR / f"{run_id}.json"
    with open(log_path, "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    logger.info(f"[8/8] Report — 완료! ({elapsed:.1f}초)")
    logger.info(f"  로그: {log_path}")
    logger.info(
        f"\n{'='*50}\n"
        f"  Run ID:      {run_id}\n"
        f"  대상 URL:    {len(targets)}\n"
        f"  수집 성공:   {fetched_ok}\n"
        f"  DB 적재:     {db_result['inserted']}건 신규\n"
        f"  Quarantine:  {summary['quarantined']}건\n"
        f"  HITL (P0):   {p_summary['P0']}건 → 대시보드 확인 필요\n"
        f"  소요 시간:   {elapsed:.1f}초\n"
        f"{'='*50}"
    )

    conn.close()
    return report


# ── CLI ──────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Price Intelligence Pipeline")
    parser.add_argument(
        "--country", nargs="+",
        default=DEFAULT_COUNTRIES,
        choices=SUPPORTED_COUNTRIES,
        help="크롤링 대상 국가 (기본: US)",
    )
    parser.add_argument(
        "--source", nargs="+",
        choices=["amazon", "manufacturer"],
        help="소스 필터 (기본: 전체)",
    )
    parser.add_argument(
        "--sku", nargs="+",
        help="특정 SKU만 실행 (예: sam_t9_2tb sd_extreme_1tb)",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="실제 크롤링 없이 파이프라인 구조 테스트",
    )
    parser.add_argument(
        "--init-db", action="store_true",
        help="DB 스키마 초기화 (최초 1회)",
    )
    parser.add_argument(
        "--init-catalog", action="store_true",
        help="카탈로그 DB 동기화만 수행",
    )

    args = parser.parse_args()
    asyncio.run(run_pipeline(args))


if __name__ == "__main__":
    main()
