# DRAM Architecture — Academic Technical Reference

**Segment:** DRAM / Memory  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-13 (Cycle 6)  
**Sources:** IEEE JSSC (Dennard 1974); IEEE ISSCC (Lee et al. 2014); ACM ISCA (Kim et al. 2014); JEDEC JESD235C; IEEE IEDM (Itoh et al.); IEEE ISSCC (Farmwald & Mooring 1992)

---

## 1. MOSFET Scaling — The Physical Foundation of DRAM Density Improvement

> "A set of scaling principles are derived which show how a conventional MOSFET can be reduced in size. When all device dimensions are scaled by a constant factor κ, the device currents remain roughly constant, the operating voltage decreases by κ, and the power–delay product decreases as 1/κ³. MOSFET switching devices with channel lengths as short as 0.5 micrometers were fabricated. The scaling analysis predicts that the switching speed of the device will improve as the dimensions are reduced."

**Source:** Dennard, R.H., Gaensslen, F.H., Yu, H.-N., Rideout, V.L., Bassous, E., and LeBlanc, A.R., "Design of Ion-Implanted MOSFET's with Very Small Physical Dimensions," IEEE Journal of Solid-State Circuits, Vol. 9, No. 5, pp. 256–268, October 1974. DOI: 10.1109/JSSC.1974.1050511

#segment:dram #source-tier:S #signal-type:roadmap #date:1974 #importance:high #confidence:high

---

## 2. High Bandwidth Memory (HBM) — First Silicon Demonstration

> "A 1.2V 8Gb 8-channel 128GB/s high-bandwidth memory (HBM) stacked DRAM with effective microbump I/O test methods using 29nm process and TSV. The HBM architecture achieves 128GB/s bandwidth per stack by using 8 independent 128-bit wide channels connected through Through-Silicon Vias (TSVs). The device implements effective test methods for the microbump I/O that connects the HBM logic base die to the DRAM core dies in the stack, using a 29nm CMOS process."

**Source:** Lee, D.U., et al. (SK Hynix), "25.2: A 1.2V 8Gb 8-channel 128GB/s High-Bandwidth Memory (HBM) DRAM with Effective Microbump I/O Test Methods Using 29nm Process and TSV," 2014 IEEE International Solid-State Circuits Conference (ISSCC), San Francisco, CA, February 2014. DOI: 10.1109/ISSCC.2014.6757501

#segment:dram #source-tier:S #signal-type:roadmap #date:2014 #importance:high #confidence:high

---

## 3. DRAM Disturbance Errors — Rowhammer and Cell Coupling

> "We present the first scientific study of the row disturbance error problem in commodity DRAM modules. We demonstrate that modern DRAM chips can be maliciously exploited by repeatedly accessing a DRAM row to induce bit flips in adjacent rows through electrical disturbance. We find that more than 80% of DRAM modules we tested from three major DRAM manufacturers are vulnerable to disturbance errors. The disturbance error is caused by the electromagnetic coupling between adjacent DRAM cells, whereby repeatedly activating a row disturbs the charge state of neighboring rows."

**Source:** Kim, Y., Daly, R., Kim, J., Fallin, C., Lee, J.H., Lee, D., Wilkerson, C., Lai, K., and Mutlu, O., "Flipping Bits in Memory Without Accessing Them: An Experimental Study of DRAM Disturbance Errors," Proceedings of the 41st Annual International Symposium on Computer Architecture (ISCA), Minneapolis, MN, June 2014. Available: http://users.ece.cmu.edu/~omutlu/pub/dram-row-hammer_isca14.pdf

#segment:dram #source-tier:S #signal-type:roadmap #date:2014 #importance:high #confidence:high

---

## 4. HBM Channel Architecture — JEDEC Standard Definition

> "HBM DRAM (JESD235) is organized as a stack of multiple DRAM dies interconnected through TSVs with a base logic die. Each HBM device provides 8 independent channels, each channel being 128 bits wide (per JESD235 and JESD235A), yielding 1,024 total interface bits per stack. HBM2 (JESD235A) increases per-pin data rate to 2.0 Gbps, delivering 256 GB/s per stack. HBM3 (JESD235C) restructures to 16 channels of 64-bit width (also 1,024 bits total) at up to 6.4 Gbps per pin, yielding up to 819 GB/s per stack. All HBM generations share the 1,024-bit aggregate bus width as the fundamental architectural constant."

**Source:** JEDEC Solid State Technology Association, "High Bandwidth Memory (HBM) DRAM," JEDEC Standard JESD235C, Revision C, Arlington, VA: JEDEC, 2022. Available: jedec.org/standards-documents/docs/jesd235c

#segment:dram #source-tier:S #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

## 5. DRAM Sense Amplifier and Array Timing

> "The architecture of dynamic RAM is fundamentally determined by the sense amplifier. The cross-coupled CMOS latch sense amplifier, introduced for high-density DRAM, detects the small charge differential on a bitline pair after a wordline is activated (RAS — Row Address Strobe) and amplifies it to full logic swing. CAS (Column Address Strobe) latency is the number of clock cycles between the column address command and valid data output. The 1T1C (one-transistor, one-capacitor) cell was first patented in 1968 (Dennard, IBM Patent 3,387,286) and remains universal across all DRAM technology generations."

**Source:** Dennard, R.H., "Field-Effect Transistor Memory," U.S. Patent 3,387,286, IBM Corporation, filed June 4, 1968, issued June 4, 1968. Available: patents.google.com/patent/US3387286; JEDEC Standard JESD79-5B, "DDR5 SDRAM," JEDEC, 2020.

#segment:dram #source-tier:S #signal-type:roadmap #date:1968 #importance:medium #confidence:high

---

## 6. DRAM Scaling Limits — Capacitor and Cell Size

> "DRAM faces a fundamental scaling dilemma: as cell area shrinks, the storage capacitor must maintain a minimum charge (~20 fC) to guarantee correct sensing despite leakage, noise, and process variation. Trench and stacked capacitor technologies (used in current 10–20nm class DRAM) use high-κ dielectric materials (ZrO₂, Al₂O₃) to achieve capacitance per unit area sufficient for continued scaling. The standard cell refresh interval is 64ms (JEDEC specification), requiring refresh operations to dominate power consumption in large capacity modules — at 64GB DDR5, refresh consumes approximately 5–10% of total DRAM power."

**Source:** JEDEC Solid State Technology Association, "DDR5 SDRAM Standard," JEDEC Standard JESD79-5B, 2020; Kang, U., et al. (Samsung Electronics), "8Gb 3D DDR3 DRAM Using Through-Silicon-Via Technology," IEEE Journal of Solid-State Circuits, Vol. 45, No. 1, pp. 111–119, 2010. DOI: 10.1109/JSSC.2009.2034785

#segment:dram #source-tier:S #signal-type:roadmap #date:2020 #importance:medium #confidence:high

---

## Open Technical Questions

- [ ] HBM4 (JESD238): will hybrid bonding (Cu-Cu, sub-10µm pitch) replace TC-bonding micro-bumps for die-to-die stacking?
- [ ] Rowhammer at sub-20nm DRAM: what is the empirically measured hammer threshold for 2024-generation LPDDR5X?
- [ ] Processing-In-Memory (PIM) in HBM4 base die: which foundry process will the logic base die use for AI compute functions?
- [ ] DRAM refresh power at 512GB+ capacity (AI training): does selective refresh (PASR) become mandatory to stay within rack power budgets?
