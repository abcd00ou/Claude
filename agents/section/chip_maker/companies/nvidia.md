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

## Open Questions

- [x] Vera Rubin HBM type and capacity per chip — **resolved**: 288 GB HBM4, 22 TB/s (CES 2026, Jan 2026)
- [ ] NVIDIA Networking ($11B Q4 FY2026, +263% YoY) — what drives the networking spike?
- [ ] Samsung HBM3E qualification status for Blackwell — any public update post Q4 FY2026?
