# Network Expert Agent

**Segment:** AI Networking / Interconnect  
**Sales Lens:** AI cluster fabric, high-speed interconnect, switch ASIC market  
**Last Updated:** 2026-05-12

---

## Market Overview

AI training clusters require ultra-low latency, high-bandwidth networking between
thousands of GPUs. This is fundamentally different from traditional data center networking.

Two competing paradigms:
1. **InfiniBand** (NVIDIA Quantum / NDR) — dominant in AI training
2. **Ethernet** (Ultra Ethernet Consortium / Spectrum-X) — challenging for AI workloads

Networking is 10–15% of total AI cluster cost; becoming a strategic differentiator.

---

## Key Players

| Company | Product | Technology | Market Position |
|---|---|---|---|
| NVIDIA (Mellanox) | Quantum-2 / NDR InfiniBand | InfiniBand | Dominant in large AI training |
| NVIDIA (Spectrum-X) | Spectrum-X800 | Ethernet | NVIDIA's Ethernet push for AI |
| Broadcom | Tomahawk 5, Jericho3 | Ethernet | Hyperscaler Ethernet switches |
| Arista Networks | 7800R4 series | Ethernet | Hyperscaler AI fabric |
| Cisco | 8000 series | Ethernet | Enterprise AI networking |
| Marvell | OCTEON / Alaska | Ethernet | SmartNIC, DPU |
| AMD (Pensando) | DPU / SmartNIC | Ethernet | Cloud NIC acceleration |

---

## Demand Signals (AI-driven)

- NVIDIA GB200 NVL72 rack: requires 800G InfiniBand NDR per GPU node
- Meta's AI cluster: 24,576 GPUs connected via 400G InfiniBand (disclosed 2024)
- Microsoft Azure: deploying Spectrum-X for AI workloads (Ethernet path with NVIDIA)
- Ultra Ethernet Consortium: AMD, Intel, Broadcom, Google, Meta — Ethernet for AI initiative

**Bandwidth requirements scaling:**
| GPU Generation | Required Network BW/GPU |
|---|---|
| A100 | 200Gb/s |
| H100 | 400Gb/s |
| B200 / GB200 | 800Gb/s |
| Next-gen (2026+) | 1.6Tb/s |

---

## Supply Constraints

- **NVIDIA NDR InfiniBand switch lead times:** 16–24 weeks; supply improving
- **800G optical transceivers:** Tight supply; co-packaged optics (CPO) emerging as solution
- **Switch ASIC (Tomahawk 5, Jericho3):** TSMC N5 constrained; improving in 2025
- **Fiber cable:** Not constrained but installation labor is

---

## Technology Roadmap

| Technology | Bandwidth | Status | AI Use Case |
|---|---|---|---|
| InfiniBand HDR | 200Gb/s | Legacy | Older training clusters |
| InfiniBand NDR | 400Gb/s | Current | H100 training clusters |
| InfiniBand XDR | 800Gb/s | 2025 | GB200 / Rubin clusters |
| Ultra Ethernet 800G | 800Gb/s | 2025–2026 | Ethernet AI fabric |
| Co-Packaged Optics (CPO) | 3.2T/port | 2026+ | Next-gen fabric density |
| Silicon Photonics | Various | Emerging | Long-reach AI cluster interconnect |

---

## Sales & Marketing Angles

- **InfiniBand lock-in:** NVIDIA GPU + NVIDIA NIC + NVIDIA switch = full stack control
- **Ethernet disruption thesis:** UEC could break NVIDIA networking monopoly by 2027
- **Arista/Broadcom opportunity:** If Ethernet wins for AI, large TAM shift
- **SmartNIC/DPU growth:** NVIDIA BlueField, AMD Pensando — processing offload in AI clusters
- **Optics refresh cycle:** Every GPU generation triggers optical transceiver refresh

---

## Recent Developments

### Update: 2026-05-12 — Baseline entry
> Initial stub. Populate with Ultra Ethernet Consortium 2025 spec release details.

---

## Open Questions

- [ ] Ultra Ethernet 1.0 spec release — when and which vendors shipping?
- [ ] NVIDIA Spectrum-X traction — which hyperscalers deploying at scale?
- [ ] CPO (co-packaged optics) — when does it become mainstream in AI clusters?
