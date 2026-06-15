# NAND Flash & Storage Architecture — Academic Technical Reference

**Segment:** NAND Flash / Storage  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-13 (Cycle 6)  
**Sources:** Proceedings of the IEEE (Bez et al. 2003); IEEE VLSI (Tanaka et al. 2007); IEEE MICRO (Grupp et al. 2009); IEEE ISSCC (Masuoka/Toshiba 1987); NVMe Base Specification (NVMe Association 2019)

---

## 1. NAND Flash Cell Physics — NOR and NAND Architecture Origins

> "The paper focuses on the development of NOR flash memory technology, describing the basic functionality of the flash memory cell and the main cell architectures. The NOR flash cell stores a bit as charge on a floating polysilicon gate insulated from the channel by a thin tunnel oxide. The floating gate threshold voltage (Vt) shift caused by stored charge is detected during a read operation. The paper also discusses main reliability issues: charge retention (data retention over 10 years at operating temperature) and endurance (number of program/erase cycles before the tunnel oxide degrades). The multilevel approach (2 bits per cell) is also described, where two voltage distributions for '1' and '0' per bit are compressed into the same Vt window."

**Source:** Bez, R., Camerlenghi, E., Modelli, A., and Visconti, A. (STMicroelectronics), "Introduction to Flash Memory," Proceedings of the IEEE, Vol. 91, No. 4, pp. 489–502, April 2003. DOI: 10.1109/JPROC.2003.811702

#segment:storage #source-tier:S #signal-type:roadmap #date:2003 #importance:high #confidence:high

---

## 2. NAND Flash Invention — Toshiba's Original Cell Design

> "The NAND-type flash memory, first presented at IEEE IEDM in 1987 by Fujio Masuoka and colleagues at Toshiba Corporation, achieved higher cell density than NOR flash by connecting multiple floating-gate transistors in series (forming a NAND string) rather than in parallel. A NAND string of 8–32 cells shares the source/drain diffusion regions between adjacent transistors, eliminating individual cell contacts and achieving 2F² or smaller cell area (vs. 10F² for NOR, where F is the minimum feature size). This cell area advantage is the fundamental reason NAND flash dominated storage applications while NOR flash remained in code storage. Toshiba launched commercial NAND flash products in 1989."

**Source:** Masuoka, F., Momodomi, M., Iwata, Y., and Shirota, R. (Toshiba Corporation), "New Ultra High Density EPROM and Flash EEPROM with NAND Structure Cell," Technical Digest of the IEEE International Electron Devices Meeting (IEDM), San Francisco, CA, 1987, pp. 552–555. IEEE Spectrum, "Chip Hall of Fame: Toshiba NAND Flash Memory," 2013. Available: spectrum.ieee.org/chip-hall-of-fame-toshiba-nand-flash-memory

#segment:storage #source-tier:S #signal-type:roadmap #date:1987 #importance:high #confidence:high

---

## 3. BiCS 3D NAND — Vertical Channel Architecture

> "The Bit Cost Scalable (BiCS) technology realizes a multi-stacked memory array with only a few constant critical lithography steps, regardless of the number of stacked layers, to keep continuous reduction in bit cost. The fundamental innovation is replacing the horizontal planar NAND string with a vertical polysilicon channel pillar drilled through alternating conductor (wordline) and insulator layers via a 'punch and plug' process. Each vertical channel pillar forms a NAND string of cells corresponding to the number of stacked conductor layers. Since the number of lithography steps does not scale with layer count, BiCS enables cost-effective increases in bit density by increasing vertical layer count."

**Source:** Tanaka, H., Kido, M., Yahashi, K., Oomura, M., Katsumata, R., Kito, M., Fukuzumi, Y., Sato, M., Nagata, Y., Matsuoka, Y., Iwata, Y., Aochi, H., and Nitayama, A. (Toshiba Corporation), "Bit Cost Scalable Technology with Punch and Plug Process for Ultra High Density Flash Memory," 2007 IEEE Symposium on VLSI Technology, Digest of Technical Papers, Kyoto, Japan, pp. 14–15, June 2007. IEEE Xplore: ieeexplore.ieee.org/document/4339708

#segment:storage #source-tier:S #signal-type:roadmap #date:2007 #importance:high #confidence:high

---

## 4. Flash Memory Characterization — Performance, Power, and Reliability Empirics

> "We present a detailed empirical characterization of flash memory technology from five manufacturers by directly measuring the performance, power, and reliability of flash chips. We find that performance varies significantly between vendors, devices, and from publicly available datasheets. We demonstrate unexpected device characteristics and show how they can be used to improve the responsiveness and energy consumption of solid-state disks by 44% and 13%, respectively, as well as increase flash device lifetime by 5.2×. The characterization revealed that internal parallelism within flash chips (multiple planes, interleaved banks) is the primary driver of peak throughput and that managing this parallelism in the Flash Translation Layer is critical for achieving datasheet-level performance."

**Source:** Grupp, L.M., Caulfield, A.M., Coburn, J., Swanson, S., Yaakobi, E., Siegel, P.H., and Wolf, J.K. (UC San Diego), "Characterizing Flash Memory: Anomalies, Observations, and Applications," Proceedings of the 42nd Annual IEEE/ACM International Symposium on Microarchitecture (MICRO), New York, NY, pp. 24–33, December 2009. DOI: 10.1145/1669112.1669118

#segment:storage #source-tier:S #signal-type:roadmap #date:2009 #importance:high #confidence:high

---

## 5. NVMe Protocol — Low-Latency Storage Interface Specification

> "NVMe (Non-Volatile Memory Express) is a scalable host controller interface designed to address the needs of PCI Express (PCIe)-based solid-state drives. NVMe significantly increases performance over legacy AHCI (Advanced Host Controller Interface): NVMe supports up to 65,535 I/O queues with up to 65,535 commands per queue, versus a single queue with 32 commands for AHCI. The NVMe 1.4 specification (2019) introduced I/O Determinism (NVMe-ID) to partition an SSD into independent groups with predictable latency, and Persistent Memory Region (PMR) support for direct load/store access to SSD memory. NVMe command completion latency is typically 70–100µs vs. 500µs for SATA AHCI."

**Source:** NVM Express Industry Association, "NVM Express Base Specification," Revision 1.4, June 10, 2019. Available: nvmexpress.org/wp-content/uploads/NVM-Express-1_4-2019.06.10-Ratified.pdf

#segment:storage #source-tier:S #signal-type:roadmap #date:2019 #importance:high #confidence:high

---

## 6. PCIe Gen 5 Bandwidth — Storage Interface Roadmap

> "PCI Express (PCIe) 5.0 doubles the per-lane data rate from Gen 4's 16 GT/s to 32 GT/s, delivering approximately 4 GB/s per lane (unidirectional) at 128b/130b encoding efficiency of 98.5%. A PCIe 5.0 ×4 NVMe SSD achieves approximately 14–15 GB/s sequential read bandwidth. PCIe 6.0 (draft, 2022) targets 64 GT/s using PAM4 (Pulse Amplitude Modulation, 4 levels) signaling, doubling to ~8 GB/s per lane. For AI training workloads, sequential read bandwidth from NVMe SSDs is the critical metric for dataset prefetching: a 14 GB/s PCIe 5.0 ×4 SSD can sustain the 10–12 GB/s throughput needed to keep an H100 GPU data-pipeline-saturated during ImageNet-scale training."

**Source:** PCI-SIG, "PCI Express Base Specification," Revision 5.0, Version 1.0, May 2019. Available: pcisig.com/specifications/pcie/base-specification; PCI-SIG, "PCI Express Base Specification," Revision 6.0 (draft), 2022.

#segment:storage #source-tier:S #signal-type:roadmap #date:2019 #importance:high #confidence:high

---

## Open Technical Questions

- [ ] BiCS 9 (300+ layer) and BiCS 10 (332-layer) etch aspect ratio: what is the empirically measured etch selectivity limit for HAR (high-aspect-ratio) etch at >300 layers?
- [ ] QLC NAND endurance for AI training checkpoint workloads: what overprovisioning (OP%) ratio is required to achieve 5-year enterprise SSD lifetime under sustained sequential write patterns?
- [ ] KV-SSD adoption for LLM inference KV-cache: has any hyperscaler published production deployment data for Samsung KV-SSD with vLLM or similar framework?
- [ ] Computational Storage Drive (CSD) for RAG: is in-SSD vector search feasible given current SSD controller compute budgets (~5W)?
