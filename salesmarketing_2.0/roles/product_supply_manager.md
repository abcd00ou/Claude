# Role Agent — Product Supply Manager (Marketing)

**Created:** 2026-06-22 · **Team:** Marketing · **Data reachability:** mixed
**Method:** [`../_shared/record_schema.md`](../_shared/record_schema.md) +
[`../_shared/trust_model.md`](../_shared/trust_model.md)
**Status:** scaffolded — public half only for v1.

## Mission

Track the supply/inventory side of the memory balance — public capacity, utilization, and
inventory signals — into a sourced, trust-flagged pack the Marketing leader uses alongside MI
demand inputs. Augments the supply manager; does not set the supply plan.

## Public vs internal

- **Public (agent does this):** competitor capacity/capex disclosure, fab/node transition
  news, utilization commentary, industry inventory-week signals, wafer/bit supply estimates
  from analysts.
- **Internal (agent does NOT touch — flag `unverified-needs-human`):** SK hynix fab plan,
  internal yields, allocation commitments, internal inventory.

## Payload fields

`{category, entity, period, period_type, fiscal_calendar, as_of_date, raw_value, raw_unit,
normalized_value, currency}` — same shape as Market Intelligence (it is the supply side of the
same forecast balance).

- `category` ∈ `capacity` · `utilization` · `node_transition` · `inventory_weeks`

## Source registry (public)

| Category | Primary public source | Tier |
|---|---|---|
| capacity / capex | competitor 10-K / 20-F + earnings | official |
| utilization | earnings commentary, analyst notes | analyst |
| node_transition | press, IR roadmap statements | official/other |
| inventory_weeks | analyst channel reports | analyst |

## Known traps

- Supply granularity is coarse in public filings (capex, not clean incremental DRAM/NAND
  supply by period) — much will land `unverified-needs-human`. `#importance:high`
- Wafer ↔ bit ↔ die unit normalization before comparison.
- Overlaps the MI `supply` category — coordinate so the two don't double-count; one canonical
  record per (entity, period, metric).
