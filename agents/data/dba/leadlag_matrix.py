"""
leadlag_matrix.py — GEM Step 1: full indicator×indicator lead-lag scanner.

"매출→매출" 하나가 아니라 features.py의 38개 지표 전체를 서로 교차해 lead-lag를
스캔한다. 이것은 GEM 자체가 아니라 GEM 방정식을 특정화하기 위한 SCREENING 단계다:
  • 어떤 X가 어떤 Y를 몇 분기 선행하는지의 지도를 만들고,
  • 각 내생변수 Y별로 상위 선행 X 후보(방정식 우변 후보)를 뽑는다.

두 축:
  scan_internal(ticker)         한 기업 안: X_t → Y_{t+k}  (38×38)
  scan_cross(customer,supplier) 밸류체인: 고객 X → 공급사 Y (섹션 집계)

reuse: features.py(지표) · cashflow_leadlag.lead_lag_scan(스캔) · valuechain(관계).
표본이 짧아(≈40q) 전부를 방정식에 넣을 수는 없다 — 스캔은 '무엇을 버릴지' 알기 위함.
"""
from __future__ import annotations
from pathlib import Path

import numpy as np
import pandas as pd

import features as F
import cashflow_leadlag as C
import panel as P
import valuechain as V

HERE = Path(__file__).parent

# GEM에서 우변(설명변수)으로는 부적절한, 항등식/사후결과 성격 지표는 X에서 제외 가능
DEFAULT_X = [f for f in F.ALL_FEATURES]
DEFAULT_Y = [f for f in F.ALL_FEATURES]
# GEM 핵심 내생변수 후보(방정식 좌변으로 특히 관심)
KEY_ENDOG = ["REVENUE_GROWTH_QOQ", "REVENUE_GROWTH_YOY", "OCF_MARGIN", "FCF_MARGIN",
             "CCC", "DSO", "DIO", "OPERATING_MARGIN"]


def _prep(feats, name):
    """feature 컬럼 -> registry 기본 변환 적용된 시리즈."""
    if name not in feats.columns:
        return pd.Series(dtype=float)
    spec = F.FEATURE_REGISTRY[name]
    how = spec["default"]
    winsor = (0.02, 0.98) if (spec["kind"] == "ratio" and how == "level") else None
    return F.transform_series(feats[name], how, winsor=winsor).dropna()


# --------------------------------------------------------------------------- #
def scan_internal(long, ticker, x_feats=None, y_feats=None, max_lag=4,
                  min_abs_corr=0.3, min_n=10):
    """한 기업 내부의 전체 지표쌍 lead-lag (X_t → Y_{t+k})."""
    x_feats = x_feats or DEFAULT_X
    y_feats = y_feats or DEFAULT_Y
    feats = F.compute_features(long, ticker)
    if feats.empty:
        return pd.DataFrame()
    cache = {f: _prep(feats, f) for f in set(x_feats) | set(y_feats)}
    name = P.company_name(long, ticker)
    rows = []
    for xf in x_feats:
        xs = cache[xf]
        if xs.empty:
            continue
        for yf in y_feats:
            if xf == yf:
                continue
            r = C.lead_lag_scan(xs, cache[yf], (0, max_lag))
            if r["status"] != "ok" or r["n"] < min_n:
                continue
            if abs(r["pearson"]) < min_abs_corr:
                continue
            rows.append(dict(ticker=ticker, company=name, X=xf, Y=yf,
                             lag=r["best_lag"], pearson=r["pearson"],
                             spearman=r["spearman"], p_value=r["p_value"],
                             n=r["n"], significant=r["significant"]))
    df = pd.DataFrame(rows)
    return df.reindex(df["pearson"].abs().sort_values(ascending=False).index) if len(df) else df


def scan_cross(long, cust, supp, x_feats=None, y_feats=None, lags=(0, 4),
               min_abs_corr=0.3, min_n=10):
    """밸류체인 한 관계의 전체 지표쌍 lead-lag (고객 X → 공급사 Y, 섹션 집계)."""
    x_feats = x_feats or DEFAULT_X
    y_feats = y_feats or DEFAULT_Y
    xc = {f: C.section_feature(long, cust, f, "auto") for f in x_feats}
    yc = {f: C.section_feature(long, supp, f, "auto") for f in y_feats}
    rows = []
    for xf in x_feats:
        sx, _ = xc[xf]
        if sx is None:
            continue
        for yf in y_feats:
            sy, _ = yc[yf]
            if sy is None:
                continue
            r = C.lead_lag_scan(sx, sy, lags)
            if r["status"] != "ok" or r["n"] < min_n or abs(r["pearson"]) < min_abs_corr:
                continue
            rows.append(dict(customer=V.SECTIONS.get(cust, cust),
                             supplier=V.SECTIONS.get(supp, supp), X=xf, Y=yf,
                             lag=r["best_lag"], pearson=r["pearson"],
                             spearman=r["spearman"], p_value=r["p_value"],
                             n=r["n"], significant=r["significant"]))
    df = pd.DataFrame(rows)
    return df.reindex(df["pearson"].abs().sort_values(ascending=False).index) if len(df) else df


# --------------------------------------------------------------------------- #
def equation_candidates(matrix_df, y_feat, top=6, only_sig=True, min_lag=0):
    """
    GEM Step 2 준비: 특정 내생변수 Y를 이끄는 상위 선행 X 후보(방정식 우변 후보).
    lag>=min_lag(예: 1) 로 하면 순수 선행변수만.
    """
    d = matrix_df[matrix_df["Y"] == y_feat]
    if only_sig:
        d = d[d["significant"]]
    d = d[d["lag"] >= min_lag]
    return d.sort_values("pearson", key=lambda s: s.abs(), ascending=False).head(top)


def run_internal_panel(long, tickers, **kw):
    """여러 기업의 내부 매트릭스를 합치고 랭킹."""
    parts = [scan_internal(long, tk, **kw) for tk in tickers]
    parts = [p for p in parts if len(p)]
    if not parts:
        return pd.DataFrame()
    df = pd.concat(parts, ignore_index=True)
    return df.reindex(df["pearson"].abs().sort_values(ascending=False).index)


def run_cross_panel(long, relationships=None, **kw):
    relationships = relationships or V.RELATIONSHIPS
    parts = [scan_cross(long, c, s, **kw) for c, s in relationships]
    parts = [p for p in parts if len(p)]
    if not parts:
        return pd.DataFrame()
    df = pd.concat(parts, ignore_index=True)
    return df.reindex(df["pearson"].abs().sort_values(ascending=False).index)


def save(df, name):
    p = HERE / f"{name}.csv"
    df.to_csv(p, index=False)
    return p
