"""
cashflow_leadlag.py — recommended variable-pair lead-lag (guide §4, §5, §9).

Two analysis axes from the cash-flow variable guide:
  • 기업 내부 (internal): within one company, does a working-capital bottleneck
    X_t lead a cash outcome Y_{t+k}?   (guide §4 / table 16, Top-8)
  • 기업 간 (cross): does a customer's X lead a supplier's Y (or supplier→customer)?
    (guide §5 / table 17), reusing the value-chain relationships.

Everything is expressed with features.py features + an EXPECTED SIGN, so a result
counts as "가설지지" only when the correlation has the economically-expected sign,
is significant, and (for causality) Granger-supports the direction.

Uses features.py (variables) + leadlag.py (_f_sf p-values, granger_p) + panel.py.
Directional convention: X is always the LEADING candidate, Y the LAGGING one,
scan k = 0..max_lag  (corr of X_t vs Y_{t+k}).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import features as F
import leadlag as ll
import panel as P
import valuechain as V

# ----- guide §4 / table 16 : 기업 내부 Top-8  (X_feat, x_tf, Y_feat, y_tf, expected, 가설) -----
INTERNAL_PAIRS = [
    ("CCC", "level", "FCF_MARGIN", "level", "-", "현금전환주기↑ → FCF마진↓"),
    ("DIO", "level", "FCF_MARGIN", "level", "-", "재고체류↑ → FCF마진↓"),
    ("DSO", "level", "OCF_MARGIN", "level", "-", "회수기간↑ → OCF마진↓"),
    ("DPO", "level", "OCF_MARGIN", "level", "+", "지급지연↑ → 단기 OCF방어"),
    ("AR_GROWTH_MINUS_REVENUE_GROWTH", "level", "OCF_MARGIN", "level", "-", "AR>매출 성장 → OCF악화"),
    ("AP_GROWTH_MINUS_COGS_GROWTH", "level", "OCF_MARGIN", "level", "+", "AP>원가 성장 → 현금방어"),
    ("INVENTORY_GROWTH_MINUS_REVENUE_GROWTH", "level", "FCF_MARGIN", "level", "-", "재고>매출 성장 → FCF악화"),
    ("CAPEX_TO_OCF", "level", "FCF_MARGIN", "level", "-", "투자부담↑ → FCF↓"),
]

# ----- guide §5 / table 17 : 기업 간  (direction, X_feat, x_tf, Y_feat, y_tf, expected, lags, 가설) -----
# direction 'c2s' = customer X → supplier Y ; 's2c' = supplier X → customer Y
CROSS_PAIRS = [
    ("c2s", "COGS_GROWTH_QOQ", "level", "REVENUE_GROWTH_QOQ", "level", "+", (0, 2), "고객 구매↑ → 공급사 매출↑"),
    ("c2s", "CAPEX_GROWTH_QOQ", "level", "REVENUE_GROWTH_QOQ", "level", "+", (1, 4), "고객 투자↑ → 공급사 매출↑"),
    ("c2s", "DPO", "level", "DSO", "level", "+", (0, 2), "고객 지급지연 → 공급사 회수지연"),
    ("c2s", "AP_TO_COGS", "level", "AR_TO_REVENUE", "level", "+", (0, 2), "고객 미지급부담 → 공급사 미수부담"),
    ("c2s", "FCF_MARGIN", "level", "REVENUE_GROWTH_QOQ", "level", "+", (1, 4), "고객 현금여력 → 공급사 매출"),
    ("s2c", "DIO", "level", "REVENUE_GROWTH_QOQ", "level", "-", (1, 3), "공급사 재고체류 → 고객 수요둔화"),
    ("s2c", "INVENTORY_GROWTH_MINUS_REVENUE_GROWTH", "level", "COGS_GROWTH_QOQ", "level", "?", (1, 3), "공급사 재고과증 → 고객 구매(±)"),
]


# --------------------------------------------------------------------------- #
def _corr_p(r, n):
    if n < 4 or abs(r) >= 1:
        return np.nan
    return ll._f_sf((r * r) * (n - 2) / (1 - r * r), 1, n - 2)


def _spearman(a, b):
    ar = pd.Series(a).rank().to_numpy()
    br = pd.Series(b).rank().to_numpy()
    if np.std(ar) == 0 or np.std(br) == 0:
        return np.nan
    return float(np.corrcoef(ar, br)[0, 1])


def lead_lag_scan(x, y, lag_range=(0, 4), expected=None, min_overlap=6):
    """
    corr(X_t, Y_{t+k}) for k in lag_range. Returns dict with the full table and the
    'best' lag = strongest |Pearson| whose sign matches `expected` ('+'/'-'/'?'/None).
    """
    k0, k1 = lag_range
    rows = []
    for k in range(k0, k1 + 1):
        d = pd.concat([x, y.shift(-k)], axis=1).dropna()
        n = len(d)
        if n >= min_overlap:
            a, b = d.iloc[:, 0].to_numpy(), d.iloc[:, 1].to_numpy()
            if np.std(a) > 0 and np.std(b) > 0:
                pear = float(np.corrcoef(a, b)[0, 1])
                rows.append((k, pear, _spearman(a, b), _corr_p(pear, n), n))
    if not rows:
        return dict(status="insufficient data", table=pd.DataFrame())
    tbl = pd.DataFrame(rows, columns=["lag_k", "pearson", "spearman", "p_value", "n"])

    cand = tbl
    if expected in ("+", "-"):
        want = tbl[tbl["pearson"] > 0] if expected == "+" else tbl[tbl["pearson"] < 0]
        cand = want if not want.empty else tbl
    best = cand.loc[cand["pearson"].abs().idxmax()]
    sign = "+" if best["pearson"] >= 0 else "-"
    sign_match = (expected in (None, "?")) or (sign == expected)
    return dict(status="ok", table=tbl,
                best_lag=int(best["lag_k"]), pearson=round(float(best["pearson"]), 3),
                spearman=round(float(best["spearman"]), 3) if not np.isnan(best["spearman"]) else None,
                p_value=round(float(best["p_value"]), 4) if not np.isnan(best["p_value"]) else None,
                n=int(best["n"]), sign=sign, expected=expected, sign_match=sign_match,
                significant=(not np.isnan(best["p_value"])) and best["p_value"] < 0.05)


# --------------------------------------------------------------------------- #
def analyze_internal(long, ticker, x_feat, x_tf, y_feat, y_tf, expected,
                     hypothesis="", max_lag=4):
    """One internal pair for one company: X_t → Y_{t+k}, k=0..max_lag."""
    x = F.get_feature(long, ticker, x_feat, x_tf)
    y = F.get_feature(long, ticker, y_feat, y_tf)
    r = lead_lag_scan(x, y, (0, max_lag), expected)
    base = dict(ticker=ticker, company=P.company_name(long, ticker),
                section=P.section_of(long, ticker),
                X=f"{x_feat}", Y=f"{y_feat}", expected=expected, hypothesis=hypothesis)
    if r["status"] != "ok":
        return {**base, "status": r["status"]}
    g = ll.granger_p(x, y, lag=max(1, min(r["best_lag"], 2)))
    verdict = _verdict(r)
    return {**base, "status": "ok", "best_lag": r["best_lag"], "pearson": r["pearson"],
            "spearman": r["spearman"], "p_value": r["p_value"], "granger_p": None if np.isnan(g) else round(g, 4),
            "n": r["n"], "sign": r["sign"], "sign_match": r["sign_match"],
            "significant": r["significant"], "verdict": verdict, "_scan": r}


def run_internal(long, tickers, pairs=INTERNAL_PAIRS, max_lag=4):
    rows = []
    for tk in tickers:
        for x_feat, x_tf, y_feat, y_tf, exp, hyp in pairs:
            rows.append(analyze_internal(long, tk, x_feat, x_tf, y_feat, y_tf, exp, hyp, max_lag))
    cols = ["company", "section", "X", "Y", "expected", "status", "best_lag",
            "pearson", "spearman", "p_value", "granger_p", "n", "sign_match", "significant", "verdict", "hypothesis"]
    df = pd.DataFrame(rows)
    return df[[c for c in cols if c in df.columns]]


# --------------------------------------------------------------------------- #
def section_feature(long, section, feat, tf, min_q=8):
    """섹션 집계 feature = 구성사 feature의 분기별 평균 (guide §2: 기업 규모 효과 완화)."""
    members = [tk for tk in long[long.section == section].ticker.unique()
               if len(F.get_feature(long, tk, feat, tf)) >= min_q]
    if not members:
        return None, []
    ser = {tk: F.get_feature(long, tk, feat, tf) for tk in members}
    agg = pd.DataFrame(ser).mean(axis=1).dropna()
    return agg.loc[sorted(agg.index, key=P.qkey)], members


def analyze_cross(long, cust, supp, direction, x_feat, x_tf, y_feat, y_tf,
                  expected, lags, hypothesis=""):
    """
    One cross-firm pair on a relationship. direction 'c2s': X=customer, Y=supplier.
    's2c': X=supplier, Y=customer. Scan uses the guide's recommended lag window.
    """
    lead_sec, lag_sec = (cust, supp) if direction == "c2s" else (supp, cust)
    base = dict(customer=V.SECTIONS.get(cust, cust), supplier=V.SECTIONS.get(supp, supp),
                direction=direction, X=f"{V.SECTIONS.get(lead_sec, lead_sec)}·{x_feat}",
                Y=f"{V.SECTIONS.get(lag_sec, lag_sec)}·{y_feat}",
                expected=expected, hypothesis=hypothesis)
    sx, mx = section_feature(long, lead_sec, x_feat, x_tf)
    sy, my = section_feature(long, lag_sec, y_feat, y_tf)
    if sx is None or sy is None:
        miss = lead_sec if sx is None else lag_sec
        return {**base, "status": "insufficient data", "note": f"{V.SECTIONS.get(miss,miss)} 데이터 부족"}
    r = lead_lag_scan(sx, sy, lags, expected)
    if r["status"] != "ok":
        return {**base, "status": r["status"]}
    g = ll.granger_p(sx, sy, lag=max(1, min(r["best_lag"], 2)))
    return {**base, "status": "ok", "best_lag": r["best_lag"], "pearson": r["pearson"],
            "spearman": r["spearman"], "p_value": r["p_value"], "granger_p": None if np.isnan(g) else round(g, 4),
            "n": r["n"], "sign": r["sign"], "sign_match": r["sign_match"],
            "significant": r["significant"], "verdict": _verdict(r), "_scan": r}


def run_cross(long, relationships=None, pairs=CROSS_PAIRS):
    relationships = relationships or V.RELATIONSHIPS
    rows = []
    for cust, supp in relationships:
        for direction, x_feat, x_tf, y_feat, y_tf, exp, lags, hyp in pairs:
            rows.append(analyze_cross(long, cust, supp, direction, x_feat, x_tf,
                                      y_feat, y_tf, exp, lags, hyp))
    cols = ["customer", "supplier", "direction", "X", "Y", "expected", "status",
            "best_lag", "pearson", "spearman", "p_value", "granger_p", "n",
            "sign_match", "significant", "verdict", "hypothesis"]
    df = pd.DataFrame(rows)
    return df[[c for c in cols if c in df.columns]]


# --------------------------------------------------------------------------- #
def _verdict(r):
    if r["status"] != "ok":
        return r["status"]
    if not r["sign_match"]:
        return f"부호불일치(기대 {r['expected']}, 실제 {r['sign']})"
    if r["significant"]:
        return f"가설지지 (lead {r['best_lag']}q, r={r['pearson']}, p={r['p_value']})"
    return f"방향일치·약함 (lead {r['best_lag']}q, r={r['pearson']})"


def generate_md(internal_df, cross_df, path, date="2026-07-06"):
    """현금흐름 lead-lag 리포트(MD). 사용자가 해석을 덧붙이도록 여백 포함."""
    from pathlib import Path
    L = ["# 현금흐름 병목 & Lead-Lag 분석 리포트\n",
         f"**분석일:** {date} · **데이터:** `panel_long`(accounts_payable 포함) · "
         "**엔진:** `features.py` + `cashflow_leadlag.py` (가이드 문서 §4·§5·§9 구현)\n",
         "**판정 규칙:** 상관 부호가 기대부호와 일치 + p<0.05 → **가설지지**. 부호만 일치 → 방향일치·약함. "
         "부호 반대 → 부호불일치.\n"]

    def sec(title, df, cols, headers):
        L.append(f"\n## {title}\n")
        ok = df[df.status == "ok"]
        good = ok[(ok.sign_match) & (ok.significant)]
        L.append(f"- 분석 케이스 {len(df)} · 분석가능 {len(ok)} · **가설지지 {len(good)}건**\n")
        L.append("| " + " | ".join(headers) + " |")
        L.append("|" + "---|" * len(headers))
        for _, r in df.iterrows():
            if r.status != "ok":
                vals = [str(r.get(c, "")) for c in cols[:-1]] + [r.get("note", r.status)]
            else:
                vals = []
                for c in cols:
                    v = r.get(c, "")
                    if c == "best_lag" and pd.notna(v):
                        v = f"{int(v):+d}"
                    vals.append(str(v))
            L.append("| " + " | ".join(vals) + " |")

    sec("1. 기업 내부 (운전자본 병목 → 현금흐름)", internal_df,
        ["company", "X", "Y", "expected", "best_lag", "pearson", "p_value", "granger_p", "verdict"],
        ["기업", "X(선행)", "Y(후행)", "기대", "lag", "Pearson", "p", "Granger", "판정"])
    sec("2. 기업 간 (고객↔공급사 전이)", cross_df,
        ["customer", "supplier", "X", "Y", "expected", "best_lag", "pearson", "p_value", "verdict"],
        ["고객", "공급사", "X(선행)", "Y(후행)", "기대", "lag", "Pearson", "p", "판정"])

    L += ["\n## 3. 해석 메모 (직접 작성)\n",
          "> 아래에 가설지지된 쌍의 경제적 해석, 시차 안정성, 표본 한계 등을 적으세요.\n",
          "- \n- \n- \n",
          "\n## 4. 방법·한계\n",
          "- lag k>0 = X가 Y를 k분기 선행. 부호는 가이드 문서의 기대부호와 대조.\n",
          "- 기업간은 섹션 구성사 feature의 분기 평균으로 집계(규모효과 완화).\n",
          "- Foundry·Server ODM은 12분기 미만으로 데이터 부족.\n",
          "- CAPEX_TO_OCF·CASH_RUNWAY 등 비율은 상하위 2% winsorize.\n",
          "- 상관≠인과: 가설지지 쌍은 Granger·rolling·event study로 추가 검증 권장.\n"]
    Path(path).write_text("\n".join(L))
    return path


def plot_pair(long, kind, a, b, x_feat, x_tf, y_feat, y_tf, expected=None,
              lags=(0, 4), direction="c2s", figsize=(13, 4.5)):
    """
    Inline 2-panel view of one pair. kind='internal' -> a=ticker (b ignored);
    kind='cross' -> a=customer section, b=supplier section.
    """
    import matplotlib.pyplot as plt
    if kind == "internal":
        x = F.get_feature(long, a, x_feat, x_tf); y = F.get_feature(long, a, y_feat, y_tf)
        title = f"{P.company_name(long,a)}  {x_feat}(t) → {y_feat}(t+k)"
        lags = (0, 4)
    else:
        lead_sec, lag_sec = (a, b) if direction == "c2s" else (b, a)
        x, _ = section_feature(long, lead_sec, x_feat, x_tf)
        y, _ = section_feature(long, lag_sec, y_feat, y_tf)
        title = f"{V.SECTIONS.get(lead_sec,lead_sec)}·{x_feat} → {V.SECTIONS.get(lag_sec,lag_sec)}·{y_feat}"
    r = lead_lag_scan(x, y, lags, expected)
    fig, ax = plt.subplots(1, 2, figsize=figsize)
    fig.suptitle(f"{title}\n{_verdict(r)}", fontsize=11, fontweight="bold")
    ax[0].plot(x.index, x.values, "-o", ms=3, color="#1f77b4", label=f"X: {x_feat}")
    ax[0].plot(y.index, y.values, "-o", ms=3, color="#d62728", label=f"Y: {y_feat}")
    ax[0].axhline(0, color="grey", lw=.6); ax[0].legend(fontsize=8); ax[0].set_title("(1) X, Y 시계열")
    [l.set_visible(i % 3 == 0) for i, l in enumerate(ax[0].get_xticklabels())]
    ax[0].tick_params(axis="x", rotation=90, labelsize=7)
    if r["status"] == "ok":
        t = r["table"]
        colors = ["#2ca02c" if k == r["best_lag"] else "#9ecae1" for k in t["lag_k"]]
        ax[1].bar(t["lag_k"], t["pearson"], color=colors); ax[1].axhline(0, color="grey", lw=.6)
        for _, rr in t.iterrows():
            ax[1].text(rr["lag_k"], rr["pearson"] + (.02 if rr["pearson"] >= 0 else -.06),
                       f"{rr['pearson']:.2f}", ha="center", fontsize=7)
    ax[1].set_title("(2) 시차상관 (k>0 ⇒ X 선행)"); ax[1].set_xlabel("lag k (분기)"); ax[1].set_ylabel("Pearson r")
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    return fig
