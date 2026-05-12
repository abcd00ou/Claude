# DBA Agent

**Role:** Knowledge schema design, source standards, tagging, versioning, routing rules  
**Last Updated:** 2026-05-12

---

## Purpose

The DBA Agent defines HOW knowledge is structured, sourced, tagged, dated, and routed
across all agent folders. Every other agent must follow these rules.
This file is the single source of truth for knowledge governance.

---

## Source Quality Standards

### Accepted Source Tiers

| Tier | Source Types | #confidence tag |
|---|---|---|
| S | Peer-reviewed journals, IEEE/ACM/Nature papers, dissertations, JEDEC/SEMI standards | `high` |
| A | SEC filings (10-K, 20-F, 8-K), official company IR, earnings call transcripts | `high` |
| B | Annual reports, named analyst research (Goldman, TF International, Bernstein, Yole), IDC/Gartner | `high` |
| C | Trade press with primary source cited (EE Times, The Register, Nikkei), SEMI data | `medium` |
| D | Analyst estimates (not research reports), trade press without primary citation | `medium` |
| X | Blog posts, social media, anonymous sources, undated content | **Rejected** |

**Rule:** Tier X content is never entered into the knowledge base, even as low-confidence.
If a Tier X claim is worth tracking, find its primary source and cite that instead.

### Required Citation Format

Every knowledge entry (company file, update entry, market file) must include:

```markdown
**Source:** [Full title], [Author/Publisher], [Date YYYY-MM-DD or YYYY-QN], [URL or report name]
```

Examples:
```markdown
**Source:** Q4 2024 Earnings Call Transcript, SK Hynix Investor Relations, 2025-01-30
**Source:** "Memory Market Outlook 2026", TF International Securities, 2025-Q4
**Source:** IEEE ISSCC 2025 Paper #3.1, "HBM4 Architecture Design", 2025-02-16
**Source:** Form 10-K FY2024, NVIDIA Corporation, 2025-02-26, SEC EDGAR
```

---

## File & Folder Structure

### Section Agent Folders
```
agents/section/<segment>/
  README.md          ← agent overview, market overview, key players (living document)
  companies/         ← one file per key company: <company_slug>.md
  market/            ← thematic files: pricing.md, roadmap.md, supply_demand.md
  updates/           ← dated update logs: YYYY-MM.md or YYYY-QN.md
```

### Data Agent Folders
```
agents/data/crawler/
  README.md          ← source registry, crawl cadence, signal taxonomy
  sources/           ← per-source monitoring notes: <source_slug>.md
  signals/           ← extracted signal logs: YYYY-MM-DD.md

agents/data/analysis/
  README.md          ← analysis frameworks and methodology
  models/            ← demand model snapshots: <topic>_<YYYY-QN>.md
  reports/           ← completed analytical reports: YYYY-MM-DD_<topic>.md

agents/data/dba/
  README.md          ← this file
  schema/            ← detailed schema per domain
```

### Orchestrator Folder
```
agents/orchestrator/
  README.md          ← routing logic, agent registry, cross-segment synthesis log
  synthesis/         ← weekly/monthly synthesis reports: YYYY-MM-DD.md
```

### File Naming Rules
- All filenames: `snake_case`, no spaces, no uppercase
- Company files: `<company_slug>.md` (e.g., `sk_hynix.md`, `tsmc.md`, `nvidia.md`)
- Update logs: `YYYY-MM.md` (monthly) or `YYYY-QN.md` (quarterly)
- Reports: `YYYY-MM-DD_<short_topic>.md`

---

## Tagging Schema

Every update entry must carry inline tags on its own line after the source citation.

### Full Tag Set

```
#segment:<value>      which section agent owns this
#source-tier:<value>  S | A | B | C | D
#signal-type:<value>  supply | demand | pricing | roadmap | geopolitical | capex | design-win
#company:<slug>       company in kebab-case
#date:YYYY-MM-DD      date of the original source (not the date of entry)
#importance:<value>   high | medium | low
#confidence:<value>   high | medium | low
#cross-ref:<segment>  present only if the entry also belongs to another segment
```

### Tag Value Definitions

**#segment:**
```
dram | storage | dc_infra | asic | chip_maker | foundry | network | power | substrate | end_market
```

**#source-tier:** (per Source Quality Standards table above)
```
S | A | B | C | D
```

**#signal-type:**
```
supply      — capacity, lead time, yield, availability
demand      — order volume, attach rate, utilization, consumption
pricing     — ASP, spot price, contract price, quote
roadmap     — product announcement, technology milestone, process node transition
geopolitical — export control, trade restriction, foreign investment review, sanctions
capex       — investment guidance, fab expansion, equipment order
design-win  — customer qualification, first silicon, volume commitment
```

**#importance:**
```
high    — affects supply/demand balance, pricing direction, or strategic positioning
medium  — corroborating data, secondary signal, useful context
low     — historical reference, background, baseline data
```

**#confidence:**
```
high    — direct statement from the company or standard body (Tier S/A/B source)
medium  — named analyst estimate or industry data (Tier C source)
low     — indirect implication verbatim from source; no primary confirmation
```

### Example Tagged Entry

```markdown
### Update: 2025-01-30 — SK Hynix guides HBM3E capacity +60% YoY for 2025

> "We expect HBM revenue to at least double in 2025 vs 2024, driven by HBM3E ramp."
> — SK Hynix CFO, Q4 2024 Earnings Call

**Source:** Q4 2024 Earnings Call Transcript, SK Hynix IR, 2025-01-30

#segment:dram #source-tier:A #signal-type:supply #company:sk-hynix
#date:2025-01-30 #importance:high #confidence:high
```

---

## Timeline Organization Rules

1. Within every file, entries are **newest first** (reverse chronological order)
2. Every entry carries a date — minimum granularity: `YYYY`; preferred: `YYYY-MM-DD`
3. The `**Last Updated:**` frontmatter of each README reflects the most recent entry date
4. Update log files (`updates/YYYY-MM.md`) group all entries for that month/quarter
5. Do not edit past entries — append corrections as new entries with a note referencing the original

### Update Entry Template

```markdown
### Update: YYYY-MM-DD — [Short factual title — no interpretation]

> [Direct quote or verbatim paraphrase from source. One paragraph max.]

**Source:** [Full citation]

#segment:X #source-tier:X #signal-type:X #company:X #date:YYYY-MM-DD #importance:X #confidence:X
[#cross-ref:Y — only if relevant to another segment]
```

---

## Cross-Segment Routing Rules

### Rule 1: Toss to existing section
If knowledge entered in section A belongs primarily or equally to section B:
```markdown
→ Toss: agents/section/<B>/updates/YYYY-MM.md
```
Copy the full entry (with source and tags) into section B's update log.
Add `#cross-ref:<B>` to the original entry in section A.

### Rule 2: Toss to multiple sections
If knowledge spans 3+ sections, place the primary entry in the most relevant section
and add a cross-reference note in each other section:
```markdown
→ Cross-ref from agents/section/<A>/updates/YYYY-MM.md: [short title]
```

### Rule 3: Propose a new section agent
If incoming knowledge does not fit any existing segment and represents a recurring,
substantial domain (not a one-off), add to `agents/orchestrator/README.md`:
```markdown
## New Section Proposals
- [ ] <proposed_segment>: [reason] — [date proposed]
```
Do not create the folder until the orchestrator confirms it warrants a dedicated agent.

---

## Facts-Only Rule

Section agent files record facts. Analysis belongs in `agents/data/analysis/`.

| Allowed in section agents | Not allowed in section agents |
|---|---|
| Direct quotes from sources | Conclusions drawn from quotes |
| Stated figures (revenue, capacity, ASP) | Estimated figures not stated by source |
| Verbatim roadmap milestones | Predictions about what will happen |
| Named design wins confirmed by company | Speculated design wins |
| Verbatim implications ("implies", "suggests") tagged `#confidence:low` | Unattributed implications |

If analysis is needed, create a model file in `agents/data/analysis/models/` and
reference it from the section agent update entry.

---

## Versioning Rules

1. **Never delete past entries** — history is permanent; append corrections as new entries
2. **Update `**Last Updated:**`** in the README frontmatter with every change
3. **When a source is superseded** (e.g., new earnings call overrides old guidance), add new entry
   and note `[supersedes: YYYY-MM-DD entry]` in the new entry body
4. **Company files in `companies/`** are living documents — update in place but add a
   dated changelog section at the bottom:
   ```markdown
   ## Changelog
   - YYYY-MM-DD: updated market share from X% to Y% (Source: ...)
   ```
5. **Do not create duplicate files** — check existing structure before creating anything new

---

## Git Commit Rules

- Commit after every meaningful knowledge addition
- Commit message format:
  ```
  [section] <segment>: <factual description of what was added>
  [data] <agent>: <what changed>
  [orchestrator]: <synthesis or routing change>

  Examples:
  [section] dram: add SK Hynix Q4 2024 HBM3E capacity guidance (Tier A)
  [section] foundry: add TSMC Q1 2025 CoWoS capacity commentary
  [data] crawler: register Yole DRAM report as Tier B source
  [orchestrator]: toss TSMC CoWoS entry to chip_maker cross-ref
  ```
- Always `git push` after committing

---

## Schema Changelog

| Date | Change |
|---|---|
| 2026-05-12 | Initial schema created |
