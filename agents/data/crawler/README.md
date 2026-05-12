# Crawler Agent

**Role:** Source monitoring, signal extraction, data ingestion rules  
**Last Updated:** 2026-05-12

---

## Purpose

The Crawler Agent defines WHAT to watch, WHERE to watch it, HOW OFTEN to check,
and WHAT signals to extract. It does not analyze — it registers sources and
classifies raw signals for routing to the Analysis Agent and section agents.

---

## Source Registry

### Tier 1 — Highest Priority (check weekly)

| Source | Type | Signal Target | Section Agent |
|---|---|---|---|
| NVIDIA Earnings Call | Audio / transcript | GPU allocation, B200 ramp, Rubin timeline | chip_maker |
| AMD Earnings Call | Audio / transcript | MI series shipment, ROCm wins | chip_maker |
| TSMC Earnings Call | Audio / transcript | CoWoS capacity, N3/N2 utilization | foundry |
| SK Hynix Earnings | Audio / transcript | HBM3E yield, capacity ramp | dram |
| Samsung Electronics Earnings | Audio / transcript | HBM qualification, NAND bit growth | dram, storage |
| Micron Technology Earnings | Audio / transcript | HBM3E delivery, NAND pricing | dram, storage |
| Microsoft Earnings Call | Audio / transcript | Azure AI capex, Maia progress | dc_infra, end_market |
| Google / Alphabet Earnings | Audio / transcript | TPU fleet, capex guidance | dc_infra, end_market |
| Amazon AWS Earnings | Audio / transcript | Trainium scale, Project Rainier | dc_infra, end_market |
| Meta Earnings Call | Audio / transcript | AI capex, MTIA v2 deployment | dc_infra, end_market |

### Tier 2 — High Priority (check bi-weekly)

| Source | Type | Signal Target | Section Agent |
|---|---|---|---|
| NVIDIA GTC / Hot Chips | Conference | Roadmap announcements | chip_maker, foundry |
| TSMC Technology Symposium | Conference | Advanced packaging roadmap | foundry |
| IEEE ISSCC / Hot Chips | Conference | ASIC architecture signals | asic |
| Marvell Earnings | Financial | ASIC design wins | asic |
| Broadcom Earnings | Financial | Networking ASIC, custom silicon | network, asic |
| Arista Networks Earnings | Financial | AI networking demand | network |
| Vertiv Earnings | Financial | Liquid cooling orders | dc_infra |
| Infineon / ON Semi Earnings | Financial | Power semiconductor demand signals | power |
| Ibiden / Unimicron Earnings | Financial | ABF substrate lead times | substrate |

### Tier 3 — Monitoring (check monthly)

| Source | Type | Signal Target |
|---|---|---|
| SEC 8-K / 10-Q filings | Regulatory | Guidance changes, material events |
| Trade press (EE Times, The Register, AnandTech) | News | Product launches, supply chain news |
| LinkedIn job postings (hyperscalers, Marvell, Broadcom) | Job market | ASIC design headcount signals |
| Patent filings (Google, Apple, AWS, Meta) | IP | Custom silicon architecture signals |
| Government procurement (SAM.gov, EU tender) | Government | Sovereign AI program contracts |
| Taiwan customs / export data | Trade data | Semiconductor shipment volume |
| Korea trade statistics (KITA) | Trade data | DRAM/NAND export volume and pricing |

---

## Signal Taxonomy

Every signal extracted should be tagged with:

```
#segment: [dram | storage | dc_infra | asic | chip_maker | foundry | network | power | substrate | end_market]
#signal-type: [supply | demand | pricing | roadmap | geopolitical | capex | design-win]
#company: [company name]
#date: YYYY-MM-DD
#confidence: [high | medium | low]
```

### Signal Types Defined

| Signal Type | Examples |
|---|---|
| `supply` | Lead time change, capacity expansion/cut, yield update |
| `demand` | Capex guidance, order volume, attach rate |
| `pricing` | ASP change, contract vs spot delta, quote |
| `roadmap` | Product announcement, technology milestone, node transition |
| `geopolitical` | Export controls, trade restrictions, foreign investment review |
| `capex` | Hyperscaler investment guidance, fab CapEx plan |
| `design-win` | Confirmed customer, qualification, first silicon |

---

## Crawl Cadence

| Cadence | Action |
|---|---|
| Weekly | Tier 1 sources — earnings transcripts, major news |
| Bi-weekly | Tier 2 sources — conference proceedings, supplier earnings |
| Monthly | Tier 3 sources — trade data, job postings, patents |
| Ad-hoc | Breaking news — product launch, export control, supply disruption |

---

## Signal Routing Rules

After a signal is extracted, route it:

1. Tag with taxonomy above
2. Route to the relevant section agent's "Recent Developments" section
3. If cross-segment, flag in `ORCHESTRATOR.md` → Open Flags section
4. If pricing-related, also update `data/analysis.md` demand model assumptions

---

## Open Questions

- [ ] Which earnings call transcript service to use? (Seeking Alpha, Motley Fool, direct IR sites)
- [ ] Job posting monitoring — manual scan or structured query?
- [ ] Korea KITA data frequency — monthly release; confirm lag time
