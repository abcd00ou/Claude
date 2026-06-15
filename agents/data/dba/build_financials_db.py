"""
Build script — agents/data/dba/financials.db

Per DBA schema: agents/data/dba/schema/financials_schema.md

Tables:
  1. companies            — master registry of AI SCM companies (public, tradeable)
  2. quarterly_financials — 10-Q/10-K/20-F sourced quarterly data (Tier A)
  3. stock_prices         — daily OHLCV from yfinance (Tier B)
  4. earnings_commentary  — verbatim earnings-call quotes (Tier A)

Seeded from:
  - agents/data/analysis/models/company_master.md  (Cycle 9, Tier A/B figures)
  - agents/data/analysis/models/market_data.md     (capex/revenue, Tier A)
  - yfinance live API                              (stock prices)

Run: python3 build_financials_db.py              (registry + curated Tier-A financials, no network)
     python3 build_financials_db.py --prices     (also pull daily stock prices via yfinance)
     python3 build_financials_db.py --financials  (also pull quarterly income statements, Tier B)
     python3 build_financials_db.py --all         (prices + financials)
"""
import sqlite3
import sys
from datetime import datetime, date, timedelta
from pathlib import Path

HERE   = Path(__file__).parent
DB_PATH = HERE / "financials.db"

PULL_PRICES     = "--prices" in sys.argv or "--all" in sys.argv
PULL_FINANCIALS = "--financials" in sys.argv or "--all" in sys.argv

HISTORY_START = "2020-01-01"   # baseline per financials_schema.md Historical Coverage


def conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


# ══════════════════════════════════════════════════════════════════════════════
# COMPANY REGISTRY  — loaded from company_universe.csv (source: user's
# company_master.xlsx, 136 companies across 18 AI-SCM sections).
# ticker (Yahoo symbol) is the primary key; exchange/currency derived from suffix.
# ══════════════════════════════════════════════════════════════════════════════
import csv as _csv
import re as _re

CSV_PATH = HERE / "company_universe.csv"

# Yahoo ticker suffix → (exchange code, trading currency)
SUFFIX_EXCH = {
    ".KS": ("KRX", "KRW"), ".KQ": ("KOSDAQ", "KRW"), ".T": ("TYO", "JPY"),
    ".TW": ("TPE", "TWD"), ".HK": ("HKEX", "HKD"), ".SS": ("SSE", "CNY"),
    ".SZ": ("SZSE", "CNY"), ".VI": ("VIE", "EUR"), ".AS": ("AMS", "EUR"),
    ".SW": ("SWX", "CHF"), ".ST": ("STO", "SEK"), ".MC": ("BME", "EUR"),
    ".DE": ("XETRA", "EUR"), ".PA": ("EPA", "EUR"), ".L": ("LSE", "GBP"),
}
HQ_ISO = {
    "United States":"US","Taiwan":"TW","South Korea":"KR","Japan":"JP","China":"CN",
    "Netherlands":"NL","Germany":"DE","France":"FR","Switzerland":"CH","Sweden":"SE",
    "Austria":"AT","Ireland":"IE","Canada":"CA","Spain":"ES","Finland":"FI",
    "United Kingdom":"GB","Singapore":"SG","Thailand":"TH",
}


def _slugify(name: str) -> str:
    s = name.lower()
    s = _re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s


def _exch_ccy(ticker: str):
    for suf, (exch, ccy) in SUFFIX_EXCH.items():
        if ticker.endswith(suf):
            return exch, ccy
    return "US", "USD"   # plain US ticker, no suffix


def load_companies():
    """Return (COMPANIES list of tuples, YF_SYMBOLS dict) from company_universe.csv."""
    companies, yf_syms, slugs = [], {}, set()
    with open(CSV_PATH) as f:
        for row in _csv.DictReader(f):
            ticker = row["ticker"].strip()
            name = row["company_name"].strip()
            section = row["section"].strip()
            country = row["country"].strip()
            exch, _ = _exch_ccy(ticker)
            slug = _slugify(name)
            while slug in slugs:           # ensure unique slug
                slug += "_x"
            slugs.add(slug)
            companies.append((ticker, slug, name, exch, section,
                              HQ_ISO.get(country, country[:2].upper()), 1, None))
            yf_syms[ticker] = ticker        # Yahoo symbol == ticker (already Yahoo format)
    return companies, yf_syms


COMPANIES, YF_SYMBOLS = load_companies()


# ══════════════════════════════════════════════════════════════════════════════
# QUARTERLY FINANCIALS  (Tier A — from Cycle 9 company_master.md / market_data.md)
# Only figures explicitly stated in the source MD files (which cite 10-Q/10-K/IR).
# Facts-only: every row carries source_doc citation.
# ══════════════════════════════════════════════════════════════════════════════
# dict per row; None where not disclosed in source
QFIN = [
    # NVIDIA — Q1 FY2027 (period ended Apr 2026)
    dict(ticker="NVDA", fy=2027, fq=1, period_end="2026-04-26", cq="2026-Q1",
         rev=None, rev_ai_dc=72000, rev_yoy=None, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Q1 FY2027 Earnings Release, NVIDIA Corporation, 2026-05-28, IR",
         src_date="2026-05-28", imp="high",
         note="Data Center revenue guidance ~$72B+; GB300 +129% YoY; 60K racks FY2026"),
    # AMD — Q1 2026
    dict(ticker="AMD", fy=2026, fq=1, period_end="2026-03-28", cq="2026-Q1",
         rev=None, rev_ai_dc=5800, rev_yoy=57.0, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Q1 2026 Earnings Release, Advanced Micro Devices, 2026-05-05, IR",
         src_date="2026-05-05", imp="high",
         note="Data Center segment $5.8B (+57% YoY); MI450 sampling"),
    # Intel — Q1 2026
    dict(ticker="INTC", fy=2026, fq=1, period_end="2026-03-28", cq="2026-Q1",
         rev=13600, rev_ai_dc=5100, rev_yoy=None, gm=None, op=-2437, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Form 10-Q Q1 2026, Intel Corporation, 2026-04-23, SEC EDGAR",
         src_date="2026-04-23", imp="high",
         note="Total rev $13.6B; DC&AI $5.1B (+22%); Foundry op loss -$2.437B"),
    # TSMC — Q1 2026
    dict(ticker="TSM", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
         rev=35900, rev_ai_dc=None, rev_yoy=35.1, gm=66.2, op=None, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Q1 2026 Earnings Release, TSMC, 2026-04-16, IR",
         src_date="2026-04-16", imp="high",
         note="Revenue $35.9B (+35.1% YoY); gross margin 66.2%"),
    # Micron — FQ2 2026
    dict(ticker="MU", fy=2026, fq=2, period_end="2026-02-26", cq="2026-Q1",
         rev=23860, rev_ai_dc=None, rev_yoy=196.0, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Form 10-Q FQ2 2026, Micron Technology, 2026-03-25, SEC EDGAR",
         src_date="2026-03-25", imp="high",
         note="Revenue $23.86B (+196% YoY); record; demand significantly in excess of supply"),
    # Pure Storage — FQ1 FY2027
    dict(ticker="PSTG", fy=2027, fq=1, period_end="2026-05-04", cq="2026-Q1",
         rev=1053, rev_ai_dc=None, rev_yoy=35.0, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=4410, guid_hi=4510,
         src="Q1 FY2027 Earnings Release, Pure Storage, 2026-05-27, IR",
         src_date="2026-05-27", imp="medium",
         note="Revenue $1.053B (+35% YoY); FY2027 guidance $4.41-4.51B; product rev +55% YoY"),
    # Vertiv — Q1 2026
    dict(ticker="VRT", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
         rev=2650, rev_ai_dc=None, rev_yoy=30.0, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=13500, guid_hi=14000,
         src="Form 10-Q Q1 2026, Vertiv Holdings, 2026-05-01, SEC EDGAR",
         src_date="2026-05-01", imp="high",
         note="Revenue $2.65B (+30% YoY); backlog $12.45B (+81%); FY2026 guide $13.5-14B"),
    # Eaton — Q1 2026
    dict(ticker="ETN", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
         rev=7500, rev_ai_dc=None, rev_yoy=17.0, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Form 10-Q Q1 2026, Eaton Corporation, 2026-05-05, SEC EDGAR",
         src_date="2026-05-05", imp="high",
         note="Revenue $7.5B (+17% YoY); DC orders +240% YoY; 32 GW US DC under construction"),
    # Arista — Q1 2026
    dict(ticker="ANET", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
         rev=2709, rev_ai_dc=None, rev_yoy=35.0, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Form 10-Q Q1 2026, Arista Networks, 2026-05-05, SEC EDGAR",
         src_date="2026-05-05", imp="medium",
         note="Revenue $2.709B (+35% YoY); FY2026 $11.5B target; AI fabric target $3.5B"),
    # MPS — Q1 2026
    dict(ticker="MPWR", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
         rev=None, rev_ai_dc=262.8, rev_yoy=97.7, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Form 10-Q Q1 2026, Monolithic Power Systems, 2026-05-06, SEC EDGAR",
         src_date="2026-05-06", imp="medium",
         note="Enterprise Data $262.8M (+97.7% YoY); sold-out; LT target raised to $6B"),
    # Hyperscaler capex (from market_data.md; Tier A 10-Q)
    dict(ticker="AMZN", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
         rev=None, rev_ai_dc=37600, rev_yoy=28.0, gm=None, op=None, ni=None, eps=None,
         capex=44200, guid_lo=None, guid_hi=None,
         src="Form 10-Q Q1 2026, Amazon.com Inc., 2026-04-29, SEC EDGAR",
         src_date="2026-04-29", imp="high",
         note="Q1 capex $44.2B (+77% YoY); AWS rev $37.6B (+28%); backlog $364B; ~$200B FY2026 capex"),
    dict(ticker="MSFT", fy=2026, fq=3, period_end="2026-03-31", cq="2026-Q1",
         rev=None, rev_ai_dc=None, rev_yoy=None, gm=None, op=None, ni=None, eps=None,
         capex=37500, guid_lo=None, guid_hi=None,
         src="Form 10-Q FQ3 2026, Microsoft Corporation, 2026-04-29, SEC EDGAR",
         src_date="2026-04-29", imp="high",
         note="Q1-cal capex $37.5B (+53% YoY); Azure AI ARR $37B (+123% YoY); ~$190B FY2026 capex"),
    dict(ticker="GOOGL", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
         rev=None, rev_ai_dc=20000, rev_yoy=63.0, gm=None, op=None, ni=None, eps=None,
         capex=35700, guid_lo=None, guid_hi=None,
         src="Form 10-Q Q1 2026, Alphabet Inc., 2026-04-29, SEC EDGAR",
         src_date="2026-04-29", imp="high",
         note="Q1 capex $35.7B (+107%); Cloud $20B (+63% YoY); backlog $462B; $180-190B FY2026 capex"),
    dict(ticker="META", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
         rev=None, rev_ai_dc=None, rev_yoy=None, gm=None, op=None, ni=None, eps=None,
         capex=19840, guid_lo=None, guid_hi=None,
         src="Form 10-Q Q1 2026, Meta Platforms Inc., 2026-04-29, SEC EDGAR",
         src_date="2026-04-29", imp="high",
         note="Q1 capex $19.84B (+61% YoY); $125-145B FY2026 capex; 1 GW MTIA deployment committed"),
]


# ══════════════════════════════════════════════════════════════════════════════
# EARNINGS COMMENTARY  (Tier A verbatim quotes)
# ══════════════════════════════════════════════════════════════════════════════
COMMENTARY = [
    dict(ticker="MU", date="2026-03-25", cq="2026-Q1",
         quote="Demand is significantly in excess of supply.",
         speaker="CFO", signal="demand", segment="storage",
         src="FQ2 2026 Earnings Call, Micron Technology, 2026-03-25, IR",
         imp="high"),
    dict(ticker="VRT", date="2026-05-01", cq="2026-Q1",
         quote="Liquid cooling has become the default for new AI data center deployments.",
         speaker="CEO", signal="demand", segment="dc_infra",
         src="Q1 2026 Earnings Call, Vertiv Holdings, 2026-05-01, IR",
         imp="high"),
    dict(ticker="GOOGL", date="2026-04-29", cq="2026-Q1",
         quote="We expect capital expenditures to significantly increase in 2027.",
         speaker="CFO", signal="capex", segment="end_market",
         src="Q1 2026 Earnings Call, Alphabet Inc., 2026-04-29, IR",
         imp="high"),
]


# ══════════════════════════════════════════════════════════════════════════════
# BUILD
# ══════════════════════════════════════════════════════════════════════════════
def build_schema(cur):
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS companies (
        ticker          TEXT PRIMARY KEY,
        slug            TEXT UNIQUE NOT NULL,
        name            TEXT NOT NULL,
        exchange        TEXT,
        segments        TEXT,
        hq_country      TEXT,
        is_public       INTEGER DEFAULT 1,
        fiscal_year_end TEXT
    );

    CREATE TABLE IF NOT EXISTS quarterly_financials (
        id                        INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker                    TEXT NOT NULL REFERENCES companies(ticker),
        fiscal_year               INTEGER NOT NULL,
        fiscal_quarter            INTEGER NOT NULL,
        period_end_date           TEXT,
        calendar_quarter          TEXT,
        revenue_usd_m             REAL,
        revenue_ai_dc_usd_m       REAL,
        revenue_yoy_pct           REAL,
        gross_profit_usd_m        REAL,
        gross_margin_pct          REAL,
        operating_income_usd_m    REAL,
        net_income_usd_m          REAL,
        eps_diluted               REAL,
        cash_usd_m                REAL,
        capex_usd_m               REAL,
        fcf_usd_m                 REAL,
        operating_cash_flow_usd_m REAL,
        inventory_usd_m           REAL,
        receivables_usd_m         REAL,
        total_assets_usd_m        REAL,
        total_debt_usd_m          REAL,
        stockholders_equity_usd_m REAL,
        revenue_guidance_low_usd_m  REAL,
        revenue_guidance_high_usd_m REAL,
        source_tier               TEXT,
        source_doc                TEXT,
        source_date               TEXT,
        source_url                TEXT,
        signal_type               TEXT DEFAULT 'earnings',
        importance                TEXT,
        confidence                TEXT DEFAULT 'high',
        notes                     TEXT,
        created_at                TEXT DEFAULT (datetime('now')),
        UNIQUE(ticker, fiscal_year, fiscal_quarter)
    );

    CREATE TABLE IF NOT EXISTS stock_prices (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker           TEXT NOT NULL REFERENCES companies(ticker),
        price_date       TEXT NOT NULL,
        open_usd         REAL,
        high_usd         REAL,
        low_usd          REAL,
        close_usd        REAL,
        adj_close_usd    REAL,
        volume           INTEGER,
        market_cap_usd_b REAL,
        currency         TEXT DEFAULT 'USD',
        source_tier      TEXT DEFAULT 'B',
        source_doc       TEXT,
        source_date      TEXT,
        UNIQUE(ticker, price_date)
    );

    CREATE TABLE IF NOT EXISTS earnings_commentary (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker           TEXT NOT NULL REFERENCES companies(ticker),
        earnings_date    TEXT,
        calendar_quarter TEXT,
        quote            TEXT,
        speaker          TEXT,
        signal_type      TEXT,
        segment          TEXT,
        source_tier      TEXT DEFAULT 'A',
        source_doc       TEXT,
        source_date      TEXT,
        importance       TEXT,
        confidence       TEXT DEFAULT 'high'
    );

    CREATE TABLE IF NOT EXISTS annual_financials (
        id                     INTEGER PRIMARY KEY AUTOINCREMENT,
        ticker                 TEXT NOT NULL REFERENCES companies(ticker),
        fiscal_year            INTEGER NOT NULL,
        period_end_date        TEXT,
        revenue_usd_m          REAL,
        gross_profit_usd_m     REAL,
        gross_margin_pct       REAL,
        operating_income_usd_m REAL,
        net_income_usd_m       REAL,
        eps_diluted            REAL,
        capex_usd_m            REAL,
        fcf_usd_m              REAL,
        operating_cash_flow_usd_m REAL,
        cash_usd_m             REAL,
        inventory_usd_m        REAL,
        receivables_usd_m      REAL,
        total_assets_usd_m     REAL,
        total_debt_usd_m       REAL,
        stockholders_equity_usd_m REAL,
        source_tier            TEXT DEFAULT 'B',
        source_doc             TEXT,
        source_date            TEXT,
        notes                  TEXT,
        created_at             TEXT DEFAULT (datetime('now')),
        UNIQUE(ticker, fiscal_year)
    );

    CREATE INDEX IF NOT EXISTS idx_qfin_ticker  ON quarterly_financials(ticker, calendar_quarter);
    CREATE INDEX IF NOT EXISTS idx_afin_ticker  ON annual_financials(ticker, fiscal_year);
    CREATE INDEX IF NOT EXISTS idx_price_ticker ON stock_prices(ticker, price_date DESC);
    """)


def seed_companies(cur):
    cur.executemany("""
        INSERT OR REPLACE INTO companies
            (ticker, slug, name, exchange, segments, hq_country, is_public, fiscal_year_end)
        VALUES (?,?,?,?,?,?,?,?)
    """, COMPANIES)
    print(f"  companies: {len(COMPANIES)} rows")


def seed_financials(cur):
    for r in QFIN:
        cur.execute("""
            INSERT OR REPLACE INTO quarterly_financials
                (ticker, fiscal_year, fiscal_quarter, period_end_date, calendar_quarter,
                 revenue_usd_m, revenue_ai_dc_usd_m, revenue_yoy_pct,
                 gross_margin_pct, operating_income_usd_m, net_income_usd_m, eps_diluted,
                 capex_usd_m, revenue_guidance_low_usd_m, revenue_guidance_high_usd_m,
                 source_tier, source_doc, source_date, signal_type, importance, confidence, notes)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            r["ticker"], r["fy"], r["fq"], r["period_end"], r["cq"],
            r["rev"], r["rev_ai_dc"], r["rev_yoy"],
            r["gm"], r["op"], r["ni"], r["eps"],
            r["capex"], r["guid_lo"], r["guid_hi"],
            "A", r["src"], r["src_date"], "earnings", r["imp"], "high", r["note"],
        ))
    print(f"  quarterly_financials: {len(QFIN)} rows")


def seed_commentary(cur):
    cur.execute("DELETE FROM earnings_commentary")  # idempotent — no natural unique key
    for c in COMMENTARY:
        cur.execute("""
            INSERT INTO earnings_commentary
                (ticker, earnings_date, calendar_quarter, quote, speaker,
                 signal_type, segment, source_tier, source_doc, source_date, importance, confidence)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            c["ticker"], c["date"], c["cq"], c["quote"], c["speaker"],
            c["signal"], c["segment"], "A", c["src"], c["date"], c["imp"], "high",
        ))
    print(f"  earnings_commentary: {len(COMMENTARY)} rows")


# YF_SYMBOLS is built from company_universe.csv in load_companies() above.
# Trading currency is derived from the Yahoo ticker suffix.


def _ticker_ccy(ticker: str) -> str:
    return _exch_ccy(ticker)[1]


def seed_prices(cur):
    try:
        import yfinance as yf
    except ImportError:
        print("  stock_prices: SKIPPED (yfinance not installed)")
        return
    today = date.today().isoformat()
    start = HISTORY_START   # full daily history from 2020-01-01 baseline
    inserted = 0
    for ticker, yf_sym in YF_SYMBOLS.items():
        ccy = _ticker_ccy(ticker)
        try:
            df = yf.download(yf_sym, start=start, progress=False, auto_adjust=False)
            if df is None or df.empty:
                print(f"    {ticker} ({yf_sym}): no data")
                continue
            cnt = 0
            for idx, row in df.iterrows():
                d = idx.strftime("%Y-%m-%d")
                def g(col):
                    v = row.get(col)
                    try:
                        fv = float(v.iloc[0]) if hasattr(v, "iloc") else float(v)
                        return fv if fv == fv else None  # NaN check
                    except Exception:
                        return None
                cur.execute("""
                    INSERT OR IGNORE INTO stock_prices
                        (ticker, price_date, open_usd, high_usd, low_usd, close_usd,
                         adj_close_usd, volume, currency, source_tier, source_doc, source_date)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    ticker, d, g("Open"), g("High"), g("Low"), g("Close"),
                    g("Adj Close"), int(g("Volume") or 0), ccy, "B",
                    f"Yahoo Finance API (yfinance), {yf_sym}, retrieved {today}", today,
                ))
                cnt += 1
            inserted += cnt
            print(f"    {ticker} ({yf_sym}): {cnt} days")
        except Exception as e:
            print(f"    {ticker} ({yf_sym}): ERROR {e}")
    print(f"  stock_prices: {inserted} rows total")


# ── statement field readers ──────────────────────────────────────────────────
def _cell(df, name, col):
    """Safe read of df.loc[name].iloc[col] → float or None (NaN-guarded)."""
    try:
        if df is not None and not df.empty and name in df.index and col < df.shape[1]:
            v = float(df.loc[name].iloc[col])
            return v if v == v else None
    except Exception:
        return None
    return None


def _M(v):
    return v / 1e6 if v is not None else None


def _extract_period(inc, bal, cfl, col, pend):
    """Build a dict of all financial fields for one period column.
    inc/bal/cfl are the income/balance/cashflow DataFrames; pend is the period date."""
    rev = _cell(inc, "Total Revenue", col)
    gp  = _cell(inc, "Gross Profit", col)
    op  = _cell(inc, "Operating Income", col)
    ni  = _cell(inc, "Net Income", col)
    eps = _cell(inc, "Diluted EPS", col)
    gm  = round(gp/rev*100, 1) if (gp and rev) else None
    # cash flow (match by same period end date when possible)
    bcol = _match_col(bal, pend)
    ccol = _match_col(cfl, pend)
    capex = _cell(cfl, "Capital Expenditure", ccol)
    fcf   = _cell(cfl, "Free Cash Flow", ccol)
    ocf   = _cell(cfl, "Operating Cash Flow", ccol)
    inv   = _cell(bal, "Inventory", bcol)
    recv  = _cell(bal, "Receivables", bcol)
    ta    = _cell(bal, "Total Assets", bcol)
    debt  = _cell(bal, "Total Debt", bcol)
    eq    = _cell(bal, "Stockholders Equity", bcol)
    cash  = _cell(bal, "Cash And Cash Equivalents", bcol)
    return dict(rev=_M(rev), gp=_M(gp), gm=gm, op=_M(op), ni=_M(ni), eps=eps,
                capex=_M(abs(capex)) if capex is not None else None,
                fcf=_M(fcf), ocf=_M(ocf), cash=_M(cash), inv=_M(inv),
                recv=_M(recv), ta=_M(ta), debt=_M(debt), eq=_M(eq))


def _match_col(df, pend):
    """Find the column index in df whose period end date == pend (within 5 days)."""
    if df is None or df.empty:
        return None
    for i, c in enumerate(df.columns):
        try:
            if abs((c.date() - pend).days) <= 5:
                return i
        except Exception:
            continue
    return None


def seed_yf_financials(cur):
    """Pull quarterly income + balance sheet + cash flow from yfinance (Tier B).
    INSERT OR IGNORE preserves curated Tier-A rows; Tier-B rows are refreshed each run."""
    try:
        import yfinance as yf
        import warnings
        warnings.filterwarnings("ignore")
    except ImportError:
        print("  quarterly_financials (yf): SKIPPED (yfinance not installed)")
        return
    today = date.today().isoformat()
    cur.execute("DELETE FROM quarterly_financials WHERE source_tier='B'")
    inserted = 0
    for ticker, yf_sym in YF_SYMBOLS.items():
        try:
            t = yf.Ticker(yf_sym)
            inc = t.quarterly_income_stmt
            bal = t.quarterly_balance_sheet
            cfl = t.quarterly_cashflow
            if inc is None or inc.empty:
                print(f"    {ticker} ({yf_sym}): no income stmt")
                continue
            cnt = 0
            for col, period in enumerate(inc.columns):
                if col >= 8:
                    break
                pend = period.date()
                cy, cq = pend.year, (pend.month - 1)//3 + 1
                f = _extract_period(inc, bal, cfl, col, pend)
                if f["rev"] is None and f["ni"] is None:
                    continue
                cur.execute("""
                    INSERT OR IGNORE INTO quarterly_financials
                        (ticker, fiscal_year, fiscal_quarter, period_end_date, calendar_quarter,
                         revenue_usd_m, gross_profit_usd_m, gross_margin_pct,
                         operating_income_usd_m, net_income_usd_m, eps_diluted,
                         cash_usd_m, capex_usd_m, fcf_usd_m, operating_cash_flow_usd_m,
                         inventory_usd_m, receivables_usd_m, total_assets_usd_m,
                         total_debt_usd_m, stockholders_equity_usd_m,
                         source_tier, source_doc, source_date, signal_type,
                         importance, confidence, notes)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    ticker, cy, cq, pend.isoformat(), f"{cy}-Q{cq}",
                    f["rev"], f["gp"], f["gm"], f["op"], f["ni"], f["eps"],
                    f["cash"], f["capex"], f["fcf"], f["ocf"],
                    f["inv"], f["recv"], f["ta"], f["debt"], f["eq"],
                    "B", f"Yahoo Finance quarterly statements (income+balance+cashflow), {yf_sym}, retrieved {today}",
                    today, "earnings", "medium", "medium",
                    "Yahoo-aggregated from filings; verify against 10-Q for Tier-A use",
                ))
                cnt += 1
            inserted += cnt
            print(f"    {ticker} ({yf_sym}): {cnt} quarters")
        except Exception as e:
            print(f"    {ticker} ({yf_sym}): ERROR {e}")
    print(f"  quarterly_financials (yf, Tier B): {inserted} rows total")


def seed_yf_annual_financials(cur):
    """Pull annual income statements from yfinance for ALL companies (Tier B, FY2021+).
    This provides the pre-2025 historical baseline per the Historical Coverage rule."""
    try:
        import yfinance as yf
        import warnings
        warnings.filterwarnings("ignore")
    except ImportError:
        print("  annual_financials: SKIPPED (yfinance not installed)")
        return
    today = date.today().isoformat()
    cur.execute("DELETE FROM annual_financials WHERE source_tier='B'")  # idempotent
    inserted = 0
    for ticker, yf_sym in YF_SYMBOLS.items():
        try:
            t = yf.Ticker(yf_sym)
            inc = t.income_stmt        # annual
            bal = t.balance_sheet
            cfl = t.cashflow
            if inc is None or inc.empty:
                print(f"    {ticker} ({yf_sym}): no annual income stmt")
                continue
            cnt = 0
            for col, period in enumerate(inc.columns):
                fy = period.year
                pend = period.date()
                f = _extract_period(inc, bal, cfl, col, pend)
                if f["rev"] is None and f["ni"] is None:
                    continue
                cur.execute("""
                    INSERT OR IGNORE INTO annual_financials
                        (ticker, fiscal_year, period_end_date, revenue_usd_m,
                         gross_profit_usd_m, gross_margin_pct, operating_income_usd_m,
                         net_income_usd_m, eps_diluted, capex_usd_m, fcf_usd_m,
                         operating_cash_flow_usd_m, cash_usd_m, inventory_usd_m,
                         receivables_usd_m, total_assets_usd_m, total_debt_usd_m,
                         stockholders_equity_usd_m, source_tier, source_doc,
                         source_date, notes)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    ticker, fy, pend.isoformat(),
                    f["rev"], f["gp"], f["gm"], f["op"], f["ni"], f["eps"],
                    f["capex"], f["fcf"], f["ocf"], f["cash"], f["inv"],
                    f["recv"], f["ta"], f["debt"], f["eq"],
                    "B", f"Yahoo Finance annual statements (income+balance+cashflow), {yf_sym}, retrieved {today}",
                    today, "Yahoo-aggregated from 10-K; verify for Tier-A use",
                ))
                cnt += 1
            inserted += cnt
            print(f"    {ticker} ({yf_sym}): {cnt} fiscal years")
        except Exception as e:
            print(f"    {ticker} ({yf_sym}): ERROR {e}")
    print(f"  annual_financials (yf, Tier B): {inserted} rows total")


if __name__ == "__main__":
    db = conn()
    cur = db.cursor()
    print(f"── Building {DB_PATH.name} ──────────────────────────")
    build_schema(cur)
    seed_companies(cur)
    seed_financials(cur)
    seed_commentary(cur)
    if PULL_PRICES:
        print(f"  pulling stock prices (from {HISTORY_START}) via yfinance…")
        seed_prices(cur)
    else:
        print("  stock_prices: SKIPPED (run with --prices to pull)")
    if PULL_FINANCIALS:
        print("  pulling quarterly income statements via yfinance…")
        seed_yf_financials(cur)
        print("  pulling annual income statements (FY2021+) via yfinance…")
        seed_yf_annual_financials(cur)
    else:
        print("  quarterly/annual_financials (yf): SKIPPED (run with --financials to pull)")
    db.commit()
    db.close()
    print(f"\n✅ {DB_PATH}")
