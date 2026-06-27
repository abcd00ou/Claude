# Marketing Workers — detailed task specs

**Created:** 2026-06-22 · **Team:** Marketing

Each worker runs a few named **tasks**. A task is the smallest unit: one trigger, one source
set, one output slice of the pack. All tasks emit canonical records (shared schema + trust
model); below specifies what each task uniquely does.

Task spec shape: **Trigger · Sources · Method · Output (payload) · Cadence · Importance · Notes.**

---

## Market Intelligence (worker)

### MI-T1 · Demand/supply forecast inputs (the wedge)
- **Trigger:** quarterly cycle + earnings events.
- **Sources:** hyperscaler earnings/10-K (capex), analyst notes (bit-growth), competitor
  filings (supply), channel/filing signals (inventory).
- **Method:** fetch → freeze snapshot → 2 independent extractors → cross-check → normalize
  (entity/period) → status/confidence → records.
- **Output:** `category ∈ {capex, bit_growth, supply, inventory}` records.
- **Cadence:** quarterly. **Importance:** high.
- **Notes:** prove a memory-relevant input first, not raw capex (weak proxy).

### MI-T2 · Competitor capex watch
- **Trigger:** earnings season (event-driven).
- **Sources:** hyperscaler + foundry + memory-maker earnings calls/filings.
- **Output:** `category = capex` records by entity/period, with guidance deltas.
- **Cadence:** event. **Importance:** medium.

### MI-T3 · Demand-signal digest
- **Trigger:** weekly roll-up + on leader request.
- **Sources:** the latest MI-T1/T2 records + analyst demand commentary.
- **Method:** select usable records, summarize what changed vs last digest (diff).
- **Output:** a short digest pack (no new claims — re-uses existing records).
- **Cadence:** weekly. **Importance:** medium.

---

## Price & Promotion (worker)

### PP-T1 · ASP / price-index tracking
- **Trigger:** weekly.
- **Sources:** published memory price indices + analyst price commentary, retailer/distributor
  listings.
- **Output:** `metric ∈ {street_asp, spot_index, contract_index}` records by product_family/region.
- **Cadence:** weekly. **Importance:** high.
- **Notes:** most sources are `other`/`analyst` tier → many land `needs-human`; correct by design.

### PP-T2 · Competitor promotion watch
- **Trigger:** weekly + ad-hoc on competitor announcements.
- **Sources:** competitor promotion pages, trade press.
- **Output:** `metric ∈ {competitor_list_price, promo_discount}` records.
- **Cadence:** weekly. **Importance:** medium.
- **Notes:** high prompt-injection risk (marketing pages) → data/instruction separation.

### PP-T3 · Pricing recommendation brief
- **Trigger:** on leader request (pricing review prep).
- **Sources:** PP-T1/T2 records (no new crawling).
- **Method:** select usable price records, structure into the pricing-review template input.
- **Output:** a brief pack feeding the leader's pricing-review deck.
- **Cadence:** on-demand. **Importance:** medium.
- **Notes:** internal quote/margin numbers are flagged `unverified-needs-human` (license-blocked/internal).

---

## Product Supply Manager (worker)

### SM-T1 · Supply / capacity signal tracking
- **Trigger:** quarterly + earnings events.
- **Sources:** competitor 10-K/20-F, capex disclosure, fab/node-transition press.
- **Output:** `category ∈ {capacity, utilization, node_transition}` records.
- **Cadence:** quarterly. **Importance:** high.
- **Notes:** coarse public granularity → much `needs-human`; coordinate with MI `supply` to
  avoid double-count (one canonical record per entity/period/metric).

### SM-T2 · Inventory-week signal brief
- **Trigger:** monthly + on leader request.
- **Sources:** analyst channel/inventory reports.
- **Output:** `category = inventory_weeks` records.
- **Cadence:** monthly. **Importance:** medium.
