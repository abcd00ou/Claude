# Orchestrator Agent

**Role:** Cross-segment synthesis and agent coordination  
**Last Updated:** 2026-05-13

---

## Purpose

The Orchestrator sits above all section expert agents and data expert agents.
It does not own segment knowledge — it routes, synthesizes, and surfaces
cross-cutting signals that no single section agent can see alone.

---

## Agent Registry

| Agent | Folder | Last Refresh |
|---|---|---|
| DRAM Expert | `section/dram/` | 2026-05-13 (Samsung Q1 2026 memory / HBM4 base-die — Cycle 6) |
| Storage Expert | `section/storage/` | 2026-04-30 (Samsung Q1 2026) |
| DC Infrastructure Expert | `section/dc_infra/` | 2026-05-13 (Microsoft Q3 FY2026 capex — Cycle 6) |
| ASIC Expert | `section/asic/` | 2026-05-13 (Trainium3 + Ironwood GA — Cycle 6) |
| Chip Maker Expert | `section/chip_maker/` | 2026-05-13 (NVIDIA Rubin production — Cycle 6) |
| Foundry & Packaging Expert | `section/foundry/` | 2026-05-13 (Samsung 2nm / Amkor Arizona — Cycle 6) |
| Network Expert | `section/network/` | 2026-05-13 (NVLink Fusion + UEC 1.0 — Cycle 6) |
| Power Semiconductor Expert | `section/power/` | 2026-05-13 (DOE/NREL/WoodMac transformer constraints — Cycle 6) |
| PCB & Substrate Expert | `section/substrate/` | 2026-05-13 (Amkor Arizona packaging campus — Cycle 6) |
| End Market Expert | `section/end_market/` | 2026-05-13 (Microsoft/Meta/Amazon AI capex — Cycle 6) |
| Crawler Agent | `data/crawler/` | 2026-05-13 (Cycle 6 extracted signals) |
| Analysis Agent | `data/analysis/` | 2026-05-13 (Cycle 6 analysis report) |
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
| What sources to watch, crawl frequency | `data/crawler/` |
| Demand models, gap analysis, trend method | `data/analysis/` |
| File structure, tagging, versioning | `data/dba/` |

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


### Update: 2026-05-13 — Cycle 6: Rubin deployment, NVLink Fusion, custom inference silicon, grid bottlenecks

> Full synthesis in `synthesis/2026-05-13_cycle6.md`.
> 6 new cross-segment signals (Signals 27–32). Key: Rubin is now a 2026 deployment event;
> NVLink Fusion turns custom ASICs into NVIDIA-compatible infrastructure; Trainium3 and
> Ironwood confirm inference-specific custom silicon is production grade; grid equipment remains
> the physical critical path; U.S. advanced packaging capacity is coming but not early enough to
> relieve 2026 CoWoS-class pressure. Cumulative 32 signals across 6 cycles.

### Update: 2026-05-12 — Cycle 5: Full-section update logs; Rubin, HBM, transformer, ASIC refresh

> Full synthesis in `synthesis/2026-05-12_cycle5.md`.
> 5 new cross-segment signals (Signals 22–26). Key: Samsung HBM share collapsed to 17%;
> Vera Rubin HBM4 load expands HBM TAM; Samsung SF2P 2nm yield became a credible second-source
> watch item; power transformer lead times reached critical-path status; Google Ironwood and
> Amazon Trainium3 confirmed the production custom-ASIC wave. Cumulative 26 signals across 5 cycles.

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

- [x] All 10 section agents active (Cycle 2 complete)
- [x] Crawler signal log created for Cycle 6: `data/crawler/signals/2026-05-13.md`
- [x] Analysis report created for Cycle 6: `data/analysis/reports/2026-05-13_cycle6_analysis.md`
- [ ] Samsung NVIDIA HBM3E / HBM4 qualification status — official confirmation still needed.
- [ ] Vera Rubin NVL72 exact volume ramp by cloud provider and quarter in H2 2026.
- [ ] AWS Trainium4 + NVLink Fusion technical disclosure and production timing.
- [ ] Google Ironwood process node and external supply-chain partners remain undisclosed in official Google materials.
- [ ] UEC 1.0 first named hyperscaler production deployment.
- [ ] Power transformer manufacturing capacity response: vendors, qualified shipment timing, and policy support.
- [ ] Amkor Arizona exact packaging technology mix and CoWoS-class qualification evidence.
- [ ] Wolfspeed post-restructuring SiC customer retention and share split versus Infineon/onsemi.
