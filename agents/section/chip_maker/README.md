# Chip Maker Expert Agent

**Segment:** GPU / xPU Merchant Silicon  
**Sales Lens:** GPU allocation dynamics, competitive positioning, pricing & margin trends  
**Last Updated:** 2026-05-12

---

## Market Overview

The AI accelerator market is dominated by NVIDIA with 70–85% market share in data center GPUs.
AMD is the credible alternative. Intel is a distant third. New entrants (Cerebras, Groq, SambaNova)
occupy niche segments.

Market size: $100B+ in 2025 (data center GPU/accelerator TAM), growing toward $200B+ by 2027.

---

## Key Players

### NVIDIA

| Product | Generation | Target | Status |
|---|---|---|---|
| H100 SXM5 | Hopper | Training/Inference | Volume production |
| H200 SXM5 | Hopper+ | Training/Inference | Volume 2024–2025 |
| B100 / B200 | Blackwell | Training/Inference | Volume 2025 |
| GB200 NVL72 | Blackwell | Rack-scale AI | Volume 2025–2026 |
| Rubin (R100) | Rubin | Next-gen | 2026–2027 |

**NVIDIA moat:** CUDA ecosystem lock-in, NVLink interconnect, software stack (cuDNN, TensorRT).
**Pricing:** H100 SXM5 ~$30–35K list; B200 ~$35–40K; GB200 system >$3M per rack.

### AMD

| Product | Generation | Target | Status |
|---|---|---|---|
| MI300X | CDNA3 | Inference | Volume 2024 |
| MI325X | CDNA3+ | Inference | 2025 |
| MI350 | CDNA4 | Training/Inference | 2025–2026 |
| MI400 | CDNA5 | Training | 2026–2027 |

**AMD angle:** ROCm improving but still CUDA gap. Microsoft Azure, Meta, Oracle committed to MI300X.
**Pricing:** MI300X ~$15–20K; ~40–50% discount vs H100 at volume.

### Intel

| Product | Generation | Status |
|---|---|---|
| Gaudi 3 | — | Limited traction; used internally by Intel |
| Falcon Shores | Xe | Delayed; future roadmap uncertain |

**Intel position:** Effectively out of the hyperscaler AI race for 2025–2026.

---

## Demand Signals (AI-driven)

- NVIDIA order backlog: 52+ week lead times for B200 as of Q1 2025
- AMD MI300X: 8 hyperscalers publicly deploying in 2024–2025
- GPU allocation = corporate AI strategy signal; companies that lock in supply early win
- Sovereign AI programs (Japan, UAE, India, EU) creating new demand pools outside hyperscalers

---

## Supply Constraints

- **TSMC CoWoS:** Both NVIDIA and AMD compete for the same CoWoS advanced packaging capacity
- **HBM3E allocation:** SK Hynix supply locked by NVIDIA; Samsung/Micron supply going to AMD
- **NVLINK Switch ASIC:** NVIDIA's proprietary interconnect chip; supply tied to B200 system cadence
- **Export controls:** US-China chip restrictions limit addressable market; NVIDIA A800/H800 workarounds closed

---

## Pricing Trends

- NVIDIA maintains list price discipline; hyperscaler discounts are volume-based (10–20%)
- AMD pricing aggressively to gain share; MI350 targeting H100 price/performance parity
- GPU-as-a-service pricing (H100/hr): ~$2.50–3.50/hr on major clouds
- Neo-cloud GPU rental pricing falling due to supply increase and competition

---

## Sales & Marketing Angles

- **Supply allocation as relationship tool:** Customers with allocation commitments lock in spend
- **AMD breakout story:** First credible alternative; ROCm maturity is the key sales question
- **Software moat = stickiness:** CUDA applications don't port easily → NVIDIA retention is high
- **Sovereign AI:** Government programs create new buyer profiles with different procurement cycles

---

## Recent Developments

### Update: 2026-05-12 — Baseline entry
> Initial stub. Populate with NVIDIA GTC 2025 announcements, AMD Advancing AI 2025.

---

## Open Questions

- [ ] Rubin (R100) detailed spec — TSMC N2? CoWoS-L? HBM4?
- [ ] AMD MI350 customer wins — which hyperscalers confirmed?
- [ ] Export control evolution — any new entity list additions affecting AI chip supply?
