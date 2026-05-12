# AI Networking Architecture — Academic Technical Reference

**Segment:** AI Cluster Networking  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-12 (Cycle 5)  
**Sources:** InfiniBand Trade Association (IBTA) specifications; IETF RoCE/RoCEv2 RFCs; IEEE 802.3 Ethernet; NVIDIA networking whitepapers; academic papers on collective communications

---

## 1. InfiniBand Architecture

### Physical Layer and Signaling

> "InfiniBand uses a point-to-point switched fabric topology. Each link is a bidirectional serial connection using NRZ (non-return-to-zero) encoding (HDR/NDR) or PAM4 (XDR 800G). Link rates: SDR (2.5 Gbps, 2001), DDR (5 Gbps), QDR (10 Gbps), FDR (14 Gbps), EDR (25 Gbps), HDR (50 Gbps), NDR (100 Gbps/lane = 200 Gbps/port with 2-lane), XDR (200 Gbps/lane = 400 Gbps/port). NDR InfiniBand (400 Gb/s per port) is the dominant AI cluster interconnect as of 2025. XDR (800 Gb/s per port) began volume production in 2025 for Stargate and Oracle clusters."

**Source:** InfiniBand Architecture Specification Volume 1, InfiniBand Trade Association (IBTA), Rev 1.7, 2023; NVIDIA ConnectX-7 Product Brief (NDR), 2022; NVIDIA Quantum-X800 XDR Switch Brief, 2024

#segment:network #source-tier:S #signal-type:roadmap #date:2023 #importance:high #confidence:high

---

### RDMA (Remote Direct Memory Access)

> "InfiniBand provides native RDMA (Remote Direct Memory Access), enabling a GPU to write data directly to the memory of another GPU across the network without involving the host CPU. RDMA operations: (1) RDMA Write — write local buffer to remote address; (2) RDMA Read — read from remote address into local buffer; (3) Send/Receive — two-sided operations requiring CPU involvement. RDMA eliminates the CPU copy-in/copy-out that plagues TCP/IP networking, reducing AI collective communication latency from ~1ms (TCP) to ~1µs (InfiniBand RDMA). NCCL (NVIDIA Collective Communications Library) uses RDMA Write operations for all-reduce."

**Source:** InfiniBand Architecture Specification (IBTA), 2023; "RDMA over Commodity Ethernet (RoCE)," IBTA, 2010; NVIDIA NCCL Documentation, NVIDIA, 2022

#segment:network #source-tier:S #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

### InfiniBand Fat-Tree Topology for AI Clusters

> "AI clusters use a fat-tree switch topology (also called Clos network or folded Clos) to provide non-blocking all-to-all communication between GPU nodes. A 2-layer fat-tree with k-port switches supports k²/4 nodes with full bisection bandwidth. For NDR (400G), a 2-layer fat-tree with 64-port Quantum-2 switches supports 2,048 GPU nodes at full bisection. NVIDIA DGX SuperPOD uses a 3-layer fat-tree for clusters of 128–8,192 DGX H100 systems. Key property: any GPU can communicate with any other GPU at the same rate, enabling efficient NCCL all-reduce without link congestion in balanced workloads."

**Source:** "A Scalable, Commodity Data Center Network Architecture," ACM SIGCOMM, Al-Fares et al., 2008; NVIDIA DGX SuperPOD Reference Architecture Guide, NVIDIA, 2023

#segment:network #source-tier:S #signal-type:roadmap #date:2008 #importance:high #confidence:high

---

## 2. Collective Communication Operations for AI Training

### All-Reduce — The Dominant AI Training Collective

> "All-reduce is the collective operation that synchronizes gradient updates across all GPU nodes in distributed training. After each backward pass, each GPU holds gradients for a subset of parameters. All-reduce sums these gradients across all GPUs so every GPU gets the same global gradient. Ring-all-reduce (Baidu, 2017) achieves optimal bandwidth utilization: GPUs form a logical ring; each GPU sends and receives 1/N of the gradient per step, requiring exactly 2(N-1)/N total data transferred per GPU regardless of N. For 1024 GPUs and 100 GB gradient: ring-all-reduce transfers 200 GB per GPU vs naive broadcast which transfers 100 TB."

**Source:** "Bringing HPC Techniques to Deep Learning," Baidu Research, Gibiansky, 2017; "Accurate, Large Minibatch SGD: Training ImageNet in 1 Hour," Facebook AI Research, 2017; NVIDIA NCCL Developer Guide, 2023

#segment:network #source-tier:S #signal-type:roadmap #date:2017 #importance:high #confidence:high

---

### All-to-All — Mixture of Experts (MoE) Communication

> "All-to-all collective operations send different data from each GPU to every other GPU — the output of GPU i sent to GPU j equals the input of GPU j from GPU i. This pattern dominates in Mixture of Experts (MoE) transformer architectures, where each token must be routed to the GPU hosting the relevant expert. All-to-all scales as O(N) in message size and requires full bisection bandwidth (unlike all-reduce which is bandwidth-efficient on rings). MoE models (GPT-4 estimated ~8 experts, Mixtral-8x7B) require InfiniBand or NVLink scale-out fabric with high bisection bandwidth to avoid MoE communication becoming the training bottleneck."

**Source:** "Outrageously Large Neural Networks: The Sparsely-Gated Mixture-of-Experts Layer," ICLR, Shazeer et al., 2017; NVIDIA Megatron-LM MoE Implementation, GitHub, 2023; "Switch Transformers: Scaling to Trillion Parameter Models," JMLR, Google, 2022

#segment:network #source-tier:S #signal-type:roadmap #date:2017 #importance:high #confidence:high

---

## 3. RDMA over Converged Ethernet (RoCEv2)

### RoCEv2 Protocol Stack

> "RoCEv2 (RDMA over Converged Ethernet version 2) encapsulates InfiniBand transport layer packets in UDP/IP over standard Ethernet, enabling RDMA semantics without InfiniBand hardware. RoCEv2 requires Priority Flow Control (PFC, IEEE 802.1Qbb) or DCQCN (Data Center Quantized Congestion Notification) to prevent packet loss that would trigger expensive RDMA retransmission. Performance gap vs InfiniBand: RoCEv2 adds ~5–10µs latency over InfiniBand (~1µs) due to Ethernet congestion control overhead. Hyperscalers (Microsoft Azure, Meta) use RoCEv2 extensively for cost-optimized AI training clusters on Ethernet."

**Source:** "RoCEv2: RDMA Over Converged Ethernet v2," InfiniBand Trade Association, 2014; "DCQCN: Congestion Control for Large-Scale RDMA Deployments," ACM SIGCOMM, Zhu et al., 2015; Meta AI Research Blog: RoCE for AI training, 2022

#segment:network #source-tier:S #signal-type:roadmap #date:2014 #importance:high #confidence:high

---

## 4. NVIDIA Spectrum-X — Ethernet AI Fabric

### Spectrum-X Architecture

> "NVIDIA Spectrum-X combines three components: (1) Spectrum-4 Ethernet switch ASIC (51.2 Tbps); (2) ConnectX-7 / BlueField-3 DPU with NVIDIA SHARP (Scalable Hierarchical Aggregation and Reduction Protocol) support; (3) NVIDIA RAIL optimization software. SHARP performs in-network computation — rather than sending all gradients from all GPUs to a reducer, SHARP aggregates gradients inside the switch itself, reducing host-to-switch traffic by up to N× where N is the number of nodes participating in all-reduce. SHARP turns the switch into a compute node for gradient aggregation."

**Source:** NVIDIA Spectrum-X Architecture Brief, NVIDIA, 2023; "SHARP: NVIDIA In-Network Computing Platform for AI," IEEE/ACM Hot Chips, NVIDIA, 2022

#segment:network #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

## 5. Ultra Ethernet Consortium (UEC) — Technical Specification

### UEC 1.0 Protocol Architecture

> "The Ultra Ethernet Consortium (UEC) 1.0 specification (released June 11, 2025) defines a vertically integrated networking stack for AI and HPC workloads over standard Ethernet physical layers. Key innovations over standard Ethernet/RoCEv2: (1) Programmable Congestion Management (PCM) replacing PFC/DCQCN with finer-grained control; (2) Advanced Collective Operations (ACO) enabling in-network reduction similar to SHARP but in a standard body; (3) Scalable Transport Protocol supporting both lossless and loss-tolerant operation; (4) Unified management plane for AI cluster observability. UEC targets parity with InfiniBand latency (<5µs) on Ethernet physical layer hardware."

**Source:** Ultra Ethernet Consortium UEC 1.0 Specification, UEC, 2025-06-11 (ultraethernet.org); HPCwire UEC 1.0 release coverage, 2025-06-11

#segment:network #source-tier:A #signal-type:roadmap #date:2025-06-11 #importance:high #confidence:high

---

## 6. Network Topology Options for AI Clusters

| Topology | Description | Bisection BW | AI Use | Scale |
|---|---|---|---|---|
| Fat-Tree (Clos) | K-ary N-tree; non-blocking | Full | Dominant for InfiniBand clusters | Up to millions of nodes |
| Dragonfly | Groups connected by all-to-all links | ~50% | HPC; some AI | 10K–100K nodes |
| Torus | Nodes on an N-dimensional grid | Varies | TPU ICI (Google) | Google TPU pods |
| Rail-Only | Direct GPU-to-GPU per rail; no fabric | Limited | Small clusters | 8–64 GPUs |
| NVLink (intra-rack) | Switch-based full mesh within rack | Full (intra-rack) | NVIDIA NVL72 | 72 GPUs per rack |

**Source:** "A Comparative Study of Interconnect Topologies for HPC and AI," IEEE SC23 Proceedings, 2023; Google TPU Pod Architecture documentation, Google, 2022

#segment:network #source-tier:S #signal-type:roadmap #date:2023 #importance:medium #confidence:high

---

## Open Technical Questions

- [ ] UEC 1.0 Programmable Congestion Management (PCM): how does it compare to DCQCN in measured AI workload performance?
- [ ] NVIDIA SHARP in-network computing: what fraction of all-reduce time is eliminated in practice for large (1,000+ GPU) clusters?
- [ ] All-to-all communication scaling for MoE models at 10,000+ GPU scale: does InfiniBand fat-tree remain the optimal topology?
- [ ] XDR InfiniBand 800G: what is the actual latency vs NDR 400G for all-reduce operations?
