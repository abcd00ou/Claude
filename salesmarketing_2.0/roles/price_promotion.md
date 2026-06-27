# Role Agent — Price & Promotion (Marketing)

**Created:** 2026-06-22 · **Team:** Marketing · **Data reachability:** mixed
**Method:** [`../_shared/record_schema.md`](../_shared/record_schema.md) +
[`../_shared/trust_model.md`](../_shared/trust_model.md)
**Status:** scaffolded — public half only for v1.

## Mission

Gather and normalize the market-price context a price & promotion manager needs each cycle —
public ASP trends, competitor pricing moves, channel/spot signals — into a sourced,
trust-flagged pack. Augments the manager's pricing judgment; does not set prices.

## Public vs internal (the data split)

- **Public (agent does this):** street/channel ASP, competitor list-price and promotion
  moves, spot/contract index commentary, distributor pricing signals.
- **Internal (agent does NOT touch — flag `unverified-needs-human` / `license-blocked`):**
  SK hynix quote prices, contract terms, margin, internal promotion approvals.

Only the public half is in v1 scope. Same trust model means an internal number simply gets
flagged for the human, never fabricated. `#importance:high`

## Payload fields

`{metric, product_family, region, channel, as_of_date, raw_value, raw_unit, normalized_value,
currency}` — on top of the shared envelope.

- `metric` ∈ `street_asp` · `competitor_list_price` · `promo_discount` · `spot_index` · `contract_index`
- `product_family` — canonical id (e.g. DDR5-16Gb, HBM3E-stack)
- `channel` ∈ `retail` · `distributor` · `spot` · `contract`

## Source registry (public)

| Metric | Primary public source | Tier |
|---|---|---|
| street_asp / competitor_list_price | retailer + distributor listings, price trackers | other |
| spot_index / contract_index | published memory price indices + analyst commentary | analyst |
| promo_discount | competitor promotion pages / trade press | other |

## Known traps

- Most sources are `other` tier (price trackers, listings) → confidence caps low; many values
  land `unverified-needs-human` by design. That is correct behavior, not a failure.
- Currency + unit normalization ($/GB vs $/die vs $/module) before comparison.
- Promotion text is high prompt-injection risk (marketing pages) — rely on the data/instruction
  separation rule in the trust model.

## Open questions

- Which product families + regions are in scope (mirror the MI entity set?).
- Index licensing — published price indices often have redistribution limits (`license-blocked`).
- Cadence: pricing moves faster than the forecast; likely weekly vs MI's quarterly.
