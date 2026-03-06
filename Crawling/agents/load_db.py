"""
Load DB Agent
accepted price_observations → PostgreSQL 멱등 적재.
멱등성 키: (run_id, sku_id, country, source, content_hash)

카탈로그 초기화 (skus + sku_urls) 기능도 포함.
"""
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any

import psycopg2
import psycopg2.extras

from config import DB_URL, CATALOG_DIR

logger = logging.getLogger(__name__)


def get_conn():
    return psycopg2.connect(DB_URL)


# ── 카탈로그 로드 ────────────────────────────────────────────

def _load_catalog_file(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def init_catalog(conn):
    """samsung.json + competitors.json → skus + sku_urls 테이블 동기화."""
    cur = conn.cursor()

    for fname in ["samsung.json", "competitors.json"]:
        cat = _load_catalog_file(CATALOG_DIR / fname)
        brand = cat.get("brand")
        skus  = cat["skus"]
        urls  = cat["urls"]

        for sku in skus:
            b = brand or sku.get("brand")
            cur.execute("""
                INSERT INTO skus (sku_id, brand, category, model, capacity, notes)
                VALUES (%s,%s,%s,%s,%s,%s)
                ON CONFLICT (sku_id) DO UPDATE SET
                    model=EXCLUDED.model, capacity=EXCLUDED.capacity, notes=EXCLUDED.notes
            """, (sku["sku_id"], b, sku["category"], sku["model"],
                  sku.get("capacity"), sku.get("notes")))

            sku_urls = urls.get(sku["sku_id"], {})
            for country, sources in sku_urls.items():
                for source, url in sources.items():
                    cur.execute("""
                        INSERT INTO sku_urls (sku_id, country, source, url)
                        VALUES (%s,%s,%s,%s)
                        ON CONFLICT (sku_id, country, source) DO UPDATE SET url=EXCLUDED.url
                    """, (sku["sku_id"], country, source, url))

    conn.commit()
    cur.close()
    logger.info("Catalog sync done.")


# ── 가격 적재 ────────────────────────────────────────────────

def insert_observations(conn, observations: list[dict]) -> dict:
    cur = conn.cursor()
    inserted = 0
    skipped  = 0
    failed   = []

    for obs in observations:
        try:
            cur.execute("""
                INSERT INTO price_observations (
                    run_id, sku_id, country, source, observed_at,
                    price, currency, original_price, shipping_price,
                    availability, seller_name, fulfillment, condition,
                    offer_scope, content_hash, raw_path, parse_confidence, parse_notes
                ) VALUES (
                    %s,%s,%s,%s,%s,
                    %s,%s,%s,%s,
                    %s,%s,%s,%s,
                    %s,%s,%s,%s,%s
                )
                ON CONFLICT (run_id, sku_id, country, source, content_hash) DO NOTHING
            """, (
                obs["run_id"], obs["sku_id"], obs["country"], obs["source"],
                obs["observed_at"],
                obs.get("price"), obs.get("currency"),
                obs.get("original_price"), obs.get("shipping_price"),
                obs.get("availability"), obs.get("seller_name"),
                obs.get("fulfillment"), obs.get("condition", "new"),
                obs.get("offer_scope", "unknown"),
                obs.get("content_hash"), obs.get("raw_path"),
                obs.get("parse_confidence"), obs.get("parse_notes"),
            ))
            if cur.rowcount > 0:
                inserted += 1
            else:
                skipped += 1
        except Exception as e:
            failed.append({"sku_id": obs["sku_id"], "error": str(e)})
            conn.rollback()
            logger.error(f"insert failed: {obs['sku_id']} — {e}")

    conn.commit()
    cur.close()
    return {"inserted": inserted, "skipped": skipped, "failed": failed}


def insert_hitl_queue(conn, items: list[dict]) -> int:
    cur = conn.cursor()
    count = 0
    for item in items:
        cur.execute("""
            INSERT INTO hitl_queue (run_id, sku_id, country, source, priority, reason, evidence, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            item["run_id"], item["sku_id"], item["country"], item["source"],
            item["priority"], item["reason"],
            psycopg2.extras.Json(item.get("evidence", {})),
            item.get("status", "pending"),
        ))
        count += 1
    conn.commit()
    cur.close()
    return count


def log_run(conn, run_id: str, data: dict):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO run_log (run_id, started_at, completed_at, total_targets,
                             success_count, quarantine_count, hitl_count, status)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        ON CONFLICT (run_id) DO UPDATE SET
            completed_at=EXCLUDED.completed_at,
            total_targets=EXCLUDED.total_targets,
            success_count=EXCLUDED.success_count,
            quarantine_count=EXCLUDED.quarantine_count,
            hitl_count=EXCLUDED.hitl_count,
            status=EXCLUDED.status
    """, (
        run_id,
        data.get("started_at"), data.get("completed_at"),
        data.get("total_targets", 0), data.get("success_count", 0),
        data.get("quarantine_count", 0), data.get("hitl_count", 0),
        data.get("status", "completed"),
    ))
    conn.commit()
    cur.close()


def fetch_last_prices(conn) -> dict:
    """최근 관측 가격 { (sku_id, country, source): price } 반환 (anomaly 감지용)."""
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT ON (sku_id, country, source)
            sku_id, country, source, price
        FROM price_observations
        WHERE is_accepted = TRUE
        ORDER BY sku_id, country, source, observed_at DESC
    """)
    result = {
        (row[0], row[1], row[2]): float(row[3])
        for row in cur.fetchall()
        if row[3] is not None
    }
    cur.close()
    return result
