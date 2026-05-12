# Custom ASIC Architecture — Academic Technical Reference

**Segment:** Custom AI Accelerator (ASIC / xPU)  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-13 (Cycle 6)  
**Sources:** SIAM (Kung & Leiserson 1978); ACM ISCA (Jouppi et al. 2017); IEEE ISSCC (Chen et al. 2016); NeurIPS (Vaswani et al. 2017; Dao et al. 2022)

---

## 1. Systolic Arrays — The Foundational Architecture of AI ASICs

> "A systolic array is a homogeneous network of tightly coupled Data Processing Units (DPUs) which rhythmically compute and pass data through the system. In a systolic system, each DPU receives data from its neighbors, processes it, and passes results onward — like a heartbeat (systole) passing data through the array. For matrix multiplication C = A × B: activations stream in from the left, weights are pre-loaded into the array, and partial sum outputs flow downward. A k×k systolic array performs k² multiply-accumulate operations per clock cycle. The key advantage over von Neumann architectures: data reuse through neighbor-to-neighbor passing eliminates the global memory bandwidth bottleneck, since each weight is loaded once and reused for all activations passing through its cell."

**Source:** Kung, H.T. and Leiserson, C.E., "Systolic Arrays (for VLSI)," in I. S. Duff and G. W. Stewart, eds., Sparse Matrix Proceedings 1978, Society for Industrial and Applied Mathematics (SIAM), Philadelphia, PA, 1979, pp. 256–282. CMU-CS-79-103 Technical Report. Available: eecs.harvard.edu/htk/static/files/1978-cmu-cs-report-kung-leiserson.pdf

#segment:asic #source-tier:S #signal-type:roadmap #date:1978 #importance:high #confidence:high

---

## 2. TPU Matrix Multiply Unit — Weight-Stationary Systolic Implementation

> "The heart of the TPU is a 65,536 8-bit MAC matrix multiply unit that offers a peak throughput of 92 TeraOps/second (TOPS). The matrix multiply unit is a 256×256 systolic array of 8-bit multipliers operating at 700 MHz, performing 65,536 multiply-accumulate operations per clock cycle. The unit operates weight-stationary: the 28 MiB software-managed on-chip weight memory (SRAM) holds the weight matrix for one neural network layer, and activation data streams through the array. This eliminates the repeated DRAM bandwidth cost of fetching the weight matrix — the dominant bottleneck in GPU inference. The TPU is on average 15× to 30× faster than contemporary GPU or CPU, with TOPS/Watt 30× to 80× higher, driven primarily by the weight-stationary dataflow's memory bandwidth efficiency."

**Source:** Jouppi, N.P., Young, C., Patil, N., Patterson, D., et al. (Google), "In-Datacenter Performance Analysis of a Tensor Processing Unit," Proceedings of the 44th Annual International Symposium on Computer Architecture (ISCA '17), Toronto, ON, June 2017. DOI: 10.1145/3079856.3080246. arXiv: 1704.04760

#segment:asic #source-tier:S #signal-type:roadmap #date:2017 #importance:high #confidence:high

---

## 3. Eyeriss — Row-Stationary Dataflow for CNN Acceleration

> "Eyeriss is an energy-efficient reconfigurable accelerator for deep convolutional neural networks that uses a novel Row Stationary (RS) dataflow to minimize data movement energy at all levels of the memory hierarchy (DRAM, global buffer, inter-PE communication, register file). In the RS dataflow, a 1D convolution row is mapped to a single Processing Element (PE) which accumulates partial sums locally — reducing data movement vs. output-stationary and weight-stationary approaches by 1.4× to 2.5× in energy. The Eyeriss chip (65nm CMOS) contains 168 PEs in a 12×14 array and processes AlexNet at 35 frames per second at 278 mW, achieving 0.5 frames-per-second-per-mW energy efficiency."

**Source:** Chen, Y.-H., Krishna, T., Emer, J.S., and Sze, V. (MIT), "14.5 Eyeriss: An Energy-Efficient Reconfigurable Accelerator for Deep Convolutional Neural Networks," 2016 IEEE International Solid-State Circuits Conference (ISSCC), San Francisco, CA, January–February 2016, pp. 262–264. DOI: 10.1109/ISSCC.2016.7418007

#segment:asic #source-tier:S #signal-type:roadmap #date:2016 #importance:high #confidence:high

---

## 4. Attention Mechanism — The Core Computation of Modern AI ASICs

> "We propose a model architecture eschewing recurrence and instead relying entirely on attention mechanisms. The attention function maps a query Q and a set of key-value pairs (K, V) to an output: Attention(Q,K,V) = softmax(QK^T/√d_k)V. Multi-Head Attention allows the model to jointly attend to information from different representation subspaces: MultiHead(Q,K,V) = Concat(head₁,...,headₙ)W^O where each head_i = Attention(QW_i^Q, KW_i^K, VW_i^V). The QK^T matrix multiplication scales as O(N²) in sequence length N, making long-context inference the dominant compute bottleneck at N=32K+ tokens. This O(N²) scaling directly drove the development of FlashAttention and the memory hierarchy requirements of all modern AI ASICs."

**Source:** Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, Ł., and Polosukhin, I. (Google Brain/Research), "Attention Is All You Need," Advances in Neural Information Processing Systems (NeurIPS 2017), Vol. 30, 2017. arXiv: 1706.03762

#segment:asic #source-tier:S #signal-type:roadmap #date:2017 #importance:high #confidence:high

---

## 5. FlashAttention — IO-Aware Attention for Memory-Bounded Acceleration

> "We propose FlashAttention, an IO-aware exact attention algorithm that uses tiling to reduce the number of memory reads/writes between GPU high bandwidth memory (HBM) and GPU on-chip SRAM. Standard attention materializes the N×N attention matrix to HBM, requiring O(N²) reads and writes. FlashAttention avoids materializing the attention matrix by computing attention in tiles that fit in SRAM, requiring only O(N) HBM reads/writes. FlashAttention is 2× to 4× faster than standard attention in PyTorch and runs up to 7.6× faster on GPT-2 (seq. len. 1K) compared to the PyTorch baseline, with memory usage scaling linearly (O(N)) rather than quadratically (O(N²)) in sequence length."

**Source:** Dao, T., Fu, D.Y., Ermon, S., Rudra, A., and Ré, C. (Stanford), "FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness," Advances in Neural Information Processing Systems (NeurIPS 2022), Vol. 35, 2022. arXiv: 2205.14135. ACM DL: dl.acm.org/doi/10.5555/3600270.3601459

#segment:asic #source-tier:S #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

## 6. ASIC vs GPU — Architectural Efficiency Tradeoff

> "The TPU analysis quantifies the ASIC vs GPU tradeoff: the TPU's 92 TOPS with 40W TDP (TPU v1) achieves 2.3 TOPS/W, versus the K80 GPU at 2.8 TFLOPS with 150W = 0.019 TFLOPS/W for FP32. The 30–80× TOPS/Watt advantage of the TPU over contemporary GPU derives from three architectural choices: (1) 8-bit integer vs. 32-bit floating point computation; (2) weight-stationary SRAM-based execution eliminating DRAM bandwidth cost for weights; (3) no programmable general-purpose pipeline overhead. The tradeoff is that the TPU cannot run arbitrary CUDA kernels and requires mapping neural network layers explicitly to the systolic array."

**Source:** Jouppi, N.P., et al. (Google), "In-Datacenter Performance Analysis of a Tensor Processing Unit," ISCA 2017. DOI: 10.1145/3079856.3080246; Williams, S., Waterman, A., and Patterson, D., "Roofline," CACM 2009. DOI: 10.1145/1498765.1498785

#segment:asic #source-tier:S #signal-type:roadmap #date:2017 #importance:high #confidence:high

---

## Open Technical Questions

- [ ] Google Ironwood ICI bandwidth and topology: how does the inter-chip interconnect bandwidth per chip compare to TPUv4's 4.8 Tb/s total ICI?
- [ ] FlashAttention-3 (H100 optimized): what is the measured FLOP/s utilization vs H100 theoretical peak for long-context (128K token) inference?
- [ ] Amazon Trainium4 chiplet integration: does NVLink Fusion interconnect achieve lower all-reduce latency than Trainium2's NeuronLink for MoE models?
- [ ] Meta MTIA Gen 2: has any published paper described its dataflow architecture (systolic vs. vector processor) and TOPS/W measurement?
