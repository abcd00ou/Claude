# Storage Expert Agent

**Segment:** NAND Flash / Enterprise Storage  
**Sales Lens:** AI training dataset storage, inference checkpoint storage, enterprise SSD attach rates  
**Last Updated:** 2026-05-12

---

## Market Overview

AI workloads create massive storage demand at every layer:
- **Training:** petabyte-scale dataset storage (object storage backed by QLC NAND)
- **Inference:** fast checkpoint/model weight loading (NVMe SSD, CXL memory)
- **Edge AI:** on-device SSD for local model caching (client NVMe)

NAND pricing is recovering from the deepest downcycle in memory history (2022–2023).
AI-driven demand is the primary upside catalyst for 2025–2026.

---

## Key Players & Market Share

| Company | NAND Bit Share | Enterprise SSD | Notes |
|---|---|---|---|
| Samsung | ~30–33% | Leading | Vertical integration: fab + controller + firmware |
| SK Hynix / Solidigm | ~20–22% | Growing | Solidigm (Intel NAND) acquired; enterprise focus |
| Kioxia / WD | ~18–20% | Strong | Joint fab (Y-series); IPO status affects capex |
| Micron | ~13–15% | Growing | 232-layer QLC; aggressive data center positioning |
| YMTC | ~8–10% | China-domestic | 232-layer; geopolitical risk for non-China customers |

---

## Demand Signals (AI-driven)

- Each AI training cluster (e.g., 50K GPU) requires 2–5 EB of accessible storage
- Model checkpoint size growing: LLaMA 3 405B = ~750 GB; GPT-4 class = multi-TB
- Inference serving: fast NVMe reduces model load latency (critical for real-time AI apps)
- Hyperscaler storage capex growing 20–30% YoY driven by AI data pipelines

**Storage attach signal:** Every $1B of GPU capex historically correlates to ~$150–200M of enterprise SSD spend.

---

## Supply Constraints

- NAND supply recovering; bit growth healthy in 2025 (~20–25% YoY)
- QLC NAND yield improving; now viable for enterprise with power-loss protection
- Enterprise SSD controller supply (Marvell, Phison) less constrained than 2021–2022
- YMTC export restrictions create supply holes in Western hyperscaler supply chains

---

## Pricing Trends

- Enterprise SSD (PCIe Gen5 NVMe): ~$0.07–0.09/GB (improving)
- QLC NAND wafer pricing up ~30% from 2023 trough
- Client SSD (M.2): ~$0.04–0.06/GB
- Long-term: eSSD ASP pressure from QLC adoption, offset by capacity mix-shift

---

## Technology Roadmap

| Technology | Status | AI Relevance |
|---|---|---|
| 232-layer QLC | Volume production | Cost-effective dataset storage |
| 300+ layer (Samsung V9, Micron B8) | 2025–2026 | Density improvement, $/GB reduction |
| PCIe Gen5 NVMe | Ramping | 2× bandwidth vs Gen4; AI model loading |
| CXL memory-semantic storage | Early | Cache tier between DRAM and NVMe |
| Computational Storage (CSDs) | Emerging | In-storage pre-processing for AI pipelines |

---

## Sales & Marketing Angles

- **Pitch:** AI model sizes double every 18 months → storage need grows faster than compute
- **QLC upgrade cycle:** Enterprise customers replacing SLC/MLC with QLC at scale
- **Gen5 NVMe attach:** New AI inference servers spec Gen5 as baseline → refresh opportunity
- **Hyperscaler direct:** Most AI storage spend goes through ODMs/JDMs, not traditional channels

---

## Recent Developments

### Update: 2026-05-12 — Baseline entry
> Initial stub. Populate with Kioxia IPO news, Micron Q2 FY2026 storage commentary.

---

## Open Questions

- [ ] Kioxia IPO status and impact on capex / supply discipline?
- [ ] YMTC market share trajectory outside China — risk or noise?
- [ ] CXL storage: which hyperscalers are deploying in production clusters?
