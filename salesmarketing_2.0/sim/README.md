# Simulation Data — spec + worked sample

**Created:** 2026-06-24 · **Format:** markdown tables · **Scope:** DRAM core (DDR · LPDDR · HBM)

The **internal-source stand-in.** Production, customer demand, and customer tech demand are
internal SK hynix data the agents can't crawl — so this simulated dataset fills those gaps and
lets the whole construct run end-to-end in dev/demo without real systems access. All numbers
here are **fictional and illustrative**, not real SK hynix data.

## Labeling rule (non-negotiable)

Every simulated record carries `source = SIMULATION` and `source_tier = simulated`. This keeps
the [trust model](../_shared/trust_model.md) honest:

- In a **sandbox** deck (dev/demo), simulated facts may be treated as usable.
- In a **real** customer deck, simulated facts are NOT allowed on a slide — they surface in the
  gap report exactly like `unverified-needs-human`. A simulated number must never masquerade as
  a real `verified` fact. `#importance:high`

## Product taxonomy (DRAM core)

| Family | Representative SKUs | Die capacity | Device/stack | Status |
|---|---|---|---|---|
| DDR4 | DDR4-3200 | 8Gb, 16Gb | module | production |
| DDR5 | DDR5-4800/5600/6400, MRDIMM | 16Gb, 24Gb, 32Gb | module/RDIMM | production |
| LPDDR5 | LPDDR5-6400 | 12Gb, 16Gb | package | production |
| LPDDR5X | LPDDR5X-8533/9600 | 16Gb, 24Gb | package | production/ramp |
| LPDDR6 | LPDDR6-10667 (target) | 24Gb+ | package | roadmap |
| HBM3 | HBM3 (24GB) | — | 24GB stack | production |
| HBM3E | HBM3E 8hi/12hi (~9.6Gbps) | — | 24GB / 36GB | ramp |
| HBM4 | HBM4 (2048-bit I/O) | — | 48GB+ stack | roadmap |

## The five datasets → which task each feeds

| File | Dataset | Feeds (task) |
|---|---|---|
| [`production.md`](production.md) | fab output by product/node | Product Supply Mgr (SM-T1) |
| [`capacity.md`](capacity.md) | supply capacity + utilization | SM-T1 ⇄ MI supply |
| [`customer_demand_request.md`](customer_demand_request.md) | customer volume asks | Product Allocator (AL-T1/T2), MI demand |
| [`customer_tech_demand.md`](customer_tech_demand.md) | required specs by customer | Customer Tech (CT-T1/T3) |
| [`future_tech_spec.md`](future_tech_spec.md) | roadmap specs | CT-T2/T3, Business Enabling |

## How it maps to the canonical record

Each sample row is a flat record. The shared [envelope](../_shared/record_schema.md) applies
(`source = SIMULATION`, `source_tier = simulated`, a `status`, a `confidence`); the per-dataset
columns below are the role payload. Sample tables keep only the payload + key envelope fields
for readability; a real generator would emit the full envelope.

## Tracked customers (real names, simulated figures)

Customer **names are real**; the demand / allocation / CRM **figures attached to them are
simulated/illustrative** (`source = SIMULATION`), never actual SK hynix account data.

| Customer | Type | Memory products | Application |
|---|---|---|---|
| NVIDIA | AI accelerator | HBM3E, HBM4 | AI training/inference (Blackwell, Rubin) |
| AMD | AI accelerator | HBM3E, HBM4 | AI accelerators (Instinct) |
| Microsoft | hyperscaler | HBM, server DDR5 | AI datacenter (Maia, Azure) |
| Google / Broadcom | hyperscaler + ASIC | HBM, DDR5 | custom AI silicon (TPU) |
| Apple | handset / PC OEM | LPDDR5X, LPDDR6 | flagship mobile & Mac |
| Dell | server OEM | DDR5 RDIMM/MRDIMM | general & AI servers |
| Bosch | automotive tier-1 | LPDDR5 (auto-grade) | ADAS / IVI |

## Period convention

`2025Q4` history · `2026Q1–Q2` current · `2026Q3+` forecast · roadmap dated to mass-production quarter.
