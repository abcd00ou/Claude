"""
update_all_reports.py — regenerate every analysis report from the current panel_long.

Runs the four analysis layers end-to-end and writes their reports/artifacts:
  1. value-chain lead-lag      -> reports/valuechain_leadlag_<date>.md + valuechain.html
  2. cash-flow variable-pairs  -> reports/cashflow_leadlag_<date>.md
  3. ECM mini-GEM              -> reports/ecm_minigem_<date>.md
(run_analysis.py handles the company/section lead-lag JSON separately.)

Run:  python3 update_all_reports.py [YYYY-MM-DD]
"""
from __future__ import annotations
import sys
from pathlib import Path

import panel as P
import valuechain as V
import cashflow_leadlag as C
import ecm as E

HERE = Path(__file__).parent
DATE = sys.argv[1] if len(sys.argv) > 1 else "2026-07-06"
CF_TICKERS = ["NVDA", "AMD", "MU", "INTC", "AMAT", "LRCX", "AMKR", "DELL", "AVGO", "STX"]


def main():
    (HERE / "reports").mkdir(exist_ok=True)
    long = P.load_long(P.DB_DEFAULT)
    print(f"panel_long: {long.shape}  ({long.ticker.nunique()} companies)")

    # 1) value chain
    vc = V.run_matrix(long)
    V.generate_md(vc, long, f"reports/valuechain_leadlag_{DATE}.md", date=DATE)
    V.generate_html(vc, "valuechain.html", date=DATE)
    ok = vc[vc.status == "ok"]
    print(f"[valuechain]  분석가능 {len(ok)}/{len(vc)} · 고객선행&유의 "
          f"{((ok.best_lag_q>0)&ok.significant).sum()}")

    # 2) cash flow
    internal = C.run_internal(long, CF_TICKERS)
    cross = C.run_cross(long)
    C.generate_md(internal, cross, f"reports/cashflow_leadlag_{DATE}.md", date=DATE)
    io, xo = internal[internal.status == "ok"], cross[cross.status == "ok"]
    print(f"[cashflow]    내부 가설지지 {((io.sign_match)&(io.significant)).sum()} · "
          f"기업간 가설지지 {((xo.sign_match)&(xo.significant)).sum()}")

    # 3) ECM mini-GEM
    E.generate_md(long, f"reports/ecm_minigem_{DATE}.md", date=DATE)
    ecm_rev = E.run_ecm(long, x_item="revenue", y_item="revenue")
    ecm_cap = E.run_ecm(long, x_item="capex", y_item="revenue")
    print(f"[ecm]         오차수정 rev={int((ecm_rev.error_correcting==True).sum())} · "
          f"capex={int((ecm_cap.error_correcting==True).sum())}")

    print(f"\nreports 갱신 완료 (date={DATE})")


if __name__ == "__main__":
    main()
