# ASIC Expert Agent

**Segment:** Custom AI Silicon / Application-Specific Integrated Circuits  
**Sales Lens:** In-house accelerator programs, merchant silicon displacement, design win timelines  
**Last Updated:** 2026-05-12

---

## Overview

Hyperscalers are building custom AI ASICs to reduce NVIDIA dependency, optimize for their specific model architectures, and lower total cost of ownership. Custom ASICs now represent 20–30% of AI accelerator deployments at leading hyperscalers, growing toward 40–50% by 2027. In Q1 2026, Meta confirmed MTIA Gen 2 (2nm/Broadcom) in production; Amazon confirmed Trainium3 shipping; Google confirmed TPU 8 training and inference variants deployed; and Microsoft confirmed Maia 200 on Azure. Every major hyperscaler now has at least one production custom silicon program.

---

## How Custom Silicon Is Built

### 2022 — Chiplet Architecture Enables Cost-Effective Custom ASIC Scaling

> "Chiplet-based design allows hyperscalers to mix-and-match compute dies (custom) with standard IP blocks (SerDes, PHY, memory controllers) from TSMC or third-party IP vendors, reducing NRE cost by 40–60% vs monolithic SoC design."

**Source:** "Chiplet Design Methodology for HPC Applications," IEEE Hot Chips Symposium 2022

#segment:asic #source-tier:S #signal-type:roadmap #date:2022 #importance:medium #confidence:high

---

### 2018 — Google TPU Architecture Published; Custom Tensor Processing Unit

> "Google published the first TPU architecture paper describing a 65,536-unit matrix multiply unit (MXU) optimized for deep learning inference. TPU achieves 15–30× better performance/watt vs GPU for TensorFlow workloads."

**Source:** "In-Datacenter Performance Analysis of a Tensor Processing Unit," Google, ISCA 2017, published 2018

#segment:asic #source-tier:S #signal-type:roadmap #company:google #date:2018 #importance:high #confidence:high

---

## History

### 2026-Q1 — Meta MTIA Gen 2 (2nm/Broadcom) in Production

> "Our MTIA Gen 2, built on a 2nm process with Broadcom as our design partner, is now in production and handling inference workloads at scale. This represents a significant step in reducing our dependence on third-party AI accelerators."
> — Meta CEO, Q1 2026 Earnings Call

**Source:** Meta Q1 2026 Earnings Call Transcript, Meta Investor Relations, 2026-04-29

#segment:asic #source-tier:A #signal-type:roadmap #company:meta #date:2026-04-29 #importance:high #confidence:high #cross-ref:foundry

---

### 2026-Q1 — Google TPU 8t and TPU 8i in Production Deployment

> "TPU 8t for training and TPU 8i for inference are both in production. They are deployed across our data centers and available to Google Cloud customers."
> — Alphabet CEO, Q1 2026 Earnings Call

**Source:** Alphabet Q1 2026 Earnings Call Transcript, Alphabet Investor Relations, 2026-04-29

#segment:asic #source-tier:A #signal-type:roadmap #company:google #date:2026-04-29 #importance:high #confidence:high

---

### 2026-Q1 — Amazon Trainium3 Shipping to Customers

> "Trainium3 is now shipping to customers. It offers significantly improved performance-per-watt for large language model training compared to Trainium2."
> — Amazon CEO, Q1 2026 Earnings Call

**Source:** Amazon Q1 2026 Earnings Call Transcript, Amazon Investor Relations, 2026-05-01

#segment:asic #source-tier:A #signal-type:roadmap #company:amazon #date:2026-05-01 #importance:high #confidence:high

---

### 2026-Q1 — Microsoft Maia 200 Deployed in Production on Azure

> "Maia 200 is deployed in our Azure AI infrastructure and handling a portion of our internal AI workloads. We continue to develop the next generation Maia architecture."
> — Microsoft CEO, Q3 FY2026 Earnings Call

**Source:** Microsoft Q3 FY2026 Earnings Call Transcript, Microsoft Investor Relations, 2026-04-29

#segment:asic #source-tier:A #signal-type:roadmap #company:microsoft #date:2026-04-29 #importance:high #confidence:high

---

### 2025 — Amazon Project Rainier: 100K+ Trainium2 Cluster Operational

> "Project Rainier is now operational — over 100,000 Trainium2 chips, the largest AI training cluster ever built by a single company."
> — Amazon CEO, AWS re:Invent 2025

**Source:** Amazon AWS re:Invent 2025 Keynote, Amazon Web Services, 2025-12

#segment:asic #source-tier:A #signal-type:demand #company:amazon #date:2025-12 #importance:high #confidence:high

---

### 2023 — ASIC Programs Shift from Inference-Only to Training-Capable

> Google TPU v4 (training at scale), Amazon Trainium2 (training), and Meta MTIA v2 (inference + future training) marked the shift from inference-only ASIC programs to full training-capable custom silicon.

**Source:** Google TPU v4 Blog Post, Google AI, 2023; Amazon Trainium2 Press Release, Amazon Web Services, 2023

#segment:asic #source-tier:A #signal-type:roadmap #date:2023 #importance:high #confidence:high

---

## Supply Chain

### 2026 — All Major Hyperscaler ASICs Fabricated at TSMC; CoWoS Required

> Google TPU 8, Amazon Trainium3, Meta MTIA Gen 2, Microsoft Maia 200 — all are fabricated at TSMC. Most require CoWoS advanced packaging, creating competition with NVIDIA/AMD for the same capacity.

**Source:** Meta Q1 2026 Earnings Call, 2026-04-29; Alphabet Q1 2026 Earnings Call, 2026-04-29; industry sources

#segment:asic #source-tier:A #signal-type:supply #date:2026-04-29 #importance:high #confidence:high #cross-ref:foundry

---

### 2026 — ASIC Design Houses: Marvell and Broadcom as Primary Partners

> Marvell (OCTEON series, custom HPC ASIC) and Broadcom (XPU programs, Meta MTIA partnership) are the primary external ASIC design service providers for hyperscalers. Both use TSMC advanced nodes.

**Source:** Marvell Q4 FY2026 Earnings Call, Marvell Investor Relations, 2026-03; Broadcom FY2025 10-K, SEC EDGAR, 2025-12

#segment:asic #source-tier:A #signal-type:supply #date:2026 #importance:high #confidence:high

---

### 2025 — ASIC Design Cycles: 3–5 Years from Concept to Volume Production

> Custom AI ASIC development cycles: architecture definition (6–12 months) → RTL design (12–18 months) → tape-out and silicon bring-up (6–9 months) → qualification (6–12 months) → volume ramp (6–12 months). Total: 3–5 years minimum.

**Source:** "Custom Silicon Development at Hyperscale," IEEE ISSCC Tutorial 2025

#segment:asic #source-tier:S #signal-type:roadmap #date:2025 #importance:medium #confidence:high

---

## Programs & Design Wins

### 2026-Q1 — Google Cloud Backlog $462B; TPU 8 Available to External Customers

> "Our Google Cloud backlog reached $462 billion. TPU 8 is now available to Cloud customers, providing Google's most capable AI training and inference hardware as an external service."

**Source:** Alphabet Q1 2026 Earnings Call Transcript, Alphabet Investor Relations, 2026-04-29

#segment:asic #source-tier:A #signal-type:design-win #company:google #date:2026-04-29 #importance:high #confidence:high #cross-ref:end_market

---

### 2026 — AMD Confirmed as MTIA Gen 2 Alternative; Meta Retains NVIDIA for Training

> Meta MTIA Gen 2 handles inference; NVIDIA H100/B200 retained for Llama model training. This bifurcated strategy (custom for inference, merchant for training) is the dominant hyperscaler ASIC pattern.

**Source:** Meta Q1 2026 Earnings Call Transcript, Meta Investor Relations, 2026-04-29

#segment:asic #source-tier:A #signal-type:demand #company:meta #company:nvidia #date:2026-04-29 #importance:high #confidence:high #cross-ref:chip_maker

---

## Technology Roadmap

### 2027 — Next-Gen Hyperscaler ASICs: N2 / A16 Nodes; 3D Integration

> Google TPU 9, Amazon Trainium4, Meta MTIA Gen 3 — all expected on TSMC N2 or A16 nodes (2027). 3D IC integration (SoIC) targeted for post-2027 generations.

**Source:** Alphabet Q1 2026 Earnings Call, 2026-04-29 (roadmap implied); TSMC Technology Roadmap 2025

#segment:asic #source-tier:A #signal-type:roadmap #date:2026 #importance:medium #confidence:medium

---

### 2026 — TSMC N2: First ASIC Programs Taping Out

> TSMC N2 customer tape-outs in 2025–2026 include multiple hyperscaler ASIC programs. N2 delivers ~20% speed improvement over N3 at equivalent power.

**Source:** TSMC Q1 2026 Earnings Call, TSMC Investor Relations, 2026-04-17

#segment:asic #source-tier:A #signal-type:roadmap #company:tsmc #date:2026-04-17 #importance:medium #confidence:high #cross-ref:foundry

---

## AI Demand Signals

### 2026 — ASIC Displacement Accelerating: Custom Silicon ~20–30% of Hyperscaler Deployments

> Hyperscaler ASIC programs collectively represent 20–30% of accelerator deployments at leading hyperscalers as of 2026, up from ~10–15% in 2023. Growing toward 40–50% by 2027 as programs mature.

**Source:** "Custom Silicon at Hyperscale," Goldman Sachs Technology Research, 2026-Q1

#segment:asic #source-tier:B #signal-type:demand #date:2026 #importance:high #confidence:medium

---

### 2026 — Inference Optimization Driving New ASIC Investment Cycle

> Agentic AI workloads (continuous inference, real-time recommendation) are driving a new cycle of inference-optimized ASIC investment. Samsung "Key Value SSD for AI inference" and MTIA Gen 2 are both inference-specific developments this cycle.

**Source:** Samsung Q1 2026 Earnings Call, 2026-04-30; Meta Q1 2026 Earnings Call, 2026-04-29

#segment:asic #source-tier:A #signal-type:demand #date:2026-04-30 #importance:high #confidence:high #cross-ref:storage

---

## Open Questions

- [ ] MTIA Gen 3 roadmap — no public disclosure as of 2026-05-12
- [ ] Microsoft Maia 200 TSMC node — not publicly confirmed (N3? N5?)
- [ ] Trainium3 detailed spec — node, memory type, bandwidth — not fully public
- [ ] Broadcom's unnamed hyperscaler ASIC programs beyond Meta MTIA — any public signals?
