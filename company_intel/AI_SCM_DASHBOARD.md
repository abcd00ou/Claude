# AI SCM Intelligence Dashboard

Single-file, self-contained sales intelligence tool for the AI supply chain. Covers 18 companies across 7 SCM layers — from nuclear power to HBM memory. Runs as a local `file://` HTML with no server required.

---

## What This Is

A dashborad built for AI semiconductor sales teams. For each company in the AI supply chain it shows:

- Snapshot financials (revenue, margins, market cap)
- SCM engagement — their exact role, what server-level products they make, who they buy from and sell to
- Lead time pipeline — how many weeks/months each step takes from their action to AI tokens being served, with the bottleneck highlighted
- Key events timeline — curated 2023–2026 events (product launches, capacity moves, financial signals, risk flags)
- Product roadmap, competitive position, sales hooks, recent news

The Overview page shows the full supply chain flow diagram, an all-company table with lead times color-coded, and a **global timeline** of all 148 events filterable by layer and category.

---

## File Structure

```
company_intel/
├── run.py                  # pipeline runner — fetches news + IR data for all 18 companies
├── config.py               # company list, layer assignments, IR URLs, news queries
├── build_dashboard.py      # reads all JSON → writes dashboard/index.html
├── enrich_scm.py           # one-time script — wrote scm_engagement blocks to all JSONs
├── enrich_timeline.py      # one-time script — wrote lead_time + key_events to all JSONs
├── agents/
│   ├── news_agent.py       # fetches Google News RSS, flags relevant articles
│   ├── ir_agent.py         # pulls financials from AI_SCM seed data
│   └── product_agent.py    # product roadmap enrichment
├── data/
│   ├── companies/          # 18 JSON profiles (one per company)
│   └── ai_scm_seed.json    # seed data: HBM market share, hyperscaler CapEx, etc.
└── dashboard/
    └── index.html          # output — open this in any browser
```

---

## 7 Supply Chain Layers

| Layer | Companies | What They Do |
|---|---|---|
| **HBM Memory** | SK Hynix, Samsung Semiconductor, Micron | Make the high-bandwidth memory stacks bonded onto every AI GPU |
| **GPU** | NVIDIA | Design the AI training/inference GPUs that use HBM |
| **Foundry** | TSMC | Fabricate GPU dies + bond HBM via CoWoS packaging |
| **Custom ASIC** | Broadcom, Marvell, AMD | Design custom AI accelerators (Google TPU, AWS Trainium, Meta MTIA) |
| **Hyperscalers** | Microsoft, Google, Amazon, Meta | Buy and deploy AI compute; fund most of the supply chain |
| **Power & Infrastructure** | Vertiv, GE Vernova, Constellation Energy | Power, cooling, and grid capacity for AI datacenters |
| **China AI Supply Chain** | Huawei, CXMT, SMIC | Parallel domestic chain: bypasses US export controls via DUV-only processes |

---

## Supply Chain Flow

```
Constellation Energy ──┐
GE Vernova            ──┤ Power → Hyperscalers (MSFT / GOOGL / AMZN / META)
Vertiv                ──┘              │
                                       ▼
                              GPU (NVIDIA, AMD)   +   Custom ASIC (Broadcom, Marvell)
                                       │
                                       ▼
                                  TSMC (CoWoS packaging — 95% market share)
                                       │
                                       ▼
                         HBM: SK Hynix (50%) / Samsung (35%) / Micron (15%)

- - - - - - - - - - - - - - - - - - - - - - - - - - -
🇨🇳 China Alt Chain (dashed red — no EUV, DUV only):
   Huawei (GPU/server) ← SMIC (foundry) ← CXMT (HBM-equivalent)
```

**Central bottleneck:** TSMC CoWoS packaging. Every HBM → GPU bond goes through TSMC's CoWoS line. New capacity takes 18 months to add. This is why SK Hynix's HBM lead time is 12 months despite producing wafers in 10 weeks.

---

## Lead Time to AI Token: All 18 Companies

Time from a company's action (investment, order, production start) to AI inference tokens being served.

| Company | Layer | Months | Bottleneck |
|---|---|---|---|
| Microsoft | Hyperscaler | **3** | Power availability at new datacenter sites |
| Google | Hyperscaler | **4** | TPU cluster Jupiter network setup |
| Meta | Hyperscaler | **4** | OAM chassis + liquid cooling custom form factor |
| Amazon | Hyperscaler | **5** | Nitro network integration with custom silicon |
| NVIDIA | GPU | **6** | TSMC CoWoS capacity slot availability |
| AMD | ASIC | **8** | ROCm/CUDA software stack maturity (vLLM, PyTorch) |
| Micron | HBM | **11** | TSMC CoWoS slot (Idaho packaging not yet online) |
| SK Hynix | HBM | **12** | TSMC CoWoS packaging slot — 18mo for new capacity |
| Samsung | HBM | **14** | NVIDIA HBM3e yield qualification (unresolved Q1 2026) |
| Huawei | China | **16** | SMIC N+2 yield (~60% vs TSMC N5 ~80%) |
| TSMC | Foundry | **18** | EUV scanner delivery from ASML (12-18 month wait) |
| SMIC | China | **18** | DUV multi-patterning yield — physically limited without EUV |
| Vertiv | Power | **18** | Building permits + electrical approval before install |
| CXMT | China | **20** | DUV yield (~50-60% vs SK Hynix EUV ~75%) |
| Marvell | ASIC | **28** | AWS software integration post-silicon (6 months vs CUDA) |
| Broadcom | ASIC | **30** | Co-design cycle (12-18 months) before TSMC tape-out |
| GE Vernova | Power | **36** | Grid transformer backlog — 18-36 months, no fast-track |
| Constellation Energy | Power | **48** | NRC regulatory approval — 18-24 months minimum |

**Color coding in dashboard:** green ≤ 6 months · amber ≤ 18 months · red > 18 months

---

## Per-Company JSON Schema

Each file in `data/companies/` follows this structure:

```json
{
  "company": "SK Hynix",
  "ticker": "000660.KS",
  "last_updated": "2026-05-11",

  "snapshot": {
    "revenue_qtr": "$4.97B (Q1 2026)",
    "op_margin_pct": 30,
    "hbm_market_share_pct": 50,
    "headcount": 30000,
    "market_cap_usd_bn": 85
  },

  "product_roadmap": [ ... ],

  "scm_engagement": {
    "scm_role": "...",
    "server_products": [
      {
        "name": "HBM3e 24GB 8-Hi Stack",
        "type": "High-bandwidth memory",
        "used_in": "NVIDIA H200 SXM5",
        "bandwidth": "1.23 TB/s",
        "note": "..."
      }
    ],
    "upstream_from": [ "ASML EUV", "Tokyo Electron CVD/ALD", ... ],
    "downstream_to": [ "NVIDIA (H200/B200)", "TSMC (CoWoS bonding)", ... ],
    "scm_position": "HBM memory tier — supplies HBM to TSMC CoWoS for all NVIDIA AI GPUs"
  },

  "lead_time": {
    "total_months_to_token": 12,
    "description": "...",
    "bottleneck": "TSMC CoWoS packaging slot — 18-month lead for new capacity additions",
    "pipeline": [
      { "stage": "HBM wafer production", "weeks": 10, "owner": "SK Hynix" },
      { "stage": "TSV drilling + die attach", "weeks": 4, "owner": "SK Hynix" },
      { "stage": "HBM stack test", "weeks": 2, "owner": "SK Hynix" },
      { "stage": "TSMC CoWoS bonding", "weeks": 12, "owner": "TSMC" },
      { "stage": "GPU system integration", "weeks": 8, "owner": "NVIDIA/ODM" },
      { "stage": "Datacenter deployment", "weeks": 12, "owner": "Hyperscaler" }
    ]
  },

  "key_events": [
    {
      "date": "2024-01",
      "event": "HBM3e 8-Hi enters mass production — first to market ahead of Samsung and Micron",
      "category": "product",
      "significance": "high"
    },
    ...
  ],

  "key_contacts": [ ... ],
  "recent_news": [ ... ],
  "flagged_news": [ ... ],
  "sales_hooks": [ ... ],
  "competitive_position": { ... },
  "financials_history": { ... },
  "sources": [ ... ]
}
```

### Event Categories

| Category | Color | Examples |
|---|---|---|
| `product` | Blue | Product launches, new node qualifications, sampling milestones |
| `financial` | Green | Earnings beats/misses, guidance changes, CapEx commitments |
| `capacity` | Yellow | Fab expansions, CoWoS capacity adds, datacenter buildouts |
| `risk` | Red | Export controls, yield failures, supply disruptions, regulatory blocks |
| `org` | Gray | Leadership changes, JVs, M&A, partnerships |
| `strategy` | Purple | Technology pivots, long-term roadmap announcements |

---

## How to Run

### Open the Dashboard

```bash
open company_intel/dashboard/index.html
```

No server needed. All data is inlined as JavaScript constants at build time.

### Update All Company Profiles (News + Financials)

```bash
cd company_intel
python3 run.py
python3 build_dashboard.py
```

`run.py` runs three agents per company:
- `news_agent` — fetches Google News RSS, flags supply-chain-relevant articles
- `ir_agent` — pulls quarterly revenue/CapEx from seed data
- `product_agent` — updates product roadmap status

### Rebuild Dashboard Only (No Fetch)

```bash
cd company_intel
python3 build_dashboard.py
```

Reads existing JSON profiles, regenerates `dashboard/index.html`. Fast — runs in < 1 second.

### Add a New Company

1. Add an entry to `TARGET_COMPANIES` in `config.py`:
   ```python
   { "id": "samsung_electronics", "name": "Samsung Electronics", "ticker": "005930.KS",
     "layer": "HBM", "ir_url": "...", "news_query": "Samsung HBM semiconductor" }
   ```
2. Create `data/companies/samsung_electronics.json` with at minimum `company`, `ticker`, `snapshot`, `product_roadmap`
3. Add SCM engagement data manually or run `enrich_scm.py` pattern
4. Add lead time and key events following the schema above
5. Run `python3 build_dashboard.py`

---

## Dashboard UI Guide

### Sidebar

- **Supply Chain Overview** — flow diagram, all-company table, global timeline
- Company buttons grouped by layer — click to open that company's profile

### Per-Company View (top to bottom)

1. **Snapshot** — 4 key metrics, layer-specific (HBM shows market share; Hyperscaler shows CapEx guidance)
2. **SCM Engagement** — role description, SCM position, upstream suppliers (red tags), downstream customers (green tags), server products table with key specs
3. **Lead Time Pipeline** — horizontal stage bar from company action → AI tokens; bottleneck stage in red
4. **Company Timeline** — key events 2023–2026, sorted chronologically, color by category
5. **Sales Hooks** — blue-highlighted conversation starters for sales meetings
6. **Product Roadmap** — layer-specific columns (BW/TB/s for HBM; HBM GB/GPU for GPU; WPM for Foundry)
7. **Competitive Position** — key differentiators and gaps
8. **Revenue / CapEx Chart** — quarterly trend bar chart
9. **HBM Market Share Chart** — doughnut (HBM layer only)
10. **Hyperscaler CapEx Comparison** — multi-line chart (Hyperscaler layer only)
11. **Recent News** — up to 8 articles; flagged articles marked with ★

### Overview Global Timeline

- Shows all 148 events from all 18 companies, sorted by date
- **Layer filter** — click any layer button to show only that layer's events
- **Category filter** — click any category (product, financial, capacity, risk, org, strategy)
- Click a company name in the timeline to jump to that company's profile
- Events from 2023-07 to 2026-05

---

## Key Sales Insights Built In

### TSMC CoWoS is the Universal Chokepoint

Every HBM supplier (SK Hynix, Samsung, Micron) and every GPU customer (NVIDIA) flows through TSMC CoWoS. New CoWoS capacity takes 18 months. This is the single most important supply constraint in the global AI stack — any news about TSMC CoWoS expansion or allocation is a tier-1 signal.

### Samsung's Yield Problem is a Competitive Opening

Samsung HBM3e failed NVIDIA qualification as of Q1 2026. This means NVIDIA is ~100% dependent on SK Hynix for H200/B200 HBM. If Samsung resolves qualification, their 35% market share can actually ship to NVIDIA — a major supply increase. If not, it creates a secondary market for SK Hynix pricing power.

### China Chain is 2 Generations Behind, But Self-Funding

CXMT/SMIC/Huawei form a complete domestic AI supply chain — GPU + foundry + HBM-equivalent — all without EUV. The technology gap is ~2 generations (HBM2E vs HBM3e, N+2 vs N3). The state subsidy means this gap will narrow regardless of commercial logic. The lead indicator to watch is SMIC N+2 yield improvement.

### Power is the Next 3-Year Constraint

Hyperscaler CapEx is now >$700B for 2026. The power layer (Constellation, GE Vernova, Vertiv) has 18-48 month lead times. Grid transformer manufacturing is a 36-month backlog. Nuclear restart is 48 months minimum. Orders placed in 2026 deliver AI capacity in 2028-2030 — this is the next generational constraint after CoWoS.

### Hyperscalers Have the Shortest Lead Times for a Reason

Microsoft (3 months), Google (4 months), Meta (4 months) can deploy AI capacity so fast because they pre-positioned: they placed TSMC CoWoS orders 18 months earlier, reserved HBM 12 months earlier, and built out power infrastructure 24+ months earlier. The "3-month" number reflects deployment of already-procured inventory, not procurement to deployment.

---

## Maintenance

### Refreshing News

Run `python3 run.py` weekly or before any customer meeting. News fetched from Google News RSS — no API key required.

### Updating Financials

Edit the quarterly earnings values directly in the company JSON files after each earnings call, then rebuild:
```bash
python3 build_dashboard.py
```

### Updating Lead Times or Key Events

Edit `enrich_timeline.py` (the `TIMELINE_DATA` dict) with new events or revised pipeline stages, then re-run:
```bash
python3 enrich_timeline.py
python3 build_dashboard.py
```

### Adding SCM Engagement Detail

Edit `enrich_scm.py` (the `SCM_DATA` dict) to add/update server products, upstream/downstream relationships, then re-run:
```bash
python3 enrich_scm.py
python3 build_dashboard.py
```

---

## Build Stats

| Metric | Value |
|---|---|
| Companies | 18 |
| SCM Layers | 7 |
| Total Key Events | 148 |
| Server Products Documented | 74 |
| Lead Time Range | 3 months (MSFT) — 48 months (CEG) |
| Dashboard Size | 205,786 bytes (self-contained) |
| Charts | HBM market share doughnut, revenue/CapEx bar, hyperscaler CapEx comparison line |
| Data Sources | Google News RSS, AI_SCM seed data, company IR filings |
| Last Enriched | 2026-05-11 |
