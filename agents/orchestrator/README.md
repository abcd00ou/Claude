# Orchestrator Agent

**Role:** Cross-segment synthesis and agent coordination  
**Last Updated:** 2026-05-12

---

## Purpose

The Orchestrator sits above all section expert agents and data expert agents.
It does not own segment knowledge — it routes, synthesizes, and surfaces
cross-cutting signals that no single section agent can see alone.

---

## Agent Registry

| Agent | Folder | Last Refresh |
|---|---|---|
| DRAM Expert | `section/dram/` | 2026-04-30 (Samsung Q1 2026) |
| Storage Expert | `section/storage/` | 2026-04-30 (Samsung Q1 2026) |
| DC Infrastructure Expert | `section/dc_infra/` | 2026-04-29 (Hyperscaler Q1 2026) |
| ASIC Expert | `section/asic/` | 2026-04-29 (Hyperscaler Q1 2026) |
| Chip Maker Expert | `section/chip_maker/` | 2026-05-05 (AMD Q1 2026) |
| Foundry & Packaging Expert | `section/foundry/` | 2026-04-16 (TSMC Q1 2026) |
| Network Expert | `section/network/` | — |
| Power Semiconductor Expert | `section/power/` | — |
| PCB & Substrate Expert | `section/substrate/` | — |
| End Market Expert | `section/end_market/` | 2026-04-29 (Hyperscaler Q1 2026) |
| Crawler Agent | `data/crawler/` | — |
| Analysis Agent | `data/analysis.md` | — |
| DBA Agent | `data/dba.md` | — |

---

## Routing Logic

### Incoming question → Agent mapping

| Topic | Route to |
|---|---|
| HBM supply, DDR5 pricing, memory lead times | `dram.md` |
| Enterprise SSD, NAND pricing, storage attach rates | `storage.md` |
| Hyperscaler capex, power/cooling, rack density | `dc_infra.md` |
| Custom silicon, TPU, Trainium, Marvell OCTEON | `asic.md` |
| NVIDIA GPU allocation, AMD MI series, Intel Gaudi | `chip_maker.md` |
| TSMC CoWoS capacity, advanced packaging, foundry | `foundry.md` |
| InfiniBand, Spectrum-X, AI cluster networking | `network.md` |
| VRM, GaN, SiC, data center power | `power.md` |
| ABF substrate, PCB supply | `substrate.md` |
| AWS/Azure/GCP/Meta AI investment, CSP capex | `end_market.md` |
| What sources to watch, crawl frequency | `data/crawler.md` |
| Demand models, gap analysis, trend method | `data/analysis.md` |
| File structure, tagging, versioning | `data/dba.md` |

### Cross-segment synthesis triggers

- DRAM tightness + DC infra demand spike → memory supply gap risk for hyperscalers
- CoWoS bottleneck + ASIC demand → custom silicon shipment delays
- Power semiconductor shortage + DC infra capex → data center build-out delay risk
- End market capex guidance change → update demand models in `analysis.md`

---

## Weekly Refresh Workflow

1. Crawler Agent: identify new signals from registered sources
2. Each section agent: ingest signals, update "Recent Developments"
3. Analysis Agent: re-run gap models with updated data
4. Orchestrator: write cross-segment synthesis below

---

## Cross-Segment Synthesis

### Update: 2026-05-12 — Cycle 1: Q1 2026 earnings

> Full synthesis in `synthesis/2026-05-12.md`.
> 7 cross-segment signals identified. Key: all CY2026 HBM supply committed across 3 suppliers;
> component pricing inflating hyperscaler capex ($25B+ confirmed); combined 4-hyperscaler
> 2026 capex ~$705–725B; Samsung warns 2027 shortage "more severe than 2026";
> AMD 6 GW commitments from Meta + OpenAI; MTIA Gen 2 (2nm/Broadcom) in production.

---

## New Section Proposals

If incoming knowledge does not fit any existing section, propose a new agent here.
Do not create the folder until it has been confirmed as a recurring, substantial domain.

| Proposed Segment | Reason | Date Proposed | Status |
|---|---|---|---|
| — | — | — | — |

---

## Open Flags

- [ ] All section agents need initial population
- [ ] Crawler source registry needs to be defined
- [ ] Analysis frameworks need baseline demand model for 2025–2026
