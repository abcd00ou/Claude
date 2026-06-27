# Simulated dataset — Capacity

**Created:** 2026-06-24 · **Feeds:** Product Supply Mgr (SM-T1) ⇄ MI supply · **source = SIMULATION** (fictional)

Supply capacity + utilization by product / node / period. Pairs with `production.md`
(production = actual output; capacity = the ceiling). All numbers fictional.

## Schema (payload)

| Field | Type | Meaning |
|---|---|---|
| `period` | quarter | e.g. 2026Q1 |
| `family` | enum | DDR5 · LPDDR5X · HBM3E · ... |
| `node` | string | process node |
| `capacity_wafers_kpm` | number | installed capacity, k wafers/month |
| `allocated_wafers_kpm` | number | capacity committed to demand |
| `utilization_pct` | number | % |
| `capacity_pb` | number | bit capacity, petabits (sim) |

## Sample

| period | family | node | capacity_wafers_kpm | allocated_wafers_kpm | utilization_pct | capacity_pb |
|---|---|---|---|---|---|---|
| 2026Q1 | HBM3E | 1b | 50 | 47 | 94 | 6.1 |
| 2026Q1 | DDR5 | 1b | 110 | 96 | 87 | 16.5 |
| 2026Q1 | LPDDR5X | 1b | 85 | 78 | 92 | 10.8 |
| 2026Q2 | HBM3E | 1c | 70 | 68 | 97 | 9.2 |
| 2026Q2 | DDR5 | 1c | 105 | 92 | 88 | 17.6 |
| 2026Q2 | LPDDR5X | 1c | 60 | 56 | 93 | 8.0 |
| 2026Q3 | HBM3E | 1c | 88 | 86 | 98 | 11.9 |

## Notes

- **HBM runs near 100% utilization** — the tight node; allocation is the binding constraint.
  This is the signal the allocator + MI care about most. `#importance:high`
- `capacity` vs `production` gap = headroom (or yield loss). HBM headroom ~0.
- Dedup rule: this `capacity` and MI-T1 `supply` describe the same balance — one canonical
  writer per (family, period). See [`../TASK_MAP.md`](../TASK_MAP.md) coordination rules.
