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
