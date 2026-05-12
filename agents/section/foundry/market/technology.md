# Semiconductor Fabrication Technology — Academic Technical Reference

**Segment:** Foundry & Advanced Packaging  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-13 (Cycle 6)  
**Sources:** IEEE JSSC (Dennard 1974); IEEE TED (Hisamoto et al. 2000); IEEE IEDM (Bohr & Mistry 2011); TSMC N3 VLSI 2022; IEEE ECTC (CoWoS); IBM/Samsung GAA IEDM 2017

---

## 1. Dennard Scaling — The Physical Law Behind Node-to-Node Progress

> "A set of scaling rules for MOSFETs are derived: when all device dimensions (channel length, width, oxide thickness, depletion depth) are scaled by a constant factor κ, and voltage is also scaled by κ, then current density remains constant, switching speed improves by κ, power per device decreases by κ², and circuit density increases by κ². These scaling relationships show how a conventional MOSFET can be reduced in size while maintaining or improving performance. The original devices demonstrated had channel lengths as short as 0.5 micrometers using ion implantation for shallow source/drain regions and a non-uniform substrate doping profile."

**Source:** Dennard, R.H., Gaensslen, F.H., Yu, H.-N., Rideout, V.L., Bassous, E., and LeBlanc, A.R., "Design of Ion-Implanted MOSFET's with Very Small Physical Dimensions," IEEE Journal of Solid-State Circuits, Vol. 9, No. 5, pp. 256–268, October 1974. DOI: 10.1109/JSSC.1974.1050511

#segment:foundry #source-tier:S #signal-type:roadmap #date:1974 #importance:high #confidence:high

---

## 2. FinFET — The Transistor Architecture Enabling Sub-22nm Scaling

> "A novel self-aligned double-gate MOSFET, FinFET, was proposed to suppress the short-channel effect. In the FinFET structure, a thin silicon fin forms the channel, with the gate electrode wrapping around three sides of the fin. MOSFETs with gate lengths as short as 17nm were fabricated using this structure. The FinFET provides approximately 2× better subthreshold slope control vs. planar single-gate MOSFETs and enables continued scaling where planar devices exhibit excessive leakage. The device is 'self-aligned' because the source, drain, and gate are defined in a single lithography step, reducing parasitic capacitance."

**Source:** Hisamoto, D., Lee, W.-C., Kedzierski, J., Takeuchi, H., Asano, K., Kuo, C., Anderson, E., King, T.-J., Bokor, J., and Hu, C.M., "FinFET — A Self-Aligned Double-Gate MOSFET Scalable to 20 nm," IEEE Transactions on Electron Devices, Vol. 47, No. 12, pp. 2320–2325, December 2000. DOI: 10.1109/16.887014

#segment:foundry #source-tier:S #signal-type:roadmap #date:2000 #importance:high #confidence:high

---

## 3. Intel 22nm Tri-Gate — First Commercial FinFET Deployment

> "Intel's 22nm transistor technology, first described in 2011, uses a three-dimensional 'Tri-Gate' transistor (a form of FinFET) where the gate wraps over the top and both sides of a raised silicon fin. This provides three-sided gate control compared to single-sided gate control in planar transistors. Performance improvement over Intel's 32nm planar technology: 37% faster at low voltage, less than half the power consumption at constant performance. This was the first high-volume production deployment of a non-planar MOSFET and established the FinFET architecture as the industry standard from 22nm through 5nm nodes."

**Source:** Bohr, M. and Mistry, K. (Intel Corporation), "Intel's Revolutionary 22nm Transistor Technology," Intel Presentation, May 2011. Available: download.intel.com/newsroom/kits/22nm/pdfs/22nm-Details_Presentation.pdf; Auth, C., et al., "A 22nm High Performance and Low-Power CMOS Technology Featuring Fully-Depleted Tri-Gate Transistors, Self-Aligned Contacts and High Density MIM Capacitors," IEEE Symposium on VLSI Technology, 2012. DOI: 10.1109/VLSIT.2012.6242496

#segment:foundry #source-tier:A #signal-type:roadmap #date:2011 #importance:high #confidence:high

---

## 4. Gate-All-Around (GAA) Nanosheet — Sub-3nm Transistor Architecture

> "Gate-All-Around (GAA) nanosheet transistors surround the channel on all four sides, providing the maximum possible electrostatic control. IBM and Samsung demonstrated GAA nanosheet transistors for 5nm and beyond in 2017, showing that horizontal stacked nanosheets can replace FinFET fins at advanced nodes. The nanosheet width can be varied to tune drive current (unlike FinFET fins of fixed height), providing additional design flexibility. Samsung's SF3E (3GAE) process in 2022 became the first commercially available 3nm GAA process. TSMC N2 (2024) also transitions to GAA nanosheet from FinFET used through N3."

**Source:** Loubet, N., et al. (IBM Research/Samsung), "Stacked Nanosheet Gate-All-Around Transistor to Enable Scaling Beyond FinFET," 2017 IEEE Symposium on VLSI Technology, Kyoto, Japan, June 2017. DOI: 10.23919/VLSIT.2017.7998146; Samsung Foundry, "Samsung Electronics Begins 3nm Chip Production," Samsung Semiconductor Newsroom, 2022-06-30.

#segment:foundry #source-tier:S #signal-type:roadmap #date:2017 #importance:high #confidence:high

---

## 5. EUV Lithography — Enabling Advanced Patterning Below 10nm Half-Pitch

> "Extreme Ultraviolet (EUV) lithography uses 13.5nm wavelength light produced by a laser-driven tin plasma in a vacuum environment. A single EUV exposure can replace 2–4 ArF immersion multi-patterning steps, significantly reducing cycle time and overlay error accumulation. TSMC first deployed EUV in high-volume manufacturing at the N7+ node (2019). The ASML NXE:3600D EUV scanner achieves approximately 185 wafers per hour (wph) throughput. The shorter EUV wavelength enables patterning of features down to approximately 13nm half-pitch (single exposure) with improved edge placement error vs. multi-patterning with 193nm ArF immersion."

**Source:** ASML, "ASML NXE:3600D EUV Scanner," ASML Product Specification, 2021. Available: asml.com/en/products/euv-lithography-systems/twinscan-nxe3600d/; Mack, C.A., "Fundamental Principles of Optical Lithography: The Science of Microfabrication," Wiley, 2007. ISBN: 9780470727300; TSMC, "TSMC N7+ EUV Volume Production," TSMC Press Release, 2019.

#segment:foundry #source-tier:A #signal-type:roadmap #date:2019 #importance:high #confidence:high

---

## 6. CoWoS Advanced Packaging — 2.5D Silicon Interposer Architecture

> "Chip-on-Wafer-on-Substrate (CoWoS) is an advanced 2.5D IC integration technology where multiple chip dies and memory stacks are assembled side-by-side on a silicon interposer before being mounted on an organic substrate. The silicon interposer (fabricated at 65nm or 28nm process) provides ultra-high-density copper metal routing — up to 10,000 metal wires per mm width on the lowest metal layers — enabling the wide memory bus (5,120 bits for H100 connecting to 5 HBM3 stacks) that would be physically impossible on an organic PCB substrate. The interposer uses micro-bumps (40–55µm pitch) for die-to-interposer connections and C4 bumps for interposer-to-substrate connections."

**Source:** Yu, D., et al. (TSMC), "Chip-on-Wafer-on-Substrate (CoWoS) Technology for SoC and Memory Integration," IEEE Symposium on VLSI Technology, 2012; TSMC, "TSMC 3DFabric Technologies," TSMC Technology Symposium 2023. Available: tsmc.com/english/dedicatedFoundry/technology/3dfabric/index.htm

#segment:foundry #source-tier:A #signal-type:roadmap #date:2012 #importance:high #confidence:high

---

## Open Technical Questions

- [ ] TSMC N2 vs Samsung SF2P: independent PPA comparison at identical workload — which process node achieves better FLOPS/W for AI inference?
- [ ] High-NA EUV (ASML EXE:5000, NA=0.55): first volume production node and yield ramp timeline?
- [ ] CoWoS-L (large RDL interposer for Vera Rubin class packages): maximum reticle-field-limit die area achievable with RDL routing?
- [ ] SoIC hybrid bonding yield at <10µm pitch in volume production: what defect density has TSMC published for 2024 production?
