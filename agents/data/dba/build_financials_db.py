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


def conn() -> sqlite3.Connection:
    c = sqlite3.connect(DB_PATH)
    c.row_factory = sqlite3.Row
    return c


# ══════════════════════════════════════════════════════════════════════════════
# COMPANY REGISTRY  (public, tradeable AI SCM companies)
# ══════════════════════════════════════════════════════════════════════════════
# (ticker, slug, name, exchange, segments, hq, is_public, fiscal_year_end)
COMPANIES = [
    # ── DRAM / Memory ──
    ("KRX:000660",   "sk_hynix",  "SK Hynix Inc.",                "KRX",    "dram,storage",            "KR", 1, "12-31"),
    ("KRX:005930",   "samsung",   "Samsung Electronics Co.",      "KRX",    "dram,storage,foundry",    "KR", 1, "12-31"),
    ("NASDAQ:MU",    "micron",    "Micron Technology Inc.",       "NASDAQ", "dram,storage",            "US", 1, "08-28"),
    # ── NAND / Storage ──
    ("TYO:285A",     "kioxia",    "Kioxia Holdings Corp.",        "TYO",    "storage",                 "JP", 1, "03-31"),
    ("NASDAQ:SNDK",  "sandisk",   "SanDisk Corporation",          "NASDAQ", "storage",                 "US", 1, "06-27"),
    ("NYSE:PSTG",    "pure_storage","Pure Storage Inc.",          "NYSE",   "storage",                 "US", 1, "02-02"),
    # ── Foundry & Packaging ──
    ("NYSE:TSM",     "tsmc",      "Taiwan Semiconductor Mfg.",    "NYSE",   "foundry",                 "TW", 1, "12-31"),
    ("NASDAQ:INTC",  "intel",     "Intel Corporation",            "NASDAQ", "foundry,chip_maker",      "US", 1, "12-27"),
    ("NASDAQ:AMKR",  "amkor",     "Amkor Technology Inc.",        "NASDAQ", "substrate",               "US", 1, "12-31"),
    ("NYSE:ASX",     "ase_group", "ASE Technology Holding",       "NYSE",   "substrate",               "TW", 1, "12-31"),
    # ── AI Accelerators ──
    ("NASDAQ:NVDA",  "nvidia",    "NVIDIA Corporation",           "NASDAQ", "chip_maker,network",      "US", 1, "01-26"),
    ("NASDAQ:AMD",   "amd",       "Advanced Micro Devices",       "NASDAQ", "chip_maker",              "US", 1, "12-27"),
    # ── Custom Silicon / Networking ──
    ("NASDAQ:GOOGL", "google",    "Alphabet Inc.",                "NASDAQ", "asic,end_market",         "US", 1, "12-31"),
    ("NASDAQ:AMZN",  "amazon",    "Amazon.com Inc.",              "NASDAQ", "asic,end_market",         "US", 1, "12-31"),
    ("NASDAQ:META",  "meta",      "Meta Platforms Inc.",          "NASDAQ", "asic,end_market",         "US", 1, "12-31"),
    ("NASDAQ:MSFT",  "microsoft", "Microsoft Corporation",        "NASDAQ", "asic,end_market",         "US", 1, "06-30"),
    ("NASDAQ:MRVL",  "marvell",   "Marvell Technology Inc.",      "NASDAQ", "asic,network",            "US", 1, "02-01"),
    ("NASDAQ:AVGO",  "broadcom",  "Broadcom Inc.",                "NASDAQ", "asic,network",            "US", 1, "11-02"),
    ("NYSE:ANET",    "arista",    "Arista Networks Inc.",         "NYSE",   "network",                 "US", 1, "12-31"),
    ("NYSE:COHR",    "coherent",  "Coherent Corp.",               "NYSE",   "network",                 "US", 1, "06-30"),
    ("NASDAQ:CRWV",  "coreweave", "CoreWeave Inc.",               "NASDAQ", "end_market",              "US", 1, "12-31"),
    # ── DC Infrastructure ──
    ("NYSE:VRT",     "vertiv",    "Vertiv Holdings Co.",          "NYSE",   "dc_infra",                "US", 1, "12-31"),
    ("NYSE:ETN",     "eaton",     "Eaton Corporation plc",        "NYSE",   "dc_infra,power",          "IE", 1, "12-31"),
    ("EPA:SU",       "schneider", "Schneider Electric SE",        "EPA",    "dc_infra,power",          "FR", 1, "12-31"),
    ("NYSE:CAT",     "caterpillar","Caterpillar Inc.",            "NYSE",   "dc_infra",                "US", 1, "12-31"),
    ("NYSE:CMI",     "cummins",   "Cummins Inc.",                 "NYSE",   "dc_infra",                "US", 1, "12-31"),
    # ── Power Semiconductors ──
    ("NASDAQ:MPWR",  "mps",       "Monolithic Power Systems",     "NASDAQ", "power",                   "US", 1, "12-31"),
    ("ETR:IFX",      "infineon",  "Infineon Technologies AG",     "ETR",    "power",                   "DE", 1, "09-30"),
    ("NASDAQ:ON",    "on_semi",   "ON Semiconductor Corp.",       "NASDAQ", "power",                   "US", 1, "12-31"),
    ("EPA:STM",      "stmicro",   "STMicroelectronics N.V.",      "EPA",    "power",                   "CH", 1, "12-31"),
    ("NYSE:WOLF",    "wolfspeed", "Wolfspeed Inc.",               "NYSE",   "power",                   "US", 1, "06-30"),
    ("NASDAQ:TXN",   "texas_instruments","Texas Instruments Inc.","NASDAQ", "power",                   "US", 1, "12-31"),
    # ── Substrate ──
    ("TPE:3037",     "unimicron", "Unimicron Technology Corp.",   "TPE",    "substrate",               "TW", 1, "12-31"),
    ("TYO:4062",     "ibiden",    "Ibiden Co. Ltd.",              "TYO",    "substrate",               "JP", 1, "03-31"),
]


# ══════════════════════════════════════════════════════════════════════════════
# QUARTERLY FINANCIALS  (Tier A — from Cycle 9 company_master.md / market_data.md)
# Only figures explicitly stated in the source MD files (which cite 10-Q/10-K/IR).
# Facts-only: every row carries source_doc citation.
# ══════════════════════════════════════════════════════════════════════════════
# dict per row; None where not disclosed in source
QFIN = [
    # NVIDIA — Q1 FY2027 (period ended Apr 2026)
    dict(ticker="NASDAQ:NVDA", fy=2027, fq=1, period_end="2026-04-26", cq="2026-Q1",
         rev=None, rev_ai_dc=72000, rev_yoy=None, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Q1 FY2027 Earnings Release, NVIDIA Corporation, 2026-05-28, IR",
         src_date="2026-05-28", imp="high",
         note="Data Center revenue guidance ~$72B+; GB300 +129% YoY; 60K racks FY2026"),
    # AMD — Q1 2026
    dict(ticker="NASDAQ:AMD", fy=2026, fq=1, period_end="2026-03-28", cq="2026-Q1",
         rev=None, rev_ai_dc=5800, rev_yoy=57.0, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Q1 2026 Earnings Release, Advanced Micro Devices, 2026-05-05, IR",
         src_date="2026-05-05", imp="high",
         note="Data Center segment $5.8B (+57% YoY); MI450 sampling"),
    # Intel — Q1 2026
    dict(ticker="NASDAQ:INTC", fy=2026, fq=1, period_end="2026-03-28", cq="2026-Q1",
         rev=13600, rev_ai_dc=5100, rev_yoy=None, gm=None, op=-2437, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Form 10-Q Q1 2026, Intel Corporation, 2026-04-23, SEC EDGAR",
         src_date="2026-04-23", imp="high",
         note="Total rev $13.6B; DC&AI $5.1B (+22%); Foundry op loss -$2.437B"),
    # TSMC — Q1 2026
    dict(ticker="NYSE:TSM", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
         rev=35900, rev_ai_dc=None, rev_yoy=35.1, gm=66.2, op=None, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Q1 2026 Earnings Release, TSMC, 2026-04-16, IR",
         src_date="2026-04-16", imp="high",
         note="Revenue $35.9B (+35.1% YoY); gross margin 66.2%"),
    # Micron — FQ2 2026
    dict(ticker="NASDAQ:MU", fy=2026, fq=2, period_end="2026-02-26", cq="2026-Q1",
         rev=23860, rev_ai_dc=None, rev_yoy=196.0, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Form 10-Q FQ2 2026, Micron Technology, 2026-03-25, SEC EDGAR",
         src_date="2026-03-25", imp="high",
         note="Revenue $23.86B (+196% YoY); record; demand significantly in excess of supply"),
    # Pure Storage — FQ1 FY2027
    dict(ticker="NYSE:PSTG", fy=2027, fq=1, period_end="2026-05-04", cq="2026-Q1",
         rev=1053, rev_ai_dc=None, rev_yoy=35.0, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=4410, guid_hi=4510,
         src="Q1 FY2027 Earnings Release, Pure Storage, 2026-05-27, IR",
         src_date="2026-05-27", imp="medium",
         note="Revenue $1.053B (+35% YoY); FY2027 guidance $4.41-4.51B; product rev +55% YoY"),
    # Vertiv — Q1 2026
    dict(ticker="NYSE:VRT", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
         rev=2650, rev_ai_dc=None, rev_yoy=30.0, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=13500, guid_hi=14000,
         src="Form 10-Q Q1 2026, Vertiv Holdings, 2026-05-01, SEC EDGAR",
         src_date="2026-05-01", imp="high",
         note="Revenue $2.65B (+30% YoY); backlog $12.45B (+81%); FY2026 guide $13.5-14B"),
    # Eaton — Q1 2026
    dict(ticker="NYSE:ETN", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
         rev=7500, rev_ai_dc=None, rev_yoy=17.0, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Form 10-Q Q1 2026, Eaton Corporation, 2026-05-05, SEC EDGAR",
         src_date="2026-05-05", imp="high",
         note="Revenue $7.5B (+17% YoY); DC orders +240% YoY; 32 GW US DC under construction"),
    # Arista — Q1 2026
    dict(ticker="NYSE:ANET", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
         rev=2709, rev_ai_dc=None, rev_yoy=35.0, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Form 10-Q Q1 2026, Arista Networks, 2026-05-05, SEC EDGAR",
         src_date="2026-05-05", imp="medium",
         note="Revenue $2.709B (+35% YoY); FY2026 $11.5B target; AI fabric target $3.5B"),
    # MPS — Q1 2026
    dict(ticker="NASDAQ:MPWR", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
         rev=None, rev_ai_dc=262.8, rev_yoy=97.7, gm=None, op=None, ni=None, eps=None,
         capex=None, guid_lo=None, guid_hi=None,
         src="Form 10-Q Q1 2026, Monolithic Power Systems, 2026-05-06, SEC EDGAR",
         src_date="2026-05-06", imp="medium",
         note="Enterprise Data $262.8M (+97.7% YoY); sold-out; LT target raised to $6B"),
    # Hyperscaler capex (from market_data.md; Tier A 10-Q)
    dict(ticker="NASDAQ:AMZN", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
         rev=None, rev_ai_dc=37600, rev_yoy=28.0, gm=None, op=None, ni=None, eps=None,
         capex=44200, guid_lo=None, guid_hi=None,
         src="Form 10-Q Q1 2026, Amazon.com Inc., 2026-04-29, SEC EDGAR",
         src_date="2026-04-29", imp="high",
         note="Q1 capex $44.2B (+77% YoY); AWS rev $37.6B (+28%); backlog $364B; ~$200B FY2026 capex"),
    dict(ticker="NASDAQ:MSFT", fy=2026, fq=3, period_end="2026-03-31", cq="2026-Q1",
         rev=None, rev_ai_dc=None, rev_yoy=None, gm=None, op=None, ni=None, eps=None,
         capex=37500, guid_lo=None, guid_hi=None,
         src="Form 10-Q FQ3 2026, Microsoft Corporation, 2026-04-29, SEC EDGAR",
         src_date="2026-04-29", imp="high",
         note="Q1-cal capex $37.5B (+53% YoY); Azure AI ARR $37B (+123% YoY); ~$190B FY2026 capex"),
    dict(ticker="NASDAQ:GOOGL", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
         rev=None, rev_ai_dc=20000, rev_yoy=63.0, gm=None, op=None, ni=None, eps=None,
         capex=35700, guid_lo=None, guid_hi=None,
         src="Form 10-Q Q1 2026, Alphabet Inc., 2026-04-29, SEC EDGAR",
         src_date="2026-04-29", imp="high",
         note="Q1 capex $35.7B (+107%); Cloud $20B (+63% YoY); backlog $462B; $180-190B FY2026 capex"),
    dict(ticker="NASDAQ:META", fy=2026, fq=1, period_end="2026-03-31", cq="2026-Q1",
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
    dict(ticker="NASDAQ:MU", date="2026-03-25", cq="2026-Q1",
         quote="Demand is significantly in excess of supply.",
         speaker="CFO", signal="demand", segment="storage",
         src="FQ2 2026 Earnings Call, Micron Technology, 2026-03-25, IR",
         imp="high"),
    dict(ticker="NYSE:VRT", date="2026-05-01", cq="2026-Q1",
         quote="Liquid cooling has become the default for new AI data center deployments.",
         speaker="CEO", signal="demand", segment="dc_infra",
         src="Q1 2026 Earnings Call, Vertiv Holdings, 2026-05-01, IR",
         imp="high"),
    dict(ticker="NASDAQ:GOOGL", date="2026-04-29", cq="2026-Q1",
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

    CREATE INDEX IF NOT EXISTS idx_qfin_ticker  ON quarterly_financials(ticker, calendar_quarter);
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


# yfinance ticker mapping (Yahoo symbols differ from our EXCHANGE:TICKER PKs)
YF_SYMBOLS = {
    "KRX:000660": "000660.KS", "KRX:005930": "005930.KS", "NASDAQ:MU": "MU",
    "TYO:285A": "285A.T", "NASDAQ:SNDK": "SNDK", "NYSE:PSTG": "PSTG",
    "NYSE:TSM": "TSM", "NASDAQ:INTC": "INTC", "NASDAQ:AMKR": "AMKR", "NYSE:ASX": "ASX",
    "NASDAQ:NVDA": "NVDA", "NASDAQ:AMD": "AMD", "NASDAQ:GOOGL": "GOOGL",
    "NASDAQ:AMZN": "AMZN", "NASDAQ:META": "META", "NASDAQ:MSFT": "MSFT",
    "NASDAQ:MRVL": "MRVL", "NASDAQ:AVGO": "AVGO", "NYSE:ANET": "ANET",
    "NYSE:COHR": "COHR", "NASDAQ:CRWV": "CRWV", "NYSE:VRT": "VRT", "NYSE:ETN": "ETN",
    "EPA:SU": "SU.PA", "NYSE:CAT": "CAT", "NYSE:CMI": "CMI", "NASDAQ:MPWR": "MPWR",
    "ETR:IFX": "IFX.DE", "NASDAQ:ON": "ON", "EPA:STM": "STMPA.PA", "NYSE:WOLF": "WOLF",
    "NASDAQ:TXN": "TXN", "TPE:3037": "3037.TW", "TYO:4062": "4062.T",
}


# Local trading currency per exchange (non-US report in local currency)
EXCHANGE_CCY = {
    "KRX": "KRW", "TYO": "JPY", "TPE": "TWD", "ETR": "EUR", "EPA": "EUR",
    "NYSE": "USD", "NASDAQ": "USD",
}


def _ticker_ccy(ticker: str) -> str:
    return EXCHANGE_CCY.get(ticker.split(":")[0], "USD")


def seed_prices(cur):
    try:
        import yfinance as yf
    except ImportError:
        print("  stock_prices: SKIPPED (yfinance not installed)")
        return
    today = date.today().isoformat()
    start = (date.today() - timedelta(days=90)).isoformat()
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


def seed_yf_financials(cur):
    """Pull quarterly income statements from yfinance for ALL companies (Tier B).
    INSERT OR IGNORE preserves curated Tier-A rows; Tier-B rows are refreshed each run."""
    try:
        import yfinance as yf
        import warnings
        warnings.filterwarnings("ignore")
    except ImportError:
        print("  quarterly_financials (yf): SKIPPED (yfinance not installed)")
        return
    today = date.today().isoformat()
    # idempotent: clear prior auto-pulled rows, keep curated Tier-A
    cur.execute("DELETE FROM quarterly_financials WHERE source_tier='B'")
    inserted = 0
    for ticker, yf_sym in YF_SYMBOLS.items():
        try:
            df = yf.Ticker(yf_sym).quarterly_income_stmt
            if df is None or df.empty:
                print(f"    {ticker} ({yf_sym}): no income stmt")
                continue
            def row(name, col):
                try:
                    if name in df.index:
                        v = df.loc[name].iloc[col]
                        fv = float(v)
                        return fv if fv == fv else None  # NaN guard
                except Exception:
                    return None
                return None
            cnt = 0
            for col, period in enumerate(df.columns):
                if col >= 8:  # last 8 quarters
                    break
                pend = period.date()
                cy, cq = pend.year, (pend.month - 1)//3 + 1
                rev = row("Total Revenue", col)
                gp  = row("Gross Profit", col)
                op  = row("Operating Income", col)
                ni  = row("Net Income", col)
                eps = row("Diluted EPS", col)
                gm  = round(gp/rev*100, 1) if (gp and rev) else None
                if rev is None and ni is None:
                    continue
                cur.execute("""
                    INSERT OR IGNORE INTO quarterly_financials
                        (ticker, fiscal_year, fiscal_quarter, period_end_date, calendar_quarter,
                         revenue_usd_m, gross_profit_usd_m, gross_margin_pct,
                         operating_income_usd_m, net_income_usd_m, eps_diluted,
                         source_tier, source_doc, source_date, signal_type,
                         importance, confidence, notes)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    ticker, cy, cq, pend.isoformat(), f"{cy}-Q{cq}",
                    rev/1e6 if rev else None, gp/1e6 if gp else None, gm,
                    op/1e6 if op else None, ni/1e6 if ni else None, eps,
                    "B", f"Yahoo Finance quarterly income statement, {yf_sym}, retrieved {today}",
                    today, "earnings", "medium", "medium",
                    "Yahoo-aggregated from filings; verify against 10-Q for Tier-A use",
                ))
                cnt += 1
            inserted += cnt
            print(f"    {ticker} ({yf_sym}): {cnt} quarters")
        except Exception as e:
            print(f"    {ticker} ({yf_sym}): ERROR {e}")
    print(f"  quarterly_financials (yf, Tier B): {inserted} rows total")


if __name__ == "__main__":
    db = conn()
    cur = db.cursor()
    print(f"── Building {DB_PATH.name} ──────────────────────────")
    build_schema(cur)
    seed_companies(cur)
    seed_financials(cur)
    seed_commentary(cur)
    if PULL_PRICES:
        print("  pulling stock prices (90d) via yfinance…")
        seed_prices(cur)
    else:
        print("  stock_prices: SKIPPED (run with --prices to pull)")
    if PULL_FINANCIALS:
        print("  pulling quarterly income statements via yfinance…")
        seed_yf_financials(cur)
    else:
        print("  quarterly_financials (yf): SKIPPED (run with --financials to pull)")
    db.commit()
    db.close()
    print(f"\n✅ {DB_PATH}")
