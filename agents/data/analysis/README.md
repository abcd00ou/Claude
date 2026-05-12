# Analysis Agent

**Role:** Demand modeling, supply gap estimation, trend interpretation  
**Last Updated:** 2026-05-12

---

## Purpose

The Analysis Agent provides frameworks for turning raw signals (from the Crawler Agent)
into actionable intelligence. It does not collect data — it defines HOW to interpret it.

Frameworks here are applied when updating section agents or synthesizing in ORCHESTRATOR.md.

---

## Framework 1: AI Accelerator Demand Model (Bottom-Up)

**Inputs:**
- Hyperscaler capex guidance (from end_market.md)
- GPU/ASIC % of capex (historical: 30–40%)
- Average GPU ASP (from chip_maker.md)

**Formula:**
```
GPU Unit Demand = (Hyperscaler Capex × GPU % of Capex) ÷ Avg GPU ASP

Example (2025):
= ($310B total × 35%) ÷ $32,000 avg ASP
= $108.5B ÷ $32K
≈ 3.4M GPU equivalents
```

**Sanity check:** Cross-reference against NVIDIA data center revenue ($80–100B expected 2025).

---

## Framework 2: HBM Demand Derived from GPU Demand

**Inputs:**
- GPU unit demand (from Framework 1)
- HBM capacity per GPU (in GB; from dram.md)

**Formula:**
```
HBM Demand (GB) = GPU Units × HBM GB per GPU

Example:
= 3.4M GPUs × 141 GB (H200) avg
≈ 480 EB HBM demand

Convert to wafers: 1 HBM3E 141GB stack ≈ X wafer-equivalents (check supplier data)
```

---

## Framework 3: Supply Gap Estimation

**Inputs:**
- Demand estimate (from Frameworks 1–2)
- Supplier capacity (from section agent supply constraint sections)

**Formula:**
```
Supply Gap = Demand - Available Supply

If Supply Gap > 0: Supply constrained → lead time extension, ASP pressure up
If Supply Gap < 0: Oversupplied → ASP pressure down, inventory build
```

**Trigger:** Update gap estimate when any Tier 1 source updates capacity or demand guidance.

---

## Framework 4: Capex Signal Interpretation

When a hyperscaler changes capex guidance:

| Change | Interpretation | Lead Time Impact |
|---|---|---|
| +10–20% raise | Strong demand, supply chain should expand | +1–2 quarters to lead times |
| Flat (0–5%) | Digestion or steady state | Neutral |
| -10–20% cut | Demand pause; monitor for structural shift | -1–2 quarters; watch inventory |
| Structural cut (multi-quarter) | Business model change or GPU program shift | Re-baseline demand model |

**Key rule:** One quarter of capex guidance change ≠ trend. Three consecutive quarters = trend.

---

## Framework 5: Lead Time as Demand Proxy

Supplier lead times are a real-time demand signal:

| Lead Time Change | Signal |
|---|---|
| Extending beyond 16 weeks | Supply tightening; demand outpacing supply |
| Shortening below 8 weeks | Supply loosening; demand cooling or supply added |
| Stable 12–16 weeks | Balanced market |
| 26+ weeks | Severe shortage; allocation-based market |

**Sources for lead time data:** Supplier earnings calls, Tier 2 distributor commentary,
procurement team anecdotes from trade press.

---

## Framework 6: Competitive Positioning Matrix

For each segment, score competitive landscape:

| Dimension | Question | Score (1–5) |
|---|---|---|
| Supply concentration | How many qualified suppliers? (1=monopoly, 5=many) | — |
| Switching cost | How hard to change supplier? (1=easy, 5=locked) | — |
| Technology moat | How defensible is the leader's advantage? (1=commodity, 5=unique) | — |
| Demand visibility | How predictable is demand? (1=volatile, 5=contracted) | — |

**Use case:** Identify segments where #2 player can displace #1; where lock-in is fragile.

---

## Framework 7: Sales Cycle Signal Detection

Signals that indicate a design win or sales opportunity:

| Signal | Source | Interpretation |
|---|---|---|
| New job posting for ASIC validation | LinkedIn | Early-stage custom silicon program |
| IP licensing announcement | PR/SEC | Technology being qualified |
| "New customer" mention in earnings | Earnings transcript | Design win without naming customer |
| Qualification timeline language ("on track") | Earnings | Active supply qualification |
| First silicon tapeout | Conference / press | 12–18 months to volume shipment |

---

## Demand Model Assumptions Log

Track assumption changes over time:

| Date | Parameter | Old Value | New Value | Source |
|---|---|---|---|---|
| 2026-05-12 | MS Capex 2025 | — | $80B | Jan 2025 earnings |
| 2026-05-12 | Google Capex 2025 | — | $75B | Q4 2024 earnings |
| 2026-05-12 | Amazon Capex 2025 | — | $75–80B | FY2024 actual |
| 2026-05-12 | Meta Capex 2025 | — | $60–65B | Jan 2025 guidance |

---

## Open Questions

- [ ] What is the most reliable source for average GPU ASP? (NVIDIA rarely discloses)
- [ ] HBM wafer-equivalent conversion factor — need to confirm from supplier data
- [ ] How to estimate ASIC vs GPU capex split for hyperscalers that don't disclose?
