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
