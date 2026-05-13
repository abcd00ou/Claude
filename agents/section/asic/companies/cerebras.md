# Cerebras Systems — Company Intelligence

**Segment(s):** asic  
**Role in AI SCM:** Builds wafer-scale AI accelerators (WSE-3 — 4 trillion transistors, 900K AI cores on a single 300mm wafer); primary customers G42 (UAE) and Mohamed bin Zayed University of AI; Vicor 48V D2C power design win.  
**HQ:** Sunnyvale, CA, USA  
**Ticker:** Private (Nasdaq IPO filing, 2026-04)  
**Last Updated:** 2026-05-13

---

## Company Overview

Cerebras Systems designs wafer-scale AI accelerators where a single die spans an entire 300mm CMOS wafer — the WSE-3 has 4 trillion transistors and 900,000 AI cores. The CS-3 system uses the WSE-3 and is manufactured by TSMC (5nm). Primary customers are UAE-based: Mohamed bin Zayed University of AI (62% of FY2025 revenue) and G42 (24% of FY2025 revenue). Cerebras filed for a Nasdaq IPO in April 2026 at a reported $23B valuation and disclosed FY2025 revenue of $510M. Cerebras and G42 completed Condor Galaxy 3 (4 exaFLOPs) and announced an 8 exaFLOP deployment in India.

**Source:** IPO filing coverage, TechCrunch / trade press, 2026-04, https://tech-insider.org/cerebras-ipo-filing-510m-revenue-openai-deal-23b-valuation-2026/

---

## Key Products & AI Relevance

| Product / Technology | AI Use Case | Market Position |
|---|---|---|
| CS-3 (WSE-3 wafer-scale engine) | Large-model AI training and inference at 125 PFLOPS claimed | Niche leader in wafer-scale; not suitable for all workloads |
| Condor Galaxy supercomputers (CG1–CG3) | Government and research AI training infrastructure | Multi-exaFLOP clusters (G42 deployments) |
| MemoryX / SwarmX interconnect | Extended memory and multi-node scaling | Cerebras proprietary |

**Source:** Cerebras corporate disclosures; IPO filing, 2026-04

---

## Key Specs (WSE-3 / CS-3)

| Spec | Value | Source |
|---|---|---|
| Process | TSMC 5nm | Cerebras corporate disclosures |
| Die size | Full 300mm wafer | Cerebras corporate |
| Transistors | 4 trillion | Cerebras corporate |
| AI cores | 900,000 | Cerebras corporate |
| Peak performance (claimed) | 125 PFLOPS | Cerebras corporate |
| System power | 23 kW per CS-3 system | Cerebras corporate |

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
| Revenue | $510M | FY2025 | IPO filing, 2026-04 |
| Customer concentration — Mohamed bin Zayed Univ. AI | 62% of FY2025 revenue | FY2025 | IPO filing |
| Customer concentration — G42 | 24% of FY2025 revenue | FY2025 | IPO filing |
| Reported IPO valuation | ~$23B | 2026-04 | TechCrunch |
| Condor Galaxy 3 scale | 64 × CS-3 systems, 4 exaFLOPs | 2026-02 | Cerebras press release |

---

## Supply Chain Position

Cerebras WSE-3 is manufactured exclusively by TSMC (5nm, full wafer die on 300mm). The CS-3 system uses Vicor 48V direct-to-chip power components. Cerebras does not use HBM — the WSE-3 integrates 44 GB of on-chip SRAM. Extended memory (beyond on-chip) uses proprietary MemoryX external DRAM boards. Heavy concentration of deployments in UAE (G42 ecosystem) represents a geographic supply chain risk.

**Key customers (publicly stated):** Mohamed bin Zayed University of AI (62% of FY2025 rev), G42 (24% of FY2025 rev), Saudi Arabia (limited via HUMAIN), India (new 8 exaFLOP announced)  
**Key suppliers (publicly stated):** TSMC (5nm, sole foundry for WSE-3), Vicor (48V D2C power components)

**Source:** Cerebras IPO filing, 2026-04; Vicor Q1 2026 earnings

---

## Technology Roadmap

| Milestone | Timeline | Status | Source |
|---|---|---|---|
| CS-3 / WSE-3 (TSMC 5nm) general availability | 2024 | Available | Cerebras corporate |
| Condor Galaxy 3 (64 × CS-3, 4 exaFLOPs) at G42 Abu Dhabi | 2026-02 | Completed | Cerebras press release |
| 8 exaFLOP deployment — India | 2026-02 (announced) | Announced / in progress | Cerebras press release |
| Nasdaq IPO filing | 2026-04 | Filed | TechCrunch, 2026-04 |
| WSE-4 (next generation) | Not publicly announced | — | — |

---

## Competitive Position

| Competitor | Segment | Key Differentiator | Source |
|---|---|---|---|
| NVIDIA GB300 NVL72 | GPU cluster | 72 GPUs, 92.1 ExaFLOPS FP4 per cluster; ecosystem dominant | Microsoft Azure Blog, 2026-02 |
| Google Ironwood | Internal ASIC | 4.6 PFLOPS/chip; 9,216-chip superpod = 42.5 ExaFLOPS | Google Cloud Blog, 2026-04 |
| Groq LPU | LPU inference | Licensed to NVIDIA Dec 2025; GroqCloud still operating | Sacra, 2025-12 |
| Tenstorrent Galaxy Blackhole | RISC-V accelerator | 23 PFLOPS FP8 per system, $110K; scales to 4,000+ chips | The Register, 2026-04-28 |

---

## Updates

### Update: 2026-04 — Cerebras files Nasdaq IPO at ~$23B valuation; FY2025 revenue $510M; UAE concentration risk

> Cerebras filed for Nasdaq IPO. Reported FY2025 revenue of $510M per IPO filing: 62% from Mohamed bin Zayed University of AI (UAE), 24% from G42.

**Source:** IPO filing coverage, TechCrunch / trade press, 2026-04, https://tech-insider.org/cerebras-ipo-filing-510m-revenue-openai-deal-23b-valuation-2026/

#segment:asic #source-tier:B #signal-type:earnings #company:cerebras #date:2026-04 #importance:high #confidence:medium #cross-ref:end_market

---

### Update: 2026-02 — G42 and Cerebras deploy 4 exaFLOP Condor Galaxy 3 (64 × CS-3); 8 exaFLOP India deployment announced

> G42 and Cerebras completed Condor Galaxy 3 — 64 × CS-3 systems delivering 4 exaFLOPs; 8 exaFLOP target underway. February 2026: G42 + Cerebras announced 8 exaFLOP deployment in India.

**Source:** Cerebras Press Release, 2026-02, https://www.cerebras.ai/press-release/cerebras-and-g42-complete-4-exaflop-ai-supercomputer-and-start-the-march-towards-8-exaflops

#segment:asic #source-tier:A #signal-type:demand #company:cerebras #date:2026-02 #importance:high #confidence:high #cross-ref:end_market

---

## Open Questions

- [ ] Has Cerebras secured any U.S. hyperscaler (AWS, Azure, GCP) customer relationship?
- [ ] What is Cerebras' WSE-4 process node and timeline?
- [ ] Will the Nasdaq IPO proceed and at what final valuation?
- [ ] How does Cerebras' UAE customer concentration affect post-IPO risk profile?
