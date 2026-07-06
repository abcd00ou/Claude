"""
build_panel_long.py — materialize the canonical LONG-FORMAT analysis table.

    panel_long(ticker, companyname, date, item, value, section)

This is the single table every analysis script reads from (Scope Document §2:
"company x item x quarter, long-format panel"). It is rebuilt from the source
tables (quarterly_financials + stock_prices + companies), so those remain the
system of record and panel_long is a derived, analysis-ready view.

Design choices (matter for correct lead-lag):
  * `date` = NORMALIZED calendar quarter-end derived from calendar_quarter
    (Q1->03-31, Q2->06-30, Q3->09-30, Q4->12-31). Every company therefore shares
    an identical quarterly grid, so cross-company alignment is exact — even for
    off-calendar fiscal years (NVDA, DELL, ...). The DB's calendar_quarter already
    reconciles fiscal->calendar, so we preserve that mapping rather than re-derive.
  * `stock_price` = the as-of close on/just before each quarter's REAL
    period_end_date (the market price when that fiscal quarter's books closed),
    stored under the normalized quarter-end date so it joins to the financials.
  * `item` uses clean names: revenue, gross_profit, operating_income, net_income,
    eps, cash, capex, fcf, operating_cash_flow, inventory, receivables,
    total_assets, total_debt, stockholders_equity, gross_margin, revenue_yoy,
    revenue_ai_dc, stock_price.

Run:  python3 build_panel_long.py
"""
from __future__ import annotations
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).parent
DB = HERE / "financials.db"

# source column -> clean item name
ITEM_MAP = {
    "revenue_usd_m": "revenue",
    "revenue_ai_dc_usd_m": "revenue_ai_dc",
    "revenue_yoy_pct": "revenue_yoy",
    "gross_profit_usd_m": "gross_profit",
    "gross_margin_pct": "gross_margin",
    "operating_income_usd_m": "operating_income",
    "net_income_usd_m": "net_income",
    "eps_diluted": "eps",
    "cash_usd_m": "cash",
    "capex_usd_m": "capex",
    "fcf_usd_m": "fcf",
    "operating_cash_flow_usd_m": "operating_cash_flow",
    "inventory_usd_m": "inventory",
    "receivables_usd_m": "receivables",
    "accounts_payable_usd_m": "accounts_payable",
    "total_assets_usd_m": "total_assets",
    "total_debt_usd_m": "total_debt",
    "stockholders_equity_usd_m": "stockholders_equity",
}

_QEND = {1: "-03-31", 2: "-06-30", 3: "-09-30", 4: "-12-31"}


def quarter_to_date(cq: str) -> str:
    """'YYYY-QN' -> normalized calendar quarter-end 'YYYY-MM-DD'."""
    y, q = cq.split("-Q")
    return f"{y}{_QEND[int(q)]}"


def build():
    con = sqlite3.connect(DB)

    companies = pd.read_sql_query(
        "SELECT ticker, name AS companyname, segments AS section FROM companies", con)
    qf = pd.read_sql_query(
        "SELECT ticker, calendar_quarter, period_end_date, " +
        ", ".join(ITEM_MAP) + " FROM quarterly_financials "
        "WHERE calendar_quarter IS NOT NULL", con)

    # A few (ticker, calendar_quarter) pairs have two source rows (fiscal/calendar
    # restatement quirk). Coalesce them: take the last non-null value per field
    # (prefers the later restatement but never drops data the later row lacks).
    def _coalesce(s):
        v = s.dropna()
        return v.iloc[-1] if len(v) else np.nan
    qf = qf.sort_values("period_end_date")
    agg = {c: _coalesce for c in ITEM_MAP}
    agg["period_end_date"] = "last"
    qf = qf.groupby(["ticker", "calendar_quarter"], as_index=False).agg(agg)

    qf = qf.merge(companies, on="ticker", how="left")
    qf["date"] = qf["calendar_quarter"].map(quarter_to_date)

    # --- melt financial items to long ---
    long_fin = qf.melt(
        id_vars=["ticker", "companyname", "date", "section"],
        value_vars=list(ITEM_MAP),
        var_name="src_col", value_name="value",
    ).dropna(subset=["value"])
    long_fin["item"] = long_fin["src_col"].map(ITEM_MAP)
    long_fin = long_fin[["ticker", "companyname", "date", "item", "value", "section"]]

    # --- stock_price: as-of close at each quarter's real period_end_date ---
    prices = pd.read_sql_query(
        "SELECT ticker, price_date, close_usd FROM stock_prices "
        "WHERE close_usd IS NOT NULL", con)
    con.close()
    prices["price_date"] = pd.to_datetime(prices["price_date"])
    prices = prices.sort_values(["ticker", "price_date"])

    per = qf[["ticker", "companyname", "date", "section", "period_end_date"]].copy()
    per["period_end_date"] = pd.to_datetime(per["period_end_date"])
    per = per.sort_values("period_end_date")

    stock_rows = []
    for tk, grp in per.groupby("ticker"):
        pg = prices[prices["ticker"] == tk]
        if pg.empty:
            continue
        merged = pd.merge_asof(
            grp.sort_values("period_end_date"),
            pg[["price_date", "close_usd"]].rename(columns={"price_date": "period_end_date"}),
            on="period_end_date", direction="backward",
        )
        merged = merged.dropna(subset=["close_usd"])
        for _, r in merged.iterrows():
            stock_rows.append((r["ticker"], r["companyname"], r["date"],
                               "stock_price", float(r["close_usd"]), r["section"]))
    long_px = pd.DataFrame(stock_rows,
                           columns=["ticker", "companyname", "date", "item", "value", "section"])

    panel = pd.concat([long_fin, long_px], ignore_index=True)
    panel = panel.sort_values(["ticker", "item", "date"]).reset_index(drop=True)

    # --- write table ---
    con = sqlite3.connect(DB)
    con.execute("DROP TABLE IF EXISTS panel_long")
    con.execute("""
        CREATE TABLE panel_long (
            ticker      TEXT NOT NULL,
            companyname TEXT,
            date        TEXT NOT NULL,
            item        TEXT NOT NULL,
            value       REAL,
            section     TEXT
        )""")
    panel.to_sql("panel_long", con, if_exists="append", index=False)
    con.execute("CREATE INDEX ix_panel_tid ON panel_long(ticker, item, date)")
    con.execute("CREATE INDEX ix_panel_item ON panel_long(item)")
    con.commit()

    n = con.execute("SELECT COUNT(*) FROM panel_long").fetchone()[0]
    items = con.execute(
        "SELECT item, COUNT(*) FROM panel_long GROUP BY item ORDER BY 2 DESC").fetchall()
    ncomp = con.execute("SELECT COUNT(DISTINCT ticker) FROM panel_long").fetchone()[0]
    con.close()

    print(f"panel_long built: {n:,} rows, {ncomp} companies, {len(items)} items")
    print(f"columns: ticker, companyname, date, item, value, section")
    print("rows per item:")
    for it, c in items:
        print(f"  {it:<22} {c:>6}")


if __name__ == "__main__":
    build()
