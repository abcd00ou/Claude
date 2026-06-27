# salesmarketing 2.0 — Agentic Sales / Marketing / Product-Planning specs

**Created:** 2026-06-22
**Source design:** `office-hours → plan-ceo-review → plan-eng-review`
(`~/.gstack/projects/abcd00ou-Claude/idongseong-fix/my-change-design-20260619-101603.md`)

Markdown agent specifications for SK hynix memory Sales / Marketing / Product-Planning
roles. No code — every agent is a `.md` spec, consistent with this repo's convention
(`agents/section/*/README.md`). Each role agent gathers and normalizes its inputs into a
trust-flagged, sourced **pack** the human owner can drop into their workflow. The agents
augment the humans; they do not replace them.

## The shared method (one pattern, every role)

All role agents follow the SAME pipeline and the SAME trust model. The two shared specs
define it once; each role spec only declares its own payload + sources.

```
  source ─▶ fetch + freeze snapshot ─▶ extract ─▶ ×2 cross-check ─▶ normalize
                                                                       │
                  pack  ◀── render ◀── diff vs last cycle ◀── status + confidence
                   │
                   ▼
              human owner reviews/edits ──▶ edits become ground truth (next cycle)
```

- [`_shared/record_schema.md`](_shared/record_schema.md) — the canonical record contract
  (envelope = provenance + trust, identical for every role; payload = what the role tracks).
- [`_shared/trust_model.md`](_shared/trust_model.md) — `status` / `confidence` / `status_reason`,
  the two-independent-extractor cross-check, and the false-verified-rate eval gate.

## Orchestration, map, and data

- [`ORCHESTRATOR.md`](ORCHESTRATOR.md) — the conductor: triggers, run lifecycle, request routing,
  data-source modes (prod vs sandbox), state/freshness, health.
- [`TASK_MAP.md`](TASK_MAP.md) + [`task_map.html`](task_map.html) — every task, how they connect,
  the cadence timeline, and the customer-meeting convergence (HTML = visual).
- [`data/`](data/) — real, sourced 2026 facts (the crawlable layer).
- [`sim/`](sim/) — fictional internal stand-in (production, allocation, customer asks).

## Roles

| Team | Role | Spec | Data reachability | Status |
|---|---|---|---|---|
| Marketing | Market Intelligence | [`roles/market_intelligence.md`](roles/market_intelligence.md) | public (earnings, filings, analyst) | wedge — validate via The Assignment first |
| Marketing | Price & Promotion | [`roles/price_promotion.md`](roles/price_promotion.md) | mixed (public market price + internal quote) | scaffolded — public half only for v1 |
| Product Planning | Customer Tech | [`roles/customer_tech.md`](roles/customer_tech.md) | mixed (public design-win/qual signals + internal) | scaffolded — public half only for v1 |

**Deferred (internal-data roles):** Sales product allocator, Sales CRM, Marketing supply
manager, PP business enabling. Their primary data is internal SK hynix systems an agent
can't reach by crawling; they wait on a data-access / governance decision (see the design
doc OQ7) before scaffolding.

## Build order (from the reviews)

1. **The Assignment first** — shadow one real Market Intelligence forecast cycle: confirm
   inputs are reachable, capture the real template/format, map public-vs-internal, rank the
   decision-driving inputs. Everything past the MI wedge is conditional on this.
2. Market Intelligence agent (the validated wedge).
3. Price & Promotion + Customer Tech — public-data halves, reusing the shared method.
4. Internal-data roles — only after data-access/governance is resolved.

## Non-negotiable rules (inherited from project CLAUDE.md)

- Reliable sources only; every value cites its source.
- Facts only — the pack records what sources state; modeling/judgment stays with the human.
- Newest-first, date-stamped entries; importance tags where relevant.
