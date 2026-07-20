# Scope Document — Lead-Lag & Money-Flow Blockage Analysis across the AI Value Chain

**Document type:** Analysis Scope & Numerical Validation
**Domain:** AI infrastructure value chain — Power / AI Chip / DRAM (extensible to Energy, Network)
**Data source:** Bloomberg Terminal (financial & price time series, SPLC supply-chain relations)
**Unit of analysis:** company × item × quarter (long-format panel)
**Methodology:** Lagged cross-correlation · Granger causality · CCC cash-cycle · transmission-gap regression
**Tooling:** Python (pandas / scipy / numpy) — `leadlag.py`, `run_analysis.py`

---

## 1. Purpose

AI-infrastructure investment cycles surface at **different times through different financial line items** depending on a company's position in the value chain. Upstream players (Power, then AI Chip) react first through capex, backlog, and inventory; that demand later propagates into the revenue and cost lines of downstream memory (DRAM) makers.

This document defines the analysis scope and, critically, **shows how each of the five outputs is numerically validated** on a controlled synthetic dataset with a known ground truth. The point of the synthetic test is falsifiability: we plant a known 3-tier chain (Power → AI Chip → DRAM) with a known lag structure and a known working-capital congestion in the DRAM firm, then confirm the pipeline recovers exactly those facts.

---

## 2. Input Data Specification

| Column | Type | Description |
|---|---|---|
| `companyname` | string | Company (analysis node) |
| `item` | string | Metric: `capex`, `revenue`, `cogs`, `inventory`, `accounts_payable`, `accounts_receivable`, `backlog`, `stock_price` … |
| `section` | string | Sector: DRAM, AI Chip, Power, Energy, Network |
| `date` | date | Quarter-end |
| `value` | float | Metric value |

**Bloomberg field availability (key point):** standard statements (`accounts_payable`, `cogs`, `accounts_receivable`, `capex`, `inventory`, `revenue`) are reliably populated; **`backlog` is sparse and issuer-dependent** and is substituted by capex/inventory when missing.

---

## 3. Synthetic Ground Truth (what we plant)

To validate the pipeline we construct 24 quarters (2019 Q1 – 2024 Q4) driven by a latent demand cycle `C(t)` and inject:

| Planted fact | Design |
|---|---|
| **Chain order** | Power → AI Chip → DRAM |
| **Lag Power → AI Chip** | AI Chip reflects `C(t−1)` (1 quarter behind) |
| **Lag AI Chip → DRAM** | DRAM reflects `C(t−3)` (⇒ 2 quarters behind AI Chip) |
| **DRAM congestion** | Inventory & receivables ramp over the last 8 quarters; payables flat |
| **No transmission break** | Downstream revenue tracks upstream faithfully (no cut injected) |

The five sections below each state the **expectation**, the **actual recovered numbers**, and the **verdict**.

---

## 4. Output ② — Sector Phase Order (numerically verified)

**What it does.** Sectors are aggregated into sector-level series, and pairwise lagged cross-correlation assigns each sector a `phase_score` (lower = more upstream). This turns the qualitative "who leads whom" into a single ordered scalar per sector.

**Expectation.** `Power (1) → AI Chip (2) → DRAM (3)`.

**Recovered result:**

| section | phase_score | rank |
|---|---|---|
| Power | **−1.990** | **1** (most upstream) |
| AI Chip | **−0.001** | **2** |
| DRAM | **+1.991** | **3** (most downstream) |

**How to read the numbers.** The `phase_score` is the signed, correlation-weighted accumulation of lead/lag votes across all sector pairs. Power sits at the extreme negative end (−1.99), DRAM at the mirror-image positive end (+1.99), and AI Chip lands almost exactly at the midpoint (−0.001). The near-perfect antisymmetry (−1.99 vs +1.99) and the mid-point AI Chip are the numerical signature of a clean, monotone 3-tier ordering.

**Verdict — PASS.** Rank order is exactly `Power(1) → AI Chip(2) → DRAM(3)`.

---

## 5. Output ③ — Lead-Lag Network (direction & lead time)

**What it does.** For every company pair, `pairwise_leadlag` scans metric×metric combinations across lags −K…+K, picks the peak-|correlation| lag, and combines four signals (lag sign, stage gap, Granger p-value asymmetry, correlation strength) into a directional score. `build_leadlag_network` emits directed edges `leader → follower`.

**Expectation.** A 3-tier chain with lead times of 1 → 2 → 3 quarters:
`Vertiv(Power) →1q→ NVDA(AI Chip) →2q→ Hynix(DRAM)`, and the transitive edge `Vertiv →3q→ Hynix`.

**Recovered result:**

| from_leader | to_follower | score | lead_quarters | sector_from | sector_to |
|---|---|---|---|---|---|
| Vertiv | NVDA | 1.001 | **1.0** | Power | AI Chip |
| NVDA | Hynix | 0.918 | **2.0** | AI Chip | DRAM |
| Vertiv | Hynix | 0.509 | **3.0** | Power | DRAM |

**How to read the numbers.** Every edge points downstream (Power→Chip→DRAM), with no reversed edges. Lead times are exactly `1 → 2 → 3` quarters, and the transitive Power→DRAM edge equals the sum of the two hops (1 + 2 = 3). The directional score decays with chain distance (1.00 → 0.92 → 0.51), which is expected: the further apart two tiers are, the more intermediate noise dilutes the direct correlation, so the adjacent hops are the most confident.

**Verdict — PASS.** Directions and lead times (1, 2, 3 quarters) match the planted chain exactly.

---

## 6. Output ④ — Working-Capital Congestion (CCC)

**What it does.** `working_capital_congestion` computes the cash-conversion cycle and flags "money stuck in working capital."

```
CCC = DIO + DSO − DPO
  DIO = inventory  / COGS    × 91.25   (days inventory outstanding)
  DSO = receivables / revenue × 91.25   (days sales outstanding)
  DPO = payables   / COGS    × 91.25   (days payables outstanding)
```
A quarter is flagged when `ΔYoY CCC > 0.15` **and** (`ΔYoY DIO > 0` **or** `ΔYoY DSO > 0`). The driver is attributed to inventory (DIO) vs. receivables (DSO) by comparing their YoY moves.

**Expectation.** Hynix flagged as congested, with the cause identified as **inventory build-up (DIO)** — since that is what we planted.

**Recovered result:**

| companyname | status | recent_CCC | CCC_yoy (recent) | congested Q (of last 4) | driver |
|---|---|---|---|---|---|
| Vertiv | insufficient data | – | – | – | – |
| NVDA | insufficient data | – | – | – | – |
| Hynix | **Congestion Warning** | **105.2** | **1.148** | **2** | **Inventory build-up (DIO)** |

Supporting CCC trajectory (Hynix, last 8 quarters):

| quarter | DIO | DSO | DPO | CCC | CCC_yoy | flagged |
|---|---|---|---|---|---|---|
| 2024-03-31 | 37.7 | 32.8 | 20.5 | 50.0 | +0.2 | no |
| 2024-06-30 | 43.2 | 37.3 | 21.8 | 58.7 | +0.0 | no |
| 2024-09-30 | 57.0 | 48.8 | 26.9 | 79.0 | +0.4 | yes |
| 2024-12-31 | 72.9 | 63.6 | 31.3 | **105.2** | **+1.1** | yes |

**How to read the numbers.** CCC climbs from ~50 to **105 days** over the final year — the cash cycle literally doubles. DIO and DSO both surge (37.7→72.9 and 32.8→63.6) while DPO stays muted (20.5→31.3), so the blockage is on the asset side, not from stretching suppliers. Because DIO's YoY move leads DSO's, the driver is correctly attributed to **inventory build-up**. Vertiv and NVDA are marked "insufficient data" — correct, since the synthetic set only gave them capex/revenue, not the full balance-sheet items CCC requires.

**Verdict — PASS.** Hynix = Congestion Warning, cause = Inventory (DIO), exactly as planted.

---

## 7. Output ⑤ — Transmission Gap (no break planted)

**What it does.** For an upstream→downstream pair, `transmission_gap` fits the normal-propagation regression and flags quarters where the downstream materially undershoots what the upstream predicts.

```
downstream_actual(t) = a + b · upstream_lead(t − k*) + ε
gap(t)   = actual − predicted
gap_z(t) = gap(t) / σ_ε           →  gap_z < −1.0 (sustained) = transmission break
```
`b` is the transmission strength (how much of an upstream move carries through). A stability guard suspends the diagnosis when the upstream signal has near-zero variance or upstream–downstream correlation < 0.2 (avoids unstable betas).

**Expectation.** We did **not** inject any break, so every pair should read **"Normal transmission,"** and the transmission strength `b` should be healthy (≈ 0.8–0.97).

**Recovered result:**

| upstream | downstream | lag (q) | transmission β | recent gap_z | blocked Q (of 4) | status |
|---|---|---|---|---|---|---|
| NVDA | Hynix | 2 | **0.927** | −0.06 | 0 | **Normal transmission** |
| Vertiv | Hynix | 3 | **0.973** | −0.81 | 0 | **Normal transmission** |
| Vertiv | NVDA | 1 | **0.843** | −0.15 | 0 | **Normal transmission** |

**How to read the numbers.** All three β values sit in the **0.84–0.97** band — strong, near-unit pass-through, meaning upstream moves flow through to downstream almost fully. No pair records a single blocked quarter (0 of 4), and the most negative `recent gap_z` is −0.81, comfortably above the −1.0 threshold. The Vertiv→Hynix lag of 3 quarters is internally consistent with the network in §5.

**Verdict — PASS.** All pairs "Normal transmission" with β in 0.8–0.97 and zero blocked quarters — exactly the no-break expectation.

---

## 8. Output ⑥ — Integrated Blockage Matrix (A × B)

**What it does.** `blockage_matrix` crosses internal congestion (**A**, from §6) with transmission break as a downstream node (**B**, from §7) to produce a per-company diagnosis and a prescription direction.

| A (internal congestion) | B (transmission break) | Diagnosis | Prescription |
|---|---|---|---|
| No | No | Healthy | — |
| Yes | No | **Internal bottleneck** | Production / collection management |
| No | Yes | Transmission bottleneck | Re-interpret upstream demand |
| Yes | Yes | Compound bottleneck | Demand–supply realignment |

**Expectation.** Hynix has congestion (A = Yes) but no transmission break (B = No), so it must land in **Internal bottleneck → Production/collection management**. Vertiv and NVDA are healthy.

**Recovered result:**

| companyname | internal_congestion (A) | transmission_block (B) | diagnosis | prescription |
|---|---|---|---|---|
| Vertiv | False | False | Healthy | — |
| NVDA | False | False | Healthy | — |
| Hynix | **True** | **False** | **Internal bottleneck** | **Production / collection management** |

**How to read the numbers.** The matrix correctly separates the *symptom location*. Hynix's cash is stuck (A = True) but upstream demand **is** reaching it normally (B = False, per §7's β≈0.93) — therefore the problem is internal (inventory it built but hasn't sold), not a demand-transmission failure. The prescription follows mechanically: manage production/collection, not upstream demand assumptions. This is the analytical payoff of separating the two diagnostics — it tells you *where* the money is stuck, which changes the response.

**Verdict — PASS.** Hynix = Internal bottleneck (A-only); Vertiv & NVDA = Healthy, exactly as planted.

---

## 9. Validation Summary

| # | Output | Expectation | Recovered | Verdict |
|---|---|---|---|---|
| ② | Sector phase | Power→AIChip→DRAM | ranks 1,2,3 (scores −1.99 / −0.00 / +1.99) | **PASS** |
| ③ | Lead-lag network | 1→2→3 q chain | 1.0 / 2.0 / 3.0 q, no reversals | **PASS** |
| ④ | CCC congestion | Hynix, driver DIO | Warning, CCC 105.2, driver Inventory | **PASS** |
| ⑤ | Transmission | all normal, β 0.8–0.97 | 0.927 / 0.973 / 0.843, 0 blocked | **PASS** |
| ⑥ | Blockage matrix | Hynix internal-only | Internal bottleneck, correct Rx | **PASS** |

All five outputs recover the planted ground truth. The pipeline is falsifiable (a wrong chain order, lag, or driver would have failed a specific numeric check) and passes.

---

## 10. Limitations & Real-Data Caveats

1. **Small sample.** Quarterly data (≈24 points) limits Granger power; correlation is the primary evidence, Granger the secondary check.
2. **Statistics ≠ contracts.** Lead-lag is a *statistical* precedence, not a proven trade relationship. Cross-validate strong candidates against **Bloomberg SPLC** (supplier/customer lists) and disclosures.
3. **Backlog gaps.** Downstream DRAM firms often omit backlog; substitute capex/inventory.
4. **Symptoms, not causes.** Rising CCC and negative gaps are symptoms — confirm the cause (demand slowdown vs. strategic inventory vs. accounting change) via filings. A rising DPO lowers CCC but can signal supplier strain, so interpret direction carefully.
5. **Transmission-gap stability.** After YoY transform, a low-variance upstream signal makes the regression β unstable; the guard suspends the call as "relationship unclear" rather than emitting a spurious number.

**Two-stage validation discipline:** (1) narrow relationship candidates statistically, then (2) confirm actual trade links via SPLC / disclosures before acting.

---

## 11. Deliverables

- Company-pair lead-lag table (direction · lead time · confidence)
- Sector phase order (upstream→downstream)
- Leading-indicator dashboard (downstream demand early-warning)
- Money-flow blockage report (CCC congestion · transmission gaps · driver attribution)
- Python modules `leadlag.py` and `run_analysis.py` with a reproducible pipeline

*End of Scope Document.*
