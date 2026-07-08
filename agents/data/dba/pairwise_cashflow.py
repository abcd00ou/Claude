"""
pairwise_cashflow.py — 단일 기업간(bottom-up) 현금흐름 lead-lag + 가중 종합.

섹터 집계(top-down)는 실제 거래관계(예: MSFT가 NVDA에서 구매)를 뭉갠다. 여기서는
고객 섹터의 각 기업 × 공급사 섹터의 각 기업 쌍마다 lead-lag를 구하고, 이를 가중치로
종합해 섹터 엣지의 대표 시차를 만든다.

  기업쌍       고객사 X → 공급사 Y (예: MSFT AP_GROWTH → NVDA REVENUE_GROWTH)
  가중 종합    유의한 쌍들을 가중평균 → 섹터 엣지 시차/상관
               weight ∈ {'equal','corr','size','composite'}  (조정 가능)
                 equal     동일 가중
                 corr      |상관| (관계 강도)
                 size      공급사 매출 규모 (큰 거래 중시)
                 composite |상관| × log(size)  [기본]

reuse: features.get_feature(기업 지표) · cashflow_leadlag.lead_lag_scan · cashflow_map.CASH_DRIVERS.
"""
from __future__ import annotations
from pathlib import Path

import numpy as np
import pandas as pd

import panel as P
import features as F
import valuechain as V
import cashflow_leadlag as C
import cashflow_map as CM

HERE = Path(__file__).parent
MIN_N = 10          # 기업쌍 최소 겹치는 분기
MIN_Q = 16          # 섹터 멤버 최소 커버리지


# --------------------------------------------------------------------------- #
def members(long, section, feat="REVENUE_GROWTH_QOQ", min_q=MIN_Q):
    d = long[long.section == section]
    out = []
    for tk in d.ticker.unique():
        if F.get_feature(long, tk, feat, "auto").dropna().shape[0] >= min_q:
            out.append(tk)
    return out


def company_size(long, ticker):
    """가중치용 규모 프록시 = 평균 매출(USD m)."""
    s = P.get_series(long, ticker, "revenue")
    return float(s.mean()) if len(s) else np.nan


def pair_leadlag(long, ct, st, xf, xtf, yf, ytf, lags=(0, 4)):
    """기업쌍 하나의 채널 lead-lag."""
    sx = F.get_feature(long, ct, xf, xtf)
    sy = F.get_feature(long, st, yf, ytf)
    if sx.dropna().empty or sy.dropna().empty:
        return None
    r = C.lead_lag_scan(sx, sy, lags, expected="+")
    return r if r.get("status") == "ok" and r["n"] >= MIN_N else None


def _weight(r, size_supp, mode):
    if mode == "equal":
        return 1.0
    if mode == "corr":
        return abs(r["pearson"])
    if mode == "size":
        return np.log1p(size_supp) if size_supp and size_supp > 0 else 0.0
    # composite
    return abs(r["pearson"]) * (np.log1p(size_supp) if size_supp and size_supp > 0 else 1.0)


# --------------------------------------------------------------------------- #
def pair_detail(long, cust, supp, channel, lags=(0, 4)):
    """섹터 엣지 하나의 모든 기업쌍 상세 (검토용): 어떤 기업쌍이 몇 분기인지."""
    xf, xtf, yf, ytf = _resolve(channel)
    cs, ss = members(long, cust), members(long, supp)
    rows = []
    for ct in cs:
        for st in ss:
            if ct == st:
                continue
            r = pair_leadlag(long, ct, st, xf, xtf, yf, ytf, lags)
            if r is None:
                continue
            rows.append(dict(customer=ct, supplier=st, lag_q=r["best_lag"],
                             pearson=r["pearson"], p_value=r["p_value"], n=r["n"],
                             significant=bool(r["significant"] and r["sign_match"]),
                             supplier_size=round(company_size(long, st) or 0, 0)))
    df = pd.DataFrame(rows)
    return df.sort_values("pearson", key=lambda s: s.abs(), ascending=False) if len(df) else df


def weighted_edge(long, cust, supp, channel, weight="composite", lags=(0, 4),
                  sig_only=True):
    """섹터 엣지 = 유의한 기업쌍들의 가중 종합."""
    det = pair_detail(long, cust, supp, channel, lags)
    base = dict(customer=cust, supplier=supp,
                customer_label=V.SECTIONS.get(cust, cust),
                supplier_label=V.SECTIONS.get(supp, supp), channel=channel)
    if det.empty:
        return {**base, "status": "insufficient data", "n_pairs": 0, "n_sig": 0}
    pool = det[det.significant] if sig_only else det
    n_sig = int(det.significant.sum())
    if pool.empty:
        return {**base, "status": "no significant pair", "n_pairs": len(det), "n_sig": n_sig}
    w = np.array([_weight({"pearson": r.pearson}, r.supplier_size, weight)
                  for r in pool.itertuples(index=False)], float)
    if w.sum() == 0:
        w = np.ones(len(pool))
    wlag = float(np.average(pool["lag_q"], weights=w))
    wcorr = float(np.average(pool["pearson"], weights=w))
    # 대표 시차 = 가중 최빈(반올림) + 연속 가중평균 병기
    lag_round = int(np.round(wlag))
    return {**base, "status": "ok", "weight": weight,
            "w_lag_q": round(wlag, 2), "lag_q": lag_round, "w_pearson": round(wcorr, 3),
            "n_pairs": len(det), "n_sig": n_sig,
            "top_pair": f"{pool.iloc[0].customer}→{pool.iloc[0].supplier}"}


def _resolve(channel):
    """channel=(Xfeat,Yfeat) 또는 CASH_DRIVERS 약칭 → (xf,xtf,yf,ytf)."""
    if isinstance(channel, (tuple, list)) and len(channel) == 2:
        for xf, xtf, yf, ytf, ch, sh in CM.CASH_DRIVERS:
            if (xf, yf) == tuple(channel):
                return xf, xtf, yf, ytf
        return channel[0], "auto", channel[1], "auto"
    for xf, xtf, yf, ytf, ch, sh in CM.CASH_DRIVERS:      # 채널명으로
        if ch == channel:
            return xf, xtf, yf, ytf
    raise ValueError(f"unknown channel {channel!r}")


def run_weighted_map(long, channel=("AP_GROWTH_QOQ", "REVENUE_GROWTH_QOQ"),
                     weight="composite", relationships=None):
    relationships = relationships or V.RELATIONSHIPS
    rows = [weighted_edge(long, c, s, channel, weight) for c, s in relationships]
    cols = ["customer_label", "supplier_label", "status", "w_lag_q", "lag_q",
            "w_pearson", "n_sig", "n_pairs", "top_pair"]
    df = pd.DataFrame(rows)
    df["customer"] = [r["customer"] for r in rows]
    df["supplier"] = [r["supplier"] for r in rows]
    df["channel"] = str(channel)
    df["weight"] = weight
    return df[[c for c in cols if c in df.columns] + ["customer", "supplier"]]


# --------------------------------------------------------------------------- #
def generate_html(df, path, channel="", weight="", date="2026-07-08"):
    edges = []
    for i, r in enumerate(df.itertuples(index=False)):
        c, s = CM._nid(r.customer_label), CM._nid(r.supplier_label)
        if r.status != "ok":
            edges.append(f'  {c}["{r.customer_label}"] -.->|"데이터부족"| {s}["{r.supplier_label}"]')
            continue
        lbl = f"가중 {r.w_lag_q}q · r={r.w_pearson} · {int(r.n_sig)}쌍"
        arrow = "==>" if r.n_sig >= 2 else "-->"
        edges.append(f'  {c}["{r.customer_label}"] {arrow}|"{lbl}"| {s}["{r.supplier_label}"]')
    mer = "flowchart LR\n" + "\n".join(edges)
    lag_color = {0: "#d62728", 1: "#ff7f0e", 2: "#2ca02c", 3: "#1f77b4", 4: "#6a3d9a"}
    styles = [f"linkStyle {i} stroke:{lag_color.get(int(round(r.w_lag_q)),'#888')},stroke-width:3px;"
              for i, r in enumerate(df.itertuples(index=False))
              if r.status == "ok" and r.n_sig >= 2]

    rows = []
    for r in df.itertuples(index=False):
        if r.status != "ok":
            rows.append(f"<tr><td>{r.customer_label}</td><td>{r.supplier_label}</td>"
                        f"<td colspan=5 class='na'>{r.status}</td></tr>")
        else:
            cls = "sig" if r.n_sig >= 2 else ""
            rows.append(f"<tr class='{cls}'><td>{r.customer_label}</td><td>{r.supplier_label}</td>"
                        f"<td>{r.w_lag_q}q</td><td>{r.w_pearson}</td>"
                        f"<td>{int(r.n_sig)}/{int(r.n_pairs)}</td><td>{r.top_pair}</td></tr>")
    table = "\n".join(rows)

    html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>기업간 가중 현금흐름 시차 맵</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
 body{{font-family:-apple-system,'Malgun Gothic',sans-serif;margin:32px;color:#1a1a1a}}
 h1{{font-size:21px}} .sub{{color:#666;margin-bottom:12px;font-size:13px}}
 .legend span{{margin-right:14px;font-size:12px}}
 .mermaid{{background:#fafafa;border:1px solid #eee;border-radius:8px;padding:16px;margin:14px 0}}
 table{{border-collapse:collapse;width:100%;font-size:13px}}
 th,td{{border:1px solid #e5e5e5;padding:6px 8px;text-align:center}}
 th{{background:#f4f4f4}} tr.sig{{background:#eefbf0}} td.na{{color:#b58900}}
</style></head><body>
<h1>기업간(bottom-up) 가중 현금흐름 Lead-Lag 시차 맵</h1>
<div class="sub">채널 <b>{channel}</b> · 가중 <b>{weight}</b> · 각 섹터 엣지 = 기업쌍 lead-lag의 가중종합 · 분석일 {date}</div>
<div class="legend"><span>🔴0q</span><span>🟠1q</span><span>🟢2q</span><span>🔵3q</span><span>🟣4q</span>
 <span>굵은 화살표=유의 기업쌍 2+ · ⋯데이터부족</span></div>
<div class="mermaid">
{mer}
{chr(10).join(styles)}
</div>
<h2 style="font-size:15px">섹터 엣지 (가중종합)</h2>
<table>
<tr><th>고객</th><th>공급사</th><th>가중시차</th><th>가중 r</th><th>유의쌍/전체</th><th>대표 기업쌍</th></tr>
{table}
</table>
</body></html>"""
    Path(path).write_text(html)
    return path


def generate_md(df, path, channel="", weight="", date="2026-07-08"):
    L = [f"# 기업간(bottom-up) 가중 현금흐름 Lead-Lag\n",
         f"**분석일:** {date} · **채널:** `{channel}` · **가중:** `{weight}`\n",
         "섹터 집계 대신 기업쌍(고객사×공급사) lead-lag를 구해 가중 종합. "
         "가중시차 = 유의 기업쌍들의 가중평균 시차.\n"]
    ok = df[df.status == "ok"]
    L.append(f"\n- 엣지 {len(df)} · 종합가능 {len(ok)} · 유의쌍 2+ {int((ok.n_sig>=2).sum())}\n")
    L.append("\n| 고객 | 공급사 | 가중시차(분기) | 가중 r | 유의쌍/전체 | 대표 기업쌍 |")
    L.append("|---|---|---|---|---|---|")
    for r in df.itertuples(index=False):
        if r.status != "ok":
            L.append(f"| {r.customer_label} | {r.supplier_label} | — | — | — | {r.status} |")
        else:
            b = "**" if r.n_sig >= 2 else ""
            L.append(f"| {r.customer_label} | {r.supplier_label} | {b}{r.w_lag_q}{b} | "
                     f"{r.w_pearson} | {int(r.n_sig)}/{int(r.n_pairs)} | {r.top_pair} |")
    L.append("\n## 가중치 방식\n- equal 동일 · corr |상관| · size 공급사규모 · composite |상관|×log(규모)[기본]\n")
    L.append("## 한계\n- 실제 거래 여부는 미상(SPLC 없음) → 통계적 기업쌍. 상위 후보는 10-K 고객집중도로 확인.\n"
             "- 기업쌍 표본 24~34분기, 개별은 노이즈 → 가중 종합으로 완화.\n")
    Path(path).write_text("\n".join(L))
    return path
