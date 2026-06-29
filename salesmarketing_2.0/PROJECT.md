# Sales & Marketing 2.0 — Project Overview

**Created:** 2026-06-30 · **Owner:** abcd00ou · **Format:** markdown (this doc) + the `app/` carve-out
**Design lineage:** `office-hours → plan-ceo-review → plan-eng-review`

A one-page project brief in four parts: **Object · Contents · Implementation · Value-Added.**
For the working detail, see [`CONSTRUCT.md`](CONSTRUCT.md) (architecture), [`ORCHESTRATOR.md`](ORCHESTRATOR.md)
(run lifecycle), [`README.md`](README.md) (role specs), and [`app/README.md`](app/README.md) (the web app).

---

## 1. Object

**Build an agentic AI layer for SK hynix memory Sales / Marketing / Product-Planning that
turns raw market + internal signals into a trust-flagged executive briefing a human leader
approves and sends to the CEO — every morning, automatically.**

The system mirrors the real org as two agent layers:

- **Worker agents** crawl and normalize their domain (market intelligence, pricing, customer
  tech, allocation, …) into sourced, trust-flagged **packs**.
- **Leader agents** (one per team — Sales / Marketing / Product Planning) synthesize their
  team's packs into a C-level deliverable.

Three design commitments fix the scope:

1. **Augment, never replace.** The agent produces a reviewable draft; the human owner edits,
   and those edits become ground truth for the next cycle.
2. **Facts only.** A pack records what sources state; modeling and judgment stay with the human.
3. **Trust is explicit.** Every value is `REAL` (web-sourced, cited) or `SIM` (simulated
   internal stand-in, clearly labeled). A simulated number can never read as real.

**Daily goal:** at 09:00 KST, each of the 3 team leaders receives a draft briefing, reviews it,
and either approves & sends it to the CEO (`abcd00ou@gmail.com`) or regenerates / requests a
data refresh.

---

## 2. Contents

What the project is made of.

### Specification layer (markdown — the construct)
| Artifact | Purpose |
|---|---|
| [`CONSTRUCT.md`](CONSTRUCT.md) | Overall architecture — the worker/leader pyramid, SOURCE→CRAWL→ANALYZE→SYNTHESIZE→DELIVER |
| [`ORCHESTRATOR.md`](ORCHESTRATOR.md) | The conductor — triggers, run lifecycle, request routing, prod-vs-sandbox data modes, health |
| [`TASK_MAP.md`](TASK_MAP.md) + [`task_map.html`](task_map.html) | Every task, how they connect, the cadence timeline, customer-meeting convergence |
| [`_shared/record_schema.md`](_shared/record_schema.md) | Canonical record contract — provenance + trust envelope, per-role payload |
| [`_shared/trust_model.md`](_shared/trust_model.md) | `status` / `confidence` / `status_reason`, two-extractor cross-check, false-verified-rate eval gate |
| [`_shared/deliverable_engine.md`](_shared/deliverable_engine.md) | How packs render into a deliverable |
| [`roles/*.md`](roles/) | Per-role task specs (market intelligence, price & promotion, customer tech, allocation, supply, CRM) |

### Data layer
| Folder | Contents |
|---|---|
| [`data/`](data/) | **Real, sourced 2026 facts** — demand/capex, market price, supply share, tech roadmap (the crawlable layer) |
| [`sim/`](sim/) | **Simulated internal stand-ins** — production, capacity, allocation, customer demand/tech asks (labeled fiction) |
| [`briefings/`](briefings/) | Dated example briefings (`2026-06-27/` — sales, marketing, product_planning) |

### Application layer (the only sanctioned production code)
| Artifact | Purpose |
|---|---|
| [`app/`](app/) | Next.js (TypeScript) human-in-the-loop web app deployed on Vercel — the 9am leader-review flow |
| [`how_it_works.html`](how_it_works.html) | Animated Korean explainer of the end-to-end workflow |

---

## 3. Implementation

How it actually runs.

### The shared method (one pipeline, every role)
```
source ─▶ fetch + freeze snapshot ─▶ extract ─▶ ×2 cross-check ─▶ normalize
                                                                     │
                pack  ◀── render ◀── diff vs last cycle ◀── status + confidence
                 │
                 ▼
            human owner reviews/edits ──▶ edits become ground truth (next cycle)
```

### The daily app flow
```
09:00 KST ─ Vercel Cron ─▶ /api/cron ─▶ generate 3 drafts (Claude + web search) ─▶ store
                                                                                     │
 leader opens app ─▶ 3 tabs (영업 · 마케팅 · 제품기획)                                 │
      ├─ Approve & send to CEO ─▶ /api/approve ─▶ Resend ─▶ abcd00ou@gmail.com         │
      ├─ Regenerate (+ feedback) ─▶ /api/generate                                      │
      └─ Request data update      ─▶ /api/generate (fresh web search)  ◀───────────────┘
```

### Tech stack
- **Next.js 16 (App Router) + TypeScript**, deployed on **Vercel** (root = `salesmarketing_2.0/app`).
- **Anthropic SDK** — model `claude-opus-4-8` (overridable via `ANTHROPIC_MODEL`), the
  `web_search` server tool, adaptive thinking, and `pause_turn` loop handling.
- **Resend** for the executive email; **Vercel KV** (or in-memory fallback) for draft storage.
- **Vercel Cron** `0 0 * * *` (00:00 UTC = 09:00 KST), guarded by `CRON_SECRET`.
- **SK hynix-branded HTML email** — natural executive commentary mixed with tables and
  CSS bar charts (no images), `REAL`/`SIM` labeling throughout. UI + email in Korean.

### What a draft contains
A categorized leader scan panel (`taskUpdates[]`) plus the natural CEO email body
(`emailBlocks[]` — ordered text / table / chart). `REAL` blocks cite a source; `SIM` blocks
are flagged "내부 추정" and a gap section lists what needs human confirmation.

### Build order (from the reviews)
1. **The Assignment first** — shadow one real Market Intelligence forecast cycle to validate
   reachable inputs and the real template before scaling.
2. Market Intelligence agent (the validated wedge).
3. Price & Promotion + Customer Tech — public-data halves, reusing the shared method.
4. Internal-data roles — only after data-access / governance is resolved.

### Honest limitations
- `SIM` data is illustrative, not real SK hynix data, and is never to be treated as fact.
- Generation (Opus + web search) can exceed Vercel Hobby's 60s cap → use **Pro** (`maxDuration` 300s).
- Resend needs a verified sender domain for reliable delivery (free tier uses `onboarding@resend.dev`,
  which only delivers to the account owner).
- Cost: 3 Opus + web-search generations/day plus regenerations — switch to Sonnet to reduce it.

---

## 4. Value-Added

Why it matters.

| Dimension | Without the system | With Sales & Marketing 2.0 |
|---|---|---|
| **Briefing prep** | Hours of manual gathering across earnings, filings, analyst notes, internal sheets | Drafted overnight; the leader reviews, not assembles |
| **Trust** | Numbers mixed with unstated assumptions | Every value tagged `REAL` (cited) or `SIM` (labeled) — no silent guessing |
| **Source discipline** | Claims hard to trace back | Every fact traces to a frozen, sourced snapshot |
| **Cadence** | Ad-hoc, when someone has time | Reliable 09:00 KST delivery, every day |
| **Human control** | All-manual or fully-automated black box | Human-in-the-loop: approve / regenerate / request update; edits feed the next cycle |
| **Scale** | One analyst, one domain at a time | Worker agents fan out across domains in parallel, leaders synthesize |

**Core value:** it compresses the *gather → normalize → cross-check → synthesize* grind into a
reviewable morning draft, while keeping the human firmly in the decision seat and keeping the
line between verified fact and internal estimate impossible to blur. The leader spends their
time on judgment, not assembly — and the CEO gets a consistent, traceable daily read on the
memory market and the customer book.

**Beyond the daily brief:** the same trust-flagged packs feed customer-meeting and conference
deliverables (PPT / Word), so the work done each morning compounds into the org's external
materials rather than being thrown away.
