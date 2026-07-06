"""
features.py — cash-flow / working-capital feature engine.

Implements EVERY variable in `cash_flow_lead_lag_variable_guide.docx` §3 as a
derived feature computed from the long table `panel_long` (via panel.py). Analysis
code asks for a feature by name + transform and gets a clean quarterly series; it
never recomputes these formulas itself.

Source items used (panel_long): revenue, cogs(=revenue-gross_profit, derived by
panel.py), inventory, receivables(=accounts_receivable), accounts_payable, capex,
cash, operating_cash_flow(=ocf), fcf, operating_income, net_income.

Feature groups (doc §3.1–3.4):
  원천        REVENUE COGS INVENTORY AR AP CAPEX CASH OCF FCF OPERATING_INCOME NET_INCOME
  운전자본    DIO DSO DPO CCC                         (average balances, days=91.25)
  성장/miss.  *_GROWTH_QOQ/_YOY, *_MINUS_* spreads
  비율/마진   AR_TO_REVENUE AP_TO_COGS OCF_MARGIN FCF_MARGIN OPERATING_MARGIN
              CAPEX_TO_OCF CASH_CONVERSION_RATIO CASH_RUNWAY_QTR FCF_TO_OPERATING_INCOME

Transforms (doc §2): level, growth_qoq, growth_yoy, change_qoq, change_yoy, zscore.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import panel as P

DAYS = 91.25

# doc item name -> panel_long item (source amounts)
SOURCE_ALIAS = {
    "REVENUE": "revenue", "COGS": "cogs", "INVENTORY": "inventory",
    "AR": "receivables", "AP": "accounts_payable", "CAPEX": "capex",
    "CASH": "cash", "OCF": "operating_cash_flow", "FCF": "fcf",
    "OPERATING_INCOME": "operating_income", "NET_INCOME": "net_income",
}

# kind drives the DEFAULT transform and how change/growth is interpreted (doc §2, tbl3)
#   amount -> growth (QoQ/YoY); days/ratio/spread/growth -> level + change
FEATURE_REGISTRY = {
    # 원천 금액
    "REVENUE": dict(kind="amount", default="growth_qoq", desc="매출"),
    "COGS": dict(kind="amount", default="growth_qoq", desc="매출원가(구매/생산 proxy)"),
    "INVENTORY": dict(kind="amount", default="growth_qoq", desc="재고"),
    "AR": dict(kind="amount", default="growth_qoq", desc="매출채권"),
    "AP": dict(kind="amount", default="growth_qoq", desc="매입채무"),
    "CAPEX": dict(kind="amount", default="growth_qoq", desc="설비투자(abs)"),
    "CASH": dict(kind="amount", default="level", desc="현금성자산"),
    "OCF": dict(kind="amount", default="growth_qoq", desc="영업활동현금흐름"),
    "FCF": dict(kind="amount", default="growth_qoq", desc="잉여현금흐름"),
    "OPERATING_INCOME": dict(kind="amount", default="growth_qoq", desc="영업이익"),
    "NET_INCOME": dict(kind="amount", default="growth_qoq", desc="순이익"),
    # 운전자본 사이클 (일수) — default level, 보조 change_qoq
    "DIO": dict(kind="days", default="level", desc="재고자산회전일수 avg(inv)/cogs*91.25"),
    "DSO": dict(kind="days", default="level", desc="매출채권회수일수 avg(AR)/revenue*91.25"),
    "DPO": dict(kind="days", default="level", desc="매입채무지급일수 avg(AP)/purchases*91.25"),
    "CCC": dict(kind="days", default="level", desc="현금전환주기 DIO+DSO-DPO"),
    # 성장/mismatch
    "REVENUE_GROWTH_QOQ": dict(kind="growth", default="level", desc="매출 QoQ"),
    "COGS_GROWTH_QOQ": dict(kind="growth", default="level", desc="원가 QoQ"),
    "AR_GROWTH_QOQ": dict(kind="growth", default="level", desc="매출채권 QoQ"),
    "AP_GROWTH_QOQ": dict(kind="growth", default="level", desc="매입채무 QoQ"),
    "INVENTORY_GROWTH_QOQ": dict(kind="growth", default="level", desc="재고 QoQ"),
    "CAPEX_GROWTH_QOQ": dict(kind="growth", default="level", desc="capex(abs) QoQ"),
    "REVENUE_GROWTH_YOY": dict(kind="growth", default="level", desc="매출 YoY"),
    "COGS_GROWTH_YOY": dict(kind="growth", default="level", desc="원가 YoY"),
    "AR_GROWTH_YOY": dict(kind="growth", default="level", desc="매출채권 YoY"),
    "AP_GROWTH_YOY": dict(kind="growth", default="level", desc="매입채무 YoY"),
    "INVENTORY_GROWTH_YOY": dict(kind="growth", default="level", desc="재고 YoY"),
    "AR_GROWTH_MINUS_REVENUE_GROWTH": dict(kind="spread", default="level",
                                           desc="AR성장-매출성장(회수병목)"),
    "AP_GROWTH_MINUS_COGS_GROWTH": dict(kind="spread", default="level",
                                        desc="AP성장-원가성장(현금방어)"),
    "INVENTORY_GROWTH_MINUS_REVENUE_GROWTH": dict(kind="spread", default="level",
                                                  desc="재고성장-매출성장(재고병목)"),
    # 비율/마진/현금여력
    "AR_TO_REVENUE": dict(kind="ratio", default="level", desc="매출대비 미회수채권"),
    "AP_TO_COGS": dict(kind="ratio", default="level", desc="원가대비 미지급채무"),
    "OCF_MARGIN": dict(kind="ratio", default="level", desc="ocf/revenue"),
    "FCF_MARGIN": dict(kind="ratio", default="level", desc="fcf/revenue"),
    "OPERATING_MARGIN": dict(kind="ratio", default="level", desc="영업이익/revenue"),
    "CAPEX_TO_OCF": dict(kind="ratio", default="level", desc="abs(capex)/ocf"),
    "CASH_CONVERSION_RATIO": dict(kind="ratio", default="level", desc="ocf/net_income"),
    "CASH_RUNWAY_QTR": dict(kind="ratio", default="level", desc="cash/max(-fcf,0) 분기"),
    "FCF_TO_OPERATING_INCOME": dict(kind="ratio", default="level", desc="fcf/operating_income"),
}
ALL_FEATURES = list(FEATURE_REGISTRY)


# --------------------------------------------------------------------------- #
def _avg(s):
    """평균잔액 = (기말 + 전기말)/2 (doc §7.1)."""
    return (s + s.shift(1)) / 2.0


def _gq(s):   # QoQ growth
    return s / s.shift(1) - 1.0


def _gy(s):   # YoY growth
    return s / s.shift(4) - 1.0


def compute_features(long, ticker) -> pd.DataFrame:
    """
    Full per-company feature panel (index=quarter). Missing sources (e.g. AP before
    the payables backfill) simply propagate as NaN, so downstream code stays robust.
    """
    src = {}
    for name, item in SOURCE_ALIAS.items():
        try:
            src[name] = P.get_series(long, ticker, item)
        except Exception:
            src[name] = pd.Series(dtype=float)
    df = pd.DataFrame(src)
    if df.empty:
        return df
    df = df.loc[sorted(df.index, key=P.qkey)]
    df["CAPEX"] = df["CAPEX"].abs()                     # 투자 규모 (doc §7.1)

    rev, cogs, inv, ar, ap = df.REVENUE, df.COGS, df.INVENTORY, df.AR, df.AP
    ocf, fcf, cash, ni, oi = df.OCF, df.FCF, df.CASH, df.NET_INCOME, df.OPERATING_INCOME

    # 운전자본 사이클 (평균잔액)
    df["DIO"] = _avg(inv) / cogs * DAYS
    df["DSO"] = _avg(ar) / rev * DAYS
    purchases = cogs + (inv - inv.shift(1))            # purchases proxy (doc tbl5)
    df["DPO"] = _avg(ap) / purchases * DAYS
    df["CCC"] = df["DIO"] + df["DSO"] - df["DPO"]

    # 성장률
    for col in ["REVENUE", "COGS", "AR", "AP", "INVENTORY", "CAPEX"]:
        df[f"{col}_GROWTH_QOQ"] = _gq(df[col])
    for col in ["REVENUE", "COGS", "AR", "AP", "INVENTORY"]:
        df[f"{col}_GROWTH_YOY"] = _gy(df[col])

    # mismatch spreads (QoQ 기준; YoY 필요시 transform으로)
    df["AR_GROWTH_MINUS_REVENUE_GROWTH"] = df.AR_GROWTH_QOQ - df.REVENUE_GROWTH_QOQ
    df["AP_GROWTH_MINUS_COGS_GROWTH"] = df.AP_GROWTH_QOQ - df.COGS_GROWTH_QOQ
    df["INVENTORY_GROWTH_MINUS_REVENUE_GROWTH"] = df.INVENTORY_GROWTH_QOQ - df.REVENUE_GROWTH_QOQ

    # 비율/마진/현금여력
    df["AR_TO_REVENUE"] = ar / rev
    df["AP_TO_COGS"] = ap / cogs
    df["OCF_MARGIN"] = ocf / rev
    df["FCF_MARGIN"] = fcf / rev
    df["OPERATING_MARGIN"] = oi / rev
    df["CAPEX_TO_OCF"] = df.CAPEX / ocf
    df["CASH_CONVERSION_RATIO"] = ocf / ni
    df["CASH_RUNWAY_QTR"] = np.where(-fcf > 0, cash / (-fcf), np.nan)
    df["FCF_TO_OPERATING_INCOME"] = fcf / oi
    return df


# --------------------------------------------------------------------------- #
def transform_series(s, how="level", winsor=None):
    """Apply a doc §2 transform. winsor=(lo,hi) clips quantiles first (for ratios)."""
    s = s.astype(float)
    if winsor:
        lo, hi = s.quantile(winsor[0]), s.quantile(winsor[1])
        s = s.clip(lo, hi)
    if how == "level":
        return s
    if how == "growth_qoq":
        return _gq(s)
    if how == "growth_yoy":
        return _gy(s)
    if how == "change_qoq":
        return s - s.shift(1)
    if how == "change_yoy":
        return s - s.shift(4)
    if how == "zscore":
        sd = s.std(ddof=0)
        return (s - s.mean()) / sd if sd else s * 0.0
    raise ValueError(f"unknown transform {how!r}")


def get_feature(long, ticker, name, transform="auto", winsor=(0.02, 0.98)):
    """
    Quarterly series for one feature. transform='auto' uses the registry default.
    winsor applies only to ratio-kind features (guards CAPEX_TO_OCF etc. blowups).
    Pass winsor=None to disable.
    """
    if name not in FEATURE_REGISTRY:
        raise ValueError(f"unknown feature {name!r}. see features.ALL_FEATURES")
    spec = FEATURE_REGISTRY[name]
    how = spec["default"] if transform == "auto" else transform
    feats = compute_features(long, ticker)
    if name not in feats.columns:
        return pd.Series(dtype=float, name=name)
    w = winsor if (spec["kind"] == "ratio" and how == "level") else None
    out = transform_series(feats[name], how, winsor=w).dropna()
    out.name = f"{ticker}:{name}:{how}"
    return out


def section_residual(long, tickers, name, transform="auto"):
    """
    Common-cycle-removed feature: subtract the cross-company mean each quarter
    (doc §2 'section residual'). Returns {ticker: residual series}.
    """
    raw = {tk: get_feature(long, tk, name, transform) for tk in tickers}
    wide = pd.DataFrame(raw)
    resid = wide.sub(wide.mean(axis=1), axis=0)
    return {tk: resid[tk].dropna() for tk in wide.columns}


def feature_catalog() -> pd.DataFrame:
    """Human-readable table of every available feature (for the notebook)."""
    return pd.DataFrame([
        {"feature": k, "kind": v["kind"], "default_transform": v["default"], "설명": v["desc"]}
        for k, v in FEATURE_REGISTRY.items()])
