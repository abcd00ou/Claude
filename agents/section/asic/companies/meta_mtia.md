# Meta MTIA (Meta Training and Inference Accelerator) — Company Intelligence

**Segment(s):** asic  
**Role in AI SCM:** Meta's in-house custom AI accelerator family for ranking, recommendation, training, and generative AI inference; multi-generational TSMC-manufactured chip co-developed with Broadcom.  
**HQ:** Menlo Park, CA, USA (parent: Meta Platforms)  
**Ticker:** NASDAQ:META (parent)  
**Last Updated:** 2026-05-13

---

## Company Overview

Meta's MTIA program is the custom silicon arm of Meta AI Infrastructure. The MTIA family spans four generations (300/400/450/500) and is co-developed with Broadcom across multiple chip generations. MTIA 300 is in production for ranking and recommendation workloads; MTIA 400 is in lab testing. The next-generation MTIA (450) will be the first AI chip manufactured on TSMC N2 (2nm), with Meta committed to deploying 1 gigawatt of MTIA chips initially. Meta's explicit strategic rationale is supply chain diversification: at $135B annual capex, dependence on a single GPU supplier is described as "an existential risk."

**Source:** Expanding Meta's Custom Silicon to Power Our AI Workloads, Meta Official Blog, 2026-03, https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/

---

## Key Products & AI Relevance

| Product / Technology | AI Use Case | Market Position |
|---|---|---|
| MTIA 300 | Ranking and recommendation training; 800W TDP, 1.2 PFLOPS FP8, 216 GB HBM | Volume production (Meta-internal only) |
| MTIA 400 | Next-gen training; 1,200W, 6 PFLOPS FP8, 288 GB HBM | Lab testing, targeting deployment |
| MTIA 450 | Generative AI inference on TSMC N2 (first AI chip on 2nm) | H2 2026 target |
| MTIA 500 | AGI-scale workloads for Meta Superintelligence Labs | 2027 target |

**Source:** Meta Official Blog, 2026-03; SiliconAngle, 2026-04-14, https://siliconangle.com/2026/04/14/meta-doubles-partnership-broadcom-committing-1-gigawatt-custom-ai-processors/

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
| Meta total capex guidance (FY2026) | $125–145B | 2026 | Meta Q1 2026 earnings, 2026-04-29 |
| Meta Q1 2026 actual capex | $19.84B | Q1 2026 | Meta Q1 2026 earnings |
| MTIA 1 GW deployment commitment | Committed, dollar value undisclosed | 2026+ | SiliconAngle, 2026-04-14 |

---

## Supply Chain Position

MTIA chips are designed in-house by Meta AI Infrastructure hardware teams and manufactured by TSMC (N3 for MTIA 300/400; N2 for MTIA 450+). Broadcom is confirmed as multi-generational co-development and packaging partner. MTIA sits alongside Meta's multi-vendor GPU strategy: Meta simultaneously deploys NVIDIA (GB300, Vera Rubin), AMD MI450 (~$60B / 6 GW deal), and MTIA — all at gigawatt scale.

**Key customers (publicly stated):** Internal Meta AI workloads only (ranking, recommendation, generative AI, training for AGI)  
**Key suppliers (publicly stated):** TSMC (N3, N2 fabrication), Broadcom (design partner), SK Hynix / Samsung (HBM supply)

**Source:** Meta Official Blog, 2026-03; AMD Newsroom, 2026-02-24

---

## Technology Roadmap

| Milestone | Timeline | Status | Source |
|---|---|---|---|
| MTIA 300 (800W, 1.2 PFLOPS, 216 GB HBM) | In production Q1 2026 | Volume production | Meta Blog, 2026-03 |
| MTIA 400 (1,200W, 6 PFLOPS, 288 GB HBM) | Lab testing, targeting data center | Pre-production | Meta Blog, 2026-03 |
| MTIA 450 — TSMC N2, generative AI inference | H2 2026 | Announced | Meta Blog, 2026-03 |
| MTIA 500 — AGI workloads | 2027 | Announced | Meta Blog, 2026-03 |
| 1 GW MTIA initial deployment | Begins with MTIA 450 | Committed | SiliconAngle, 2026-04-14 |
| Multi-GW MTIA scale-up | By 2027 | Guided | SiliconAngle, 2026-04-14 |

---

## Competitive Position

| Competitor | Segment | Key Differentiator (stated) | Source |
|---|---|---|---|
| Google Ironwood (TPU7) | Internal ASIC | 4.6 PFLOPS/chip on TSMC N3P; 9,216-chip superpod = 42.5 ExaFLOPS | Google Cloud Blog, 2026-04 |
| AWS Trainium3/4 | Internal ASIC | Trainium4: 6× FP4 vs Trn3; NVLink Fusion integration | NVIDIA Technical Blog, 2025-12-02 |
| Microsoft Maia 200 | Internal ASIC | TSMC 3nm; >10 PFLOPS FP4; powers GPT-5.2 on Azure | Microsoft Blog, 2026-01-26 |
| NVIDIA GB300 | GPU | Largest external GPU ecosystem; sold out through mid-2026 | NVIDIA earnings, 2026-02-26 |

---

## Updates

### Update: 2026-03 — Meta MTIA next-generation on TSMC N2 (first AI chip on 2nm); 1 GW initial deployment; Broadcom multi-gen partnership

> Meta's next-generation MTIA chip will be the first AI chip manufactured on TSMC N2 (2nm process). Meta committed to deploying 1 gigawatt (1,000 MW) of MTIA chips initially, scaling to multiple gigawatts by 2027. Meta deepened its partnership with Broadcom to co-develop "multiple generations" of MTIA chips covering chip architecture co-development across the MTIA roadmap (MTIA 300/400/450/500). MTIA 450 is slated for H2 2026 targeting generative AI inference; MTIA 500 targeted for 2027. Meta Superintelligence Labs appointed a dedicated hardware leader to oversee custom chip development for AGI workloads.

**Source:** Expanding Meta's Custom Silicon to Power Our AI Workloads, Meta Official Blog, 2026-03, https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/; Meta commits to deploying 1 gigawatt of MTIA chips, SiliconAngle, 2026-04-14

#segment:asic #source-tier:A #signal-type:roadmap #company:meta #date:2026-03 #importance:high #confidence:high #cross-ref:foundry #cross-ref:end_market #cross-ref:dram

---

### Update: 2026-03 — MTIA roadmap announced: four generations (300–500); MTIA 300 in production; MTIA 400 in lab testing

> Meta announced a four-generation MTIA roadmap (MTIA 300/400/450/500). MTIA 300 is already in production for ranking and recommendation training: 800W TDP, 1.2 PFLOPS FP8, 216 GB HBM. MTIA 400 is in lab testing ahead of data center deployment: 1,200W, 6 PFLOPS FP8, 288 GB HBM. Meta plans to train next-generation models on MTIA hardware.

**Source:** Expanding Meta's Custom Silicon to Power Our AI Workloads, Meta Official Blog, 2026-03, https://about.fb.com/news/2026/03/expanding-metas-custom-silicon-to-power-our-ai-workloads/

#segment:asic #source-tier:A #signal-type:roadmap #company:meta #date:2026-03 #importance:high #confidence:high #cross-ref:dram #cross-ref:end_market #cross-ref:foundry

---

## Open Questions

- [ ] What are MTIA 450 performance specs (PFLOPS, memory capacity, TDP)?
- [ ] Which TSMC N2 fab site is allocated for MTIA 450 production?
- [ ] What percentage of Meta's total compute hours run on MTIA vs. NVIDIA vs. AMD?
- [ ] Will MTIA ever be offered externally via Meta AI services or chip licensing?
