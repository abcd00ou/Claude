## gstack (REQUIRED — global install)

**Before doing ANY work, verify gstack is installed:**

```bash
test -d ~/.claude/skills/gstack/bin && echo "GSTACK_OK" || echo "GSTACK_MISSING"
```

If GSTACK_MISSING: STOP. Do not proceed. Tell the user:

> gstack is required for all AI-assisted work in this repo.
> Install it:
> ```bash
> git clone --depth 1 https://github.com/garrytan/gstack.git ~/.claude/skills/gstack
> cd ~/.claude/skills/gstack && ./setup --team
> ```
> Then restart your AI coding tool.

Do not skip skills, ignore gstack errors, or work around missing gstack.

Using gstack skills: After install, skills like /qa, /ship, /review, /investigate,
and /browse are available. Use /browse for all web browsing.
Use ~/.claude/skills/gstack/... for gstack file paths (the global path).

---

## Project Mission

**AI Supply Chain Intelligence — Semiconductor Marketing & Sales Focus**

This project builds a structured knowledge base and multi-agent intelligence system
to monitor, analyze, and synthesize the AI semiconductor supply chain from a
**marketing and sales perspective**.

No production code. All knowledge is organized as Markdown (`.md`) files.

Outputs: market intelligence reports, segment deep-dives, demand signals, competitive
landscape snapshots — all written and updated as structured MD documents.

---

## Agent Architecture

### Orchestrator Agent

**Role:** `ORCHESTRATOR.md`  
Coordinates all section expert agents and data expert agents. Responsibilities:

- Collect updates from each section expert agent
- Trigger data refresh (crawler → DBA → analysis pipeline in knowledge form)
- Synthesize cross-segment signals (e.g., DRAM tightness affecting DC build-out)
- Produce consolidated market intelligence summaries
- Route incoming questions or research requests to the correct expert agent

**Trigger:** Any cross-segment question, weekly refresh, or top-level synthesis request.

---

### Section Expert Agents

Each section agent owns a domain. It maintains a structured MD knowledge base covering:
supply/demand balance, key players, pricing trends, technology roadmap, and sales signals.

| Agent | File | Coverage |
|---|---|---|
| DRAM Expert | `agents/section/dram.md` | HBM, DDR5, LPDDR5X — memory for AI training/inference |
| NAND / Storage Expert | `agents/section/storage.md` | QLC NAND, enterprise SSD, AI storage tiers |
| DC Infrastructure Expert | `agents/section/dc_infra.md` | Power, cooling, rack density, hyperscaler capex |
| ASIC Expert | `agents/section/asic.md` | Custom AI accelerators (TPU, Trainium, Inferentia, Marvell, etc.) |
| Chip Maker Expert | `agents/section/chip_maker.md` | NVIDIA, AMD, Intel — GPU/xPU supply chain |
| Foundry & Packaging Expert | `agents/section/foundry.md` | TSMC, Samsung, CoWoS, SoIC, advanced packaging |
| Network Expert | `agents/section/network.md` | InfiniBand, Ethernet, Spectrum-X, AI cluster interconnects |
| Power Semiconductor Expert | `agents/section/power.md` | VRM, GaN, SiC — AI data center power chain |
| PCB & Substrate Expert | `agents/section/substrate.md` | ABF substrates, HDI PCB, supply constraints |
| End Market Expert | `agents/section/end_market.md` | Hyperscalers (AWS, Azure, GCP, Meta), CSP AI capex trends |

**Each section MD file structure:**
```
# [Segment] Expert Agent

## Market Overview
## Key Players & Market Share
## Demand Signals (AI-driven)
## Supply Constraints
## Pricing Trends
## Technology Roadmap
## Sales & Marketing Angles
## Recent Developments (dated entries)
## Open Questions
```

---

### Data Expert Agents

| Agent | File | Role |
|---|---|---|
| Crawler Agent | `agents/data/crawler.md` | Defines what sources to monitor, crawl cadence, and signal extraction rules |
| Analysis Agent | `agents/data/analysis.md` | Frameworks for interpreting raw data — demand models, gap analysis, trend detection |
| DBA Agent | `agents/data/dba.md` | Knowledge schema design — how data is structured, tagged, versioned across MD files |

**Crawler Agent** (`agents/data/crawler.md`):
- Source registry: earnings calls, SEC filings, analyst reports, trade press, job postings
- Signal taxonomy: capex guidance, lead time changes, ASP movement, headcount signals
- Update frequency guidelines per source type

**Analysis Agent** (`agents/data/analysis.md`):
- Demand modeling frameworks (bottom-up from hyperscaler capex, top-down from TAM)
- Supply gap estimation methodology
- Competitive positioning analysis templates
- Sales cycle signal detection (design wins, RFQs, qualification timelines)

**DBA Agent** (`agents/data/dba.md`):
- MD file naming conventions and folder structure
- Tagging schema: `#segment`, `#company`, `#date`, `#signal-type`
- Version control discipline: how to date-stamp updates within MD files
- Cross-reference patterns between section agents

---

## Knowledge Base Structure

Each agent is a **folder**, not a single file. `README.md` is the agent's main document.
Subfolders hold organized supporting knowledge.

```
Claude/
├── CLAUDE.md                            ← This file (project instructions + architecture)
├── agents/
│   ├── orchestrator/
│   │   ├── README.md                    ← Orchestrator: routing logic + cross-segment synthesis
│   │   └── synthesis/                   ← Weekly/monthly synthesis reports (YYYY-MM-DD.md)
│   │
│   ├── section/                         ← One folder per semiconductor segment
│   │   ├── dram/
│   │   │   ├── README.md                ← Main agent (market overview, signals, roadmap)
│   │   │   ├── companies/               ← Per-company deep dives (sk_hynix.md, samsung.md, micron.md)
│   │   │   ├── market/                  ← Pricing trends, supply/demand data (pricing.md, roadmap.md)
│   │   │   └── updates/                 ← Dated update logs (2026-Q2.md, 2026-05.md)
│   │   ├── storage/         (same structure)
│   │   ├── dc_infra/        (same structure)
│   │   ├── asic/            (same structure)
│   │   ├── chip_maker/      (same structure)
│   │   ├── foundry/         (same structure)
│   │   ├── network/         (same structure)
│   │   ├── power/           (same structure)
│   │   ├── substrate/       (same structure)
│   │   └── end_market/      (same structure)
│   │
│   └── data/                            ← Data pipeline expert agents
│       ├── crawler/
│       │   ├── README.md                ← Source registry, crawl cadence, signal taxonomy
│       │   ├── sources/                 ← Per-source detail files (nvidia_ir.md, tsmc_ir.md)
│       │   └── signals/                 ← Extracted signal logs (YYYY-MM-DD.md)
│       ├── analysis/
│       │   ├── README.md                ← Analysis frameworks and methodology
│       │   ├── models/                  ← Demand model snapshots (hbm_demand_2026.md)
│       │   └── reports/                 ← Completed analysis reports
│       └── dba/
│           ├── README.md                ← Schema design, tagging rules, versioning
│           └── schema/                  ← Detailed schema definitions per domain
│
├── company_intel/                       ← Per-company deep dives (existing)
├── AI_SCM/                              ← Supply chain timeline & gap analysis (existing)
├── dashboard/                           ← HTML dashboard (existing)
└── marketing/                           ← Marketing & sales output layer
```

### Subfolder Usage Rules

| Subfolder | What goes in it |
|---|---|
| `companies/` | One `.md` per key player in the segment (company name in snake_case) |
| `market/` | Thematic files: `pricing.md`, `roadmap.md`, `supply_demand.md` |
| `updates/` | Dated update logs: `YYYY-MM.md` or `YYYY-QN.md` per period |
| `synthesis/` | (Orchestrator only) Cross-segment reports by date |
| `sources/` | (Crawler only) Per-source monitoring notes |
| `signals/` | (Crawler only) Raw extracted signals by date |
| `models/` | (Analysis only) Demand model snapshots with assumptions |
| `reports/` | (Analysis only) Completed analytical reports |
| `schema/` | (DBA only) Detailed schema for specific domains |

---

## Knowledge Principles

These four rules govern every piece of knowledge added to this system.
They are non-negotiable and apply to all agents.

### 1. Reliable Sources Only

Only accept knowledge from:
- Academic: peer-reviewed journals, conference papers (IEEE, ACM, Nature, Science), theses, dissertations
- Official: company IR pages, SEC/regulatory filings (10-K, 20-F, 8-K), press releases, official roadmaps
- Financial: earnings call transcripts, annual reports, analyst research (Goldman, Morgan Stanley, BofA, TF International Securities)
- Industry: SEMI, JEDEC, IEEE standards bodies, trade associations
- Research: IDC, Gartner, TechInsights, Yole Développement, Omdia (cite specific report title + date)

**Not accepted:** blog posts without primary source citation, unverified social media, anonymous forums, undated content.

Every knowledge entry must cite its source:
```
**Source:** [Title], [Publisher/Author], [Date], [URL or report name]
```

### 2. Organize by Timeline and Importance

- All entries carry a date: `YYYY-MM-DD` or `YYYY-QN` or `YYYY` minimum
- Within any file, entries are ordered **newest first** (reverse chronological)
- Each entry carries an importance tag: `#importance:high | medium | low`
  - `high` = affects supply/demand balance, pricing, or strategic direction
  - `medium` = useful context, corroborating data, secondary signals
  - `low` = background reference, historical baseline

### 3. Cross-Segment Routing

When knowledge better belongs to another section:
- **Toss to existing section:** add a `→ Toss: section/X/` note and place the file or entry there
- **Toss to multiple sections:** duplicate the entry in each relevant section, tag with `#cross-ref`
- **Likely new section:** flag in `agents/orchestrator/README.md` under "New Section Proposals" — do not create the folder until the Orchestrator confirms it warrants a dedicated agent

### 4. Facts Only — No Derived Insights

- Record what sources state directly. Do not add interpretation, inference, or conclusions.
- If a source *implies* something, quote the implication verbatim and tag `#confidence:low`
- Analysis and modeling belong only in `agents/data/analysis/` — never in section agent files
- Acceptable: "SK Hynix guided HBM3E capacity to grow 60% YoY in 2025 (SK Hynix Q4 2024 earnings)"
- Not acceptable: "This suggests HBM supply will be sufficient in 2025"

---

## Work Rules

- **No Python code.** All knowledge, frameworks, and agent logic lives in `.md` files.
- **Always date-stamp entries** inside MD files using `YYYY-MM-DD`.
- **After every completed task: `git commit` and `git push`.**
- Section expert agents write within their own folder; the orchestrator synthesizes across them.
- When a new signal is added, update the relevant section agent first, then flag cross-refs in `orchestrator/README.md`.

---

## Skill Routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action.

Key routing rules:
- Product ideas, "is this worth building", brainstorming → invoke office-hours
- Bugs, errors, "why is this broken", 500 errors → invoke investigate
- Ship, deploy, push, create PR → invoke ship
- QA, test the site, find bugs → invoke qa
- Code review, check my diff → invoke review
- Update docs after shipping → invoke document-release
- Weekly retro → invoke retro
- Design system, brand → invoke design-consultation
- Visual audit, design polish → invoke design-review
- Architecture review → invoke plan-eng-review
- Save progress, checkpoint, resume → invoke checkpoint
- Code quality, health check → invoke health
- Supply chain research, segment analysis → update the relevant section agent MD file
- Cross-segment synthesis → update ORCHESTRATOR.md
