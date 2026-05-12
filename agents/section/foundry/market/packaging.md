# Advanced Packaging — AI Foundry Market

**Last Updated:** 2026-05-12 (Cycle 4)  
**Coverage:** CoWoS, SoIC, OSAT chiplet packaging, HBM integration, industry capacity constraints

---

## Overview

Advanced packaging has become a primary competitive and supply chain battleground for AI semiconductors. The shift from monolithic dies to chiplet-based architectures (GPU + HBM + I/O dies in a single package) requires wafer-level packaging techniques not available at standard OSAT (Outsourced Semiconductor Assembly and Test) facilities. TSMC's CoWoS (Chip on Wafer on Substrate) is the industry standard for AI GPU packaging and remains the tightest capacity constraint in the AI supply chain.

---

## CoWoS (Chip on Wafer on Substrate)

### Technology Description

CoWoS is TSMC's proprietary advanced packaging technology that integrates multiple chiplets (GPU die, HBM stacks, I/O dies) on a silicon interposer or RDL (Redistribution Layer), then bonds the assembly to an organic substrate (ABF). It enables:
- Short HBM-to-GPU interconnect distances (<1mm) for maximum bandwidth
- 2.5D integration (side-by-side dies on interposer) — used in H100, H200, B200
- CoWoS-S: silicon interposer
- CoWoS-R: RDL-based; for larger packages (GB200)
- CoWoS-L: combined EMIB-like approach; next-gen

**Source:** TSMC Technology Symposium 2023; TSMC Q1 2026 Earnings, 2026-04-17

### Capacity Status

| Period | Status | Detail | Source |
|---|---|---|---|
| CY2024 | Demand > capacity by 20–30% | Primary binding constraint for AI GPU shipments | NVIDIA 10-K FY2025, 2025-02-26 |
| CY2025 | Demand still exceeds capacity | No relief until new capex lands | TSMC Q1 2026 Earnings, 2026-04-17 |
| CY2026 | Expanding but still tight | TSMC $52–56B capex; CoWoS portion ~$5–8B (est.) | Industry estimates, 2026 |

**Source:** TSMC Q1 2026 Earnings, 2026-04-17; NVIDIA 10-K FY2025, 2025-02-26

#segment:foundry #source-tier:A #signal-type:supply #date:2026-04-17 #importance:high #confidence:high

---

## SoIC (System on Integrated Chips)

TSMC's 3D stacking technology, bonding chiplets face-to-face or face-to-back using hybrid bonding (no solder bumps). Achieves much finer pitch than CoWoS.

| Variant | Description | AI Application | Status |
|---|---|---|---|
| SoIC-X (face-to-face) | Highest density; 9µm pitch | SRAM + compute die stacking | Production (limited) |
| SoIC-P (face-to-back) | Standard; 36µm pitch | HBM die stacking, logic stacking | Ramping |

**Relevance to AI:** SoIC enables future HBM-on-logic integration where HBM memory is directly bonded on top of the GPU die (not side-by-side), eliminating the interposer. This is a roadmap item for post-2026 AI chips.

**Source:** TSMC Technology Symposium 2024; IEEE ECTC 2024 papers

---

## HBM Integration (CoW — Chip on Wafer)

HBM stacks are integrated by memory makers (SK Hynix, Samsung, Micron) using their own CoW (Chip on Wafer) process before delivery to TSMC for CoWoS integration:

1. Memory maker bonds HBM DRAM dies into a stack (using TC-Bonding or thermocompression)
2. Stack is bonded to a base die (logic die or interposer base) at the memory maker
3. HBM + base die assembly is shipped to TSMC
4. TSMC integrates HBM + GPU die on CoWoS interposer

**Source:** SK Hynix HBM Technical Brief, 2024; TSMC Technology Symposium 2023

---

## OSAT Packaging (ASE Group, Amkor)

OSATs (Outsourced Semiconductor Assembly and Test) perform backend packaging for standard semiconductor products. For AI chips, OSATs have limited CoWoS-equivalent capability but are increasingly involved in:

| OSAT | Role in AI | Technology | Status |
|---|---|---|---|
| ASE Group | SiP (System in Package), fan-out | FOWLP; traditional BGA | No CoWoS equivalent; involved in networking ASICs |
| Amkor Technology | SiP + advanced packaging | SLIM (Substrate-Like PCB Interposer); CoWoS-like R&D | Not yet in AI GPU supply chain volume |

**Key signal:** TSMC is exploring Amkor as a CoWoS overflow partner as demand far exceeds TSMC in-house capacity. No volume production confirmed as of Q1 2025.

**Source:** Industry reports, Q1 2025; Amkor investor presentations, 2024

#segment:foundry #source-tier:B #signal-type:supply #date:2025 #importance:high #confidence:medium #cross-ref

---

## Advanced Packaging Lead Times and Constraints

| Process | Lead Time | Constraint Level | Notes |
|---|---|---|---|
| CoWoS (TSMC) | Allocated; demand > capacity 20–30% | Critical | All CY2026 slots committed |
| SoIC (TSMC) | Demand > capacity | High | Limited to advanced customers (Apple, NVIDIA) |
| FOWLP (OSAT) | 8–12 weeks | Normal | Not applicable to AI GPU class |
| HBM CoW integration (at memory maker) | Included in HBM lead time | Tied to HBM | 4–6 quarter allocation window |

**Source:** TSMC Q1 2026 Earnings, 2026-04-17; Supply chain analysis, Q1 2025

---

## Competitor Packaging Strategies

| Company | Packaging Technology | AI Product | Fabbed At |
|---|---|---|---|
| TSMC | CoWoS-S / CoWoS-R / CoWoS-L | NVIDIA H100/H200/B200; AMD MI300X; Google TPU | TSMC in-house |
| Samsung Foundry | I-Cube (2.5D) / X-Cube (3D) | Limited AI customers; SF3E base | Samsung in-house |
| Intel | EMIB + Foveros | Ponte Vecchio (legacy); Gaudi (internal) | Intel in-house |
| ASE Group | FOWLP / SiP | Networking ASICs (non-GPU) | OSAT |

**Source:** Company disclosures 2024–2025; TechInsights packaging analysis, 2024

---

## Open Questions

- [ ] Will TSMC qualify Amkor for CoWoS overflow production, and at what volume?
- [ ] CoWoS-L (for Vera Rubin / GB300 class) — what is the capacity plan and timeline?
- [ ] Can SoIC achieve yields suitable for AI GPU class volumes by 2026?
- [ ] Samsung I-Cube: has any AI GPU customer qualified Samsung 2.5D packaging?
- [ ] OSAT entry into AI-class packaging: what is the technology gap vs TSMC CoWoS?
