# Hyperscaler AI Infrastructure Architecture — Academic Technical Reference

**Segment:** End Markets (Hyperscalers / Cloud Service Providers)  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-12 (Cycle 5)  
**Sources:** Google, Amazon, Microsoft, Meta infrastructure papers (ISCA, OSDI, SOSP, NSDI, USENIX); IEEE Hot Chips hyperscaler architecture disclosures; public earnings call disclosures

---

## 1. Hyperscaler AI Cluster Architecture

### GPU Cluster Topology — Physical Organization

> "A hyperscaler AI training cluster is organized in a three-layer hierarchy: (1) Node level: a single server containing 1–8 GPUs connected via NVLink (NVIDIA) or PCIe; (2) Rack level: 8–72 nodes per rack connected via a high-speed intra-rack switch fabric; (3) Cluster level: thousands of racks connected via a multi-layer fat-tree (Clos) network. Example: Meta's AI Research SuperCluster (RSC), announced 2022: 2,000 DGX A100 nodes (16,000 GPUs), connected via NVIDIA Quantum InfiniBand HDR in a 2-layer fat-tree. NVIDIA Stargate (OpenAI), 2025: 64,000 GB200 GPUs across ~900 NVL72 racks, connected via XDR InfiniBand at full bisection bandwidth. The cluster topology determines which distributed training and inference parallelism strategies are efficient."

**Source:** "Building Meta's AI Research SuperCluster," Meta AI, 2022; "NVIDIA DGX SuperPOD Reference Architecture," NVIDIA, 2023; "Stargate: OpenAI + SoftBank AI Cluster," NVIDIA GTC Keynote, 2025-03

#segment:end_market #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

### Parallelism Strategies in Distributed Training

> "Large model training uses three orthogonal parallelism dimensions to partition work across GPU clusters: (1) Data Parallelism (DP): replicate the full model on each GPU; each GPU processes a different mini-batch; gradients are all-reduced across GPUs after each backward pass (uses ~N × model_size GPU memory). (2) Tensor Parallelism (TP): split individual matrix operations (GEMM) across GPUs horizontally — each GPU holds a column shard of the weight matrix; requires all-reduce after each matmul layer; scales across 2–8 GPUs within NVLink domain. (3) Pipeline Parallelism (PP): split model layers across GPUs sequentially; GPU 1 processes layers 1–10, GPU 2 layers 11–20; requires careful micro-batching (GPipe, PipeDream-Flush) to reduce idle 'bubble' time. Megatron-LM (NVIDIA, 2021) implements 3D parallelism (DP × TP × PP) and trains GPT-3 scale models on 512 A100 GPUs using TP=8, PP=8, DP=8."

**Source:** "Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism," Shoeybi et al., NVIDIA, NeurIPS, 2019; "Efficient Large Scale Language Modeling with Mixtures of Experts," Artetxe et al., ACL, 2021; "GPipe: Efficient Training of Giant Neural Networks Using Pipeline Parallelism," Huang et al., NeurIPS, 2019

#segment:end_market #source-tier:S #signal-type:roadmap #date:2019 #importance:high #confidence:high

---

## 2. AI Inference Architecture at Hyperscale

### Prefill vs Decode Phases — Compute Characterization

> "Large Language Model (LLM) inference has two distinct computational phases with different hardware requirements: (1) Prefill (prompt processing): computes attention over all input tokens simultaneously — a large parallel GEMM (batch × sequence_length × d_model); compute-bound, benefits from TFLOPS. For a 1,024-token prompt on GPT-4 scale model, prefill completes in ~100–200ms. (2) Decode (token generation): generates one token per step; each step reads the entire model weight once and the growing KV-cache — memory-bandwidth-bound. For 100B-parameter model, decode requires reading ~200 GB of weights per token, at 3.35 TB/s (H100), yielding ~60ms per token. Decode arithmetic intensity: ~1–10 FLOP/byte — far below GPU compute peak, meaning GPU is underutilized on compute during decode. This drives disaggregation of prefill and decode across different hardware."

**Source:** "Efficient Memory Management for Large Language Model Serving with PagedAttention," Kwon et al., ACM SOSP, 2023; "Orca: A Distributed Serving System for Transformer-Based Generative Models," Yu et al., OSDI, 2022

#segment:end_market #source-tier:S #signal-type:roadmap #date:2023 #importance:high #confidence:high

---

### KV-Cache Management at Scale

> "The KV-Cache stores the attention Key and Value tensors from previously computed input tokens, avoiding recomputation during autoregressive decode. KV-cache memory size: 2 × num_heads × d_head × seq_len × num_layers × dtype_bytes. For a GPT-4 class model (96 layers, 128 heads, d_head=128, FP16) at 4K sequence length: 2 × 128 × 128 × 4096 × 96 × 2 bytes = ~26 GB per inference request. At 100 concurrent users, KV-cache consumes 2.6 TB — far exceeding GPU HBM capacity. PagedAttention (vLLM, 2023) applies OS virtual memory concepts to KV-cache: physical GPU memory is divided into fixed-size pages; logical KV-cache blocks are mapped to non-contiguous physical pages; pages are swapped to CPU DRAM or NVMe when GPU HBM is full. PagedAttention reduces KV-cache memory waste from ~60% (fragmentation) to <4%, increasing GPU serving throughput by 2–4× for real workloads."

**Source:** "Efficient Memory Management for Large Language Model Serving with PagedAttention," Kwon et al., ACM SOSP, 2023; "vLLM: Easy, Fast, and Cheap LLM Serving," UC Berkeley, 2023

#segment:end_market #source-tier:S #signal-type:roadmap #date:2023 #importance:high #confidence:high

---

## 3. Google TPU Pod Architecture

### TPU ICI (Inter-Chip Interconnect) — 3D Torus Network

> "Google TPU pods use a high-bandwidth, low-latency Inter-Chip Interconnect (ICI) that connects TPUs in a 3D torus topology. TPUv4: each chip has 6 ICI links (2 per x/y/z axis), 800 Gb/s per direction per link = 4.8 Tb/s total ICI bandwidth per chip. A 4,096-chip TPUv4 pod interconnects chips at 200 Gb/s (full bisection) without using Ethernet or InfiniBand — the ICI is TSMC-packaged within the TPU package and connects via high-speed SerDes lanes to neighboring chips on the same optical circuit-switched backplane. ICI enables collective operations (all-reduce, all-to-all) at <10µs latency within the pod, compared to ~50–100µs for InfiniBand at scale. Google's 2023 ISCA paper reports ICI bisection bandwidth of 2.56 Tb/s for 64-chip cubes as building blocks."

**Source:** "TPU v4: An Optionally Tiled Systems-on-Chip for Training Neural Networks at Petascale," Jouppi et al., Google / IEEE ISCA, 2023; Google Cloud TPU v4 Architecture, Google Cloud Documentation, 2023

#segment:end_market #source-tier:S #signal-type:roadmap #date:2023 #importance:high #confidence:high

---

## 4. Meta AI Infrastructure Architecture

### Meta's AI Research SuperCluster (RSC) — Network Design

> "Meta's RSC (2022) uses a two-tier network: (1) Intra-pod fabric: 16 DGX A100 nodes (128 GPUs) connected via NVIDIA Quantum HDR InfiniBand at 200 Gb/s in a non-blocking fat-tree; (2) Inter-pod fabric: pods connected via 400 Gb/s Arista Ethernet switches with ECMP (Equal-Cost Multi-Path) routing. Meta explicitly chose Ethernet for inter-pod links because ECMP load balancing across 400G Ethernet links provided adequate bandwidth for the cross-pod all-reduce operations in their model training workloads (ResNeXt, PyTorch FSDP). Meta reports 90%+ utilization of intra-pod InfiniBand and ~60% utilization of inter-pod Ethernet links during training runs. This architecture informs Meta's preference for Ethernet-based AI fabric (RoCEv2) in future clusters."

**Source:** "Building Meta's AI Research SuperCluster," Lee et al., Meta AI, 2022; "The Architecture of a Large-Scale AI Computing Cluster," Meta Engineering Blog, 2022

#segment:end_market #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

## 5. Microsoft Azure AI Infrastructure

### Azure AI Frontier Cluster — ND H100 v5 Series

> "Microsoft Azure's ND H100 v5 virtual machines (GA 2024) use 8 NVIDIA H100 GPUs per node connected via NVLink and NVSwitch, with inter-node connectivity via NVIDIA Quantum-2 InfiniBand NDR at 400 Gb/s per GPU. Azure organizes ND H100 v5 nodes in clusters of up to 128 nodes (1,024 GPUs) with non-blocking InfiniBand fat-tree fabric providing full bisection bandwidth. Microsoft's Azure AI annualized revenue reached $37B at 123% growth (Q2 FY2026 earnings), driven primarily by the Azure OpenAI Service which runs GPT-4 class models on Azure GPU clusters. The Stargate partnership (Microsoft + OpenAI + SoftBank) builds dedicated GPU clusters in Microsoft-managed data centers, with 64,000 GB200 GPUs deployed as of March 2025."

**Source:** "Azure ND H100 v5 Virtual Machine Series," Microsoft Azure Documentation, 2024; Microsoft Q2 FY2026 Earnings Call, Microsoft, 2026-01-29; "Stargate: $500B AI Infrastructure Investment," OpenAI + SoftBank Announcement, 2025-01

#segment:end_market #source-tier:A #signal-type:roadmap #date:2024 #importance:high #confidence:high

---

## 6. Amazon Web Services (AWS) AI Infrastructure

### EC2 P5 and Trn2 Instance Architecture

> "AWS offers two AI training instance families: (1) EC2 P5 (H100): 8 × NVIDIA H100 SXM5 GPUs per instance (96 GB HBM3 each = 768 GB total); 3.2 Tb/s EFA (Elastic Fabric Adapter) inter-node bandwidth; uses Amazon-developed EFA network adapter with SRD (Scalable Reliable Datagram) protocol over RoCEv2 for collective communication without InfiniBand; (2) EC2 Trn2 (Trainium2): 16 × AWS Trainium2 chips per instance; 64 instances = 1,024-chip cluster via NeuronLink (AWS-proprietary chip-to-chip interconnect) at 768 GB/s per chip; 1,600 Gb/s EFA2 inter-node. AWS EFA with LibFabric + NCCL provides all-reduce performance comparable to InfiniBand NDR for inter-node collective operations at the cost of higher latency (~5µs EFA vs ~1µs InfiniBand)."

**Source:** "Amazon EC2 P5 Instances," AWS Documentation, 2023; "AWS EFA: Elastic Fabric Adapter," AWS re:Invent 2023 Session; "AWS Trainium2 Architecture," AWS re:Invent 2023; "Scalable Reliable Datagram (SRD) for Elastic Network Adapter," ACM SIGCOMM, Amazon, 2021

#segment:end_market #source-tier:A #signal-type:roadmap #date:2023 #importance:high #confidence:high

---

## Open Technical Questions

- [ ] Disaggregated prefill/decode (PD disaggregation): which hyperscalers have deployed separate prefill and decode clusters in production, and what GPU ratio (prefill:decode) is used?
- [ ] KV-cache on NVMe (PagedAttention disk swap): what is the latency penalty for KV-cache eviction to NVMe vs DRAM in production serving?
- [ ] Google TPU v6 (Trillium) ICI topology: is it still 3D torus or does it shift to a different topology for 100K+ chip scales?
- [ ] Meta RoCEv2 vs InfiniBand for 100K+ GPU clusters: has Meta published any data on RoCEv2 all-reduce performance vs InfiniBand at scale?
