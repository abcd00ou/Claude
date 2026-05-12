# Western Digital / SanDisk

**Segment(s):** storage  
**Role in AI SCM:** Major NAND producer via Kioxia JV (Yokkaichi + Kitakami fabs); NAND flash business spun off as independent SanDisk Corp (Feb 2025)  
**HQ:** United States (San Jose, CA)  
**Ticker:** NASDAQ:WDC (HDD); SanDisk: NASDAQ:SNDK (post-spin, Feb 2025)  
**Last Updated:** 2025-02-05

---

## Company Overview

Western Digital operated two major business lines — NAND flash and HDDs — before completing the spin-off of its NAND flash business as an independent company, SanDisk Corporation, in February 2025. The NAND business operates jointly with Kioxia via a shared fab agreement (BiCS technology) at Yokkaichi and Kitakami facilities in Japan. Post-spin, SanDisk controls approximately 13–15% of global NAND bits on its own, with additional output from the Kioxia JV. Enterprise SSDs (targeting AI hyperscaler storage workloads) are a key growth segment.

**Source:** Western Digital Q2 FY2025 Earnings, 2025-02-05; WD Separation Press Release, 2025-02-19

---

## Key Products & AI Relevance

| Product / Technology | AI Use Case | Market Position |
|---|---|---|
| BiCS 8 (218-layer QLC NAND) | AI training dataset storage, inference checkpointing | Volume production; co-developed with Kioxia |
| WD Gold Enterprise NVMe SSD | Hyperscaler AI storage tier | Qualifying at major hyperscalers |
| WD Ultrastar DC SS540 (SAS SSD) | AI warm storage | Enterprise production |
| HDD (WD Gold, WD Ultrastar) | AI cold storage / data lake | 26TB+ capacity point; HAMR roadmap |
| KV-SSD (key-value SSD) | Agentic AI KV cache | Kioxia JV collaboration; early development |

**Source:** WD Product Catalog 2024; Kioxia CD8P qualification announcement, 2024

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
| Total WD Revenue | $4.285B (+38% YoY) | Q2 FY2025 (Jan 2025) | WD Q2 FY2025 Earnings, 2025-02-05 |
| Flash (NAND) Revenue | ~$2.5B | Q2 FY2025 | WD Q2 FY2025 Earnings, 2025-02-05 |
| HDD Revenue | ~$1.8B | Q2 FY2025 | WD Q2 FY2025 Earnings, 2025-02-05 |
| Flash Gross Margin | ~35% (recovering) | Q2 FY2025 | WD Q2 FY2025 Earnings, 2025-02-05 |

---

## Supply Chain Position

Western Digital/SanDisk's NAND output is produced jointly with Kioxia at shared fabs using BiCS (Be-Inverse-Charge-Stacked) stacking technology. Combined, the WD-Kioxia JV represents the world's second-largest NAND manufacturer by bits. Post-spin, SanDisk sells NAND products independently while the Kioxia JV manufacturing relationship continues. Enterprise SSD customers include major hyperscalers (AWS, Azure, GCP — qualification status not publicly confirmed).

**Key customers (publicly stated):** Hyperscaler enterprise qualification (not named)  
**Key suppliers (publicly stated):** Kioxia (JV fab partner); ASML (EUV for advanced NAND); Applied Materials

**Source:** WD Q2 FY2025 Earnings, 2025-02-05; WD Annual Report FY2024

---

## Technology Roadmap

| Milestone | Timeline | Status | Source |
|---|---|---|---|
| BiCS 8 (218-layer QLC) | 2024 | Volume production | WD, 2024 |
| BiCS 9 (300+ layer) | 2025–2026 | Co-development with Kioxia | Kioxia/WD joint announcement, 2024 |
| PCIe Gen5 NVMe Enterprise SSD | 2025 | Qualification at hyperscalers | WD Product Roadmap, 2024 |
| SanDisk spin-off completion | 2025-02-19 | Completed | WD Press Release, 2025-02-19 |

---

## Competitive Position

| Competitor | Segment | Key Differentiator (stated by company or analyst) | Source |
|---|---|---|---|
| Samsung | NAND | ~31% bit share; full vertical integration; KV-SSD pioneer | Samsung Q1 2026 Earnings |
| Micron | NAND | Gen5 NVMe in qualification; 232-layer QLC ramp | Micron FQ2 2026 Earnings |
| SK Hynix / Solidigm | NAND | Enterprise SSD qualification at hyperscalers; Solidigm brand | Various, 2024 |

---

## Updates

### Update: 2025-02-19 — SanDisk spin-off completed; independent NAND company created

> Western Digital completed the separation of its NAND flash business as SanDisk Corporation on February 19, 2025. SanDisk began trading independently on NASDAQ (SNDK). The HDD business retained the Western Digital name and ticker (WDC). The Kioxia JV manufacturing agreement continues under SanDisk. SanDisk's flash bit share is approximately 13–15% of global NAND output.

**Source:** WD Separation Press Release, 2025-02-19

#segment:storage #source-tier:A #signal-type:supply #company:western_digital #date:2025-02-19 #importance:high #confidence:high

### Update: 2025-02-05 — Q2 FY2025: Revenue $4.285B (+38% YoY); NAND recovery confirmed

> WD Q2 FY2025 (quarter ended January 2025): total revenue $4.285B, up 38% YoY. Flash revenue ~$2.5B; HDD ~$1.8B. Flash gross margin recovered from 2023 trough levels. Enterprise SSD demand cited as strongest growth driver. Company reiterated spin-off timeline for February 2025.

**Source:** Western Digital Q2 FY2025 Earnings, 2025-02-05

#segment:storage #source-tier:A #signal-type:demand #company:western_digital #date:2025-02-05 #importance:medium #confidence:high

---

## Open Questions

- [ ] SanDisk (post-spin) enterprise SSD qualification status at AWS/Azure/GCP — confirmed?
- [ ] BiCS 9 production timeline relative to Samsung V9 and Micron 276-layer
- [ ] WD-Kioxia JV: will the manufacturing agreement be renegotiated post-spin?
- [ ] HDD role in AI storage: cold tier growth rate as AI dataset volumes scale
