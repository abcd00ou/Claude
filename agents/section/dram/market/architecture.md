# DRAM Architecture — Academic Technical Reference

**Segment:** DRAM / Memory  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-12 (Cycle 5)  
**Sources:** JEDEC standards (JESD79, JESD235), IEEE ISSCC/IEDM papers, SK Hynix and Micron technical briefs

---

## 1. DRAM Cell Fundamentals

### 1T1C Cell — The Foundation of All DRAM

> "The dynamic random-access memory (DRAM) cell consists of one transistor and one capacitor (1T1C). The transistor controls access; the capacitor stores a single bit as charge. Charge leaks over time — cells must be refreshed every 64ms (JEDEC standard) to prevent data loss. This 'dynamic' refresh requirement distinguishes DRAM from static SRAM."

**Source:** "Field-Effect Transistor Memory," US Patent 3,387,286, Robert Dennard / IBM, 1968-06-04; JEDEC JESD79-5B Standard, JEDEC Solid State Technology Association, 2020

#segment:dram #source-tier:S #signal-type:roadmap #date:1968 #importance:medium #confidence:high

---

### Sense Amplifier and Row/Column Architecture

> "DRAM is organized as a 2D array of cells accessed by row (wordline) and column (bitline) addresses. A sense amplifier detects charge on the bitline when a row is activated (RAS — Row Address Strobe), then the column address (CAS — Column Address Strobe) selects the specific bit. CAS Latency (CL) is the primary timing parameter: the number of clock cycles from column address to data availability. DDR5 CL values range from CL36 to CL52 at standard XMP frequencies."

**Source:** JEDEC JESD79-5B (DDR5 Standard), JEDEC, 2020; Micron DDR5 Technical Note TN-48-04, Micron Technology, 2021

#segment:dram #source-tier:S #signal-type:roadmap #date:2020 #importance:medium #confidence:high

---

## 2. HBM (High Bandwidth Memory) Architecture

### Physical Stack Construction

> "HBM stacks DRAM dies vertically using Through-Silicon Vias (TSVs). A TSV is a vertical copper via ~5µm in diameter drilled through a silicon die, enabling electrical connection from the bottom to top of the die. An HBM3 stack consists of: (1) one logic base die (containing PHY, ECC, address decode); (2) up to 12 DRAM core dies above it (HBM3E 12-Hi). Dies are bonded face-to-face or face-to-back using thermocompression bonding (TC-bonding) with copper micro-bumps at 40–55µm pitch."

**Source:** "A 1.2V 8Gb 8-channel 128GB/s High-Bandwidth Memory (HBM) DRAM," IEEE International Solid-State Circuits Conference (ISSCC), SK Hynix and AMD, 2014-02; JEDEC JESD235C (HBM3 Standard), JEDEC, 2022

#segment:dram #source-tier:S #signal-type:roadmap #date:2014 #importance:high #confidence:high

---

### HBM Channel Architecture and Bus Width

> "Each HBM stack exposes 8 independent 128-bit channels (per JEDEC JESD235 HBM/HBM2) or 16 channels of 64-bit (per JESD235C HBM3/HBM3E), yielding a total aggregate bus width of 1024 bits per stack. This extremely wide bus enables high bandwidth at relatively low pin frequencies — e.g., HBM3 operates at 3.2–6.4 Gbps per pin, yielding 819 GB/s – 1.638 TB/s per stack. HBM3E (used in NVIDIA H200 and B200) operates at up to 9.6 Gbps per pin."

**Source:** JEDEC JESD235C Standard — High Bandwidth Memory (HBM) DRAM, JEDEC Solid State Technology Association, 2022; JEDEC JESD235D Standard (HBM3E), JEDEC, 2023

#segment:dram #source-tier:S #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

### HBM Generation Comparison

| Generation | Standard | Pin Rate (Gbps) | Bandwidth/Stack | Capacity/Stack | Stacks in H-series GPU |
|---|---|---|---|---|---|
| HBM (1st) | JESD235 | 1.0 | 128 GB/s | 4 GB (4-Hi) | AMD Fiji (4 stacks) |
| HBM2 | JESD235A | 2.0 | 256 GB/s | 8 GB (4-Hi) | NVIDIA V100 (4 stacks) |
| HBM2E | JESD235B | 3.6 | 461 GB/s | 16 GB (8-Hi) | AMD MI250X (4 stacks) |
| HBM3 | JESD235C | 6.4 | 819 GB/s | 16–24 GB (8-Hi/12-Hi) | NVIDIA H100 (5 stacks, 80GB) |
| HBM3E | JESD235D | 9.6 | 1.15 TB/s | 24–36 GB (12-Hi) | NVIDIA H200 (6 stacks, 141GB); B200 (8 stacks, 192GB) |
| HBM4 | JESD238 | 12.8 (target) | 1.6+ TB/s | 36–48 GB (12–16-Hi) | NVIDIA Vera Rubin R100 (target 288 GB) |

**Source:** JEDEC standards JESD235 through JESD238; NVIDIA H100, H200, B200 product briefs; AMD MI series data sheets

#segment:dram #source-tier:S #signal-type:roadmap #date:2023 #importance:high #confidence:high

---

## 3. HBM Integration with GPU: CoWoS and Memory Controller

### Silicon Interposer (CoWoS-S) as the Integration Platform

> "In CoWoS-S (Chip on Wafer on Substrate — Silicon interposer), the GPU compute die and HBM stacks are mounted side-by-side on a passive silicon interposer fabricated on a 65nm or 28nm node. The interposer provides high-density metal routing (10,000+ wires per mm width) connecting the GPU's HBM PHY to the HBM base die. Interposer trace length: approximately 5–15mm vs 40–80mm for GDDR6 PCB traces on a discrete GPU. The shorter traces reduce signal integrity constraints and power consumption."

**Source:** "TSMC CoWoS Technology Overview," IEEE Symposium on VLSI Technology and Circuits, TSMC, 2022; NVIDIA H100 SXM5 product brief, 2022

#segment:dram #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

### GPU HBM Memory Controller Integration

> "The NVIDIA GH100 GPU die (used in H100) integrates 6 HBM3 memory controllers, each managing one HBM3 stack (5 active stacks used, 1 for redundancy in SXM5 configuration). Each controller implements the full HBM3 PHY, including ClockGen, DFI interface, and ECC engine. The memory bus from the GPU to each HBM stack operates at 128 bytes per clock cycle (1024 bits) with write-leveling and on-die termination (ODT) managed through the HBM base die logic layer."

**Source:** NVIDIA Hopper Architecture Whitepaper — H100 GPU, NVIDIA Corporation, 2022; "Hot Chips 34: NVIDIA Hopper H100 GPU Architecture," IEEE/ACM Hot Chips Symposium, 2022-08

#segment:dram #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

## 4. HBM vs GDDR6X — Technical Comparison

| Parameter | HBM3E (NVIDIA B200) | GDDR6X (NVIDIA RTX 4090) |
|---|---|---|
| Bus width per device | 1024 bits (per stack) | 32 bits (per GDDR chip) |
| Total bus width | 8,192 bits (8 stacks) | 384 bits (12 chips) |
| Pin rate | 9.6 Gbps | 21 Gbps |
| Total bandwidth | **8.0 TB/s** | ~1.0 TB/s |
| Capacity | 192 GB (8×24 GB stacks) | 24 GB (12×2 GB chips) |
| Package integration | On-package (CoWoS interposer) | Discrete soldered packages on PCB |
| Power efficiency | ~2× better than GDDR6X | Baseline |
| Trace length | ~5–15mm (interposer) | ~40–80mm (PCB) |
| Use case | AI training/inference GPU | Gaming GPU, professional visualization |

> "HBM achieves higher bandwidth through extreme bus width rather than extreme pin speed. GDDR6X uses PAM4 (Pulse Amplitude Modulation 4-level) signaling to achieve 21 Gbps at the cost of signal integrity complexity. HBM uses NRZ (non-return-to-zero) signaling at lower speeds but with 64× more pins per stack, yielding far superior bandwidth density per mm² of package area."

**Source:** JEDEC JESD235D (HBM3E); JEDEC JESD250E (GDDR6); NVIDIA RTX 4090 Whitepaper, 2022; NVIDIA B200 Product Brief, 2024; Micron GDDR6X Technology Overview, 2020

#segment:dram #source-tier:S #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

## 5. ECC in HBM

> "HBM3 implements per-channel Single-Error Correction, Double-Error Detection (SECDED) ECC natively within the HBM base die's logic layer. The HBM3 standard (JEDEC JESD235C) specifies that 128-bit data words are protected by 8 check bits (Hamming code), yielding 136-bit codewords per burst. Post-package repair (PPR) allows row-level repair after packaging using spare rows in each DRAM die, reducing yield loss from defective cells."

**Source:** JEDEC JESD235C Standard — High Bandwidth Memory DRAM, Section 4.2 (ECC), JEDEC, 2022

#segment:dram #source-tier:S #signal-type:roadmap #date:2022 #importance:medium #confidence:high

---

## 6. LPDDR5X — Inference Server and Edge AI

> "LPDDR5X (Low Power DDR5) achieves up to 9.6 Gbps per pin in a JEDEC JESD209-5B-compliant implementation. Used in AI inference devices (smartphones, edge AI servers) where power efficiency is paramount over raw bandwidth. A 64-bit LPDDR5X channel delivers ~77 GB/s — approximately 5× less than a single HBM3E stack but at a small fraction of the power."

**Source:** JEDEC JESD209-5B Standard (LPDDR5/LPDDR5X), JEDEC, 2022; Qualcomm Snapdragon 8 Gen 3 Memory Subsystem Brief, 2023

#segment:dram #source-tier:S #signal-type:roadmap #date:2022 #importance:low #confidence:high

---

## Open Technical Questions

- [ ] HBM4 die-to-die bonding: will hybrid bonding (copper-to-copper, sub-10µm pitch) replace TC-bonding micro-bumps?
- [ ] HBM4 logic base die: will it include compute logic (Processing In Memory — PIM) to reduce data movement?
- [ ] CoWoS-L (RDL-based) vs CoWoS-S (silicon interposer) for Vera Rubin: what is the electrical performance tradeoff?
