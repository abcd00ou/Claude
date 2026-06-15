# NVIDIA Corporation

**Segment(s):** chip_maker  
**Role in AI SCM:** Dominant AI accelerator supplier; ~80%+ data center GPU market share; CUDA ecosystem lock-in; NVLink interconnect  
**HQ:** Santa Clara, California, USA  
**Ticker:** NASDAQ:NVDA  
**Last Updated:** 2026-02-25

---

## Company Overview

NVIDIA is the dominant supplier of AI accelerators, with FY2026 Data Center revenue of $193.7 billion — representing approximately 90% of total company revenue. Its CUDA software ecosystem creates strong switching costs. NVIDIA's Blackwell architecture (H/B/GB series) is the current high-volume product. Vera Rubin is the next-generation platform with production targeted for H2 FY2027 (calendar Aug 2027–Jan 2028).

**Source:** NVIDIA Q4 FY2026 Earnings Press Release, 8-K (accession 0001045810-26-000019), 2026-02-25; NVIDIA 10-K FY2026 (accession 0001045810-26-000021), 2026-02-25

---

## Key Products & AI Relevance

| Product / Technology | AI Use Case | Status |
|---|---|---|
| Blackwell B200 / GB200 NVL72 | AI training and inference (rack-scale) | In volume production |
| Grace Blackwell (GB200) | Inference; "order-of-magnitude lower cost per token" | Volume production |
| Vera Rubin platform (6 chips) | Next-gen training/inference; "up to 10x lower inference token cost vs Blackwell" | Production H2 FY2027 |
| NVLink interconnect | GPU-to-GPU connectivity in AI clusters | Proprietary |
| CUDA platform | AI software ecosystem, framework support | Market standard |
| Networking (InfiniBand NDR, Spectrum-X) | AI cluster fabric | Mellanox/NVIDIA |

**Source:** NVIDIA Q4 FY2026 Earnings Press Release, 2026-02-25; NVIDIA 10-K FY2026, 2026-02-25

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
| Total Revenue | $16.68B | FY2021 (ended Jan 2021) | NVIDIA Q4 FY2021 Press Release |
| Data Center Revenue | $6.04B | FY2021 | NVIDIA Q4 FY2021 Press Release |
| Total Revenue | $26.97B | FY2022 (ended Jan 2022) | NVIDIA Q4 FY2022 SEC Filing |
| Data Center Revenue | $10.61B (+58% YoY) | FY2022 | NVIDIA Q4 FY2022 SEC Filing |
| Total Revenue | $26.97B (flat) | FY2023 (ended Jan 2023) | NVIDIA Q4 FY2023 Press Release |
| Data Center Revenue | $15.01B (+41% YoY) | FY2023 | NVIDIA Q4 FY2023 Press Release |
| Total Revenue | $60.92B (+126% YoY) | FY2024 (ended Jan 2024) | NVIDIA Q4 FY2024 Investor Relations |
| Data Center Revenue | $47.53B (78% of total) | FY2024 | NVIDIA Q4 FY2024 Investor Relations |
| Total Revenue | $130.50B (+114% YoY) | FY2025 (ended Jan 2025) | NVIDIA Q4 FY2025 Press Release |
| Data Center Revenue | $115.2B | FY2025 | NVIDIA Q4 FY2025 Press Release |
| Total Revenue | $215.9B (+65% YoY) | FY2026 (ended Jan 2026) | NVIDIA 10-K FY2026, 2026-02-25 |
| Data Center Revenue | $193.7B (+68% YoY) | FY2026 | NVIDIA 10-K FY2026, 2026-02-25 |
| Q4 FY2026 Data Center Revenue | $62.3B (+22% QoQ, +75% YoY) | Q4 FY2026 | NVIDIA Q4 FY2026 Press Release, 2026-02-25 |
| Q4 FY2026 DC Compute | $51.3B (+19% QoQ, +58% YoY) | Q4 FY2026 | NVIDIA Q4 FY2026 CFO Commentary 8-K, 2026-02-25 |
| Q4 FY2026 DC Networking | $11.0B (+34% QoQ, +263% YoY) | Q4 FY2026 | NVIDIA Q4 FY2026 CFO Commentary 8-K, 2026-02-25 |
| Q1 FY2027 Revenue Guidance | $78.0B ±2% | Q1 FY2027 outlook | NVIDIA Q4 FY2026 CFO Commentary, 2026-02-25 |
| China DC compute in guidance | $0 (excluded) | Q1 FY2027 | NVIDIA Q4 FY2026 CFO Commentary, 2026-02-25 |

---

## Supply Chain Position

NVIDIA designs GPUs and sources manufacturing from TSMC (confirmed in 10-K: uses CoWoS packaging). HBM3E is sourced from SK Hynix (primary), Micron (qualified), Samsung (qualification in progress as of early 2025). Vera Rubin platform requires HBM4, with Micron confirmed as HBM4 supplier.

**Key customers (publicly stated):** AWS, Google Cloud, Microsoft Azure, Oracle Cloud Infrastructure (confirmed Vera Rubin first deployers)  
**Key suppliers (publicly stated):** TSMC (fab + CoWoS confirmed in 10-K)

**Source:** NVIDIA 10-K FY2026, SEC, 2026-02-25; NVIDIA Q4 FY2026 Press Release, 2026-02-25

---

## Technology Roadmap

| Milestone | Timeline | Status | Source |
|---|---|---|---|
| Blackwell / Grace Blackwell | FY2026 (volume) | In production | NVIDIA 10-K FY2026, 2026-02-25 |
| Vera Rubin platform (6 chips) | H2 FY2027 (Aug 2027–Jan 2028 calendar) | Production commencing | NVIDIA 10-K FY2026, 2026-02-25 |
| Vera Rubin perf claim | "Up to 10x lower inference token cost vs Blackwell" | Announced | NVIDIA Q4 FY2026 Press Release, 2026-02-25 |

---

## Updates

### Update: 2020-04-27 — Mellanox acquisition closes at $6.9B; NVIDIA enters networking

> NVIDIA completed the acquisition of Mellanox Technologies for $6.9 billion (approximately $125 per share) on April 27, 2020. Mellanox provides InfiniBand and high-speed Ethernet interconnect technology. The acquisition gave NVIDIA ownership of NDR InfiniBand (400G), ConnectX NICs, and the Quantum switch family — becoming the technology foundation for AI cluster networking. CEO Jensen Huang called the acquisition a "homerun deal." China regulatory approval was the final gating item.

**Source:** NVIDIA Completes Acquisition of Mellanox, NVIDIA Newsroom, 2020-04-27

#segment:chip_maker #source-tier:A #signal-type:supply #company:nvidia #date:2020-04-27 #importance:high #confidence:high

---

### Update: 2020-05-14 — A100 GPU announced (Ampere architecture); first AI-class GPU for DGX A100

> NVIDIA announced the A100 GPU at GTC May 2020. Built on TSMC 7nm (Samsung 8nm for some variants), A100 features 40GB (later 80GB) HBM2e, 6,912 CUDA cores, and the first Tensor Core third-generation supporting TF32 and BF16 precision. The DGX A100 system (8× A100 SXM, NVLink interconnect) became the standard AI training cluster of 2020-2022. Data center revenue in FY2021 (ended Jan 2021) was $6.04B.

**Source:** NVIDIA Newsroom GTC 2020; NVIDIA Q4 FY2021 Press Release, 2021-02-24

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:nvidia #date:2020-05-14 #importance:high #confidence:high

---

### Update: 2022-03-22 — H100 GPU announced (Hopper architecture); first PCIe Gen5/SXM5 AI chip

> NVIDIA announced the H100 GPU at GTC March 2022. Built on TSMC 4nm (N4), H100 features 80GB HBM2e (SXM5), 4th-gen Tensor Cores, NVLink 4.0 (900 GB/s bidirectional), and the Transformer Engine — dedicated for large language model training. H100 became the dominant AI training GPU of 2023-2024. NVIDIA FY2022 total revenue: $26.97B; Data Center revenue: $10.61B (+58% YoY).

**Source:** NVIDIA Announces Hopper GPU Architecture, NVIDIA Newsroom, 2022-03-22; NVIDIA Q4 FY2022 SEC Filing, 2022

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:nvidia #date:2022-03-22 #importance:high #confidence:high

---

### Update: 2022-10-07 — BIS export controls ban A100/H100 to China; NVIDIA develops A800/H800

> The U.S. Bureau of Industry and Security imposed export controls on October 7, 2022, prohibiting sale of NVIDIA A100 and H100 GPUs to China and Russia without a license. NVIDIA responded by developing China-compliant variants: A800 (A100 equivalent with reduced NVLink bandwidth) and H800 (H100 equivalent with reduced chip-to-chip interconnect). Both chips were later banned in October 2023 when BIS tightened rules, prompting NVIDIA to develop H20 and L20 as compliant alternatives for China. NVIDIA FY2023 total revenue: $26.97B (flat YoY); Data Center: $15.01B (+41%).

**Source:** BIS Export Controls Rule, 2022-10-07; CNBC, Reuters, 2022-10-07

#segment:chip_maker #source-tier:A #signal-type:geopolitical #company:nvidia #date:2022-10-07 #importance:high #confidence:high

---

### Update: 2023-11 — H200 announced with 141GB HBM3E; 4.89 TB/s bandwidth

> At SC23 (November 2023), NVIDIA announced the H200 GPU — a Hopper-architecture upgrade featuring 141GB HBM3E (vs. H100's 80GB HBM2e) and approximately 4.89 TB/s memory bandwidth. SK Hynix supplied the first HBM3E in volume. H200 became the primary AI inference chip for hyperscalers in 2024. NVIDIA FY2024 revenue: $60.92B (+126% YoY); Data Center: $47.53B (78% of total).

**Source:** NVIDIA SC23 Announcement, 2023-11; NVIDIA Q4 FY2024 Investor Relations, 2024

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:nvidia #date:2023-11 #importance:high #confidence:high

---

### Update: 2024-03-18 — B200/GB200 announced (Blackwell architecture); GB200 NVL72 rack-scale design

> At GTC March 2024, NVIDIA announced the Blackwell B200 GPU and GB200 "Grace Blackwell" superchip (Blackwell GPU + Grace ARM CPU). The GB200 NVL72 rack system contains 72 B200 GPUs connected via NVLink 5 with 1.8 exaflops compute. Blackwell uses TSMC 4NP (custom 4nm) with a two-die 208B transistor design connected by NVLink-C2C. GB200 NVL72 began customer shipments in December 2024. NVIDIA FY2025 total revenue: $130.5B (+114% YoY); Data Center: $115.2B.

**Source:** NVIDIA GTC 2024 Announcement, 2024-03-18; NVIDIA Q4 FY2025 Press Release, 2025

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:nvidia #date:2024-03-18 #importance:high #confidence:high

---

### Update: 2025-09 — Samsung clears NVIDIA HBM3E qualification after 18-month delay

> Samsung cleared NVIDIA's 12-layer HBM3E validation in mid-to-late September 2025 after approximately 18 months of failed qualification attempts. Samsung had been unable to meet NVIDIA's performance and thermal requirements for the 12-high (36GB) HBM3E stack. The fix involved redesigning the DRAM core. Prior to qualification, Samsung was not a meaningful supplier for H100 or H200 HBM. Following clearance, Samsung began HBM3E shipments to NVIDIA for Blackwell products and sold out its 2026 HBM allocation.

**Source:** Samsung 12H HBM3E Clears NVIDIA Tests, TrendForce, 2025-09-22; Tom's Hardware, 2025-09

#segment:chip_maker #source-tier:A #signal-type:supply #company:nvidia #date:2025-09 #importance:high #confidence:high

---

### Update: 2026-03 — Samsung and SK Hynix both tapped as HBM4 suppliers for Vera Rubin

> Samsung began world-first HBM4 mass production in the third week of February 2026. Samsung and SK Hynix were both confirmed as NVIDIA Vera Rubin HBM4 suppliers as of March 2026. SK Hynix holds approximately 70% of NVIDIA's Vera Rubin HBM4 orders (per UBS estimates); Samsung approximately 30%. Micron was also confirmed as a HBM4 supplier. SK Hynix completed world-first HBM4 development on September 12, 2025 and declared mass production readiness.

**Source:** Samsung, SK Hynix Reportedly Tapped as NVIDIA Rubin HBM4 Suppliers, TrendForce, 2026-03-09; SK Hynix HBM4 Development Completion, SK Hynix Newsroom, 2025-09-12

#segment:chip_maker #source-tier:A #signal-type:supply #company:nvidia #date:2026-03 #importance:high #confidence:high

---

### Update: 2026-02-25 — Q4 FY2026: DC revenue $62.3B (record); FY2026 DC total $193.7B; Q1 FY2027 guided $78B

> Record quarterly Data Center revenue of $62.3 billion, up 22% from Q3 and up 75% from a year ago. Full-year FY2026 Data Center revenue: $193.7 billion (up 68%). Q1 FY2027 outlook: revenue $78.0B ±2%. "We are not assuming any Data Center compute revenue from China in our outlook."

**Source:** NVIDIA Q4 FY2026 Earnings Press Release, 8-K (accession 0001045810-26-000019), 2026-02-25; NVIDIA Q4 FY2026 CFO Commentary, 2026-02-25

#segment:chip_maker #source-tier:A #signal-type:demand #company:nvidia #date:2026-02-25 #importance:high #confidence:high #cross-ref:foundry

---

### Update: 2026-01 — Vera Rubin Hardware Specs Disclosed at CES 2026: 288 GB HBM4, 22 TB/s, 50 PFLOPS

> NVIDIA disclosed Vera Rubin (R100) hardware specifications at CES 2026 (January 2026): 336 billion transistors; TSMC 3nm dual-die design; 288 GB HBM4 per GPU; 22 TB/s memory bandwidth (vs. Blackwell B200: 8 TB/s — 2.75× increase); 50 PFLOPS NVFP4 inference per GPU (5× Blackwell inference performance). Vera Rubin NVL72 system: 72 GPUs connected via NVLink 6; 3.6 exaflops compute; 260 TB/s all-to-all bandwidth. Jensen Huang confirmed first Vera Rubin NVL72 rack operational at Microsoft Azure. Full production shipments targeted H2 2026. Blackwell sold out through mid-2026 with a backlog of approximately 3.6 million units; B300 lead times improved from 36 weeks to ~18 weeks.

**Source:** NVIDIA Newsroom, 2026-01; Tom's Hardware, 2026-01; ServeTheHome, 2026-01; NVIDIA Technical Blog, 2026-01

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:nvidia #date:2026-01 #importance:high #confidence:high #cross-ref:foundry,dram

---

### Update: 2026-02-25 — Vera Rubin platform: production H2 FY2027; first customers AWS/Google/Azure/Oracle

> "We unveiled the NVIDIA Rubin platform, comprising six new chips to deliver up to a 10x reduction in inference token cost, compared with the NVIDIA Blackwell platform; cloud providers Amazon Web Services (AWS), Google Cloud, Microsoft Azure and Oracle Cloud Infrastructure will be among the first to deploy Vera Rubin-based instances." Production shipments expected to commence in the second half of fiscal year 2027 (calendar Aug 2027–Jan 2028).

**Source:** NVIDIA Q4 FY2026 Earnings Press Release, 2026-02-25; NVIDIA 10-K FY2026, 2026-02-25

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:nvidia #date:2026-02-25 #importance:high #confidence:high #cross-ref:foundry #cross-ref:dram

---

### Update: 2026-02-25 — Jensen Huang: "Grace Blackwell with NVLink is the king of inference today"

> Jensen Huang, CEO: "Computing demand is growing exponentially — the agentic AI inflection point has arrived. Grace Blackwell with NVLink is the king of inference today — delivering an order-of-magnitude lower cost per token — and Vera Rubin will extend that leadership even further."

**Source:** NVIDIA Q4 FY2026 Earnings Press Release, 8-K, 2026-02-25

#segment:chip_maker #source-tier:A #signal-type:demand #company:nvidia #date:2026-02-25 #importance:high #confidence:high

---

### Update: 2026-02-25 — CoWoS confirmed in 10-K; China DC compute excluded from guidance

> 10-K filing confirms: "We utilize CoWoS technology for semiconductor packaging." Q1 FY2027 guidance explicitly states: "We are not assuming any Data Center compute revenue from China in our outlook."

**Source:** NVIDIA 10-K FY2026 (accession 0001045810-26-000021), SEC EDGAR, 2026-02-25; NVIDIA Q4 FY2026 CFO Commentary, 2026-02-25

#segment:chip_maker #source-tier:A #signal-type:geopolitical #company:nvidia #date:2026-02-25 #importance:high #confidence:high #cross-ref:foundry

---

### Update: 2026-05 — Vera Rubin NVL72 hyperscaler deployments confirmed; NVL144 disclosed; Spectrum-X >$10B run rate; Q1 FY2027 earnings May 20

> Confirmed NVL72 early deployments: Microsoft was first to power on an NVL72 system (GTC 2026, March); AWS committed 1M+ NVIDIA GPUs including Vera Rubin H2 2026; Google Cloud and OCI confirmed as first cloud providers for NVL72 instances in H2 2026; CoreWeave and xAI committed as early adopters. NVL144 (Vera Rubin Ultra) specs disclosed: 144 GPUs, 600 kW/rack, 15 EFLOPS FP4, availability H2 2027. Spectrum-X Ethernet networking crossed $10B annualized run rate and is growing faster than InfiniBand. NVIDIA Q1 FY2027 earnings scheduled May 20, 2026; sell-side consensus: ~$78.8B total / $72.8B Data Center; buy-side whisper ~$79–80B.

**Source:** NVIDIA Newsroom, DataCenterDynamics, S&P Global, Motley Fool, 247WallSt, 2026-05

#segment:chip_maker #source-tier:A #signal-type:demand #company:nvidia #date:2026-05 #importance:high #confidence:high #cross-ref:network #cross-ref:end_market #cross-ref:dram

---

## Open Questions

- [x] Vera Rubin HBM type and capacity per chip — **resolved**: 288 GB HBM4, 22 TB/s (CES 2026, Jan 2026)
- [x] NVIDIA Networking ($11B Q4 FY2026, +263% YoY) — **resolved**: Spectrum-X Ethernet crossed $10B annualized run rate, growing faster than InfiniBand (May 2026)
- [ ] Samsung HBM3E qualification status for Blackwell — any public update post Q4 FY2026?
