"""
refresh_financials.py — INCREMENTAL financial refresh from SEC EDGAR.

Re-pulls each US-SEC filer's quarterly financials and:
  • UPDATEs existing (ticker, fiscal_year, fiscal_quarter) rows — refreshes the
    numeric columns only, preserving calendar_quarter / source metadata / curated fields.
  • INSERTs genuinely new quarters (e.g. a freshly-filed 10-Q), placing them on the
    existing calendar grid via each ticker's learned fiscal→calendar offset.

This is the safe "증분 최신화" path: no full rebuild, no calendar remapping risk.
Non-US names (mostly .KS/.TW/.T) aren't SEC filers and are left untouched.

Run:  python3 refresh_financials.py
"""
from __future__ import annotations
import sqlite3
from collections import Counter
from pathlib import Path

import edgar_financials as E

DB = Path(__file__).parent / "financials.db"

# edgar row key -> quarterly_financials numeric column
COLMAP = {
    "revenue": "revenue_usd_m", "gross_profit": "gross_profit_usd_m", "gm": "gross_margin_pct",
    "op": "operating_income_usd_m", "ni": "net_income_usd_m", "eps": "eps_diluted",
    "capex": "capex_usd_m", "fcf": "fcf_usd_m", "ocf": "operating_cash_flow_usd_m",
    "cash": "cash_usd_m", "inv": "inventory_usd_m", "recv": "receivables_usd_m",
    "payables": "accounts_payable_usd_m", "ta": "total_assets_usd_m",
    "debt": "total_debt_usd_m", "eq": "stockholders_equity_usd_m",
}
_QN = {1: 1, 2: 2, 3: 3, 4: 4}


def _cq_from_key(k):
    y, q = divmod(k - 1, 4)
    return f"{y}-Q{q + 1}"


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row

    # existing grid + fiscal→calendar offset per ticker
    grid = {}          # (ticker,fy,fq) -> calendar_quarter
    offsets = {}       # ticker -> Counter(calendar_key - fiscal_key)
    for r in con.execute("SELECT ticker, fiscal_year, fiscal_quarter, calendar_quarter "
                         "FROM quarterly_financials WHERE calendar_quarter IS NOT NULL"):
        grid[(r["ticker"], r["fiscal_year"], r["fiscal_quarter"])] = r["calendar_quarter"]
        cy, cq = r["calendar_quarter"].split("-Q")
        ck = int(cy) * 4 + int(cq)
        fk = r["fiscal_year"] * 4 + r["fiscal_quarter"]
        offsets.setdefault(r["ticker"], Counter())[ck - fk] += 1
    off = {t: c.most_common(1)[0][0] for t, c in offsets.items()}

    tickers = [r[0] for r in con.execute("SELECT DISTINCT ticker FROM quarterly_financials")]
    cmap = E.cik_map()
    us = [t for t in tickers if t.upper() in cmap]
    print(f"{len(us)} US-SEC filers → EDGAR incremental refresh", flush=True)

    done = updated = inserted = 0
    for tk in us:
        done += 1
        try:
            _, qrows = E.pull(tk)
        except Exception:
            continue
        for r in qrows:
            fy, fq = r["fiscal_year"], r["fiscal_quarter"]
            sets = {c: r[k] for k, c in COLMAP.items() if r.get(k) is not None}
            if not sets:
                continue
            key = (tk, fy, fq)
            if key in grid:
                assigns = ", ".join(f"{c}=?" for c in sets)
                con.execute(f"UPDATE quarterly_financials SET {assigns} "
                            "WHERE ticker=? AND fiscal_year=? AND fiscal_quarter=?",
                            (*sets.values(), tk, fy, fq))
                updated += 1
            elif tk in off:
                cq = _cq_from_key(fy * 4 + fq + off[tk])
                cols = ["ticker", "fiscal_year", "fiscal_quarter", "calendar_quarter",
                        "period_end_date", "source_tier", "source_doc", *sets.keys()]
                vals = [tk, fy, fq, cq, r.get("period_end"), "A", "SEC EDGAR (refresh)",
                        *sets.values()]
                con.execute(f"INSERT OR IGNORE INTO quarterly_financials "
                            f"({', '.join(cols)}) VALUES ({', '.join('?' * len(cols))})", vals)
                grid[key] = cq
                inserted += 1
        if done % 20 == 0:
            con.commit()
            print(f"  ...{done}/{len(us)}  updated={updated} inserted={inserted}", flush=True)
    con.commit()
    latest = con.execute("SELECT MAX(calendar_quarter) FROM quarterly_financials").fetchone()[0]
    n = con.execute("SELECT COUNT(*) FROM quarterly_financials").fetchone()[0]
    con.close()
    print(f"DONE: updated={updated}, inserted={inserted}, total rows={n}, latest quarter={latest}")


if __name__ == "__main__":
    main()
