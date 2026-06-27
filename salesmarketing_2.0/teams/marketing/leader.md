# Marketing Team Leader — agent + deliverables (PPT-first)

**Created:** 2026-06-22 · **Team:** Marketing · **Type:** leader (no crawling)
**Engine:** [`../../_shared/deliverable_engine.md`](../../_shared/deliverable_engine.md)

Consumes the three Marketing worker packs (MI demand, Price & Promotion, Product Supply) and
runs the Deliverable Engine to draft PPTs. Produces three deliverables, each an instance of
the engine with a specific audience template. Never fabricates — un-trusted facts go to the
gap report.

## Deliverables

| Deliverable | Audience | Trigger | Template |
|---|---|---|---|
| Market-update deck | internal review / exec | weekly cadence + on-demand | `market_update` |
| Pricing-review deck | internal pricing decision | on-demand (pricing cycle) | `pricing_review` |
| Conference / customer talk | external (customer / conference) | meeting/conference date | `external_talk` |

## PPT audience templates (slide arcs)

Each template is an ordering of slides; the engine fills each headline from usable records and
routes gaps to the gap report. Sources appendix + gap slide are always appended.

### `market_update` (internal)
1. Cover — period, "what changed this week."
2. Demand signals — from MI packs (capex, bit-growth deltas).
3. Supply signals — from Product Supply packs (capacity, utilization).
4. Price — from Price & Promotion packs (ASP, index moves).
5. Net read — the balance picture (facts grouped, not interpreted by the agent).
6. Gaps — what's `needs-human` this week.
7. Sources appendix.

### `pricing_review` (internal)
1. Cover — product families in scope.
2. ASP trend — street/spot/contract index by family.
3. Competitor moves — list-price + promotion changes.
4. Supply/demand context — one slide pulling MI + Supply.
5. Decision inputs — the facts a pricing decision needs (internal quote/margin = gap, leader supplies).
6. Gaps + sources.

### `external_talk` (customer / conference) — highest trust bar
1. Cover — thesis/title.
2. Market context — only `verified`/`reconciled` macro facts.
3. Relevant-to-this-audience — facts filtered to the customer/topic.
4. Our position — leader-authored (agent supplies sourced facts, not the stance).
5. Takeaway / next steps.
6. Sources appendix (every external number cited).
- **No `needs-human` fact may appear** — external decks are customer-facing; the gap report is
  resolved by the human leader before the talk, not shown. `#importance:high`

## Gap report (leader-facing)

Every deliverable ships with the engine's gap report: `{wanted fact, why, best status found,
reason flagged, what you must supply}`. For `external_talk`, the leader MUST clear or remove
each gap before finalizing — no naked numbers in front of a customer.

## What stays human

- The **stance / narrative judgment** (what the facts mean, what to recommend) — agent supplies
  sourced facts, leader writes the interpretation (Facts-Only rule).
- All internal numbers (quote, margin, allocation) — agent flags, leader fills.
- Final edit + approval before any meeting.

## Open items

- Customer/topic taxonomy for the `external_talk` relevance filter (reuse `company_intel/`?).
- Slide visual template / branding (app-layer, deferred).
- Whether leader edits feed back as worker ground truth (recommended; needs a write path).
