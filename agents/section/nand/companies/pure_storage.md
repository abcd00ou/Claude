# Pure Storage

**Segment(s):** storage
**Role in AI SCM:** All-flash enterprise storage for AI training, checkpointing, and unstructured data; certified NVIDIA DGX SuperPOD partner; subscription/evergreen model; ~$3.2B revenue (FY2025)
**HQ:** Mountain View, California, USA
**Ticker:** NYSE:PSTG
**Last Updated:** 2026-06-08

---

## Company Overview

Pure Storage is the leading all-flash enterprise storage vendor, offering FlashArray (block storage) and FlashBlade (file/object storage) platforms purpose-built for performance-intensive workloads including AI training, checkpointing, and inference. Its Evergreen subscription model allows customers to upgrade hardware without data migration or downtime. In 2025, Pure expanded into hyperscaler licensing — monetizing its DirectFlash and Purity OS IP — and secured a design win at Meta for massive-scale AI storage.

**Source:** Pure Storage FY2025 Earnings, 2025-02-27; Pure Storage Investor Day 2025

---

## Key Products & AI Relevance

| Product / Technology | AI Use Case | Market Position |
|---|---|---|
| FlashArray//XL | AI training dataset storage, model checkpointing (block) | Flagship high-density all-flash array |
| FlashBlade//S (S200/S500) | Unstructured AI data, parallel training, NFS/S3 storage | Certified with NVIDIA DGX SuperPOD (2024) |
| FlashBlade//EXA | Ultra-high-performance AI/HPC storage; >10 TB/s read in single namespace | Launched March 2025; generally available summer 2025 |
| Portworx (acquired 2020) | Kubernetes-native persistent storage for containerized AI pipelines | Market leader in K8s data services |
| Evergreen//One | Storage-as-a-service with guaranteed performance SLA | AI/cloud consumption model |
| DirectFlash + Purity OS (licensed) | Hyperscaler-scale AI storage software; IP licensing to cloud providers | Meta design win 2025 |
| Pure Storage GenAI Pod | Turnkey validated AI stack with NVIDIA, Arista, Cisco, Red Hat | GA H1 2025 |

**Source:** Pure Storage Product Pages 2025; FlashBlade//EXA Press Release, 2025-03-11; Pure//Accelerate, 2025-06-18

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
| Total Revenue | $1.002B | FY2020 (ended Feb 2020) | Pure Storage FY2020 Annual Report |
| Total Revenue | $1.684B | FY2021 (ended Jan 2021) | Pure Storage FY2021 Annual Report |
| Total Revenue | $2.180B | FY2022 (ended Jan 2022) | Pure Storage FY2022 Annual Report |
| Total Revenue | $2.570B | FY2023 (ended Jan 2023) | Pure Storage FY2023 Annual Report |
| Total Revenue | $2.827B | FY2024 (ended Feb 2024) | Pure Storage FY2024 Annual Report |
| Total Revenue | $3.162B (+12% YoY) | FY2025 (ended Feb 2025) | Pure Storage FY2025 Earnings, 2025-02-27 |
| Subscription Services Revenue | $1.5B (+22% YoY) | FY2025 | Pure Storage FY2025 Earnings, 2025-02-27 |
| ARR (Annual Recurring Revenue) | ~$1.8B | FY2025 | Pure Storage FY2025 Earnings, 2025-02-27 |
| Subscription % of Revenue | ~47% | FY2025 | Pure Storage FY2025 Earnings, 2025-02-27 |

**Source:** Pure Storage SEC filings; MacroTrends PSTG revenue history; blocksandfiles.com, 2025-02-27

---

## Supply Chain Position

Pure Storage designs proprietary DirectFlash Modules (DFMs) using raw NAND sourced from major suppliers (Samsung, Kioxia, Micron, SK Hynix, WD). Pure bypasses the traditional SSD controller layer by connecting NAND directly to its Purity OS, enabling higher endurance and performance. This makes Pure a significant NAND customer but an independent storage system vendor.

**Key customers:** Meta (DirectFlash hyperscaler design win); enterprise across financial services, healthcare, media, government; AI cloud builders
**Key suppliers:** NAND flash: Samsung, Kioxia, Micron, SK Hynix, WD/SanDisk; ASIC controllers: internally designed; hardware manufacturing: ODM partners
**Source:** Pure Storage FY2025 10-K; ainvest.com, 2025

---

## Investment & M&A

| Date | Event | Amount | Counter-party | AI Relevance | Source |
|---|---|---|---|---|---|
| 2020-09 | Acquired Portworx (Kubernetes data services platform) | $370M cash | Portworx Inc. | Enables persistent storage for containerized AI/ML pipelines on K8s | Pure Storage Press Release, 2020-09-16 |
| 2024-11 | FlashBlade//S500 certified with NVIDIA DGX SuperPOD | N/A (partnership) | NVIDIA | Reference architecture for enterprise AI training clusters | CDOTrends / Pure Storage, 2024-11 |
| 2025-03 | Pure Storage GenAI Pod validated designs launched | N/A (ecosystem) | NVIDIA, Arista, Cisco, Red Hat, Meta, SuperMicro | Turnkey AI infrastructure pod | Pure Storage Press Release, 2025-03 |
| 2025 | Hyperscaler Licensing — DirectFlash + Purity OS IP licensing | Undisclosed | Meta (first known) | High-margin software licensing for hyperscaler-scale AI storage | ainvest.com, 2025 |

**Source:** Pure Storage Press Releases; ainvest.com, 2025; stocktitan.net, 2024-11-18

---

## Technology Roadmap

| Milestone | Timeline | Status | Source |
|---|---|---|---|
| FlashBlade//S500 — NVIDIA DGX SuperPOD certification | 2024-11 | Completed | Pure Storage / CDOTrends, 2024-11 |
| FlashBlade//EXA — >10 TB/s single-namespace AI/HPC storage | Summer 2025 | GA | Pure Storage Press Release, 2025-03-11 |
| FlashBlade//S R2 — 30% AI pipeline performance improvement | June 2025 | Launched | Pure//Accelerate, 2025-06-18 |
| FlashArray next-gen — high-performance block AI storage | June 2025 | Launched | Pure//Accelerate, 2025-06-18 |
| DirectFlash hyperscaler licensing expansion | 2025 ongoing | In progress | ainvest.com, 2025 |

---

## Updates

### Update: 2025-02-27 — FY2025 Revenue $3.162B; First Year Above $3B; Subscription ARR $1.8B

> Pure Storage crossed $3B in annual revenue for the first time in FY2025, reporting $3.162B total revenue (+12% YoY). Subscription services revenue reached $1.5B (+22%), with ARR growing to ~$1.8B. FlashBlade demand from AI workloads and the Meta DirectFlash design win were cited as key growth drivers. Faster AI storage platforms (FlashBlade//EXA) were announced.

**Source:** Pure Storage FY2025 Q4 Earnings, 2025-02-27; blocksandfiles.com, 2025-02-27
#segment:storage #source-tier:A #signal-type:demand #company:pure_storage #date:2025-02-27 #importance:high #confidence:high

---

### Update: 2025-03-11 — FlashBlade//EXA Launched; >10 TB/s for AI/HPC

> Pure Storage introduced FlashBlade//EXA, targeting the highest-performance AI training and HPC storage requirements. The platform delivers more than 10 terabytes per second read performance in a single namespace, with significantly improved metadata performance and parallelism for GPU cluster utilization during training and checkpointing.

**Source:** Pure Storage Press Release, purestorage.com, 2025-03-11
#segment:storage #source-tier:A #signal-type:capacity #company:pure_storage #date:2025-03-11 #importance:high #confidence:high

---

### Update: 2025 — Meta DirectFlash Design Win; Hyperscaler IP Licensing Strategy

> Pure Storage secured a design win at Meta, bringing its DirectFlash software into hyperscaler-scale environments traditionally dominated by HDDs. Pure expanded this into a hyperscaler licensing model, where large cloud providers license Purity OS and DirectFlash technology — representing a high-margin IP-first revenue stream distinct from hardware sales.

**Source:** ainvest.com, 2025; markets.financialcontent.com, 2026-01-02
#segment:storage #source-tier:B #signal-type:demand #company:pure_storage #date:2025-01-01 #importance:high #confidence:medium

---

### Update: 2026-05-27 — FY2027 Q1: Revenue $1.053B (+35% YoY); Product Revenue +55%; FY2027 Guidance $4.41–4.51B

> Pure Storage reported FY2027 Q1 (quarter ended April 2026) total revenue of $1.053B, up 35% YoY — fastest growth pace in several quarters. Product revenue grew 55% YoY. Subscription services revenue +17% YoY, comprising 45% of total revenue. Operating profit grew >90% YoY. FlashBlade//EXA and CoreWeave partnership for standardized AI storage highlighted. Full-year FY2027 guidance raised to $4.41–4.51B. Stock rose ~10% on results.

**Source:** Pure Storage 8-K / Investing.com earnings transcript, 2026-05-27
#segment:storage #source-tier:A #signal-type:earnings #company:pure_storage #date:2026-05-27 #importance:high #confidence:high

---

## Open Questions

- [ ] Meta design win scale — how many exabytes? Revenue contribution to hyperscaler licensing?
- [ ] FlashBlade//EXA pricing vs. competing all-flash scale-out (IBM Spectrum Scale, VAST Data, WekaIO)?
- [ ] DirectFlash hyperscaler licensing: additional cloud customers beyond Meta?
- [ ] CoreWeave partnership scope — exclusive? Revenue contribution in FY2027?
