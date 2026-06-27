# Live Data — real 2026 facts, sourced

**Created:** 2026-06-24 · **Format:** markdown tables · **Gathered via:** web search on 2026-06-24

The **real counterpart to [`../sim/`](../sim/)**. Where `sim/` is fictional internal data, this
folder holds **actual public facts from 2026** (news, analyst notes, company IR, JEDEC) for the
public-data tasks — every value cites a real source, per the project's Reliable-Sources rule.

These are public-source facts as reported on their publication dates; figures (especially
analyst forecasts) reflect the source at that time, not a guarantee. Each row carries a trust
`status` so the [trust model](../_shared/trust_model.md) is visible on real data:

- **verified** — official IR / JEDEC standard / company announcement (single authoritative source).
- **reconciled** — multiple outlets agree on the same figure.
- **unverified-needs-human** — analyst estimate, "reportedly", or rumor → flagged, not trusted.

## Files → which task each feeds

| File | Domain | Feeds (task) |
|---|---|---|
| [`demand_capex.md`](demand_capex.md) | hyperscaler AI capex 2026 | MI capex watch (MI-T2), MI demand (MI-T1) |
| [`market_price.md`](market_price.md) | HBM + DRAM/DDR5/mobile contract price 2026 | Price & Promotion (PP-T1) |
| [`supply_share.md`](supply_share.md) | HBM share + supply-demand tightness 2026 | Product Supply Mgr (SM-T1) ⇄ MI supply |
| [`tech_roadmap.md`](tech_roadmap.md) | HBM4 / HBM4E / LPDDR6 / DDR specs + MP status | Customer Tech (CT-T1/T2), future spec |

## Trust-tier convention used here

| Source type | tier | typical status |
|---|---|---|
| company IR / SK hynix news / SEC filing | official | verified |
| JEDEC standard | official | verified |
| TrendForce / Counterpoint / Goldman forecast | analyst | verified (analyst), lower confidence |
| trade press report ("reportedly", estimate) | other | unverified-needs-human |

> This is a starter database from a single research pass (2026-06-24). It can be widened with
> more searches per task; the sim/ layer covers the internal data this public layer can't reach.
