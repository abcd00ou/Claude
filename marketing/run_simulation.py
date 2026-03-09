"""
Marketing Simulation Runner — 매 시간 실행 (launchd)
1회 실행 시:
  1. 시뮬레이션 1개월 전진 (더미 데이터 생성)
  2. 모든 에이전트 실행 (Excel + PPT 4종)
  3. 이메일 리포트 전송 (abcd00ou@gmail.com)

launchd가 1시간마다 이 스크립트를 실행함.
"""
import sys
import time
import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def header(title: str):
    print("\n" + "=" * 65)
    print(f"  {title}")
    print("=" * 65)


def run_agent(name: str, fn):
    print(f"\n▶ [{name}] 시작...")
    t0 = time.time()
    try:
        result = fn()
        elapsed = time.time() - t0
        print(f"  ✅ 완료 ({elapsed:.1f}s)")
        return result
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback
        traceback.print_exc()
        return None


def main():
    now = datetime.datetime.now()
    header(f"SanDisk Marketing Simulation — {now.strftime('%Y-%m-%d %H:%M')}")

    # ── 1. 시뮬레이션 1개월 전진 ────────────────────────────────
    header("STEP 1 · 시뮬레이션 월 전진")
    from simulation_engine import advance_month
    sim_data = run_agent("시뮬레이션 엔진", advance_month)
    if sim_data is None:
        print("  ❌ 시뮬레이션 실패 — 종료")
        sys.exit(1)

    sim_date = sim_data.get("sim_date", "?")
    print(f"\n  📅 시뮬 날짜: {sim_date}")
    print(f"  💰 총 월 매출: ${sim_data.get('total_rev_m', 0):.1f}M")
    print(f"  📊 GM%: {sim_data.get('blended_gm_pct', 0):.1f}%")

    event = sim_data.get("event", {})
    if event.get("description"):
        print(f"  🎯 이벤트: {event['description']}")

    results = {}

    # ── 2. 에이전트 실행 ─────────────────────────────────────────
    header("STEP 2 · 에이전트 실행")

    from agents.production_agent import build_excel as prod_excel
    results["production"] = run_agent("생산 에이전트", prod_excel)

    from agents.supply_agent import build_excel as supply_excel
    results["supply"] = run_agent("공급 에이전트", supply_excel)

    from agents.demand_forecast_agent import build_excel as fc_excel
    results["demand_excel"] = run_agent("수요예측 (Excel)", fc_excel)

    import ppt_demand_forecast
    results["demand_pptx_vp"] = run_agent("수요예측 VP PPT", ppt_demand_forecast.build)

    from agents.marketing_strategy_agent import build_excel as ms_excel
    results["strategy_excel"] = run_agent("마케팅 전략 (Excel)", ms_excel)

    import ppt_marketing_strategy
    results["strategy_pptx_vp"] = run_agent("마케팅 전략 VP PPT", ppt_marketing_strategy.build)

    import ppt_marcom
    results["marcom_pptx_vp"] = run_agent("MarCom VP PPT", ppt_marcom.build)

    import ppt_product_mix
    results["product_mix_pptx_vp"] = run_agent("Product Mix VP PPT", ppt_product_mix.build)

    # ── 3. 이메일 전송 ────────────────────────────────────────────
    header("STEP 3 · 이메일 리포트 전송")
    from email_reporter import send_report
    email_ok = send_report(sim_data, results)

    # ── 결과 요약 ─────────────────────────────────────────────────
    header("📋 실행 요약")
    success = sum(1 for v in results.values() if v is not None)
    total = len(results)
    print(f"\n  시뮬 날짜 : {sim_date}")
    print(f"  에이전트  : {success}/{total} 성공")
    print(f"  이메일    : {'✅ 전송 완료' if email_ok else '⚠️  전송 실패 (환경변수 확인)'}")

    from config import PPTX_DIR
    pptx_files = list(PPTX_DIR.glob("*.pptx"))
    if pptx_files:
        print(f"\n  📁 PPT 산출물:")
        for f in sorted(pptx_files):
            print(f"    {f.name}  ({f.stat().st_size / 1024:.0f} KB)")

    print(f"\n  ✅ 완료 — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()


if __name__ == "__main__":
    main()
