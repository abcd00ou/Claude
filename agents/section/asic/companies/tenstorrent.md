# Tenstorrent — Company Intelligence

**Segment(s):** asic  
**Role in AI SCM:** Designs RISC-V-based AI accelerators (Blackhole architecture); Galaxy Blackhole system reached general availability April 2026; raised $693M Series D led by Samsung Securities; founded by Jim Keller.  
**HQ:** Santa Clara, CA, USA  
**Ticker:** Private  
**Last Updated:** 2026-05-13

---

## Company Overview

Tenstorrent designs RISC-V-based AI accelerators optimized for both AI inference and training on cloud and edge platforms. Its Blackhole architecture uses a scalable mesh-connected RISC-V core design. The Galaxy Blackhole system — a 6U chassis with 32 Blackhole accelerators — reached general availability on April 28, 2026, pricing at $110,000 per system (Galaxy Supercluster: 4 systems for $440,000). Tenstorrent's founder Jim Keller (formerly AMD, Apple, Tesla, Intel) is a key credibility driver. The company raised $693M in Series D funding in December 2024, led by Samsung Securities, with Hyundai and LG as co-investors.

**Source:** The Register / HPCwire, 2026-04-28, https://www.theregister.com/2026/04/28/tenstorrent_galaxy_blackhole_ai_servers_ga/

---

## Key Products & AI Relevance

| Product / Technology | AI Use Case | Market Position |
|---|---|---|
| Blackhole BH0 accelerator chip | AI training and inference | Challenger; RISC-V based |
| Galaxy Blackhole system (6U, 32× BH0) | Cloud AI training/inference cluster node | GA April 2026 |
| Galaxy Supercluster (4× Galaxy, 128× BH0) | Scale-out AI training | $440K at launch |
| 144-node / 4,000+ chip clusters | Large-scale AI training | Scaling roadmap |
| Grayskull e75/e150 (prior gen) | Edge AI inference | Available |

**Source:** The Register, 2026-04-28; Tenstorrent corporate disclosures

---

## Key Specs (Galaxy Blackhole)

| Spec | Value | Source |
|---|---|---|
| Form factor | 6U chassis | The Register, 2026-04-28 |
| Accelerators per system | 32 Blackhole chips | The Register, 2026-04-28 |
| Memory | 1 TB GDDR6 | The Register, 2026-04-28 |
| Memory bandwidth | 16 TB/s | The Register, 2026-04-28 |
| Peak performance | 23 PFLOPS FP8 | The Register, 2026-04-28 |
| Internal fabric | 100 Tbps aggregate Ethernet mesh | The Register, 2026-04-28 |
| Price (single system) | $110,000 | The Register, 2026-04-28 |
| Price (Galaxy Supercluster, 4 systems) | $440,000 | The Register, 2026-04-28 |
| Maximum cluster scale | 144 nodes / 4,000+ chips | The Register, 2026-04-28 |

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
| Series D funding | $693M | 2024-12 | PR Newswire, 2024-12 |
| Series E targeted (reported) | ~$800M at ~$3.2B valuation | 2025-11 | Trade press |
| Revenue | Not publicly disclosed | — | Private company |
| Galaxy Blackhole system price | $110,000 / system | GA 2026-04-28 | The Register |

---

## Supply Chain Position

Tenstorrent's Blackhole chips are manufactured by TSMC (process node not publicly confirmed; believed to be 7nm based on specs and pricing). The Galaxy system uses GDDR6 memory (not HBM — differentiating from NVIDIA/AMD at lower cost). Korean conglomerate investors (Samsung Securities, Hyundai, LG Electronics) suggest potential strategic alignment with Korean electronics supply chains.

**Key customers (publicly stated):** Not publicly disclosed; targeting cloud providers and AI research institutions  
**Key suppliers (publicly stated):** TSMC (fabrication — not confirmed publicly), GDDR6 memory (Samsung or SK Hynix — not confirmed)

**Source:** PR Newswire, 2024-12; The Register, 2026-04-28

---

## Technology Roadmap

| Milestone | Timeline | Status | Source |
|---|---|---|---|
| Galaxy Blackhole general availability | 2026-04-28 | Available | The Register, 2026-04-28 |
| 144-node / 4,000+ chip cluster scaling | 2026 | Scaling roadmap available | The Register, 2026-04-28 |
| Series E funding (~$800M at ~$3.2B valuation) | 2025-11 (seeking) | Potential | Trade press, 2025-11 |
| Blackhole successor (Quasar?) | Not publicly announced | — | — |

---

## Competitive Position

| Competitor | Segment | Key Differentiator | Source |
|---|---|---|---|
| NVIDIA GB300 NVL72 | GPU | 92.1 ExaFLOPS FP4 per 4,608-GPU cluster; HBM3e | Microsoft Azure Blog, 2026-02 |
| AMD MI450 | GPU | 432 GB HBM4, TSMC 2nm; Meta $60B deal | Digitimes, 2026-02-06 |
| Cerebras CS-3 | Wafer-scale | 125 PFLOPS claimed; full-wafer die; no HBM — on-chip SRAM | Cerebras corporate |
| Intel Gaudi 3 | GPU/ASIC | Gaudi line discontinued; Jaguar Shores 2026 | Intel Newsroom, 2026-01-09 |

---

## Updates

### Update: 2026-04-28 — Galaxy Blackhole reaches general availability; scales to 144 nodes / 4,000+ chip clusters; priced $110K/system

> Tenstorrent announced general availability of Galaxy Blackhole AI system. 6U chassis, 32 Blackhole accelerators, 1 TB GDDR6, 16 TB/s memory bandwidth, 23 PFLOPS FP8, 100 Tbps Ethernet mesh. Scales to 144 nodes / 4,000+ chips. Single Galaxy $110,000; Galaxy Supercluster (4 systems) $440,000.

**Source:** The Register / HPCwire, 2026-04-28, https://www.theregister.com/2026/04/28/tenstorrent_galaxy_blackhole_ai_servers_ga/

#segment:asic #source-tier:B #signal-type:roadmap #company:tenstorrent #date:2026-04-28 #importance:high #confidence:medium #cross-ref:end_market

---

### Update: 2024-12 — $693M Series D led by Samsung Securities; Hyundai, LG, Bezos Expeditions co-invest

> Tenstorrent closed $693M Series D led by Samsung Securities and AFW Partners. Co-investors: Fidelity, Bezos Expeditions, Hyundai, LG Electronics. Potential Series E (2025-11): seeking $800M at $3.2B valuation, Fidelity leading.

**Source:** PR Newswire, 2024-12, https://www.prnewswire.com/news-releases/tenstorrent-closes-693m-of-series-d-funding-led-by-samsung-securities-and-afw-partners-302319584.html

#segment:asic #source-tier:A #signal-type:roadmap #company:tenstorrent #date:2024-12 #importance:medium #confidence:high

---

## Open Questions

- [ ] Has Tenstorrent secured any named hyperscaler or government AI customer?
- [ ] What process node is the Blackhole chip manufactured on?
- [ ] What is Tenstorrent's revenue for FY2025 and FY2026 (Series E prospectus may disclose)?
