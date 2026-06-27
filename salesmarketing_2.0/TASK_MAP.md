# TASK MAP — relations, procedure, timeline

**Created:** 2026-06-23 · **Scope:** all teams, all tasks, organically connected

How every task across Sales / Marketing / Product Planning connects: what feeds what
(dependency graph), when each fires (timeline), and where they converge (the customer
meeting). This is the orchestration layer over [`CONSTRUCT.md`](CONSTRUCT.md).

## Legend — task IDs

| ID | Role (team) | Task |
|----|-------------|------|
| MI-T1 | Market Intelligence (Mktg) | demand/supply forecast inputs |
| MI-T2 | Market Intelligence (Mktg) | competitor capex watch |
| MI-T3 | Market Intelligence (Mktg) | demand-signal digest |
| PP-T1 | Price & Promotion (Mktg) | ASP / price-index tracking |
| PP-T2 | Price & Promotion (Mktg) | competitor promotion watch |
| PP-T3 | Price & Promotion (Mktg) | pricing recommendation brief |
| SM-T1 | Product Supply Mgr (Mktg) | supply / capacity tracking |
| SM-T2 | Product Supply Mgr (Mktg) | inventory-week brief |
| AL-T1 | Product Allocator (Sales) | customer demand-context tracking |
| AL-T2 | Product Allocator (Sales) | allocation-vs-demand brief* |
| CRM-T1 | Customer Relation Mgr (Sales) | customer account-news watch |
| CRM-T2 | Customer Relation Mgr (Sales) | pre-meeting customer brief |
| CRM-T3 | Customer Relation Mgr (Sales) | customer sentiment digest |
| CT-T1 | Customer Tech (Prod Planning) | design-win / qualification tracking |
| CT-T2 | Customer Tech (Prod Planning) | standards-adoption watch |
| CT-T3 | Customer Tech (Prod Planning) | tech roadmap brief |
| BE-T1 | Business Enabling (Prod Planning) | TAM / SAM updates |
| BE-T2 | Business Enabling (Prod Planning) | business-case data pack* |

> `PP-T*` = **Price & Promotion** tasks (Marketing). "Product Planning" is always spelled out.
> `*` = internal-data-gated; v1 produces the public half only.

Leader deliverables (consume packs, never crawl):

| ID | Leader | Deliverable | Trigger |
|----|--------|-------------|---------|
| D-MKT-UPDATE | Marketing | market-update deck | weekly + on-demand |
| D-MKT-PRICE | Marketing | pricing-review deck | on-demand |
| D-MKT-TALK | Marketing | conference / external talk | meeting/conf date |
| D-SAL-CUST | Sales | **customer-meeting deck** | meeting date |
| D-SAL-QBR | Sales | QBR deck | quarterly |
| D-SAL-WL | Sales | win/loss synthesis | on-demand |
| D-PLN-ROADMAP | Prod Planning | product-roadmap deck | on-demand |
| D-PLN-CTREVIEW | Prod Planning | customer-tech review | cadence |
| D-PLN-CONF | Prod Planning | standards/conference deck | conf date |

## 1. Dependency graph (what feeds what)

Data flows upward: sources → worker tasks → intra-role briefs → leaders → deliverables.

```
 SOURCES (public): earnings · filings · analyst notes · price indices · press · standards
 ────────────────────────────────────────────────────────────────────────────────────────

 MARKETING
   MI-T1 forecast inputs ─┐
   MI-T2 capex watch ─────┼──▶ MI-T3 demand digest ─┐
   SM-T1 capacity ────────┼───(dedup: one canonical ┤
   SM-T2 inventory ───────┤    record per entity/    ├──▶ MARKETING LEADER ─┬─▶ D-MKT-UPDATE
   PP-T1 ASP index ───┐   │    period/metric)        │                      ├─▶ D-MKT-PRICE
   PP-T2 promo watch ─┴──▶ PP-T3 pricing brief ──────┘                      └─▶ D-MKT-TALK

 SALES
   AL-T1 demand ctx ───▶ AL-T2 alloc brief* ─┐
   CRM-T1 news watch ──▶ CRM-T2 cust brief ───┼──▶ SALES LEADER ─┬─▶ D-SAL-CUST  ◀═╗
   CRM-T3 sentiment ──────────────────────────┘                  ├─▶ D-SAL-QBR    ║ cross-team
                                                                  └─▶ D-SAL-WL     ║ pull
 PRODUCT PLANNING                                                                  ║
   CT-T1 design-win ──┐                                                            ║
   CT-T2 standards ───┼──▶ CT-T3 tech brief ─┐                                     ║
   BE-T1 TAM/SAM ─────┤                       ├──▶ PLANNING LEADER ─┬─▶ D-PLN-ROADMAP
   BE-T2 biz-case* ───┘                       │                     ├─▶ D-PLN-CTREVIEW
                                              └─────────────────────┴─▶ D-PLN-CONF
```

### Intra-role chains (a task feeds its own role's brief)
- `MI-T1, MI-T2 → MI-T3` (digest summarizes the raw inputs)
- `PP-T1, PP-T2 → PP-T3` (pricing brief from ASP + promo)
- `AL-T1 → AL-T2` · `CRM-T1 → CRM-T2` · `CT-T1, CT-T2 → CT-T3`

### Cross-worker coordination (no double-counting)
- `MI-T1 (supply) ⇄ SM-T1 (capacity)` — same entity/period/metric space; one canonical
  record, owned by one writer. Dedup before either pack ships.

## 2. Convergence — the customer-meeting deck pulls all three teams

`D-SAL-CUST` is where the org connects. The Sales leader reads cross-team packs (read-only;
each worker stays the single writer of its records):

```
                         ┌──────────────────────────────┐
   Sales  CRM-T2 ───────▶│                              │
          (cust brief)   │   D-SAL-CUST                 │
                         │   customer-meeting deck      │──▶ gap report ─▶ human leader
   Mktg   MI-T3 ────────▶│   (Deliverable Engine,       │     (clears every gap before
          PP-T3 ────────▶│    external trust bar:        │      the meeting — no naked
          SM packs ─────▶│    no needs-human on a slide) │      numbers to a customer)
                         │                              │
   Plan   CT-T3 ────────▶│                              │
          (roadmap fit)  └──────────────────────────────┘
```

Slide arc maps to sources: *understand your business* ← CRM-T2; *market context* ← MI-T3 +
PP-T3 + SM; *roadmap fit* ← CT-T3; *our position / asks* ← human leader.

## 3. Timeline — when each task fires (procedure by cadence)

```
 LANE            TASKS                                         TRIGGER
 ───────────────────────────────────────────────────────────────────────────────
 WEEKLY          PP-T1 · PP-T2 · CRM-T1 · CRM-T3 · MI-T3       schedule
 MONTHLY         SM-T2                                          schedule
 QUARTERLY       MI-T1 · SM-T1 · AL-T1 · D-SAL-QBR             forecast cycle
 EVENT-DRIVEN    MI-T2 · CRM-T1 · CT-T1 · CT-T2                 earnings / announcements
 MEETING-DRIVEN  CRM-T2 · D-SAL-CUST · D-MKT-TALK · D-PLN-CONF  calendar date
 ON-DEMAND       PP-T3 · AL-T2 · MI-T3 · BE-T2 · all D-* decks  leader request
```

### Typical quarter (rhythm)
```
  Wk 0 ─────────────── Wk 4 ─────────────── Wk 8 ─────────────── Wk 13
  │ quarterly refresh   │ weekly cadence ───────────────────────▶ │ QBR
  │ MI-T1 SM-T1 AL-T1   │ PP-T1/2 CRM-T1/3 MI-T3 (every week)      │ D-SAL-QBR
  │                     │ SM-T2 (monthly)                          │
  ▼                     ▼  ◀── earnings season: MI-T2, CT-T1/2 ──▶ ▼
  meeting-driven decks (D-SAL-CUST / D-MKT-TALK) fire ANY time a date lands
```

## 4. Per-team task table (consumes → produces → feeds)

| Task | Cadence | Consumes | Produces | Feeds |
|------|---------|----------|----------|-------|
| MI-T1 | quarterly | sources | demand/supply records | MI-T3, Mktg leader, D-SAL-CUST |
| MI-T2 | event | sources | capex records | MI-T3 |
| MI-T3 | weekly | MI-T1/T2 | demand digest | Mktg leader, Sales leader |
| PP-T1 | weekly | sources | ASP/index records | PP-T3, Mktg leader |
| PP-T2 | weekly | sources | promo records | PP-T3 |
| PP-T3 | on-demand | PP-T1/T2 | pricing brief | D-MKT-PRICE, D-SAL-CUST |
| SM-T1 | quarterly | sources | capacity records | Mktg leader (dedup MI-T1) |
| SM-T2 | monthly | sources | inventory records | Mktg leader |
| AL-T1 | quarterly | sources | demand-context records | AL-T2, Sales leader |
| AL-T2 | on-demand | AL-T1 (+internal*) | alloc brief | Sales leader |
| CRM-T1 | weekly/event | sources | account-news records | CRM-T2, CRM-T3 |
| CRM-T2 | meeting | CRM-T1 | per-customer brief | D-SAL-CUST |
| CRM-T3 | weekly | CRM-T1 | sentiment digest | Sales leader |
| CT-T1 | event | sources | design-win records | CT-T3, Plan leader |
| CT-T2 | event | sources | standards records | CT-T3 |
| CT-T3 | on-demand | CT-T1/T2 | tech brief | D-PLN-ROADMAP, D-SAL-CUST |
| BE-T1 | quarterly | sources | TAM/SAM records | Plan leader |
| BE-T2 | on-demand | BE-T1 (+internal*) | business-case pack | D-PLN-ROADMAP |

## 5. Coordination rules (what keeps it organic, not tangled)

1. **One writer per record.** A `(entity, period, metric)` fact is owned by exactly one task
   (e.g. supply = MI-T1 *or* SM-T1, decided once). No double-write.
2. **Leaders are read-only** across all packs, own-team and cross-team.
3. **Same contract everywhere.** Every task emits the shared canonical record + trust model,
   which is what makes cross-team pulls (section 2) clean instead of glue code.
4. **Trust travels with the fact.** A record's `status`/`source`/`quote` ride along into every
   downstream brief and deliverable, so a customer slide can always be traced to its source.
5. **Internal-gated tasks** (`*`) emit only their public half in v1; internal facts ride as
   `unverified-needs-human` and surface in the leader's gap report.

## 6. End-to-end procedures

### A. Quarterly forecast refresh
1. MI-T1, SM-T1, AL-T1 run the quarterly cycle (fetch → cross-check → status).
2. MI-T1/SM-T1 dedup the supply records (one canonical writer).
3. MI-T3 digests the new inputs; packs are now fresh for any deck.
4. D-SAL-QBR builds from CRM + Marketing packs at quarter end.

### B. Customer meeting prep (the convergence)
1. A meeting date lands → triggers CRM-T2 (pre-meeting brief for that customer).
2. Sales leader runs D-SAL-CUST: pulls CRM-T2 + cross-team MI-T3 / PP-T3 / SM / CT-T3.
3. Engine selects only `verified`/`reconciled` facts; routes everything else to the gap report.
4. Leader clears every gap (supplies internal/judgment facts) — no `needs-human` on a slide.
5. Leader writes the stance/asks; finalizes the deck before the meeting.

> Product Planning tasks (CT-T*, BE-T*) are mapped here for full connectivity; the PP team
> folder (`teams/product_planning/`) is the remaining detail step.
```
