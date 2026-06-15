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

The section taxonomy follows `agents/data/dba/company_universe.csv` (18 sections,
136 tracked public companies — source: company_master.xlsx). The same section
slugs are the canonical `#segment` tag values and the `financials.db` segment keys.

| Agent (slug) | Folder | Coverage |
|---|---|---|
| AI Chip (`ai_chip`) | `agents/section/ai_chip/` | NVIDIA, AMD, Qualcomm, Marvell, Alchip — GPU/xPU accelerators (incl. former chip_maker + asic) |
| AI Platforms (`ai_platforms`) | `agents/section/ai_platforms/` | Palantir, Salesforce, ServiceNow, Snowflake, Datadog — enterprise AI software |
| AI Software (`ai_software`) | `agents/section/ai_software/` | Meta, Baidu — AI model/app builders |
| Components (`components`) | `agents/section/components/` | ABF substrate, PCB, passives, VRM/power semis, MPS, Analog Devices (incl. former substrate + power) |
| Cooling (`cooling`) | `agents/section/cooling/` | Vertiv DLC, Alfa Laval, Trane, Carrier, Modine — thermal management |
| CPU (`cpu`) | `agents/section/cpu/` | ARM, Intel — host CPUs & IP cores |
| DRAM (`dram`) | `agents/section/dram/` | HBM, DDR5, LPDDR5X — Samsung, SK hynix, Micron |
| Energy (`energy`) | `agents/section/energy/` | Power & grid: Vertiv, Eaton, Schneider, GE Vernova, NextEra, Constellation (incl. former dc_infra) |
| Foundry (`foundry`) | `agents/section/foundry/` | TSMC, SMIC — leading-edge fabrication |
| HW Equipment (`hw_equipment`) | `agents/section/hw_equipment/` | ASML, AMAT, Lam, KLA, TEL, Advantest — fab equipment |
| Hyperscalers (`hyperscalers`) | `agents/section/hyperscalers/` | Google, Microsoft, Amazon, Oracle, Alibaba, Tencent — CSP capex & custom silicon |
| Materials (`materials`) | `agents/section/materials/` | Linde, Air Liquide, Shin-Etsu, Entegris, Corning — gases, wafers, chemicals |
| NAND (`nand`) | `agents/section/nand/` | Kioxia, Seagate, WD — NAND & enterprise SSD (former storage) |
| Neocloud (`neocloud`) | `agents/section/neocloud/` | CoreWeave, Nebius, IREN — GPU-cloud specialists |
| OSAT / Packaging (`osat_packaging`) | `agents/section/osat_packaging/` | ASE, Amkor, JCET, Tongfu — assembly & advanced packaging |
| Server Networking (`server_networking`) | `agents/section/server_networking/` | Broadcom, Arista, Astera, Coherent, Lumentum, Fabrinet — switch ASIC + optics (incl. former network + photonics) |
| Server OEM/EMS/ODM (`server_oem_ems_odm`) | `agents/section/server_oem_ems_odm/` | Foxconn, Dell, HPE, SMCI, Quanta, Wiwynn, Celestica — AI server/rack builders |
| SW Equipment (`sw_equipment`) | `agents/section/sw_equipment/` | Synopsys — EDA & design software |

**Reconciliation note (2026-06-15):** the prior 12-folder taxonomy was reconciled
to these 18 sections. Renamed: storage→nand, chip_maker→ai_chip, network→server_networking,
end_market→hyperscalers, dc_infra→energy, equipment→hw_equipment, substrate→components.
Merged: photonics→server_networking, asic→ai_chip, power→components (the merged
folder's original README is kept as `_merged_<name>_README.md` in the target).

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
│   ├── section/                         ← One folder per AI-SCM section (18 total)
│   │   ├── dram/
│   │   │   ├── README.md                ← Main agent (market overview, signals, roadmap)
│   │   │   ├── companies/               ← Per-company deep dives (sk_hynix.md, samsung.md, micron.md)
│   │   │   ├── market/                  ← Pricing trends, supply/demand data (pricing.md, roadmap.md)
│   │   │   └── updates/                 ← Dated update logs (2026-Q2.md, 2026-05.md)
│   │   ├── nand/                  (same structure)
│   │   ├── foundry/               (same structure)
│   │   ├── ai_chip/               (same structure)
│   │   ├── cpu/                   (same structure)
│   │   ├── hyperscalers/          (same structure)
│   │   ├── neocloud/              (same structure)
│   │   ├── ai_platforms/          (same structure)
│   │   ├── ai_software/           (same structure)
│   │   ├── server_networking/     (same structure)
│   │   ├── server_oem_ems_odm/    (same structure)
│   │   ├── components/            (same structure)
│   │   ├── osat_packaging/        (same structure)
│   │   ├── hw_equipment/          (same structure)
│   │   ├── sw_equipment/          (same structure)
│   │   ├── materials/             (same structure)
│   │   ├── energy/                (same structure)
│   │   └── cooling/               (same structure)
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

### 5. Academic Architecture Standard — Bible Papers Rule

Each section agent MUST maintain a `market/architecture.md` (or `market/technology.md` for foundry)
file that is grounded exclusively in **verified foundational academic sources**.

**Requirements:**
- Minimum **5 "bible" papers** per section — foundational, highly-cited, peer-reviewed works that
  define the technical standard for that domain
- Each paper must be **verified**: author, title, venue, year, and DOI or publisher URL confirmed
  via web search before being cited
- Content entries must be **derived from what the paper explicitly states** — do not paraphrase
  from training memory; fetch the abstract or key sections first
- No fabricated citations — every `**Source:**` line must correspond to a retrieved document

**Bible paper criteria (all must apply):**
1. Peer-reviewed: IEEE, ACM, Nature, Science, or equivalent standards body (JEDEC, IPC, SEMI)
2. Foundational: defines or first describes a core concept for the domain (invention paper,
   first deployment paper, or canonical architecture reference)
3. Highly cited: >100 citations OR is an industry-defining standard document
4. Verifiable: DOI or publisher URL exists and resolves

**Per-section canonical bible paper anchors (minimum, add more):**

| Section | Bible Papers (minimum 5) |
|---|---|
| DRAM | Dennard et al. (1974) IEEE JSSC — MOSFET scaling; Lee et al. (2014) ISSCC — first HBM; JEDEC JESD235C; Micron DDR5 tech note; Kim et al. (2014) ISCA — Rowhammer |
| Chip Maker | Williams et al. (2009) CACM — Roofline; Jouppi et al. (2017) ISCA — TPU; NVIDIA Hopper whitepaper; Hennessy & Patterson (2017) — Computer Architecture; Fowers et al. (2018) ISCA — Brainwave FPGA |
| Foundry | Hisamoto et al. (2000) IEEE TED — FinFET; Bohr (2007) IEEE IEDM — 32nm HKMG; TSMC N3 VLSI 2022; Mack (2011) — EUV lithography; Clark et al. (2016) ECTC — CoWoS |
| Storage | Masuoka et al. (1987) IEDM — NAND flash invention; Tanaka et al. (2007) VLSI — BiCS; NVMe Base Spec 1.4; Bez et al. (2003) Proc. IEEE — flash memory overview; Cai et al. (2017) SIGMETRICS — NAND reliability |
| Network | Al-Fares et al. (2008) SIGCOMM — fat-tree; Gibiansky (2017) — ring-allreduce; IBTA InfiniBand spec; Zhu et al. (2015) SIGCOMM — DCQCN; Dean et al. (2012) NIPS — DistBelief |
| ASIC | Kung & Leiserson (1978) — systolic array; Jouppi et al. (2017) ISCA — TPU; Chen et al. (2016) ISSCC — Eyeriss; Vaswani et al. (2017) NeurIPS — Attention; Dao et al. (2022) NeurIPS — FlashAttention |
| Power | Baliga (1989) IEEE EDL — power device FOM; Kimoto & Cooper (2014) Wiley — SiC Technology; Jones et al. (2016) Nat. Electron. — GaN on Si; Lidow et al. (2012) — GaN textbook; IEEE Std 1547 — DER interconnect |
| Substrate | IPC-2221B; Garrou et al. (2008) — Handbook of 3D IC; Tummala (2001) — Fundamentals of Microsystems Packaging; Lau (2011) — Reliability of RoHS-compliant 2D & 3D IC; SEMI G69 — substrate standard |
| DC Infra | ASHRAE TC 9.9 (2021) — Thermal Guidelines; Patterson (2008) CACM — energy-proportional computing; Barroso & Hölzle (2007) IEEE Micro — warehouse-scale computing; Koomey (2011) — data center energy use; Green Grid WP #49 — PUE |
| End Market | Vaswani et al. (2017) NeurIPS — Attention; Shoeybi et al. (2019) — Megatron-LM; Kwon et al. (2023) SOSP — PagedAttention; Rajbhandari et al. (2020) SC — ZeRO; Dean et al. (2012) NIPS — DistBelief |

**Workflow for updating architecture files:**
1. Web search each bible paper to confirm: exact title, authors, venue, year, DOI
2. Fetch abstract or key sections (methodology, results tables, key numbers)
3. Write knowledge entries using only what the fetched content states
4. Tag each entry: `#source-tier:S` (peer-reviewed) or `#source-tier:A` (official whitepaper/standard)

---

## Work Rules

- **No Python code.** All knowledge, frameworks, and agent logic lives in `.md` files.
- **Always date-stamp entries** inside MD files using `YYYY-MM-DD`.
- **After every completed task: `git commit` and `git push`.**
- Section expert agents write within their own folder; the orchestrator synthesizes across them.
- When a new signal is added, update the relevant section agent first, then flag cross-refs in `orchestrator/README.md`.

### New Company Rule

When new information about a company is found from a reliable source:

1. **Check if a company file exists** in the relevant section's `companies/` folder  
   e.g., `agents/section/dram/companies/sk_hynix.md`
2. **If the file exists** — append a dated entry under `## Updates` (newest first)
3. **If the file does not exist** — create it using the company file template in  
   `agents/data/dba/schema/company_template.md`
4. **If the company spans multiple segments** — create a file in each relevant segment's  
   `companies/` folder (e.g., Samsung appears in `dram/`, `nand/`, `foundry/`)
5. **Always also check** `company_intel/` at the project root — if a file exists there, add  
   the same update there too so both knowledge layers stay in sync

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
