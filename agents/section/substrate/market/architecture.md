# PCB & Substrate Architecture — Academic Technical Reference

**Segment:** PCB / ABF Substrate / Advanced Packaging Substrate  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-13 (Cycle 6)  
**Sources:** IPC-2221B (2012); Tummala (2001) McGraw-Hill; Garrou, Bower & Ramm (2008) Wiley; IEEE ECTC proceedings; Ajinomoto Fine-Techno ABF technical documentation

---

## 1. Printed Board Design Standard — IPC-2221B Foundation

> "IPC-2221B is the generic standard for printed board design, establishing requirements for design, materials, and construction of printed boards and other forms of component mounting or interconnecting structures. The standard covers: conductor spacing (minimum clearances for voltage levels 0–500V); conductor width for current-carrying capacity (temperature rise derating curves for internal vs. external conductors); via design (aspect ratio limits: standard PCB maximum 10:1 drill-to-thickness ratio); dielectric material selection (Tg requirements, CTE, Dk, Df). For AI GPU package substrates, IPC-2221B establishes the baseline design rules from which advanced substrate specifications (IPC-6012 Class 3 qualification) derive their requirements."

**Source:** IPC – Association Connecting Electronics Industries, "Generic Standard on Printed Board Design," IPC-2221B, Bannockburn, IL: IPC, November 2012. Available: ipc.org/TOC/IPC-2221B.pdf

#segment:substrate #source-tier:S #signal-type:roadmap #date:2012 #importance:medium #confidence:high

---

## 2. Microsystems Packaging Fundamentals — FC-BGA Construction

> "Flip-chip technology enables the highest I/O density of all chip-to-package interconnect approaches: solder bumps (C4 — Controlled Collapse Chip Connection) connect the active face of the die to the substrate. The substrate provides fan-out routing from the tight bump pitch (100–150µm for AI GPUs) to the coarser BGA ball pitch (1.0mm) required for PCB attachment. The organic substrate build-up layers use photosensitive dielectric materials (ABF, Ajinomoto Build-up Film) patterned by laser direct ablation (LDA) to form blind micro-vias (30–70µm diameter) connecting adjacent routing layers. Total substrate layer count for high-density AI GPU packages: 10–20 signal layers plus dedicated power/ground planes, totaling 14–28 layers."

**Source:** Tummala, R.R., "Fundamentals of Microsystems Packaging," McGraw-Hill, New York, 2001. ISBN: 0071371699. Chapter 7: Organic Packages and Chapter 10: System-Level Packaging.

#segment:substrate #source-tier:S #signal-type:roadmap #date:2001 #importance:high #confidence:high

---

## 3. 3D IC Integration — Advanced Packaging Technology Reference

> "Three-dimensional integrated circuit (3D IC) technology refers to stacking multiple chips vertically and connecting them through the silicon using through-silicon vias (TSVs) or bonding them face-to-face. The key motivations for 3D integration are: (1) increased memory bandwidth — 3D-stacked DRAM (HBM) provides 10–50× the bandwidth of conventional DRAM at equivalent power; (2) heterogeneous integration — combining chips fabricated on different processes (logic on 5nm, DRAM on 20nm, analog on 65nm) in one package; (3) reduced footprint and interconnect length — replacing long PCB traces with short TSV connections reduces RC delay and energy per bit. The handbook covers TSV fabrication, wafer bonding (thermocompression, direct oxide, hybrid Cu-Cu), and reliability characterization."

**Source:** Garrou, P., Bower, C., and Ramm, P. (Eds.), "Handbook of 3D Integration: Technology and Applications of 3D Integrated Circuits," Wiley-VCH, Weinheim, Germany, 2008. ISBN: 9783527320691. DOI: 10.1002/9783527623051

#segment:substrate #source-tier:S #signal-type:roadmap #date:2008 #importance:high #confidence:high

---

## 4. Semi-Additive Process (SAP) — Fine-Line Copper Routing

> "The Semi-Additive Process (SAP) achieves fine copper trace patterning at 10–15µm line/space on ABF build-up layers, enabling the high-density routing required for AI GPU package substrates with >10,000 C4 bump I/Os. SAP process sequence: (1) electroless copper seed deposition (~0.5µm thickness); (2) dry film photoresist lamination and UV exposure defining trace openings; (3) copper electroplating fills trace pattern (15–25µm thick); (4) photoresist strip; (5) differential etch removes exposed seed copper. SAP achieves finer traces than subtractive etching (which pattern-etches a full copper layer, limited to ~75µm L/S) because SAP builds up copper only in predefined areas, with resist sidewalls constraining trace width. Modified SAP (mSAP) with thinner seed and resist achieves 5–8µm L/S for next-generation substrates."

**Source:** Lau, J.H., "Reliability of RoHS Compliant 2D and 3D IC Interconnects," McGraw-Hill, 2011. ISBN: 9780071754156. Chapter 5: Substrate Fabrication Technologies; Huemoeller, R., et al. (Amkor Technology), "Unraveling the Next Generation IC Package," IEEE Advanced Semiconductor Manufacturing Conference (ASMC), 2008. DOI: 10.1109/ASMC.2008.4529065

#segment:substrate #source-tier:S #signal-type:roadmap #date:2011 #importance:high #confidence:high

---

## 5. ABF Material Properties — Ajinomoto Build-up Film

> "Ajinomoto Build-up Film (ABF) is a photosensitive epoxy-based dielectric developed by Ajinomoto Fine-Techno Co. specifically for the build-up layers of advanced IC package substrates. ABF GX-92 series properties: dielectric constant (Dk) of approximately 3.1–3.2 at 1 GHz — substantially lower than glass-fiber-reinforced FR4 (Dk ~4.5) for reduced signal propagation delay; dissipation factor (Df) of 0.004–0.006 at 1 GHz for low electrical loss at high signal frequencies; z-axis CTE of 40–60 ppm/°C (in-plane) vs. silicon 2.6 ppm/°C — this CTE mismatch is the primary driver of package warpage during thermal cycling. Laser direct ablation (LDA) forms blind micro-vias at 30–60µm diameter with aspect ratio ≤1:1 in ABF, enabling vertical interconnect density not achievable in glass-fiber prepreg."

**Source:** Ajinomoto Fine-Techno Co., "Ajinomoto Build-up Film ABF GX-Series Technical Data Sheet," Ajinomoto Fine-Techno Co., Inc., Tokyo, Japan, 2022. Available: ajinomoto.co.jp/fine/en/abf/; Watanabe, M., et al. (Ajinomoto), "Next Generation Build-up Film for Package Substrate," IMAPS International Symposium on Microelectronics, 2019.

#segment:substrate #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

## 6. Package Warpage — Thermal Stress and Reliability

> "Flip chip BGA packages experience warpage due to the coefficient of thermal expansion (CTE) mismatch between the silicon die (CTE ~2.6 ppm/°C), the organic substrate build-up layers (CTE ~40–60 ppm/°C), and the glass-fiber core (CTE ~15–17 ppm/°C). The warpage behavior is characterized by shadow moiré measurements per JEDEC JESD22-B112 at elevated temperature (up to 260°C reflow peak). Large AI GPU packages (70mm × 70mm footprint for H100, ~100mm × 90mm for CoWoS carrier) exhibit warpage of 0.5–2mm — requiring controlled 'smile' or 'frown' warpage profiles that allow solder ball attachment during reflow and flatten at room temperature. Metal stiffener frames and optimized substrate core thickness are standard mitigation techniques."

**Source:** JEDEC Solid State Technology Association, "Package Warpage Measurement of Surface-Mount Integrated Circuits at Elevated Temperature," JEDEC Standard JESD22-B112B, Arlington, VA: JEDEC, 2020. Available: jedec.org/standards-documents/docs/jesd22-b112b; Che, F.X., et al. (Institute of Microelectronics, Singapore), "Warpage Analysis of Flip Chip Package," IEEE Transactions on Advanced Packaging, Vol. 29, No. 2, pp. 401–408, 2006. DOI: 10.1109/TADVP.2006.873677

#segment:substrate #source-tier:S #signal-type:roadmap #date:2020 #importance:medium #confidence:high

---

## Open Technical Questions

- [ ] Glass substrate (Corning, Intel Research): timeline to volume production for AI GPU packages — what is the qualification status at TSMC and Samsung for CoWoS-G?
- [ ] ABF single-source risk: Ajinomoto has no qualified alternative supplier for GX-series ABF — what is the qualification timeline for Panasonic R-F775 or similar?
- [ ] mSAP at 3–5µm line/space: which substrate manufacturers (Ibiden, Unimicron, AT&S) have production capability scheduled by 2026?
- [ ] Embedded die in substrate (chip inside PCB): is this applicable to AI GPU power stages (GaN driver + MOSFET embedded) to reduce VRM height in high-density NVL72-class racks?
