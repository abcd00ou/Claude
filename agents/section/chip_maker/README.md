# Chip Maker Expert Agent

**Segment:** GPU / xPU Merchant Silicon  
**Sales Lens:** GPU allocation dynamics, competitive positioning, pricing & margin trends  
**Last Updated:** 2026-05-13

---

## Overview

The AI accelerator market is dominated by NVIDIA with approximately 70–85% market share in data center GPUs. AMD is the only credible at-scale alternative; Intel's Gaudi has minimal hyperscaler traction. NVIDIA's FY2026 data center revenue reached $193.7B (+68% YoY). AMD's data center GPU revenue hit $5.8B in Q1 2026 (+57% YoY), driven by 6-gigawatt purchase commitments from both Meta and OpenAI for the MI450 platform. CoWoS packaging at TSMC and HBM supply remain the binding constraints for both vendors.

---

## How AI Accelerators Work

### 2022 — Transformer Engine and FP8 Training Introduced (NVIDIA H100)

> "NVIDIA H100 introduced the Transformer Engine with FP8 mixed-precision training, delivering 4× the training throughput of A100 for transformer models — the dominant AI architecture."

**Source:** NVIDIA H100 Tensor Core GPU Architecture Whitepaper, NVIDIA Corporation, 2022-03

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:nvidia #date:2022-03 #importance:high #confidence:high

---

### 2020 — NVLink and NVSwitch Enable Multi-GPU Scaling Beyond PCIe

> "NVLink 3.0 delivers 600 GB/s GPU-to-GPU bandwidth — 10× PCIe Gen4 — enabling the all-reduce operations required for large model training across hundreds of GPUs."

**Source:** NVIDIA A100 Architecture Whitepaper, NVIDIA Corporation, 2020-05

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:nvidia #date:2020-05 #importance:high #confidence:high

---

### 2007 — CUDA Parallel Computing Platform Released; AI Compute Foundation Set

> "NVIDIA CUDA enabled general-purpose GPU programming, establishing the programming model that would later become the de facto standard for AI model training."

**Source:** NVIDIA CUDA Programming Guide 1.0, NVIDIA Corporation, 2007

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:nvidia #date:2007 #importance:high #confidence:high

---

## History

### 2026-Q1 — AMD: Meta and OpenAI Each Commit 6 GW to MI450

> "We received 6-gigawatt purchase commitments from both Meta and OpenAI for the MI450 platform — the largest publicly disclosed AI chip purchase agreements by wattage outside NVIDIA."
> — AMD CEO, Q1 2026 Earnings Call

**Source:** AMD Q1 2026 Earnings Call Transcript, AMD Investor Relations, 2026-04-29

#segment:chip_maker #source-tier:A #signal-type:design-win #company:amd #company:meta #date:2026-04-29 #importance:high #confidence:high #cross-ref:end_market

---

### 2026-Q1 — NVIDIA FY2026 DC Revenue $193.7B; Q1 FY2027 Guidance $78B

> NVIDIA FY2026 data center revenue: $193.7B (+68% YoY). Q1 FY2027 guidance: approximately $78B in revenue. Blackwell architecture accounting for majority of data center revenue.

**Source:** NVIDIA FY2026 10-K Annual Report, SEC EDGAR, 2026-02-26; NVIDIA Q4 FY2026 Earnings Call, 2026-02-26

#segment:chip_maker #source-tier:A #signal-type:demand #company:nvidia #date:2026-02-26 #importance:high #confidence:high

---

### 2026-Q1 — AMD Q1 2026: DC Revenue $5.8B (+57% YoY)

> "Data center revenue was $5.8 billion for Q1 2026, up 57% year-over-year, driven by MI300X/MI325X ramp and initial MI450 customer qualifications."
> — AMD CFO, Q1 2026 Earnings Call

**Source:** AMD Q1 2026 Earnings Call Transcript, AMD Investor Relations, 2026-04-29

#segment:chip_maker #source-tier:A #signal-type:demand #company:amd #date:2026-04-29 #importance:high #confidence:high

---

### 2025 — NVIDIA Blackwell GB200 NVL72 Begins Volume Production

> NVIDIA Blackwell GB200 NVL72 rack-scale system entered volume production. Each rack: 72 B200 GPUs, 36 HBM3E stacks per GPU, 120 kW power consumption, NVLink interconnect.

**Source:** NVIDIA GTC 2025 Keynote Presentation, NVIDIA Corporation, 2025-03; NVIDIA FY2026 10-K, SEC EDGAR, 2026-02-26

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:nvidia #date:2025 #importance:high #confidence:high

---

### 2024 — AMD MI300X Achieves 8 Hyperscaler Deployments

> AMD MI300X (CDNA3, 192GB HBM3) was deployed by 8 hyperscalers including Microsoft Azure, Meta, Oracle OCI, and Google. First credible high-volume NVIDIA alternative.

**Source:** AMD Q4 2024 Earnings Call, AMD Investor Relations, 2025-01-28

#segment:chip_maker #source-tier:A #signal-type:design-win #company:amd #date:2024 #importance:high #confidence:high

---

### 2022 — NVIDIA H100: First Transformer-Native GPU; $30K+ List Price

> NVIDIA H100 SXM5 introduced at ~$30–35K list price, establishing a new price tier for AI accelerators. First GPU architected specifically for transformer model training and inference.

**Source:** NVIDIA H100 SXM5 Product Brief, NVIDIA Corporation, 2022; NVIDIA FY2023 10-K, SEC EDGAR, 2023

#segment:chip_maker #source-tier:A #signal-type:pricing #company:nvidia #date:2022 #importance:high #confidence:high

---

## Supply Chain

### 2026-02-26 — NVIDIA 10-K Confirms CoWoS Dependency

> "We utilize CoWoS technology for semiconductor packaging. This advanced packaging is performed exclusively at TSMC."
> — NVIDIA Corporation, FY2026 Form 10-K

**Source:** NVIDIA Corporation Form 10-K FY2026, SEC EDGAR, 2026-02-26

#segment:chip_maker #source-tier:A #signal-type:supply #company:nvidia #company:tsmc #date:2026-02-26 #importance:high #confidence:high #cross-ref:foundry

---

### 2026 — SK Hynix Primary HBM Supplier to NVIDIA; Samsung to AMD

> SK Hynix holds approximately 57% HBM share and is the primary supplier to NVIDIA for H200 and Blackwell. Samsung HBM4 collaboration with AMD for MI455X confirmed. Micron supplies both.

**Source:** Samsung Q1 2026 Earnings Call, 2026-04-30; AMD Q1 2026 Earnings Call, 2026-04-29

#segment:chip_maker #source-tier:A #signal-type:supply #date:2026 #importance:high #confidence:high #cross-ref:dram

---

### 2025 — Export Controls Exclude China from Advanced AI Chip Supply

> US export controls (BIS Entity List, H20 restrictions) effectively prohibit NVIDIA from shipping A100/H100 class or above to China. NVIDIA stated China exclusion in FY2026 guidance.

**Source:** US Bureau of Industry and Security Export Control Rules; NVIDIA FY2026 10-K, SEC EDGAR, 2026-02-26

#segment:chip_maker #source-tier:A #signal-type:geopolitical #company:nvidia #date:2025 #importance:high #confidence:high

---

## Competition

### 2026 — NVIDIA ~70–85% DC GPU Share; AMD ~10–15%; Intel Gaudi <2%

> NVIDIA dominates data center AI accelerator revenue at 70–85% share. AMD growing to approximately 10–15% with MI300X/MI325X/MI450. Intel Gaudi 3 remains below 2% despite internal deployments.

**Source:** IDC Worldwide Quarterly Accelerated Computing Tracker, IDC, 2026-Q1

#segment:chip_maker #source-tier:B #signal-type:demand #date:2026 #importance:high #confidence:medium

---

### 2026 — CUDA Software Moat Quantified: 4M+ Developers, 600+ Libraries

> NVIDIA CUDA ecosystem: 4 million+ registered developers, 600+ GPU-accelerated libraries, cuDNN/TensorRT embedded in every major AI framework. This software moat is NVIDIA's primary competitive barrier.

**Source:** NVIDIA GTC 2026 Keynote Presentation, NVIDIA Corporation, 2026-03

#segment:chip_maker #source-tier:A #signal-type:demand #company:nvidia #date:2026-03 #importance:high #confidence:high

---

### 2025 — AMD ROCm 6.0: Closed Key CUDA Compatibility Gaps

> AMD ROCm 6.0 achieved compatibility with PyTorch 2.x, JAX, and key cuDNN/cuBLAS equivalents. Microsoft Azure, Meta, and Oracle confirmed production AI workloads on MI300X without CUDA rewrite.

**Source:** AMD ROCm 6.0 Release Notes, AMD, 2025-Q1; AMD Q1 2025 Earnings Call, AMD Investor Relations, 2025-04

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:amd #date:2025 #importance:high #confidence:high

---

## Product Roadmap

### 2027 — NVIDIA Vera Rubin Production (H2 FY2027); HBM4 Required

> "Vera Rubin is on track for production in the second half of fiscal year 2027." Vera Rubin confirmed to use HBM4. TSMC N2 process node implied but not formally disclosed.

**Source:** NVIDIA FY2026 10-K, SEC EDGAR, 2026-02-26; NVIDIA Q4 FY2026 Earnings Call, 2026-02-26

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:nvidia #date:2026-02-26 #importance:high #confidence:high #cross-ref:dram

---

### 2026–2027 — AMD MI455X: Samsung HBM4, Next CoWoS Generation

> AMD MI455X confirmed to use Samsung HBM4 (differentiated from MI450 which uses SK Hynix HBM3E). TSMC CoWoS-L next generation required. Timeline: H2 2026 sampling, 2027 production.

**Source:** Samsung Q1 2026 Earnings Call, 2026-04-30; AMD Q1 2026 Earnings Call, 2026-04-29

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:amd #company:samsung #date:2026-04-30 #importance:high #confidence:high #cross-ref:dram

---

### 2026 — AMD MI450: 6-GW Commitments; CDNA4 Architecture

> AMD MI450 (CDNA4) secured 6 GW commitments each from Meta and OpenAI. Represents AMD's largest single-generation design win. Manufactured at TSMC with SK Hynix HBM3E.

**Source:** AMD Q1 2026 Earnings Call Transcript, AMD Investor Relations, 2026-04-29; Meta Q1 2026 Earnings Call, 2026-04-29

#segment:chip_maker #source-tier:A #signal-type:design-win #company:amd #date:2026-04-29 #importance:high #confidence:high

---

## Pricing & Allocation

### 2026 — NVIDIA B200 System: >$3M Per GB200 NVL72 Rack

> GB200 NVL72 rack system pricing estimated at $3–4M per rack (72 GPUs + NVLink switches + HBM). Single B200 GPU die: approximately $35–40K list price.

**Source:** NVIDIA GB200 NVL72 System Pricing, industry sources, 2025-Q4; Goldman Sachs AI Infrastructure Report, Goldman Sachs, 2025-Q4

#segment:chip_maker #source-tier:B #signal-type:pricing #company:nvidia #date:2025 #importance:high #confidence:medium

---

### 2026 — AMD MI300X: ~40–50% Discount to Comparable NVIDIA at Volume

> AMD MI300X (192GB HBM3): volume pricing approximately $15–20K vs H100 SXM5 ~$30–35K. AMD pricing strategy: match NVIDIA price-performance, not price point.

**Source:** AMD Investor Day 2025, AMD Corporation, 2025; TF International Securities Chip Pricing Report, 2025-Q3

#segment:chip_maker #source-tier:B #signal-type:pricing #company:amd #date:2025 #importance:medium #confidence:medium

---

### 2024 — GPU-as-a-Service Cloud Pricing: H100 ~$2.50–3.50/hr

> H100 SXM5 cloud rental pricing on major hyperscalers (Azure, AWS, GCP): approximately $2.50–3.50/hr in 2024. Neo-cloud (CoreWeave, Lambda): $2.00–2.75/hr due to lower overhead.

**Source:** Cloud pricing pages (Azure, AWS, GCP), 2024-Q4; Lambda Labs GPU Cloud pricing, 2024

#segment:chip_maker #source-tier:C #signal-type:pricing #date:2024 #importance:medium #confidence:medium

---

## AI Demand Signals

### 2026-04-29 — Alphabet Q1 2026 Capex: $35.7B (+107% YoY); AI Infra Primary Driver

> "Capital expenditures were $35.7 billion in Q1 2026, up 107% year-over-year. The majority of spend is on AI infrastructure including TPU and GPU capacity."
> — Alphabet CFO, Q1 2026 Earnings Call

**Source:** Alphabet Q1 2026 Earnings Call Transcript, Alphabet Investor Relations, 2026-04-29

#segment:chip_maker #source-tier:A #signal-type:demand #company:google #date:2026-04-29 #importance:high #confidence:high #cross-ref:end_market

---

### 2026 — Sovereign AI Programs: Saudi Arabia HUMAIN, UAE G42, Japan SoftBank

> Saudi Arabia HUMAIN and UAE G42 AI programs collectively committed $10–20B+, primarily to NVIDIA. Japan SoftBank/NVIDIA AI initiative: ¥500B commitment. Creates new demand pools outside hyperscalers.

**Source:** NVIDIA GTC 2026 Keynote, NVIDIA Corporation, 2026-03; Saudi HUMAIN Program Announcement, 2026

#segment:chip_maker #source-tier:A #signal-type:demand #company:nvidia #date:2026 #importance:high #confidence:high

---

## 2026-Q2 Updates (2026-05-13)

### 2026-05-20 — NVIDIA Q1 FY2027 Earnings Scheduled; DC Guidance $78B (±2%)

> NVIDIA Q1 FY2027 earnings are scheduled for 2026-05-20. The company guided Q1 FY2027 revenue at approximately $78 billion (±2%), representing ~77% year-over-year growth and exceeding prior consensus by over $5 billion. NVIDIA enters the quarter with a $51.1B net cash position and 71.1% full-year gross margin. China data center revenue explicitly excluded from the guidance.

**Source:** NVIDIA Q1 FY2027 Earnings Preview, IG International, 2026-05-13, https://www.ig.com/en/news-and-trade-ideas/nvidia-q1-fy-2027-earnings-preview-260513; MarketBeat NVDA Q1 2027 Earnings Report, 2026-05-20, https://www.marketbeat.com/earnings/reports/2026-5-20-nvidia-co-stock/

#segment:chip_maker #source-tier:B #signal-type:demand #company:nvidia #date:2026-05-13 #importance:high #confidence:high

---

### 2026-Q1 — NVIDIA Blackwell Sold Out Through Mid-Year; $1 Trillion Order Backlog

> NVIDIA Blackwell GPU systems are completely sold out through mid-2026. Disclosed backlog: $1 trillion in orders for Blackwell and Vera Rubin platforms through 2027 from Meta, Anthropic, OpenAI, AWS, Google Cloud, Microsoft Azure, and Oracle. Data center segment generated $39.1 billion in Q1 FY2027 (calendar Q1 2026), up 69% YoY.

**Source:** NVIDIA Q1 FY2027 Earnings Preview, TIKR, 2026-05, https://www.tikr.com/blog/nvidia-stock-pulls-back-before-may-20-earnings-heres-what-the-1-trillion-demand-story-still-needs-to-prove; NVIDIA Newsroom FY2026 Annual Results, 2026-02-26, https://nvidianews.nvidia.com/news/nvidia-announces-financial-results-for-fourth-quarter-and-fiscal-2026

#segment:chip_maker #source-tier:B #signal-type:supply #company:nvidia #date:2026-Q1 #importance:high #confidence:high

---

### 2026-H2 — NVIDIA Vera Rubin NVL144: Volume Production H2 2026; Foxconn EVT Underway

> NVIDIA Vera Rubin NVL144 rack packs 8 exaflops of AI performance and 100TB of fast memory. Foxconn has begun engineering validation testing (EVT) for the NVL144 MGX liquid-cooled rack. Mass production planned for the latter half of 2026. Vera Rubin promises 10x reduction in inference token cost versus Blackwell.

**Source:** TechPowerUp, "NVIDIA Vera Rubin NVL144 Servers Set for 2026 Volume Production," 2026, https://www.techpowerup.com/342049/nvidia-vera-rubin-nvl144-servers-set-for-2026-volume-production

#segment:chip_maker #source-tier:B #signal-type:roadmap #company:nvidia #date:2026 #importance:high #confidence:high #cross-ref:foundry

---

### 2026-02-06 — AMD MI450 Shipment Ramp: Small Q3, Sharp Q4 2026

> AMD MI450 AI accelerator remains on schedule for volume production in H2 2026. Ramp weighted toward Q4, with small shipments beginning in Q3 2026. AMD guided a "2H26 turning point" in overall AI GPU revenue trajectory.

**Source:** Digitimes, "AMD flags 2H26 turning point as MI450 shipments stay on track," 2026-02-06, https://www.digitimes.com/news/a20260206PD230/amd-shipments-2026-cpu-data-center.html

#segment:chip_maker #source-tier:B #signal-type:supply #company:amd #date:2026-02-06 #importance:high #confidence:high

---

### 2026-Q2 — AMD MI450: TSMC 2nm, 432GB HBM4, 19.6 TB/s Bandwidth

> AMD MI450 manufactured on TSMC 2nm process node. Each GPU features 432GB HBM4 (vs. 288GB HBM3e on MI350), with memory bandwidth of 19.6 TB/s (vs. 8 TB/s on MI350), a 145% improvement. Meta deal: $60B over five years for up to 6GW of MI450 GPUs, with a performance-based warrant for 160 million AMD shares (~10% of company) vesting at 1GW–6GW shipment milestones.

**Source:** AMD MI400 Series Coverage, Tech-Insider.org, 2026, https://tech-insider.org/amd-mi400-series-ai-gpu-data-center-2026/; Digitimes AMD MI450 coverage, 2026-02-06

#segment:chip_maker #source-tier:B #signal-type:roadmap #company:amd #company:meta #date:2026-Q2 #importance:high #confidence:medium #cross-ref:end_market

---

### 2026 — Intel Ends Gaudi Line; Gaudi 3 Is Final Standalone Accelerator

> Intel's Gaudi product line is officially being retired. Gaudi 3, unveiled in 2024, is the final entry in Intel's standalone AI chip series. No Gaudi 4 planned. Intel's next AI platform, codenamed Jaguar Shores, is a rack-scale system integrating compute, networking, and memory — not a discrete accelerator — targeting 2026 launch. Jaguar Shores will use HBM4 memory (SK Hynix). Intel's strategic pivot is away from competing directly with NVIDIA/AMD in the discrete accelerator market.

**Source:** PC Outlet, "Intel Ends Gaudi Line: What Jaguar Shores Means for the Future of AI Hardware," 2026, https://pcoutlet.com/software/ai/intel-ends-gaudi-line-what-jaguar-shores-means-for-the-future-of-ai-hardware; Tom's Hardware, "Jaguar Shores is the successor to Intel's Falcon Shores AI accelerators," 2026, https://www.tomshardware.com/tech-industry/artificial-intelligence/jaguar-shores-is-the-successor-to-intels-falcon-shores-ai-accelerators-gaudi-asics-and-xe-hpc-gpus-united-in-a-single-lineup

#segment:chip_maker #source-tier:B #signal-type:roadmap #company:intel #date:2026 #importance:high #confidence:high

---

## Open Questions

- [ ] Vera Rubin (R100) detailed spec — TSMC N2? CoWoS-L next-gen? HBM4 configuration?
- [ ] AMD MI450 custom specs for Meta vs. OpenAI — same chip or differentiated?
- [ ] Intel Jaguar Shores — any hyperscaler evaluation or LOI disclosed?
- [ ] NVIDIA Q1 FY2027 actual results — confirm $78B guidance hit (earnings 2026-05-20)
- [ ] NVIDIA exclusion of China DC guidance — how large is the China revenue gap?
