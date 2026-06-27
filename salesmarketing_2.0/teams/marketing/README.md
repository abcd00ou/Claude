# Marketing Team — end-to-end construct (the template)

**Created:** 2026-06-22 · **Status:** detailed reference team (replicate this shape to Sales + PP)

The first team detailed end-to-end. Three worker agents feed one leader agent that produces
PPT deliverables. Everything below is the concrete instance of the
[`../../CONSTRUCT.md`](../../CONSTRUCT.md) pyramid for Marketing.

## Team dataflow

```
  SOURCES (public)
   earnings · filings · analyst notes · price indices · press · standards
        │            │              │
        ▼            ▼              ▼
  ┌───────────┐ ┌──────────────┐ ┌────────────────────┐    WORKER LAYER
  │ Market    │ │ Price &      │ │ Product Supply Mgr │   (cadence refresh,
  │ Intel     │ │ Promotion    │ │                    │    trust-flagged packs)
  └─────┬─────┘ └──────┬───────┘ └─────────┬──────────┘
        │ demand pack  │ price pack        │ supply pack
        └──────────────┼───────────────────┘
                       ▼
            ┌───────────────────────┐                       LEADER LAYER
            │ Marketing Team Leader │  ── Deliverable Engine ──▶ PPT draft
            │ (no crawling)         │      (meeting/on-demand)    + gap report
            └───────────┬───────────┘
                        ▼
                 human leader edits ──▶ final deck for meeting / conference
```

## Members

| Agent | Type | Spec | Tasks | Cadence |
|---|---|---|---|---|
| Market Intelligence | worker | [`../../roles/market_intelligence.md`](../../roles/market_intelligence.md) | 3 (see `workers.md`) | quarterly + event |
| Price & Promotion | worker | [`../../roles/price_promotion.md`](../../roles/price_promotion.md) | 3 | weekly |
| Product Supply Mgr | worker | [`../../roles/product_supply_manager.md`](../../roles/product_supply_manager.md) | 2 | quarterly + event |
| **Team Leader** | leader | [`leader.md`](leader.md) | 3 deliverables | meeting / on-demand |

Detailed task specs: [`workers.md`](workers.md). Leader deliverables + PPT templates:
[`leader.md`](leader.md).

## Trigger model (this team)

- Workers refresh on their own cadence (above); packs always reasonably fresh.
- Leader builds a deck when a customer meeting / conference is scheduled, or on request,
  against the latest packs. Stale packs are flagged (`stale-source`), never block.

## Coordination rules

- One canonical record per `(entity, period, metric)` across the three workers — MI `supply`
  and Product Supply Mgr `capacity` must not double-count.
- All three reuse the shared record schema + trust model; only payloads + sources differ.
- Internal data stays out of v1; flagged `unverified-needs-human`, surfaced in the leader's gap report.
