"""
valuechain.py — customer→supplier lead-lag engine over the AI value chain.

Analysis-only layer: it reads the already-preprocessed `panel_long` table (via
panel.py) and derives everything it needs (section aggregates, YoY, cogs, ...)
INSIDE the analysis functions. It never rebuilds or writes the panel — that is
build_panel_long.py's job.

Given the user's [customer] → [supplier] relationships, for each edge we test the
hypothesis "the customer's activity LEADS the supplier's revenue" by lagged
cross-correlation + Granger causality on section-aggregate signals.

Public API (used by valuechain_playground.ipynb):
    SECTIONS, RELATIONSHIPS
    section_members(section)            -> tickers used for the aggregate
    section_signal(long, section, item) -> (signal, raw, members)
    analyze_edge(long, cust, supp, x_item, y_item)     -> dict (one edge)
    run_matrix(long, var_pairs)         -> DataFrame (all edges × variable views)
    generate_md(results, path)          -> markdown report
    generate_html(results, path)        -> mermaid value-chain diagram
"""
from __future__ import annotations
from pathlib import Path

import numpy as np
import pandas as pd

import leadlag as ll
import panel as P

HERE = Path(__file__).parent
MIN_QUARTERS = 12          # a company must have >=12 quarters to join a section aggregate

# section slug -> display label
SECTIONS = {
    "hyperscalers": "Hyperscaler",
    "ai_chip": "AI Chip",
    "cpu": "CPU",
    "dram": "DRAM",
    "nand": "NAND",
    "foundry": "Foundry",
    "hw_equipment": "HW Equipment",
    "osat_packaging": "OSAT/Packaging",
    "server_networking": "Server Networking",
    "server_oem": "Server OEM",
    "server_odm": "Server ODM",
}

# [customer] -> [supplier]  (customer buys from supplier; demand/cash starts at customer)
# 사용자 정의 섹터간 고객-공급사 흐름 (2026-07-07 업데이트: oem->dram 추가).
RELATIONSHIPS = [
    ("hyperscalers", "ai_chip"),
    ("server_oem", "ai_chip"),
    ("server_oem", "cpu"),
    ("hyperscalers", "cpu"),
    ("ai_chip", "dram"),
    ("hyperscalers", "dram"),
    ("server_oem", "dram"),
    ("hyperscalers", "nand"),
    ("server_oem", "nand"),
    ("ai_chip", "nand"),
    ("foundry", "hw_equipment"),
    ("dram", "hw_equipment"),
    ("cpu", "hw_equipment"),
    ("ai_chip", "osat_packaging"),
    ("cpu", "osat_packaging"),
    ("hyperscalers", "server_networking"),
    ("server_oem", "server_networking"),
    ("ai_chip", "foundry"),
    ("cpu", "foundry"),
    ("server_networking", "foundry"),
    ("cpu", "server_odm"),
    ("dram", "server_odm"),
    ("nand", "server_odm"),
    ("ai_chip", "server_odm"),
]

# variable views for the "cash-flow" matrix: (customer_item, supplier_item, label)
DEFAULT_VAR_PAIRS = [
    ("revenue", "revenue", "매출→매출 (수요전달)"),
    ("cogs", "revenue", "매출원가→매출 (구매흐름)"),
    ("capex", "revenue", "capex→매출 (투자흐름)"),
]


# --------------------------------------------------------------------------- #
def _corr_p(r, n):
    """Two-sided p-value for Pearson r (t^2 ~ F(1,n-2)); numpy-only via leadlag._f_sf."""
    if n < 4 or abs(r) >= 1:
        return np.nan
    t2 = (r * r) * (n - 2) / (1 - r * r)
    return ll._f_sf(t2, 1, n - 2)


def section_members(long, section, item="revenue", min_q=MIN_QUARTERS):
    """Tickers in `section` with enough coverage of `item` to join the aggregate."""
    need = list(P.DERIVED_ITEMS[item]) if item in P.DERIVED_ITEMS else [item]
    d = long[(long.section == section) & (long.item.isin(need))]
    if d.empty:
        return []
    # for derived items, require every component present
    cov = d.groupby("ticker")["quarter"].nunique()
    return sorted(cov[cov >= min_q].index)


def section_signal(long, section, item="revenue", transform="yoy_z", min_q=MIN_QUARTERS):
    """
    Aggregate a section into one quarterly signal: sum of member companies' `item`,
    then transform. Returns (signal, raw_sum, members). signal is None if no member
    has >= min_q quarters (e.g. foundry, server_odm in this DB).
    """
    members = section_members(long, section, item, min_q)
    if not members:
        return None, None, []
    cols = {tk: P.get_series(long, tk, item) for tk in members}
    raw = pd.DataFrame(cols).sum(axis=1, min_count=1).dropna()
    raw = raw.loc[sorted(raw.index, key=P.qkey)]
    if transform == "level_z":
        sig = ll.zscore(raw)
    elif transform == "yoy":
        sig = ll.yoy(raw)
    else:
        sig = ll.zscore(ll.yoy(raw))
    return sig, raw, members


# --------------------------------------------------------------------------- #
def analyze_edge(long, cust, supp, x_item="revenue", y_item="revenue",
                 max_lag=4, transform="yoy_z"):
    """
    One customer->supplier edge. X = customer(x_item), Y = supplier(y_item).
    Hypothesis: customer LEADS supplier (best_lag > 0).
    """
    base = dict(customer=cust, supplier=supp,
                customer_label=SECTIONS.get(cust, cust), supplier_label=SECTIONS.get(supp, supp),
                x_item=x_item, y_item=y_item)
    sx, _, mem_x = section_signal(long, cust, x_item, transform)
    sy, _, mem_y = section_signal(long, supp, y_item, transform)
    if sx is None or sy is None:
        miss = cust if sx is None else supp
        return {**base, "status": "insufficient data",
                "note": f"{SECTIONS.get(miss, miss)} 데이터 부족(<{MIN_QUARTERS}분기)",
                "n": 0, "members_x": mem_x, "members_y": mem_y}

    lag, corr, _ = ll.lagged_xcorr(sx, sy, max_lag)     # signed positive peak
    if np.isnan(corr):
        return {**base, "status": "no signal", "n": 0,
                "note": "양(+)의 상관 피크 없음", "members_x": mem_x, "members_y": mem_y}
    n = len(pd.concat([sx, sy.shift(-lag)], axis=1).dropna())
    p = _corr_p(corr, n)

    lg = max(1, min(abs(lag), 2))
    g_c2s = ll.granger_p(sx, sy, lag=lg)   # customer -> supplier
    g_s2c = ll.granger_p(sy, sx, lag=lg)   # supplier -> customer

    # transmission (leader -> follower)
    if lag >= 0:
        up, down, lead = sx, sy, lag
    else:
        up, down, lead = sy, sx, -lag
    reg = pd.concat({"down": down, "up": up.shift(lead)}, axis=1).dropna()
    beta = r2 = np.nan
    if len(reg) >= 6:
        Xm = np.hstack([np.ones((len(reg), 1)), reg[["up"]].to_numpy()])
        b, *_ = np.linalg.lstsq(Xm, reg["down"].to_numpy(), rcond=None)
        beta = float(b[1])
        pred = Xm @ b
        sst = float(((reg["down"] - reg["down"].mean()) ** 2).sum())
        r2 = 1 - float(((reg["down"].to_numpy() - pred) ** 2).sum()) / sst if sst > 0 else np.nan

    sig5 = (not np.isnan(p)) and p < 0.05
    if lag > 0:
        verdict = "고객 선행 (가설지지)" if sig5 else "고객 선행(약함)"
    elif lag < 0:
        verdict = "공급사 선행 (역방향)" if sig5 else "공급사 선행(약함)"
    else:
        verdict = "동시(리드 없음)"

    return {**base, "status": "ok",
            "best_lag_q": lag, "leader": base["customer_label"] if lag > 0 else
            (base["supplier_label"] if lag < 0 else "—"),
            "corr": round(corr, 3), "p_value": round(p, 4) if not np.isnan(p) else None,
            "granger_c2s_p": None if np.isnan(g_c2s) else round(g_c2s, 4),
            "granger_s2c_p": None if np.isnan(g_s2c) else round(g_s2c, 4),
            "beta": None if np.isnan(beta) else round(beta, 3),
            "r2": None if np.isnan(r2) else round(r2, 3),
            "n": n, "significant": sig5, "verdict": verdict,
            "members_x": mem_x, "members_y": mem_y}


def run_matrix(long, var_pairs=DEFAULT_VAR_PAIRS, relationships=RELATIONSHIPS,
               max_lag=4, transform="yoy_z"):
    """All edges × all variable views -> tidy DataFrame."""
    rows = []
    for x_item, y_item, view in var_pairs:
        for cust, supp in relationships:
            r = analyze_edge(long, cust, supp, x_item, y_item, max_lag, transform)
            r["view"] = view
            rows.append(r)
    cols = ["view", "customer_label", "supplier_label", "x_item", "y_item", "status",
            "best_lag_q", "leader", "corr", "p_value", "granger_c2s_p", "granger_s2c_p",
            "beta", "r2", "n", "significant", "verdict", "note"]
    df = pd.DataFrame(rows)
    return df[[c for c in cols if c in df.columns]]


# --------------------------------------------------------------------------- #
def generate_md(df, long, path, date="2026-07-06"):
    """Write the markdown analysis report."""
    L = []
    L.append("# AI 밸류체인 고객→공급사 Lead-Lag 분석 (현금흐름 관점)\n")
    L.append(f"**분석일:** {date}  ·  **데이터:** `panel_long` (분기 재무, 2016–2027)  "
             f"·  **엔진:** `valuechain.py` + `leadlag.py`\n")
    L.append("**방법:** 섹션 집계 신호(구성사 매출 합)의 YoY를 z-score → 시차상관(±4분기) + "
             "Granger 인과. 가설: **고객(customer)의 활동이 공급사(supplier) 매출을 선행**한다.\n")

    ok = df[df.status == "ok"]
    L.append("## 0. 요약\n")
    lead_ok = ok[(ok.best_lag_q > 0) & ok.significant]
    L.append(f"- 분석 대상 엣지: **{len(RELATIONSHIPS)}개** × 재무관점 **{df.view.nunique()}종** "
             f"= {len(df)} 케이스\n")
    L.append(f"- 데이터 부족(foundry·ODM 등)으로 분석 불가: **{df[df.status!='ok'].shape[0]} 케이스**\n")
    L.append(f"- '고객 선행' 가설이 통계적으로 지지된 케이스(유의, lead>0): **{len(lead_ok)}건**\n")

    # section coverage
    L.append("\n## 1. 섹션 구성 (집계에 쓰인 회사)\n")
    L.append("| 섹션 | 집계 회사 | 상태 |\n|---|---|---|")
    for slug, label in SECTIONS.items():
        mem = section_members(long, slug, "revenue")
        state = "✅" if mem else "⚠️ 데이터 부족"
        L.append(f"| {label} | {', '.join(mem) if mem else '—'} | {state} |")

    # per-view tables
    for view in df.view.unique():
        sub = df[df.view == view]
        xi = sub.x_item.iloc[0]; yi = sub.y_item.iloc[0]
        L.append(f"\n## 2. 관점: {view}  (`{xi}`→`{yi}`)\n")
        L.append("| 고객(X) | 공급사(Y) | best lag(분기) | 리더 | corr | p | Granger C→S | β | 판정 |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for _, r in sub.iterrows():
            if r.status != "ok":
                L.append(f"| {r.customer_label} | {r.supplier_label} | — | — | — | — | — | — | "
                         f"{r.get('note','데이터 부족')} |")
                continue
            star = "**" if r.significant else ""
            L.append(f"| {r.customer_label} | {r.supplier_label} | {star}{int(r.best_lag_q):+d}{star} | "
                     f"{r.leader} | {r['corr']} | {r.p_value} | {r.granger_c2s_p} | {r.beta} | {r.verdict} |")

    L.append("\n## 3. 해석 가이드\n")
    L.append("- **best lag > 0** ⇒ 고객이 공급사를 그만큼 분기 선행 (수요가 먼저 → 매출로 전달).\n")
    L.append("- **p < 0.05** ⇒ 해당 시차의 상관이 통계적으로 유의.\n")
    L.append("- **Granger C→S < 0.05 이고 < S→C** ⇒ 인과 방향이 고객→공급사로 확인.\n")
    L.append("- **β** = 전달 강도(고객 1σ 변화가 공급사에 전달되는 비율).\n")
    L.append("\n## 4. 한계\n")
    L.append("- Foundry(TSM 등)·Server ODM(대만 ODM)은 이 DB에서 12분기 미만 → 신호 생성 불가, "
             "해당 엣지 전부 '데이터 부족'.\n")
    L.append("- 섹션당 대표사가 1개인 경우(cpu=INTC, dram=MU, osat=AMKR) 집계=단일사.\n")
    L.append("- 지급어음(payables) 컬럼이 없어 순수 현금전환주기는 다루지 않음(별도 리포트 참조).\n")
    L.append("- lead-lag는 통계적 선행일 뿐 계약관계 증명이 아님 → 상위 후보는 SPLC/10-K로 교차검증.\n")
    Path(path).write_text("\n".join(L))
    return path


def generate_html(df, path, view=None, date="2026-07-06"):
    """Value-chain diagram (mermaid). Uses one variable view (default: first)."""
    view = view or df.view.iloc[0]
    sub = df[df.view == view]
    edges = []
    for _, r in sub.iterrows():
        c, s = r.customer_label, r.supplier_label
        if r.status != "ok":
            edges.append(f'  {_nid(c)}["{c}"] -.->|"데이터부족"| {_nid(s)}["{s}"]')
            continue
        lead = int(r.best_lag_q)
        lbl = f"lead {lead:+d}q, r={r['corr']}"
        arrow = "==>" if r.significant and lead > 0 else ("-->" if lead != 0 else "-.->")
        edges.append(f'  {_nid(c)}["{c}"] {arrow}|"{lbl}"| {_nid(s)}["{s}"]')
    mer = "flowchart LR\n" + "\n".join(edges)

    rows = []
    for _, r in sub.iterrows():
        if r.status != "ok":
            rows.append(f"<tr><td>{r.customer_label}</td><td>{r.supplier_label}</td>"
                        f"<td colspan=5 class='na'>데이터 부족</td></tr>")
        else:
            cls = "sig" if r.significant else ""
            rows.append(f"<tr class='{cls}'><td>{r.customer_label}</td><td>{r.supplier_label}</td>"
                        f"<td>{int(r.best_lag_q):+d}</td><td>{r['corr']}</td><td>{r.p_value}</td>"
                        f"<td>{r.granger_c2s_p}</td><td>{r.verdict}</td></tr>")
    table = "\n".join(rows)

    html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>AI 밸류체인 Lead-Lag</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
 body{{font-family:-apple-system,Segoe UI,Roboto,'Malgun Gothic',sans-serif;margin:32px;color:#1a1a1a}}
 h1{{font-size:22px}} .sub{{color:#666;margin-bottom:20px}}
 .legend span{{margin-right:16px;font-size:13px}}
 .mermaid{{background:#fafafa;border:1px solid #eee;border-radius:8px;padding:16px;margin:16px 0}}
 table{{border-collapse:collapse;width:100%;font-size:13px}}
 th,td{{border:1px solid #e5e5e5;padding:6px 8px;text-align:center}}
 th{{background:#f4f4f4}} tr.sig{{background:#eefbf0}} td.na{{color:#b58900}}
 caption{{text-align:left;font-weight:600;margin:8px 0}}
</style></head><body>
<h1>AI 밸류체인 고객→공급사 Lead-Lag</h1>
<div class="sub">관점: <b>{view}</b> · 분석일 {date} · 굵은 화살표(==) = 고객 선행 & 유의 · 점선 = 데이터부족</div>
<div class="legend">
 <span>➡️ <b>==&gt;</b> 고객 선행(유의)</span>
 <span>→ 약한/역방향</span>
 <span>⋯ 데이터 부족</span>
</div>
<div class="mermaid">
{mer}
</div>
<table>
<caption>엣지별 결과 ({view})</caption>
<tr><th>고객(X)</th><th>공급사(Y)</th><th>best lag(분기)</th><th>corr</th><th>p</th><th>Granger C→S</th><th>판정</th></tr>
{table}
</table>
<script>mermaid.initialize({{startOnLoad:true,flowchart:{{curve:'basis'}}}});</script>
</body></html>"""
    Path(path).write_text(html)
    return path


def _nid(label):
    return "n_" + label.replace(" ", "").replace("/", "").replace("-", "")


# --------------------------------------------------------------------------- #
def plot_edge(long, cust, supp, x_item="revenue", y_item="revenue",
              max_lag=4, transform="yoy_z", figsize=(13, 4.5)):
    """Inline-friendly 2-panel view of one customer->supplier edge (for the notebook)."""
    import matplotlib.pyplot as plt
    sx, _, mem_x = section_signal(long, cust, x_item, transform)
    sy, _, mem_y = section_signal(long, supp, y_item, transform)
    cl, sl = SECTIONS.get(cust, cust), SECTIONS.get(supp, supp)
    if sx is None or sy is None:
        raise ValueError(f"신호 생성 불가: {cl if sx is None else sl} 데이터 부족")

    lag, corr, tbl = ll.lagged_xcorr(sx, sy, max_lag)
    e = analyze_edge(long, cust, supp, x_item, y_item, max_lag, transform)

    fig, ax = plt.subplots(1, 2, figsize=figsize)
    fig.suptitle(f"{cl}·{x_item}  →  {sl}·{y_item}   |   {e['verdict']} "
                 f"(lag {int(lag):+d}q, r={corr:.2f}, p={e.get('p_value')})",
                 fontsize=11, fontweight="bold")
    a = ax[0]
    a.plot(sx.index, sx.values, "-o", ms=3, color="#1f77b4", label=f"고객: {cl}")
    a.plot(sy.index, sy.values, "-o", ms=3, color="#d62728", label=f"공급사: {sl}")
    a.axhline(0, color="grey", lw=.6); a.legend(fontsize=8); a.set_ylabel("z-score(YoY)")
    a.set_title("(1) 섹션 집계 신호"); [l.set_visible(i % 3 == 0) for i, l in enumerate(a.get_xticklabels())]
    a.tick_params(axis="x", rotation=90, labelsize=7)
    b = ax[1]
    t = tbl.dropna(subset=["corr"])
    colors = ["#2ca02c" if k == lag else "#9ecae1" for k in t["lag"]]
    b.bar(t["lag"], t["corr"], color=colors); b.axhline(0, color="grey", lw=.6)
    b.axvline(lag, color="#2ca02c", ls="--", lw=1)
    b.set_title("(2) 시차상관 (k>0 ⇒ 고객 선행)"); b.set_xlabel("lag k (분기)"); b.set_ylabel("corr")
    for _, r in t.iterrows():
        b.text(r["lag"], r["corr"] + (.02 if r["corr"] >= 0 else -.06), f"{r['corr']:.2f}",
               ha="center", fontsize=7)
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    return fig
