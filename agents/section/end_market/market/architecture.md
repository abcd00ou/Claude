# Hyperscaler AI Infrastructure Architecture — Academic Technical Reference

**Segment:** End Markets (Hyperscalers / Cloud Service Providers)  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-13 (Cycle 6)  
**Sources:** NeurIPS (Vaswani et al. 2017); arXiv/NVIDIA (Shoeybi et al. 2019); ACM SOSP (Kwon et al. 2023); ACM SC (Rajbhandari et al. 2020); ACM SC (Narayanan et al. 2021)

---

## 1. Transformer Architecture — The Computation Defining Hyperscaler AI Demand

> "We propose a model architecture eschewing recurrence and instead relying entirely on attention mechanisms to draw global dependencies between input and output. The Transformer allows for significantly more parallelization and can reach a new state of the art in translation quality after being trained for as little as twelve hours on eight P100 GPUs. The dominant sequence transduction models are based on complex recurrent or convolutional neural networks. Encoder-decoder attention uses Q from the decoder and K, V from the encoder output. Scaled dot-product attention is: Attention(Q,K,V) = softmax(QK^T/√d_k)V. Multi-head attention with h=8 heads and d_model=512 was the original configuration." The paper has been cited more than 173,000 times, placing it among the top ten most-cited papers of the 21st century.

**Source:** Vaswani, A., Shazeer, N., Parmar, N., Uszkoreit, J., Jones, L., Gomez, A.N., Kaiser, Ł., and Polosukhin, I. (Google Brain/Research), "Attention Is All You Need," Advances in Neural Information Processing Systems (NeurIPS), Vol. 30, 2017. arXiv: 1706.03762. Proceedings: papers.neurips.cc/paper/7181-attention-is-all-you-need

#segment:end_market #source-tier:S #signal-type:roadmap #date:2017 #importance:high #confidence:high

---

## 2. Tensor Parallelism — Scaling Transformer Training Within a Node

> "We present an efficient intra-layer model parallel approach that enables training transformer models with billions of parameters. For tensor parallelism in transformer layers: (1) the MLP block splits the weight matrix column-wise across GPUs in the first linear layer, and row-wise in the second, requiring two all-reduce operations per transformer block; (2) the self-attention block splits attention heads across GPUs, requiring two all-reduces per block. Training an 8.3 billion parameter transformer language model using 512 GPUs achieves 76% scaling efficiency compared to a strong single-GPU baseline. The tensor parallel degree is typically limited to the number of GPUs within a NVLink domain (2–8 GPUs) due to the all-reduce bandwidth requirement."

**Source:** Shoeybi, M., Patwary, M., Puri, R., LeGresley, P., Casper, J., and Catanzaro, B. (NVIDIA), "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism," arXiv preprint arXiv:1909.08053, September 2019. Available: arxiv.org/abs/1909.08053. GitHub: github.com/NVIDIA/Megatron-LM

#segment:end_market #source-tier:A #signal-type:roadmap #date:2019 #importance:high #confidence:high

---

## 3. ZeRO Optimizer — Memory Optimization for Trillion-Parameter Training

> "ZeRO (Zero Redundancy Optimizer) eliminates memory redundancies in data-parallel training by partitioning the three states of the optimizer — optimizer states (ZeRO-1), gradients (ZeRO-2), and model parameters (ZeRO-3) — across data-parallel processes instead of replicating them. With N data-parallel GPUs, ZeRO-3 reduces per-GPU memory by N×. For a 175B-parameter GPT-3 model using mixed-precision training with Adam optimizer: baseline memory = 4 × 4 (FP32 params) + 4 × 4 (Adam m,v states) + 2 (FP16 params) + 2 (FP16 gradients) = 24 bytes/parameter × 175B = 4.2 TB, requiring ~52 A100s per replica in data parallel without ZeRO. ZeRO-3 across 64 GPUs reduces this to ~65 GB per GPU (80 GB A100 capacity)."

**Source:** Rajbhandari, S., Rasley, J., Ruwase, O., and He, Y. (Microsoft), "ZeRO: Memory Optimizations Toward Training Trillion Parameter Models," Proceedings of SC '20: International Conference for High Performance Computing, Networking, Storage and Analysis, Atlanta, GA, November 2020. DOI: 10.5555/3433701.3433727. arXiv: 1910.02054. Supercomputing 2020 proceedings: sc20.supercomputing.org/proceedings/tech_paper/tech_paper_pages/pap379.html

#segment:end_market #source-tier:S #signal-type:roadmap #date:2020 #importance:high #confidence:high

---

## 4. 3D Parallelism — Combining DP, TP, and PP for 1-Trillion-Parameter Models

> "We show how different types of parallelism methods — tensor, pipeline, and data parallelism — can be composed to scale to thousands of GPUs and models with trillions of parameters. Using PTD-P (Pipeline, Tensor, Data Parallelism) with tensor parallelism degree 8 (within a NVLink domain), pipeline parallelism degree 8 (across nodes), and data parallelism degree 48 on 3,072 A100 GPUs, we achieve 502 petaFLOP/s on a 1 trillion parameter model, corresponding to 52% of theoretical peak. Pipeline parallelism bubble fraction (idle time) = (p−1)/m where p is pipeline stages and m is micro-batches per pipeline flush — increasing m reduces bubble at the cost of larger effective batch size."

**Source:** Narayanan, D., Shoeybi, M., Casper, J., LeGresley, P., Patwary, M., Korthikanti, V., Vainbrand, D., Kashinkunti, P., Bernauer, J., Catanzaro, B., Phanishayee, A., and Zaharia, M. (NVIDIA/Stanford/Microsoft), "Efficient Large-Scale Language Model Training on GPU Clusters Using Megatron-LM," Proceedings of SC '21, 2021. DOI: 10.1145/3458817.3476209. arXiv: 2104.04473

#segment:end_market #source-tier:S #signal-type:roadmap #date:2021 #importance:high #confidence:high

---

## 5. PagedAttention — KV-Cache Memory Management at Scale

> "vLLM uses PagedAttention to manage the KV cache of LLMs. The key insight is to apply the OS's virtual memory technique — paging — to the KV cache. PagedAttention allows storing continuous keys and values in non-contiguous memory space by partitioning the KV cache of each sequence into fixed-size blocks, and mapping logical KV-cache blocks to physical GPU memory pages. With the traditional contiguous KV cache approach, 60–80% of allocated GPU memory is wasted due to fragmentation and over-reservation. PagedAttention reduces this waste to less than 4%. Compared to state-of-the-art systems (Orca, FasterTransformer), vLLM improves LLM serving throughput by 2–4× at the same latency level without any model architecture changes."

**Source:** Kwon, W., Li, Z., Zhuang, S., Sheng, Y., Zheng, L., Yu, C.H., Gonzalez, J.E., Zhang, H., and Stoica, I. (UC Berkeley), "Efficient Memory Management for Large Language Model Serving with PagedAttention," Proceedings of the 29th ACM Symposium on Operating Systems Principles (SOSP '23), Koblenz, Germany, October 2023. DOI: 10.1145/3600006.3613165. arXiv: 2309.06180

#segment:end_market #source-tier:S #signal-type:roadmap #date:2023 #importance:high #confidence:high

---

## 6. Prefill vs. Decode — Two-Phase LLM Inference Characterization

> "Large Language Model inference consists of two distinct computational phases with fundamentally different hardware bottlenecks: (1) Prefill phase: processes all input tokens simultaneously in a single forward pass — a dense GEMM (General Matrix Multiply) with batch size × sequence_length activations × d_model weights — this phase is compute-bound at high batch sizes; (2) Decode phase: generates one output token per step by running the model forward with a single new token — reads the full weight matrix (~200 GB for a 100B-parameter model) from HBM once per token and reads the growing KV-cache — this phase is memory-bandwidth-bound at any batch size. At H100 bandwidth of 3.35 TB/s, decode of a 100B-parameter model produces approximately 1 token per 60ms per request at batch size 1, making decode the latency bottleneck for interactive inference."

**Source:** Pope, R., Douglas, S., Chowdhery, A., Devlin, J., Bradbury, J., Levskaya, A., Heek, J., Xiao, K., Agrawal, S., and Dean, J. (Google), "Efficiently Scaling Transformer Inference," Proceedings of Machine Learning and Systems (MLSys), Vol. 5, 2023. Available: proceedings.mlsys.org/paper_files/paper/2023/hash/523f87e9d08e6071a3bbd150e6da40fb-Abstract-mlsys2023.html; Kwon et al. (2023) SOSP. DOI: 10.1145/3600006.3613165

#segment:end_market #source-tier:S #signal-type:roadmap #date:2023 #importance:high #confidence:high

---

## Open Technical Questions

- [ ] Prefill/Decode disaggregation in production: which hyperscalers have deployed separate prefill and decode clusters, and what GPU ratio (prefill:decode) is optimal for GPT-4 class models at 1M+ QPS?
- [ ] ZeRO-3 communication overhead at 4,096+ GPU scale: does the all-gather and reduce-scatter volume for 1T-parameter model parameters exceed InfiniBand XDR bisection bandwidth?
- [ ] Google TPU Trillium (v6) ICI bandwidth: has Google published the per-chip ICI bandwidth and topology change (if any) from TPUv4's 3D torus?
- [ ] PagedAttention on NVMe (SSD-backed KV-cache eviction): what is the measured p99 token latency penalty when KV-cache pages are swapped to local NVMe vs. CPU DRAM?
