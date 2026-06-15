# Google TPU (Tensor Processing Unit)

**Segment(s):** asic  
**Role in AI SCM:** World's largest captive AI accelerator fleet; TPU v5 + TPU 8 generation in production; ~2M+ chips deployed  
**HQ:** United States (Mountain View, CA)  
**Ticker:** NASDAQ:GOOGL (Alphabet)  
**Last Updated:** 2026-05-18

---

## Company Overview

Google's Tensor Processing Unit (TPU) program is the world's largest and longest-running custom AI ASIC program, beginning internal deployment in 2015 and publicly available via Google Cloud since 2018. Google's TPU fleet underpins all Gemini model training and inference, as well as Google Search, YouTube recommendations, and Google Cloud AI services. TPUs are designed in-house at Google and manufactured at TSMC. The latest generation (TPU 8t for training, TPU 8i for inference) entered production in 2025.

**Source:** Google Q1 2026 Earnings, 2026-04-29; Google I/O 2024; Google Cloud Next 2025

---

## Key Products & AI Relevance

| Product / Technology | AI Use Case | Market Position |
|---|---|---|
| TPU v5e (2023) | Inference-optimized; cost-efficient | In production; Google Cloud public offering |
| TPU v5p (2024) | Large model training (Gemini Ultra) | In production; 459 TFLOPS BF16; 96GB HBM2e |
| TPU 8t (training, 2025) | Frontier model training | In production; TSMC N3 generation |
| TPU 8i (inference, 2025) | High-throughput AI inference | In production; Google Cloud offering |
| Google Ironwood / TPU v7 (2025–2026) | Inference at scale; superpod 9,216 chips = 42.5 ExaFLOPS | GA on Google Cloud (US/EU/APAC); TSMC N3P; 2 chiplets/chip; 192 GB HBM3E (2×96 GB); 7.37 TB/s; CoWoS via MediaTek; ~1M chips planned 2026 |
| TPU 8t "Sunfish" (training, ~2027) | Frontier model training (next gen) | Announced; targeting TSMC N2; late 2027 |
| TPU 8i "Zebrafish" (inference, ~2027) | High-throughput inference (next gen) | Announced; targeting TSMC N2; late 2027 |

**Source:** Google Cloud Next 2025; Google Q1 2026 Earnings, 2026-04-29; Google I/O 2024

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
| Google Cloud Revenue | $12.26B (+28% YoY) | Q1 2026 (Jan–Mar 2026) | Google Q1 2026 Earnings, 2026-04-29 |
| Google Cloud Backlog | $462B | Q1 2026 | Google Q1 2026 Earnings, 2026-04-29 |
| Alphabet Capex | $35.7B (+107% YoY) | Q1 2026 | Google Q1 2026 Earnings, 2026-04-29 |
| TPU Fleet Size (est.) | ~2M+ chips | 2025 estimate | Industry analyst estimates, 2025 |

---

## Supply Chain Position

Google designs TPUs internally (Google DeepMind + Google Brain hardware teams). Manufacturing is at TSMC (N3/N4 for TPU 8 generation, N5 for TPU v5). HBM for TPU v5p is sourced from SK Hynix and Samsung (HBM2e/HBM3). Google's Andromeda AI networking fabric (custom ICI — Inter-Chip Interconnect) connects TPU pods. Google is both the world's largest consumer of its own ASIC and a cloud provider offering TPU access to external customers.

**Key customers (publicly stated):** Internal (Google Search, YouTube, Gemini); external via Google Cloud (available as cloud TPUs)  
**Key suppliers (publicly stated):** TSMC (fabrication), SK Hynix / Samsung (HBM)

**Source:** Google Cloud Next 2025; Google 10-K FY2024, 2025-02-04

---

## Technology Roadmap

| Milestone | Timeline | Status | Source |
|---|---|---|---|
| TPU v4 (32GB HBM, 275 TFLOPS BF16) | 2021 | In production / legacy | Google I/O 2021 |
| TPU v5e (inference-optimized) | 2023 | Volume production | Google Cloud Next 2023 |
| TPU v5p (training; 96GB HBM2e) | 2024 | Volume production | Google I/O 2024 |
| TPU 8t (training, TSMC N3) | 2025 | In production | Google Q1 2026 Earnings, 2026-04-29 |
| TPU 8i (inference, TSMC N3) | 2025 | In production | Google Q1 2026 Earnings, 2026-04-29 |
| Google Ironwood / TPU v7 (TSMC N3P, CoWoS) | 2025–2026 | GA (US/EU/APAC); ~1M chips planned 2026 | Google Cloud Next 2026; ServeTheHome; Jon Peddie Research |
| TPU 8t "Sunfish" (training, TSMC N2) | Late 2027 | Announced | Google Cloud Next 2026 |
| TPU 8i "Zebrafish" (inference, TSMC N2) | Late 2027 | Announced | Google Cloud Next 2026 |

---

## Competitive Position

| Competitor | Segment | Key Differentiator (stated by company or analyst) | Source |
|---|---|---|---|
| NVIDIA H100/B200 | AI training / inference | CUDA ecosystem moat; third-party availability | NVIDIA Q1 FY2026 Earnings |
| Amazon Trainium3 | Custom AI training ASIC | AWS-captive; available via Bedrock | Amazon Q1 2026 Earnings |
| Microsoft Maia 200 | Custom AI inference | Azure-captive; 30%+ tokens/dollar improvement | Microsoft Q3 FY2026 Earnings |

---

## Updates

### Update: 2026-05 — Google Cloud Next 2026: Ironwood (TPU v7) confirmed TSMC N3P, CoWoS via MediaTek, 2-chiplet architecture; ~1M chips 2026; Anthropic 1M TPU / 1GW allocation; next gen "Sunfish"/"Zebrafish" on TSMC N2

> Google Cloud Next 2026 confirmed full Ironwood (TPU v7) specifications and general availability across US, EU, and APAC regions. Process node: TSMC N3P (3nm). Packaging: CoWoS via MediaTek-TSMC partnership — MediaTek acts as volume production coordinator. Architecture: 2 chiplets per chip, each with 1 TensorCore + 2 SparseCores. Memory: HBM3E, 192 GB per chip (two chiplets × 96 GB each), 7.37 TB/s bandwidth — 4.5× Trillium (TPU v6e). Superpod: 9,216 chips = 42.5 ExaFLOPS aggregate. ~1 million Ironwood chips planned for deployment in 2026 (400K first phase via Google Cloud); up to 1 GW of Ironwood capacity accessible through Google Cloud in 2026. Anthropic allocated up to 1M TPU chips + 1 GW capacity in 2026. Next-generation confirmed: TPU 8t "Sunfish" (training) and TPU 8i "Zebrafish" (inference) — both targeting TSMC N2, late 2027.

**Source:** Google Cloud Blog; ServeTheHome; Jon Peddie Research; Google Cloud TPU docs; The Next Web, 2026-05

#segment:asic #source-tier:A #signal-type:supply #company:google_tpu #date:2026-05 #importance:high #confidence:high #cross-ref:foundry #cross-ref:dram #cross-ref:end_market

---

### Update: 2026-04-29 — Q1 2026: Cloud backlog $462B; TPU 8t + TPU 8i in production; Ironwood announced

> Google Q1 2026 earnings (April 29, 2026): Google Cloud revenue $12.26B (+28% YoY); backlog $462B, guiding for continued 2027 growth. CEO Sundar Pichai confirmed TPU 8t (training) and TPU 8i (inference) are in production and available on Google Cloud. Google Ironwood — the next-generation inference-optimized TPU — was announced for future cloud availability. Alphabet capex $35.7B (+107% YoY), primarily data center and TPU manufacturing capacity.

**Source:** Google Q1 2026 Earnings, 2026-04-29

#segment:asic #source-tier:A #signal-type:demand #company:google_tpu #date:2026-04-29 #importance:high #confidence:high

### Update: 2024 — TPU v5p in volume production; 8,960-chip clusters confirmed

> Google announced TPU v5p clusters of up to 8,960 chips at Google Cloud Next 2024. TPU v5p delivers 459 TFLOPS BF16 per chip with 96GB HBM2e and 4.8 TB/s bandwidth. The ICI (Inter-Chip Interconnect) fabric connects TPU v5p pods at 1.6 Tbps per chip. TPU v5p is Google's primary chip for Gemini Ultra training.

**Source:** Google Cloud Next 2024; Google I/O 2024

#segment:asic #source-tier:A #signal-type:supply #company:google_tpu #date:2024 #importance:high #confidence:high

---

### Update: 2025-11 — Google Ironwood (7th Gen TPU) GA: 4,614 FP8 TFLOPS/chip; 192 GB HBM3E; 9,216-Chip Pod = 42.5 ExaFLOPS

> Google Ironwood (7th-generation TPU) reached general availability in November 2025. Specifications: 4,614 FP8 TFLOPS per chip; 192 GB HBM3E per chip; 7.37 TB/s memory bandwidth per chip (4.5× previous Trillium generation); die size 700 mm². Pod scale: 9,216 chips = 42.5 ExaFLOPS. TSMC fabrication confirmed; specific node not disclosed in public filings (not N3/N4 confirmed; TSMC N2 reported for next generation — TPU 8t "Sunfish" / TPU 8i "Zebrafish" — targeted late 2027). Ironwood was first announced at Google Cloud Next in April 2025 and reached GA in November 2025.

**Source:** Google Cloud Blog, 2025-04 and 2025-11; TrendForce, 2025-11-07; The Register, 2025-11-06; ServeTheHome, 2025; The Next Web, 2025

#segment:asic #source-tier:A #signal-type:supply #company:google_tpu #date:2025-11 #importance:high #confidence:high

---

## Open Questions

- [x] Google Ironwood specs — **resolved**: 4,614 FP8 TFLOPS, 192 GB HBM3E, 7.37 TB/s, 9,216-chip pod = 42.5 ExaFLOPS (GA November 2025)
- [x] Google Ironwood process node — **resolved**: TSMC N3P (confirmed Google Cloud Next 2026)
- [x] Google Ironwood packaging — **resolved**: CoWoS via MediaTek-TSMC partnership; MediaTek coordinates volume production (confirmed Google Cloud Next 2026)
- [x] TPU 8t "Sunfish" / TPU 8i "Zebrafish" (next gen) node — **resolved**: TSMC N2 confirmed; late 2027 target (Google Cloud Next 2026)
- [ ] TPU 8t/8i (current in-production gen): TSMC node not confirmed — N3B, N3E, or N3P?
- [ ] TPU fleet total deployed chip count — 2M estimate from analysts; has Google disclosed?
- [ ] How does Google's TPU capex split between internal use vs cloud customer-facing capacity?
