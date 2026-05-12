# Custom ASIC Architecture — Academic Technical Reference

**Segment:** Custom AI Accelerator (ASIC / xPU)  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-12 (Cycle 5)  
**Sources:** Google TPU papers (ISCA, CACM); IEEE Hot Chips; AWS Annapurna documentation; academic papers on systolic array and dataflow architectures

---

## 1. Systolic Array Architecture — The Foundation of TPU

### Systolic Array Concept

> "A systolic array is a homogeneous network of tightly coupled data processing units (DPUs) that rhythmically compute and pass data through the array. Introduced by H.T. Kung and Charles Leiserson (1978), systolic arrays perform matrix multiplication by flowing input matrices from two directions: activations enter from the left, weights are pre-loaded into the array cells, and partial sum outputs flow downward. Each cell performs a single multiply-accumulate (MAC) operation per clock cycle. A systolic array avoids the global memory bandwidth bottleneck of von Neumann architectures: data reuse is achieved by passing values between adjacent cells rather than fetching from DRAM."

**Source:** "Systolic Arrays (for VLSI)," H.T. Kung and C.E. Leiserson, Sparse Matrix Proceedings, 1978; "In-Datacenter Performance Analysis of a Tensor Processing Unit," Google / ACM ISCA, Jouppi et al., 2017

#segment:asic #source-tier:S #signal-type:roadmap #date:1978 #importance:high #confidence:high

---

### Google TPU Matrix Multiply Unit (MXU)

> "The Google TPUv1 Matrix Multiply Unit (MXU) is a 256×256 systolic array of 8-bit integer multiply-accumulate units, performing 65,536 multiply-accumulate operations per clock cycle at 700 MHz, yielding 92 TOPS (tera-operations per second). The MXU operates in 'weight stationary' mode: the weight matrix for a neural network layer is pre-loaded into the 28 MiB on-chip weight FIFO and held stationary while activations stream through left to right. The systolic array avoids reading weights from DRAM during computation — the key DRAM bandwidth saving vs GPU which re-fetches weights from HBM every forward pass."

**Source:** "In-Datacenter Performance Analysis of a Tensor Processing Unit," Jouppi et al., ACM ISCA, 2017; "A Domain-Specific Supercomputer for Training Deep Neural Networks," Jouppi et al., CACM, 2020

#segment:asic #source-tier:S #signal-type:roadmap #date:2017 #importance:high #confidence:high

---

### Dataflow Architecture Variants

> "Three principal dataflow strategies exist for neural network accelerators, each differing in what data is kept stationary in the register file: (1) Weight Stationary (WS): weights held in register file; activations and partial sums move — used in Google TPU MXU; (2) Output Stationary (OS): partial sums accumulated locally; weights and activations move — minimizes partial sum memory accesses; (3) No Local Reuse (NLR): no data held stationary; optimizes for total data movement across the chip. For transformer inference, output stationary achieves higher efficiency because attention partial sums are large relative to weight matrices in multi-head attention."

**Source:** "Eyeriss: An Energy-Efficient Reconfigurable Accelerator for Deep Convolutional Neural Networks," Chen et al., IEEE ISSCC, 2016; "Eyeriss v2: A Flexible and High-Performance Accelerator for Emerging Deep Neural Networks," Chen et al., IEEE JETCAS, 2019

#segment:asic #source-tier:S #signal-type:roadmap #date:2016 #importance:high #confidence:high

---

## 2. ASIC vs GPU — Architectural Tradeoffs

### Fixed-Function vs Programmable Architecture

> "A custom ASIC (Application-Specific Integrated Circuit) implements a fixed set of compute operations in silicon, achieving maximum area and energy efficiency for the target workload. A GPU implements programmable CUDA cores with a general-purpose ISA. Tradeoff: (1) Performance per watt: AI ASIC achieves 3–10× better performance per watt vs GPU for a fixed workload (e.g., BF16 matrix multiplication) by eliminating programmable control overhead; (2) Flexibility: GPU can run any CUDA kernel; ASIC cannot run arbitrary code; (3) Development time: GPU uses existing CUDA toolchain; new ASIC requires 18–24 months from tapeout to volume production. ASICs are cost-effective only at sufficiently high deployment volume to amortize $100–500M NRE (non-recurring engineering) costs."

**Source:** "Custom Silicon for AI Accelerators," Gwennap, Microprocessor Report, 2021; "Evaluating Deep Learning Inference at the Edge," IEEE Micro, 2020; Google TPU vs NVIDIA GPU benchmark, MLPerf Training v3.0, 2023

#segment:asic #source-tier:A #signal-type:roadmap #date:2021 #importance:high #confidence:high

---

### Memory Hierarchy Design for Inference vs Training

> "AI accelerator memory hierarchy differs fundamentally between inference and training workloads: (1) Inference: weight matrices are fixed; on-chip SRAM for KV-cache and activations; bandwidth demand scales with batch size × sequence length; prefill phase is compute-bound, decode phase is memory-bandwidth-bound; (2) Training: weights change every step; requires gradient accumulation buffers; optimizer state (Adam: 3× weight size for momentum/variance/weights) demands far more HBM capacity. Google Ironwood (inference TPU) uses 192 GB HBM3E with 7.37 TB/s bandwidth — emphasizing bandwidth for token decode. NVIDIA H100 (training) uses 80 GB HBM3 at 3.35 TB/s — emphasizing compute TFLOPS over bandwidth."

**Source:** "Efficiently Scaling Transformer Inference," Pope et al., Google, MLSys 2023; "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness," Dao et al., NeurIPS 2022

#segment:asic #source-tier:S #signal-type:roadmap #date:2023 #importance:high #confidence:high

---

## 3. Chiplet-Based ASIC Design

### Chiplet Integration — Die-Level Modularity

> "Chiplet design disaggregates a monolithic SoC into multiple smaller dies (chiplets) connected by a high-speed die-to-die interconnect. Chiplet advantages over monolithic: (1) Yield improvement — a 400mm² monolithic die at 95% defect-free site probability yields ~14%; a 100mm² chiplet at the same defect density yields ~67%; (2) Technology mixing — compute chiplet on 3nm; I/O chiplet on 12nm; analog on 28nm; memory (HBM) as separate stack; (3) IP reuse — same chiplet across product SKUs with different configurations. AMD MI300X uses this approach: 3 CDNA3 compute dies (5nm) + 4 Active Bridge Dies (6nm) + 8 HBM3 stacks on one package."

**Source:** "Die-to-Die Interconnects: Enabling Multi-Chiplet Architectures," IEEE Micro, 2021; "OCP Chiplet Design Principles," Open Compute Project, 2022; AMD CDNA3 Architecture Whitepaper, AMD, 2023

#segment:asic #source-tier:S #signal-type:roadmap #date:2021 #importance:high #confidence:high

---

### UCIe (Universal Chiplet Interconnect Express)

> "UCIe (Universal Chiplet Interconnect Express) is an open chiplet interconnect standard ratified in 2022, providing die-to-die interconnect at physical layer: (1) Standard package: 2 mm/s bump pitch, 16 GB/s per mm per direction; (2) Advanced package: 25µm bump pitch (compatible with hybrid bonding), 32+ GB/s per mm per direction; (3) Protocol layer: supports CXL and PCIe over the UCIe physical layer. UCIe enables cross-vendor chiplet assembly — an Intel CPU chiplet could use a TSMC-fabricated accelerator chiplet in the same package via UCIe interconnect. Amazon Trainium4 (announced 2025) is reported to use a chiplet design with NVLink Fusion for third-party GPU-compatible interconnect."

**Source:** "UCIe 1.0 Specification," UCIe Consortium, 2022; "Universal Chiplet Interconnect Express (UCIe): Enabling Multi-Chip AI Accelerators," IEEE Hot Chips 34, 2022

#segment:asic #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

## 4. Transformer Accelerator Architecture

### Attention Mechanism Hardware Requirements

> "The transformer attention operation requires: (1) QKV projection: three GEMM operations (query, key, value); (2) Attention score: Q×Kᵀ GEMM — scales as O(N²) in sequence length N; (3) Softmax: element-wise reduction across sequence dimension; (4) Value aggregation: attention_weights × V GEMM. For long sequences (N=100K tokens), the O(N²) attention score GEMM dominates compute: a 100K-token context at 4K attention heads requires 4×10¹⁰ FLOPs per attention layer. FlashAttention (Dao et al., 2022) restructures the attention computation to reduce HBM reads from O(N²) to O(N) by tiling Q/K/V in on-chip SRAM, critical for fitting long contexts in AI ASIC memory hierarchies."

**Source:** "Attention Is All You Need," Vaswani et al., NeurIPS 2017; "FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning," Dao, ICLR 2024; "Efficiently Scaling Transformer Inference," Pope et al., MLSys 2023

#segment:asic #source-tier:S #signal-type:roadmap #date:2017 #importance:high #confidence:high

---

### Sparsity and Quantization in Custom ASICs

> "Structured sparsity (50% zero weights in a 2:4 pattern — every 2 of 4 consecutive weights are zero) can be exploited in hardware via sparse tensor cores (NVIDIA) or equivalent ASIC units. In a 2:4 sparse pattern, the ASIC stores only 50% of weights and performs 50% fewer MACs, achieving ~2× effective TFLOPS. Quantization reduces precision: INT8 (8-bit integer) achieves 2× throughput vs FP16 on the same MAC array; INT4 achieves 4×. Google TPU v4 uses bfloat16 (BF16) for training and INT8 for inference. Amazon Trainium uses StochasticRoundingFP8 (custom 8-bit format) to maintain training accuracy while doubling throughput vs BF16."

**Source:** "NVIDIA Sparse Tensor Core Technology," IEEE Hot Chips 33, 2021; "BF16 Numeric Properties for Neural Network Training," Google Brain, 2019; Amazon Trainium Technical Reference, AWS, 2023

#segment:asic #source-tier:A #signal-type:roadmap #date:2021 #importance:high #confidence:high

---

## 5. ASIC Interconnect: Intra-Chip and Inter-Chip

### On-Chip Network-on-Chip (NoC)

> "Large AI ASICs use a Network-on-Chip (NoC) to route data between the array of compute tiles, SRAM banks, and HBM controllers. A 2D mesh NoC connects each tile to its 4 neighbors; a 2D torus adds wrap-around connections to reduce diameter. For a 1024-tile ASIC, a 32×32 mesh has diameter 62 hops (32+32-2); a 2D torus has diameter 32 hops. Google TPUv4 uses a 3D torus inter-chip network (within a TPU pod) for collective communication — 6 ICI (Inter-Chip Interconnect) links per chip at 1.2 TB/s total, avoiding the need for InfiniBand or Ethernet for all-reduce in a 4,096-chip pod."

**Source:** "TPU v4: An Optionally Tiled Systems-on-Chip for Training Neural Networks at PaetaScale," Jouppi et al., Google, ISCA 2023; "A Survey of Network-on-Chip Architectures," ACM Computing Surveys, 2018

#segment:asic #source-tier:S #signal-type:roadmap #date:2023 #importance:high #confidence:high

---

## Open Technical Questions

- [ ] Google Ironwood ICI (Inter-Chip Interconnect): bandwidth per chip and topology vs TPUv4 3D torus?
- [ ] Amazon Trainium4 chiplet design: die count, die area, and UCIe vs NVLink-Fusion interconnect bandwidth?
- [ ] ASIC systolic array vs GPU tensor core for sparse attention (FlashAttention-3): which achieves better FLOP/W?
- [ ] Meta MTIA Gen 2: published architecture details (systolic array vs vector processor)?
