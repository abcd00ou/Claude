# ORCHESTRATOR — salesmarketing 2.0

**Created:** 2026-06-24 · **Role:** the conductor over the whole construct

Coordinates every worker + leader agent: fires task runs on their triggers, assembles packs,
routes incoming requests to the right agents, enforces the coordination rules, picks the right
data source, and tracks freshness/state. It owns *when* and *who*; the agents own *how*.

References: [`CONSTRUCT.md`](CONSTRUCT.md) (architecture), [`TASK_MAP.md`](TASK_MAP.md)
(relations + timeline), [`_shared/`](_shared/) (contract + trust + engine),
[`data/`](data/) (real), [`sim/`](sim/) (internal stand-in).

## What it coordinates (inventory)

- **18 worker tasks** across 3 teams (see TASK_MAP legend).
- **9 leader deliverables** (PPT/Word).
- **2 data layers** — `data/` (real, sourced) + `sim/` (fictional internal).
- **1 contract + trust model** every task shares.

## Trigger model (the scheduler) — blend

```
  CADENCE        weekly / monthly / quarterly  ─▶ refresh worker packs (keep fresh)
  EVENT          earnings / announcement       ─▶ fire event tasks (MI-T2, CRM-T1, CT-T1/2)
  MEETING        calendar date                 ─▶ CRM-T2 + leader deck build
  ON-DEMAND      leader request                ─▶ any task / any deck, now
```

The orchestrator watches these triggers and dispatches. Workers stay fresh on cadence;
deliverables build on meeting/on-demand against the latest packs.

## Run lifecycle (one orchestrated cycle)

```
  TRIGGER ─▶ RESOLVE ─▶ RUN WORKERS ─▶ DEDUP/RECONCILE ─▶ WRITE PACKS ─┐
                                                                        │
   (if deliverable requested)                                          │
   HUMAN EDIT ◀─ GAP REPORT ◀─ DRAFT ◀─ SYNTHESIZE ◀─ SELECT (usable) ◀┘
```

1. **Trigger** — a cadence tick, an event, a meeting date, or a request.
2. **Resolve** — figure out which tasks + which packs are needed (see Routing).
3. **Run workers** — each task: fetch → snapshot → 2 extractors → cross-check → status/confidence.
4. **Dedup/reconcile** — enforce single-writer per `(entity, period, metric)` (e.g. MI-T1 vs SM-T1).
5. **Write packs** — atomic publish (temp → validate → publish); re-runs byte-identical.
6. **Select / synthesize / draft** — leader engine, usable records only, gaps to the report.
7. **Human edit** — leader finalizes; corrections can feed back as ground truth.

## Routing — request → tasks/agents

The orchestrator turns a request into a run plan. Worked example:

> **Request:** "Customer-meeting deck for HYPER-A, 2026-07-10, PPT."

```
  1. audience = HYPER-A (customer) · format = PPT · template = customer_meeting (Sales leader)
  2. needed packs:
       CRM-T2  (HYPER-A pre-meeting brief)         ── own team, meeting-driven → RUN NOW
       MI-T3 · PP-T3 · SM   (market context)       ── cross-team Marketing → pull latest
       CT-T3   (roadmap fit)                        ── cross-team Planning → pull latest
  3. freshness check: any pack stale vs 07-10? → refresh its cadence task or flag stale-source
  4. run CRM-T2; pull cross-team usable records (real data/ only — customer-facing, see modes)
  5. Sales leader → Deliverable Engine → draft + gap report
  6. return to human leader; gaps must be cleared before the meeting
```

Routing rules:
- Map audience → leader + template (customer→Sales/customer_meeting; conference→any/external_talk; internal→QBR/review).
- Map template → required tasks (own-team + cross-team), from the TASK_MAP "feeds" column.
- Pull cross-team packs read-only; the owning worker stays the single writer.

## Data-source routing (data/ vs sim/) — modes

The orchestrator runs in one of two modes and enforces which source feeds tasks:

| Mode | Uses | Customer-facing decks |
|---|---|---|
| **PROD** | `data/` (real, sourced) + live crawl only | allowed (real verified facts only) |
| **SANDBOX** | `data/` + `sim/` (both, all labeled) | NOT allowed — demo/dev only |

Hard rule: a `source = SIMULATION` record can never land on a real customer slide. In PROD the
orchestrator excludes `sim/` entirely; in SANDBOX it lets sim flow but the deck is marked demo.

## State + freshness registry (what it tracks)

A run registry (shape; actual store is app-layer):

| task | last_run | pack | freshness | status |
|---|---|---|---|---|
| MI-T1 | 2026-06-01 | packs/mi_2026Q2 | fresh (≤quarter) | ok |
| PP-T1 | 2026-06-23 | packs/price_wk25 | fresh (≤week) | ok |
| CRM-T2:HYPER-A | — | — | missing | run-on-meeting |

Freshness windows match each task's cadence (week/month/quarter). Stale = older than its window
relative to the request/meeting date.

## Failure & staleness handling

- A task fails → its records ship `unverified-needs-human` (`extraction-failed`); the run continues.
- A pack is stale → flagged `stale-source`, NOT blocked; surfaces in the leader's gap report.
- A source conflict survives reconcile → `conflict` → gap report.
- No single failure ever blocks a whole deliverable; the gap report carries the honesty.

## Health / observability

Per run, the orchestrator aggregates each task's health log into one view: tasks run vs failed,
records by status, **% unverified** (the headline health signal), cross-check disagreements,
stale packs. A spike in % unverified means sources broke or extraction degraded — investigate
before trusting the next deck.

## Maps to existing repo

- `agents/orchestrator/` — this is the salesmarketing-2.0 instance of that role.
- `agents/data/{crawler,analysis,dba}/` — the crawl/analyze/schema methods the workers use.
- The orchestrator does NOT crawl or synthesize itself — it routes, schedules, dedups, and
  enforces. Workers crawl; leaders synthesize; the human decides.
```
