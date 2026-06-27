# CONSTRUCT — Agentic Sales / Marketing / Product-Planning App (suggested architecture)

**Created:** 2026-06-22 · **Status:** PROPOSAL (design before build) · **Format:** markdown only

The end goal: an app that mirrors the SK hynix memory Sales / Marketing / Product-Planning
org. Worker roles crawl + analyze their domain; leader roles synthesize the team's output
into a **PPT or Word deliverable** for customer meetings, conferences, and presentations.
Every claim in a deliverable traces to a sourced, trust-flagged record.

This doc is the overall construct. The data contract + trust model are already specced in
[`_shared/`](_shared/); the per-role task specs live in [`roles/`](roles/).

## The pyramid (who feeds whom)

```
            ┌──────────────────────────────────────────────────────┐
  LEADER    │  Leader agent (per team)                             │
  LAYER     │  aggregate team packs → select facts → synthesize →  │
            │  generate PPT / Word → gap report → human edits      │
            └───────────────▲──────────────────────────────────────┘
                            │ trust-flagged packs (canonical records)
            ┌───────────────┴──────────────────────────────────────┐
  WORKER    │  Worker agents (per non-leader role)                 │
  LAYER     │  each role runs a few TASKS: crawl → extract →       │
            │  cross-check → status/confidence → analyze → pack    │
            └───────────────▲──────────────────────────────────────┘
                            │ frozen source snapshots
  SOURCE    earnings · filings · analyst notes · price indices · press · standards · internal*
  LAYER     (* internal sources gated on data-access/governance — flagged, never fabricated)
```

Five responsibilities, bottom to top: **SOURCE → CRAWL → ANALYZE → SYNTHESIZE → DELIVER.**

## The two agent types

### Worker agent (one per non-leader role)
- Owns a domain + a short list of **tasks** (see `roles/` and the role table below).
- Runs the shared method: fetch → freeze snapshot → extract (×2 cross-check) → normalize →
  status/confidence → analyze → write a trust-flagged **pack** (canonical records).
- Output is data, not opinion. Modeling/judgment stays with the human (Facts-Only rule).

### Leader agent (one per team)
- Consumes the team's worker packs. Does NOT crawl.
- Runs the **Deliverable Engine** (below) to draft a PPT/Word for a specific audience.
- Surfaces a **gap report** (what's `needs-human` / missing) so the human leader supplies
  judgment instead of the agent guessing.

## Roles → tasks (each role has a few tasks)

| Team | Role | Type | Tasks (v1 sketch) | Data |
|---|---|---|---|---|
| Sales | Product Allocator | worker | allocation-vs-demand tracking · supply-commitment risk flags | internal |
| Sales | Customer Relation Mgr | worker | account-news/earnings watch · pre-meeting customer brief · sentiment | mixed |
| Sales | **Team Leader** | leader | customer-meeting deck · QBR deck · win/loss synthesis | — |
| Marketing | Product Supply Mgr | worker | supply/inventory signal tracking · supply-risk brief | mixed |
| Marketing | Price & Promotion Mgr | worker | ASP/price-index tracking · competitor promo watch · pricing brief | mixed |
| Marketing | Market Intelligence | worker | demand/supply forecast inputs (wedge) · capex watch · demand digest | public |
| Marketing | **Team Leader** | leader | market-update deck · pricing-review deck · conference talk | — |
| Product Planning | Business Enabling | worker | TAM/SAM updates · business-case data pack | mixed |
| Product Planning | Customer Tech | worker | design-win/qual signal tracking · standards-adoption watch · tech brief | mixed |
| Product Planning | **Team Leader** | leader | product-roadmap deck · customer-tech review · standards/conference deck | — |

Each task is a small, named unit with its own source registry + output. Detailed task specs
expand per role in `roles/` (MI, Price & Promotion, Customer Tech already scaffolded).

## The Deliverable Engine (the new top layer)

The leader's PPT/Word generator. Steps:

```
  1. BRIEF      leader specifies: audience (customer X / conference / internal),
                date, topic, format (PPT|Word), length, language.
  2. SELECT     pull relevant records from team packs — filter by customer/topic/
                recency/#importance; ONLY usable (verified|reconciled) status.
  3. SYNTHESIZE structure into a narrative via an audience template
                (customer-meeting ≠ conference ≠ QBR have different arcs).
  4. DRAFT      generate PPT|Word; EVERY claim carries its source record in
                speaker-notes / footnotes (traceable, no naked numbers).
  5. GAP REPORT list every needs-human / missing fact the deck wanted but couldn't
                trust — the leader fills these with judgment.
  6. HUMAN EDIT leader finalizes before the meeting. Edits can feed back as ground truth.
```

**Trust carry-through is the point:** a slide may state a fact only if it traces to a
`verified`/`reconciled` record. Anything weaker is surfaced in the gap report, never silently
placed in a customer deck. This is what makes the output safe to put in front of a customer.

## Trigger / orchestration model (DECISION NEEDED — see end)

Three candidate triggers for running tasks + building deliverables:
- **Meeting/calendar-driven** — "prep for [customer] on [date]" pulls the right tasks + builds the deck.
- **On-demand** — leader requests a deliverable manually.
- **Cadence** — workers refresh on a schedule (e.g. weekly), decks built when asked.
Likely a blend: workers on cadence, deliverables meeting-driven + on-demand.

## How it maps to what already exists

| Existing asset | Role in the construct |
|---|---|
| `agents/orchestrator/` | the orchestration spine (routes tasks, triggers refresh) |
| `agents/section/*/` | domain knowledge the worker agents draw on |
| `agents/data/{crawler,analysis,dba}/` | the crawl + analyze + schema methods |
| `company_intel/`, `AI_SCM/` | existing intel the workers reuse (don't duplicate) |
| `dashboard/` | candidate surface for the app's control panel |
| `salesmarketing_2.0/_shared/` | the canonical record + trust model (data contract) |
| `salesmarketing_2.0/roles/` | per-role task specs |

## The app (target — design only, not built here)

A control surface where a leader: picks an audience + date + format → the system runs the
relevant team tasks (or uses cached packs) → returns a draft PPT/Word + a gap report. Workers
run on cadence in the background. Built only after the construct is detailed and the MI wedge
is validated (The Assignment).

## Phasing (suggested)

1. **Detail the construct** (this stage) — finish role/task specs + the deliverable-engine spec + audience templates, all markdown.
2. **Validate the MI wedge** — The Assignment (shadow one real cycle).
3. **One team end-to-end** — pick a team (recommend Marketing), build its workers + leader + one deliverable as the template.
4. **Replicate** to the other teams; add internal-data roles once governance is resolved.

## Decisions needed before writing the detailed specs

1. **Detail scope** — full-org overview + ONE team fully detailed as the template, or all 10 roles fully detailed now?
2. **Deliverable format priority** — PPT-first, Word-first, or both equally?
3. **Trigger model** — meeting-driven, on-demand, or cadence as the primary?
4. **First team** — which team to detail end-to-end first (Marketing recommended — its MI wedge is furthest along + most public-data).
