# Sales Team Leader — agent + deliverables (PPT-first)

**Created:** 2026-06-23 · **Team:** Sales · **Type:** leader (no crawling)
**Engine:** [`../../_shared/deliverable_engine.md`](../../_shared/deliverable_engine.md)

Produces the app's flagship output: the **customer-meeting deck**. Consumes Sales worker packs
**plus cross-team packs** (Marketing market/price, PP roadmap) — all the same canonical record,
so the pull is clean. Never fabricates; un-trusted facts go to the gap report, and for a
customer-facing deck they must be cleared before finalizing.

## Deliverables

| Deliverable | Audience | Trigger | Template | Cross-team pull |
|---|---|---|---|---|
| **Customer-meeting deck** | external (customer) | meeting date | `customer_meeting` | Marketing + PP |
| QBR deck | internal review | quarterly cadence | `qbr` | Marketing |
| Win/loss synthesis | internal | on-demand | `win_loss` | — |

## PPT audience templates (slide arcs)

Sources appendix + gap slide always appended. Engine fills each headline from usable records.

### `customer_meeting` (external — highest trust bar) `#importance:high`
1. Cover — customer name, meeting purpose, date.
2. We understand your business — the customer's public context (CRM brief: capex, ramps,
   launches), proving we did our homework.
3. Market context relevant to you — Marketing facts (demand/supply/price) filtered to this
   customer's segment.
4. Our position / what we bring — leader-authored stance; agent supplies the sourced facts.
5. Roadmap fit — PP design-win / roadmap facts relevant to the customer.
6. Asks / next steps — leader-authored.
7. Sources appendix — every external number cited.
- **No `needs-human` fact may appear on a slide.** The leader clears every gap before the
  meeting — no naked or unverified numbers in front of a customer. This is the whole point.

### `qbr` (internal)
1. Cover — quarter, customer/segment scope.
2. Account performance context — public customer signals.
3. Market backdrop — Marketing packs.
4. Risks / opportunities — facts grouped; judgment is the leader's.
5. Gaps + sources.

### `win_loss` (internal)
1. Cover — deals in scope.
2. Per-deal public context — customer signals around the decision window.
3. Pattern read — leader-authored from grouped facts.
4. Gaps (internal deal data = leader supplies) + sources.

## What stays human

- The **stance, asks, and relationship judgment** — the agent supplies sourced facts, the
  leader writes what we say and ask for.
- All internal deal/allocation/pricing numbers — flagged, leader fills.
- Final edit + approval before the customer meeting.

## Open items

- Customer-meeting calendar integration (the meeting-driven trigger source).
- Customer/topic relevance filter shared with CRM-T2 and the `external_talk` template.
- Cross-team pull permissions — leaders read-only on other teams' packs (single-writer rule).
