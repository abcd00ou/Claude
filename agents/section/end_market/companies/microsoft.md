# Microsoft

**Segment(s):** end_market, dc_infra  
**Role in AI SCM:** Largest single AI infrastructure investor; primary OpenAI compute partner; Azure cloud + Maia custom silicon  
**HQ:** Redmond, Washington, USA  
**Ticker:** NASDAQ:MSFT  
**Last Updated:** 2026-04-29

---

## Company Overview

Microsoft is the largest declared spender on AI infrastructure in 2026, with approximately $190 billion in capital expenditures planned for calendar year 2026. It is the exclusive cloud partner for OpenAI and operates Azure, one of the three leading hyperscaler platforms. Microsoft also develops its own Maia AI accelerator for inference workloads.

**Source:** Microsoft Q3 FY2026 Earnings Conference Call, Microsoft IR, 2026-04-29

---

## Key Products & AI Relevance

| Product / Technology | AI Use Case | Market Position |
|---|---|---|
| Azure AI (H100/B200 fleet) | AI training and inference for third-party customers | Leading cloud AI platform |
| Maia 200 | Internal inference; >30% improved tokens per dollar vs latest silicon | Deployed in own fleet |
| Azure OpenAI Service | GPT-4o, o-series model serving | Exclusive OpenAI cloud partner |
| Copilot (M365, GitHub, etc.) | Enterprise AI applications | Market leader in enterprise AI apps |

**Source:** Microsoft Q3 FY2026 Earnings Conference Call, Microsoft IR, 2026-04-29

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
| Q3 FY2026 Capex | $31.9B (+49% YoY) | Q3 FY2026 (Jan–Mar 2026) | Microsoft Q3 FY2026 Earnings Call, 2026-04-29 |
| CY2026 Capex Guidance | ~$190B | CY2026 full year | Microsoft Q3 FY2026 Earnings Call, CFO Amy Hood, 2026-04-29 |
| Component pricing impact on capex | ~$25B of the $190B | CY2026 | Microsoft Q3 FY2026 Earnings Call, CFO Amy Hood, 2026-04-29 |
| Short-lived asset % of capex | ~2/3 (GPUs, CPUs) | Q3 FY2026 | Microsoft Q3 FY2026 Earnings Call, 2026-04-29 |
| Capacity added Q3 FY2026 | +1 gigawatt | Q3 FY2026 | Microsoft Q3 FY2026 Earnings Call, CEO Satya Nadella, 2026-04-29 |

---

## Supply Chain Position

Microsoft is a direct customer of NVIDIA (Blackwell GPU fleet), AMD (CPUs and some GPU), and deploys its Maia 200 ASIC in Azure. It also procures storage (SSD, HDD) and networking equipment at hyperscaler scale.

**Key suppliers (publicly stated):** NVIDIA (Blackwell GPUs confirmed), AMD, and Maia 200 (internal ASIC via TSMC)  
**Key customers:** OpenAI (primary), enterprise Azure customers

**Source:** Microsoft Q3 FY2026 Earnings Conference Call, Microsoft IR, 2026-04-29

---

## Technology Roadmap

| Milestone | Timeline | Status | Source |
|---|---|---|---|
| Maia 200 deployment | Active in fleet | In production | Q3 FY2026 Earnings Call, 2026-04-29 |
| Doubling overall DC footprint | "Just two years" from ~2024 | On track | Q3 FY2026 Earnings Call, Nadella, 2026-04-29 |
| Fairwater DC (Wisconsin, NVIDIA Blackwell) | Came online 6 weeks early | Operational | Q3 FY2026 Earnings Call, 2026-04-29 |
| Constrained capacity through 2026 | Through end of CY2026 | Stated | Q3 FY2026 Earnings Call, CFO Hood, 2026-04-29 |

---

## Updates

### Update: 2026-04-29 — CY2026 capex ~$190B; adding 1 GW/quarter; capacity constrained through 2026

> CFO Amy Hood: "We expect CapEx spend to increase to over $40 billion as we continue to bring more capacity online... For calendar year 2026, we expect to invest roughly $190 billion in capital expenditures which includes approximately $25 billion from the impact of higher component pricing."
> CEO Satya Nadella: "All up, we added another gigawatt of capacity this quarter, and remain on track to double our overall footprint in just two years."
> CFO Hood: "we expect to remain constrained at least through 2026."

**Source:** Microsoft Q3 FY2026 Earnings Conference Call, Microsoft IR, 2026-04-29

#segment:end_market #source-tier:A #signal-type:capex #company:microsoft #date:2026-04-29 #importance:high #confidence:high #cross-ref:dc_infra

---

### Update: 2026-04-29 — Q3 FY2026: first GB300 NVL72 supercluster (4,608 GPUs / 92.1 ExaFLOPS); Azure AI ARR $37B +123% YoY; Azure +40% CC (5th consecutive quarter of acceleration)

> Microsoft launched the first GB300 NVL72 supercluster: 4,608 GB300 GPUs delivering 92.1 ExaFLOPS FP4, deployed for OpenAI training workloads (announced at NVIDIA GTC March 2026). Azure grew 40% constant currency in Q3 FY2026 — 5th consecutive quarter of acceleration. Annualized Azure AI revenue reached $37B (+123% YoY). CY2026 capex guidance ~$190B exceeded analyst consensus of $154.6B by ~$35B. Fairwater superfactories in Wisconsin and Atlanta designated for Vera Rubin architecture.

**Source:** Microsoft Q3 FY2026 Earnings Call, April 29 2026; NVIDIA Blog (GTC 2026); Data Center Dynamics

#segment:end_market #source-tier:A #signal-type:roadmap #company:microsoft #date:2026-04-29 #importance:high #confidence:high #cross-ref:chip_maker #cross-ref:dc_infra

---

### Update: 2026-04-29 — Maia 200 deployed: "over 30% improved tokens per dollar vs latest silicon"

> CEO Satya Nadella: "Our Maia 200 AI accelerator — which offers over 30% improved tokens per dollar, compared to the latest silicon in our fleet." Fairwater datacenter in Wisconsin came online six weeks ahead of schedule, housing hundreds of thousands of NVIDIA Blackwell GPUs.

**Source:** Microsoft Q3 FY2026 Earnings Conference Call, Microsoft IR, 2026-04-29

#segment:end_market #source-tier:A #signal-type:design-win #company:microsoft #date:2026-04-29 #importance:high #confidence:high #cross-ref:asic

---

## Open Questions

- [ ] Maia 200 fabricated at which TSMC node — N3? N5?
- [ ] What fraction of Azure AI workloads run on Maia 200 vs. NVIDIA Blackwell?
- [ ] Microsoft Q4 FY2026 capex trajectory — will $40B+ per quarter be sustained?
