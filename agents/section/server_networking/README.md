# Network Expert Agent

**Segment:** AI Networking / Interconnect  
**Sales Lens:** AI cluster fabric, high-speed interconnect, switch ASIC market  
**Last Updated:** 2026-05-12

---

## Overview

AI training clusters require ultra-low latency, high-bandwidth networking between thousands of GPUs — fundamentally different from traditional data center networking. Two competing paradigms define the market: InfiniBand (NVIDIA Quantum/NDR), which dominates large-scale AI training, and Ethernet (Ultra Ethernet Consortium / Spectrum-X), which is challenging for AI workloads. Networking represents 10–15% of total AI cluster cost and is becoming a strategic differentiator. Per-GPU bandwidth requirements scale from 400Gb/s (H100) to 800Gb/s (B200/GB200) to 1.6Tb/s (next-gen 2026+).

---

## How AI Networking Works

### 2023 — InfiniBand NDR (400Gb/s) Becomes AI Training Standard

> "InfiniBand NDR delivers 400Gb/s per port, enabling all-reduce collective operations across 10,000+ GPU clusters with sub-microsecond latency. This latency profile is required for gradient synchronization in large model training."

**Source:** NVIDIA Quantum-2 InfiniBand Architecture Technical Brief, NVIDIA Corporation, 2023

#segment:network #source-tier:A #signal-type:roadmap #company:nvidia #date:2023 #importance:high #confidence:high

---

### 2022 — Ultra Ethernet Consortium (UEC) Founded; Ethernet AI Challenge

> "The Ultra Ethernet Consortium was founded by AMD, Intel, Broadcom, Google, and Meta to develop Ethernet specifications suitable for AI workload all-reduce operations, targeting <10μs end-to-end latency."

**Source:** Ultra Ethernet Consortium Founding Press Release, UEC, 2022-07

#segment:network #source-tier:A #signal-type:roadmap #date:2022-07 #importance:high #confidence:high

---

### 2014 — RDMA over Converged Ethernet (RoCE) Enables AI-Grade Ethernet

> "RDMA over Converged Ethernet v2 (RoCEv2) provided kernel-bypass networking for Ethernet, enabling latencies approaching InfiniBand for specific workloads and establishing the technical foundation for UEC."

**Source:** IEEE 802.1Q RoCEv2 Specification, IEEE, 2014

#segment:network #source-tier:S #signal-type:roadmap #date:2014 #importance:low #confidence:high

---

## History

### 2025 — NVIDIA Spectrum-X Deployed at Microsoft Azure for AI Workloads

> Microsoft Azure announced deployment of NVIDIA Spectrum-X (Ethernet-based AI networking) for AI workloads, providing an Ethernet alternative to InfiniBand within NVIDIA's ecosystem. First major hyperscaler Spectrum-X deployment.

**Source:** Microsoft Azure Networking Blog, "Spectrum-X on Azure," Microsoft, 2025-Q2

#segment:network #source-tier:A #signal-type:design-win #company:nvidia #company:microsoft #date:2025 #importance:high #confidence:high

---

### 2024 — Meta AI Cluster: 24,576 GPUs on 400G InfiniBand Disclosed

> "Meta's AI Research SuperCluster (RSC) Phase 2 consists of 24,576 H100 GPUs connected via 400G InfiniBand NDR fabric, representing one of the largest publicly disclosed AI training clusters."

**Source:** Meta AI Research SuperCluster Technical Blog, Meta AI, 2024

#segment:network #source-tier:A #signal-type:demand #company:meta #date:2024 #importance:high #confidence:high

---

### 2023 — NVIDIA Acquires Full InfiniBand Stack via Mellanox; Vertical Integration Complete

> NVIDIA's 2020 Mellanox acquisition gave it full vertical integration: GPU + NIC (ConnectX) + switch (Quantum-2) + cables + software (NCCL). This stack lock-in became NVIDIA's networking moat.

**Source:** NVIDIA FY2021 10-K, SEC EDGAR, 2021; NVIDIA Networking Product Portfolio 2023

#segment:network #source-tier:A #signal-type:supply #company:nvidia #date:2023 #importance:high #confidence:high

---

### 2022 — Arista Networks Enters AI Cluster Fabric Market

> Arista Networks introduced the 7800R4 series targeting AI cluster spine/leaf deployments, competing with NVIDIA Spectrum for Ethernet-based AI fabrics at hyperscale.

**Source:** Arista Networks FY2022 10-K, SEC EDGAR, 2023

#segment:network #source-tier:A #signal-type:roadmap #date:2022 #importance:medium #confidence:high

---

## Supply Chain

### 2025 — 800G Optical Transceivers: Tight Supply; CPO Emerging as Solution

> 800G QSFP-DD optical transceivers for InfiniBand XDR and Ultra Ethernet are supply-constrained in 2025. Co-packaged optics (CPO) is being developed by Intel, Broadcom, and Marvell as a capacity solution.

**Source:** "AI Networking Supply Chain," Yole Développement, 2025-Q3

#segment:network #source-tier:B #signal-type:supply #date:2025 #importance:medium #confidence:medium

---

### 2025 — Switch ASIC (Tomahawk 5, Jericho3) at TSMC N5; Improving Supply

> Broadcom Tomahawk 5 (51.2 Tb/s) and Jericho3 (routing) fabricated at TSMC N5. Supply constraints from 2023–2024 are improving. Switch ASICs deliver the spine capacity for Ethernet AI fabrics.

**Source:** Broadcom FY2025 10-K, SEC EDGAR, 2025-12; TSMC Q4 2025 Earnings Call, 2026-01

#segment:network #source-tier:A #signal-type:supply #date:2025 #importance:medium #confidence:high

---

### 2024 — NVIDIA NDR InfiniBand Lead Times: Improving from 24 to 12–16 Weeks

> NVIDIA Quantum-2 InfiniBand NDR switch lead times improved from 20–24 weeks (2023 peak) to 12–16 weeks by mid-2024 as TSMC switch ASIC capacity expanded.

**Source:** NVIDIA Q3 FY2025 Earnings Call, NVIDIA Investor Relations, 2024-11

#segment:network #source-tier:A #signal-type:supply #company:nvidia #date:2024 #importance:medium #confidence:high

---

## Competition

### 2026 — InfiniBand vs Ethernet Market Share: InfiniBand ~65%, Ethernet ~35%

> InfiniBand retains ~65% of AI training cluster interconnect revenue. Ethernet (Spectrum-X + traditional) growing to ~35% driven by Ethernet-native hyperscalers (Google, Arista/Broadcom deployments).

**Source:** "AI Networking Market Share," Dell'Oro Group Report, 2026-Q1

#segment:network #source-tier:B #signal-type:demand #date:2026 #importance:high #confidence:medium

---

### 2025 — Ultra Ethernet Consortium 1.0 Spec Released; Sampling Begins

> Ultra Ethernet 1.0 specification was released. Early silicon sampling from Broadcom, Intel, and AMD/Pensando. Full production deployments targeting 2026 for hyperscalers choosing Ethernet-native AI fabrics.

**Source:** Ultra Ethernet Consortium 1.0 Release Announcement, UEC, 2025-Q2

#segment:network #source-tier:A #signal-type:roadmap #date:2025 #importance:high #confidence:high

---

### 2025 — Broadcom Tomahawk 5: 51.2 Tb/s; Dominant Hyperscaler Ethernet Switch

> Broadcom Tomahawk 5 (51.2 Tb/s port capacity) is the primary switching ASIC in hyperscaler Ethernet AI fabrics. Google, Meta, and Amazon deploy Tomahawk-based Arista or white-box switches.

**Source:** Broadcom Tomahawk 5 Product Brief, Broadcom Corporation, 2025; Arista Networks FY2025 10-K, SEC EDGAR, 2025

#segment:network #source-tier:A #signal-type:supply #date:2025 #importance:medium #confidence:high

---

## Technology Roadmap

### 2026+ — InfiniBand XDR: 800Gb/s Per Port; GB200 Clusters

> InfiniBand XDR (800Gb/s) is required for NVIDIA GB200 NVL72 rack-scale deployments. Each GPU requires 800Gb/s NIC bandwidth for NVLink-to-fabric bridging. Quantum-3 switch in sampling.

**Source:** NVIDIA InfiniBand XDR Product Brief, NVIDIA Corporation, 2025; NVIDIA GTC 2026 Keynote, 2026-03

#segment:network #source-tier:A #signal-type:roadmap #company:nvidia #date:2025 #importance:high #confidence:high

---

### 2026+ — Co-Packaged Optics (CPO): 3.2Tb/s Per Port; Next-Gen Fabric Density

> Co-packaged optics integrates optical transceivers directly on the switch ASIC package, eliminating pluggable transceiver power loss. Targets 3.2Tb/s per port for post-2026 AI cluster fabrics.

**Source:** Intel CPO Development Program, Intel, 2025; Broadcom CPO Initiative, Broadcom, 2025

#segment:network #source-tier:A #signal-type:roadmap #date:2025 #importance:medium #confidence:high

---

### 2025 — Ultra Ethernet 800G: Production Sampling; 2026 Deployment Target

> Ultra Ethernet 800G specification with <5μs end-to-end latency for AI all-reduce operations. Broadcom, Intel, AMD/Pensando shipping engineering samples. Hyperscaler production deployments expected 2026.

**Source:** Ultra Ethernet Consortium Technical Roadmap, UEC, 2025

#segment:network #source-tier:A #signal-type:roadmap #date:2025 #importance:high #confidence:high

---

## AI Cluster Deployments

### 2025 — Per-GPU Bandwidth Requirements Scaling 2× Per GPU Generation

> Per-GPU network bandwidth: A100 → 200Gb/s, H100 → 400Gb/s, B200/GB200 → 800Gb/s, Next-gen (2026+) → 1.6Tb/s. This scaling drives the optical transceiver and switch ASIC upgrade cycle in sync with GPU generations.

**Source:** NVIDIA GPU Networking Roadmap Presentation, NVIDIA GTC 2025, 2025-03

#segment:network #source-tier:A #signal-type:demand #company:nvidia #date:2025-03 #importance:high #confidence:high

---

### 2024 — NVIDIA BlueField-3 DPU: SmartNIC Offloading in AI Clusters

> NVIDIA BlueField-3 DPU offloads network processing (encryption, compression, RDMA) from CPU cores in AI clusters, freeing CPU cycles for AI workload management. Deployed at Microsoft, Amazon.

**Source:** NVIDIA BlueField-3 Product Brief, NVIDIA Corporation, 2024; Microsoft Azure DPDK Integration, 2024

#segment:network #source-tier:A #signal-type:design-win #company:nvidia #date:2024 #importance:medium #confidence:high

---

## Open Questions

- [ ] Ultra Ethernet 1.0 production deployment — which hyperscalers shipping at scale in 2026?
- [ ] NVIDIA Spectrum-X traction — how many hyperscalers deploying vs InfiniBand?
- [ ] CPO mainstream timeline — which GPU generation first requires CPO vs pluggable optics?
- [ ] Arista revenue from AI networking — what % of FY2026 revenue is AI cluster fabric?
