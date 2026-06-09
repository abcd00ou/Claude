"""
Build script — creates two SQLite databases:

1. marketing/data/price_intel.db
   Tables: skus, price_observations, run_log
   Seeded from: internal_sales.json amazon_real_prices

2. agents/data/dba/intelligence.db
   Tables: companies, market_pricing, hyperscaler_capex, hbm_share, nand_share
   Seeded from: analysis/models/company_master.md + market_data.md parsed tables
                + marketing/data/market_data.json

Run: python3 build_db.py
"""
import json
import sqlite3
import re
from datetime import datetime
from pathlib import Path

ROOT      = Path(__file__).parent.parent   # /Users/idongseong/Claude
MKT_DATA  = Path(__file__).parent / "data"
AGENTS    = ROOT / "agents"

TODAY = datetime.now().strftime("%Y-%m-%d")

# ── helpers ───────────────────────────────────────────────────────────────────

def conn(path: Path) -> sqlite3.Connection:
    path.parent.mkdir(parents=True, exist_ok=True)
    c = sqlite3.connect(path)
    c.row_factory = sqlite3.Row
    return c

def parse_md_table(md_text: str, section_header: str) -> list[dict]:
    """Extract the first markdown table after `section_header`. Returns list of row dicts."""
    lines = md_text.splitlines()
    in_section = False
    table_lines = []
    header_re = re.compile(r"^#{1,3}\s+" + re.escape(section_header), re.IGNORECASE)
    for line in lines:
        if header_re.match(line):
            in_section = True
            continue
        if in_section:
            stripped = line.strip()
            if stripped.startswith("|"):
                table_lines.append(stripped)
            elif table_lines:
                break  # end of table
    if not table_lines:
        return []
    # first line = headers, second = separator, rest = rows
    headers = [h.strip() for h in table_lines[0].strip("|").split("|")]
    rows = []
    for row_line in table_lines[2:]:
        cells = [c.strip() for c in row_line.strip("|").split("|")]
        if len(cells) == len(headers):
            rows.append(dict(zip(headers, cells)))
    return rows


# ══════════════════════════════════════════════════════════════════════════════
# DATABASE 1: price_intel.db
# ══════════════════════════════════════════════════════════════════════════════

PRICE_DB_PATH = MKT_DATA / "price_intel.db"

SKU_META = {
    # sku_id: (brand, category, model, capacity_gb)
    "sd_extreme_1tb":         ("SanDisk", "external_ssd",   "Extreme",              1000),
    "sd_extreme_2tb":         ("SanDisk", "external_ssd",   "Extreme",              2000),
    "sd_extreme_pro_1tb":     ("SanDisk", "external_ssd",   "Extreme Pro",          1000),
    "sd_extreme_pro_2tb":     ("SanDisk", "external_ssd",   "Extreme Pro",          2000),
    "wd_my_passport_1tb":     ("WD",      "external_hdd",   "My Passport",          1000),
    "wd_my_passport_2tb":     ("WD",      "external_hdd",   "My Passport",          2000),
    "wd_sn850x_1tb":          ("WD",      "internal_nvme",  "Black SN850X",         1000),
    "wd_sn850x_2tb":          ("WD",      "internal_nvme",  "Black SN850X",         2000),
    "sd_extreme_micro_256g":  ("SanDisk", "microsd",        "Extreme MicroSD",       256),
    "sd_extreme_micro_512g":  ("SanDisk", "microsd",        "Extreme MicroSD",       512),
    "sd_extreme_micro_1tb":   ("SanDisk", "microsd",        "Extreme MicroSD",      1000),
    "sam_t9_1tb":             ("Samsung", "external_ssd",   "T9",                   1000),
    "sam_t9_2tb":             ("Samsung", "external_ssd",   "T9",                   2000),
    "sam_980_pro_1tb":        ("Samsung", "internal_nvme",  "980 Pro",              1000),
    "sam_990_pro_2tb":        ("Samsung", "internal_nvme",  "990 Pro",              2000),
    "sam_evo_plus_256g":      ("Samsung", "microsd",        "EVO Plus MicroSD",      256),
    "sam_evo_plus_512g":      ("Samsung", "microsd",        "EVO Plus MicroSD",      512),
    "crucial_p3_1tb":         ("Crucial", "internal_nvme",  "P3",                   1000),
    "crucial_p3_2tb":         ("Crucial", "internal_nvme",  "P3",                   2000),
    "kingston_canvas_256g":   ("Kingston","microsd",        "Canvas Select Plus",    256),
}

# Map from internal_sales.json amazon_real_prices keys → sku_id
PRICE_KEY_MAP = {
    "SD_EXTREME_1TB_USD":         "sd_extreme_1tb",
    "SD_EXTREME_2TB_USD":         "sd_extreme_2tb",
    "SD_EXTREME_PRO_1TB_USD":     "sd_extreme_pro_1tb",
    "SD_EXTREME_PRO_2TB_USD":     "sd_extreme_pro_2tb",
    "WD_MY_PASSPORT_1TB_USD":     "wd_my_passport_1tb",
    "WD_MY_PASSPORT_2TB_USD":     "wd_my_passport_2tb",
    "WD_SN850X_1TB_USD":          "wd_sn850x_1tb",
    "WD_SN850X_2TB_USD":          "wd_sn850x_2tb",
    "SD_EXTREME_MICRO_256G_USD":  "sd_extreme_micro_256g",
    "SD_EXTREME_MICRO_512G_USD":  "sd_extreme_micro_512g",
    "SD_EXTREME_MICRO_1TB_USD":   "sd_extreme_micro_1tb",
    "SAM_T9_1TB_USD":             "sam_t9_1tb",
    "SAM_T9_2TB_USD":             "sam_t9_2tb",
    "SAM_980_PRO_1TB_USD":        "sam_980_pro_1tb",
    "SAM_990_PRO_2TB_USD":        "sam_990_pro_2tb",
    "SAM_EVO_PLUS_256G_USD":      "sam_evo_plus_256g",
    "SAM_EVO_PLUS_512G_USD":      "sam_evo_plus_512g",
    "CRUCIAL_P3_1TB_USD":         "crucial_p3_1tb",
    "CRUCIAL_P3_2TB_USD":         "crucial_p3_2tb",
    "KINGSTON_CANVAS_256G_USD":   "kingston_canvas_256g",
}


def build_price_intel_db():
    print("\n── Building price_intel.db ──────────────────────────────")
    db = conn(PRICE_DB_PATH)
    cur = db.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS skus (
        sku_id       TEXT PRIMARY KEY,
        brand        TEXT NOT NULL,
        category     TEXT NOT NULL,
        model        TEXT,
        capacity     INTEGER,
        created_at   TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS price_observations (
        obs_id          INTEGER PRIMARY KEY AUTOINCREMENT,
        sku_id          TEXT NOT NULL REFERENCES skus(sku_id),
        price           REAL NOT NULL,
        msrp            REAL,
        premium_pct     REAL,
        currency        TEXT DEFAULT 'USD',
        country         TEXT DEFAULT 'US',
        source          TEXT,
        seller_name     TEXT,
        availability    TEXT,
        fulfillment     TEXT,
        parse_confidence REAL DEFAULT 1.0,
        is_accepted     INTEGER DEFAULT 1,
        observed_at     TEXT NOT NULL,
        created_at      TEXT DEFAULT (datetime('now'))
    );

    CREATE INDEX IF NOT EXISTS idx_obs_sku_date
        ON price_observations(sku_id, observed_at DESC);

    CREATE TABLE IF NOT EXISTS run_log (
        run_id            TEXT PRIMARY KEY,
        started_at        TEXT NOT NULL,
        completed_at      TEXT,
        total_targets     INTEGER DEFAULT 0,
        success_count     INTEGER DEFAULT 0,
        quarantine_count  INTEGER DEFAULT 0,
        hitl_count        INTEGER DEFAULT 0,
        status            TEXT DEFAULT 'completed'
    );
    """)

    # ── seed skus ─────────────────────────────────────────────
    for sku_id, (brand, cat, model, cap) in SKU_META.items():
        cur.execute("""
            INSERT OR IGNORE INTO skus(sku_id, brand, category, model, capacity)
            VALUES (?,?,?,?,?)
        """, (sku_id, brand, cat, model, cap))
    print(f"  skus: {len(SKU_META)} rows inserted")

    # ── seed price_observations from internal_sales.json ──────
    sales_path = MKT_DATA / "internal_sales.json"
    with open(sales_path) as f:
        sales = json.load(f)

    raw_prices = sales.get("amazon_real_prices", {})
    obs_date = "2026-03-09"
    inserted = 0
    for raw_key, val in raw_prices.items():
        if raw_key.startswith("_"):
            continue
        sku_id = PRICE_KEY_MAP.get(raw_key)
        if not sku_id:
            continue
        cur.execute("""
            INSERT OR IGNORE INTO price_observations
                (sku_id, price, msrp, premium_pct, currency, country,
                 source, seller_name, observed_at)
            VALUES (?,?,?,?,?,?,?,?,?)
        """, (
            sku_id,
            val.get("crawled"),
            val.get("msrp"),
            val.get("premium_pct"),
            "USD", "US",
            "amazon", "3P",
            obs_date,
        ))
        inserted += 1
    print(f"  price_observations: {inserted} rows inserted (obs_date={obs_date})")

    # ── seed run_log ───────────────────────────────────────────
    cur.execute("""
        INSERT OR IGNORE INTO run_log
            (run_id, started_at, completed_at, total_targets, success_count, status)
        VALUES (?,?,?,?,?,?)
    """, ("seed-001", "2026-03-09T09:00:00", "2026-03-09T09:05:32",
          inserted, inserted, "completed"))
    print(f"  run_log: 1 seed run inserted")

    db.commit()
    db.close()
    print(f"  ✅ {PRICE_DB_PATH}")


# ══════════════════════════════════════════════════════════════════════════════
# DATABASE 2: intelligence.db
# ══════════════════════════════════════════════════════════════════════════════

INTEL_DB_PATH = AGENTS / "data" / "dba" / "intelligence.db"

SEGMENT_MAP = {
    "DRAM / Memory": "dram",
    "NAND / Storage": "storage",
    "Foundry & Advanced Packaging": "foundry",
    "AI Accelerators (Chip Makers)": "chip_maker",
    "Custom Silicon (ASIC)": "asic",
    "AI Networking": "network",
    "End Markets / Hyperscalers": "end_market",
    "DC Infrastructure": "dc_infra",
    "Power Semiconductors": "power",
}


def build_intelligence_db():
    print("\n── Building intelligence.db ─────────────────────────────")
    db = conn(INTEL_DB_PATH)
    cur = db.cursor()

    cur.executescript("""
    CREATE TABLE IF NOT EXISTS companies (
        id            INTEGER PRIMARY KEY AUTOINCREMENT,
        segment       TEXT NOT NULL,
        company       TEXT NOT NULL,
        role          TEXT,
        share_metric  TEXT,
        share_value   TEXT,
        latest_revenue TEXT,
        key_signal    TEXT,
        last_sourced  TEXT,
        cycle         TEXT DEFAULT 'Cycle 9',
        updated_at    TEXT DEFAULT (datetime('now')),
        UNIQUE(segment, company)
    );

    CREATE TABLE IF NOT EXISTS market_pricing (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        category    TEXT NOT NULL,
        product     TEXT NOT NULL,
        price       TEXT,
        direction   TEXT,
        period      TEXT,
        source      TEXT,
        cycle       TEXT DEFAULT 'Cycle 9',
        updated_at  TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS hyperscaler_capex (
        id               INTEGER PRIMARY KEY AUTOINCREMENT,
        company          TEXT NOT NULL UNIQUE,
        cy2026_guidance  TEXT,
        q1_2026_actual   TEXT,
        q1_yoy_growth    TEXT,
        source           TEXT,
        cycle            TEXT DEFAULT 'Cycle 9',
        updated_at       TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS hbm_market_share (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        supplier    TEXT NOT NULL,
        period      TEXT NOT NULL,
        share_pct   TEXT,
        notes       TEXT,
        cycle       TEXT DEFAULT 'Cycle 9',
        updated_at  TEXT DEFAULT (datetime('now')),
        UNIQUE(supplier, period)
    );

    CREATE TABLE IF NOT EXISTS nand_market_share (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        supplier    TEXT NOT NULL UNIQUE,
        bit_share   TEXT,
        notes       TEXT,
        cycle       TEXT DEFAULT 'Cycle 9',
        updated_at  TEXT DEFAULT (datetime('now'))
    );

    CREATE TABLE IF NOT EXISTS nand_b2c_tam (
        id          INTEGER PRIMARY KEY AUTOINCREMENT,
        category    TEXT NOT NULL,
        year        INTEGER NOT NULL,
        tam_usd_b   REAL,
        cagr        REAL,
        cycle       TEXT DEFAULT 'Cycle 9',
        updated_at  TEXT DEFAULT (datetime('now')),
        UNIQUE(category, year)
    );

    CREATE TABLE IF NOT EXISTS nand_b2c_asp (
        id           INTEGER PRIMARY KEY AUTOINCREMENT,
        sku_desc     TEXT NOT NULL UNIQUE,
        asp_usd      REAL,
        cycle        TEXT DEFAULT 'Cycle 9',
        updated_at   TEXT DEFAULT (datetime('now'))
    );
    """)

    # ── seed companies from company_master.md ─────────────────
    cm_path = AGENTS / "data" / "analysis" / "models" / "company_master.md"
    cm_text = cm_path.read_text()

    inserted_co = 0
    current_segment = None
    for line in cm_text.splitlines():
        # detect segment header (## level)
        m = re.match(r"^##\s+(.+)", line)
        if m:
            heading = m.group(1).strip()
            current_segment = SEGMENT_MAP.get(heading, heading.lower().replace(" ", "_"))
            continue

        # parse table rows
        if current_segment and line.strip().startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 2 or cells[0].startswith("-") or cells[0].lower() == "company":
                continue
            company = cells[0]
            if not company or company.startswith("-"):
                continue

            # flexible assignment based on segment column count
            role = cells[1] if len(cells) > 1 else ""
            share_metric = None
            share_value = None
            latest_revenue = None
            key_signal = None
            last_sourced = None

            if current_segment in ("dram", "storage", "foundry", "chip_maker"):
                share_metric = "share"
                share_value  = cells[2] if len(cells) > 2 else ""
                latest_revenue = cells[3] if len(cells) > 3 else ""
                key_signal     = cells[4] if len(cells) > 4 else ""
                last_sourced   = cells[5] if len(cells) > 5 else ""
            elif current_segment == "asic":
                role     = cells[1] if len(cells) > 1 else ""
                key_signal = cells[2] if len(cells) > 2 else ""
                last_sourced = cells[3] if len(cells) > 3 else ""
            elif current_segment == "end_market":
                latest_revenue = cells[2] if len(cells) > 2 else ""
                key_signal = cells[3] if len(cells) > 3 else ""
                last_sourced = cells[4] if len(cells) > 4 else ""
            elif current_segment == "dc_infra":
                share_metric = "key_metric"
                share_value  = cells[2] if len(cells) > 2 else ""
                key_signal   = cells[3] if len(cells) > 3 else ""
                last_sourced = cells[4] if len(cells) > 4 else ""
            else:
                key_signal   = cells[2] if len(cells) > 2 else ""
                last_sourced = cells[3] if len(cells) > 3 else ""

            cur.execute("""
                INSERT OR REPLACE INTO companies
                    (segment, company, role, share_metric, share_value,
                     latest_revenue, key_signal, last_sourced)
                VALUES (?,?,?,?,?,?,?,?)
            """, (current_segment, company, role, share_metric, share_value,
                  latest_revenue, key_signal, last_sourced))
            inserted_co += 1

    print(f"  companies: {inserted_co} rows inserted")

    # ── seed market_pricing from market_data.md ───────────────
    md_path = AGENTS / "data" / "analysis" / "models" / "market_data.md"
    md_text = md_path.read_text()

    pricing_sections = [
        ("Memory Pricing (DRAM)", "dram"),
        ("Storage Pricing (NAND)", "nand"),
        ("AI Accelerator Pricing", "accelerator"),
    ]
    inserted_pr = 0
    for section, category in pricing_sections:
        rows = parse_md_table(md_text, section)
        for row in rows:
            product = row.get("Product") or row.get("product", "")
            if not product or product.startswith("-"):
                continue
            cur.execute("""
                INSERT INTO market_pricing
                    (category, product, price, direction, period, source)
                VALUES (?,?,?,?,?,?)
            """, (
                category,
                product,
                row.get("Price ($/GB)") or row.get("Price") or row.get("List Price (est.)"),
                row.get("Direction", ""),
                row.get("Period", ""),
                row.get("Source", ""),
            ))
            inserted_pr += 1
    print(f"  market_pricing: {inserted_pr} rows inserted")

    # ── seed hyperscaler_capex ─────────────────────────────────
    capex_rows = parse_md_table(md_text, "Hyperscaler Capex — CY2026")
    inserted_cx = 0
    for row in capex_rows:
        company = row.get("Company", "")
        if not company or company.startswith("-") or company.startswith("**Big"):
            continue
        cur.execute("""
            INSERT OR REPLACE INTO hyperscaler_capex
                (company, cy2026_guidance, q1_2026_actual, q1_yoy_growth, source)
            VALUES (?,?,?,?,?)
        """, (
            company,
            row.get("CY2026 Guidance", ""),
            row.get("Q1 2026 Actual", ""),
            row.get("YoY Q1 Growth", ""),
            row.get("Source", ""),
        ))
        inserted_cx += 1
    print(f"  hyperscaler_capex: {inserted_cx} rows inserted")

    # ── seed HBM market share ──────────────────────────────────
    hbm_rows = parse_md_table(md_text, "HBM Market Share")
    inserted_hbm = 0
    for row in hbm_rows:
        supplier = row.get("Supplier", "")
        if not supplier or supplier.startswith("-"):
            continue
        for period, col in [("Q2 2025", "Share (Q2 2025)"), ("HBM4 CY2026", "Share (HBM4, CY2026)")]:
            cur.execute("""
                INSERT OR REPLACE INTO hbm_market_share
                    (supplier, period, share_pct, notes)
                VALUES (?,?,?,?)
            """, (supplier, period, row.get(col, ""), row.get("Notes", "")))
            inserted_hbm += 1
    print(f"  hbm_market_share: {inserted_hbm} rows inserted")

    # ── seed NAND market share ─────────────────────────────────
    nand_rows = parse_md_table(md_text, "NAND Bit Share (CY2026)")
    inserted_nand = 0
    for row in nand_rows:
        supplier = row.get("Supplier", "")
        if not supplier or supplier.startswith("-"):
            continue
        cur.execute("""
            INSERT OR REPLACE INTO nand_market_share
                (supplier, bit_share, notes)
            VALUES (?,?,?)
        """, (supplier, row.get("Bit Share", ""), row.get("Notes", "")))
        inserted_nand += 1
    print(f"  nand_market_share: {inserted_nand} rows inserted")

    # ── seed B2C TAM from market_data.json ────────────────────
    mkt_path = MKT_DATA / "market_data.json"
    with open(mkt_path) as f:
        mkt = json.load(f)
    tam = mkt.get("tam_usd_b", {})
    inserted_tam = 0
    cat_map = {
        "external_ssd": "external_ssd",
        "internal_ssd_consumer": "internal_ssd",
        "microsd": "microsd",
    }
    for cat_key, cat_label in cat_map.items():
        for year in [2024, 2025]:
            val = tam.get(f"{cat_key}_{year}")
            cagr = tam.get(f"cagr_{cat_key}")
            if val is None:
                continue
            cur.execute("""
                INSERT OR REPLACE INTO nand_b2c_tam
                    (category, year, tam_usd_b, cagr)
                VALUES (?,?,?,?)
            """, (cat_label, year, val, cagr))
            inserted_tam += 1
    print(f"  nand_b2c_tam: {inserted_tam} rows inserted")

    # ── seed ASP ──────────────────────────────────────────────
    asp = mkt.get("asp_usd", {})
    inserted_asp = 0
    for sku_desc, price in asp.items():
        cur.execute("""
            INSERT OR REPLACE INTO nand_b2c_asp(sku_desc, asp_usd)
            VALUES (?,?)
        """, (sku_desc, price))
        inserted_asp += 1
    print(f"  nand_b2c_asp: {inserted_asp} rows inserted")

    db.commit()
    db.close()
    print(f"  ✅ {INTEL_DB_PATH}")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    build_price_intel_db()
    build_intelligence_db()
    print("\n✅ All databases built successfully.")
    print(f"   {PRICE_DB_PATH}")
    print(f"   {INTEL_DB_PATH}")
