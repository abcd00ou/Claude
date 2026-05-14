# Marvell Technology — Network / AI ASIC

**Segment:** network, asic  
**Company Slug:** marvell  
**Last Updated:** 2025-03-06

---

## Overview

Marvell Technology is a fabless semiconductor company that designs Ethernet switch ASICs, SerDes PHY, and custom AI silicon (XPU) for hyperscalers. It is the largest pure-play AI custom silicon design partner, serving at least three major hyperscalers with multi-generation ASIC programs. AI revenue surpassed $1B/quarter in Q4 FY2025 and is the primary growth driver.

---

## Key Products

| Product | Category | AI Relevance |
|---|---|---|
| Teralynx (switch ASIC) | Ethernet switching | Hyperscaler AI spine/leaf |
| OCTEON data processor | DPU/SmartNIC | AI cluster traffic offload |
| Custom XPU (unnamed) | AI ASIC | Hyperscaler inference/training |
| Alaska PHY | SerDes/optical | 800G optical interface for AI |

---

## Financial Profile

| Period | Revenue | AI Revenue | Source |
|---|---|---|---|
| Q4 FY2025 (ended Feb 2025) | $1.817B | ~$1.08B | Q4 FY2025 Earnings Call |
| Q3 FY2025 (ended Nov 2024) | $1.516B | ~$825M | Q3 FY2025 Earnings Call |
| Q2 FY2025 (ended Aug 2024) | $1.274B | ~$881M | Q2 FY2025 Earnings Call |
| Total Revenue | $2.70B | FY2020 (ended Feb 2020) | MacroTrends |
| Total Revenue | $2.97B (+10% YoY) | FY2021 | MacroTrends |
| Total Revenue | $4.46B (+50% YoY); Inphi first full year | FY2022 (ended Jan 2022) | StockAnalysis |
| Total Revenue | $5.92B (+33% YoY) | FY2023 | StockAnalysis |
| Total Revenue | $5.51B (-7% YoY); carrier downcycle | FY2024 | StockAnalysis |
| Total Revenue | $5.767B (+5% YoY) | FY2025 | StockAnalysis |
| Total Revenue | $8.195B (+42% YoY); DC revenue $6.10B | FY2026 (ended Feb 2026) | Marvell FY2026 PR |

---

## Supply Chain Position

Marvell is a fabless designer; all production at TSMC (N5, N3 nodes for advanced AI chips). Custom XPU programs use TSMC CoWoS for HBM integration in some configurations. Marvell's ASIC design services reduce hyperscaler NRE investment while sharing TSMC allocation risk.

---

## Technology Roadmap

| Generation | Node | Status | Notes |
|---|---|---|---|
| Current XPU gen | TSMC N5 | Volume | Hyperscaler inference at scale |
| Next XPU gen | TSMC N3 | In development | Higher bandwidth, lower power |
| Teralynx 10 | TSMC N5 | Sampling | 100Tb/s Ethernet switching |

---

## Updates

### Update: 2021-04-20 — Inphi acquisition closes at ~$10B; optical interconnect leadership established

> Marvell Technology completed the acquisition of Inphi Corporation on April 20, 2021 for approximately $10B in cash and stock. Inphi designs high-speed optical interconnect ICs for data center (PAM4 DSPs, coherent optics) and 5G applications. The Inphi acquisition gave Marvell technology leadership in 400G/800G optical transceivers and became the foundation for Marvell's CPO (co-packaged optics) strategy for AI datacenter networking.

**Source:** Marvell Completes Acquisition of Inphi, Marvell IR, 2021-04-20; CNBC, 2021-04-21

#segment:network #source-tier:A #signal-type:corporate #company:marvell #date:2021-04-20 #importance:high #confidence:high

---

### Update: 2025 — 18 active cloud custom silicon wins; $1.5B annual run rate; Amazon Trainium key customer

> Marvell Technology had 18 active cloud-provider custom silicon design wins as of 2025, with a custom silicon business at an approximately $1.5B annual revenue run rate. Key design partners include Amazon Web Services (AWS Trainium AI chip — Marvell's largest custom AI chip customer), Microsoft (Maia 100 AI accelerator on TSMC 3nm), Meta (DPU), and Google (Axion Arm-based CPU collaboration). FY2026 (ended Feb 2026) total revenue: $8.195B (+42% YoY); Data Center revenue: $6.10B (record, +46% YoY).

**Source:** TSPA Semiconductor analysis, 2025; HashRateIndex Hyperscaler ASIC report, 2025; Marvell FY2026 PR

#segment:network #segment:asic #source-tier:A #signal-type:design-win #company:marvell #date:2025 #importance:high #confidence:high

---

### Update: 2026-03-31 — NVIDIA invests $2B in Marvell; NVLink Fusion partnership for custom XPUs

> NVIDIA invested $2 billion in Marvell Technology on March 31, 2026 as part of the NVIDIA NVLink Fusion rack-scale platform partnership. Marvell will provide custom XPUs and NVLink Fusion-compatible scale-up networking, enabling hyperscalers to integrate NVIDIA interconnects into custom ASICs. Amazon Trainium 4 was confirmed as supporting NVLink Fusion protocol, making AWS one of the primary beneficiaries of the NVIDIA-Marvell partnership.

**Source:** NVIDIA AI Ecosystem Expands as Marvell Joins Forces through NVLink Fusion, NVIDIA Newsroom, 2026-03-31; Marvell IR, 2026-03-31

#segment:network #segment:asic #source-tier:A #signal-type:design-win #company:marvell #date:2026-03-31 #importance:high #confidence:high

---

### Update: 2025-03-06 — Q4 FY2025: AI Revenue $1.08B; FY2026 AI Guidance >$8B

> "AI revenue in Q4 was $1.08 billion, driven by ramp of our custom silicon programs and strong demand for our networking products. For fiscal year 2026, we now expect AI revenue to exceed $8 billion."
> — Marvell CEO, Q4 FY2025 Earnings Call

**Source:** Marvell Technology Q4 FY2025 Earnings Call Transcript, Marvell Investor Relations, 2025-03-06

#segment:network #segment:asic #source-tier:A #signal-type:demand #company:marvell #date:2025-03-06 #importance:high #confidence:high

---

### Update: 2025-03-06 — Three Hyperscaler XPU Programs Confirmed in Production

> "We are now in production with custom AI silicon programs at three hyperscaler customers. These programs are in their second or third generation with us, giving us deep integration into our customers' AI roadmaps."
> — Marvell CEO, Q4 FY2025 Earnings Call

**Source:** Marvell Technology Q4 FY2025 Earnings Call Transcript, Marvell Investor Relations, 2025-03-06

#segment:asic #source-tier:A #signal-type:design-win #company:marvell #date:2025-03-06 #importance:high #confidence:high #cross-ref:asic

---

### Update: 2025-03-06 — Data Center Revenue $1.37B; 75% of Total Revenue

> "Data center revenue was $1.37 billion in Q4 FY2025, representing approximately 75% of total company revenue and growing 78% year-over-year."
> — Marvell CFO, Q4 FY2025 Earnings Call

**Source:** Marvell Technology Q4 FY2025 Earnings Call Transcript, Marvell Investor Relations, 2025-03-06

#segment:network #source-tier:A #signal-type:demand #company:marvell #date:2025-03-06 #importance:high #confidence:high

---

## Open Questions

- [ ] Which three hyperscalers are confirmed XPU customers? (Amazon, Google, Microsoft implied but not named)
- [ ] Teralynx 10 production timeline and first customers?
- [ ] Marvell ASIC for 800G optical (CPO programs) — timeline?
