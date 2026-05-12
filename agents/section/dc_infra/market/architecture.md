# Data Center Infrastructure Architecture — Academic Technical Reference

**Segment:** Data Center Infrastructure (Power, Cooling, Facilities)  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-12 (Cycle 5)  
**Sources:** ASHRAE TC 9.9 standards; IEEE Power & Energy Society; ASHRAE 90.4; ASME papers on two-phase cooling; Green Grid PUE standard; academic papers on liquid cooling thermodynamics

---

## 1. Data Center Power Architecture

### Power Distribution Hierarchy

> "Modern AI data center power delivery follows a hierarchical distribution chain: (1) Utility substation: medium-voltage (12–35 kV) feeds the campus; (2) Main Transformer: steps down to 480V or 277V AC (three-phase); (3) UPS (Uninterruptible Power Supply): provides battery backup for the 480V distribution bus, protects against grid outages; (4) Power Distribution Unit (PDU): distributes 480V to rack-level circuits at 30A–60A per branch; (5) Rack Power Strip (rPDU): provides per-outlet monitoring and 208V or 48V to servers; (6) Server PSU: converts AC to 48VDC for server board power rails. Total chain efficiency (utility transformer to server): ~88–92%. Power Usage Effectiveness (PUE) = Total Facility Power / IT Equipment Power; industry target for hyperscaler AI data centers is PUE < 1.2 (vs global average PUE ~1.6)."

**Source:** "Data Center Power Distribution Best Practices," IEEE Std 3001.4, 2017; Green Grid White Paper #49: PUE, 2016; ASHRAE Technical Committee TC 9.9, Mission Critical Facilities, 2021

#segment:dc_infra #source-tier:S #signal-type:roadmap #date:2017 #importance:high #confidence:high

---

### Transformer Technology — AI Data Center Bottleneck

> "A liquid-immersed power transformer (rated 1 MVA – 100 MVA) steps medium-voltage utility power down to the 480V AC bus used inside data centers. Transformer construction: a laminated silicon steel core with copper (or aluminum) primary and secondary windings, immersed in transformer oil (mineral oil or ester-based fluid) for cooling and insulation. Core material: grain-oriented electrical steel (GOES), 0.27mm laminations; GOES supply is dominated by Nippon Steel, JFE Steel (Japan), POSCO (Korea), and ThyssenKrupp (Germany). U.S. large power transformer (LPT) lead times reached 128 weeks (2.5 years) in 2025 due to AI data center construction demand outpacing domestic transformer manufacturing capacity — only two major domestic LPT manufacturers (ABB/Hitachi Energy, SPX Transformer Solutions) serve the U.S. market with limited capacity."

**Source:** "Large Power Transformers and the U.S. Electric Grid," U.S. Department of Energy, 2014; "Power Transformer Supply Chain Analysis," Lawrence Berkeley National Laboratory, 2024; Vertiv Q1 2026 Earnings Call, Vertiv, 2026-05-01

#segment:dc_infra #source-tier:A #signal-type:roadmap #date:2024 #importance:high #confidence:high

---

## 2. Data Center Cooling Architecture

### Air Cooling — Fundamental Thermodynamics

> "Traditional data center cooling uses forced convection air cooling. Thermodynamic basis: Q = ṁ × Cp × ΔT, where Q is heat removed (W), ṁ is mass flow rate of air (kg/s), Cp is specific heat of air (1,005 J/kg·K), and ΔT is air temperature rise across the hot aisle (K). For a 20kW rack cooled with 20°C inlet air rising to 40°C outlet (ΔT = 20°C): ṁ = Q / (Cp × ΔT) = 20,000 / (1,005 × 20) = 0.995 kg/s ≈ ~0.83 m³/s (830 L/s). At 400 W/m² rack floor density, a 10,000 m² data center hall requires approximately 8.3 m³/s per rack × 250 racks = ~2,080 m³/s total airflow — physically impractical for AI GPU racks exceeding 50–100 kW per rack, driving the transition to liquid cooling."

**Source:** "Fundamentals of Heat and Mass Transfer," Incropera et al., 7th Edition, Wiley, 2011; ASHRAE TC 9.9: "Thermal Guidelines for Data Processing Environments," 5th Edition, 2021

#segment:dc_infra #source-tier:S #signal-type:roadmap #date:2021 #importance:high #confidence:high

---

### Single-Phase Liquid Cooling (Direct Liquid Cooling)

> "Direct Liquid Cooling (DLC) replaces air cooling for GPUs and CPUs by attaching a cold plate (a metal heat exchanger) directly to the chip package. Single-phase DLC uses liquid water (or water-glycol mixture) that remains in the liquid phase throughout the loop. Heat exchange: Q = ṁ × Cp_water × ΔT, where Cp_water = 4,186 J/kg·K — 4.2× higher specific heat than air. For a 700W H100 GPU cold plate with 20°C inlet, 40°C outlet: ṁ = 700 / (4,186 × 20) = 0.00836 kg/s ≈ 0.5 L/min. Single-phase DLC components: cold plate (copper or aluminum), coolant distribution unit (CDU), supply/return manifold, quick-disconnect fittings. CDU: heat exchanger between the facility chilled water loop (7–15°C facility water) and the server-side cooling water loop. Cooling capacity per CDU: 200 kW–2 MW for rack-scale or pod-scale deployments."

**Source:** "Direct Liquid Cooling for Microprocessors," IEEE Transactions on Components, Packaging and Manufacturing Technology, 2021; "Rack-Level Liquid Cooling Design," Green Grid White Paper #65, 2019

#segment:dc_infra #source-tier:S #signal-type:roadmap #date:2021 #importance:high #confidence:high

---

### Two-Phase Immersion Cooling

> "Two-phase immersion cooling submerges server electronics in a dielectric fluid (e.g., 3M Novec, Engineered Fluids EC-100) at atmospheric pressure. The fluid boils at ~50–55°C directly on hot chip surfaces, absorbing latent heat of vaporization: Q = ṁ × L_v, where L_v (latent heat of vaporization) for 3M Novec 649 = ~88 kJ/kg — compared to 2,257 kJ/kg for water (water vaporizes at 100°C, not useful for atmospheric pressure electronics). Boiling heat transfer coefficient for immersion fluids: 2,000–10,000 W/m²·K (vs air natural convection ~5–25 W/m²·K). The vapor condenses on a submerged coil cooled by facility water, returning condensate to the bath. Two-phase immersion advantages: (1) no pumping energy for coolant circulation (passive thermosiphon); (2) uniform temperature across all components; (3) no fan energy. Disadvantage: high fluid cost (~$50/L for Novec vs ~$0.01/L for water) and 3M's 2025 production exit for PFAS-based fluids."

**Source:** "Two-Phase Immersion Cooling for Electronics," IEEE Transactions on Components and Packaging Technologies, 2019; "3M Novec Fluids for Electronics Cooling," 3M Technical Data Sheet, 2022; "PFAS Phase-Out Impact on Data Center Cooling," IEEE SEMI-THERM, 2023

#segment:dc_infra #source-tier:S #signal-type:roadmap #date:2019 #importance:high #confidence:high

---

## 3. Rack Power Density Evolution

### Power Density Trend — Air Cooling Limit

> "Rack power density (W per rack) has increased with each generation of AI accelerator: (1) DGX A100 (2020): 10.2 kW per server, ~40 kW per 4-server rack; (2) DGX H100 (2022): 10.2 kW per server, ~50 kW per 4-server rack; (3) GB200 NVL72 (2024): 120 kW per rack unit (72 GPUs in one 19" rack unit system); (4) GB200 SuperPOD: 14 NVL72 racks = 14 × 120 kW = 1.68 MW per SuperPOD. Air cooling (ASHRAE Class A4) is certified to 45 kW per rack maximum. GB200 NVL72 at 120 kW requires liquid cooling — specifically rear-door liquid cooling or direct liquid cooling — to operate. The industry transition from air to liquid cooling is driven primarily by GB200 NVL72 deployment, which began in volume at hyperscalers in H1 2025."

**Source:** ASHRAE TC 9.9: "IT Equipment Power Trends," 2023; NVIDIA GB200 NVL72 System Specifications, NVIDIA, 2024; "Data Center Thermal Management for High-Performance Computing," IEEE SEMI-THERM Keynote, 2024

#segment:dc_infra #source-tier:A #signal-type:roadmap #date:2024 #importance:high #confidence:high

---

### Coolant Distribution Unit (CDU) — Architecture

> "A Coolant Distribution Unit (CDU) is the rack-level or row-level heat exchanger that transfers heat from the server-side liquid loop to the facility chilled water loop. CDU components: (1) primary heat exchanger (plate-and-frame design for high heat transfer area); (2) pump(s) for the server-side loop; (3) sensors (flow, pressure, temperature at supply/return); (4) electronic control valve for supply temperature regulation; (5) manifold connections (supply/return per rack). CDU sizing for GB200 NVL72: 120 kW per rack minimum; deployment practice is 20–30% over-sizing (150 kW CDU per rack). Row-level CDU handles up to 10 racks (1.2 MW capacity). Facility water inlet temperature to CDU: 7–18°C for cooling tower-based facilities; 18–25°C for economizer-based facilities (free cooling in cold climates). Higher facility water temperature enables economizer hours but increases pumping flow rate per kW of heat removed."

**Source:** "CDU Sizing and Selection for High-Density AI Server Deployments," ASHRAE TC 9.9, 2024; Vertiv Liebert CDU Product Brief, 2024; "High-Density Liquid Cooling Infrastructure Design," IEEE ITHERM, 2023

#segment:dc_infra #source-tier:A #signal-type:roadmap #date:2024 #importance:high #confidence:high

---

## 4. Mechanical and Electrical Integration — Rack Design

### Open Rack V3 Standard (OCP)

> "Open Rack V3 (ORV3) is the Open Compute Project data center rack standard designed for 48V direct power delivery to servers. ORV3 specifications: (1) rack height: 48U (standard) or 21U (half-rack); (2) power: 48VDC bus bar at up to 200A (9.6 kW) per Power Shelf zone; (3) cooling: rear-door CDU compatible; (4) power shelf: 6 × 1,000W PSU modules per shelf (6 kW per shelf), with multiple shelves per rack; (5) compute trays: horizontal slide-in sleds. NVIDIA GB200 NVL72 is not ORV3 form factor — it uses NVIDIA's proprietary NVL72 rack form factor at 120 kW, requiring a dedicated rack design. Hyperscalers (Meta, Microsoft) use ORV3 for smaller GPU-per-server configurations (8-GPU HGX servers)."

**Source:** "Open Rack V3 Specification v1.0," Open Compute Project, 2021; "48V Power Architecture in Open Compute Racks," OCP Summit Presentation, 2022

#segment:dc_infra #source-tier:S #signal-type:roadmap #date:2021 #importance:medium #confidence:high

---

## Open Technical Questions

- [ ] Two-phase direct-on-chip boiling for GPU chiplets: has any hyperscaler deployed vapor chamber + two-phase at wafer-scale?
- [ ] PFAS-free immersion fluids: which alternatives (synthetic hydrocarbon, low-GWP HFOs) are qualified for server electronics?
- [ ] Rear-door heat exchanger (RDHX) vs direct liquid cold plate for 120 kW racks: which achieves lower PUE in practice?
- [ ] Modular data center (containerized) for AI: what is the maximum rack density achievable in a 40-foot containerized deployment?
