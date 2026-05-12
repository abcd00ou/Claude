# Chip Maker Segment — GPU Generation Roadmap

**Segment:** chip_maker  
**Type:** Technology Roadmap Thematic File  
**Last Updated:** 2025-06-05

---

## NVIDIA GPU Generation Roadmap

### 2027 (H2 FY2027) — Vera Rubin Platform; HBM4; TSMC N2 (implied)

> "We unveiled the NVIDIA Rubin platform, comprising six new chips to deliver up to a 10x reduction in inference token cost vs Blackwell. Production scheduled to commence in the second half of fiscal year 2027."

**Source:** NVIDIA Q4 FY2026 Earnings Press Release, NVIDIA Corporation, 2026-02-25

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:nvidia #date:2026-02-25 #importance:high #confidence:high #cross-ref:dram #cross-ref:foundry

---

### 2025–2026 — Blackwell B200 / GB200 NVL72; HBM3E; TSMC N4P/N3

> NVIDIA Blackwell B200 (TSMC N4P, 208B transistors) and GB200 NVL72 rack-scale system in volume production through FY2026. GB200 NVL72: 72 B200 GPUs, 120kW power, NVLink 5.0 interconnect.

**Source:** NVIDIA GTC 2024 Keynote, NVIDIA Corporation, 2024-03; NVIDIA FY2026 10-K, SEC EDGAR, 2026-02-25

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:nvidia #date:2024-03 #importance:high #confidence:high

---

### 2024 — Hopper H200; HBM3E Upgrade; TSMC N4

> NVIDIA H200 SXM5 upgraded H100 with HBM3E (141GB, 4.8 TB/s bandwidth), shipped to hyperscalers in 2024. First NVIDIA GPU with HBM3E; SK Hynix sole initial HBM3E supplier.

**Source:** NVIDIA H200 Datasheet, NVIDIA Corporation, 2024

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:nvidia #date:2024 #importance:high #confidence:high #cross-ref:dram

---

### 2022–2023 — Hopper H100; HBM3; TSMC N4

> NVIDIA H100 SXM5: first Transformer Engine with FP8, 80GB HBM3, 3.35 TB/s bandwidth, NVLink 4.0. Defined the baseline for AI training infrastructure 2023–2024.

**Source:** NVIDIA H100 GPU Architecture Whitepaper, NVIDIA Corporation, 2022-03

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:nvidia #date:2022-03 #importance:high #confidence:high

---

## AMD Instinct GPU Generation Roadmap

### 2026–2027 — MI455X; Samsung HBM4; TSMC (CoWoS next-gen)

> AMD MI455X confirmed to use Samsung HBM4, differentiating from MI450 (SK Hynix HBM3E). Development phase; 2027 production target.

**Source:** Samsung Q1 2026 Earnings Call, 2026-04-30; AMD Q1 2026 Earnings Call, 2026-04-29

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:amd #company:samsung #date:2026-04-30 #importance:high #confidence:high #cross-ref:dram

---

### 2026 — MI450 (CDNA4); SK Hynix HBM3E; 6 GW Commitments from Meta and OpenAI

> AMD MI450 (CDNA4) secured 6 GW commitments each from Meta and OpenAI — largest publicly disclosed AI chip purchase agreements by wattage outside NVIDIA.

**Source:** AMD Q1 2026 Earnings Call, 2026-04-29; Meta Q1 2026 Earnings Call, 2026-04-29

#segment:chip_maker #source-tier:A #signal-type:design-win #company:amd #date:2026-04-29 #importance:high #confidence:high

---

### 2025 — MI350 (CDNA3+); Ramping; 8 Hyperscaler Customers

> AMD MI350 ramping in 2025, targeting performance parity with NVIDIA H100 at lower cost. 8 hyperscalers publicly deploying Instinct series.

**Source:** AMD Q4 2024 Earnings Call, AMD Investor Relations, 2025-01-28

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:amd #date:2025-01-28 #importance:high #confidence:high

---

### 2024 — MI300X (CDNA3); 192GB HBM3; Inference Leader

> AMD MI300X launched with 192GB HBM3 — 2.4× NVIDIA H100's 80GB. Established AMD as inference leader on memory capacity, with Azure, Meta, Oracle, Google deploying.

**Source:** AMD MI300X Product Brief, AMD Corporation, 2024; AMD Q1 2024 Earnings Call, AMD Investor Relations, 2024-04

#segment:chip_maker #source-tier:A #signal-type:roadmap #company:amd #date:2024 #importance:high #confidence:high

---

## Per-Generation HBM Content Comparison

| GPU | HBM Gen | Capacity | Bandwidth | Supplier |
|---|---|---|---|---|
| NVIDIA A100 | HBM2e | 80GB | 2.0 TB/s | SK Hynix |
| NVIDIA H100 | HBM3 | 80GB | 3.35 TB/s | SK Hynix |
| NVIDIA H200 | HBM3E | 141GB | 4.8 TB/s | SK Hynix |
| NVIDIA B200 | HBM3E | 192GB | 8.0 TB/s | SK Hynix / Micron |
| AMD MI300X | HBM3 | 192GB | 5.3 TB/s | Samsung |
| AMD MI450 | HBM3E | TBD | TBD | SK Hynix |
| AMD MI455X | HBM4 | TBD | TBD | Samsung |
| NVIDIA Vera Rubin | HBM4 | TBD | TBD | Micron (confirmed) |

**Source:** NVIDIA and AMD product datasheets, earnings calls; Samsung Q1 2026 Earnings, 2026-04-30; Micron FQ2 2026 Earnings, 2026-03-18

#segment:chip_maker #source-tier:A #signal-type:roadmap #date:2026-04-30 #importance:high #confidence:high #cross-ref:dram
