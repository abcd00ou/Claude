# GPU Architecture — Academic Technical Reference

**Segment:** AI Chip Makers (GPU / xPU)  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-13 (Cycle 6)  
**Sources:** ACM CACM (Williams et al. 2009); ACM ISCA (Jouppi et al. 2017); ACM SC (Narayanan et al. 2021); NVIDIA Hopper Architecture Whitepaper (2022); NeurIPS (Vaswani et al. 2017)

---

## 1. Roofline Model — Compute-Bound vs Memory-Bandwidth-Bound

> "The Roofline model ties together floating-point performance, operational intensity, and memory performance in a 2D graph. The model sets an upper bound on performance of a kernel depending on its operational intensity: a kernel either hits the flat part of the roof (indicating compute-bound performance, limited by peak FLOPS) or the slanted part (indicating memory-bandwidth-bound performance, limited by memory bandwidth). Operational intensity is defined as the ratio of floating-point operations to bytes of DRAM traffic. The Roofline model was demonstrated on four diverse multicore computers using four key floating-point kernels, providing actionable insight on how to improve both software and hardware."

**Source:** Williams, S., Waterman, A., and Patterson, D., "Roofline: An Insightful Visual Performance Model for Multicore Architectures," Communications of the ACM (CACM), Vol. 52, No. 4, pp. 65–76, April 2009. DOI: 10.1145/1498765.1498785

#segment:chip_maker #source-tier:S #signal-type:roadmap #date:2009 #importance:high #confidence:high

---

## 2. Tensor Processing Unit (TPU) — In-Datacenter Performance Analysis

> "The TPU is a custom ASIC deployed in datacenters since 2015 that accelerates the inference phase of neural networks. The heart of the TPU is a 65,536 8-bit MAC matrix multiply unit that offers a peak throughput of 92 TeraOps/second (TOPS) and a large (28 MiB) software-managed on-chip memory. Despite having low utilization for some applications, the TPU is on average about 15× to 30× faster than its contemporary GPU or CPU, with TOPS/Watt about 30× to 80× higher. The TPU's relatively modest memory bandwidth of 30 GB/s is sufficient because the 28 MiB on-chip SRAM acts as a large software-managed scratchpad, eliminating external memory accesses for weights during inference."

**Source:** Jouppi, N.P., Young, C., Patil, N., Patterson, D., et al. (Google), "In-Datacenter Performance Analysis of a Tensor Processing Unit," Proceedings of the 44th Annual International Symposium on Computer Architecture (ISCA '17), Toronto, ON, June 2017. DOI: 10.1145/3079856.3080246. arXiv: 1704.04760

#segment:chip_maker #source-tier:S #signal-type:roadmap #date:2017 #importance:high #confidence:high

---

## 3. 3D Parallelism — Scaling Transformer Training to Thousands of GPUs

> "We present a PTD-P approach combining pipeline, tensor, and data parallelism to train models with trillions of parameters. Using 3072 A100 GPUs with 3D parallelism (tensor parallelism degree 8, pipeline parallelism degree 8, data parallelism degree 48), we achieve 502 petaFLOP/s throughput on a model with 1 trillion parameters — corresponding to 52% of the theoretical peak. Tensor parallelism partitions individual matrix operations across GPUs; pipeline parallelism partitions model layers into stages; data parallelism replicates stages across worker groups. The paper demonstrates that naive pipeline parallelism incurs a 'bubble' fraction of idle time equal to (p−1)/m where p is pipeline stages and m is micro-batches."

**Source:** Narayanan, D., Shoeybi, M., Casper, J., LeGresley, P., Patwary, M., Korthikanti, V., Vainbrand, D., Kashinkunti, P., Bernauer, J., Catanzaro, B., Phanishayee, A., and Zaharia, M. (NVIDIA/Stanford/Microsoft), "Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM," Proceedings of SC '21: International Conference for High Performance Computing, Networking, Storage and Analysis, 2021. DOI: 10.1145/3458817.3476209. arXiv: 2104.04473

#segment:chip_maker #source-tier:S #signal-type:roadmap #date:2021 #importance:high #confidence:high

---

## 4. Transformer Architecture — The Computation That Defines GPU Workloads

> "We propose the Transformer, a model architecture eschewing recurrence and instead relying entirely on an attention mechanism to draw global dependencies between input and output. The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs. The dominant sequence transduction models are based on complex recurrent or convolutional neural networks; we show that the Transformer can be trained significantly faster than architectures based on recurrent or convolutional layers." The paper has been cited more than 173,000 times, making it among the top ten most-cited papers of the 21st century.

**Source:** Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, Ł., and Polosukhin, I. (Google Brain), "Attention Is All You Need," Advances in Neural Information Processing Systems (NeurIPS), Vol. 30, 2017. arXiv: 1706.03762. Proceedings: papers.neurips.cc/paper/7181

#segment:chip_maker #source-tier:S #signal-type:roadmap #date:2017 #importance:high #confidence:high

---

## 5. NVIDIA Hopper Architecture — H100 GPU Specifications

> "The NVIDIA H100 Tensor Core GPU is built on the Hopper GPU architecture. The H100 SXM5 features 80 billion transistors on a 4nm process (TSMC N4). Key components per Streaming Multiprocessor (SM): 128 FP32 CUDA cores, 4th-generation Tensor Cores supporting FP8/FP16/BF16/TF32/FP32, 256KB L1 data cache/shared memory. Total: 132 SMs, 50MB L2 cache, 5 HBM3 stacks (80GB) via a 5120-bit memory interface delivering 3.35 TB/s. The Transformer Engine dynamically casts weights to FP8 and computes in FP8 with accumulation in higher precision, enabling 3,958 TFLOPS peak sparse FP16."

**Source:** NVIDIA Corporation, "NVIDIA H100 Tensor Core GPU Architecture," NVIDIA Whitepaper WP-10184-001, v1.0, March 2022. Available: resources.nvidia.com/en-us-tensor-core/gtc22-whitepaper-hopper

#segment:chip_maker #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

## 6. Megatron-LM Tensor Parallelism — Intra-Layer Model Parallelism

> "We present an efficient, intra-layer model parallel approach that enables training transformer models with billions of parameters. We demonstrate this approach by training an 8.3 billion parameter transformer language model using 512 GPUs, achieving 76% scaling efficiency when compared to a single GPU baseline. We show that a carefully designed model parallel approach can reduce the need for both data and pipeline parallelism; tensor parallelism places the attention heads and feed-forward layers directly across multiple GPUs within a single transformer layer using two all-reduce operations per transformer block."

**Source:** Shoeybi, M., Patwary, M., Puri, R., LeGresley, P., Casper, J., and Catanzaro, B. (NVIDIA), "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism," arXiv preprint arXiv:1909.08053, September 2019. Available: arxiv.org/abs/1909.08053

#segment:chip_maker #source-tier:A #signal-type:roadmap #date:2019 #importance:high #confidence:high

---

## Open Technical Questions

- [ ] Roofline for sparse Transformer attention (FlashAttention-3): what is the measured operational intensity on H100 vs theoretical HBM roof?
- [ ] NVLink-C2C (GB200): what is the measured latency and bandwidth for CPU-GPU communication vs PCIe Gen5?
- [ ] FP4 Tensor Core accuracy (Blackwell B200): what is the empirically measured training accuracy gap vs FP8 for LLM pre-training?
- [ ] GPU pipeline parallelism bubble ratio at scale: for Llama-3 class models on 1024 GPUs, what is the measured bubble fraction?
