# Financials DB Schema — AI Supply Chain Companies

**File:** `agents/data/dba/financials.db`  
**Last Updated:** 2026-06-11  
**Governed by:** DBA Agent (`agents/data/dba/README.md`)

---

## Purpose

Structured SQLite database for quarterly/annual financial data (10-K/10-Q) and
stock prices across AI supply chain companies. All rows must comply with
DBA source quality standards.

---

## Historical Coverage Requirement

**Baseline start year: 2020.** All time-series data must extend back to at least
2020-01-01 where the source provides it.

| Table | Required history | Source reality |
|---|---|---|
| `stock_prices` | Daily OHLCV from **2020-01-01** to present | Full — Yahoo Finance provides 2020+ daily |
| `annual_financials` | Full-year P&L from **FY2021** (5 fiscal years) | Yahoo `income_stmt` returns 5 annual periods |
| `quarterly_financials` | Most recent **5 quarters** + curated Tier-A | Yahoo `quarterly_income_stmt` caps at ~5 quarters; deeper quarterly requires SEC EDGAR XBRL parsing (future work) |

**Note:** Yahoo's free tier limits quarterly statements to ~5 trailing quarters.
To obtain quarterly history before 2025, parse SEC EDGAR XBRL company facts
(`https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json`) — tracked as future work.
Annual financials (FY2021+) and full daily stock prices (2020+) are the current
historical baseline.

---

## Source Tier Rules (enforced)

| Data Type | Required Tier | Accepted Sources |
|---|---|---|
| Quarterly financials (revenue, GM, EPS) | **A** | SEC Form 10-Q, 10-K, 20-F (EDGAR); official IR earnings releases |
| Capex / guidance | **A** | Same SEC filings + earnings call transcripts (official IR pages) |
| Stock prices (daily OHLCV) | **A/B** | NYSE/NASDAQ official; Yahoo Finance API; Bloomberg |
| Analyst estimates | **B** | Goldman Sachs, Morgan Stanley, Bernstein, TF International — named only |

Tier X (blogs, social, anonymous) is **never accepted**. Tier D estimates go into
`agents/data/analysis/models/` — not this database.

---

## Tables

### 1. `companies`
Master registry of all AI SCM companies tracked.

| Column | Type | Description |
|---|---|---|
| `ticker` | TEXT PK | `EXCHANGE:TICKER` — e.g., `NASDAQ:NVDA`, `NYSE:TSM`, `KRX:000660` |
| `slug` | TEXT UNIQUE | snake_case cross-ref slug — matches `company_master.md` |
| `name` | TEXT | Full legal company name |
| `exchange` | TEXT | NYSE \| NASDAQ \| KRX \| TYO \| ETR \| EPA \| Private |
| `segments` | TEXT | Comma-separated: dram, storage, foundry, chip_maker, asic, network, end_market, dc_infra, power, substrate |
| `hq_country` | TEXT | ISO 3166-1 alpha-2 |
| `is_public` | INTEGER | 1 = public, 0 = private |
| `fiscal_year_end` | TEXT | MM-DD (e.g., "01-26" for NVIDIA Jan fiscal year end) |

---

### 2. `quarterly_financials`
One row per company per fiscal quarter. Source = SEC 10-Q/10-K/20-F (Tier A).

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK | Auto-increment |
| `ticker` | TEXT FK | References `companies.ticker` |
| `fiscal_year` | INTEGER | Fiscal year (calendar year for most; note NVIDIA uses FY ending Jan) |
| `fiscal_quarter` | INTEGER | 1/2/3/4 within the fiscal year |
| `period_end_date` | TEXT | YYYY-MM-DD — last day of the fiscal quarter |
| `calendar_quarter` | TEXT | CQ label for cross-company comparison: e.g., "2026-Q1" |
| `revenue_usd_m` | REAL | Total net revenue (USD millions) |
| `revenue_ai_dc_usd_m` | REAL | AI / Data Center segment revenue (USD millions; NULL if not disclosed) |
| `revenue_yoy_pct` | REAL | YoY growth % (stated in filing or IR release) |
| `gross_profit_usd_m` | REAL | Gross profit (USD millions) |
| `gross_margin_pct` | REAL | Gross margin % |
| `operating_income_usd_m` | REAL | Operating income/loss (USD millions) |
| `net_income_usd_m` | REAL | Net income/loss (USD millions) |
| `eps_diluted` | REAL | Diluted EPS (USD) |
| `cash_usd_m` | REAL | Cash + short-term investments (USD millions) |
| `capex_usd_m` | REAL | Capital expenditures (USD millions) |
| `fcf_usd_m` | REAL | Free cash flow (USD millions; NULL if not stated) |
| `revenue_guidance_low_usd_m` | REAL | Next-quarter revenue guidance, low end |
| `revenue_guidance_high_usd_m` | REAL | Next-quarter revenue guidance, high end |
| `source_tier` | TEXT | Must be 'A' for 10-Q/10-K/20-F |
| `source_doc` | TEXT | Full citation: "Form 10-Q Q1 FY2027, NVIDIA Corporation, 2026-05-28, SEC EDGAR" |
| `source_date` | TEXT | YYYY-MM-DD — filing date |
| `source_url` | TEXT | SEC EDGAR URL or official IR page |
| `signal_type` | TEXT | Always 'earnings' for this table |
| `importance` | TEXT | high / medium / low |
| `confidence` | TEXT | high (Tier A) |
| `notes` | TEXT | Verbatim quote or context from earnings release |
| `created_at` | TEXT | datetime('now') |

**Unique constraint:** `(ticker, fiscal_year, fiscal_quarter)`

---

### 2b. `annual_financials`
One row per company per fiscal year. Source = Yahoo `income_stmt` (Tier B,
filing-derived) covering FY2021+. Provides the pre-2025 historical baseline.

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK | Auto-increment |
| `ticker` | TEXT FK | References `companies.ticker` |
| `fiscal_year` | INTEGER | Fiscal year (period end year) |
| `period_end_date` | TEXT | YYYY-MM-DD — fiscal year end |
| `revenue_usd_m` | REAL | Total revenue (USD millions) |
| `gross_profit_usd_m` | REAL | Gross profit (USD millions) |
| `gross_margin_pct` | REAL | Gross margin % |
| `operating_income_usd_m` | REAL | Operating income/loss (USD millions) |
| `net_income_usd_m` | REAL | Net income/loss (USD millions) |
| `eps_diluted` | REAL | Diluted EPS (USD) |
| `source_tier` | TEXT | 'B' (Yahoo, filing-derived) |
| `source_doc` | TEXT | "Yahoo Finance annual income statement, [SYM], retrieved YYYY-MM-DD" |
| `source_date` | TEXT | YYYY-MM-DD — retrieval date |
| `notes` | TEXT | "Yahoo-aggregated from 10-K; verify for Tier-A use" |

**Unique constraint:** `(ticker, fiscal_year)`

---

### 3. `stock_prices`
Daily OHLCV. Source = exchange data or Yahoo Finance API (Tier A/B).

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK | Auto-increment |
| `ticker` | TEXT FK | References `companies.ticker` |
| `price_date` | TEXT | YYYY-MM-DD |
| `open_usd` | REAL | Opening price (USD or local currency — see notes) |
| `high_usd` | REAL | Intraday high |
| `low_usd` | REAL | Intraday low |
| `close_usd` | REAL | Closing price |
| `adj_close_usd` | REAL | Adjusted close (accounts for splits/dividends) |
| `volume` | INTEGER | Shares traded |
| `market_cap_usd_b` | REAL | Market cap (USD billions) — computed from adj_close × shares outstanding |
| `currency` | TEXT | USD / KRW / JPY / EUR — original currency before USD conversion |
| `source_tier` | TEXT | 'A' (exchange) or 'B' (Yahoo Finance API) |
| `source_doc` | TEXT | "Yahoo Finance API yfinance v0.2.x, [TICKER], retrieved YYYY-MM-DD" |
| `source_date` | TEXT | YYYY-MM-DD — date data was retrieved |

**Unique constraint:** `(ticker, price_date)`

---

### 4. `earnings_commentary`
Verbatim key quotes from earnings calls. Source = official IR transcript (Tier A).

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER PK | Auto-increment |
| `ticker` | TEXT FK | References `companies.ticker` |
| `earnings_date` | TEXT | YYYY-MM-DD — date of earnings call |
| `calendar_quarter` | TEXT | e.g., "2026-Q1" |
| `quote` | TEXT | Verbatim quote from filing or transcript |
| `speaker` | TEXT | "CEO" / "CFO" / "IR" |
| `signal_type` | TEXT | earnings / capex / demand / supply / roadmap / guidance |
| `segment` | TEXT | Primary segment this quote relates to |
| `source_tier` | TEXT | 'A' |
| `source_doc` | TEXT | Full citation |
| `source_date` | TEXT | YYYY-MM-DD |
| `importance` | TEXT | high / medium / low |
| `confidence` | TEXT | high |

---

## Versioning Rules (per DBA README)

1. Never DELETE rows — mark superseded entries in `notes` column
2. When guidance is updated, INSERT a new row with `notes = "[supersedes: prior entry id=X]"`
3. `created_at` is immutable after insert
4. Update `**Last Updated:**` in this file after each schema change

---

## Schema Changelog

| Date | Change |
|---|---|
| 2026-06-11 | Added Historical Coverage Requirement (baseline 2020); added `annual_financials` table (FY2021+); `stock_prices` now full daily history from 2020-01-01 (was 90-day window) |
| 2026-06-10 | Initial schema — 4 tables: companies, quarterly_financials, stock_prices, earnings_commentary |
