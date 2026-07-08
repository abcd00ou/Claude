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


def _vd(feat, tf):
    return feat if tf == "auto" else f"{feat}[{tf}]"


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


def corr_weighted_supplier(long, driver, supp_section, y_feat="REVENUE_GROWTH_YOY",
                           ytf="auto", lags=(0, 4), min_q=MIN_Q):
    """
    공급사 섹터를 driver(고객 신호)와의 상관 가중으로 '매출 가중합' 신호로 만든다.
    w_j = max(corr(driver, 공급사_j), 0). 신호 = Σ(w_j·y_j)/Σw_j.
    반환: (가중합 신호, 기여 테이블[ticker·name·corr·w·size]).
    """
    mem = members(long, supp_section, y_feat, min_q)
    sigs, contrib = {}, []
    for j in mem:
        sy = F.get_feature(long, j, y_feat, ytf)
        if sy.dropna().shape[0] < MIN_N:
            continue
        r = C.lead_lag_scan(driver, sy, lags)
        c = r["pearson"] if r.get("status") == "ok" else np.nan
        sigs[j] = sy
        contrib.append(dict(ticker=j, name=P.company_name(long, j),
                            corr=round(c, 3) if not np.isnan(c) else None,
                            best_lag=r.get("best_lag") if r.get("status") == "ok" else None,
                            size=round(company_size(long, j) or 0, 0)))
    cdf = pd.DataFrame(contrib)
    if cdf.empty:
        return None, cdf
    cdf["w"] = cdf["corr"].clip(lower=0).fillna(0)
    if cdf["w"].sum() == 0:
        return None, cdf
    wide = pd.DataFrame(sigs)
    w = cdf.set_index("ticker")["w"].reindex(wide.columns).fillna(0).to_numpy()
    wsig = (wide.to_numpy() * w).sum(axis=1) / w.sum()      # 분기별 상관가중 매출합
    wsig = pd.Series(wsig, index=wide.index).dropna()
    cdf["weight_share"] = (cdf["w"] / cdf["w"].sum()).round(3)
    return wsig.loc[sorted(wsig.index, key=P.qkey)], cdf.sort_values("w", ascending=False)


def relation_corrweighted(long, cust_ticker, supp_section,
                          x_feat="AP_GROWTH_YOY", xtf="auto",
                          y_feat="REVENUE_GROWTH_YOY", ytf="auto", lags=(0, 4)):
    """
    고객 단일기업(예: NVDA)의 X → 공급사 섹터의 '상관가중 매출합' Y 의 lead-lag.
    사용자 방식: AP·revenue YoY 상관을 가중치로 공급사 매출을 가중합해 관계 재정리.
    """
    driver = F.get_feature(long, cust_ticker, x_feat, xtf)
    base = dict(customer=cust_ticker, customer_name=P.company_name(long, cust_ticker),
                supplier_section=supp_section, supplier_label=V.SECTIONS.get(supp_section, supp_section),
                x_feat=_vd(x_feat, xtf), y_feat=_vd(y_feat, ytf))
    if driver.dropna().shape[0] < MIN_N:
        return {**base, "status": "insufficient customer data"}, pd.DataFrame()
    wsig, cdf = corr_weighted_supplier(long, driver, supp_section, y_feat, ytf, lags)
    if wsig is None:
        return {**base, "status": "insufficient supplier data"}, cdf
    r = C.lead_lag_scan(driver, wsig, lags)
    if r.get("status") != "ok":
        return {**base, "status": "no signal"}, cdf
    return {**base, "status": "ok", "lag_q": r["best_lag"], "pearson": r["pearson"],
            "spearman": r["spearman"], "p_value": r["p_value"], "n": r["n"],
            "significant": bool(r["significant"] and r["sign_match"]),
            "n_suppliers": int((cdf["w"] > 0).sum())}, cdf


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
def top_company(long, section, feat="REVENUE_GROWTH_YOY"):
    mem = members(long, section, feat)
    return max(mem, key=lambda t: company_size(long, t) or 0) if mem else None


def run_corrweighted_map(long, x=("AP_GROWTH_YOY", "auto"),
                         y=("REVENUE_GROWTH_YOY", "auto"), relationships=None):
    """
    각 엣지: 고객 섹터 매출 1위 기업 → 공급사 섹터 '상관가중 매출합'의 lead-lag.
    반환: (요약 DataFrame, {엣지: 기여 테이블}).
    """
    relationships = relationships or V.RELATIONSHIPS
    rows, contribs = [], {}
    for cs, ss in relationships:
        rep = top_company(long, cs)
        base = dict(customer_sec=cs, customer_label=V.SECTIONS.get(cs, cs),
                    supplier_sec=ss, supplier_label=V.SECTIONS.get(ss, ss))
        if rep is None:
            rows.append({**base, "status": "insufficient customer data"}); continue
        res, cdf = relation_corrweighted(long, rep, ss, x[0], x[1], y[0], y[1])
        contribs[(cs, ss)] = cdf
        rows.append({**base, "customer_rep": rep, "customer_rep_name": P.company_name(long, rep),
                     **{k: res.get(k) for k in ("status", "lag_q", "pearson", "p_value",
                                                "n", "n_suppliers")}})
    cols = ["customer_label", "customer_rep", "supplier_label", "status",
            "lag_q", "pearson", "p_value", "n", "n_suppliers"]
    df = pd.DataFrame(rows)
    df["customer_sec"] = [r["customer_sec"] for r in rows]
    df["supplier_sec"] = [r["supplier_sec"] for r in rows]
    return df[[c for c in cols if c in df.columns] + ["customer_sec", "supplier_sec"]], contribs


def generate_corrweighted_md(df, contribs, path, x="", y="", date="2026-07-08"):
    L = [f"# 기업간 상관가중 매출합 현금흐름 Lead-Lag\n",
         f"**분석일:** {date} · **채널:** 고객 `{x}` → 공급사 `{y}`\n",
         "섹터 단순합 대신, 공급사 각 기업의 매출을 **고객과의 상관값으로 가중합**해 관계 재정리. "
         "고객은 섹터 매출 1위 기업. 가중치 = max(상관, 0).\n"]
    ok = df[df.status == "ok"]
    L.append(f"\n- 엣지 {len(df)} · 분석가능 {len(ok)} · 유의 {int((ok.get('p_value', 1) < 0.05).sum() if len(ok) else 0)}\n")
    L.append("\n## 섹터 엣지 (상관가중 매출합)\n")
    L.append("| 고객(대표) | 공급사 | 시차(분기) | r | p | 공급사수 |")
    L.append("|---|---|---|---|---|---|")
    for r in df.itertuples(index=False):
        if r.status != "ok":
            L.append(f"| {r.customer_label} | {r.supplier_label} | — | — | — | {r.status} |")
        else:
            b = "**" if (r.p_value or 1) < 0.05 else ""
            L.append(f"| {r.customer_label}({r.customer_rep}) | {r.supplier_label} | "
                     f"{b}{int(r.lag_q):+d}{b} | {r.pearson} | {r.p_value} | {int(r.n_suppliers)} |")
    L.append("\n## 엣지별 공급사 기여 (상관 가중치)\n")
    for (cs, ss), cdf in contribs.items():
        if cdf is None or cdf.empty or "weight_share" not in cdf:
            continue
        top = cdf[cdf.w > 0].head(5)
        if top.empty:
            continue
        line = ", ".join(f"{t.name}({t.ticker}) r={t.corr} w={t.weight_share}"
                         for t in top.itertuples(index=False))
        L.append(f"- **{V.SECTIONS.get(cs,cs)}→{V.SECTIONS.get(ss,ss)}**: {line}")
    L.append("\n## 한계\n- 공급사 상관가중합은 '통계적 거래처 비중'. 실제 매출 비중/거래는 10-K로 확인.\n"
             "- Foundry·Server ODM(대만)은 5분기뿐이라 불가.\n")
    Path(path).write_text("\n".join(L))
    return path


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
 .interp{{background:#fff8e1;border-left:4px solid #f0b400;padding:12px 16px;margin:14px 0;font-size:13px;line-height:1.75;border-radius:4px}}
 .interp b{{color:#8a6d00}}
 h1{{font-size:21px}} .sub{{color:#666;margin-bottom:12px;font-size:13px}}
 .legend span{{margin-right:14px;font-size:12px}}
 .mermaid{{background:#fafafa;border:1px solid #eee;border-radius:8px;padding:16px;margin:14px 0}}
 table{{border-collapse:collapse;width:100%;font-size:13px}}
 th,td{{border:1px solid #e5e5e5;padding:6px 8px;text-align:center}}
 th{{background:#f4f4f4}} tr.sig{{background:#eefbf0}} td.na{{color:#b58900}}
</style></head><body>
<h1>기업간(bottom-up) 가중 현금흐름 Lead-Lag 시차 맵</h1>
<div class="sub">채널 <b>{channel}</b> · 가중 <b>{weight}</b> · 각 섹터 엣지 = 기업쌍 lead-lag의 가중종합 · 분석일 {date}</div>
<div class="interp">
📖 <b>이 맵 읽는 법</b><br>
섹터 집계 대신 <b>기업쌍(고객사 × 공급사)</b> lead-lag를 구해 가중종합한 맵입니다.
섹터 단순합은 실제 거래관계를 뭉개므로, 기업 단위로 보고 가중치로 다시 합칩니다.<br>
• <b>대표 기업쌍</b> = 그 섹터 관계를 실제로 이끄는 조합 (예: MSFT→AVGO, MU→LRCX).<br>
• <b>가중시차</b> = 유의한 기업쌍들의 가중평균 시차. 굵은 화살표 = 유의 기업쌍 2개 이상.<br>
• <b>유의쌍/전체</b> = 그 엣지에서 유의하게 나온 기업쌍 비율 (많을수록 견고).<br>
👉 대표 기업쌍이 곧 "이 섹터 관계를 대표하는 실제 거래선"입니다(통계적 추정, 10-K로 교차확인 권장).
</div>
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
