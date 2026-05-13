# ROI Calculator - HBM Allocation

**Use case:** Executive discussion for GPU/ASIC platform launch risk.

## Inputs

| Field | Value | Notes |
|---|---:|---|
| Planned accelerator units |  | Customer forecast |
| HBM stacks per accelerator |  | Platform BOM |
| HBM ASP per stack |  | Pricing owner input |
| Platform revenue per deployed accelerator |  | Sales/customer estimate |
| Delay risk in weeks |  | Account team estimate |
| Revenue lost per delayed week |  | Customer or sales estimate |
| Allocation premium |  | Pricing owner input |
| LTA duration |  | Months or years |

## Formulas

```text
Total HBM Stacks = Planned Accelerator Units * HBM Stacks Per Accelerator
HBM Revenue = Total HBM Stacks * HBM ASP Per Stack
Delay Cost Avoided = Delay Risk Weeks * Revenue Lost Per Delayed Week
Commercial Value = HBM Revenue + Delay Cost Avoided
```

## Decision Rule

Recommend LTA/allocation discussion if:

```text
Delay Cost Avoided > Discount Requested
```
