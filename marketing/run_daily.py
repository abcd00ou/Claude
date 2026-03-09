"""
Daily 오케스트레이터 — SanDisk B2C Storage Marketing Team
팀 리더(Claude)가 5개 에이전트를 순서대로 실행하여 일일 산출물 생성

VP급 PPT 빌더:
  - ppt_demand_forecast     : 수요예측 (10슬라이드)
  - ppt_marketing_strategy  : 마케팅 전략 (10슬라이드)
  - ppt_marcom              : 마케팅 커뮤니케이션 (10슬라이드)
  - ppt_product_mix         : 제품 믹스 전략 (10슬라이드, 이미지 + DB 가격 포함)
"""
import sys
import datetime
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

def header(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def run_agent(name, fn):
    print(f"\n▶ [{name}] 시작...")
    t0 = time.time()
    try:
        result = fn()
        elapsed = time.time() - t0
        print(f"  ✅ 완료 ({elapsed:.1f}s)")
        return result
    except Exception as e:
        print(f"  ❌ 오류: {e}")
        import traceback; traceback.print_exc()
        return None


def main():
    today = datetime.date.today()
    header(f"SanDisk B2C Marketing Team — Daily Run ({today})")
    print(f"""
  팀 구성:
  ┌─ 🏭 생산 에이전트         → production_simulation.xlsx
  ├─ 📦 공급 에이전트         → supply_plan.xlsx
  ├─ 📈 수요예측 에이전트      → demand_forecast.xlsx + demand_forecast_vp.pptx
  ├─ 💡 마케팅 전략 에이전트   → marketing_strategy.xlsx + marketing_strategy_vp.pptx
  ├─ 📢 마케팅 커뮤니케이션    → marcom_plan_vp.pptx
  └─ 🔢 제품 믹스 전략        → product_mix_vp.pptx (이미지 + DB 가격 포함)
    """)

    results = {}

    # ── 1. 생산 에이전트 ─────────────────────────────────────
    header("1/5 · 생산 에이전트 (Production Agent)")
    from agents.production_agent import build_excel as prod_excel
    results["production"] = run_agent("생산 에이전트", prod_excel)

    # ── 2. 공급 에이전트 ─────────────────────────────────────
    header("2/5 · 공급 에이전트 (Supply Agent)")
    from agents.supply_agent import build_excel as supply_excel
    results["supply"] = run_agent("공급 에이전트", supply_excel)

    # ── 3. 수요예측 에이전트 ─────────────────────────────────
    header("3/5 · 수요예측 에이전트 (Demand Forecast Agent)")
    from agents.demand_forecast_agent import build_excel as fc_excel
    results["demand_excel"] = run_agent("수요예측 에이전트 (Excel)", fc_excel)
    # VP급 PPT (ppt_demand_forecast.py)
    import ppt_demand_forecast
    results["demand_pptx_vp"] = run_agent("수요예측 VP PPT", ppt_demand_forecast.build)

    # ── 4. 마케팅 전략 에이전트 ──────────────────────────────
    header("4/5 · 마케팅 전략 에이전트 (Marketing Strategy Agent)")
    from agents.marketing_strategy_agent import build_excel as ms_excel
    results["strategy_excel"] = run_agent("마케팅 전략 에이전트 (Excel)", ms_excel)
    # VP급 PPT (ppt_marketing_strategy.py)
    import ppt_marketing_strategy
    results["strategy_pptx_vp"] = run_agent("마케팅 전략 VP PPT", ppt_marketing_strategy.build)

    # ── 5. 마케팅 커뮤니케이션 에이전트 ─────────────────────
    header("5/5 · 마케팅 커뮤니케이션 에이전트 (MarCom Agent)")
    import ppt_marcom
    results["marcom_pptx_vp"] = run_agent("마케팅 커뮤니케이션 VP PPT", ppt_marcom.build)

    # ── 6. 제품 믹스 전략 PPT (이미지 + DB 가격 포함) ────────
    header("6/6 · 제품 믹스 전략 (Product Mix VP PPT)")
    import ppt_product_mix
    results["product_mix_pptx_vp"] = run_agent("제품 믹스 VP PPT", ppt_product_mix.build)

    # ── 결과 요약 ────────────────────────────────────────────
    header("📋 Daily Run 완료 요약")
    success = sum(1 for v in results.values() if v is not None)
    total   = len(results)
    print(f"\n  성공: {success}/{total} 에이전트")
    print(f"\n  📁 산출물 위치:")

    from config import EXCEL_DIR, PPTX_DIR
    files = list(EXCEL_DIR.glob("*.xlsx")) + list(PPTX_DIR.glob("*.pptx"))
    for f in sorted(files):
        size_kb = f.stat().st_size / 1024
        print(f"    {f.relative_to(Path(__file__).parent)}  ({size_kb:.0f} KB)")

    print(f"\n  ✅ 모든 에이전트 실행 완료 — {today}")
    print()


if __name__ == "__main__":
    main()
