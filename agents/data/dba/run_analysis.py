"""
run_analysis.py — reproducible Lead-Lag pipeline on the REAL AI-value-chain panel.

Reads financials.db, builds a company x quarter panel, and emits the five scope
outputs (② sector phase, ③ lead-lag network, ④ CCC/operating-cycle congestion,
⑤ transmission gap, ⑥ blockage matrix) as JSON + a markdown report.

Run:  python3 run_analysis.py
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

import leadlag as ll
import panel as P                       # single data-access layer (panel_long)

HERE = Path(__file__).parent
DB = P.DB_DEFAULT

# --- Company panel: representative, well-covered nodes across the AI supply chain ---
# stage = qualitative upstream(low)->downstream(high) prior for the physical build-out.
PANEL = {
    # ticker : (display, sector-label, stage-prior)
    "MSFT": ("Microsoft",   "Hyperscaler", 0),   # capex origin (demand)
    "VRT":  ("Vertiv",      "Power",       1),
    "ETN":  ("Eaton",       "Power",       1),
    "MOD":  ("Modine",      "Cooling",     1),
    "AMAT": ("Applied Mat", "FabEquip",    2),
    "LRCX": ("Lam Research","FabEquip",    2),
    "NVDA": ("NVIDIA",      "AI Chip",     3),
    "AMD":  ("AMD",         "AI Chip",     3),
    "AVGO": ("Broadcom",    "AI Chip",     3),
    "MRVL": ("Marvell",     "AI Chip",     3),
    "MU":   ("Micron",      "DRAM",        4),
    "AMKR": ("Amkor",       "Packaging",   4),
    "ANET": ("Arista",      "Networking",  5),
    "SMCI": ("Super Micro", "Server OEM",  6),
    "DELL": ("Dell",        "Server OEM",  6),
}


def load_panel(db):
    """Wide-per-ticker frame [ticker, calendar_quarter, <items>] from panel_long."""
    items = ["revenue", "gross_profit", "inventory", "receivables", "capex"]
    long = P.load_long(db, tickers=list(PANEL), items=items)
    df = (long.pivot_table(index=["ticker", "quarter"], columns="item",
                           values="value", aggfunc="last")
              .reset_index().rename(columns={"quarter": "calendar_quarter"}))
    df["qkey"] = df["calendar_quarter"].map(P.qkey)
    df = df.sort_values(["ticker", "qkey"])
    df["cogs"] = df["revenue"] - df["gross_profit"]
    return df


def series_for(df, ticker, col):
    s = df[df.ticker == ticker].set_index("calendar_quarter")[col]
    return s[~s.index.duplicated()]


def main():
    df = load_panel(DB)

    # ---- revenue-YoY signal per company (the lead-lag backbone) ----
    signals, sectors, stage = {}, {}, {}
    for tk, (disp, sec, st) in PANEL.items():
        rev = series_for(df, tk, "revenue")
        if rev.dropna().shape[0] < 12:
            continue
        signals[disp] = ll.zscore(ll.yoy(rev))
        sectors[disp] = sec
        stage[disp] = st

    # ---- Output ③: lead-lag network ----
    net = ll.build_leadlag_network(signals, sectors, stage, max_lag=4, corr_floor=0.40)

    # ---- Company-level phase score (direct "who leads whom" per company) ----
    comp_phase = ll.sector_phase_order(signals, max_lag=4).rename(
        columns={"section": "company"})
    comp_phase["sector"] = comp_phase["company"].map(sectors)

    # ---- Output ②: sector phase order (aggregate revenue by sector, then YoY) ----
    sec_rev = {}
    for tk, (disp, sec, st) in PANEL.items():
        rev = series_for(df, tk, "revenue")
        if disp not in signals:
            continue
        sec_rev.setdefault(sec, []).append(rev)
    sector_signals = {}
    for sec, lst in sec_rev.items():
        agg = pd.concat(lst, axis=1).sum(axis=1, min_count=1)
        sector_signals[sec] = ll.zscore(ll.yoy(agg))
    phase = ll.sector_phase_order(sector_signals, max_lag=4)

    # ---- Output ④: working-capital congestion per company ----
    congestion, cong_details = {}, {}
    for tk, (disp, sec, st) in PANEL.items():
        wc = df[df.ticker == tk].set_index("calendar_quarter")[
            ["revenue", "cogs", "inventory", "receivables"]]
        summ, detail = ll.working_capital_congestion(wc, disp)
        congestion[disp] = summ
        cong_details[disp] = detail

    # ---- Output ⑤: transmission gap along the strongest downstream edges ----
    trans = []
    trans_by_down = {}
    for _, e in net.iterrows():
        up, down = e["from_leader"], e["to_follower"]
        lag = int(e["lead_quarters"])
        r = ll.transmission_gap(signals[up], signals[down], lag, up, down)
        trans.append(r)
        # keep the most upstream-anchored break signal per downstream node
        if r.get("transmission_block"):
            trans_by_down[down] = r
        trans_by_down.setdefault(down, r)

    # ---- Output ⑥: blockage matrix ----
    matrix = []
    for tk, (disp, sec, st) in PANEL.items():
        if disp not in congestion:
            continue
        matrix.append(ll.blockage_matrix(congestion[disp], trans_by_down.get(disp)))

    # ---- persist ----
    out = {
        "panel": {v[0]: {"ticker": k, "sector": v[1]} for k, v in PANEL.items()},
        "company_phase": comp_phase.to_dict(orient="records"),
        "output2_sector_phase": phase.to_dict(orient="records"),
        "output3_leadlag_network": net.to_dict(orient="records"),
        "output4_congestion": [c for c in congestion.values()],
        "output5_transmission": trans,
        "output6_blockage_matrix": matrix,
    }
    (HERE / "leadlag_results.json").write_text(json.dumps(out, indent=2, default=str))
    _write_md(comp_phase, phase, net, congestion, trans, matrix,
              HERE / "reports" / "company_section_leadlag_2026-07-06.md")

    # ---- console summary ----
    pd.set_option("display.width", 160, "display.max_columns", 20)
    print("\n===== COMPANY PHASE (leads = upstream/negative, lags = downstream/positive) =====")
    print(comp_phase[["company", "sector", "phase_score", "rank"]].to_string(index=False))
    print("\n===== OUTPUT ② SECTOR PHASE ORDER (upstream -> downstream) =====")
    print(phase.to_string(index=False))
    print("\n===== OUTPUT ③ LEAD-LAG NETWORK (top edges) =====")
    show = net[["from_leader", "to_follower", "lead_quarters", "peak_corr",
                "granger_p_fwd", "score"]].head(20)
    print(show.to_string(index=False))
    print("\n===== OUTPUT ④ WORKING-CAPITAL CONGESTION (OC = DIO+DSO; no DPO in DB) =====")
    cdf = pd.DataFrame([c for c in congestion.values()])
    print(cdf.to_string(index=False))
    print("\n===== OUTPUT ⑤ TRANSMISSION GAP =====")
    print(pd.DataFrame(trans).to_string(index=False))
    print("\n===== OUTPUT ⑥ INTEGRATED BLOCKAGE MATRIX =====")
    print(pd.DataFrame(matrix).to_string(index=False))
    print("\n[written] leadlag_results.json")


def _df_md(df, cols=None):
    d = df[cols] if cols else df
    head = "| " + " | ".join(map(str, d.columns)) + " |"
    sep = "|" + "---|" * len(d.columns)
    rows = ["| " + " | ".join(str(v) for v in r) + " |" for r in d.itertuples(index=False)]
    return "\n".join([head, sep, *rows])


def _write_md(comp_phase, phase, net, congestion, trans, matrix, path):
    import pandas as pd
    Path(path).parent.mkdir(exist_ok=True)
    L = ["# 기업·섹션 Lead-Lag 분석 (기업/섹션 위상 · 네트워크 · 병목)\n",
         "**분석일:** 2026-07-06 · **데이터:** `panel_long` · **엔진:** `run_analysis.py` + `leadlag.py`\n",
         "매출 YoY(z-score) 시차상관 기반. phase_score 음수=상류(선행), 양수=하류(후행).\n",
         "\n## 1. 기업 위상 (선행 ↔ 후행)\n",
         _df_md(comp_phase.round(3), ["company", "sector", "phase_score", "rank"]),
         "\n## 2. 섹션 위상 순서\n", _df_md(phase.round(3)),
         "\n## 3. Lead-Lag 네트워크 (상위 엣지)\n",
         _df_md(net.round(3).head(15), ["from_leader", "to_follower", "lead_quarters",
                                        "peak_corr", "granger_p_fwd", "score"]),
         "\n## 4. 운전자본 병목 (OC=DIO+DSO)\n",
         _df_md(pd.DataFrame([c for c in congestion.values()])),
         "\n## 5. 통합 병목 매트릭스\n", _df_md(pd.DataFrame(matrix)),
         "\n## 6. 한계\n- 표본 ~40분기, 상관 1차·Granger 2차. 섹션 위상은 구성사 얇으면 노이즈.\n"]
    Path(path).write_text("\n".join(L))


if __name__ == "__main__":
    main()
