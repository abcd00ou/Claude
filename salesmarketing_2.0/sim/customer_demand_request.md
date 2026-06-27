# Simulated dataset — Customer Demand Request

**Created:** 2026-06-24 · **Feeds:** Product Allocator (AL-T1/T2), MI demand · **source = SIMULATION** (fictional)

Customer volume asks — who wants how much of what, when, at what priority. This is the demand
side the allocator weighs against `capacity.md`. All entities/numbers fictional.

## Schema (payload)

| Field | Type | Meaning |
|---|---|---|
| `request_id` | string | unique id |
| `customer` | enum | HYPER-A · GPU-D · MOBILE-B · SERVER-C · AUTO-E |
| `period_needed` | quarter | when |
| `family` | enum | product family |
| `sku` | string | requested SKU |
| `requested_kunits` | number | volume, thousands of units (or stacks for HBM) |
| `priority` | enum | P1 (strategic) · P2 · P3 |
| `application` | string | end use |
| `status` | enum | open · committed · partial · declined |

## Sample

| request_id | customer | period_needed | family | sku | requested_kunits | priority | application | status |
|---|---|---|---|---|---|---|---|---|
| REQ-0001 | GPU-D | 2026Q2 | HBM3E | HBM3E-12hi | 180 | P1 | AI training | committed |
| REQ-0002 | HYPER-A | 2026Q2 | HBM3E | HBM3E-12hi | 140 | P1 | AI inference | partial |
| REQ-0003 | HYPER-A | 2026Q2 | DDR5 | DDR5-6400 24Gb | 900 | P2 | AI server DRAM | open |
| REQ-0004 | MOBILE-B | 2026Q3 | LPDDR5X | LPDDR5X-9600 | 1200 | P1 | flagship phone | open |
| REQ-0005 | SERVER-C | 2026Q2 | DDR5 | DDR5-5600 16Gb | 1500 | P2 | general server | committed |
| REQ-0006 | AUTO-E | 2026Q3 | LPDDR5 | LPDDR5-6400 | 300 | P3 | ADAS | open |
| REQ-0007 | GPU-D | 2026Q4 | HBM4 | HBM4-48GB | 90 | P1 | next-gen accelerator | open |

## Notes

- **HBM3E P1 demand (REQ-0001/0002) > HBM3E headroom** (see `capacity.md`: ~0 headroom). The
  allocator must split — that's the conflict the agent surfaces, human decides. `#importance:high`
- REQ-0007 (HBM4) is a future ask against a roadmap part (see `future_tech_spec.md`).
- `requested_kunits` is stacks for HBM, packages for LPDDR, modules/components for DDR.
