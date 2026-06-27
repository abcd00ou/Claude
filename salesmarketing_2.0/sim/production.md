# Simulated dataset — Production

**Created:** 2026-06-24 · **Feeds:** Product Supply Mgr (SM-T1) · **source = SIMULATION** (fictional)

Fab output by product / node / period. All numbers fictional/illustrative.

## Schema (payload)

| Field | Type | Meaning |
|---|---|---|
| `period` | quarter | e.g. 2026Q1 |
| `site` | string | fab site code (simulated) |
| `family` | enum | DDR4 · DDR5 · LPDDR5 · LPDDR5X · HBM3 · HBM3E |
| `sku` | string | e.g. HBM3E-12hi |
| `node` | string | process node (e.g. 1b, 1c) |
| `wafer_starts_kpm` | number | wafer starts, thousands/month |
| `die_per_wafer` | number | good-die assumption input |
| `yield_pct` | number | % |
| `output_pb` | number | output in petabits (sim) |
| `output_kunits` | number | finished units, thousands |

## Sample

| period | site | family | sku | node | wafer_starts_kpm | yield_pct | output_pb | output_kunits |
|---|---|---|---|---|---|---|---|---|
| 2025Q4 | FAB-M14 | HBM3E | HBM3E-8hi | 1b | 35 | 68 | 4.1 | 210 |
| 2026Q1 | FAB-M14 | HBM3E | HBM3E-12hi | 1b | 42 | 64 | 5.0 | 230 |
| 2026Q1 | FAB-M16 | DDR5 | DDR5-5600 16Gb | 1b | 90 | 91 | 12.8 | 1850 |
| 2026Q1 | FAB-M16 | LPDDR5X | LPDDR5X-8533 | 1b | 70 | 89 | 8.6 | 1400 |
| 2026Q2 | FAB-M14 | HBM3E | HBM3E-12hi | 1c | 55 | 70 | 7.4 | 320 |
| 2026Q2 | FAB-M16 | DDR5 | DDR5-6400 24Gb | 1c | 85 | 88 | 13.9 | 1600 |
| 2026Q2 | FAB-M15 | LPDDR5X | LPDDR5X-9600 | 1c | 48 | 85 | 6.1 | 950 |

## Notes

- HBM yields run low vs commodity DDR/LPDDR (stacking) — reflected above. `#importance:high`
- `1c` node ramps across 2026Q2 (capex-heavy); output rises as yield matures.
- Real generator would add the full envelope (`run_id`, `confidence`, `status=verified` within
  the sandbox, `source=SIMULATION`).
