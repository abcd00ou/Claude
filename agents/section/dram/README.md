# DRAM Expert Agent

**Segment:** DRAM / Memory  
**Sales Lens:** AI training & inference memory demand, HBM allocation, DDR5 ramp  
**Last Updated:** 2026-05-12

---

## Overview

DRAM is the most supply-constrained memory type for AI workloads in 2025–2026. HBM (High Bandwidth Memory) is a specialized DRAM variant stacked directly on AI accelerators via advanced packaging. Standard DDR5 serves CPU-side AI inference and general server memory. Three suppliers — SK Hynix, Samsung, Micron — control 100% of HBM production. As of Q1 2026, all three have confirmed their entire CY2026 HBM supply is fully committed.

---

## How DRAM Works

### 2020 — JEDEC DDR5 Standard Published

> "DDR5 doubles the bandwidth of DDR4 (6400 MT/s vs 3200 MT/s) and increases bank group counts for AI inference workload parallelism."

**Source:** JEDEC JESD79-5 Standard, JEDEC Solid State Technology Association, 2020

#segment:dram #source-tier:S #signal-type:roadmap #date:2020 #importance:medium #confidence:high

---

### 2013 — HBM Architecture Concept Introduced

> "High Bandwidth Memory stacks DRAM dies vertically using through-silicon vias (TSVs), enabling bandwidth of 128 GB/s per stack — 4× conventional DDR3."

**Source:** "A 1.2V 8Gb 8-channel 128GB/s High-Bandwidth Memory (HBM) DRAM," IEEE ISSCC 2014, SK Hynix / AMD, 2014-02

#segment:dram #source-tier:S #signal-type:roadmap #date:2013 #importance:high #confidence:high

---

### 1966 — DRAM Cell Invented

> "The single-transistor, single-capacitor DRAM cell was invented by Robert Dennard at IBM, enabling high-density volatile memory."

**Source:** "Field-Effect Transistor Memory," US Patent 3,387,286, Robert Dennard / IBM, 1968-06-04

#segment:dram #source-tier:S #signal-type:roadmap #date:1966 #importance:low #confidence:high

---

## History

### 2026-Q1 — HBM4 Enters Mass Production; All 3 Suppliers Confirm 2026 Sold Out

> SK Hynix: "HBM4 is now in mass production." Micron: "Entire calendar 2026 HBM supply, including HBM4, is fully committed." Samsung: "All HBM capacity for calendar 2026 is sold out."

**Source:** SK Hynix Q1 2026 Earnings Call, 2026-04-23; Micron FQ2 2026 Earnings Call, 2026-03-18; Samsung Q1 2026 Earnings Call, 2026-04-30

#segment:dram #source-tier:A #signal-type:supply #company:sk-hynix #company:micron #company:samsung #date:2026-04-30 #importance:high #confidence:high

---

### 2024 — HBM3E Ramps; SK Hynix Sole Supplier to NVIDIA for H200/B200

> SK Hynix was the sole qualified HBM3E supplier for NVIDIA's H200 and Blackwell B200 through most of 2024. Samsung HBM3E qualification delayed.

**Source:** Multiple earnings call transcripts, 2024; TF International Securities DRAM Outlook 2025, 2025-Q1

#segment:dram #source-tier:A #signal-type:supply #company:sk-hynix #company:nvidia #date:2024 #importance:high #confidence:high

---

### 2023 — Deepest DRAM Downcycle; All Suppliers Cut Capex

> DRAM prices fell 50–60% from peak; all major suppliers posted operating losses in H1 2023 and cut capex by 30–50% to accelerate supply correction.

**Source:** Micron FY2023 10-K, SEC EDGAR, 2023-10; SK Hynix FY2023 Annual Report, 2024-03

#segment:dram #source-tier:A #signal-type:pricing #date:2023 #importance:high #confidence:high

---

### 2021 — DDR5 First Shipments; AI Server Memory Transition Begins

> Intel Sapphire Rapids (Xeon 4th gen) introduced DDR5 support, triggering the first large-scale server DDR5 deployments in AI training racks.

**Source:** Intel Xeon Scalable 4th Gen Press Release, Intel Corporation, 2023-01-10

#segment:dram #source-tier:A #signal-type:roadmap #date:2021 #importance:medium #confidence:high

---

### 2015 — HBM1 First Commercial Deployment (AMD Fury X)

> AMD Radeon R9 Fury X was the first commercial GPU to use HBM1 (High Bandwidth Memory, 1st generation), manufactured by SK Hynix.

**Source:** AMD Radeon R9 Fury X Product Page, AMD Corporation, 2015-06

#segment:dram #source-tier:A #signal-type:roadmap #company:amd #company:sk-hynix #date:2015 #importance:low #confidence:high

---

## Supply Chain

### 2026-04-23 — SK Hynix: Customer Demand for Next 3 Years Exceeds Capacity

> "Customer demand for the next three years already exceeds our supply capacity. This is structural, not temporary."
> — SK Hynix CFO, Q1 2026 Earnings Call

**Source:** SK Hynix Q1 2026 Earnings Call Transcript, SK Hynix Investor Relations, 2026-04-23

#segment:dram #source-tier:A #signal-type:supply #company:sk-hynix #date:2026-04-23 #importance:high #confidence:high

---

### 2026-04-30 — Samsung Signs Multi-Year HBM Supply Contracts Through 2028

> "We have signed multi-year supply agreements with major AI customers extending into 2028 for both HBM3E and HBM4."
> — Samsung DS Division, Q1 2026 Earnings Call

**Source:** Samsung Q1 2026 Earnings Call Transcript, Samsung Investor Relations, 2026-04-30

#segment:dram #source-tier:A #signal-type:supply #company:samsung #date:2026-04-30 #importance:high #confidence:high

---

### 2026-03-18 — Micron: HBM Backend Packaging at Singapore Facility

> "Our HBM packaging operations are primarily in Singapore; we are expanding TSV and CoW capacity there to support HBM4 ramp."
> — Micron Technology, FQ2 2026 Earnings Call

**Source:** Micron FQ2 2026 Earnings Call Transcript, Micron Investor Relations, 2026-03-18

#segment:dram #source-tier:A #signal-type:supply #company:micron #date:2026-03-18 #importance:medium #confidence:high #cross-ref:foundry

---

### 2025 — CoWoS Packaging Remains Binding Constraint for HBM-on-GPU

> TSMC CoWoS-L is required to integrate HBM stacks onto GPU dies. Demand for CoWoS exceeds TSMC's capacity by an estimated 20–30% through 2026.

**Source:** TSMC FY2025 20-F Annual Report, SEC EDGAR, 2026-02; TSMC Q4 2025 Earnings Call, 2026-01-16

#segment:dram #source-tier:A #signal-type:supply #company:tsmc #date:2025 #importance:high #confidence:high #cross-ref:foundry

---

## Competition

### 2026-04-30 — HBM Market Share: SK Hynix ~57%, Samsung ~35%, Micron ~8%

> Samsung Q1 2026: HBM market share for 2025 approximately 35%. SK Hynix maintained dominant share. Micron: "We have captured approximately 8% of HBM revenue share in 2025."

**Source:** Samsung Q1 2026 Earnings Call, 2026-04-30; Micron FQ2 2026 Earnings Call, 2026-03-18

#segment:dram #source-tier:A #signal-type:supply #date:2026-04-30 #importance:high #confidence:high

---

### 2026-04-30 — AMD Selects Samsung HBM4 for MI455X

> "AMD and Samsung have confirmed a collaboration on HBM4 supply for the MI455X accelerator."
> — Samsung DS Division, Q1 2026 Earnings Call

**Source:** Samsung Q1 2026 Earnings Call Transcript, Samsung Investor Relations, 2026-04-30

#segment:dram #source-tier:A #signal-type:design-win #company:samsung #company:amd #date:2026-04-30 #importance:high #confidence:high #cross-ref:chip_maker

---

### 2025 — HBM vs Conventional DRAM Profitability Divergence

> HBM3E ASP approximately $15–18/GB vs DDR5 $3–4/GB — a 4–5× premium. HBM gross margins estimated at 60–70% vs 30–40% for conventional DRAM.

**Source:** TF International Securities DRAM Report, TF International Securities, 2025-Q2

#segment:dram #source-tier:B #signal-type:pricing #date:2025 #importance:medium #confidence:medium

---

## Technology Roadmap

### 2027 — HBM4E Mass Production Target; All 3 Suppliers

> SK Hynix: HBM4E samples H2 2026 using 1Cnm node; mass production 2027. Samsung: HBM4E samples Q2 2026; mass production 2027. Micron: HBM4E roadmap confirmed for 2027.

**Source:** SK Hynix Q1 2026 Earnings Call, 2026-04-23; Samsung Q1 2026 Earnings Call, 2026-04-30; Micron FQ2 2026 Earnings Call, 2026-03-18

#segment:dram #source-tier:A #signal-type:roadmap #date:2026-04-30 #importance:high #confidence:high

---

### 2026 — HBM4 in Volume Production; Vera Rubin Demand Driver

> Micron: "HBM4 36GB 12-high is in volume shipments." NVIDIA Vera Rubin (H2 FY2027) is confirmed to use HBM4. SK Hynix: HBM4 mass production confirmed Q1 2026.

**Source:** Micron FQ2 2026 Earnings Call, 2026-03-18; NVIDIA FY2026 10-K, SEC EDGAR, 2026-02-26

#segment:dram #source-tier:A #signal-type:roadmap #company:micron #company:nvidia #date:2026-03-18 #importance:high #confidence:high #cross-ref:chip_maker

---

### 2026 — DDR6 Specification Finalized; AI Server Ramp Expected 2027

> JEDEC DDR6 specification finalized. First AI server deployments with DDR6 expected 2027, initially in inference configurations.

**Source:** JEDEC DDR6 Standard Publication, JEDEC, 2026

#segment:dram #source-tier:S #signal-type:roadmap #date:2026 #importance:medium #confidence:high

---

### 2022 — HBM3 First Deployment (SK Hynix / NVIDIA H100)

> SK Hynix shipped HBM3 for NVIDIA H100, delivering 819 GB/s per stack bandwidth — 2.3× HBM2e.

**Source:** SK Hynix HBM3 Product Announcement, SK Hynix, 2022-10; NVIDIA H100 Whitepaper, NVIDIA Corporation, 2022

#segment:dram #source-tier:A #signal-type:roadmap #company:sk-hynix #company:nvidia #date:2022 #importance:medium #confidence:high

---

## Pricing

### 2026-Q1 — DRAM Contract Pricing: Server +90–95% QoQ; HBM Premium Expands

> Samsung Q1 2026: "Server DRAM ASP increased approximately 90–95% quarter-over-quarter in Q1 2026." HBM pricing premium over conventional DRAM widened.

**Source:** Samsung Q1 2026 Earnings Call Transcript, Samsung Investor Relations, 2026-04-30

#segment:dram #source-tier:A #signal-type:pricing #company:samsung #date:2026-04-30 #importance:high #confidence:high

---

### 2026-Q1 — Micron: DRAM Revenue $18.8B (+207% YoY); Record Gross Margin 74.9%

> "DRAM revenue was $18.8 billion, up 207% year-over-year. Our gross margin of 74.9% represents a new company record, driven primarily by HBM and server DRAM mix."
> — Micron CFO, FQ2 2026 Earnings Call

**Source:** Micron FQ2 2026 Earnings Call Transcript, Micron Investor Relations, 2026-03-18

#segment:dram #source-tier:A #signal-type:pricing #company:micron #date:2026-03-18 #importance:high #confidence:high

---

### 2023 — DRAM Spot Pricing Trough; 50–60% Below Peak

> DRAM spot prices hit the lowest level since 2016 in mid-2023. DDR5 spot at $3.50/8Gb; compared to peak of $7.50 in 2022.

**Source:** DRAMeXchange / TrendForce Spot Price Data, TrendForce, 2023-Q2

#segment:dram #source-tier:B #signal-type:pricing #date:2023 #importance:medium #confidence:medium

---

## AI Demand Signals

### 2026-04-29 — Microsoft: Capacity Constrained; Adding 1 GW/Quarter of AI Compute

> "We are constrained on AI capacity despite adding approximately 1 gigawatt of compute per quarter. AI workloads are continuous, not batch — this drives sustained DRAM demand."
> — Microsoft CFO, Q3 FY2026 Earnings Call

**Source:** Microsoft Q3 FY2026 Earnings Call Transcript, Microsoft Investor Relations, 2026-04-29

#segment:dram #source-tier:A #signal-type:demand #company:microsoft #date:2026-04-29 #importance:high #confidence:high #cross-ref:end_market

---

### 2026-04-30 — Samsung: Agentic AI Driving HBM and Server DRAM Demand

> "Adoption of agentic AI drove further growth in relevant demands, mostly for HBM, server DRAM, and server SSD."
> — Samsung DS Division, Q1 2026 Earnings Call

**Source:** Samsung Q1 2026 Earnings Call Transcript, Samsung Investor Relations, 2026-04-30

#segment:dram #source-tier:A #signal-type:demand #company:samsung #date:2026-04-30 #importance:high #confidence:high

---

### 2026-04-30 — Samsung Forecasts 2027 HBM Shortage "More Severe Than 2026"

> "We believe the supply-demand imbalance for HBM in 2027 will be more severe than what we are experiencing in 2026."
> — Samsung DS Division, Q1 2026 Earnings Call

**Source:** Samsung Q1 2026 Earnings Call Transcript, Samsung Investor Relations, 2026-04-30

#segment:dram #source-tier:A #signal-type:supply #company:samsung #date:2026-04-30 #importance:high #confidence:high

---

### 2025 — NVIDIA GB200 NVL72: 576 HBM3E Stacks Per Rack

> Each GB200 NVL72 rack contains 72 GPUs, each requiring 8 HBM3E stacks × 36GB = ~20.7TB HBM per rack. This is a 4× increase in HBM content vs H100 NVL8 rack.

**Source:** NVIDIA GB200 NVL72 Technical Brief, NVIDIA Corporation, 2025; NVIDIA FY2026 10-K, SEC EDGAR, 2026-02-26

#segment:dram #source-tier:A #signal-type:demand #company:nvidia #date:2025 #importance:high #confidence:high #cross-ref:chip_maker

---

## Open Questions

- [ ] Vera Rubin HBM type and capacity per chip — not yet publicly disclosed (as of 2026-05-12)
- [ ] AMD MI450 HBM4 sourcing split between Samsung and SK Hynix — not confirmed
- [ ] LPDDR6 ramp timeline — which edge AI devices first?
- [ ] HBM allocation for hyperscaler custom ASICs (Google TPU 8, AWS Trainium3) — any public data?
