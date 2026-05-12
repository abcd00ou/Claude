# DBA Agent

**Role:** Knowledge schema design, file structure, tagging conventions, versioning  
**Last Updated:** 2026-05-12

---

## Purpose

The DBA Agent is the keeper of knowledge structure. It does not contain market data.
It defines HOW information is organized, tagged, and versioned across all MD files
so the knowledge base remains consistent, searchable, and maintainable over time.

---

## File Naming Conventions

### Section Agent Files
```
agents/section/<segment>.md

Allowed segments:
  dram.md
  storage.md
  dc_infra.md
  asic.md
  chip_maker.md
  foundry.md
  network.md
  power.md
  substrate.md
  end_market.md
```

### Data Agent Files
```
agents/data/<role>.md

Allowed roles:
  crawler.md
  analysis.md
  dba.md  ← this file
```

### Company Intelligence Files
```
company_intel/<company-slug>.md

Examples:
  company_intel/nvidia.md
  company_intel/sk_hynix.md
  company_intel/tsmc.md
```

### Output Reports
```
outputs/<YYYY-MM-DD>-<report-type>.md

Examples:
  outputs/2026-05-12-weekly-synthesis.md
  outputs/2026-Q2-hbm-supply-gap.md
```

---

## Tagging Schema

Every "Recent Developments" entry and synthesized signal must include inline tags:

```markdown
### Update: YYYY-MM-DD — [Short title]
> Signal text here.
> #segment:dram #signal-type:supply #company:sk-hynix #confidence:high
```

### Tag Definitions

**#segment** — which section agent this belongs to:
```
dram | storage | dc_infra | asic | chip_maker | foundry | network | power | substrate | end_market
```

**#signal-type** — nature of the signal:
```
supply | demand | pricing | roadmap | geopolitical | capex | design-win
```

**#company** — company name in kebab-case:
```
nvidia | amd | tsmc | sk-hynix | samsung | micron | google | microsoft | amazon | meta
broadcom | marvell | arista | infineon | on-semi | ibiden | unimicron | mps | renesas
```

**#confidence** — reliability of the signal:
```
high    = direct company statement (earnings, press release, SEC filing)
medium  = analyst estimate, trade press with named source
low     = speculation, unnamed source, inference
```

---

## Section Agent File Structure (Canonical)

Each section agent file MUST follow this structure. Do not add sections without updating
this schema.

```markdown
# [Segment] Expert Agent

**Segment:** [Full name]
**Sales Lens:** [One line — marketing/sales focus]
**Last Updated:** YYYY-MM-DD

---

## Market Overview
[2–4 paragraph landscape description]

---

## Key Players & Market Share
[Table: Company | Share | Notes]

---

## Demand Signals (AI-driven)
[Bullet list of current demand drivers + demand model trigger]

---

## Supply Constraints
[Bullet list of current supply limitations + lead times]

---

## Pricing Trends
[Current ASP ranges, trend direction]

---

## Technology Roadmap
[Table: Technology | Status | AI Relevance]

---

## Sales & Marketing Angles
[Bullet list of sales narratives and positioning]

---

## Recent Developments
[Dated entries in reverse chronological order]
### Update: YYYY-MM-DD — [Title]
> [Signal text with tags]

---

## Open Questions
[Checkbox list of unresolved intelligence gaps]
```

---

## Versioning Rules

1. **Always date-stamp updates** at the top of the file (`**Last Updated:** YYYY-MM-DD`)
2. **Never delete old "Recent Developments" entries** — append new ones at top, keep history below
3. **When an assumption changes**, update the "Demand Model Assumptions Log" in `analysis.md`
4. **Company data changes** → update both the section agent AND company_intel file if it exists
5. **Do not create duplicate files** — check existing structure before creating new files

---

## Cross-Reference Patterns

When a signal in one section agent has implications for another, add a cross-reference:

```markdown
> CoWoS capacity constraint at TSMC limits GPU shipments.
> #segment:foundry #signal-type:supply #company:tsmc #confidence:high
> → Cross-ref: chip_maker.md (supply constraint), dram.md (HBM on-GPU assembly)
```

The Orchestrator reads these cross-references during weekly synthesis.

---

## Git Commit Rules

- Commit after every meaningful update to any agent file
- Commit message format:
  ```
  [agent] <segment>: <what changed>
  
  Examples:
  [agent] dram: add SK Hynix Q1 2026 HBM3E capacity update
  [agent] orchestrator: cross-segment synthesis May 2026
  [data] crawler: add KITA Korea trade data to Tier 3 sources
  ```
- Always `git push` after committing

---

## Open Questions

- [ ] Should company_intel files be cross-linked from section agents?
- [ ] Should outputs/ reports be auto-indexed anywhere for easy retrieval?
- [ ] Tagging format: inline in body vs frontmatter YAML?
