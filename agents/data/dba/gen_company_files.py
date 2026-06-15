"""
Generate per-company markdown files for the section agent folders, populated
from financials.db (real, sourced financial data — Yahoo/SEC, Tier B/A).

- Reads company_universe.csv (section, company, ticker, country)
- For each company WITHOUT an existing file in its section's companies/ folder,
  writes <slug>.md using the DBA company_template structure with a Financial
  Profile table filled from the latest annual + quarterly rows in financials.db.
- NEVER overwrites an existing hand-curated file.

Run: python3 gen_company_files.py        (dry run — lists what it would create)
     python3 gen_company_files.py --write (create the files)
"""
import csv, sqlite3, re, sys, datetime
from pathlib import Path

HERE = Path(__file__).parent
SECTION_DIR = HERE.parent.parent / "section"   # agents/data/dba → agents → section
CSV = HERE / "company_universe.csv"
DB = HERE / "financials.db"
WRITE = "--write" in sys.argv
TODAY = datetime.date.today().isoformat()

SECTION_LABEL = {
    'ai_chip':'AI Chip','ai_platforms':'AI Platforms','ai_software':'AI Software',
    'components':'Components','cooling':'Cooling','cpu':'CPU','dram':'DRAM','energy':'Energy',
    'foundry':'Foundry','hw_equipment':'HW Equipment','hyperscalers':'Hyperscalers',
    'materials':'Materials','nand':'NAND','neocloud':'Neocloud','osat_packaging':'OSAT / Packaging',
    'server_networking':'Server Networking','server_oem_ems_odm':'Server OEM/EMS/ODM',
    'sw_equipment':'SW Equipment',
}
ROLE = {
    'ai_chip':'AI accelerator / GPU silicon','ai_platforms':'Enterprise AI software platform',
    'ai_software':'AI model / application developer','components':'Component / board-level supplier',
    'cooling':'Datacenter thermal management','cpu':'Host CPU / IP cores','dram':'DRAM / HBM memory',
    'energy':'Datacenter power & grid','foundry':'Semiconductor foundry',
    'hw_equipment':'Fab equipment','hyperscalers':'Hyperscale cloud / CSP capex',
    'materials':'Semiconductor materials & chemicals','nand':'NAND flash / storage',
    'neocloud':'GPU-cloud specialist','osat_packaging':'Assembly & advanced packaging',
    'server_networking':'Switch ASIC / optical networking',
    'server_oem_ems_odm':'AI server / rack builder','sw_equipment':'EDA / design software',
}


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def fmtM(v):
    if v is None: return "—"
    if abs(v) >= 1000: return f"${v/1000:.2f}B"
    return f"${v:.0f}M"


def existing_stems(section):
    d = SECTION_DIR / section / "companies"
    if not d.exists(): return set()
    return {p.stem for p in d.glob("*.md")}


def existing_tickers(section):
    """Set of bare ticker symbols already covered by hand-written files in this section."""
    d = SECTION_DIR / section / "companies"
    if not d.exists(): return set()
    syms = set()
    for p in d.glob("*.md"):
        try:
            for line in p.read_text().splitlines():
                if line.strip().startswith("**Ticker:**"):
                    # extract alphanumeric symbols from e.g. "NYSE:TSM / TWSE:2330"
                    for tok in re.findall(r"[A-Za-z0-9]+", line.split("**Ticker:**")[1]):
                        if tok not in ("NASDAQ","NYSE","KRX","TWSE","TYO","TPE","HKEX",
                                       "SSE","SZSE","ETR","EPA","Private","KOSDAQ"):
                            syms.add(tok.upper())
                    break
        except Exception:
            pass
    return syms


def ticker_core(t):
    return t.split(".")[0].upper()   # "005930.KS" → "005930", "NVDA" → "NVDA"


def latest_rows(con, ticker):
    a = con.execute("""SELECT fiscal_year,revenue_usd_m,gross_margin_pct,net_income_usd_m,
        capex_usd_m,fcf_usd_m,inventory_usd_m,total_debt_usd_m,stockholders_equity_usd_m,
        total_assets_usd_m,source_doc FROM annual_financials WHERE ticker=?
        ORDER BY fiscal_year DESC LIMIT 1""", (ticker,)).fetchone()
    q = con.execute("""SELECT calendar_quarter,revenue_usd_m,gross_margin_pct,net_income_usd_m,
        capex_usd_m,source_doc FROM quarterly_financials WHERE ticker=?
        ORDER BY period_end_date DESC LIMIT 1""", (ticker,)).fetchone()
    px = con.execute("""SELECT close_usd,currency,price_date FROM stock_prices WHERE ticker=?
        ORDER BY price_date DESC LIMIT 1""", (ticker,)).fetchone()
    return a, q, px


def build_md(section, name, ticker, country, a, q, px):
    label = SECTION_LABEL.get(section, section)
    role = ROLE.get(section, "AI supply-chain participant")
    fin_rows = []
    if a:
        fy=a[0]
        fin_rows.append(f"| Revenue | {fmtM(a[1])} | FY{fy} | Yahoo Finance annual statements |")
        fin_rows.append(f"| Gross Margin | {a[2]:.1f}% | FY{fy} | Yahoo Finance annual statements |" if a[2] is not None else "| Gross Margin | — | — | — |")
        fin_rows.append(f"| Net Income | {fmtM(a[3])} | FY{fy} | Yahoo Finance annual statements |")
        fin_rows.append(f"| Capex | {fmtM(a[4])} | FY{fy} | Yahoo Finance cash-flow statement |")
        fin_rows.append(f"| Free Cash Flow | {fmtM(a[5])} | FY{fy} | Yahoo Finance cash-flow statement |")
        fin_rows.append(f"| Inventory | {fmtM(a[6])} | FY{fy} | Yahoo Finance balance sheet |")
        fin_rows.append(f"| Total Debt | {fmtM(a[7])} | FY{fy} | Yahoo Finance balance sheet |")
        fin_rows.append(f"| Stockholders' Equity | {fmtM(a[8])} | FY{fy} | Yahoo Finance balance sheet |")
        fin_rows.append(f"| Total Assets | {fmtM(a[9])} | FY{fy} | Yahoo Finance balance sheet |")
    if q:
        fin_rows.append(f"| Revenue (latest Q) | {fmtM(q[1])} | {q[0]} | Yahoo Finance / SEC filing |")
    if not fin_rows:
        fin_rows.append("| Revenue | _no data_ | — | — |")
    fin_table = "\n".join(fin_rows)
    price_line = ""
    if px:
        price_line = f"\n**Latest close:** {px[0]:.2f} {px[1]} (as of {px[2]}) — Source: Yahoo Finance (yfinance)\n"
    src = (a[10] if a else (q[5] if q else "Yahoo Finance"))

    return f"""# {name}

**Segment(s):** {section}
**Role in AI SCM:** {role}
**HQ:** {country}
**Ticker:** {ticker}
**Last Updated:** {TODAY}

---

## Company Overview

{name} ({ticker}) is a tracked public company in the **{label}** section of the AI
supply chain. Detailed product and supply-chain narrative to be populated from
primary sources (10-K/10-Q, IR, analyst research) per the DBA source rules.
{price_line}
**Source:** Company registry — `agents/data/dba/company_universe.csv`

---

## Key Products & AI Relevance

| Product / Technology | AI Use Case | Market Position |
|---|---|---|
| _to be populated_ | _to be populated_ | _to be populated_ |

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
{fin_table}

**Source:** {src}
_Financial figures auto-populated from `agents/data/dba/financials.db` (Tier B —
Yahoo-aggregated from filings). Verify against the primary 10-K/10-Q for Tier-A use._

---

## Supply Chain Position
_To be populated from primary sources._

---

## Updates

[Newest first. Each entry must have a date, source, and full tag set per the DBA schema.]

### Update: {TODAY} — Company file created from financials.db

> Auto-generated registry entry with latest available financial profile.

**Source:** financials.db build, {TODAY}

#segment:{section} #source-tier:B #signal-type:earnings #company:{slugify(name).replace('_','-')} #date:{TODAY} #importance:low #confidence:medium

---

## Open Questions

- [ ] Populate product/technology and supply-chain narrative from primary sources
- [ ] Add AI demand signals and competitive positioning
- [ ] Upgrade financial figures to Tier-A (SEC 10-K/10-Q) where material
"""


def main():
    con = sqlite3.connect(DB)
    created = skipped = 0
    by_section = {}
    for row in csv.DictReader(open(CSV)):
        by_section.setdefault(row["section"], []).append(row)

    for section, comps in sorted(by_section.items()):
        stems = existing_stems(section)
        tickers = existing_tickers(section)
        cdir = SECTION_DIR / section / "companies"
        for r in comps:
            name, ticker, country = r["company_name"], r["ticker"], r["country"]
            slug = slugify(name)
            core = ticker_core(ticker)
            # skip if already covered: ticker match (authoritative) OR slug match
            if core in tickers or slug in stems or \
               any(s in slug or slug in s for s in stems if len(s) > 3):
                skipped += 1
                continue
            a, q, px = latest_rows(con, ticker)
            md = build_md(section, name, ticker, country, a, q, px)
            target = cdir / f"{slug}.md"
            if WRITE:
                cdir.mkdir(parents=True, exist_ok=True)
                target.write_text(md)
            created += 1
            print(f"  {'WROTE' if WRITE else 'would create'}: {section}/companies/{slug}.md")
    con.close()
    print(f"\n{'Created' if WRITE else 'Would create'} {created} files · skipped {skipped} existing")


if __name__ == "__main__":
    main()
