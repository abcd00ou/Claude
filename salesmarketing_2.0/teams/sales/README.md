# Sales Team — end-to-end construct

**Created:** 2026-06-23 · **Status:** detailed (replicates the Marketing template)

The Sales team, built on the same pyramid as Marketing. Its leader produces the **flagship
deliverable of the whole app: the customer-meeting deck** — the original use case ("if my role
is leader, I make a PPT before meetings with customers"). That deck pulls **cross-team** facts.

## Team dataflow (note the cross-team pull)

```
  SALES WORKERS (cadence)              CROSS-TEAM PACKS (shared schema)
  ┌────────────────┐ ┌──────────────┐   Marketing: MI demand · price · supply
  │ Product        │ │ Customer     │   Product Planning: roadmap · design wins
  │ Allocator      │ │ Relation Mgr │          │
  │ (demand ctx)   │ │ (cust brief) │          │
  └───────┬────────┘ └──────┬───────┘          │
          │ demand-ctx pack  │ customer pack    │
          └────────┬─────────┴──────────────────┘
                   ▼
         ┌──────────────────────┐
         │ Sales Team Leader    │ ── Deliverable Engine ──▶ customer-meeting PPT
         │ (no crawling)        │     (meeting-driven)        + gap report
         └──────────┬───────────┘
                    ▼
             human leader edits ──▶ final deck for the customer meeting
```

## Members

| Agent | Type | Spec | Tasks | Cadence |
|---|---|---|---|---|
| Product Allocator | worker | [`../../roles/product_allocator.md`](../../roles/product_allocator.md) | 2 | quarterly + event |
| Customer Relation Mgr | worker | [`../../roles/customer_relation_manager.md`](../../roles/customer_relation_manager.md) | 3 | weekly + event |
| **Team Leader** | leader | [`leader.md`](leader.md) | 3 deliverables | meeting / on-demand |

Detailed task specs: [`workers.md`](workers.md).

## Cross-team consumption rule (new — emerges here)

A customer-meeting deck needs market context (Marketing) + roadmap (PP) + the customer
relationship picture (Sales). Because **every team writes the same canonical record + trust
model**, a leader can pull any team's `verified`/`reconciled` records. Rule: leaders read
cross-team packs read-only; the owning worker remains the single writer of its records (no
double-writing a fact). This is why the shared contract was worth building.

## Honest scope note

Two of the three Sales workers are **internal-data heavy** (allocator, and the relationship
half of CRM). v1 delivers their **public halves** (demand context, customer public signals);
the internal core is flagged `unverified-needs-human` and surfaced in the leader's gap report
until data-access/governance is resolved.
