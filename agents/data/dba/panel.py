"""
panel.py — the ONE data-access + preprocessing layer for lead-lag analysis.

Every analysis script reads from the canonical long table `panel_long`
(ticker, companyname, date, item, value, section) via this module — no script
touches quarterly_financials / stock_prices directly anymore.

Core preprocessing:
    load_long(...)               -> filtered long DataFrame (the raw table)
    get_series(ticker,item,...)  -> quarterly pd.Series, optional transform
    to_wide(item, ...)           -> wide DataFrame [index=quarter, cols=ticker]
    to_wide_balanced(item, ...)  -> to_wide + min_quarters coverage filter
    build_dataset(...)           -> convenience: dict of {item: wide frame} + metadata

Derived items (computed here, not stored): `cogs` = revenue - gross_profit.

Transforms available in get_series() via transform= parameter:
    'level'      : raw value (default)
    'log'        : natural log (for VECM — requires positive values)
    'zscore'     : (x - mean) / std over the ticker's own history
    'growth_qoq' : QoQ % change
    'growth_yoy' : YoY % change
"""
from __future__ import annotations
from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
DB_DEFAULT = HERE / "financials.db"
CSV_DEFAULT = HERE / "panel_long.csv"     # 모든 분석의 시작점 (read_csv)

# items physically present in panel_long
STORED_ITEMS = [
    "revenue", "revenue_ai_dc", "revenue_yoy", "gross_profit", "gross_margin",
    "operating_income", "net_income", "eps", "cash", "capex", "fcf",
    "operating_cash_flow", "inventory", "receivables", "accounts_payable",
    "total_assets", "total_debt", "stockholders_equity", "stock_price",
]
# items computed on the fly from stored ones
DERIVED_ITEMS = {"cogs": ("revenue", "gross_profit")}  # cogs = revenue - gross_profit

# Materialized cash-flow-guide features now stored directly in panel_long (level form),
# so analysis reads them instead of recomputing. Keep in sync with features.ALL_FEATURES
# minus the source aliases (which are the lower-case stored items above).
FEATURE_ITEMS = [
    "DIO", "DSO", "DPO", "CCC",
    "REVENUE_GROWTH_QOQ", "COGS_GROWTH_QOQ", "AR_GROWTH_QOQ", "AP_GROWTH_QOQ",
    "INVENTORY_GROWTH_QOQ", "CAPEX_GROWTH_QOQ",
    "REVENUE_GROWTH_YOY", "COGS_GROWTH_YOY", "AR_GROWTH_YOY", "AP_GROWTH_YOY",
    "INVENTORY_GROWTH_YOY",
    "AR_GROWTH_MINUS_REVENUE_GROWTH", "AP_GROWTH_MINUS_COGS_GROWTH",
    "INVENTORY_GROWTH_MINUS_REVENUE_GROWTH",
    "AR_TO_REVENUE", "AP_TO_COGS", "OCF_MARGIN", "FCF_MARGIN", "OPERATING_MARGIN",
    "CAPEX_TO_OCF", "CASH_CONVERSION_RATIO", "CASH_RUNWAY_QTR", "FCF_TO_OPERATING_INCOME",
]
STORED_ITEMS = STORED_ITEMS + FEATURE_ITEMS
AVAILABLE_ITEMS = STORED_ITEMS + list(DERIVED_ITEMS)

_MONTH_Q = {3: 1, 6: 2, 9: 3, 12: 4}


def date_to_quarter(date: str) -> str:
    """'YYYY-MM-DD' (normalized quarter-end) -> 'YYYY-QN'."""
    y, m, _ = str(date)[:10].split("-")
    return f"{y}-Q{_MONTH_Q[int(m)]}"


def qkey(cq: str) -> int:
    y, q = cq.split("-Q")
    return int(y) * 4 + int(q)


# --------------------------------------------------------------------------- #
def load_long(source=None, tickers=None, items=None, sections=None) -> pd.DataFrame:
    """
    분석의 시작점. 기본은 CSV(panel_long.csv)를 read_csv로 읽는다. CSV가 없으면
    DB(financials.db)로 자동 fallback → 데이터가 나중에 갱신돼도 코드는 그대로 돈다.
    `source`로 .csv/.db 경로를 명시할 수도 있다.
    """
    if source is None:
        source = CSV_DEFAULT if Path(CSV_DEFAULT).exists() else DB_DEFAULT
    src = str(source)

    if src.endswith(".csv"):
        if not Path(source).exists():                      # robust fallback
            return load_long(DB_DEFAULT, tickers, items, sections)
        df = pd.read_csv(source, dtype={"ticker": str})
        if tickers:
            df = df[df["ticker"].isin(list(tickers))]
        if sections:
            df = df[df["section"].isin(list(sections))]
        if items:
            need = set()
            for it in items:
                need.update(DERIVED_ITEMS[it] if it in DERIVED_ITEMS else [it])
            df = df[df["item"].isin(need)]
        df = df.reset_index(drop=True)
    else:
        con = sqlite3.connect(source)
        where, params = [], []
        if tickers:
            where.append("ticker IN (%s)" % ",".join("?" * len(tickers))); params += list(tickers)
        stored_req = [i for i in items if i in STORED_ITEMS] if items else None
        if stored_req is not None:
            where.append("item IN (%s)" % ",".join("?" * len(stored_req))); params += stored_req
        if sections:
            where.append("section IN (%s)" % ",".join("?" * len(sections))); params += list(sections)
        sql = "SELECT ticker, companyname, date, item, value, section FROM panel_long"
        if where:
            sql += " WHERE " + " AND ".join(where)
        df = pd.read_sql_query(sql, con, params=params)
        con.close()

    if "quarter" not in df.columns:
        df["quarter"] = df["date"].map(date_to_quarter)
    return df


def export_csv(path=CSV_DEFAULT, db=DB_DEFAULT) -> str:
    """DB의 panel_long 전체를 CSV로 저장 (분석 시작점). build 후 호출."""
    df = load_long(db)
    df.to_csv(path, index=False)
    return str(path)


def _stored_series(long_or_db, ticker, item):
    if isinstance(long_or_db, pd.DataFrame):
        d = long_or_db[(long_or_db.ticker == ticker) & (long_or_db.item == item)]
    else:
        d = load_long(long_or_db, tickers=[ticker], items=[item])
    if d.empty:
        return pd.Series(dtype=float, name=item)
    s = (d.drop_duplicates("quarter")
           .sort_values("quarter", key=lambda x: x.map(qkey))
           .set_index("quarter")["value"])
    s.name = item
    return s


def get_series(source, ticker, item, transform: str = "level") -> pd.Series:
    """
    Quarterly series for (ticker, item), indexed by 'YYYY-QN'. `source` may be a DB
    path or a preloaded long DataFrame. Handles derived items (e.g. 'cogs').

    transform options:
      'level'      - raw value (default)
      'log'        - natural log; non-positive values become NaN
      'zscore'     - (x - mean) / std over the ticker's own history
      'growth_qoq' - QoQ % change (x/x.shift(1) - 1)
      'growth_yoy' - YoY % change (x/x.shift(4) - 1)
    """
    if item in DERIVED_ITEMS:
        a, b = DERIVED_ITEMS[item]
        sa, sb = _stored_series(source, ticker, a), _stored_series(source, ticker, b)
        s = (sa - sb).dropna()
        s.name = item
    elif item not in STORED_ITEMS:
        raise ValueError(f"unknown item {item!r}. options: {AVAILABLE_ITEMS}")
    else:
        s = _stored_series(source, ticker, item)

    if transform == "level":
        return s
    if transform == "log":
        out = np.log(s.where(s > 0))
        out.name = f"{item}_log"
        return out.dropna()
    if transform == "zscore":
        sd = s.std(ddof=0)
        out = (s - s.mean()) / sd if sd else s * 0.0
        out.name = f"{item}_zscore"
        return out.dropna()
    if transform == "growth_qoq":
        out = s / s.shift(1) - 1.0
        out.name = f"{item}_growth_qoq"
        return out.dropna()
    if transform == "growth_yoy":
        out = s / s.shift(4) - 1.0
        out.name = f"{item}_growth_yoy"
        return out.dropna()
    raise ValueError(f"unknown transform {transform!r}. options: level, log, zscore, growth_qoq, growth_yoy")


def to_wide(item, db=DB_DEFAULT, tickers=None, sections=None,
            transform: str = "level") -> pd.DataFrame:
    """Wide frame for one item: index = quarter (sorted), columns = ticker.

    transform: same options as get_series() — 'level', 'log', 'zscore',
               'growth_qoq', 'growth_yoy'.
    """
    need = list(DERIVED_ITEMS[item]) if item in DERIVED_ITEMS else [item]
    long = load_long(db, tickers=tickers, items=need, sections=sections)
    ticks = tickers or sorted(long.ticker.unique())
    cols = {tk: get_series(long, tk, item, transform=transform) for tk in ticks}
    wide = pd.DataFrame(cols)
    return wide.loc[sorted(wide.index, key=qkey)]


def to_wide_balanced(item, min_quarters: int = 20, db=DB_DEFAULT,
                     tickers=None, sections=None,
                     transform: str = "level") -> pd.DataFrame:
    """Wide frame filtered to tickers with >= min_quarters non-null observations.

    VECM/ECM 추정에서 표본 수가 부족한 ticker(스타트업·신규 상장)를 자동 제외한다.
    min_quarters 기본값 20 = 5년치 분기 (VECM 최소 추정 가능 수준).

    Returns:
        wide DataFrame, plus attribute .excluded listing dropped tickers.
    """
    wide = to_wide(item, db=db, tickers=tickers, sections=sections, transform=transform)
    coverage = wide.notna().sum()
    keep = coverage[coverage >= min_quarters].index
    excluded = sorted(set(wide.columns) - set(keep))
    result = wide[keep]
    result.excluded = excluded          # caller may inspect
    return result


def companies(db=DB_DEFAULT) -> pd.DataFrame:
    con = sqlite3.connect(db)
    df = pd.read_sql_query(
        "SELECT ticker, MAX(companyname) companyname, MAX(section) section, "
        "COUNT(DISTINCT CASE WHEN item='revenue' THEN date END) revenue_quarters "
        "FROM panel_long GROUP BY ticker ORDER BY section, revenue_quarters DESC", con)
    con.close()
    return df


def company_name(source, ticker) -> str:
    if isinstance(source, pd.DataFrame):
        m = source[source.ticker == ticker]
        return m["companyname"].iloc[0] if not m.empty else ticker
    con = sqlite3.connect(source)
    r = con.execute("SELECT companyname FROM panel_long WHERE ticker=? LIMIT 1", [ticker]).fetchone()
    con.close()
    return r[0] if r else ticker


def section_of(source, ticker) -> str:
    if isinstance(source, pd.DataFrame):
        m = source[source.ticker == ticker]
        return m["section"].iloc[0] if not m.empty else "?"
    con = sqlite3.connect(source)
    r = con.execute("SELECT section FROM panel_long WHERE ticker=? LIMIT 1", [ticker]).fetchone()
    con.close()
    return r[0] if r else "?"


def build_dataset(tickers, items=("revenue",), db=DB_DEFAULT) -> dict:
    """
    Convenience preprocessing bundle for analysis: one wide frame per item, plus
    company metadata. Returns {'wide': {item: DataFrame}, 'meta': DataFrame}.
    """
    long = load_long(db, tickers=list(tickers))
    wide = {}
    for it in items:
        cols = {tk: get_series(long, tk, it) for tk in tickers}
        w = pd.DataFrame(cols)
        wide[it] = w.loc[sorted(w.index, key=qkey)] if len(w) else w
    meta = (long.groupby("ticker")
                .agg(companyname=("companyname", "first"), section=("section", "first"))
                .reindex(tickers).reset_index())
    return {"wide": wide, "meta": meta}
