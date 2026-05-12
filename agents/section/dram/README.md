# DRAM Expert Agent

**Segment:** DRAM / Memory  
**Sales Lens:** AI training & inference memory demand, HBM allocation, DDR5 ramp  
**Last Updated:** 2026-05-12

---

## Market Overview

DRAM is the most supply-constrained memory type for AI workloads in 2025–2026.
HBM (High Bandwidth Memory) is a specialized DRAM variant stacked on AI accelerators.
Standard DDR5 and LPDDR5X serve edge AI, client AI (NPU), and general server memory.

**Key segments:**
- **HBM3 / HBM3E** — on-package memory for NVIDIA H/B series, AMD MI series, Google TPU
- **DDR5** — server DRAM for CPU-side AI inference, memory capacity scaling
- **LPDDR5X** — edge AI, on-device inference (smartphones, PCs with NPU)

---

## Key Players & Market Share

| Company | HBM Share | DDR5 Share | Notes |
|---|---|---|---|
| SK Hynix | ~50–55% | ~30% | Sole HBM3E supplier to NVIDIA (2024–2025) |
| Samsung | ~35–40% | ~40% | Ramping HBM3E; qualification delays vs Hynix |
| Micron | ~10–15% | ~25% | HBM3E shipping to NVIDIA; aggressive ramp plan |

---

## Demand Signals (AI-driven)

- NVIDIA GB200 NVL72 requires 8× HBM3E per GPU → 576 HBM stacks per rack
- Each HBM3E stack = 36 GB; total per rack = ~20.7 TB HBM
- Google TPUv5p clusters: 8× HBM2e per chip
- Meta, Microsoft, Amazon all designing custom ASICs with HBM
- Edge AI (Snapdragon X, Apple M-series) driving LPDDR5X upgrades per cycle

**Demand model trigger:** Any hyperscaler capex increase → proportional HBM demand increase.

---

## Supply Constraints

- **CoWoS packaging bottleneck at TSMC** limits HBM-on-GPU yield throughput
- SK Hynix HBM3E capacity: ~12–14 layers stacked; yield ramp takes 12–18 months
- Samsung HBM3E qualification with NVIDIA pushed repeatedly (as of early 2025)
- Micron HBM3E qualified at NVIDIA; scaling constrained by back-end capacity

**Lead times:** HBM allocation is locked 4–6 quarters in advance by hyperscalers.

---

## Pricing Trends

- HBM3E ASP: ~$15–18 per GB (vs DDR5 ~$3–4/GB) — ~5× premium
- DDR5 pricing recovering from 2023 downcycle; server DRAM mix improving
- Spot DRAM pricing volatile; contract pricing more stable for AI-directed supply

---

## Technology Roadmap

| Node | Availability | Notes |
|---|---|---|
| HBM3E | 2024–2026 | Current high-volume node |
| HBM4 | 2026+ | Logic die from TSMC; memory die from HBM vendors |
| HBM4E | 2027+ | Higher bandwidth, lower power per bit |
| DDR6 | 2026–2027 | JEDEC spec; AI server ramp expected 2027 |
| LPDDR6 | 2025–2026 | Edge AI devices, Snapdragon / Apple chips |

---

## Sales & Marketing Angles

- **Pitch for storage/memory teams:** HBM allocation = GPU allocation; win HBM design-in = win GPU program
- **DDR5 angle:** AI inference server deployments are doubling DIMM count per server
- **Upgrade cycle:** On-device AI (PC AI, mobile AI) is compressing DRAM upgrade cycles
- **Competitive differentiator:** SK Hynix HBM3E yield advantage is a 2-year window; positioning now matters

---

## Recent Developments

### Update: 2026-05-12 — Baseline entry
> Initial stub. Populate with Q1 2026 earnings call data from SK Hynix, Samsung, Micron.

---

## Open Questions

- [ ] Samsung HBM3E qualification status with NVIDIA (Q1 2026 earnings)?
- [ ] Micron HBM4 roadmap timeline confirmed?
- [ ] HBM supply allocation for custom ASICs (Google, AWS, Meta) — public data available?
