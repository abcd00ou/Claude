# NAND Flash & Storage Architecture — Academic Technical Reference

**Segment:** NAND Flash / Storage  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-12 (Cycle 5)  
**Sources:** IEEE ISSCC/IEDM/VLSI papers; JEDEC standards (JESD218, JESD219); NVMe specification; PCIe Base Specification; Kioxia, Samsung, Micron technical briefs

---

## 1. NAND Flash Cell Architecture

### Flash Cell Physics — Floating Gate and Charge Trap

> "NAND flash stores data as charge in an insulated (floating) gate or charge-trap layer above the silicon channel. In Floating Gate (FG) NAND, charge is stored in a polysilicon floating gate surrounded by oxide (ONO — oxide/nitride/oxide stack). In Charge Trap Flash (CTF), charge is stored in a silicon nitride (Si₃N₄) layer. CTF has become dominant in 3D NAND because it tolerates the thin ONO layers required for vertical stacking (e.g., Samsung V-NAND, Kioxia BiCS). Reading the cell involves measuring the threshold voltage (Vt) shift caused by stored charge."

**Source:** "Charge Trap Flash Memory for 3D NAND Applications," IEEE IEDM, Samsung, 2015; Kioxia BiCS Technology White Paper, Kioxia, 2021; "Three-Dimensional Floating Gate NAND Flash Memory," IEEE IEDM, Toshiba, 2007

#segment:storage #source-tier:S #signal-type:roadmap #date:2015 #importance:high #confidence:high

---

### SLC / MLC / TLC / QLC — Bits Per Cell Comparison

> "NAND flash cells can store multiple voltage levels to encode more than 1 bit per cell: SLC (1 bit, 2 voltage levels), MLC (2 bits, 4 levels), TLC (3 bits, 8 levels), QLC (4 bits, 16 levels). Each additional bit halves cell spacing between voltage thresholds, reducing noise margin and increasing program/erase P/E cycles required. Endurance comparison: SLC ~100,000 P/E cycles; MLC ~10,000; TLC ~3,000; QLC ~1,000. QLC enterprise SSDs (Samsung PM9C3a, Kioxia CD8P) achieve ~1,000 P/E with aggressive error correction (LDPC codes) and overprovisioning."

**Source:** JEDEC JESD218B (SSD Endurance Workloads Standard), JEDEC, 2021; "QLC NAND for Enterprise Storage," IEEE Flash Memory Summit, Micron, 2019; Kioxia CD8P Product Brief, 2024

#segment:storage #source-tier:S #signal-type:roadmap #date:2019 #importance:high #confidence:high

---

## 2. 3D NAND Stacking Architecture

### BiCS (Bit Cost Scalable) — Kioxia Vertical NAND

> "BiCS (Bit Cost Scalable) technology, invented by Toshiba (now Kioxia) in 2007, stacks NAND string cells vertically by replacing horizontal cell arrays with a vertical polysilicon channel pillar drilled through alternating conductor (wordline) and insulator layers. One BiCS 'string' contains 96–300+ cells stacked vertically above a single select gate. BiCS 8 (218-layer BiCS, Kioxia 2024) achieves approximately 8 Gb/mm² array density — 3× the density of planar NAND."

**Source:** "A Novel Three-Dimensional Flash Memory Cell Technology," IEEE VLSI Technology Symposium, Toshiba, 2007; Kioxia BiCS 8 Technology Introduction, Kioxia, 2024

#segment:storage #source-tier:S #signal-type:roadmap #date:2007 #importance:high #confidence:high

---

### V-NAND (Samsung) and 3D NAND Layer Count Race

> "Samsung's V-NAND (Vertical NAND) uses a similar vertical channel architecture to BiCS. Samsung V8 (2024) achieves 236 layers. The layer count race directly drives bit density improvement: doubling layer count approximately doubles bits per unit die area, reducing cost per GB. Current state-of-the-art (2025): Micron 276-layer; Samsung ~280+ layer (V9, sampling); Kioxia BiCS 9 (300+ layer, targeted 2026); Kioxia BiCS 10 (332-layer, expedited to 2026). Higher layer count requires taller etch aspect ratios — etch aspect ratio of 3D NAND holes exceeded 100:1 at 200+ layers, representing a key manufacturing challenge."

**Source:** "Samsung V-NAND Technology Overview," Samsung Semiconductor, 2022; Micron 276-Layer NAND Flash Technology Brief, Micron, 2024; Tom's Hardware NAND Layer Count Analysis, 2024

#segment:storage #source-tier:A #signal-type:roadmap #date:2024 #importance:high #confidence:high

---

## 3. NVMe Protocol Stack

### NVMe over PCIe — Architecture

> "NVMe (Non-Volatile Memory Express) is a host interface protocol designed for low-latency, high-parallelism access to NAND flash via PCIe. NVMe replaces SATA and SAS for performance SSDs. Key NVMe advantages over SATA: (1) up to 65,535 I/O queues (vs SATA: 1 queue); (2) up to 65,535 commands per queue depth (vs SATA: 32); (3) direct PCIe attachment eliminating AHCI overhead; (4) latency ~70µs vs SATA ~500µs. NVMe 1.4 (2019) introduced I/O determinism (predictable latency) and persistent memory region (PMR) support."

**Source:** NVMe Base Specification 1.4, NVM Express Industry Association, 2019; "NVMe and the Move to PCIe-Based Solid State Storage," JEDEC Flash Summit, 2014

#segment:storage #source-tier:S #signal-type:roadmap #date:2019 #importance:high #confidence:high

---

### PCIe Gen 5 — AI Storage Bandwidth

> "PCIe 5.0 (PCI-SIG 2019) doubles the per-lane bandwidth from Gen 4's 2 GB/s to 4 GB/s (unidirectional), and from 16 GT/s to 32 GT/s. A PCIe 5.0 x4 NVMe SSD achieves approximately 14–15 GB/s sequential read bandwidth. Enterprise Gen5 NVMe SSDs (Kioxia CD9P, Micron 6550 ION) are qualifying at hyperscalers for AI training dataset storage, where sequential read throughput drives I/O performance for large dataset loading. PCIe 6.0 (draft 2022) targets 8 GB/s per lane using PAM4 signaling."

**Source:** PCI Express Base Specification 5.0, PCI-SIG, 2019; PCI Express Base Specification 6.0 (draft), PCI-SIG, 2022; Kioxia CD9P Product Brief, 2025

#segment:storage #source-tier:S #signal-type:roadmap #date:2019 #importance:high #confidence:high

---

## 4. Enterprise SSD Architecture for AI Workloads

### NAND Flash Controller and FTL (Flash Translation Layer)

> "Enterprise SSDs use a dedicated controller ASIC (e.g., Marvell Bravura, Samsung in-house, Phison E26) to manage NAND flash behind a logical block address (LBA) abstraction. The Flash Translation Layer (FTL) maps LBAs to physical NAND pages, handles garbage collection (reclaiming erased blocks), and implements wear leveling (distributing P/E cycles across cells). In QLC enterprise SSDs, the FTL implements aggressive SLC caching — incoming writes first land in fast SLC mode (1 bit/cell) before being folded to QLC (4 bits/cell) in the background."

**Source:** "A Survey of Flash-based Solid-State Drives," ACM Computing Surveys, 2018; JEDEC JESD219B (Endurance Workload Definition for Client and Enterprise SSDs), JEDEC, 2023

#segment:storage #source-tier:S #signal-type:roadmap #date:2018 #importance:medium #confidence:high

---

### KV-SSD — Key-Value SSD for Agentic AI Inference

> "A Key-Value SSD (KV-SSD) exposes a key-value interface directly to the host (put/get/delete by key) instead of the traditional block interface. Samsung introduced the KV-SSD concept to address the efficiency loss in database-style access patterns: a traditional block I/O read-modify-write (RMW) for a small key-value update requires reading an entire 4KB page and rewriting it. KV-SSDs process key-value operations in the SSD controller directly, eliminating unnecessary RMW amplification. For agentic AI inference, KV-cache (key-value pairs from transformer attention) can be stored and retrieved directly via KV-SSD API, enabling persistent KV-cache across inference sessions without CPU memory bottlenecks."

**Source:** "KVSSD: Close Integration of LSM-Trees and Flash Translation Layer for Write-Efficient KV Store," IEEE Design, Automation and Test in Europe (DATE), Samsung, 2018; Samsung KV-SSD Technology Whitepaper, Samsung Semiconductor, 2024

#segment:storage #source-tier:A #signal-type:roadmap #date:2018 #importance:high #confidence:high

---

## 5. Error Correction in Enterprise NAND

### LDPC (Low-Density Parity-Check) Codes

> "Enterprise NAND SSDs use LDPC (Low-Density Parity-Check) error-correcting codes to extend QLC and TLC NAND endurance beyond raw cell P/E cycle limits. LDPC decoding uses iterative belief propagation (sum-product algorithm) to correct multi-bit errors in a codeword. LDPC codes can correct up to ~15–20% raw bit error rate (RBER) in soft-decision implementations, enabling QLC NAND with raw RBER of ~10⁻³ to achieve system-level RBER of <10⁻¹⁵ suitable for enterprise storage. LDPC decoding latency: approximately 1–5µs in hardware, which is the dominant contributor to enterprise SSD read latency at low queue depths."

**Source:** "LDPC Codes for Error Correction in Flash Memories," IEEE Signal Processing Magazine, 2014; "Error Correction Technology in Enterprise Flash Storage," Micron Technical Paper, 2018

#segment:storage #source-tier:S #signal-type:roadmap #date:2014 #importance:medium #confidence:high

---

## Open Technical Questions

- [ ] QLC NAND for AI training checkpointing: what is the optimal OP (overprovisioning) ratio for sustained sequential write workloads?
- [ ] Computational Storage Drives (CSD): will in-SSD AI inference (running neural networks inside the SSD controller) become practical for RAG workloads?
- [ ] BiCS 9 (300+ layer) manufacturability: what are the key etch selectivity challenges at >300-layer aspect ratios?
- [ ] NVMe over Fabrics (NVMe-oF) adoption in AI clusters: will disaggregated storage replace local NVMe for training?
