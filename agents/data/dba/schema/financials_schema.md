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

**Baseline start year: 2016.** All time-series data must extend back to at least
2016-01-01 where the source provides it.

| Table | Required history | Source reality |
|---|---|---|
| `stock_prices` | Daily OHLCV from **2016-01-01** to present | Full — Yahoo Finance provides 2016+ daily for all 136 |
| `annual_financials` | Full-year P&L from **FY2016** | **SEC EDGAR XBRL** (Tier A) for US filers back to FY2016; Yahoo `income_stmt` (Tier B) fills foreign/non-filers (recent ~5 yrs) |
| `quarterly_financials` | Discrete quarters from **2016** where filed | SEC EDGAR XBRL discrete-quarter facts (Tier A) for US filers; Yahoo (Tier B) + curated rows fill the rest |

**Source precedence (built in this order, first writer wins):**
1. Curated Tier-A rows (hand-entered from IR/10-Q, with AI/DC revenue + guidance)
2. **SEC EDGAR XBRL** companyfacts (`edgar_financials.py`) — Tier A, deep history FY2016+
   (`https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json`)
3. Yahoo Finance (`yfinance`) — Tier B, fills foreign companies & any gaps

EDGAR covers US-SEC filers (incl. foreign 20-F filers like TSM, ASX, ASML).
Pure foreign listings (Samsung .KS, SK hynix, most .T/.TW/.DE) stay on Yahoo (recent years).
Quarterly EDGAR uses discrete ~3-month facts only (YTD cumulative facts are skipped).

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
| `ticker` | TEXT PK | Yahoo symbol — e.g., `NVDA`, `TSM`, `005930.KS`, `2330.TW` |
| `slug` | TEXT UNIQUE | snake_case cross-ref slug |
| `name` | TEXT | Full legal company name |
| `exchange` | TEXT | Derived from ticker suffix (US/KRX/TYO/TPE/HKEX/XETRA/EPA/…) |
| `segments` | TEXT | One of the 20 sections in `company_universe.csv` (ai_chip, dram, energy, server_oem, …) |
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
| `capex_usd_m` | REAL | Capital expenditures (USD millions; abs value of cash-flow capex) |
| `fcf_usd_m` | REAL | Free cash flow (USD millions) |
| `operating_cash_flow_usd_m` | REAL | Cash from operations (USD millions) |
| `inventory_usd_m` | REAL | Inventories (balance sheet, USD millions) |
| `receivables_usd_m` | REAL | Accounts receivable (USD millions) |
| `total_assets_usd_m` | REAL | Total assets (USD millions) |
| `total_debt_usd_m` | REAL | Total debt (USD millions) |
| `stockholders_equity_usd_m` | REAL | Total stockholders' equity (USD millions) |
| `revenue_guidance_low_usd_m` | REAL | Next-quarter revenue guidance, low end |
| `revenue_guidance_high_usd_m` | REAL | Next-quarter revenue guidance, high end |
| `source_tier` | TEXT | 'A' for curated 10-Q/10-K rows; 'B' for Yahoo-pulled rows |
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
One row per company per fiscal year, **FY2016+**. Primary source = SEC EDGAR XBRL
(Tier A) for US filers; Yahoo `income_stmt` (Tier B) fills foreign/non-filers.

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
| `capex_usd_m` | REAL | Capital expenditures (USD millions) |
| `fcf_usd_m` | REAL | Free cash flow (USD millions) |
| `operating_cash_flow_usd_m` | REAL | Cash from operations (USD millions) |
| `cash_usd_m` | REAL | Cash & equivalents (USD millions) |
| `inventory_usd_m` | REAL | Inventories (USD millions) |
| `receivables_usd_m` | REAL | Accounts receivable (USD millions) |
| `total_assets_usd_m` | REAL | Total assets (USD millions) |
| `total_debt_usd_m` | REAL | Total debt (USD millions) |
| `stockholders_equity_usd_m` | REAL | Total stockholders' equity (USD millions) |
| `source_tier` | TEXT | 'B' (Yahoo, filing-derived) |
| `source_doc` | TEXT | "Yahoo Finance annual statements, [SYM], retrieved YYYY-MM-DD" |
| `source_date` | TEXT | YYYY-MM-DD — retrieval date |
| `notes` | TEXT | "Yahoo-aggregated from 10-K; verify for Tier-A use" |

**Unique constraint:** `(ticker, fiscal_year)`

**Data composition:** income statement (`income_stmt`), balance sheet
(`balance_sheet`), and cash flow (`cashflow`) merged by period end date.

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
| 2026-06-16 | History baseline 2016: stock prices 2016+ (323K rows); added SEC EDGAR XBRL puller (edgar_financials.py) for deep Tier-A annual+quarterly financials FY2016+ (72 US filers, 608 annual + 1929 quarterly); annual_financials now FY2016-2027 |
| 2026-06-11 | Expanded both financial tables with balance-sheet + cash-flow columns (inventory, receivables, total assets, total debt, equity, capex, FCF, operating cash flow) — pulled from Yahoo income_stmt + balance_sheet + cashflow, merged by period |
| 2026-06-11 | Added Historical Coverage Requirement (baseline 2020); added `annual_financials` table (FY2021+); `stock_prices` now full daily history from 2020-01-01 (was 90-day window) |
| 2026-06-10 | Initial schema — 4 tables: companies, quarterly_financials, stock_prices, earnings_commentary |
