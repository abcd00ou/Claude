"""
panel.py — the ONE data-access + preprocessing layer for lead-lag analysis.

Every analysis script reads from the canonical long table `panel_long`
(ticker, companyname, date, item, value, section) via this module — no script
touches quarterly_financials / stock_prices directly anymore.

Core preprocessing:
    load_long(...)          -> filtered long DataFrame (the raw table)
    get_series(ticker,item) -> quarterly pd.Series indexed by 'YYYY-QN'
    to_wide(item, ...)      -> wide DataFrame [index=quarter, cols=ticker]
    build_dataset(...)      -> convenience: dict of {item: wide frame} + metadata

Derived items (computed here, not stored): `cogs` = revenue - gross_profit.
"""
from __future__ import annotations
from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd

DB_DEFAULT = Path(__file__).parent / "financials.db"

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
def load_long(db=DB_DEFAULT, tickers=None, items=None, sections=None) -> pd.DataFrame:
    """Return the (optionally filtered) long table with a derived 'quarter' column."""
    con = sqlite3.connect(db)
    where, params = [], []
    if tickers:
        where.append("ticker IN (%s)" % ",".join("?" * len(tickers))); params += list(tickers)
    # only filter stored items in SQL; derived items are added afterwards
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
    df["quarter"] = df["date"].map(date_to_quarter)
    return df


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


def get_series(source, ticker, item) -> pd.Series:
    """
    Quarterly series for (ticker, item), indexed by 'YYYY-QN'. `source` may be a DB
    path or a preloaded long DataFrame. Handles derived items (e.g. 'cogs').
    """
    if item in DERIVED_ITEMS:
        a, b = DERIVED_ITEMS[item]
        sa, sb = _stored_series(source, ticker, a), _stored_series(source, ticker, b)
        s = (sa - sb).dropna()
        s.name = item
        return s
    if item not in STORED_ITEMS:
        raise ValueError(f"unknown item {item!r}. options: {AVAILABLE_ITEMS}")
    return _stored_series(source, ticker, item)


def to_wide(item, db=DB_DEFAULT, tickers=None, sections=None) -> pd.DataFrame:
    """Wide frame for one item: index = quarter (sorted), columns = ticker."""
    need = list(DERIVED_ITEMS[item]) if item in DERIVED_ITEMS else [item]
    long = load_long(db, tickers=tickers, items=need, sections=sections)
    ticks = tickers or sorted(long.ticker.unique())
    cols = {tk: get_series(long, tk, item) for tk in ticks}
    wide = pd.DataFrame(cols)
    return wide.loc[sorted(wide.index, key=qkey)]


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
