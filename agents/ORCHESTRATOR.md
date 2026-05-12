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

| Agent | File | Last Refresh |
|---|---|---|
| DRAM Expert | `section/dram.md` | — |
| Storage Expert | `section/storage.md` | — |
| DC Infrastructure Expert | `section/dc_infra.md` | — |
| ASIC Expert | `section/asic.md` | — |
| Chip Maker Expert | `section/chip_maker.md` | — |
| Foundry & Packaging Expert | `section/foundry.md` | — |
| Network Expert | `section/network.md` | — |
| Power Semiconductor Expert | `section/power.md` | — |
| PCB & Substrate Expert | `section/substrate.md` | — |
| End Market Expert | `section/end_market.md` | — |
| Crawler Agent | `data/crawler.md` | — |
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

### Update: 2026-05-12 — Initial baseline

> Baseline entry. Section agents not yet populated.
> Synthesis will be added here as agents are built out.

---

## Open Flags

- [ ] All section agents need initial population
- [ ] Crawler source registry needs to be defined
- [ ] Analysis frameworks need baseline demand model for 2025–2026
