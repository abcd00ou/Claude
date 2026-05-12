# Google TPU (Tensor Processing Unit)

**Segment(s):** asic  
**Role in AI SCM:** World's largest captive AI accelerator fleet; TPU v5 + TPU 8 generation in production; ~2M+ chips deployed  
**HQ:** United States (Mountain View, CA)  
**Ticker:** NASDAQ:GOOGL (Alphabet)  
**Last Updated:** 2026-04-29

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
| Google Ironwood (announced 2025) | Next-gen inference at scale | Announced; cloud availability TBD |

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
| Google Ironwood (next-gen inference) | 2025–2026 | Announced; timeline TBD | Google Cloud Next 2025 |

---

## Competitive Position

| Competitor | Segment | Key Differentiator (stated by company or analyst) | Source |
|---|---|---|---|
| NVIDIA H100/B200 | AI training / inference | CUDA ecosystem moat; third-party availability | NVIDIA Q1 FY2026 Earnings |
| Amazon Trainium3 | Custom AI training ASIC | AWS-captive; available via Bedrock | Amazon Q1 2026 Earnings |
| Microsoft Maia 200 | Custom AI inference | Azure-captive; 30%+ tokens/dollar improvement | Microsoft Q3 FY2026 Earnings |

---

## Updates

### Update: 2026-04-29 — Q1 2026: Cloud backlog $462B; TPU 8t + TPU 8i in production; Ironwood announced

> Google Q1 2026 earnings (April 29, 2026): Google Cloud revenue $12.26B (+28% YoY); backlog $462B, guiding for continued 2027 growth. CEO Sundar Pichai confirmed TPU 8t (training) and TPU 8i (inference) are in production and available on Google Cloud. Google Ironwood — the next-generation inference-optimized TPU — was announced for future cloud availability. Alphabet capex $35.7B (+107% YoY), primarily data center and TPU manufacturing capacity.

**Source:** Google Q1 2026 Earnings, 2026-04-29

#segment:asic #source-tier:A #signal-type:demand #company:google_tpu #date:2026-04-29 #importance:high #confidence:high

### Update: 2024 — TPU v5p in volume production; 8,960-chip clusters confirmed

> Google announced TPU v5p clusters of up to 8,960 chips at Google Cloud Next 2024. TPU v5p delivers 459 TFLOPS BF16 per chip with 96GB HBM2e and 4.8 TB/s bandwidth. The ICI (Inter-Chip Interconnect) fabric connects TPU v5p pods at 1.6 Tbps per chip. TPU v5p is Google's primary chip for Gemini Ultra training.

**Source:** Google Cloud Next 2024; Google I/O 2024

#segment:asic #source-tier:A #signal-type:supply #company:google_tpu #date:2024 #importance:high #confidence:high

---

## Open Questions

- [ ] Google Ironwood specs — TFLOPS, HBM capacity, bandwidth?
- [ ] TPU 8t/8i: what TSMC node (N3B, N3E, or N3P)?
- [ ] TPU fleet total deployed chip count — 2M estimate from analysts; has Google disclosed?
- [ ] How does Google's TPU capex split between internal use vs cloud customer-facing capacity?
