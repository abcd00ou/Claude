"""
add_payables_edgar.py — backfill accounts_payable from SEC EDGAR (deep history).

yfinance only exposes the last ~2-3 quarters of the balance sheet, too short for
lead-lag. EDGAR companyfacts gives full history (2016+). This matches on
(ticker, fiscal_year, fiscal_quarter) — the same keys build_financials_db.py used —
so it lines up exactly with the existing calendar_quarter grid. US filers get EDGAR
history; non-US names keep whatever yfinance already wrote.

Run:  python3 add_payables_edgar.py
"""
from __future__ import annotations
import sqlite3
from pathlib import Path

import edgar_financials as E

DB = Path(__file__).parent / "financials.db"


def main():
    con = sqlite3.connect(DB)
    cols = [r[1] for r in con.execute("PRAGMA table_info(quarterly_financials)")]
    if "accounts_payable_usd_m" not in cols:
        con.execute("ALTER TABLE quarterly_financials ADD COLUMN accounts_payable_usd_m REAL")
        con.commit()

    tickers = [r[0] for r in con.execute(
        "SELECT DISTINCT ticker FROM quarterly_financials ORDER BY ticker")]
    cmap = E.cik_map()
    us = [t for t in tickers if t.upper() in cmap]
    print(f"{len(us)}/{len(tickers)} tickers are US-SEC filers → EDGAR payables", flush=True)

    done = filled = 0
    for tk in us:
        done += 1
        try:
            _, q = E.pull(tk)
        except Exception:
            continue
        for r in q:
            ap = r.get("payables")
            if ap is None:
                continue
            cur = con.execute(
                "UPDATE quarterly_financials SET accounts_payable_usd_m=? "
                "WHERE ticker=? AND fiscal_year=? AND fiscal_quarter=?",
                (ap, tk, r["fiscal_year"], r["fiscal_quarter"]))
            filled += cur.rowcount
        if done % 20 == 0:
            con.commit()
            print(f"  ...{done}/{len(us)} filers, {filled} rows filled", flush=True)
    con.commit()
    n = con.execute("SELECT COUNT(accounts_payable_usd_m) FROM quarterly_financials").fetchone()[0]
    ncomp = con.execute("SELECT COUNT(DISTINCT ticker) FROM quarterly_financials "
                        "WHERE accounts_payable_usd_m IS NOT NULL").fetchone()[0]
    # coverage of key names
    key = con.execute(
        "SELECT ticker, COUNT(accounts_payable_usd_m) FROM quarterly_financials "
        "WHERE ticker IN ('NVDA','AMD','MU','INTC','AMAT','LRCX','MSFT','DELL','AMKR','STX','WDC') "
        "GROUP BY ticker").fetchall()
    con.close()
    print(f"DONE: accounts_payable filled for {n} rows / {ncomp} companies")
    print("key coverage:", dict(key))


if __name__ == "__main__":
    main()
