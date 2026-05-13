# ROI Calculator - DDR5 / MRDIMM Attach

**Use case:** OEM, ODM, cloud, and enterprise AI server attach-rate expansion.

## Inputs

| Field | Value | Notes |
|---|---:|---|
| AI servers planned |  | Account forecast |
| DIMMs per server |  | Platform BOM |
| ASP per DIMM |  | Pricing owner input |
| Gross margin per DIMM |  | Finance input |
| Current attach share |  | Sales baseline |
| Target attach share |  | Campaign target |
| Higher-density mix uplift |  | Product marketing estimate |

## Formulas

```text
DIMM TAM = AI Servers Planned * DIMMs Per Server
Incremental Units = DIMM TAM * (Target Attach Share - Current Attach Share)
Incremental Revenue = Incremental Units * ASP Per DIMM
Incremental Gross Profit = Incremental Units * Gross Margin Per DIMM
Mix Uplift Revenue = Incremental Revenue * Higher Density Mix Uplift
```

## Decision Rule

Prioritize accounts where:

```text
Incremental Revenue is high AND qualification timing is before BOM lock
```
