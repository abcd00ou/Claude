# Broadcom — AI ASIC / Networking

**Segment:** network, asic  
**Company Slug:** broadcom  
**Last Updated:** 2025-06-05

---

## Overview

Broadcom is the world's largest networking semiconductor company and the leading provider of custom AI ASIC (XPU) services for hyperscalers. Its Tomahawk and Jericho switch ASICs dominate hyperscaler Ethernet fabric; its custom XPU programs (in partnership with Google and others) represent a major custom silicon revenue stream. Broadcom raised its long-term AI addressable market estimate to $60–90B by FY2027.

---

## Key Products

| Product | Category | AI Relevance |
|---|---|---|
| Tomahawk 5 (BCM56990) | Ethernet switch ASIC | 51.2 Tb/s; AI spine/leaf fabric |
| Jericho3-AI | Routing ASIC | AI cluster routing, congestion control |
| Custom XPU (Google TPU partner) | AI ASIC | Training + inference accelerator |
| Trident 5 | Ethernet switch | Mid-tier AI cluster |
| BCM87000 (Bailly) | 800G PAM4 DSP | Optical interface for AI cluster |

---

## Financial Profile

| Period | Revenue | AI Revenue | Source |
|---|---|---|---|
| Q2 FY2025 (ended May 2025) | $15.04B | $4.4B | Q2 FY2025 Earnings Call |
| Q1 FY2025 (ended Feb 2025) | $14.92B | $4.1B | Q1 FY2025 Earnings Call |
| Q4 FY2024 (ended Oct 2024) | $14.05B | $3.8B | Q4 FY2024 Earnings Call |
| Total Revenue | $23.89B | FY2020 | MacroTrends |
| Total Revenue | $27.45B | FY2021 | MacroTrends |
| Total Revenue | $33.20B | FY2022 | MacroTrends |
| Total Revenue | $35.82B; semi ~$27.9B, infra software ~$7.9B | FY2023 | MacroTrends |
| Total Revenue | $51.574B (+44% YoY); AI revenue $12.2B (+220% YoY) | FY2024 | Broadcom FY2024 PR |
| Total Revenue | $63.887B (+24% YoY); AI semiconductor revenue growing | FY2025 | Broadcom FY2025 PR |
| AI Semiconductor Revenue | $8.4B (+106% YoY) | Q1 FY2026 | Broadcom Q1 FY2026 PR |

---

## Supply Chain Position

Broadcom is fabless; all advanced silicon at TSMC (Tomahawk 5 at N5; XPU at N3/N5). Broadcom's XPU programs include packaging with HBM at TSMC CoWoS in some configurations. Meta MTIA Gen 2 uses Broadcom as design partner (confirmed Q1 2026 Meta earnings).

---

## Technology Roadmap

| Product | Node | Status | Notes |
|---|---|---|---|
| Tomahawk 5 | TSMC N5 | Volume | 51.2 Tb/s; AI cluster standard |
| Tomahawk 6 | TSMC N3 | In development | 102+ Tb/s target |
| XPU (current gen) | TSMC N3 | Production | Hyperscaler AI workloads |
| Jericho3-AI | TSMC N5 | Volume | AI-specific routing features |

---

## Updates

### Update: 2022-08-16 — Tomahawk 5 ships: first 51.2 Tbps switch chip; 5nm, 256 ports × 200GbE

> Broadcom shipped Tomahawk 5 (BCM78900) on August 16, 2022 — the industry's first 51.2 Tbps switch chip. Tomahawk 5 is manufactured on 5nm process with 256 ports at 200GbE, enabling 400GbE and 800GbE Ethernet for AI cluster back-end networking. Broadcom Tomahawk series has been the dominant AI cluster networking chip, deployed across NVIDIA-based training clusters at hyperscalers.

**Source:** Broadcom Ships Tomahawk 5, Broadcom Investor Relations, 2022-08-16

#segment:network #source-tier:A #signal-type:roadmap #company:broadcom #date:2022-08-16 #importance:high #confidence:high

---

### Update: 2023-11-22 — VMware acquisition closes at $69B; software revenue transforms revenue mix

> Broadcom completed the acquisition of VMware on November 22, 2023 at an enterprise value of $69B ($61B cash+stock + ~$8B assumed debt). The acquisition was originally announced in May 2022 and faced an extended regulatory review. VMware contributes recurring infrastructure software revenue (virtualization, cloud management, networking security), transforming Broadcom from a chip-heavy to a software+chip business. FY2024 revenue: $51.574B (+44% YoY), with approximately $21B attributed to VMware contribution.

**Source:** Broadcom-VMware Close, BusinessWire via Broadcom PR, 2023-11-22; Broadcom FY2024 Earnings

#segment:network #source-tier:A #signal-type:corporate #company:broadcom #date:2023-11-22 #importance:high #confidence:high

---

### Update: 2025-06-03 — Tomahawk 6 ships: world's first 102.4 Tbps switch; 3nm chiplet TSMC

> Broadcom shipped Tomahawk 6 on June 3, 2025 — the world's first 102.4 Tbps switch chip (doubling Tomahawk 5). Built on TSMC 3nm chiplet architecture with up to 64 ports at 1.6T Ethernet. Tomahawk 6-Davisson (CPO variant) was announced October 8, 2025 as the industry's first 102.4 Tbps co-packaged optics switch. Broadcom AI switch backlog exceeded $10B in Q1 FY2026. AI semiconductor revenue: $8.4B (+106% YoY) in Q1 FY2026; guided at $10.7B (+140% YoY) for Q2 FY2026.

**Source:** Broadcom Ships Tomahawk 6, Broadcom Investor Relations, 2025-06-03; Broadcom Q1 FY2026 PR

#segment:network #source-tier:A #signal-type:roadmap #company:broadcom #date:2025-06-03 #importance:high #confidence:high

---

### Update: 2025-06-05 — Q2 FY2025: AI Revenue $4.4B (+46% YoY); TAM Raised to $60–90B

> "AI revenue was $4.4 billion in Q2 FY2025, growing 46% year-over-year. We are increasing our serviceable addressable market estimate for AI semiconductor opportunities to $60 to $90 billion by fiscal year 2027."
> — Broadcom CEO Hock Tan, Q2 FY2025 Earnings Call

**Source:** Broadcom Q2 FY2025 Earnings Call Transcript, Broadcom Investor Relations, 2025-06-05

#segment:network #segment:asic #source-tier:A #signal-type:demand #company:broadcom #date:2025-06-05 #importance:high #confidence:high

---

### Update: 2025-06-05 — Three XPU Hyperscaler Programs; Two New Ones in Development

> "We currently have three hyperscaler XPU customers in production and are developing next-generation programs with two additional hyperscalers who are qualifying our design services."
> — Broadcom CEO Hock Tan, Q2 FY2025 Earnings Call

**Source:** Broadcom Q2 FY2025 Earnings Call Transcript, Broadcom Investor Relations, 2025-06-05

#segment:asic #source-tier:A #signal-type:design-win #company:broadcom #date:2025-06-05 #importance:high #confidence:high #cross-ref:asic

---

### Update: 2025-06-05 — Networking Revenue $4.0B; Tomahawk 5 in Volume at Multiple Hyperscalers

> "Infrastructure software revenue was $6.0 billion, semiconductor revenue was $9.0 billion. Within semiconductors, networking was approximately $4.0 billion, driven by Tomahawk 5 volume deployments at multiple hyperscalers."
> — Broadcom CFO, Q2 FY2025 Earnings Call

**Source:** Broadcom Q2 FY2025 Earnings Call Transcript, Broadcom Investor Relations, 2025-06-05

#segment:network #source-tier:A #signal-type:demand #company:broadcom #date:2025-06-05 #importance:high #confidence:high

---

### Update: 2025-03-06 — Q1 FY2025: AI Revenue $4.1B; 27% of Total Revenue

> "AI revenue for fiscal Q1 was $4.1 billion, representing 27% of total revenue and growing 77% year-over-year."
> — Broadcom CEO Hock Tan, Q1 FY2025 Earnings Call

**Source:** Broadcom Q1 FY2025 Earnings Call Transcript, Broadcom Investor Relations, 2025-03-06

#segment:network #source-tier:A #signal-type:demand #company:broadcom #date:2025-03-06 #importance:high #confidence:high

---

### Update: 2026-03-12 — Tomahawk 6 volume production shipping; Jericho4 shipping since August 2025

> Broadcom Tomahawk 6 (102.4 Tbps, TSMC N3 chiplet) entered volume production shipping on March 12, 2026 per Broadcom IR announcement. Initial engineering samples had shipped in October 2025 (Edgecore/Accton demonstrated at OCP Global Summit). Tomahawk 6 doubles Tomahawk 5 bandwidth (51.2 Tbps → 102.4 Tbps) with up to 64 ports at 1.6 Tbps Ethernet. Jericho4 (distributed AI routing across data centers) began shipping in August 2025. Broadcom AI switch backlog exceeded $10B in Q1 FY2026. Q1 FY2026 AI semiconductor revenue: $8.4B (+106% YoY); Q2 FY2026 AI guidance: $10.7B (+27% sequential).

**Source:** Broadcom IR, 2026-03-12; Data Center Dynamics; Broadcom Q1 FY2026 PR

#segment:network #source-tier:A #signal-type:roadmap #company:broadcom #date:2026-03-12 #importance:high #confidence:high #cross-ref:chip_maker

---

## Open Questions

- [ ] Which two additional hyperscalers are qualifying Broadcom XPU design services?
- [x] Tomahawk 6 tape-out timeline and first customer production? — Volume shipping began March 12, 2026; initial samples October 2025
- [ ] Meta MTIA Gen 2 revenue contribution — how large as % of XPU revenue?
