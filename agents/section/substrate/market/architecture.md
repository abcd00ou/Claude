# PCB & Substrate Architecture — Academic Technical Reference

**Segment:** PCB / ABF Substrate / Advanced Packaging Substrate  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-12 (Cycle 5)  
**Sources:** IEEE ECTC; IPC standards (IPC-2221, IPC-6012); Ajinomoto Build-up Film (ABF) technical documentation; Ibiden, Unimicron, AT&S technical papers; SEMI standards

---

## 1. Flip-Chip Ball Grid Array (FC-BGA) Substrate Architecture

### FC-BGA Construction

> "An FC-BGA (Flip-Chip Ball Grid Array) substrate is a laminated organic package substrate that mechanically supports the GPU or ASIC die and provides electrical routing from the die's C4 (Controlled Collapse Chip Connection) bumps to the PCB's BGA solder balls. Construction layers from top to bottom: (1) build-up layers (signal routing, 2–8 layers) using ABF dielectric with embedded copper traces; (2) core layer (mechanical rigidity, typically glass-fiber reinforced epoxy or glass cloth); (3) build-up layers (mirrored structure below core). Total layer count for AI GPU substrates: 10–20 signal routing layers + 4–8 power/ground planes = 14–28 total layers. Die-side pitch (C4 bumps): 100–150µm. PCB-side pitch (BGA balls): 1.0mm typical for large packages."

**Source:** "Advanced Flip Chip Package Substrate Technology," IEEE ECTC, 2018; IPC-2221B Design Standard for Printed Board Design, IPC, 2012

#segment:substrate #source-tier:S #signal-type:roadmap #date:2018 #importance:high #confidence:high

---

### ABF (Ajinomoto Build-up Film) Chemistry

> "ABF (Ajinomoto Build-up Film) is a photosensitive epoxy-based dielectric film developed by Ajinomoto Co. (now Ajinomoto Fine-Techno) in 1996, designed for the build-up layers of advanced IC package substrates. Key ABF properties: (1) dielectric constant (Dk) = 2.9–3.1 at 1 GHz — lower than glass fiber FR4 (Dk ~4.5) for reduced signal delay; (2) dissipation factor (Df) = 0.005 at 1 GHz — low electrical loss for high-frequency signaling; (3) coefficient of thermal expansion (CTE) = 40–60 ppm/°C (x-y direction) vs silicon CTE = 2.6 ppm/°C — CTE mismatch is the primary driver of solder joint reliability failures; (4) via formation: laser direct ablation (LDA) creates blind micro-vias at 30–70µm diameter to connect adjacent build-up layers. ABF dominates AI GPU substrate dielectric because it achieves finer via pitch (30µm vs 75µm for glass-fiber prepreg) enabling higher routing density."

**Source:** "Ajinomoto Build-up Film ABF GX13 Technical Datasheet," Ajinomoto Fine-Techno, 2022; "Advances in Build-Up Film Technology for High-Speed Substrate," IEEE ECTC, 2020

#segment:substrate #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

## 2. Substrate Signal Routing Technology

### Semi-Additive Process (SAP) — Fine-Line Copper Traces

> "The Semi-Additive Process (SAP) is the copper patterning method used in advanced ABF build-up layers to achieve fine-line traces at 10–15µm line/space (L/S). Process flow: (1) electroless copper seed deposition on the ABF layer (~0.5µm); (2) dry film photoresist lamination and UV exposure to define trace pattern; (3) copper electroplating fills the open trenches (forming traces 15–25µm thick); (4) photoresist strip; (5) differential etch removes seed copper between traces. SAP achieves finer traces than subtractive etching (which can only reliably pattern to ~75µm L/S in mass production) because SAP builds up copper in predefined areas rather than etching away a full copper layer. For AI GPU substrates, 10–15µm L/S SAP enables the high pin-count I/O routing required to fan out the >10,000 C4 bumps on an H100 GPU die."

**Source:** "Semi-Additive Process for Fine-Line Substrate Fabrication," IEEE ECTC, 2017; "Advanced Package Substrate Routing Technology," AT&S Technical Paper, 2022

#segment:substrate #source-tier:S #signal-type:roadmap #date:2017 #importance:high #confidence:high

---

### mSAP (Modified Semi-Additive Process) — Next Generation

> "mSAP (modified Semi-Additive Process) achieves 5–8µm line/space by further thinning the electroless copper seed layer (to <0.3µm) and using ultra-thin dry film photoresist (<15µm thick). The thinner photoresist enables sharper sidewall definition during plating. mSAP at 5µm L/S is required for the CoWoS RDL (Redistribution Layer) in CoWoS-R packages and for very high-density FC-BGA substrates (>1,000 signal layers × mm²). Ibiden and Unimicron have demonstrated mSAP at <10µm L/S for AI GPU substrates as of 2024. Industry roadmap: mSAP target for 2026 is 3–5µm L/S, approaching the density of TSMC silicon interposer at ~2µm."

**Source:** "Modified Semi-Additive Process for Next-Generation Package Substrates," IEEE ECTC, 2022; Ibiden Technical Presentation, iMAPS International, 2023

#segment:substrate #source-tier:A #signal-type:roadmap #date:2022 #importance:high #confidence:high

---

## 3. Power Delivery in Substrate

### Power Planes and Decoupling Capacitor Integration

> "AI GPU substrates carry current from BGA balls (PCB side) to the GPU die's VCC power pads at up to 1,000A total. Power delivery in the substrate uses: (1) solid copper power planes (2–4 oz copper, 70–140µm thick) in dedicated build-up layers; (2) arrays of blind vias and through-hole vias to carry current between layers with minimum resistance; (3) embedded capacitors in the substrate dielectric to provide on-substrate decoupling (20–100 nF per capacitor cell). The substrate DC resistance from BGA ball to die bump must be <0.1 mΩ for 1,000A delivery at <100mV drop, requiring via count optimization and copper plane width calculation. NVIDIA GB200 substrate design requires routing >1,000A at 48V → 0.9V with sub-mΩ path resistance per power domain."

**Source:** "Power Delivery Network Design for High-Current Package Substrates," IEEE ECTC, 2021; "Embedded Capacitor Technology in Package Substrates," IMAPS, 2023

#segment:substrate #source-tier:A #signal-type:roadmap #date:2021 #importance:high #confidence:high

---

## 4. Substrate-Level Reliability — CTE Mismatch and Warpage

### Warpage and Thermal Stress

> "Substrate warpage is the deformation of the package substrate due to CTE mismatch between materials during thermal cycling. For a GPU package: silicon die CTE ~2.6 ppm/°C; ABF build-up layers CTE ~40 ppm/°C (x-y); glass-fiber core CTE ~15 ppm/°C. At reflow temperatures (260°C peak), the ABF layers expand ~60× more than silicon, inducing bow. Package warpage is quantified as the maximum out-of-plane displacement: JEDEC JESD22-B112 test method. For large AI GPU substrates (70×70mm, the H100 package footprint), warpage of >1mm is common — requiring controlled warpage 'smile' or 'frown' profile that allows solder ball attachment during reflow and then returns to flat at room temperature. Stiffener frames are added to large substrates to limit warpage."

**Source:** "Package Warpage Assessment for Large Die Packages," IEEE ECTC, 2019; JEDEC JESD22-B112B: Package Warpage Measurement of Surface-Mount Integrated Circuits at Elevated Temperature, JEDEC, 2020

#segment:substrate #source-tier:S #signal-type:roadmap #date:2019 #importance:medium #confidence:high

---

## 5. Substrate Role in CoWoS Advanced Packaging

### CoWoS Organic Substrate (Carrier Substrate)

> "In TSMC CoWoS packages, the GPU die and HBM stacks are assembled on a silicon interposer (CoWoS-S) or RDL carrier (CoWoS-R), and the entire interposer+die assembly is then mounted on an organic substrate (the ABF FC-BGA carrier substrate). This organic substrate provides: (1) mechanical support for the interposer-level assembly; (2) BGA ball attachment to the PCB; (3) power delivery from 12V PCB planes to the VRM and then to the package; (4) signal routing from the GPU's PCIe/NVLink SerDes to the PCB edge connectors. The organic carrier substrate for CoWoS-S (H100) has approximate dimensions: 100×90mm — one of the largest organic substrates in production, requiring special panel-level handling. Only Ibiden, Unimicron, and Shinko Electric have validated capability for these large CoWoS organic carrier substrates."

**Source:** TSMC Technology Symposium 2023: CoWoS-S package architecture; "Large-Format FC-BGA Substrate for CoWoS Applications," IEEE ECTC, 2023; Ibiden Investor Presentation, 2024

#segment:substrate #source-tier:A #signal-type:roadmap #date:2023 #importance:high #confidence:high

---

## 6. Substrate Supply Chain — Panel Size and Yield

### Panel Size Economics

> "Package substrates are fabricated on large panels (analogous to wafers in semiconductor manufacturing). Panel sizes used by leading substrate manufacturers: (1) Standard panel: 510×410mm (Panasonic, Ibiden legacy); (2) Large panel: 510×515mm (Ibiden next-generation); (3) 600×500mm (Unimicron development). Larger panels increase yield per cycle by processing more substrates per exposure step, reducing cost per substrate. For a 100×90mm CoWoS carrier substrate on a 510×410mm panel: usable area fraction ~70% after edge exclusion → approximately 15 substrates per panel per layer pair exposure. With 28 layers × 4 photolithography passes per layer = 112 panel passes — substrate fabrication cycle time is 14–21 days."

**Source:** "Advanced Package Substrate Manufacturing Economics," SEMI FlexTech, 2022; AT&S Annual Report 2023 (substrate manufacturing capacity); Ibiden Investor Day 2024

#segment:substrate #source-tier:A #signal-type:roadmap #date:2022 #importance:medium #confidence:high

---

## Open Technical Questions

- [ ] Glass substrate (Corning, Intel Research): when does it outperform ABF for AI GPU packages — what is the timeline to volume production?
- [ ] ABF supply single-source risk: Ajinomoto's ABF film has no qualified alternative — what is the qualification timeline for alternative suppliers?
- [ ] mSAP at 3µm L/S: which substrate makers (Ibiden, Unimicron, AT&S) will achieve this in volume by 2026?
- [ ] Embedded die technology (chip inside substrate): is this applicable to AI GPU power stages to reduce VRM height in high-density racks?
