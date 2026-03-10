"""
Marketing Simulation Runner — 매 시간 실행 (launchd)
1회 실행 시:
  1. NAND 시장 실시간 데이터 수집 (web search)
  2. 시뮬레이션 1개월 전진 (시장 데이터 반영)
  3. 모든 에이전트 실행 (Excel + VP PPT 4종)
  4. 동적 이메일 리포트 전송 (abcd00ou@gmail.com)
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

    # ── 1. NAND 시장 실시간 데이터 수집 ─────────────────────────
    header("STEP 1 · NAND 시장 인텔리전스 수집")
    from market_intel import fetch_market_intel
    market_intel = run_agent("시장 데이터 수집", fetch_market_intel)
    if market_intel:
        mi = market_intel
        print(f"\n  📡 NAND 시그널  : {mi.get('nand_signal','?')}")
        print(f"  📈 가격 트렌드  : {mi.get('price_trend','?')}")
        print(f"  💹 가격 변화    : {mi.get('price_change_pct', 0):+.1f}%/월")
        context = mi.get("market_context", "")
        if context:
            print(f"  ℹ️  {context}")
    else:
        market_intel = None
        print("  ⚠️ 시장 데이터 수집 실패 — 기본값으로 진행")

    # ── 2. 시뮬레이션 1개월 전진 ────────────────────────────────
    header("STEP 2 · 시뮬레이션 월 전진")
    from simulation_engine import advance_month, get_current_state
    sim_data = run_agent("시뮬레이션 엔진",
                         lambda: advance_month(market_intel=market_intel))
    if sim_data is None:
        print("  ❌ 시뮬레이션 실패 — 종료")
        sys.exit(1)

    sim_date = sim_data.get("sim_date", "?")
    print(f"\n  📅 시뮬 날짜 : {sim_date}")
    print(f"  💰 총 월 매출: ${sim_data.get('total_rev_m', 0):.1f}M")
    print(f"  📊 GM%       : {sim_data.get('blended_gm_pct', 0):.1f}%")
    event = sim_data.get("event", {})
    if event.get("description"):
        print(f"  🎯 이벤트    : {event['description']}")

    results = {}

    # ── 3. 에이전트 실행 ─────────────────────────────────────────
    header("STEP 3 · 에이전트 실행")

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

    # ── 4. 이메일 전송 ────────────────────────────────────────────
    header("STEP 4 · 이메일 리포트 전송")
    from email_reporter import send_report
    from simulation_engine import get_current_state
    state = get_current_state()
    history = state.get("history", [])

    email_ok = send_report(
        sim_data=sim_data,
        agent_results=results,
        market_intel=market_intel,
        history=history,
    )

    # ── 결과 요약 ─────────────────────────────────────────────────
    header("📋 실행 요약")
    success = sum(1 for v in results.values() if v is not None)
    total = len(results)
    print(f"\n  시뮬 날짜  : {sim_date}")
    print(f"  NAND 시그널: {market_intel.get('nand_signal','N/A') if market_intel else 'N/A'}")
    print(f"  에이전트   : {success}/{total} 성공")
    print(f"  이메일     : {'✅ 전송 완료' if email_ok else '⚠️  전송 실패'}")

    from config import PPTX_DIR
    vp_pptx = list(PPTX_DIR.glob("*_vp.pptx"))
    if vp_pptx:
        print(f"\n  📁 VP PPT ({len(vp_pptx)}종):")
        for f in sorted(vp_pptx):
            print(f"    {f.name}  ({f.stat().st_size / 1024:.0f} KB)")

    print(f"\n  ✅ 완료 — {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()


if __name__ == "__main__":
    main()
