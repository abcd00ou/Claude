# GPU Architecture — Academic Technical Reference

**Segment:** AI Chip Makers (GPU / xPU)  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-12 (Cycle 5)  
**Sources:** NVIDIA architecture whitepapers (Ampere, Hopper, Blackwell); AMD CDNA whitepapers; IEEE ISSCC/Hot Chips papers; CUDA programming guide

---

## 1. GPU Streaming Multiprocessor (SM) — Core Compute Unit

### SM Architecture (NVIDIA Hopper / H100)

> "The NVIDIA H100 GH100 GPU contains 144 Streaming Multiprocessors (SMs). Each SM includes: (1) 128 CUDA cores (FP32); (2) 4 Tensor Core units (4th generation); (3) 256 KB shared memory (SRAM); (4) a warp scheduler managing 64-thread warps; (5) an L1 data cache. The SM executes Single Instruction Multiple Thread (SIMT) parallelism — all 128 CUDA cores in an SM execute the same instruction on different data simultaneously, similar to SIMD but with per-thread divergence handling."

**Source:** NVIDIA Hopper Architecture Whitepaper, NVIDIA Corporation, 2022; "NVIDIA H100 Tensor Core GPU Architecture," NVIDIA, 2022-03; IEEE Hot Chips 34: NVIDIA Hopper, 2022-08

#segment:chip_maker #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

### Tensor Core — Matrix Multiplication Accelerator

> "Tensor Cores perform mixed-precision matrix multiply-accumulate (MMA) operations in a single clock cycle. A 4th-generation Tensor Core (H100) operates on 8×8×4 matrix tiles for FP32 or 16×8×16 tiles for FP16/BF16, executing 256 FP16 multiply-add operations per clock per Tensor Core. Each H100 SM contains 4 Tensor Cores, and with 144 SMs, the H100 delivers approximately 3,958 TFLOPS peak sparse FP16 performance. Transformer Engine (NVIDIA H100 feature) dynamically selects FP8 or BF16 precision per layer during training, enabling further performance improvement."

**Source:** NVIDIA Hopper Architecture Whitepaper, 2022; CUDA C++ Programming Guide, NVIDIA, 2023; "Dissecting the NVIDIA Volta GPU Architecture via Microbenchmarking," IEEE IPDPS, 2018

#segment:chip_maker #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

## 2. GPU Memory Hierarchy

### L1/L2 Cache and Shared Memory

> "The NVIDIA H100 GPU memory hierarchy consists of: (1) per-SM L1 cache / shared memory: 256 KB configurable (up to 228 KB shared, 128 KB L1); (2) L2 cache: 50 MB total on GH100, shared across all SMs; (3) HBM3 DRAM: 80 GB, accessed via the memory interconnect at 3.35 TB/s. The L2 cache acts as a bandwidth multiplier — repeated data access hits L2 instead of HBM3, reducing effective bandwidth pressure. AI inference benefits strongly from large L2 caches when KV-cache or weight matrices fit within the 50 MB L2."

**Source:** NVIDIA H100 SXM5 Product Datasheet, 2022; NVIDIA Hopper Architecture Whitepaper, 2022

#segment:chip_maker #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

### HBM-to-GPU Memory Interface

> "The H100 SXM5 connects to 5 HBM3 stacks (80 GB total) via a 5120-bit memory bus routed through the CoWoS silicon interposer. The GPU die includes 5 independent HBM memory controllers, each managing one 1024-bit HBM3 stack channel group. Memory access latency from SM to HBM3: approximately 200–300 clock cycles (100–150 ns at 1.7 GHz boost clock). L2 cache latency: ~30 cycles. L1/shared memory: ~20 cycles. The HBM memory controller implements: address hashing across stacks for load balancing, DRAM refresh scheduling, and ECC correction reporting."

**Source:** NVIDIA H100 Datasheet, 2022; "Memory Hierarchy in NVIDIA Ampere GPU Architecture," NVIDIA Technical Blog, 2020

#segment:chip_maker #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

## 3. NVLink — High-Speed GPU-to-GPU Interconnect

### NVLink Architecture

> "NVLink is NVIDIA's proprietary high-speed interconnect for GPU-to-GPU and GPU-to-CPU data transfer. NVLink 4.0 (H100) operates at 900 GB/s total bidirectional bandwidth per GPU (18 links × 50 GB/s each). NVLink uses point-to-point SerDes lanes with 8b/10b or 128b/132b encoding. Within an NVL72 rack (Blackwell GB200), NVLink 5 connects 72 GPUs in a fully non-blocking fat-tree topology via the NVLink Switch (NVSwitch), enabling each GPU to communicate with any other at full 900+ GB/s bandwidth without using InfiniBand."

**Source:** NVIDIA H100 NVLink Technical Overview, NVIDIA, 2022; NVIDIA Blackwell Architecture Whitepaper, 2024; IEEE Hot Chips 36: NVIDIA Blackwell, 2024

#segment:chip_maker #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

### NVSwitch — All-to-All GPU Fabric

> "The NVSwitch is a dedicated interconnect switch ASIC enabling all-to-all GPU-to-GPU communication within a server or rack. NVSwitch 3.0 (H100 DGX): each switch connects 8 GPUs at 900 GB/s total per GPU; 4 NVSwitches provide non-blocking all-to-all fabric for an 8-GPU DGX H100. NVSwitch 4.0 (GB200 NVL72): scales to 72 GPUs per rack with full non-blocking connectivity. This eliminates the need for InfiniBand for intra-rack all-reduce operations in transformer training, which dominate collective communication time."

**Source:** NVIDIA DGX H100 Architecture Guide, 2022; NVIDIA Blackwell GB200 NVL72 Technical Overview, 2024

#segment:chip_maker #source-tier:A #signal-type:roadmap #date:2024 #importance:high #confidence:high

---

## 4. GPU vs GDDR6X vs HBM — Workload Fit

> "AI training is dominated by large matrix multiplications (GEMM) and attention operations. The H100 (HBM3) achieves ~3.35 TB/s memory bandwidth and 3,958 TFLOPS sparse FP16 — an arithmetic intensity of 1,180 FLOPs per byte. Most transformer layer GEMM operations achieve 300–800 FLOPs/byte, making them memory-bandwidth-bound on GPUs without HBM. GDDR6X GPUs (RTX 4090, ~1.0 TB/s, ~82 TFLOPS FP16) achieve approximately the same arithmetic intensity but deliver far less total bandwidth and throughput for large-batch AI inference. This is why GDDR6X GPUs are used for gaming and consumer AI inference (small batch, low latency) while HBM GPUs dominate data center AI training."

**Source:** NVIDIA H100 vs RTX 4090 specifications, 2022; "Roofline: An Insightful Visual Performance Model for Floating-Point Programs and Multicore Architectures," ACM Communications, Williams et al., 2009; NVIDIA Transformer Engine documentation, 2022

#segment:chip_maker #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

## 5. AMD CDNA Architecture (Instinct Series)

> "AMD's Compute DNA (CDNA) architecture (MI200, MI300 series) separates compute GPU design from gaming GPU (RDNA). The AMD MI300X uses a multi-chiplet design: 3 Compute Dies (CDNA 3, 5nm TSMC) + 4 Active Bridge Dies (6nm) assembled on a single HBM3 interposer package. MI300X integrates 192 GB HBM3 across 8 stacks (5.3 TB/s bandwidth), the highest HBM capacity of any single GPU package as of 2023. CDNA 3 introduces unified CPU+GPU memory architecture (MI300A variant) with CPU and GPU dies sharing the HBM3 pool."

**Source:** AMD CDNA 3 Architecture Whitepaper, AMD, 2023; "AMD Instinct MI300X Accelerator," IEEE Hot Chips 35, 2023; AMD Radeon Instinct MI300X Product Brief, 2023

#segment:chip_maker #source-tier:A #signal-type:roadmap #date:2023 #importance:high #confidence:high

---

## 6. NVIDIA Blackwell Architecture

> "The NVIDIA Blackwell GPU (B100/B200, GH200/GB200) introduces several architectural advances over Hopper: (1) 2-die design (2 GPC dies connected via 10 TB/s NVLink-C2C); (2) 5th-generation Tensor Cores supporting FP4/FP6 precision in addition to FP8/BF16/FP32; (3) 2nd-generation Transformer Engine with dynamic FP8 casting per attention head; (4) 192 GB HBM3E (8 stacks) at 8.0 TB/s; (5) RAS Engine for reliability, availability, and serviceability in data center deployments. GB200 pairs one Grace CPU (72-core Arm Neoverse V2) with two B200 GPUs via NVLink-C2C at 900 GB/s."

**Source:** NVIDIA Blackwell Architecture Technical Overview, NVIDIA, 2024; IEEE Hot Chips 36: NVIDIA Blackwell GB200, 2024-08

#segment:chip_maker #source-tier:A #signal-type:roadmap #date:2024 #importance:high #confidence:high

---

## Open Technical Questions

- [ ] Vera Rubin R100: how does the dual-die 3nm design partition compute vs memory logic between the two dies?
- [ ] NVLink Fusion (Trainium4 support): what is the electrical specification of NVLink-compatible interfaces for third-party ASICs?
- [ ] NVIDIA Tensor Core FP4: what is the actual training accuracy impact of 4-bit weights vs FP8?
- [ ] AMD MI400 (HBM4): will CDNA 4 integrate compute and HBM base die (monolithic) or remain chiplet-based?
