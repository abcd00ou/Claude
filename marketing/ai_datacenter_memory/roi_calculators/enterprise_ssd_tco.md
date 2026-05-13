# ROI Calculator - Enterprise SSD / AI Retrieval TCO

**Use case:** Shift customer discussion from price per GB to AI workload economics.

## Inputs

| Field | Value | Notes |
|---|---:|---|
| PB deployed |  | Customer forecast |
| Price per TB |  | Pricing input |
| Power per TB |  | Product spec |
| Energy cost per kWh |  | Customer region |
| Drive endurance |  | Product spec |
| Annual replacement rate |  | Reliability estimate |
| Retrieval requests per day |  | Workload estimate |
| Cost of latency / failed retrieval |  | Customer estimate |

## Formulas

```text
Hardware Cost = PB Deployed * 1000 * Price Per TB
Annual Energy Cost = PB Deployed * 1000 * Power Per TB * 24 * 365 * Energy Cost Per kWh
Replacement Cost = Hardware Cost * Annual Replacement Rate
Annual TCO = Hardware Cost + Annual Energy Cost + Replacement Cost
Cost Per Retrieval = Annual TCO / (Retrieval Requests Per Day * 365)
```

## Decision Rule

Lead with TCO if:

```text
Power, endurance, or latency savings outweigh price-per-GB disadvantage
```
