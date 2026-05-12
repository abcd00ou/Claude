# Market Data Master — AI Supply Chain

**Last Updated:** 2026-05-12 (Cycle 3)  
**Coverage:** Pricing, capacity, market share, capex across all segments

---

## Memory Pricing (DRAM)

| Product | Price ($/GB) | Direction | Period | Source |
|---|---|---|---|---|
| HBM3E | $15–18/GB | Structurally elevated | Q1 2026 | TF International Securities, 2026-Q1 |
| DDR5 Server DRAM | $3–5/GB | +90–95% QoQ | Q1 2026 | Samsung Q1 2026 Earnings, 2026-04-30 |
| DDR5 Spot | ~$3.50/8Gb equiv. | Recovering from 2023 trough | 2023 trough | DRAMeXchange, 2023-Q2 |
| LPDDR5X | ~$4–6/GB | Stable | 2025 | Industry pricing data |

**HBM pricing mechanics:**
- No spot market — 100% contract allocation
- Locked 4–6 quarters in advance
- SK Hynix: 3-year demand exceeds supply → no ASP compression risk before 2029

---

## Storage Pricing (NAND)

| Product | Price | Direction | Period | Source |
|---|---|---|---|---|
| Enterprise NVMe SSD (PCIe Gen4, 4TB) | $0.08–0.10/GB | +55–75% QoQ | Q1 2026 | Samsung Q1 2026; TrendForce 2026-Q1 |
| Enterprise NVMe SSD (PCIe Gen5, 4TB) | $0.10–0.13/GB | Premium over Gen4 | 2025–2026 | Industry pricing |
| QLC NAND Wafer | ~$2.20–2.60/128Gb equiv. | Recovery | 2025 | TrendForce 2025-Q4 |
| QLC NAND Wafer (2023 trough) | $1.50–1.80/128Gb | Below cash cost | 2023-Q2 | DRAMeXchange, 2023-Q2 |

---

## AI Accelerator Pricing

| Product | List Price (est.) | Form Factor | Source |
|---|---|---|---|
| NVIDIA H100 SXM5 | ~$30–35K | SXM5 module | Industry pricing, 2023–2024 |
| NVIDIA B200 | ~$35–40K | SXM6 module | Goldman Sachs AI Report, 2025-Q4 |
| NVIDIA GB200 NVL72 rack | ~$3–4M | Full rack system | Industry estimate, 2025 |
| AMD MI300X | ~$15–20K | OAM module | TF International Securities, 2025-Q3 |
| H100 cloud rental | $2.00–3.50/hr | GPU-hour | Cloud pricing pages, 2024-Q4 |

---

## Hyperscaler Capex — CY2026

| Company | CY2026 Guidance | Q1 2026 Actual | YoY Q1 Growth | Source |
|---|---|---|---|---|
| Amazon | ~$200B | $43.2B | — | Q1 2026 Earnings, 2026-05-01 |
| Microsoft | ~$190B | $31.9B | +49% | Q3 FY2026 Earnings, 2026-04-29 |
| Alphabet | Up to $190B | $35.7B | +107% | Q1 2026 Earnings, 2026-04-29 |
| Meta | $125–145B | $19.8B | — | Q1 2026 Earnings, 2026-04-29 |
| **Total** | **$705–725B** | **~$130.6B** | — | Combined |

**Component pricing inflation:** Microsoft +$25B, Meta +$10B above initial guidance — driven by memory ASP increases

---

## Market Share — Key Segments

### HBM Market Share (CY2026)

| Supplier | Share | Notes |
|---|---|---|
| SK Hynix | ~57% | NVIDIA primary; HBM4 in production |
| Samsung | ~35% | AMD MI455X HBM4 partner; 2026 fully sold out |
| Micron | ~8% | Vera Rubin HBM4 confirmed; growing |

### NAND Bit Share (CY2026)

| Supplier | Bit Share | Notes |
|---|---|---|
| Samsung | ~31% | Full vertical integration |
| Kioxia | ~19% | WD joint fab; IPO Dec 2024 |
| SK Hynix / Solidigm | ~19% | Enterprise SSD focus |
| Micron | ~14% | Gen5 NVMe growing |
| YMTC | ~9% | China-domestic only |

### Foundry Revenue Share

| Foundry | Revenue Share | AI Node |
|---|---|---|
| TSMC | ~64% | N3/N2/CoWoS |
| Samsung Foundry | ~13% | 3nm (yield issues) |
| GlobalFoundries | ~6% | Mature nodes |
| Intel Foundry | ~4% | 18A (sampling) |

### AI Accelerator DC Revenue Share

| Company | Share (est.) | Notes |
|---|---|---|
| NVIDIA | ~75–85% | $39.1B in Q1 FY2026 alone |
| AMD | ~10–15% | $5.8B Q1 2026 |
| Google (internal TPU) | ~5% captive | Not sold externally at full revenue |
| Custom ASIC (Marvell/Broadcom) | Growing | $5.5B/Q combined AI revenue |

### ABF Substrate Market Share

| Supplier | Revenue Share | AI Exposure |
|---|---|---|
| Unimicron | ~25% | AMD + TSMC CoWoS ecosystem |
| Ibiden | ~20% | NVIDIA primary |
| Shinko Electric | ~15% | Intel captive |
| AT&S | ~10% | TSMC + Intel |
| Kinsus | ~10% | AMD/NVIDIA |

---

## Supply Lead Times (as of Q1 2025)

| Component | Lead Time | Direction | Binding Constraint |
|---|---|---|---|
| HBM (DRAM) | Allocated 4–6 quarters ahead | Structural allocation | Yes — all CY2026 committed |
| TSMC CoWoS | Demand > capacity by 20–30% | No relief until capex lands | Yes |
| ABF Substrate (AI grade) | 20–24 weeks | Fully allocated | Yes — Ibiden/Unimicron at capacity |
| Power Transformers | 52–65 weeks | No meaningful improvement | Yes — AI DC deployment bottleneck |
| Direct Liquid Cooling | 28–36 weeks (improved) | Improving: was 40–52wk | Easing |
| NVIDIA NDR InfiniBand | 12–16 weeks (improved) | Improving: was 20–24wk | Easing |
| Enterprise SSD (Gen5) | 8–12 weeks | Normal | No |

---

## Power Content per AI System (BOM)

| System | Power Semi Content | vs Standard Server |
|---|---|---|
| Standard 1U server | $15–25 | baseline |
| AI GPU server (8× H100) | $80–120 | 4–6× |
| AI rack system (GB200 NVL72) | $500–800+ | 25–35× |

**Source:** IHS Markit Power Semiconductor Content Report, 2025-Q4; MPS Q4 2024 Earnings, 2025-02-05

---

## HBM Content Per GPU Generation

| GPU | HBM Gen | Capacity | Bandwidth | Stacks per Chip |
|---|---|---|---|---|
| NVIDIA A100 | HBM2e | 80GB | 2.0 TB/s | 5 |
| NVIDIA H100 | HBM3 | 80GB | 3.35 TB/s | 5 |
| NVIDIA H200 | HBM3E | 141GB | 4.8 TB/s | 6 |
| NVIDIA B200 | HBM3E | 192GB | 8.0 TB/s | 8 |
| AMD MI300X | HBM3 | 192GB | 5.3 TB/s | 8 |
| NVIDIA Vera Rubin | HBM4 | TBD | TBD | TBD |
| AMD MI455X | HBM4 | TBD | TBD | TBD |
