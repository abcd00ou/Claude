# Intel Foundry (IFS)

**Segment(s):** foundry  
**Role in AI SCM:** #3 foundry by revenue; 18A (1.8nm-class) in customer sampling; no confirmed AI GPU volume win  
**HQ:** United States  
**Ticker:** NASDAQ:INTC  
**Last Updated:** 2025-04-25

---

## Company Overview

Intel Foundry Services (IFS), rebranded Intel Foundry in 2024, is Intel's external contract manufacturing business built on Intel's leading-edge process nodes. Intel 18A (1.8nm-class, using RibbonFET GAA + PowerVia backside power delivery) entered customer sampling in early 2025. Despite technology claims, no major external AI GPU customer has confirmed volume production at Intel Foundry. Intel's own Clearwater Forest server CPU is the primary confirmed 18A product.

**Source:** Intel Q1 2025 Earnings, 2025-04-25; Intel Foundry Direct Connect 2024

---

## Key Products & AI Relevance

| Product / Technology | AI Use Case | Market Position |
|---|---|---|
| Intel 18A (RibbonFET + PowerVia) | Next-gen AI chip candidate | Sampling phase; no AI GPU win confirmed |
| Intel 3 (FinFET) | CPU, server compute | In volume production; limited AI chip customer |
| Intel 16 (FinFET) | Mature logic | Production; older-gen AI applications |
| EMIB (Embedded Multi-die Interconnect Bridge) | Chiplet integration | Intel proprietary; used for internal AI products (Ponte Vecchio) |
| Foveros (3D stacking) | Die stacking | Internal; limited external adoption |

**Source:** Intel Foundry Technology Roadmap 2024; Intel Q1 2025 Earnings, 2025-04-25

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
| Intel Foundry Revenue | ~$4.7B | Q1 2025 | Intel Q1 2025 Earnings, 2025-04-25 |
| Intel Foundry Operating Loss | ~-$2.3B | Q1 2025 | Intel Q1 2025 Earnings, 2025-04-25 |
| Total Intel Revenue | $12.7B (-1% YoY) | Q1 2025 | Intel Q1 2025 Earnings, 2025-04-25 |

---

## Supply Chain Position

Intel Foundry is vertically integrated — Intel designs, manufactures, and packages its own chips in-house. For external customers, Intel Foundry provides wafer fabrication on Intel process nodes. Microsoft has been confirmed as an 18A external customer (sampling/development). Intel Foundry uses ASML EUV scanners (same as TSMC and Samsung). Intel's advanced packaging (Foveros, EMIB) is done in-house at Oregon and Arizona facilities.

**Key customers (publicly stated):** Microsoft (18A development/sampling confirmed), AWS (exploratory; not confirmed volume)  
**Key suppliers (publicly stated):** ASML (High-NA EUV for 14A+), Applied Materials, Lam Research

**Source:** Intel Q1 2025 Earnings, 2025-04-25; Intel Foundry Direct Connect 2024

---

## Technology Roadmap

| Milestone | Timeline | Status | Source |
|---|---|---|---|
| Intel 3 (FinFET) | 2023–present | Volume production (internal) | Intel Q3 2023 Earnings |
| Intel 18A (RibbonFET + PowerVia) | H1 2025 | Customer sampling; yield improving | Intel Q1 2025 Earnings, 2025-04-25 |
| Clearwater Forest (first 18A product) | 2025 | Development / pre-production | Intel, 2025 |
| Intel 14A (High-NA EUV) | 2026+ | R&D / early planning | Intel Foundry Roadmap 2024 |
| Falcon Shores discrete GPU | Cancelled | Cancelled Jan 2024 | Intel, 2024-01 |

---

## Competitive Position

| Competitor | Segment | Key Differentiator (stated by company or analyst) | Source |
|---|---|---|---|
| TSMC | Foundry | N2/N3 in volume; CoWoS integrated; sole AI GPU fab | Multiple analyst reports, 2025 |
| Samsung Foundry | Foundry | SF3E/SF2 GAA competing; both in yield improvement phase vs TSMC | TechInsights, 2024-Q3 |

---

## Updates

### Update: 2025-04-25 — Q1 2025: Revenue $12.7B; Intel Foundry loss -$2.3B; 18A sampling only

> Intel Q1 2025 earnings (April 25, 2025): total revenue $12.7B (-1% YoY). Intel Foundry revenue ~$4.7B with operating loss of approximately -$2.3B. CEO Pat Gelsinger confirmed 18A customer sampling is progressing. Gaudi AI accelerator revenue was not separately disclosed. Falcon Shores discrete GPU was cancelled. No external AI GPU design win at Intel Foundry was announced.

**Source:** Intel Q1 2025 Earnings, 2025-04-25

#segment:foundry #source-tier:A #signal-type:supply #company:intel_foundry #date:2025-04-25 #importance:high #confidence:high

### Update: 2024-01 — Falcon Shores discrete GPU cancelled; Gaudi road narrows

> Intel cancelled Falcon Shores as a discrete GPU product. The Falcon Shores architecture will be retained only as an internal accelerator tile for Intel AI systems (not a standalone product). This eliminates Intel's competitive GPU offering against NVIDIA and AMD in the AI data center market.

**Source:** Intel, January 2024 (widely reported: The Register, HPCwire, 2024-01)

#segment:foundry #source-tier:A #signal-type:roadmap #company:intel_foundry #date:2024-01 #importance:high #confidence:high #cross-ref

---

## Open Questions

- [ ] Will Microsoft 18A move from sampling to volume production for any AI workload chip?
- [ ] What is Intel 18A's wafer yield relative to TSMC N2?
- [ ] Can Intel Foundry reach profitability before 2027?
- [ ] Is any hyperscaler evaluating Intel 18A for a custom AI ASIC?
