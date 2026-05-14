# NVIDIA Networking (Mellanox / ConnectX)

**Segment(s):** network  
**Role in AI SCM:** Dominant AI cluster interconnect provider; InfiniBand NDR 400G + Spectrum-X Ethernet; acquired Mellanox 2020  
**HQ:** United States (Santa Clara, CA)  
**Ticker:** NASDAQ:NVDA  
**Last Updated:** 2025-05-28

---

## Company Overview

NVIDIA's networking business (built on the 2020 acquisition of Mellanox Technologies for $6.9B) provides the cluster interconnect fabric for the majority of AI data centers worldwide. Products span InfiniBand (dominant in AI training clusters) and Spectrum-X (Ethernet-based alternative for non-InfiniBand environments). NVIDIA networking revenue is included in the Data Center segment and was $4.6B in Q1 FY2026 (quarter ended April 2025), making NVIDIA the largest AI networking vendor by revenue.

**Source:** NVIDIA Q1 FY2026 Earnings, 2025-05-28; Mellanox acquisition, 2020-04-27

---

## Key Products & AI Relevance

| Product / Technology | AI Use Case | Market Position |
|---|---|---|
| NDR InfiniBand 400G (ConnectX-7) | AI training cluster interconnect | Market leader; ~75% of AI cluster fabric (est.) |
| XDR InfiniBand 800G (ConnectX-8) | Next-gen AI training at scale | Ramping; NVIDIA-owned full stack |
| Quantum-2 InfiniBand Switches (400G) | AI cluster spine/leaf | In production at NVIDIA customers |
| Quantum-3 InfiniBand Switches (800G) | Next-gen AI cluster | Sampling / early production |
| Spectrum-X (Ethernet) | AI clusters preferring open Ethernet | Growing; Meta H100 Ethernet clusters confirmed |
| BlueField-3 DPU | GPU server accelerated networking | In production; SmartNIC + DPU market |

**Source:** NVIDIA Q1 FY2026 Earnings, 2025-05-28; NVIDIA GTC 2025 product announcements

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
| Networking Revenue (est.) | ~$4.6B | Q1 FY2026 (Apr 2025) | NVIDIA Q1 FY2026 Earnings, 2025-05-28 |
| Data Center Total Revenue | $39.1B | Q1 FY2026 | NVIDIA Q1 FY2026 Earnings, 2025-05-28 |
| Mellanox Acquisition Price | $6.9B | 2020-04-27 | NVIDIA Press Release, 2020-04-27 |
| Networking Revenue | >$8B annualized run rate (Spectrum-X) | Q1 FY2026 (ended Apr 2025) | NVIDIA Q1 FY2026 PR |
| Networking Revenue | >$10B annualized run rate | Q2 FY2026 (ended Aug 2025) | NVIDIA Q2 FY2026 PR |
| Q4 FY2026 DC Networking Revenue | $11.0B (+263% YoY, +34% QoQ) | Q4 FY2026 (ended Jan 2026) | NVIDIA Q4 FY2026 CFO Commentary |

---

## Supply Chain Position

NVIDIA networking silicon (ConnectX NICs, Quantum switches) is fabbed at TSMC. The full InfiniBand stack — NICs, switches, cables, software — is NVIDIA-owned post-Mellanox. This vertical integration gives NVIDIA pricing power and supply control over AI cluster interconnect. Cable (Active Optical Cable, DAC) supply for NDR InfiniBand is sourced from multiple optical vendors (II-VI/Coherent, InnoLight, Eoptolink).

**Key customers (publicly stated):** CoreWeave, Amazon AWS, Microsoft Azure, Google (InfiniBand at scale); Meta (Spectrum-X Ethernet H100 clusters)  
**Key suppliers (publicly stated):** TSMC (silicon), multiple AOC/DAC cable vendors

**Source:** NVIDIA Q1 FY2026 Earnings, 2025-05-28; CoreWeave S-1, 2025-03-01

---

## Technology Roadmap

| Milestone | Timeline | Status | Source |
|---|---|---|---|
| NDR InfiniBand 400G (ConnectX-7) | 2022–present | Volume production | NVIDIA, 2022 |
| Spectrum-X (Ethernet AI fabric) | 2023–present | Volume; Meta deployment confirmed | NVIDIA GTC 2024 |
| XDR InfiniBand 800G (ConnectX-8) | 2025 | Ramping | NVIDIA GTC 2025 |
| Quantum-3 (800G switches) | 2025–2026 | Sampling / early production | NVIDIA GTC 2025 |
| NVLink 5 (intra-node, Vera Rubin) | 2026+ | Announced | NVIDIA GTC 2025 |

---

## Competitive Position

| Competitor | Segment | Key Differentiator (stated by company or analyst) | Source |
|---|---|---|---|
| Broadcom | Ethernet switch ASIC | Tomahawk 5 (51.2 Tbps); open ecosystem alternative | Broadcom Q2 FY2025 Earnings, 2025-06-05 |
| Arista | AI cluster Ethernet switches | EOS software; 7800R4 series; Microsoft + Meta deployments | Arista Q1 2025 Earnings, 2025-05-07 |
| Marvell | Switch ASIC + DPU | Teralynx; Alaska 800G; DC = 75% of revenue | Marvell Q4 FY2025, 2025-03-06 |
| Ultra Ethernet Consortium (UEC) | Open Ethernet standard | UEC 1.0 spec ratified 2024; no hyperscaler production deployment confirmed | UEC, 2024 |

---

## Updates

### Update: 2020-04-27 — Mellanox acquisition closes at $6.9B; NVIDIA owns InfiniBand + Ethernet

> NVIDIA completed acquisition of Mellanox Technologies for $6.9 billion on April 27, 2020, bringing ownership of HDR InfiniBand (200G), ConnectX NICs, Quantum switch family, and the ConnectX Ethernet portfolio. Mellanox had ~$1.3B in annual revenue at time of acquisition. China regulatory approval (requiring NVIDIA to pledge continued local sales) was the last gating item. The acquisition made NVIDIA the owner of both AI compute (GPUs) and AI cluster networking.

**Source:** NVIDIA Completes Acquisition of Mellanox, NVIDIA Newsroom, 2020-04-27

#segment:network #source-tier:A #signal-type:corporate #company:nvidia_networking #date:2020-04-27 #importance:high #confidence:high

---

### Update: 2023-05 — Spectrum-X announced at Computex; Ethernet purpose-built for AI workloads

> NVIDIA introduced Spectrum-X at Computex May 2023 — an accelerated Ethernet platform purpose-built for AI workloads, combining the Spectrum-4 switch chip with BlueField-3 DPU NICs and adaptive routing technology to reduce AI job completion time over standard Ethernet. Spectrum-X addressed the primary limitation of Ethernet for AI training: network unpredictability and head-of-line blocking. Initial deployments at Microsoft Azure, xAI, Meta, and Google Cloud followed in 2024.

**Source:** NVIDIA Introduces Spectrum-X, Neowin, 2023-05; NVIDIA Newsroom, 2023-11

#segment:network #source-tier:A #signal-type:roadmap #company:nvidia_networking #date:2023-05 #importance:high #confidence:high

---

### Update: 2025-03-18 — Spectrum-X and Quantum-X Photonics CPO switches announced; 100-400 Tb/s

> At GTC March 2025, NVIDIA announced Spectrum-X Photonics and Quantum-X Photonics co-packaged optics switches: 100 Tb/s configuration (128 × 800G ports) and 400 Tb/s configuration (512 × 800G ports), delivering 3.5× power efficiency improvement vs. pluggable optics. Partners: TSMC, Coherent, Corning, Foxconn, Lumentum. InfiniBand Photonics (Quantum-X) expected early 2026; Ethernet Photonics (Spectrum-X) expected H2 2026. Spectrum-X annualizing at >$8B run rate by Q1 FY2026.

**Source:** NVIDIA Announces Spectrum-X Photonics CPO Networking Switches, NVIDIA Investor Relations, 2025-03-18

#segment:network #source-tier:A #signal-type:roadmap #company:nvidia_networking #date:2025-03-18 #importance:high #confidence:high

---

### Update: 2025-05-28 — Q1 FY2026: Networking ~$4.6B; lead times improving to 12–16 weeks

> NVIDIA Q1 FY2026 earnings (May 28, 2025): Data Center revenue $39.1B (+73% YoY). Management noted networking revenue (InfiniBand + Spectrum-X) was approximately $4.6B within DC segment. NDR InfiniBand lead times improved from 20–24 weeks to 12–16 weeks as supply catches up. Spectrum-X Ethernet gaining traction for customers not requiring InfiniBand's full RDMA stack.

**Source:** NVIDIA Q1 FY2026 Earnings, 2025-05-28

#segment:network #source-tier:A #signal-type:supply #company:nvidia_networking #date:2025-05-28 #importance:high #confidence:high

### Update: 2024 — Ultra Ethernet Consortium (UEC) 1.0 spec ratified; no hyperscaler production deployment yet

> The Ultra Ethernet Consortium ratified the Ultra Ethernet 1.0 specification in 2024, targeting an open Ethernet standard optimized for AI cluster workloads (addressing RDMA and congestion control). As of Q1 2025, no major hyperscaler has confirmed volume production deployment of Ultra Ethernet 1.0 hardware. InfiniBand NDR 400G remains the dominant AI training cluster interconnect.

**Source:** Ultra Ethernet Consortium press release, 2024; Industry analysis, Q1 2025

#segment:network #source-tier:B #signal-type:roadmap #company:nvidia_networking #date:2024 #importance:medium #confidence:high #cross-ref

---

## Open Questions

- [ ] Which hyperscaler will be first to deploy Ultra Ethernet 1.0 in production (2025 or 2026)?
- [ ] Spectrum-X market share vs InfiniBand NDR by end of 2025?
- [ ] XDR 800G InfiniBand adoption rate — is it shipping to any customer cluster in H2 2025?
- [ ] NVLink 5 scale-out capability for Vera Rubin — does it reduce InfiniBand dependency?
