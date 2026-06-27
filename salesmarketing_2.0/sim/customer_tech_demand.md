# Simulated dataset — Customer Tech Demand

**Created:** 2026-06-24 · **Feeds:** Customer Tech (CT-T1/T3), Business Enabling · **source = SIMULATION** (fictional)

What spec each customer needs (not just how much). Drives qualification + roadmap fit. Pairs
with `future_tech_spec.md` (what's on the roadmap to meet these). All fictional.

## Schema (payload)

| Field | Type | Meaning |
|---|---|---|
| `customer` | enum | HYPER-A · GPU-D · MOBILE-B · SERVER-C · AUTO-E |
| `family` | enum | required family |
| `required_data_rate` | string | e.g. 9600 Mbps, 9.6 Gbps/pin |
| `required_capacity` | string | die/stack capacity needed |
| `required_power` | string | power/thermal target |
| `target_design_date` | quarter | when they design it in |
| `application` | string | end use |
| `current_status` | enum | eval · sampling · qualified · production |
| `gap_vs_current` | string | what's missing today |

## Sample

| customer | family | required_data_rate | required_capacity | target_design_date | application | current_status | gap_vs_current |
|---|---|---|---|---|---|---|---|
| GPU-D | HBM4 | 8 Gbps/pin, 2048-bit | 48GB stack | 2026Q4 | AI accelerator | eval | HBM4 not in MP yet |
| HYPER-A | HBM3E | 9.6 Gbps | 36GB (12hi) | 2026Q2 | AI inference | qualified | volume, not spec |
| MOBILE-B | LPDDR5X | 9600 Mbps | 24Gb die | 2026Q3 | flagship phone | sampling | 9600 bin yield |
| MOBILE-B | LPDDR6 | 10667 Mbps | 32Gb die | 2027Q2 | next platform | eval | LPDDR6 roadmap |
| SERVER-C | DDR5 | 6400 MT/s MRDIMM | 24Gb | 2026Q3 | server DRAM | qualified | MRDIMM ramp |
| AUTO-E | LPDDR5 | 6400 Mbps, AEC-Q | 16Gb | 2026Q4 | ADAS | qualified | auto-grade qual |

## Notes

- **GPU-D HBM4 + MOBILE-B LPDDR6** are spec demands ahead of mass production — they map to
  roadmap parts in `future_tech_spec.md`. This is where Customer Tech + Business Enabling feed
  the Planning leader's roadmap deck. `#importance:high`
- `gap_vs_current` distinguishes a *volume* gap (we have the spec) from a *spec* gap (we don't
  yet) — different actions for the human owner.
