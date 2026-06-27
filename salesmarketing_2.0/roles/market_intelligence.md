# Role Agent — Market Intelligence (Marketing)

**Created:** 2026-06-22 · **Team:** Marketing · **Data reachability:** public
**Method:** [`../_shared/record_schema.md`](../_shared/record_schema.md) +
[`../_shared/trust_model.md`](../_shared/trust_model.md)
**Status:** the chosen wedge — validate via The Assignment before building.

## Mission

Gather and normalize the memory demand/supply **forecast inputs** each cycle into a sourced,
trust-flagged pack the MI analyst drops straight into their model. Augments the analyst; does
not do the modeling judgment.

## Why this is the wedge

The only role whose primary inputs are **public and crawlable** — so an agent can do it
without internal-systems access. Reuses this repo's existing assets (`marketing/` crawlers,
`agents/data/dba/financials.db`, the company files).

## Payload fields

`{category, entity, period, period_type, fiscal_calendar, as_of_date, raw_value, raw_unit,
normalized_value, currency}` — on top of the shared envelope.

- `category` ∈ `capex` · `bit_growth` · `supply` · `inventory`
- `entity` — canonical entity id (not a free-text name)

## Source registry (public)

| Category | Primary public source | Tier |
|---|---|---|
| capex | hyperscaler earnings calls / 10-K | official |
| bit-growth | analyst research notes | analyst |
| supply | competitor 10-K / 20-F + capex disclosure | official |
| inventory | filing/channel signals | analyst/other |

## Known traps (carry into extraction)

- **Capex is a weak proxy** — hyperscaler capex bundles land/buildings/networking/non-memory
  spend, and lands late for a forecast cycle. Phase 1 proves a memory-relevant input, not raw
  capex; capex may run first only as a pipeline/plumbing test. `#importance:high`
- Entity + period normalization (canonical ids, fiscal-vs-calendar) before any comparison —
  the biggest hidden trap.
- The crawlable share of *decision-driving* inputs may be < 70%; some supply/inventory
  numbers are internal. Flag those `unverified-needs-human`, never fabricate.

## The Assignment (do before building)

Shadow one real forecast-input cycle without helping: time how long input-gathering takes,
capture the real template + format, list every source per category, map public-vs-internal,
rank the decision-driving inputs. That artifact is both the demand evidence and the eval
ground truth. Try to observe one normal cycle plus one event-driven/earnings-heavy update.

## Open questions

- Output format (Excel/CSV/PPT) — TBD from the analyst's real template, not assumed.
- Analyst-note licensing/entitlements before automating that source.
- Cadence: monthly / quarterly / event-driven.
