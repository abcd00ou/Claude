"""
Export script — builds dashboard_data.js from the DBA databases.

Reads:
  - agents/data/dba/financials.db   (companies, quarterly_financials, stock_prices, earnings_commentary)
  - agents/data/dba/intelligence.db (companies — AI SCM segment intelligence)

Writes:
  - agents/data/dba/dashboard/dashboard_data.js   (window.DASHBOARD_DATA = {...})

The dashboard HTML loads this JS file directly (no server / no SQLite-in-browser needed).

Run: python3 export_dashboard_data.py
"""
import sqlite3
import json
import re
from pathlib import Path

HERE       = Path(__file__).parent
FIN_DB     = HERE / "financials.db"
INTEL_DB   = HERE / "intelligence.db"
OUT_DIR    = HERE / "dashboard"
OUT_JS     = OUT_DIR / "dashboard_data.js"


def rows(con, sql, params=()):
    con.row_factory = sqlite3.Row
    return [dict(r) for r in con.execute(sql, params).fetchall()]


# ── Map intelligence.db company-name variants → financials.db slug ───────────
# A company may appear under several names/segments in intelligence.db.
NAME_TO_SLUG = {
    "amd": "amd",
    "ase group": "ase_group", "ase technology": "ase_group",
    "at&s": None,                       # no ticker tracked
    "alphabet (google)": "google", "google": "google",
    "amazon (aws)": "amazon", "amazon aws": "amazon",
    "amkor": "amkor", "amkor technology": "amkor",
    "arista": "arista",
    "broadcom": "broadcom",
    "caterpillar": "caterpillar",
    "coherent / lumentum / fabrinet": "coherent",
    "coreweave": "coreweave",
    "cummins": "cummins",
    "eaton": "eaton",
    "ibiden": "ibiden",
    "infineon": "infineon",
    "intel": "intel", "intel foundry": "intel",
    "kioxia": "kioxia",
    "mps": "mps",
    "marvell": "marvell",
    "meta": "meta",
    "micron": "micron",
    "microsoft": "microsoft", "microsoft (azure)": "microsoft",
    "nvidia": "nvidia", "nvidia (networking)": "nvidia",
    "on semiconductor": "on_semi",
    "pure storage": "pure_storage",
    "renesas": None,                    # no ticker tracked
    "sk hynix": "sk_hynix", "sk hynix / solidigm": "sk_hynix",
    "stmicroelectronics": "stmicro",
    "samsung": "samsung", "samsung foundry": "samsung",
    "sandisk (wd spin-off)": "sandisk",
    "schneider electric": "schneider",
    "shinko electric": None,            # no ticker tracked
    "tsmc": "tsmc",
    "texas instruments": "texas_instruments",
    "unimicron": "unimicron",
    "vertiv": "vertiv",
    "wolfspeed": "wolfspeed",
    "xai": None,                        # private
}


def main():
    OUT_DIR.mkdir(exist_ok=True)
    fin   = sqlite3.connect(FIN_DB)
    intel = sqlite3.connect(INTEL_DB)

    companies = rows(fin, "SELECT * FROM companies ORDER BY name")

    # group SCM intelligence rows by slug
    scm_by_slug = {}
    for r in rows(intel, "SELECT * FROM companies"):
        key = r["company"].strip().lower()
        slug = NAME_TO_SLUG.get(key)
        if not slug:
            continue
        scm_by_slug.setdefault(slug, []).append({
            "segment":  r.get("segment"),
            "role":     r.get("role"),
            "share":    f'{r.get("share_metric") or ""}: {r.get("share_value") or ""}'.strip(": ").strip(),
            "revenue":  r.get("latest_revenue"),
            "signal":   r.get("key_signal"),
            "sourced":  r.get("last_sourced"),
        })

    data = {"companies": [], "generated_at": None}

    for c in companies:
        slug = c["slug"]
        ticker = c["ticker"]

        qfin = rows(fin, """
            SELECT calendar_quarter, period_end_date, fiscal_year, fiscal_quarter,
                   revenue_usd_m, revenue_ai_dc_usd_m, revenue_yoy_pct,
                   gross_margin_pct, operating_income_usd_m, net_income_usd_m,
                   capex_usd_m, revenue_guidance_low_usd_m, revenue_guidance_high_usd_m,
                   source_doc, source_date, importance, notes
            FROM quarterly_financials WHERE ticker=? ORDER BY period_end_date
        """, (ticker,))

        prices = rows(fin, """
            SELECT price_date, open_usd, high_usd, low_usd, close_usd,
                   adj_close_usd, volume, currency
            FROM stock_prices WHERE ticker=? ORDER BY price_date
        """, (ticker,))

        commentary = rows(fin, """
            SELECT earnings_date, calendar_quarter, quote, speaker,
                   signal_type, segment, source_doc
            FROM earnings_commentary WHERE ticker=? ORDER BY earnings_date DESC
        """, (ticker,))

        data["companies"].append({
            "slug": slug,
            "ticker": ticker,
            "name": c["name"],
            "exchange": c["exchange"],
            "segments": c["segments"].split(",") if c["segments"] else [],
            "hq_country": c["hq_country"],
            "fiscal_year_end": c["fiscal_year_end"],
            "currency": prices[-1]["currency"] if prices else "USD",
            "scm": scm_by_slug.get(slug, []),
            "financials": qfin,
            "prices": prices,
            "commentary": commentary,
        })

    from datetime import datetime
    data["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    OUT_JS.write_text("window.DASHBOARD_DATA = " + json.dumps(data, ensure_ascii=False) + ";\n")
    fin.close(); intel.close()

    n = len(data["companies"])
    px = sum(len(c["prices"]) for c in data["companies"])
    qf = sum(len(c["financials"]) for c in data["companies"])
    scm = sum(len(c["scm"]) for c in data["companies"])
    print(f"✅ {OUT_JS}")
    print(f"   {n} companies · {qf} financial rows · {px} price points · {scm} SCM rows")
    matched = sum(1 for c in data["companies"] if c["scm"])
    print(f"   {matched}/{n} companies have SCM intelligence matched")


if __name__ == "__main__":
    main()
