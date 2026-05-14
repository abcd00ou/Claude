# AMD (Advanced Micro Devices)

**Segment(s):** chip_maker  
**Role in AI SCM:** Primary NVIDIA alternative for AI accelerators; EPYC CPU for AI servers; Instinct GPU series; OpenAI and Meta committed as 6 GW customers  
**HQ:** Santa Clara, California, USA  
**Ticker:** NASDAQ:AMD  
**Last Updated:** 2026-05-05

---

## Company Overview

AMD is the most credible alternative to NVIDIA in AI accelerators. Its Instinct GPU series (MI300X → MI350 → MI450) targets both training and inference workloads. In Q1 2026, AMD Data Center revenue reached $5.8 billion (+57% YoY). Two landmark partnerships were disclosed: OpenAI and Meta each committed to deploying up to 6 gigawatts of AMD Instinct GPUs. AMD is collaborating with Samsung on HBM4 supply for AMD Instinct MI455X GPUs.

**Source:** AMD Q1 2026 Earnings Press Release, ir.amd.com, 2026-05-05; AMD 10-K FY2025 (accession 0000002488-26-000018), SEC, 2026-02-04

---

## Key Products & AI Relevance

| Product / Technology | AI Use Case | Status |
|---|---|---|
| Instinct MI300X | AI inference; ~30% better price-perf than comparable GPU | Volume production |
| Instinct MI350 | AI training and inference | Ramping |
| Instinct MI450 | AI training; "custom AMD Instinct MI450-based GPU" for Meta/OpenAI | Ramping 2026 |
| Instinct MI455X | AI training; paired with Samsung HBM4 | In development |
| Helios (platform) | Next-gen AI platform with MI450 | Customer engagement strengthening |
| EPYC CPU (server) | AI inference server CPU; +57% YoY DC revenue | Volume production |
| ROCm platform | AI software / CUDA alternative | Improving; no quantitative metric disclosed in 10-K |

**Source:** AMD Q1 2026 Earnings Press Release, 2026-05-05; AMD 10-K FY2025, 2026-02-04

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
| Total Revenue | $10.3B (+38% YoY) | Q1 2026 | AMD Q1 2026 Earnings Press Release, 2026-05-05 |
| Data Center Revenue | $5.8B (+57% YoY) | Q1 2026 | AMD Q1 2026 Earnings Press Release, 2026-05-05 |
| Q2 2026 Revenue Guidance | ~$11.2B ±$300M (+46% YoY est.) | Q2 2026 | AMD Q1 2026 Earnings Press Release, 2026-05-05 |
| Q2 2026 Non-GAAP Gross Margin | ~56% | Q2 2026 | AMD Q1 2026 Earnings Press Release, 2026-05-05 |
| Total Revenue | $34.64B (+34% YoY) | FY2025 | AMD Q4 FY2025 PR |
| Data Center Revenue | $16.6B (+32% YoY) | FY2025 | AMD Q4 FY2025 PR |
| Total Revenue | $25.78B | FY2024 | AMD 10-K FY2024 |
| Data Center Revenue | $12.6B (~2× YoY) | FY2024 | AMD 10-K FY2024 |
| Total Revenue | $22.68B (-4% YoY) | FY2023 | AMD Q4 FY2023 PR |
| Data Center Revenue | $6.50B (+7% YoY) | FY2023 | AMD Q4 FY2023 PR |
| Total Revenue | $23.60B | FY2022 | AMD SEC 10-K |
| Data Center Revenue | $6.04B | FY2022 | AMD SEC 10-K |
| Total Revenue | $16.43B | FY2021 | AMD SEC filing |
| Data Center Revenue (approx) | ~$4.1B | FY2021 | AMD earnings |
| Total Revenue | $9.76B | FY2020 | AMD SEC filing |

---

## Supply Chain Position

AMD designs chips and sources manufacturing from TSMC. Its Instinct GPUs use HBM (Samsung HBM4 confirmed for MI455X). AMD is also a large buyer of TSMC CoWoS packaging capacity.

**Key customers (publicly stated):** OpenAI (6 GW MI450 commitment), Meta (up to 6 GW MI450 commitment)  
**Key suppliers (publicly stated):** Samsung (HBM4 for MI455X, confirmed in Q1 2026 press release), TSMC (implied foundry)

**Source:** AMD Q1 2026 Earnings Press Release, 2026-05-05; AMD 10-K FY2025, SEC, 2026-02-04

---

## Technology Roadmap

| Milestone | Timeline | Status | Source |
|---|---|---|---|
| MI300X | In volume | Largely deployed | AMD Q1 2026 Earnings Press Release, 2026-05-05 |
| MI350 | Ramping | In production | AMD Q1 2026 Earnings Press Release, 2026-05-05 |
| MI450 (custom for Meta/OpenAI) | Ramping 2026 | Customer forecasts "exceeding initial expectations" | AMD Q1 2026 Earnings Press Release, 2026-05-05 |
| MI455X + Samsung HBM4 | In development | Collaboration announced | AMD Q1 2026 Earnings Press Release, 2026-05-05 |
| Helios platform | 2026–2027 | Customer engagement strengthening | AMD Q1 2026 Earnings Press Release, 2026-05-05 |

---

## Updates

### Update: 2026-02 — Meta commits to deploy up to 6 GW of AMD GPUs; 160M share warrant issued

> AMD and Meta Platforms amended a master purchase agreement in February 2026 under which Meta committed to deploy up to 6 gigawatts of AMD GPU-based AI infrastructure, with the first 1 GW powered by MI450-based Helios systems with 6th Gen EPYC CPUs. AMD issued Meta a warrant to purchase up to 160 million shares at $0.01/share, vesting based on AMD Instinct GPU purchase milestones and AMD stock price targets, exercisable through February 23, 2031. AMD Q1 CY2026 Data Center revenue: $5.8B (+57% YoY); total revenue $10.30B (+38% YoY).

**Source:** AMD Reports First Quarter 2026 Financial Results, AMD Investor Relations, 2026-04; AMD Q1 2026 Press Release

#segment:chip_maker #source-tier:A #signal-type:design-win #company:amd #date:2026-02 #importance:high #confidence:high

---

### Update: 2023-12 — MI300X (CDNA3) launches; 192GB HBM3 sets new AI memory benchmark

> AMD launched the Instinct MI300X GPU accelerator in December 2023 at the CDNA3 architecture event. The MI300X features 192GB HBM3 memory — the largest memory capacity of any AI GPU at launch — with 5.3 TB/s bandwidth and peak 1.3 PFLOPS FP8 performance on a single chip. Design wins followed at Meta Platforms, Microsoft Azure (for inferencing), and Oracle Cloud. MI300X became AMD's first meaningful AI accelerator revenue generator, contributing to FY2024 Data Center revenue of $12.6B (nearly double FY2023). AMD FY2024 total revenue: $25.78B.

**Source:** AMD Instinct MI300X Launch, AMD IR, 2023-12; AMD Q4 FY2024 Press Release, 2024

#segment:chip_maker #source-tier:A #signal-type:product-launch #company:amd #date:2023-12 #importance:high #confidence:high

---

### Update: 2022-05 — Pensando acquisition closes at $1.9B; AMD adds DPU/SmartNIC capability

> AMD closed the acquisition of Pensando Systems for approximately $1.9 billion in May 2022. Pensando provides DPU (Data Processing Unit) and SmartNIC technology for data center networking offload. The Pensando Elba chip became AMD's Pensando DPU lineup, enabling programmable networking acceleration for cloud providers. This acquisition was later used as the basis for the AMD Pensando product line serving hyperscalers.

**Source:** AMD $1.9B Acquisition of Pensando Closes, Data Center Dynamics, 2022-05

#segment:chip_maker #source-tier:A #signal-type:acquisition #company:amd #date:2022-05 #importance:high #confidence:high

---

### Update: 2022-02-14 — Xilinx acquisition closes at ~$49B; AMD adds FPGAs and adaptive SoCs

> AMD completed acquisition of Xilinx Corporation on February 14, 2022 for approximately $49 billion in an all-stock transaction. Xilinx added FPGAs and adaptive SoCs to AMD's portfolio, enabling AMD to serve AI inference at the edge and in data centers via FPGA-based acceleration. FY2022 Data Center segment revenue: $6.04B (includes first full year of Xilinx contribution). AMD FY2022 total revenue: $23.60B.

**Source:** AMD Xilinx Acquisition Complete, AMD Corporate Press Release, 2022-02-14

#segment:chip_maker #source-tier:A #signal-type:acquisition #company:amd #date:2022-02-14 #importance:high #confidence:high

---

### Update: 2026-05-05 — Q1 2026: DC revenue $5.8B (+57% YoY); Q2 guided $11.2B total; MI450 demand exceeding expectations

> Dr. Lisa Su, Chair and CEO: "We delivered an outstanding first quarter, driven by accelerating demand for AI infrastructure, with Data Center now the primary driver of our revenue and earnings growth... Customer engagement around MI450 Series and Helios is strengthening, with leading customer forecasts exceeding our initial expectations and a growing pipeline of large-scale deployments providing us with increasing visibility into our growth trajectory."

**Source:** AMD Q1 2026 Earnings Press Release, ir.amd.com, 2026-05-05

#segment:chip_maker #source-tier:A #signal-type:demand #company:amd #date:2026-05-05 #importance:high #confidence:high

---

### Update: 2026-05-05 — Meta commits up to 6 GW AMD Instinct; OpenAI commits 6 GW MI450

> "Meta and AMD announced plans to deploy up to 6 gigawatts of AMD Instinct GPUs, with the first 1-GW to be powered by a custom AMD Instinct MI450-based GPU."
> AMD 10-K FY2025 (filed Feb 2026): "In October 2025, we entered into a product purchase agreement with OpenAI OpCo, LLC, to deploy 6 gigawatts of AMD GPUs, with the deployment of the first gigawatt of capacity powered by our AMD Instinct MI450 series products."

**Source:** AMD Q1 2026 Earnings Press Release, ir.amd.com, 2026-05-05; AMD 10-K FY2025 (accession 0000002488-26-000018), SEC, 2026-02-04

#segment:chip_maker #source-tier:A #signal-type:design-win #company:amd #date:2026-05-05 #importance:high #confidence:high #cross-ref:end_market #cross-ref:asic

---

### Update: 2026-05-05 — AMD + Samsung: HBM4 supply for AMD Instinct MI455X confirmed

> "AMD and Samsung are collaborating on next-generation AI memory and compute technologies, including HBM4 supply for AMD Instinct MI455X GPUs."

**Source:** AMD Q1 2026 Earnings Press Release, ir.amd.com, 2026-05-05

#segment:chip_maker #source-tier:A #signal-type:supply #company:amd #date:2026-05-05 #importance:high #confidence:high #cross-ref:dram

---

## Open Questions

- [ ] MI450 custom specs for Meta vs. OpenAI — same chip or differentiated designs?
- [ ] Helios platform architecture — publicly disclosed?
- [ ] AMD CoWoS capacity allocation at TSMC — competing with NVIDIA for same packaging line?
