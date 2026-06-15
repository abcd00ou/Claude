# DC Infrastructure Expert Agent

**Segment:** Data Center Infrastructure  
**Sales Lens:** Hyperscaler capex cycles, power/cooling constraints, AI cluster build-out  
**Last Updated:** 2026-05-12

---

## Overview

AI data centers operate at fundamentally different physical parameters than traditional cloud data centers: 100–200 kW/rack power density vs 10–15 kW for standard racks, mandatory liquid cooling for 400W+ GPU TDPs, and 18–36 month build timelines from land acquisition to live cluster. Combined CY2026 capex from four hyperscalers (Amazon, Microsoft, Alphabet, Meta) totals $705–725B. Power availability — not GPU supply — is now cited as the primary constraint for 2026 cluster deployments.

---

## How AI Data Centers Work

### 2025 — Direct Liquid Cooling (DLC) Becomes Mandatory for 400W+ GPU TDP

> "Direct liquid cooling routes chilled water through cold plates mounted directly on GPU and CPU heat spreaders, removing 80–90% of heat at the chip level. Required for NVIDIA B200 (700W TDP) and GB200 NVL72 (120 kW/rack)."

**Source:** ASHRAE TC 9.9 Data Center Thermal Guidelines 2025 Edition, ASHRAE, 2025

#segment:dc_infra #source-tier:S #signal-type:roadmap #date:2025 #importance:high #confidence:high

---

### 2022 — 48V Power Architecture Adopted for AI Server Racks

> "48V rack power distribution reduces copper bus losses by ~16× compared to 12V distribution at equivalent power levels. AI GPU racks require 48V to deliver 100+ kW without excessive cable gauge."

**Source:** Open Compute Project 48V Power Spec, OCP Foundation, 2022; NVIDIA DGX H100 Power Brief, NVIDIA, 2022

#segment:dc_infra #source-tier:A #signal-type:roadmap #date:2022 #importance:medium #confidence:high

---

## History

### 2026-Q1 — Alphabet Doubles Capex YoY to $35.7B; Guides 2027 Growth

> "Capital expenditures were $35.7 billion in Q1 2026, up 107% year-over-year. We expect capex to grow further in 2027 as AI infrastructure demand continues to increase."
> — Alphabet CFO, Q1 2026 Earnings Call

**Source:** Alphabet Q1 2026 Earnings Call Transcript, Alphabet Investor Relations, 2026-04-29

#segment:dc_infra #source-tier:A #signal-type:capex #company:google #date:2026-04-29 #importance:high #confidence:high #cross-ref:end_market

---

### 2026-Q1 — Amazon Q1 2026 Capex $43.2B; CY2026 Full-Year Guidance ~$200B

> "Capital expenditures were $43.2 billion in Q1 2026. Our full-year 2026 expectation remains approximately $200 billion, weighted toward AI infrastructure and AWS data center expansion."
> — Amazon CFO, Q1 2026 Earnings Call

**Source:** Amazon Q1 2026 Earnings Call Transcript, Amazon Investor Relations, 2026-05-01

#segment:dc_infra #source-tier:A #signal-type:capex #company:amazon #date:2026-05-01 #importance:high #confidence:high #cross-ref:end_market

---

### 2026-Q1 — Microsoft: Constrained Despite +1 GW/Quarter; $190B CY2026 Capex

> "We are adding approximately 1 gigawatt of compute capacity per quarter and remain supply-constrained despite this pace. AI workloads are continuous — not batch — driving persistent demand."
> — Microsoft CFO, Q3 FY2026 Earnings Call

**Source:** Microsoft Q3 FY2026 Earnings Call Transcript, Microsoft Investor Relations, 2026-04-29

#segment:dc_infra #source-tier:A #signal-type:capex #company:microsoft #date:2026-04-29 #importance:high #confidence:high #cross-ref:end_market

---

### 2026-Q1 — Meta Raises 2026 Capex Guidance to $125–145B (+$10B); Component Pricing Cited

> "We are raising our 2026 capital expenditure guidance to $125–145 billion from $115–135 billion. The increase reflects both expanded AI infrastructure plans and higher component pricing."
> — Meta CFO, Q1 2026 Earnings Call

**Source:** Meta Q1 2026 Earnings Call Transcript, Meta Investor Relations, 2026-04-29

#segment:dc_infra #source-tier:A #signal-type:capex #company:meta #date:2026-04-29 #importance:high #confidence:high #cross-ref:end_market

---

### 2025 — Microsoft Signs 10+ GW of Power Deals for AI Data Centers

> Microsoft signed power purchase agreements exceeding 10 gigawatts in 2024–2025 globally, including nuclear (Three Mile Island restart), natural gas, and renewable sources specifically for AI data centers.

**Source:** Microsoft FY2025 10-K, SEC EDGAR, 2025-07; Microsoft Press Release on Three Mile Island, 2023-09-20

#segment:dc_infra #source-tier:A #signal-type:capex #company:microsoft #date:2025 #importance:high #confidence:high

---

### 2023 — AI Rack Power Density Crosses 100 kW/Rack Threshold

> NVIDIA H100 DGX systems established 100 kW/rack as the new AI server standard, forcing wholesale infrastructure redesign at hyperscalers. Prior generation (A100): ~40–60 kW/rack.

**Source:** NVIDIA DGX H100 System Specifications, NVIDIA Corporation, 2023

#segment:dc_infra #source-tier:A #signal-type:roadmap #company:nvidia #date:2023 #importance:high #confidence:high

---

## Supply Chain

### 2026 — Power Transformers: 52–65 Week Lead Times; Critical Path Item

> Utility-scale power transformers required for AI data center substations have 52–65 week lead times as of 2026. Driven by simultaneous demand from AI data centers and US grid modernization.

**Source:** "Power Transformer Supply Chain Report," S&P Global Commodity Insights, 2025-Q4

#segment:dc_infra #source-tier:B #signal-type:supply #date:2025 #importance:high #confidence:medium

---

### 2025 — Liquid Cooling Unit Lead Times: 40–52 Weeks

> Direct liquid cooling (DLC) units and rear-door heat exchangers have 40–52 week lead times from Vertiv, Alfa Laval, and CoolIT. Skilled electrical engineering labor is a co-constraint.

**Source:** Vertiv FY2025 Earnings Call, Vertiv Investor Relations, 2026-02; industry supply chain data

#segment:dc_infra #source-tier:A #signal-type:supply #date:2025 #importance:high #confidence:high

---

### 2025 — Land with Power Access Fully Committed in Tier-1 Markets

> Premium data center land sites (proximity to hydro, nuclear, cheap grid) in Northern Virginia, Dublin, Singapore, and Tokyo are fully committed through 2027 by hyperscalers.

**Source:** CBRE Data Center Market Report Q4 2025, CBRE Research, 2026-01

#segment:dc_infra #source-tier:B #signal-type:supply #date:2025 #importance:high #confidence:medium

---

## Power & Cooling

### 2026 — GB200 NVL72 Rack: 120 kW Power Draw; Mandatory Liquid Cooling

> NVIDIA GB200 NVL72 rack-scale system: ~120 kW continuous power draw per rack. Requires direct liquid cooling; air cooling is physically impossible at this density. 400V 3-phase power delivery required.

**Source:** NVIDIA GB200 NVL72 System Technical Brief, NVIDIA Corporation, 2025

#segment:dc_infra #source-tier:A #signal-type:demand #company:nvidia #date:2025 #importance:high #confidence:high #cross-ref:power

---

### 2026 — Microsoft Three Mile Island Nuclear Restart: 835 MW for AI DCs

> Microsoft's agreement to restart Three Mile Island Unit 1 (835 MW) entered operation, providing carbon-free baseload power dedicated to Microsoft AI data centers in the Mid-Atlantic region.

**Source:** Microsoft Press Release, "Constellation Energy Restarts Three Mile Island," Microsoft Corporation, 2024-09-20; Operation update, 2026

#segment:dc_infra #source-tier:A #signal-type:capex #company:microsoft #date:2024-09-20 #importance:high #confidence:high

---

### 2028–2030 — Small Modular Reactors (SMR): Microsoft and Google Evaluating

> Microsoft and Google are evaluating SMR contracts as long-term power solutions for AI data centers. Commercial SMR availability estimated 2028–2030. Not a near-term solution.

**Source:** Microsoft FY2025 Sustainability Report, Microsoft, 2025; Google Clean Energy Report, Google, 2025

#segment:dc_infra #source-tier:A #signal-type:capex #date:2025 #importance:medium #confidence:high

---

## Capacity & Investment

### 2026 — Combined 4-Hyperscaler Q1 2026 Capex: ~$130.6B

> Q1 2026 actual capex: Amazon $43.2B, Microsoft $31.9B, Alphabet $35.7B, Meta $19.8B. Total: ~$130.6B in a single quarter. Annualized run rate implies $520B+ before guidance escalations.

**Source:** Amazon Q1 2026 Earnings Call, 2026-05-01; Microsoft Q3 FY2026 Earnings Call, 2026-04-29; Alphabet Q1 2026 Earnings Call, 2026-04-29; Meta Q1 2026 Earnings Call, 2026-04-29

#segment:dc_infra #source-tier:A #signal-type:capex #date:2026-05-01 #importance:high #confidence:high #cross-ref:end_market

---

### 2026 — Component Pricing Inflating Capex: Microsoft +$25B, Meta +$10B

> Microsoft raised CY2026 capex by ~$25B and Meta by +$10B, both citing "higher component pricing" as the primary driver. Cross-confirms memory/chip ASP increases reported by suppliers.

**Source:** Microsoft Q3 FY2026 Earnings Call, 2026-04-29; Meta Q1 2026 Earnings Call, 2026-04-29

#segment:dc_infra #source-tier:A #signal-type:pricing #date:2026-04-29 #importance:high #confidence:high #cross-ref:dram

---

## AI Demand Signals

### 2026-04-29 — Power = Primary Constraint for 2026 AI Cluster Deployments

> Multiple hyperscalers cited power availability — not GPU supply — as the binding constraint for new AI cluster deployments in 2026. Microsoft: "We are power-constrained in several regions."

**Source:** Microsoft Q3 FY2026 Earnings Call, 2026-04-29; Alphabet Q1 2026 Earnings Call, 2026-04-29

#segment:dc_infra #source-tier:A #signal-type:supply #date:2026-04-29 #importance:high #confidence:high

---

### 2025 — Neo-Cloud (CoreWeave, Lambda, Together) Building AI-First DCs

> CoreWeave (~100K H100 equivalent), Lambda Labs (~30K GPU), Oracle OCI (~60K H100 equiv.) are building purpose-built AI data centers with liquid cooling as baseline. Different procurement profile from hyperscalers.

**Source:** CoreWeave S-1 Filing, SEC EDGAR, 2025-Q1; Lambda Labs Growth Announcement, 2024

#segment:dc_infra #source-tier:A #signal-type:demand #date:2025 #importance:medium #confidence:high

---

## Open Questions

- [ ] Power transformer lead time trend: improving or worsening through 2026?
- [ ] Google DC build pace in 2026 — accelerating or digesting 2025 investments?
- [ ] HVDC power distribution adoption timeline in AI racks — which hyperscaler first?
- [ ] SMR commercial timeline: is 2028–2030 realistic given NRC licensing backlog?
