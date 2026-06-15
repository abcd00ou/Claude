# AI Networking Technology Roadmap

**Last Updated:** 2026-05-12 (Cycle 4)  
**Coverage:** InfiniBand, Ethernet, Ultra Ethernet, Spectrum-X, AI cluster interconnect evolution

---

## Overview

AI cluster networking is bifurcating into two camps: InfiniBand (NVIDIA-controlled, dominant for training) and Ethernet (open ecosystem, lower cost, increasingly competitive). A third path — Ultra Ethernet (open standard, AI-optimized) — was ratified in 2024 but has not yet reached production deployment at any major hyperscaler. The choice of networking fabric is a 5–10 year infrastructure commitment and directly impacts which silicon vendors supply the cluster.

---

## InfiniBand Roadmap (NVIDIA / Mellanox)

| Generation | Bandwidth | Switch | NIC | Status | Source |
|---|---|---|---|---|---|
| HDR (2019) | 200 Gb/s per port | Quantum (HDR) | ConnectX-6 | Legacy; still deployed | NVIDIA/Mellanox, 2019 |
| NDR (2022) | 400 Gb/s per port | Quantum-2 | ConnectX-7 | Volume production; dominant AI cluster standard | NVIDIA GTC 2022 |
| XDR (2025) | 800 Gb/s per port | Quantum-3 | ConnectX-8 | Sampling / early production | NVIDIA GTC 2025 |
| GDR (2027+) | 1,600 Gb/s per port | Quantum-4 (est.) | ConnectX-9 (est.) | Roadmap; not announced | Industry estimates |

**Lead times (NDR, Q1 2025):** 12–16 weeks (improved from 20–24wk in 2024)

**Source:** NVIDIA GTC 2022, 2024, 2025; NVIDIA Q1 FY2026 Earnings, 2025-05-28

#segment:network #source-tier:A #signal-type:roadmap #date:2025 #importance:high #confidence:high

---

## Ethernet AI Networking

### Standard Ethernet for AI (pre-Ultra Ethernet)

Large Ethernet switches for AI clusters use Broadcom Tomahawk and Jericho ASICs with standard RDMA over Converged Ethernet (RoCE) or similar protocols. Deployed by hyperscalers preferring open ecosystems.

| Broadcom Product | Bandwidth | Status | AI Deployment | Source |
|---|---|---|---|---|
| Tomahawk 5 | 51.2 Tbps total | Volume production | Multiple hyperscalers confirmed | Broadcom Q2 FY2025, 2025-06-05 |
| Jericho3-AI | Distributed Ethernet fabric | Production | Meta, other hyperscalers | Broadcom Q2 FY2025, 2025-06-05 |
| Tomahawk 6 (est.) | ~102.4 Tbps | Development | Roadmap | Industry estimates |

**Source:** Broadcom Q2 FY2025, 2025-06-05; Arista Q1 2025, 2025-05-07

### NVIDIA Spectrum-X (Ethernet AI Fabric)

NVIDIA's Spectrum-X is an Ethernet-based AI networking product combining Spectrum-4 switches (51.2 Tbps) with BlueField-3 DPUs and NVIDIA's RAIL optimization software. It targets customers who want Ethernet economics with InfiniBand-like all-reduce performance.

| Product | Technology | Status | Customer | Source |
|---|---|---|---|---|
| Spectrum-4 switch (51.2 Tbps) | Ethernet | Volume production | Meta (H100 Ethernet clusters) | NVIDIA GTC 2024 |
| Spectrum-X integrated solution | Ethernet + DPU + software | Growing adoption | Meta confirmed; others TBD | NVIDIA Q1 FY2026 Earnings, 2025-05-28 |

**Source:** NVIDIA GTC 2024; NVIDIA Q1 FY2026 Earnings, 2025-05-28

---

## Ultra Ethernet Consortium (UEC)

### Background

The Ultra Ethernet Consortium was formed in 2023 by AMD, Arista, Broadcom, Cisco, Hewlett Packard Enterprise, Intel, Meta, and Microsoft to define an open Ethernet standard optimized for AI cluster workloads. The UEC aims to address RDMA performance, congestion control, and multicast limitations of standard Ethernet for collective AI communication operations (all-reduce, all-gather).

| Milestone | Date | Status |
|---|---|---|
| UEC founded | July 2023 | Complete |
| Ultra Ethernet 1.0 specification ratified | 2024 | Complete |
| First silicon supporting UEC 1.0 | 2025 (est.) | Pending |
| First hyperscaler production deployment | 2025–2026 (est.) | Not confirmed as of Q1 2025 |

**Key gap (as of Q1 2025):** Ultra Ethernet 1.0 spec is ratified, but no major hyperscaler has confirmed volume production deployment. InfiniBand NDR 400G remains the dominant AI training cluster fabric.

**Source:** Ultra Ethernet Consortium press release, July 2023; UEC specification release, 2024; Industry analysis, Q1 2025

#segment:network #source-tier:B #signal-type:roadmap #date:2024 #importance:high #confidence:high

---

## Cluster Networking by Hyperscaler

| Hyperscaler | Training Fabric | Inference Fabric | Custom Networking | Source |
|---|---|---|---|---|
| Amazon AWS | NVIDIA InfiniBand NDR; EFA (custom) for Trainium | EFA | EFA (Elastic Fabric Adapter) for Trainium clusters | AWS re:Invent 2024 |
| Microsoft Azure | NVIDIA InfiniBand NDR (H100) | Ethernet | InfiniBand for OpenAI GPU clusters | Microsoft Q3 FY2026 Earnings |
| Google | Custom ICI (Inter-Chip Interconnect) for TPU pods | ICI | Andromeda (Jupiter network fabric) | Google Cloud Next 2024 |
| Meta | NVIDIA InfiniBand (MI450 training); Spectrum-X (H100 inference) | Spectrum-X | MTIA inference uses internal fabric | Meta Q1 2026 Earnings, 2026-04-29 |
| CoreWeave | NVIDIA InfiniBand NDR | InfiniBand | NVIDIA reference architecture | CoreWeave S-1, 2025-03-01 |

**Source:** Multiple earnings calls and product announcements, 2024–2026

---

## AI Networking Revenue by Vendor (est. Q1 2025 run-rate)

| Vendor | Est. Quarterly Revenue | Technology | Source |
|---|---|---|---|
| NVIDIA (InfiniBand + Spectrum-X) | ~$4.6B | InfiniBand NDR + Ethernet | NVIDIA Q1 FY2026 Earnings, 2025-05-28 |
| Broadcom (switch ASIC) | ~$4.4B AI total (includes ASIC) | Ethernet switch ASICs | Broadcom Q2 FY2025, 2025-06-05 |
| Marvell (switch + DPU) | ~$1.08B AI total | Ethernet switch + DPU | Marvell Q4 FY2025, 2025-03-06 |
| Arista (cluster switches) | ~$1.93B total; AI "material" | EOS Ethernet | Arista Q1 2025, 2025-05-07 |

---

## Open Questions

- [ ] Ultra Ethernet 1.0: which hyperscaler deploys first, and when?
- [ ] Spectrum-X vs InfiniBand split in new H100/B200 clusters — is Spectrum-X gaining share?
- [ ] XDR 800G InfiniBand: volume ramp timeline and first customer cluster?
- [ ] Google Andromeda / ICI: will it be offered externally or remain captive?
- [ ] Arista 400G AI cluster switches — volume with which customer in 2025?
