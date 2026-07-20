"""
update_all_reports.py — 모든 분석의 리포트+HTML을 고정 이름으로 재생성 (overwrite).

CSV(panel_long.csv) 하나에서 시작해 전 분석을 돌리고, 결과를 날짜 없는 고정 파일명으로
덮어쓴다(같은 내용이면 계속 overwrite). run_analysis(기업/섹션)는 자체 main으로 처리.

Run:  python3 update_all_reports.py
"""
from __future__ import annotations
from pathlib import Path

import panel as P
import valuechain as V
import cashflow_leadlag as C
import cashflow_map as CM
import pairwise_cashflow as PW
import ecm as E
import universal as U
import vecm as VE
import accounting_leadlag as AC
import run_analysis as RA

HERE = Path(__file__).parent
DATE = "2026-07-09"
CF_TICKERS = ["NVDA", "AMD", "MU", "INTC", "AMAT", "LRCX", "AMKR", "DELL", "AVGO", "STX"]


def R(name):
    return str(HERE / "reports" / name)


def main():
    (HERE / "reports").mkdir(exist_ok=True)
    long = P.load_long()
    print(f"panel_long.csv: {long.shape} ({long.ticker.nunique()} companies, {long.item.nunique()} items)")

    # 0) 기업·섹션 lead-lag (자체 main → company_section_leadlag.md, JSON)
    RA.main()

    # 1) 밸류체인 lead-lag
    vc = V.run_matrix(long)
    V.generate_md(vc, long, R("valuechain_leadlag.md"), date=DATE)
    V.generate_html(vc, str(HERE / "valuechain.html"), date=DATE)

    # 2) 현금흐름 변수쌍 (내부/기업간)
    internal = C.run_internal(long, CF_TICKERS)
    cross = C.run_cross(long)
    C.generate_md(internal, cross, R("cashflow_leadlag.md"), date=DATE)

    # 3) ECM 2변수 (섹터 매출)
    E.generate_md(long, R("ecm_minigem.md"), date=DATE)

    # 4) 현금흐름 시차 맵 (자동선택 + AP 고정 + 채널 전체)
    auto = CM.run_map(long)
    CM.generate_md(auto, R("cashflow_map.md"), date=DATE)
    CM.generate_html(auto, str(HERE / "cashflow_map.html"), date=DATE)
    ap = CM.run_map(long, channel=("AP_GROWTH_QOQ", "REVENUE_GROWTH_QOQ"))
    CM.generate_md(ap, R("cashflow_map_AP.md"), date=DATE)
    CM.generate_html(ap, str(HERE / "cashflow_map_AP.html"), date=DATE)
    CM.generate_channels_report(long, R("cashflow_channels.md"), date=DATE)

    # 5) 기업간 상관가중 매출합
    cw, contribs = PW.run_corrweighted_map(long)
    PW.generate_corrweighted_md(cw, contribs, R("cashflow_corrweighted.md"),
                                x="AP_GROWTH_YOY", y="REVENUE_GROWTH_YOY", date=DATE)

    # 6) 보편관계
    udf, _ = U.find_universal(long)
    udf.to_csv(HERE / "universal_channels.csv", index=False)
    U.generate_md(udf, R("universal_relations.md"), date=DATE)
    U.generate_html(udf, str(HERE / "universal.html"), date=DATE)

    # 7) VECM mini-GEM
    eqs, exog, _ = VE.build_system(long)
    VE.generate_md(eqs, exog, long, R("vecm_minigem.md"), date=DATE)
    VE.generate_html(eqs, exog, long, str(HERE / "vecm.html"), date=DATE)

    # 8) 논문 산출물: 회계 lead-lag(a) + 시뮬레이터(c)  [이론/매뉴얼은 정적 md]
    ac = AC.run_hypotheses(long)
    AC.generate_md(ac, long, R("accounting_leadlag.md"), date=DATE)
    AC.generate_html(ac, str(HERE / "accounting_leadlag.html"), date=DATE)
    # 기업(쌍)별 상세 통계 검증 (부록)
    det = AC.run_detail(long)
    det.to_csv(HERE / "accounting_leadlag_detail.csv", index=False)
    AC.generate_detail_html(det, str(HERE / "accounting_leadlag_detail.html"), date=DATE)
    VE.generate_simulator_html(eqs, exog, long, str(HERE / "simulator.html"), date=DATE)

    print("\n[완료] 모든 리포트·HTML 고정 이름으로 overwrite:")
    print("  reports/*.md (company_section, valuechain, cashflow_leadlag, ecm_minigem,")
    print("               cashflow_map[_AP], cashflow_channels, cashflow_corrweighted,")
    print("               universal_relations, vecm_minigem)")
    print("  *.html (valuechain, cashflow_map[_AP], universal, vecm)")


if __name__ == "__main__":
    main()
