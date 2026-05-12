# ASIC Expert Agent

**Segment:** Custom AI Silicon / Application-Specific Integrated Circuits  
**Sales Lens:** In-house accelerator programs, merchant silicon displacement, design win timelines  
**Last Updated:** 2026-05-12

---

## Market Overview

Hyperscalers are building custom AI ASICs to reduce NVIDIA dependency, optimize for their
specific model architectures, and lower total cost of ownership (TCO).

Custom ASICs now represent 20–30% of AI accelerator deployments at leading hyperscalers,
growing toward 40–50% by 2027 as programs mature.

The ASIC market bifurcates:
1. **Hyperscaler in-house** (Google TPU, AWS Trainium, Meta MTIA, Microsoft Maia)
2. **ASIC design houses** (Marvell, Broadcom custom, Alchip, GUC)

---

## Key Players & Programs

| Company | ASIC | Generation | Foundry | Notes |
|---|---|---|---|---|
| Google | TPU v5p / v6 | 5th–6th gen | TSMC | Training + inference; largest custom fleet |
| Amazon AWS | Trainium2, Inferentia3 | 2nd–3rd gen | TSMC | Trainium2 in production 2024 |
| Meta | MTIA v2 | 2nd gen | TSMC | Inference-focused; training still NVIDIA |
| Microsoft | Maia 100 | 1st gen | TSMC N5 | Azure AI inference; Maia 2 in development |
| Apple | Neural Engine (ANE) | Gen 5 | TSMC | On-device; not data center |
| Marvell | Octeon / custom | — | TSMC | ASIC design partner for hyperscalers |
| Broadcom | XPU programs | — | TSMC | Google TPU collab; other hyperscaler NDA |

---

## Demand Signals (AI-driven)

- Google TPU fleet estimated at 2M+ chips (as of 2025); growing
- AWS Trainium2 cluster: 100K+ chip deployments at Amazon scale
- Meta MTIA v2: targeting 50%+ of inference workload in 2026
- ASIC programs require 3–5 year design-to-production cycles

**ASIC displacement signal:** Every dollar shifted from merchant GPU to custom ASIC
reduces NVIDIA TAM but grows foundry (TSMC) and packaging TAM.

---

## Supply Constraints

- **CoWoS packaging** at TSMC: most advanced ASICs require CoWoS; same bottleneck as GPU
- **N3/N2 node allocation:** TSMC N3 capacity split between Apple, NVIDIA, AMD, and custom ASIC
- **Design talent:** ASIC design teams are a 5–7 year build; not easily scaled
- **EDA tool licenses (Synopsys, Cadence):** Not a bottleneck but a cost center

---

## Technology Roadmap

| Node | Availability | ASIC Programs |
|---|---|---|
| TSMC N5 | Volume | Maia 100, TPUv5 variants |
| TSMC N3 | Ramping | TPUv6, Trainium2 |
| TSMC N2 | 2025–2026 | Next-gen hyperscaler ASICs |
| TSMC A16 (backside power) | 2026–2027 | Post-N2 for top programs |
| 3D IC / SoIC | Emerging | Multi-die ASIC integration |

---

## Sales & Marketing Angles

- **Merchant silicon risk:** NVIDIA pricing power is the primary driver of hyperscaler ASIC investment
- **ASIC ≠ GPU replacement (yet):** Custom silicon optimized for known workloads; NVIDIA still wins for flexibility
- **Marvell/Broadcom opportunity:** ASIC design services are growing; not just in-house
- **EDA and IP:** Arm, Synopsys, Cadence benefit regardless of who designs the ASIC

---

## Recent Developments

### Update: 2026-05-12 — Baseline entry
> Initial stub. Populate with Google Next 2025 TPU announcements, AWS re:Invent Trainium3 preview.

---

## Open Questions

- [ ] Trainium3 timeline and spec — any public data from AWS?
- [ ] Broadcom's unnamed hyperscaler ASIC programs — can we identify from job postings?
- [ ] Meta MTIA v2 inference deployment scale — any earnings call color?
