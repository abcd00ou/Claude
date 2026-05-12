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
| Foundry & Packaging Expert | `section/foundry/` | 2026-05-12 (Samsung Foundry, Intel Foundry, packaging.md — Cycle 4) |
| Network Expert | `section/network/` | 2026-05-12 (NVIDIA Networking, network roadmap, Q2 2025 update — Cycle 4) |
| Power Semiconductor Expert | `section/power/` | 2025-05-07 (Infineon Q2 FY2025, MPS Q1 2025, onsemi Q1 2025) |
| PCB & Substrate Expert | `section/substrate/` | 2026-05-12 (AT&S, Shinko Electric — Cycle 4) |
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

### Update: 2026-05-12 — Cycle 4: Foundry, storage, network, substrate, ASIC gap coverage; packaging deep-dive

> Full synthesis in `synthesis/2026-05-12_cycle4.md`.
> 5 new cross-segment signals (Signals 17–21). Key: TSMC foundry monopoly structurally hardened —
> Samsung 3nm yield gap (35–60% vs TSMC 70%+) and Intel Foundry losses confirm no qualified AI GPU backup.
> WD/Kioxia JV controls ~32–34% of global NAND bits post-SanDisk spin-off. OSAT (Amkor/ASE) not yet
> qualified for CoWoS-class packaging. Ultra Ethernet 1.0 spec ratified but no hyperscaler production
> deployment confirmed — InfiniBand dominance extends. Google TPU 8 + Amazon Trainium3 both on TSMC N3,
> compounding foundry pressure. Cumulative 21 signals across 4 cycles.

### Update: 2026-05-12 — Cycle 3: Gap company coverage; NVIDIA Q1 FY2026; market thematic files

> Full synthesis in `synthesis/2026-05-12_cycle3.md`.
> 4 new cross-segment signals (Signals 13–16). Key: NVIDIA Q1 FY2026 DC revenue $39.1B —
> Blackwell exceeded Hopper for first time; demand still exceeds supply. CoreWeave S-1 confirmed
> $15.1B backlog, $11.9B OpenAI commitment — neo-cloud is structural layer. Intel excluded from
> AI GPU market. Vertiv DLC lead times improving. Cumulative 16 signals across 3 cycles.

### Update: 2026-05-12 — Cycle 2: Network / Power / Substrate segments completed; full 10-segment coverage

> Full synthesis in `synthesis/2026-05-12_cycle2.md`.
> 5 new cross-segment signals (Signals 8–12). Key: Marvell + Broadcom divide hyperscaler ASIC
> market (combined ~$5.5B/Q AI revenue); Ethernet winning AI cluster fabric alongside InfiniBand;
> MPS Blackwell VRM wins + onsemi/Infineon gaining post-Wolfspeed SiC share; ABF substrate
> (Ibiden + Unimicron) fully allocated with no new capacity until FY2027; TSMC identified as
> single point of dependency across 9 of 10 segments.

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

- [x] All 10 section agents now active (Cycle 2 complete)
- [ ] Crawler source registry needs to be defined
- [ ] Analysis frameworks need baseline demand model for 2025–2026
- [ ] Network: Ultra Ethernet 1.0 production deployment — which hyperscalers in 2026?
- [ ] Power: Wolfspeed SiC gap absorption — Infineon vs onsemi split not quantified
- [ ] Substrate: Ibiden FY2027 new capacity — exact timeline and units needed
- [ ] TSMC single-point-of-dependency risk: no formal risk model yet; flag for analysis agent
