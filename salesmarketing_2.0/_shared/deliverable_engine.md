# Shared Deliverable Engine — leader PPT/Word generation

**Created:** 2026-06-22 · **Used by:** every leader agent · **v1 target:** PPT-first

The engine a leader agent runs to turn the team's trust-flagged packs into a draft
**PPT** (Word is the same pipeline, different renderer — see end). The non-negotiable
property: **no claim reaches a slide unless it traces to a `verified`/`reconciled` record.**
Everything weaker goes to the gap report for the human leader to fill with judgment.

## Inputs

- **Team packs** — canonical records from the team's worker agents (see
  [`record_schema.md`](record_schema.md)). Already status/confidence-flagged.
- **Brief** — what the leader wants this deliverable to be (see Brief intake below).

## Pipeline

```
  1. BRIEF      ─▶ 2. SELECT ─▶ 3. SYNTHESIZE ─▶ 4. DRAFT ─▶ 5. GAP REPORT ─▶ 6. HUMAN EDIT
   audience+date    relevant +     audience          PPT with        what's missing      leader
   +topic+format    USABLE only    template arc      cited claims     / needs-human       finalizes
```

### 1. Brief intake
Leader specifies: `audience` (customer name | conference | internal-review), `date`,
`topic`, `format` (`pptx` | `docx`), `length` (slide/page budget), `language`.

### 2. Select (the trust filter)
- Pull records relevant to the brief: filter by customer/topic match, recency window,
  and `#importance`.
- **Keep only `verified`/`reconciled` records.** `unverified-needs-human` records are NOT
  dropped silently — they are routed to the gap report (step 5).
- Deduplicate by entity + period + metric (prefer higher `source_tier`).

### 3. Synthesize
Structure the selected facts into a narrative using the audience template (each leader spec
lists its templates; e.g. customer-meeting vs conference vs pricing-review have different
arcs). The narrative is an ordering + grouping of facts, not new claims — Facts-Only still
holds; interpretation is the human leader's.

### 4. Draft (PPT structure)
A deck is:
```
  cover  ·  agenda  ·  [content slides]  ·  gap slide  ·  sources appendix
```
Each **content slide**:
- **headline** = the slide's single claim (must trace to ≥1 usable record).
- **support** = 1–4 facts, each one record (number + unit + period + entity).
- **speaker notes** = for every fact: the `source`, `source_url`, `quote`, `status`,
  `confidence`. This is the traceability layer — a reviewer can audit any number to its source.
- **No naked numbers rule:** a number with no cited record cannot appear. If the narrative
  needs it and no record exists, it becomes a gap, not a guess.

### 5. Gap report (always attached)
A list the leader must resolve before the meeting. Each row:
`{wanted fact, why it matters, best status found, reason flagged, what the leader must supply}`.
This is where `needs-human` items surface — the agent says "I couldn't trust this" instead of
fabricating. A customer deck with naked or wrong numbers is the failure this prevents.

### 6. Human edit
Leader reviews the draft + gap report, fills judgment, finalizes. Optionally, the leader's
factual corrections feed back as ground truth for the workers' next cycle.

## Trigger / orchestration (blend model — chosen 2026-06-22)

- **Workers run on cadence** — each worker task refreshes its pack on a schedule (per task;
  e.g. MI quarterly, Price & Promotion weekly). Packs are always reasonably fresh.
- **Deliverables are meeting-driven + on-demand** — a scheduled customer meeting / conference
  date, or a manual leader request, triggers the engine against the latest packs. If a pack
  is stale relative to the meeting, the engine flags it (stale-source) rather than blocking.

## Quality gates (a draft is not "done" until all pass)

1. Every number on every slide traces to a cited record. `#importance:high`
2. No `unverified-needs-human` fact placed as a slide claim — all in the gap report.
3. Sources appendix lists every record used, with `source_url` + `status`.
4. Gap report attached and non-silent.
5. Language + length within the brief.

## Word (`docx`) variant

Same 6-step pipeline; step 4 renders a document instead of slides: sections replace slides,
inline citations replace speaker notes, the gap report becomes a "Open items" section. PPT is
detailed first (v1); Word reuses select/synthesize/gap untouched.

> Generation of the actual `.pptx`/`.docx` binary is an app-layer concern (deferred — this
> repo is markdown specs). This file specifies the structure, rules, and templates the app
> will implement.
