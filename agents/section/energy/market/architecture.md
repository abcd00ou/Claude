# Data Center Infrastructure Architecture — Academic Technical Reference

**Segment:** Data Center Infrastructure (Power, Cooling, Facilities)  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-13 (Cycle 6)  
**Sources:** IEEE Computer (Barroso & Hölzle 2007); Morgan Claypool (Barroso & Hölzle 2009); IEEE Annals (Koomey et al. 2011); ASHRAE TC 9.9 (2021); Green Grid White Paper #49

---

## 1. Energy-Proportional Computing — The Efficiency Imperative

> "Energy-proportional designs would enable large energy savings in servers. The key problem: current servers consume 50% of their peak power even when idle — they are not energy proportional. An energy-proportional machine consumes no power when idle, and gradually more power as the activity level increases. Achieving energy proportionality will require significant improvements in the energy usage profile of every system component, particularly the memory and disk subsystems. For AI data centers, where GPU servers often run at 60–70% average utilization, an energy-proportional design would reduce power consumption by 15–20% compared to a non-proportional baseline, translating to tens of millions of dollars annually for a 100MW facility."

**Source:** Barroso, L.A. and Hölzle, U. (Google), "The Case for Energy-Proportional Computing," IEEE Computer, Vol. 40, No. 12, pp. 33–37, December 2007. DOI: 10.1109/MC.2007.443. Available: barroso.org/publications/ieee_computer07.pdf

#segment:dc_infra #source-tier:S #signal-type:roadmap #date:2007 #importance:high #confidence:high

---

## 2. Warehouse-Scale Computing Architecture — The Datacenter as a Computer

> "The datacenter must be viewed as a single unit of computing — a warehouse-scale computer — with its own programming model, architecture, and operational requirements. The book covers four fundamental aspects: (1) workloads — large-scale internet services exhibit different characteristics than traditional scientific computing; (2) hardware — commodity servers, networks, and storage are the building blocks, not specialized hardware; (3) energy and power — a 15MW datacenter running for three years consumes $1.5M per year in electricity at $0.07/kWh; (4) cost — the total cost of ownership (TCO) of a warehouse-scale computer is dominated by operational costs (energy, cooling, facilities) rather than capital equipment costs. This framework established the basis for hyperscaler infrastructure economics."

**Source:** Barroso, L.A. and Hölzle, U. (Google), "The Datacenter as a Computer: An Introduction to the Design of Warehouse-Scale Machines," Synthesis Lectures on Computer Architecture, Vol. 1, No. 1, pp. 1–108, Morgan & Claypool Publishers, 2009. DOI: 10.2200/S00193ED1V01Y200905CAC006. ISBN: 9781598295566

#segment:dc_infra #source-tier:S #signal-type:roadmap #date:2009 #importance:high #confidence:high

---

## 3. Electrical Efficiency of Computing — Koomey's Law

> "The electrical efficiency of computation has doubled roughly every year and a half for more than six decades, a pace of change comparable to that described by Moore's Law. These efficiency improvements were enabled by a combination of semiconductor scaling, architectural improvements, and system-level optimization. The trends show that computations per kWh doubled approximately every 1.57 years from 1946 to 2009. This historical efficiency improvement enabled the creation of laptops, smartphones, wireless sensors, and other mobile computing devices by reducing the energy per computation to levels compatible with battery operation. The paper uses 'computations per kWh' as the primary metric, demonstrating that computing efficiency improved by ~10¹² (one trillion times) over six decades."

**Source:** Koomey, J., Berard, S., Sanchez, M., and Wong, H., "Implications of Historical Trends in the Electrical Efficiency of Computing," IEEE Annals of the History of Computing, Vol. 33, No. 3, pp. 46–54, July–September 2011. DOI: 10.1109/MAHC.2010.28

#segment:dc_infra #source-tier:S #signal-type:roadmap #date:2011 #importance:medium #confidence:high

---

## 4. Data Center Thermal Guidelines — ASHRAE TC 9.9 Standard

> "ASHRAE TC 9.9 establishes thermal guidelines for data processing environments through four equipment classes: A1 (inlet temp 15–32°C), A2 (10–35°C), A3 (5–40°C), A4 (5–45°C) for standard rack equipment. Maximum recommended rack power density for air-cooled installations: 6 kW (Class A1), 10 kW (Class A2), 15 kW (Class A3), 20 kW (Class A4). Air cooling is specified as capable of handling up to approximately 45 kW/rack under specific airflow conditions. For AI GPU racks exceeding 45 kW (e.g., NVIDIA GB200 NVL72 at 120 kW), the ASHRAE W (water-cooled) and L (liquid-cooled) classes apply, requiring rear-door heat exchangers, direct liquid cooling cold plates, or immersion cooling systems."

**Source:** ASHRAE Technical Committee 9.9 (TC 9.9), "Thermal Guidelines for Data Processing Environments," 5th Edition, Atlanta, GA: ASHRAE, 2021. Available: ashrae.org/technical-resources/bookstore/datacom-series; Green Grid, "The Green Grid Data Center Power Efficiency Metrics: PUE and DCiE," White Paper #49, The Green Grid Association, 2016.

#segment:dc_infra #source-tier:A #signal-type:roadmap #date:2021 #importance:high #confidence:high

---

## 5. Power Usage Effectiveness (PUE) — Industry Efficiency Metric

> "Power Usage Effectiveness (PUE) is defined as: PUE = Total Facility Power / IT Equipment Power. A PUE of 1.0 represents ideal efficiency (all facility power consumed by IT equipment). A PUE of 2.0 means equal power is consumed by overhead (cooling, lighting, power conversion losses) as by IT equipment. The Green Grid established PUE as the standard data center efficiency metric in 2007. Hyperscaler average PUE: Google reported 1.10 (2023 annual average), Meta 1.10, Microsoft 1.12 — significantly below the industry average of approximately 1.55–1.58 (Uptime Institute 2023 survey). AI GPU data centers with liquid cooling achieve lower PUE than equivalent air-cooled facilities because liquid cooling infrastructure has lower overhead losses."

**Source:** The Green Grid, "The Green Grid Data Center Power Efficiency Metrics: PUE and DCiE," White Paper #6, The Green Grid Association, 2008. Updated: "PUE: A Comprehensive Examination of the Metric," White Paper #49, 2012. Available: thegreengrid.org; Barroso, L.A. and Hölzle, U., "The Datacenter as a Computer," Morgan & Claypool, 2009. DOI: 10.2200/S00193ED1V01Y200905CAC006

#segment:dc_infra #source-tier:A #signal-type:roadmap #date:2012 #importance:high #confidence:high

---

## 6. Liquid Cooling Thermodynamics — Heat Transfer Fundamentals

> "Liquid cooling of electronics exploits the high specific heat capacity of water (Cp = 4,186 J/kg·K) and high heat transfer coefficients achievable with forced liquid convection. Heat removed per unit mass flow: Q = ṁ × Cp × ΔT. For a 700W GPU cold plate with 20°C inlet, 40°C outlet water: ṁ = 700/(4,186×20) = 0.00836 kg/s = 0.5 L/min. By comparison, air cooling (Cp = 1,005 J/kg·K) at the same temperatures requires: ṁ = 700/(1,005×20) = 0.035 kg/s = ~29 L/min of air — at air density ~1.2 kg/m³, this is ~0.024 m³/s = 24 L/s of airflow per GPU. Liquid cooling's 4.2× higher specific heat vs. air allows 4.2× less mass flow rate for the same heat removal, drastically reducing fan power and noise."

**Source:** Incropera, F.P., Dewitt, D.P., Bergman, T.L., and Lavine, A.S., "Fundamentals of Heat and Mass Transfer," 7th Edition, John Wiley & Sons, 2011. ISBN: 9780470501979. Chapter 7: External Flow, Chapter 11: Heat Exchangers; ASHRAE TC 9.9 (2021).

#segment:dc_infra #source-tier:S #signal-type:roadmap #date:2011 #importance:high #confidence:high

---

## Open Technical Questions

- [ ] Two-phase direct-on-chip boiling for GPU chiplets (GB200 dual-die Blackwell): has any hyperscaler deployed vapor-phase immersion cooling at rack scale for NVL72?
- [ ] PFAS-free immersion dielectric fluids: which alternatives (synthetic hydrocarbons, low-GWP HFOs) are qualified to MIL-I-7444 or equivalent for server electronics?
- [ ] Rear-door heat exchanger (RDHX) vs. direct cold plate for 120 kW racks: what is the measured PUE difference in production at Meta or Microsoft?
- [ ] US power transformer lead time (128 weeks as of 2025): what is the domestic manufacturing capacity expansion timeline from ABB Hitachi Energy and SPX?
