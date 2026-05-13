# Microsoft Maia 200 — Company Intelligence

**Segment(s):** asic  
**Role in AI SCM:** Microsoft's in-house AI inference accelerator for Azure; manufactured on TSMC 3nm; deployed to power OpenAI GPT-5.2 and Microsoft Foundry inference workloads; part of Microsoft's custom silicon multi-vendor strategy.  
**HQ:** Redmond, WA, USA (parent: Microsoft)  
**Ticker:** NASDAQ:MSFT (parent)  
**Last Updated:** 2026-05-13

---

## Company Overview

Microsoft's Maia 200 is the company's first generally available custom AI accelerator, designed for inference workloads under Project Maia. Manufactured on TSMC 3nm, Maia 200 is deployed in Azure AI infrastructure to power OpenAI workloads and Microsoft Foundry services. It is available in US Central (Des Moines, IA) and US West 3 (Phoenix, AZ) as of January 2026. Mass production was delayed from 2025 to 2026. Alongside Maia, Microsoft also deploys NVIDIA GB300 NVL72 clusters at scale (first large-scale cluster: 4,608 GPUs, 92.1 ExaFLOPS FP4 for OpenAI).

**Source:** Microsoft Official Blog, 2026-01-26, https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/

---

## Key Products & AI Relevance

| Product / Technology | AI Use Case | Market Position |
|---|---|---|
| Maia 200 ASIC | Azure AI inference for GPT-5.2, Microsoft Foundry | Internal only; 140B+ transistors |
| Maia 200 (TSMC 3nm, 750W TDP) | Large model inference (>1T parameter models) | Internal deployment only |
| Azure GB300 NVL72 clusters | OpenAI training and inference at ExaFLOP scale | First hyperscaler GB300 NVL72 large-scale cluster |
| Azure Cobalt CPU (Arm-based) | AI workload host processor — not accelerator | Available on Azure |

**Source:** Microsoft Official Blog, 2026-01-26; Microsoft Azure Blog, 2026-02

---

## Key Specs (Maia 200)

| Spec | Value | Source |
|---|---|---|
| Process | TSMC 3nm | Microsoft Blog, 2026-01-26 |
| Transistors | 140B+ | Microsoft Blog, 2026-01-26 |
| Memory | 216 GB HBM3e | Microsoft Blog, 2026-01-26 |
| Memory bandwidth | 7 TB/s | Microsoft Blog, 2026-01-26 |
| On-chip SRAM | 272 MB | Microsoft Blog, 2026-01-26 |
| Performance (FP4) | >10 PFLOPS | Microsoft Blog, 2026-01-26 |
| Performance (FP8) | >5 PFLOPS | Microsoft Blog, 2026-01-26 |
| TDP | 750W | Microsoft Blog, 2026-01-26 |
| Efficiency vs. prior fleet | 30% better performance-per-dollar | Microsoft Blog, 2026-01-26 |
| FP4 vs. Amazon Trainium3 | 3× | Microsoft Blog, 2026-01-26 |

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
| Microsoft FY2026 capex guidance | ~$190B (includes ~$25B from higher component pricing) | FY2026 | Microsoft Q3 FY2026 earnings, 2026-04-29 |
| Q3 FY2026 actual capex | $31.9B (+49% YoY) | Q3 FY2026 | Microsoft Q3 FY2026 earnings |
| Azure AI business run rate | $37B annually (+123% YoY) | Q3 FY2026 | Microsoft Q3 FY2026 earnings |
| Maia 200 ASIC capex contribution | Not separately disclosed | — | — |

---

## Supply Chain Position

Maia 200 is designed by Microsoft Silicon Engineering Group and manufactured by TSMC (3nm). Marvell is the confirmed package design partner for Maia. SK Hynix supplies HBM3e. Microsoft uses Maia alongside a large NVIDIA GPU fleet — the two are complementary, not exclusive. Microsoft is also part of NVIDIA NVLink Fusion ecosystem, and Marvell (Maia packaging partner) is a confirmed NVLink Fusion partner.

**Key customers (publicly stated):** OpenAI (primary inference customer on Azure), Microsoft Foundry  
**Key suppliers (publicly stated):** TSMC (3nm fabrication), Marvell (packaging/design partner), SK Hynix (HBM3e)

**Source:** Microsoft Blog, 2026-01-26; NVIDIA NVLink Fusion ecosystem, 2026-03

---

## Technology Roadmap

| Milestone | Timeline | Status | Source |
|---|---|---|---|
| Maia 200 general availability | 2026-01-26 | Live in US Central + US West 3 | Microsoft Blog, 2026-01-26 |
| Powering GPT-5.2 (OpenAI) | As of GA | In production | Microsoft Blog, 2026-01-26 |
| Microsoft Azure GB300 NVL72 large-scale cluster (4,608 GPUs) | 2026-02 | Deployed | Microsoft Azure Blog, 2026-02 |
| Maia next generation (Maia 2 or successor) | Not publicly announced | — | — |

---

## Competitive Position

| Competitor | Segment | Key Differentiator | Source |
|---|---|---|---|
| Google Ironwood (TPU7) | Internal ASIC | 4.6 PFLOPS/chip at TSMC N3P; 9,216-chip superpod | Google Cloud Blog, 2026-04 |
| AWS Trainium3 | Internal ASIC | 2.52 PFLOPS/chip FP8; 144 chips per UltraServer | AWS re:Invent, 2025-12-02 |
| Meta MTIA 300 | Internal ASIC | 1.2 PFLOPS FP8; ranking/recommendation focus | Meta Blog, 2026-03 |
| NVIDIA GB300 | GPU | Ecosystem leader; sold out through mid-2026 | NVIDIA earnings |

---

## Updates

### Update: 2026-01-26 — Maia 200 generally available; deployed in US Central and US West 3; powers GPT-5.2

> Maia 200 is live in US Central (Des Moines, IA) and US West 3 (Phoenix, AZ). Powers GPT-5.2 (OpenAI) and Microsoft Foundry workloads. Mass production was delayed from 2025 to 2026. Performance: >10 PFLOPS FP4, 216 GB HBM3e at 7 TB/s bandwidth, 750W TDP, 30% better performance-per-dollar vs. prior fleet hardware, 3× FP4 vs. Amazon Trainium 3.

**Source:** Microsoft Official Blog, 2026-01-26, https://blogs.microsoft.com/blog/2026/01/26/maia-200-the-ai-accelerator-built-for-inference/

#segment:asic #source-tier:A #signal-type:roadmap #company:microsoft #date:2026-01-26 #importance:high #confidence:high #cross-ref:end_market #cross-ref:foundry

---

## Open Questions

- [ ] What percentage of Azure AI inference hours run on Maia 200 vs. NVIDIA GPUs?
- [ ] Has Microsoft announced a Maia 200 successor or roadmap for next-generation custom silicon?
- [ ] What training workloads (if any) run on Maia vs. NVIDIA GB300?
