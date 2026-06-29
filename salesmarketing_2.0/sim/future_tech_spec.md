# Simulated dataset — Future Tech Specification (roadmap)

**Created:** 2026-06-24 · **Feeds:** Customer Tech (CT-T2/T3), Business Enabling, Planning leader · **source = SIMULATION** (fictional)

The roadmap parts that meet (or miss) the `customer_tech_demand.md` asks. All specs fictional/
illustrative — for simulation only, not a real SK hynix roadmap.

## Schema (payload)

| Field | Type | Meaning |
|---|---|---|
| `family` | enum | DDR5 · LPDDR5X · LPDDR6 · HBM3E · HBM4 |
| `spec_name` | string | part/bin name |
| `data_rate` | string | speed |
| `io_width` | string | interface width |
| `capacity` | string | die / stack capacity |
| `bandwidth_gbps` | number | per device/stack (sim) |
| `power_index` | string | relative power (1.0 = current gen) |
| `status` | enum | production · sampling · roadmap |
| `target_mp` | quarter | mass-production target |

## Sample

| family | spec_name | data_rate | io_width | capacity | bandwidth_gbps | power_index | status | target_mp |
|---|---|---|---|---|---|---|---|---|
| HBM3E | HBM3E-12hi | 9.6 Gbps | 1024-bit | 36GB stack | 1229 | 1.00 | production | 2025Q4 |
| HBM4 | HBM4-48GB | 8.0 Gbps | 2048-bit | 48GB stack | 2048 | 0.85 | sampling | 2026Q4 |
| HBM4 | HBM4E-64GB | 10 Gbps | 2048-bit | 64GB stack | 2560 | 0.80 | roadmap | 2027Q4 |
| LPDDR5X | LPDDR5X-9600 | 9600 Mbps | x16/x32 | 24Gb die | 76.8 | 1.00 | production | 2026Q1 |
| LPDDR6 | LPDDR6-10667 | 10667 Mbps | x24 | 32Gb die | 102 | 0.85 | roadmap | 2027Q2 |
| DDR5 | DDR5-6400 MRDIMM | 6400 MT/s | 64/72-bit | 24Gb | 51.2 | 1.00 | production | 2026Q1 |
| DDR5 | DDR5-7200 | 7200 MT/s | 64-bit | 32Gb | 57.6 | 0.95 | sampling | 2026Q4 |

## Roadmap → demand fit (why this dataset matters)

| Customer ask (from tech demand) | Roadmap part | Fit |
|---|---|---|
| NVIDIA HBM4 48GB @ 2026Q4 | HBM4-48GB (sampling, MP 2026Q4) | tight — qual timing risk `#importance:high` |
| Apple LPDDR6 @ 2027Q2 | LPDDR6-10667 (roadmap, MP 2027Q2) | on track |
| Dell DDR5-6400 MRDIMM @ 2026Q3 | DDR5-6400 MRDIMM (production) | met |

## Notes

- This is the dataset the **Planning leader's roadmap deck** (D-PLN-ROADMAP) and the **Sales
  customer-meeting deck** (D-SAL-CUST, "roadmap fit" slide) draw from.
- `power_index` < 1.0 = better than current gen (lower power per bit).
