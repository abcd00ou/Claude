"""
add_payables.py — backfill accounts_payable into quarterly_financials from yfinance.

The source DB lacked accounts_payable, which the cash-flow variable guide needs for
DPO / CCC / AP_TO_COGS / AP_GROWTH. This puller fetches 'Accounts Payable' from each
company's quarterly balance sheet and matches it to the existing period_end_date /
calendar_quarter grid (nearest within ±35 days), then writes it into a new column
`accounts_payable_usd_m`. Rebuild panel_long afterwards to expose it.

Run:  python3 add_payables.py
"""
from __future__ import annotations
import sqlite3
from pathlib import Path

import pandas as pd
import yfinance as yf

DB = Path(__file__).parent / "financials.db"


def main():
    con = sqlite3.connect(DB)
    cols = [r[1] for r in con.execute("PRAGMA table_info(quarterly_financials)")]
    if "accounts_payable_usd_m" not in cols:
        con.execute("ALTER TABLE quarterly_financials ADD COLUMN accounts_payable_usd_m REAL")
        con.commit()

    ref = pd.read_sql_query(
        "SELECT ticker, period_end_date, calendar_quarter FROM quarterly_financials", con)
    ref["period_end_date"] = pd.to_datetime(ref["period_end_date"])
    tickers = sorted(ref["ticker"].unique())

    done = filled = 0
    for tk in tickers:
        done += 1
        try:
            bs = yf.Ticker(tk).quarterly_balance_sheet
        except Exception:
            continue
        if bs is None or bs.empty:
            continue
        rows = [i for i in bs.index if i.strip().lower() == "accounts payable"]
        if not rows:
            rows = [i for i in bs.index if "payable" in i.lower() and "tax" not in i.lower()]
        if not rows:
            continue
        ser = bs.loc[rows[0]].dropna()
        grid = ref[ref.ticker == tk]
        for dt, val in ser.items():
            dt = pd.Timestamp(dt)
            diff = (grid["period_end_date"] - dt).abs()
            if diff.min() <= pd.Timedelta(days=35):
                cq = grid.loc[diff.idxmin(), "calendar_quarter"]
                con.execute(
                    "UPDATE quarterly_financials SET accounts_payable_usd_m=? "
                    "WHERE ticker=? AND calendar_quarter=?", (float(val) / 1e6, tk, cq))
                filled += 1
        if done % 20 == 0:
            con.commit()
            print(f"  ...{done}/{len(tickers)} tickers, {filled} rows filled", flush=True)
    con.commit()
    n = con.execute(
        "SELECT COUNT(accounts_payable_usd_m) FROM quarterly_financials").fetchone()[0]
    ncomp = con.execute(
        "SELECT COUNT(DISTINCT ticker) FROM quarterly_financials "
        "WHERE accounts_payable_usd_m IS NOT NULL").fetchone()[0]
    con.close()
    print(f"DONE: accounts_payable filled for {n} rows across {ncomp} companies")


if __name__ == "__main__":
    main()
