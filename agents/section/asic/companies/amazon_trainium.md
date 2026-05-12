# Amazon Trainium / Inferentia (AWS Custom Silicon)

**Segment(s):** asic  
**Role in AI SCM:** AWS custom AI training (Trainium) and inference (Inferentia) ASIC program; Trainium3 shipping in 2025  
**HQ:** United States (Seattle, WA)  
**Ticker:** NASDAQ:AMZN  
**Last Updated:** 2026-05-01

---

## Company Overview

Amazon Web Services (AWS) designs custom AI accelerators under the Trainium (training) and Inferentia (inference) brands as part of Annapurna Labs, acquired by Amazon in 2015. The program aims to reduce AWS's dependence on NVIDIA GPUs for AI workloads while offering cost-efficient alternatives to customers. Trainium3 entered early shipping in 2025. Amazon has demonstrated 100,000+ Trainium2 chip clusters, one of the world's largest single-technology AI compute clusters. AWS is also the world's largest cloud provider and NVIDIA's largest GPU customer.

**Source:** Amazon Q1 2026 Earnings, 2026-05-01; AWS re:Invent 2024; Amazon 10-K FY2024

---

## Key Products & AI Relevance

| Product / Technology | AI Use Case | Market Position |
|---|---|---|
| Trainium (1st gen, 2021) | ML training; AWS-internal initially | Legacy; succeeded by Trainium2 |
| Trainium2 (4nm TSMC, 2024) | Large model training; 100K+ cluster | In production; customer available via AWS |
| Trainium3 (2025) | Next-gen training; performance uplift | Early shipping; sampling to select customers |
| Inferentia2 (4nm TSMC, 2023) | AI inference; cost-efficient | In production; AWS Bedrock; SageMaker |
| AWS Neuron SDK | Trainium/Inferentia software stack | Open-source; supports PyTorch, JAX |

**Source:** AWS re:Invent 2024; Amazon Q1 2026 Earnings, 2026-05-01; AWS Neuron documentation

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
| AWS Revenue | $29.3B (+17% YoY) | Q1 2026 (Jan–Mar 2026) | Amazon Q1 2026 Earnings, 2026-05-01 |
| Amazon Capex | $43.2B | Q1 2026 | Amazon Q1 2026 Earnings, 2026-05-01 |
| Amazon CY2026 Capex Guidance | ~$200B | CY2026 | Amazon Q1 2026 Earnings, 2026-05-01 |
| Multi-year AWS Commitments | $225B+ | Announced | Amazon Q1 2026 Earnings, 2026-05-01 |

---

## Supply Chain Position

Trainium and Inferentia chips are designed at AWS (Annapurna Labs, Cupertino CA) and manufactured at TSMC (N4/N3 nodes for current generation). HBM for Trainium is sourced from SK Hynix and Micron. AWS deploys Trainium clusters in its own data centers and offers access via Amazon EC2 Trn1/Trn1n instances and Amazon Bedrock (for AI services). AWS simultaneously remains one of the largest NVIDIA GPU cloud operators.

**Key customers (publicly stated):** Internal (Amazon search, Alexa, Rufus AI); external via EC2 Trn1 (Anthropic, Samsung, others publicly stated as Bedrock users)  
**Key suppliers (publicly stated):** TSMC (fabrication), SK Hynix / Micron (HBM), Marvell / Broadcom (networking ASICs)

**Source:** Amazon Q1 2026 Earnings, 2026-05-01; AWS re:Invent 2024; Anthropic partnership announcement

---

## Technology Roadmap

| Milestone | Timeline | Status | Source |
|---|---|---|---|
| Trainium (1st gen, 7nm) | 2021 | Legacy / succeeded | AWS re:Invent 2021 |
| Inferentia2 (4nm TSMC) | 2023 | Volume production | AWS re:Invent 2022 |
| Trainium2 (4nm TSMC) | 2024 | Volume production; 100K+ cluster | AWS re:Invent 2023 |
| Trainium2 UltraServer (64-chip) | 2024 | Production | AWS re:Invent 2024 |
| Trainium3 | 2025 | Early shipping (select customers) | Amazon Q1 2026 Earnings, 2026-05-01 |

---

## Competitive Position

| Competitor | Segment | Key Differentiator (stated by company or analyst) | Source |
|---|---|---|---|
| NVIDIA H100/B200 | AI training / inference | CUDA ecosystem; universal compatibility; AWS also offers H100 | NVIDIA Q1 FY2026 Earnings |
| Google TPU 8t/8i | Custom AI training | GCP-captive; Gemini optimized; Cloud backlog $462B | Google Q1 2026 Earnings |
| Microsoft Maia 200 | Custom AI inference | Azure-captive; OpenAI integration | Microsoft Q3 FY2026 Earnings |

---

## Updates

### Update: 2026-05-01 — Q1 2026: Capex $43.2B; Trainium3 shipping; $225B+ multi-year commitments

> Amazon Q1 2026 earnings (May 1, 2026): AWS revenue $29.3B (+17% YoY). Amazon capex $43.2B for the quarter, with CY2026 guidance ~$200B. CEO Andy Jassy confirmed Trainium3 is in early shipping and being sampled by select customers. AWS multi-year commitments exceed $225B, reflecting strong AI workload demand. Amazon cited both Trainium and NVIDIA GPU infrastructure as part of its AI compute strategy.

**Source:** Amazon Q1 2026 Earnings, 2026-05-01

#segment:asic #source-tier:A #signal-type:demand #company:amazon_trainium #date:2026-05-01 #importance:high #confidence:high

### Update: 2024 — Trainium2 100,000+ chip cluster demonstrated; world's largest single custom AI cluster

> At AWS re:Invent 2024, Amazon announced a 100,000+ Trainium2 chip cluster as one of the world's largest single-technology AI training clusters. The cluster uses Trainium2 UltraServer (64 chips per server) connected via AWS's custom EFA (Elastic Fabric Adapter) networking. Anthropic was cited as a customer using Trainium2 for Claude model training.

**Source:** AWS re:Invent 2024 (Adam Selipsky keynote, November 2024)

#segment:asic #source-tier:A #signal-type:supply #company:amazon_trainium #date:2024-11 #importance:high #confidence:high

---

## Open Questions

- [ ] Trainium3 specs — TFLOPS, HBM configuration, TSMC node?
- [ ] Trainium market share vs NVIDIA within AWS infrastructure — what % of AWS AI compute is custom silicon?
- [ ] Anthropic (Claude) training workload split between Trainium2 and NVIDIA GPUs?
- [ ] AWS Neuron SDK adoption — how many external customers are using Trainium vs staying on NVIDIA?
