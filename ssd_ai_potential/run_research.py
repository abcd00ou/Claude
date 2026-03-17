"""
run_research.py — SSD × AI 수요 조사 전체 실행 진입점

사용법:
  python run_research.py --mode full          # 최초 실행 (6개월치 전체)
  python run_research.py --mode incremental   # 이후 실행 (12시간 신규)
  python run_research.py --mode report-only   # 크롤링 없이 리포트만 재생성
"""
import argparse
import logging
import subprocess
import sys
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [RUN] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("research.log", encoding="utf-8"),
    ]
)
log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="SSD AI 수요 조사 에이전트")
    parser.add_argument("--mode", choices=["full", "incremental", "report-only"],
                        default="full", help="실행 모드")
    parser.add_argument("--no-open", action="store_true",
                        help="리포트 브라우저 자동 열기 비활성화")
    args = parser.parse_args()

    start = datetime.now(timezone.utc)
    log.info(f"=== SSD × AI 수요 조사 시작 | 모드: {args.mode} | {start.isoformat()} ===")

    # ── 1. 크롤링 ──────────────────────────────────────────────
    if args.mode != "report-only":
        log.info("─── [1/3] 크롤링 시작 ───")
        from crawler_agent import CrawlerAgent
        crawler = CrawlerAgent()
        new_count = crawler.run(mode=args.mode)
        log.info(f"크롤링 완료: 신규 {new_count}개")
    else:
        log.info("report-only 모드 — 크롤링 생략")

    # ── 2. 분석 ────────────────────────────────────────────────
    log.info("─── [2/3] 분석 시작 ───")
    from analyzer_agent import AnalyzerAgent
    analyzer = AnalyzerAgent()
    result = analyzer.run()
    if result:
        log.info(f"분석 완료: 수요신호 {result['demand_total']}개 ({result['demand_rate_pct']}%)")
    else:
        log.error("분석 실패")
        sys.exit(1)

    # ── 3. 리포트 ──────────────────────────────────────────────
    log.info("─── [3/3] 리포트 생성 ───")
    from report_agent import ReportAgent
    reporter = ReportAgent()
    report_path = reporter.run()
    if report_path:
        log.info(f"리포트 생성 완료: {report_path}")
        if not args.no_open:
            subprocess.Popen(["open", str(report_path)])
    else:
        log.error("리포트 생성 실패")

    # ── 완료 ───────────────────────────────────────────────────
    elapsed = (datetime.now(timezone.utc) - start).total_seconds()
    log.info(f"=== 완료 | 소요시간: {elapsed:.0f}초 ===")

    # 요약 출력
    if result:
        print("\n" + "="*60)
        print("📊 SSD × AI 수요 분석 요약")
        print("="*60)
        print(f"분석 포스트: {result['total_posts']:,}개")
        print(f"수요 신호:   {result['demand_total']:,}개 ({result['demand_rate_pct']}%)")
        sigs = result['demand_signals']
        print(f"  ▸ 구매 의향:    {sigs.get('buy_intent',0)}건")
        print(f"  ▸ 교체/확장:    {sigs.get('upgrade_intent',0)}건")
        print(f"  ▸ 기술적 필요:  {sigs.get('technical_need',0)}건")
        print(f"포터블 SSD:  {result.get('portable_ssd_mentions',0)}건 ({result.get('portable_ssd_pct',0)}%)")
        if result.get('technical_factors'):
            top = sorted(result['technical_factors'].items(), key=lambda x:-x[1])[:3]
            print(f"기술 근거 TOP3: {', '.join(f'{k}({v})' for k,v in top)}")
        if report_path:
            print(f"\n리포트: {report_path}")
        print("="*60)


if __name__ == "__main__":
    main()
