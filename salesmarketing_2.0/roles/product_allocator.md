# Role Agent — Product Allocator (Sales)

**Created:** 2026-06-23 · **Team:** Sales · **Data reachability:** internal-heavy
**Method:** [`../_shared/record_schema.md`](../_shared/record_schema.md) +
[`../_shared/trust_model.md`](../_shared/trust_model.md)
**Status:** scaffolded — thin public contribution for v1; core data is internal.

## Mission

Support allocation decisions by tracking the **public demand context** behind each customer's
allocation ask (their build-out, capex, product ramps), so the human allocator weighs requests
against external signals. The actual allocation — SK hynix supply commitments and fulfillment —
is internal and stays with the human.

## Public vs internal (be honest: this role is mostly internal)

- **Public (agent does this):** customer demand signals — capex, datacenter builds, product
  ramps, stated volume needs from earnings/press. Context for "is this ask backed by real demand?"
- **Internal (agent does NOT touch — flag `unverified-needs-human`):** allocation quantities,
  supply commitments, fulfillment status, customer-specific supply plan. This is the bulk of
  the role. `#importance:high`

## Payload fields

`{customer, product_family, period, demand_signal_type, as_of_date, raw_value, raw_unit,
normalized_value, currency}` — on top of the shared envelope.

- `demand_signal_type` ∈ `capex` · `datacenter_buildout` · `product_ramp` · `stated_volume`

## Source registry (public)

| Signal | Primary public source | Tier |
|---|---|---|
| capex / stated_volume | customer earnings / 10-K | official |
| datacenter_buildout | press, IR, regulatory filings | official/other |
| product_ramp | product announcements, analyst notes | analyst/other |

## Honest scope note

Because the core allocation data is internal, this worker's v1 value is **demand-context only**.
It does not produce an allocation; it gives the human allocator (and the Sales leader's deck) a
sourced read on whether a customer's ask is backed by visible external demand. Full allocation
support waits on the internal-data-access / governance decision (CONSTRUCT.md, design doc OQ7).
