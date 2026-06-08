# Market Data Master — AI Supply Chain

**Last Updated:** 2026-06-08 (Cycle 9)  
**Coverage:** Pricing, capacity, market share, capex across all segments

---

## Memory Pricing (DRAM)

| Product | Price ($/GB) | Stack Price | Direction | Period | Source |
|---|---|---|---|---|---|
| HBM4 | ~$17–20/GB (est.) | ~$500–600/stack | New benchmark; all 3 vendors NVIDIA-certified June 5, 2026; 30%+ premium over HBM3E | Q2 2026 | TrendForce, 2025-12-24; NVIDIA certification statement, 2026-06-05 |
| HBM3E | $15–18/GB | ~$300/stack | +20% contract price increase for 2026 delivery | Q4 2025 | TrendForce, 2025-12-24; TF International Securities, 2026-Q1 |
| DDR5 Server DRAM | $3–5/GB | — | +90–95% QoQ | Q1 2026 | Samsung Q1 2026 Earnings, 2026-04-30 |
| DDR5 Spot | ~$3.50/8Gb equiv. | — | Recovering from 2023 trough | 2023 trough | DRAMeXchange, 2023-Q2 |
| LPDDR5X | ~$4–6/GB | — | Stable | 2025 | Industry pricing data |

**HBM pricing mechanics:**
- No spot market — 100% contract allocation
- Locked 4–6 quarters in advance
- SK Hynix: 3-year demand exceeds supply → no ASP compression risk before 2029
- HBM4 ramp delayed to Q3 2026 (SK Hynix 70% yield milestone; Micron ramp at 15K wafers/mo Q2 2026)
- HBM market size: ~$35B (2025) → ~$58B (2026) → ~$100B (2028) — Source: Silicon Analysts, Introl Blog, 2025–2026

---

## Storage Pricing (NAND)

| Product | Price | Direction | Period | Source |
|---|---|---|---|---|
| Enterprise NVMe SSD (PCIe Gen4, 4TB) | $0.13–0.17/GB | +70–75% QoQ (Q2 2026 second wave); +55–75% QoQ in Q1 | Q2 2026 | Samsung NAND pricing commentary, 2026-04-30; TrendForce 2026-Q2 |
| Enterprise NVMe SSD (PCIe Gen5, 4TB) | $0.16–0.22/GB | Premium over Gen4; growing demand for AI workloads | Q2 2026 | Industry pricing |
| QLC NAND Wafer | ~$3.20–3.80/128Gb equiv. | Sharp recovery driven by AI storage demand; structural deficit declared | Q2 2026 | TrendForce 2026-Q2; Kioxia sold-out commentary, 2026-05-24 |
| QLC NAND Wafer (2023 trough) | $1.50–1.80/128Gb | Below cash cost | 2023-Q2 | DRAMeXchange, 2023-Q2 |

**NAND structural signals (Q2 2026):**
- Kioxia: entire 2026 NAND sold out; BiCS10 (332-layer) sampling summer 2026
- Samsung Q2 2026 NAND prices: +70–75% QoQ (second wave price hike)
- Demand "significantly in excess of supply" — Micron FQ2 2026 earnings
- NVIDIA ICMSP NVMe standard emerging for AI DC workloads (June 2026)

---

## AI Accelerator Pricing

| Product | List Price (est.) | Form Factor | Source |
|---|---|---|---|
| NVIDIA H100 SXM5 | ~$30–35K | SXM5 module | Industry pricing, 2023–2024 |
| NVIDIA B200 | ~$35–40K | SXM6 module | Goldman Sachs AI Report, 2025-Q4 |
| NVIDIA GB200 NVL72 rack | ~$3–4M | Full rack system | Industry estimate, 2025 |
| NVIDIA GB300 NVL72 rack | ~$4–5M (est.) | Full rack system; +129% GB200 content upgrade | GB300 launch commentary, 2026-Q1 |
| AMD MI300X | ~$15–20K | OAM module | TF International Securities, 2025-Q3 |
| AMD MI450 | Sampling; pricing TBD | OAM module; 6 GW Meta + OpenAI commitment | AMD Q1 2026 Earnings, 2026-05-05 |
| H100 cloud rental | $2.00–3.50/hr | GPU-hour | Cloud pricing pages, 2024-Q4 |
| H200 / B200 cloud rental | $3.50–5.50/hr (est.) | GPU-hour; premium over H100 | Industry estimate, 2026 |

---

## Hyperscaler Capex — CY2026

| Company | CY2026 Guidance | Q1 2026 Actual | YoY Q1 Growth | Source |
|---|---|---|---|---|
| Amazon (AWS) | ~$200B | $44.2B | +77% YoY | Q1 2026 Earnings, 2026-04-29 |
| Microsoft (Azure) | ~$190B | $37.5B (FY Q3) | +53% YoY | FY Q3 2026 Earnings, 2026-04-29 |
| Alphabet (Google) | $180–190B | $35.7B | +107% | Q1 2026 Earnings, 2026-04-29 |
| Meta | $125–145B | $19.84B | +61% | Q1 2026 Earnings, 2026-04-29 |
| xAI | ~$30B (annualized) | $7.7B Q1 | — | xAI Series E filing, 2026-06-08 |
| **Big-4 Total** | **$695–715B** | **~$137.2B** | ~+70% avg | Combined |

**Key June 2026 signals:**
- Amazon Q1 AWS revenue $37.6B (+28% YoY); backlog $364B; Trainium commitments $225B
- Microsoft Azure AI ARR $37B (+123% YoY); first GB300 NVL72 cluster (4,608 GPUs)
- Google Cloud $20B (+63% YoY); TPU v7 Ironwood 4.3M chips; backlog $462B
- Meta +$10B raise vs initial guidance; 1 GW MTIA deployment committed; 8,000 layoffs alongside
- xAI: $20B Series E closed; Colossus 2 at 555K GPUs / 2 GW; implied valuation >$200B

---

## Market Share — Key Segments

### HBM Market Share

| Supplier | Share (Q2 2025) | Share (HBM4, CY2026) | Notes |
|---|---|---|---|
| SK Hynix | **62%** | ~60–62% | NVIDIA primary; NVIDIA-certified HBM4 June 5, 2026; 70% yield on 12-Hi; ramp Q3 2026 |
| Samsung | **17%** | ~mid-20% | HBM4 commercial Feb 2026; HBM4E samples May 29 (16 Gbps / 3.6 TB/s); NVIDIA-certified |
| Micron | **21%** | ~20% | NVIDIA-certified June 5, 2026; entire CY2026 HBM4 sold out; ramp 15K wafers/mo Q2 2026 |

**June 5, 2026 milestone:** All 3 HBM4 vendors (SK Hynix, Samsung, Micron) simultaneously NVIDIA-certified — first time all three certified for a single HBM generation.

**Source:** NVIDIA HBM4 certification statement, 2026-06-05; SK Hynix IR, 2026; Samsung IR, 2026-05-29; Micron IR, 2026-06-05

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

| Supplier | Revenue Share | AI Exposure | June 2026 Status |
|---|---|---|---|
| Unimicron | ~25% | AMD + TSMC CoWoS ecosystem | ~90% utilization; Hsinchu Phase 2 ramp ongoing |
| Ibiden | ~20% | NVIDIA primary | AI = 60%+ of electronics rev; Ogaki full capacity; new lines FY2027 |
| Shinko Electric | ~15% | Intel captive | CoWoS-compatible R&D underway; no external AI GPU win |
| AT&S | ~10% | TSMC + Intel | Kulim (Malaysia) 100% utilization; Kulim 2 approved |
| Kinsus | ~10% | AMD/NVIDIA | — |

**ABF structural deficit:** 10% supply shortfall H2 2026 → 42% by 2028; Ajinomoto ABF film price +30% Q3 2026

---

## Supply Lead Times (Updated Cycle 9 — June 2026 data)

| Component | Lead Time | Direction | Binding Constraint | Source |
|---|---|---|---|---|
| HBM4 (DRAM) | Allocated 4–6 quarters ahead | Structural allocation; all CY2026 committed; ramp Q3 2026 | Yes — SK Hynix +70% yield milestone required before volume | SK Hynix / Micron Q1 2026 |
| TSMC CoWoS | ~127–130K WPM end-2026 target (from ~75K) | Growing rapidly; SoIC-X 6μm now HVM | Yes — NVIDIA holds >60% of slots; AP7 Chiayi move-in 2026 | TSMC Q1 2026 Earnings, 2026-04-17 |
| Power Transformers (U.S.) | **128–160 weeks (2.5–3 years)** | Worsening; 7 GW US AI DC completions delayed | Yes — primary binding constraint on DC completions; $228 GW pipeline | Wood Mackenzie; Eaton Q1 2026 |
| ABF Substrate (AI grade) | 20–24 weeks; structurally: 10% deficit H2 2026 → 42% deficit by 2028 | Worsening; Ajinomoto +30% film price hike Q3 2026 | Yes — Ibiden + Unimicron at ~90% utilization; new capacity not until FY2027 | TechTicker; Ajinomoto IR, 2026 |
| 200G EML Laser (optical) | Severely constrained; primary bottleneck for 800G/1.6T transceivers | Primary bottleneck for AI networking scale-out | Yes — $26B optical market; 800G+ units 24M→63M demand | Coherent / Lumentum commentary, 2026 |
| Direct Liquid Cooling | DLC now default for new AI DC builds | Mainstream; Vertiv: "liquid cooling is default" | No — DLC now standard for AI racks | Vertiv Q1 2026, 2026-05-01 |
| NVIDIA Spectrum-X 400 Tb/s (Ethernet) | H2 2026 commercial availability | Ramping; deployed at Meta + Oracle | Easing — 67% AI back-end switch share | NVIDIA GTC 2026 |
| Enterprise SSD (Gen4/Gen5) | 8–12 weeks | Tightening on Gen5; structural NAND deficit declared | Tightening — NAND Q2 +70-75% QoQ | Micron / Kioxia Q1 2026 |

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
| NVIDIA GB300 (Blackwell Ultra) | HBM3E | 192GB+ | 8.0 TB/s+ | 8 |
| NVIDIA Vera Rubin (GR300) | HBM4 | TBD; 12-Hi stack | >4.0 TB/s target | TBD |
| AMD MI450 | HBM4 | TBD | TBD | TBD; sampling 2026 |
| Google Ironwood (TPU v7) | HBM | TBD (42.5 exaFLOPS/superpod) | — | — |
