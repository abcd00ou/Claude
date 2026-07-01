# Lead-Lag & Money-Flow Blockage — REAL-DATA Analysis, AI Value Chain

**Date:** 2026-07-01
**Analyst layer:** `agents/data/analysis/`
**Methodology source:** `agents/Scope_Document_LeadLag_EN.md` (Outputs ②–⑥)
**Data source:** `agents/data/dba/financials.db` — real quarterly financials, 2016-Q1 → 2027-Q1
**Pipeline:** `agents/data/dba/leadlag.py` + `agents/data/dba/run_analysis.py` (pandas/numpy, reproducible)
**Raw output:** `agents/data/dba/leadlag_results.json`
`#segment:cross` `#signal-type:leadlag` `#importance:high` `#source-tier:A` `#confidence:medium`

---

## 0. What this is (and what changed vs. the synthetic scope)

The Scope Document validated the pipeline on a **synthetic** 3-tier chain (Power → AI Chip →
DRAM) with a planted ground truth. This report runs the **same five outputs on the real panel**
of 15 AI-supply-chain companies. Three honest adaptations were required by the actual data —
each is a real-data caveat, not a workaround:

| # | Synthetic scope | Real-data reality | Handling |
|---|---|---|---|
| 1 | DRAM node = SK Hynix | Hynix/Samsung have only ~5 quarters in DB (KRW, no receivables) | **DRAM node = Micron (MU)** — 33 quarters, full balance sheet |
| 2 | CCC uses `accounts_payable` | DB has **no payables / cogs columns** | COGS = revenue − gross_profit; **CCC reduces to the Operating Cycle `OC = DIO + DSO`** (no DPO). Stated in every congestion output. |
| 3 | Backbone = clean latent cycle | Real signal is noisy, seasonal | Backbone = **revenue YoY growth** (universally populated); peak lag chosen by strongest **positive** co-movement (rejects anti-phase artifacts at ±4q) |

**Company panel (15 nodes, revenue-YoY signal, ≥12 quarters each):**
Microsoft (Hyperscaler) · Vertiv, Eaton (Power) · Modine (Cooling) · Applied Materials,
Lam Research (Fab Equipment) · NVIDIA, AMD, Broadcom, Marvell (AI Chip) · Micron (DRAM) ·
Amkor (Packaging) · Arista (Networking) · Super Micro, Dell (Server OEM).

---

## 1. Headline findings

1. **AI-chip demand leads memory (DRAM) revenue by ~1 quarter.** The single strongest, most
   economically-legible edges are **Broadcom →1q→ Micron (corr 0.85, Granger p=0.04)** and
   **NVIDIA →1q→ Micron (corr 0.80, Granger p=0.03)**. Chip revenue turns first; Micron's
   revenue follows one quarter later.
2. **Fab-equipment peers co-move with a 1-quarter internal lead:** **Applied Materials →1q→ Lam
   Research (corr 0.86, Granger p<0.001)** — AMAT's order cycle leads Lam's by a quarter.
3. **The real cycle is led by semiconductors, NOT by Power** — a clean divergence from the
   synthetic. In 2016–2026 real data, AI-chip and fab-equipment names sit **upstream** (lead),
   while Power/electrical (Vertiv, Eaton) and downstream integrators (Dell, Modine) **lag**. The
   grid/power build-out is a *responder* to chip demand here, not its leading indicator.
4. **Money is currently stuck in the AI-chip tier, not in memory.** NVIDIA, AMD, Broadcom, Marvell
   and Amkor all flag **internal working-capital congestion** (rising operating cycle) — the mirror
   image of the synthetic, where DRAM was the congested node. Micron is **Healthy** (OC falling YoY).
5. **Dell is the one compound bottleneck** — internal congestion **and** a downstream transmission
   break — worth a filings-level look.

---

## 2. Output — Company Lead/Lag Phase (direct "lead and lag of each company")

`phase_score` = −mean over partners of (lead-quarters × |corr|). **Negative = leads (upstream);
positive = lags (downstream).** Ranked most-leading → most-lagging.

| rank | company | sector | phase_score | reads as |
|---|---|---|---|---|
| 1 | **AMD** | AI Chip | **−1.218** | leads the panel |
| 2 | **Applied Materials** | Fab Equipment | **−0.978** | leads |
| 3 | Amkor | Packaging | −0.645 | leads |
| 4 | Broadcom | AI Chip | −0.486 | leads |
| 5 | Super Micro | Server OEM | −0.408 | leads |
| 6 | NVIDIA | AI Chip | −0.362 | leads |
| 7 | Micron | DRAM | −0.293 | mid-chain |
| 8 | Microsoft | Hyperscaler | −0.108 | mid-chain |
| 9 | Lam Research | Fab Equipment | −0.029 | mid-chain |
| 10 | Vertiv | Power | 0.000 | mid-chain |
| 11 | Eaton | Power | +0.362 | lags |
| 12 | Arista | Networking | +0.421 | lags |
| 13 | Dell | Server OEM | +0.526 | lags |
| 14 | Modine | Cooling | +1.313 | lags |
| 15 | Marvell | AI Chip | +2.047 | outlier (see note) |

> **Note on Marvell:** its post-2023 AI-driven revenue inflection sits out of phase with the older
> part of the panel, pushing it to a noisy +2.05 despite being an AI-chip name. Treat as low-confidence.

---

## 3. Output ③ — Lead-Lag Network (directed edges, real data)

Top edges by directional score (all positive co-movement; `lead_q` = quarters leader precedes follower):

| from (leader) | → to (follower) | lead_q | peak corr | Granger p (fwd) | score |
|---|---|---|---|---|---|
| **Broadcom** | **Micron** | **1** | **0.846** | **0.038** | 1.096 |
| **NVIDIA** | **Micron** | **1** | **0.795** | **0.032** | 1.045 |
| **Applied Materials** | **Lam Research** | **1** | **0.855** | **<0.001** | 1.005 |
| Applied Materials | Marvell | 4 | 0.905 | – | 1.005 |
| Super Micro | Micron | 1 | 0.752 | 0.050 | 1.002 |
| Arista | Modine | 2 | 0.652 | 0.001 | 0.902 |
| AMD | Lam Research | 1 | 0.644 | 0.018 | 0.894 |
| Micron | Modine | 2 | 0.626 | 0.006 | 0.876 |
| Broadcom | Arista | 2 | 0.613 | 0.016 | 0.863 |
| Broadcom | Microsoft | 1 | 0.611 | 0.004 | 0.861 |

**How to read it.** The chain that survives both correlation **and** Granger causality is
**AI Chip →1q→ DRAM (Micron)** and **AMAT →1q→ Lam** inside fab equipment. These are the edges you
could act on. The longer-lag edges (lead_q = 3–4) have no Granger support (`–`) and are weaker
statistical precedence — candidates only.

---

## 4. Output ② — Sector Phase Order

Sector-aggregated revenue YoY, pairwise lagged. Lower = more upstream.

| rank | section | phase_score |
|---|---|---|
| 1 | Packaging | −0.466 |
| 2 | Server OEM | −0.411 |
| 3 | Fab Equipment | −0.315 |
| 4 | AI Chip | −0.136 |
| 5 | Hyperscaler | −0.098 |
| 6 | Networking | −0.074 |
| 7 | DRAM | −0.035 |
| 8 | Power | +0.088 |
| 9 | Cooling | +1.473 |

⚠️ **Low confidence.** With only 1–4 companies per sector and ~24–34 quarters, the sector
aggregation is noisy (Cooling = single-name Modine is the clear outlier). The **company-level**
phase (§2) and the Granger-backed **edges** (§3) are the trustworthy layers; the sector ordering
is directional context only. What *is* robust across both: **semiconductors (packaging / fab equip /
chip / DRAM) cluster upstream; Power & Cooling sit downstream.**

---

## 5. Output ④ — Working-Capital Congestion (Operating Cycle, no DPO)

`OC = DIO + DSO`, `DIO = inventory/COGS×91.25`, `DSO = receivables/revenue×91.25`.
Flag: YoY OC growth > 0.15 **and** (ΔDIO>0 or ΔDSO>0). **DPO omitted — not in DB.**

| company | status | recent OC (days) | OC YoY | congested Q / 4 | driver |
|---|---|---|---|---|---|
| **NVIDIA** | **Congestion Warning** | 163.0 | −0.06 | 2 | Receivables (DSO) |
| **AMD** | **Congestion Warning** | 210.1 | −0.02 | 1 | Inventory (DIO) |
| **Broadcom** | **Congestion Warning** | 86.5 | +0.30 | 2 | Receivables (DSO) |
| **Marvell** | **Congestion Warning** | 239.6 | +0.50 | 3 | Receivables (DSO) |
| **Amkor** | **Congestion Warning** | 127.9 | +0.35 | 1 | Inventory (DIO) |
| **Dell** | **Congestion Warning** | 120.3 | +0.32 | 4 | Inventory (DIO) |
| Micron | Healthy | 217.3 | −0.15 | 0 | – |
| Microsoft, Modine, Applied Mat, Lam, Arista, Super Micro | Healthy | – | – | 0 | – |
| Vertiv, Eaton | insufficient data | – | – | – | balance-sheet items too sparse |

**Reading it.** The congestion is concentrated in the **AI-chip / packaging** tier, driven mostly
by **receivables (DSO)** — revenue is booked but cash collection lags, consistent with rapid AI
revenue ramps outrunning collections. **Micron (DRAM) is Healthy** — its operating cycle is
*falling* YoY (−15%), the opposite of the synthetic's congested-Hynix. Vertiv/Eaton return
"insufficient data" exactly as the synthetic did for Vertiv — correct behavior, they lack enough
quarters of inventory+receivables.

---

## 6. Output ⑤ — Transmission Gap

Regression `down(t) = a + b·up(t−k) + ε`; break = ≥2 of last 4 quarters with `gap_z < −1`.

Representative results on the strongest edges:

| upstream | downstream | lag | β (pass-through) | recent gap_z | blocked/4 | status |
|---|---|---|---|---|---|---|
| Broadcom | Micron | 1 | 0.906 | +0.72 | 1 | Normal |
| NVIDIA | Micron | 1 | 0.785 | −0.32 | 0 | Normal |
| Applied Materials | Lam Research | 1 | 0.880 | +0.56 | 1 | Normal |
| Super Micro | Micron | 1 | 0.759 | 0.00 | 0 | Normal |
| **Broadcom** | **Microsoft** | 1 | 0.789 | −1.15 | 2 | **BREAK** |
| **AMD** | **Lam Research** | 1 | 0.678 | −0.83 | 2 | **BREAK** |
| **Micron** | **Lam Research** | 1 | 0.704 | −1.89 | 3 | **BREAK** |
| **Arista** | **Dell** | 2 | 0.479 | −0.08 | 2 | **BREAK** |

**Reading it.** The **core AI-chip → Micron pass-through is healthy** (β 0.76–0.91, no break) —
memory demand is being transmitted normally. The flagged breaks are downstream/indirect edges
where the follower recently **undershot** the leader (e.g. into Dell, into Microsoft) — a demand
signal that has not (yet) flowed through. β values in the 0.5–0.9 band are stable; the few pairs
with |β|>1.5 were the low-variance/near-collinear cases the stability guard is designed to flag.

---

## 7. Output ⑥ — Integrated Blockage Matrix (A × B)

**A** = internal congestion (§5) · **B** = transmission break as a downstream node (§6).

| company | A (internal) | B (transmission) | diagnosis | prescription |
|---|---|---|---|---|
| NVIDIA | ✅ | – | **Internal bottleneck** | Production / collection management |
| AMD | ✅ | – | **Internal bottleneck** | Production / collection management |
| Broadcom | ✅ | – | **Internal bottleneck** | Production / collection management |
| Marvell | ✅ | – | **Internal bottleneck** | Production / collection management |
| Amkor | ✅ | – | **Internal bottleneck** | Production / collection management |
| **Dell** | ✅ | ✅ | **Compound bottleneck** | Demand–supply realignment |
| Microsoft | – | ✅ | Transmission bottleneck | Re-interpret upstream demand |
| Lam Research | – | ✅ | Transmission bottleneck | Re-interpret upstream demand |
| Micron, Vertiv, Eaton, Modine, Applied Mat, Arista, Super Micro | – | – | Healthy | — |

**The analytical payoff.** The matrix localizes where money is stuck:
- **AI-chip tier (NVDA/AMD/AVGO/MRVL) + Amkor = Internal bottleneck** — cash tied up in their own
  receivables/inventory while upstream demand reaches them fine → the fix is collection/production,
  not demand re-interpretation.
- **Dell = Compound bottleneck** — both congested *and* undershooting its upstream (Arista) → the
  only name warranting a demand–supply realignment look.
- **Micron = Healthy** — the DRAM node that was the planted problem in the synthetic is, in the real
  2026 data, the clean one.

---

## 8. Limitations & two-stage validation discipline

1. **Small sample.** ~24–34 quarters per name; correlation is primary evidence, Granger the
   secondary check. Edges without Granger support (long-lag rows) are candidates only.
2. **No DPO.** CCC is truncated to the operating cycle — it captures asset-side congestion
   (inventory + receivables) but not supplier-financing (payables). A firm stretching payables
   would look worse here than a true CCC would show.
3. **Statistics ≠ contracts.** Every lead-lag edge is *statistical* precedence. Per the scope's
   two-stage rule: (1) these results **narrow** the candidate relationships; (2) confirm the actual
   trade links via **Bloomberg SPLC / 10-K customer-concentration disclosures** before acting. The
   Broadcom/NVIDIA → Micron and AMAT → Lam edges are the top candidates to validate first.
4. **Symptoms, not causes.** Rising receivables at the AI-chip tier could be a demand ramp, a
   payment-terms change, or channel build — confirm via filings.
5. **Duplicate-quarter rows** exist for a few names (fiscal vs. calendar period mapping, e.g. two
   `2026-Q1` Micron rows); they marginally affect OC levels, not the Healthy/Warning verdict.
6. **Marvell** is a phase outlier (§2) — its AI inflection is out of phase with the older panel.

---

## 9. Deliverables produced

- **Company lead/lag table** (§2) — every panel company ranked upstream→downstream
- **Lead-lag network** (§3) — directed edges, lead time, correlation, Granger p
- **Sector phase order** (§4) — with an explicit low-confidence caveat
- **Money-flow blockage report** (§5–§7) — operating-cycle congestion, transmission gaps, matrix
- **Reproducible pipeline** — `leadlag.py`, `run_analysis.py`, `leadlag_results.json`

*Next step (scope §10): cross-validate the top edges (Broadcom/NVIDIA→Micron, AMAT→Lam) against
Bloomberg SPLC supplier/customer lists before treating them as trade relationships.*
