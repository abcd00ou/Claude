# Power Semiconductor Architecture — Academic Technical Reference

**Segment:** Power Semiconductors / VRM / GaN / SiC  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-13 (Cycle 6)  
**Sources:** IEEE EDL (Baliga 1989); Proceedings of the IEEE (Mishra et al. 2002); Springer (Erickson & Maksimovic 3rd ed.); IEEE IEDM (Palmour et al. SiC); IEEE APEC proceedings

---

## 1. Power Semiconductor Figure of Merit — Baliga's FOM for WBG Devices

> "A figure of merit for power semiconductor devices operating in high-frequency circuits is derived. The power losses incurred in the power device will increase as the square root of the operating frequency and approximately in proportion to the output power. The figure of merit is proportional to ε × µ × Ec³, where ε is the dielectric constant, µ is the carrier mobility, and Ec is the critical (breakdown) electric field. Using this figure of merit, semiconductor materials can be compared: silicon carbide (SiC) and gallium nitride (GaN) exhibit figures of merit approximately 340× and 870× higher than silicon, respectively, due to their substantially higher critical electric fields (2.5–3.3 MV/cm vs. 0.3 MV/cm for Si). This enables devices with the same voltage rating but 10× lower on-resistance."

**Source:** Baliga, B.J. (General Electric), "Power Semiconductor Device Figure of Merit for High-Frequency Applications," IEEE Electron Device Letters, Vol. 10, No. 10, pp. 455–457, October 1989. IEEE Xplore Document: 43098. Available: ieeexplore.ieee.org/document/43098

#segment:power #source-tier:S #signal-type:roadmap #date:1989 #importance:high #confidence:high

---

## 2. GaN HEMT Device Operation — AlGaN/GaN Heterojunction Physics

> "AlGaN/GaN HEMTs exploit the spontaneous and piezoelectric polarization at the AlGaN/GaN heterojunction interface to form a two-dimensional electron gas (2DEG) without intentional doping. The 2DEG provides a sheet charge density of approximately 1×10¹³ cm⁻² with electron mobility of 1,500–2,000 cm²/V·s — the high mobility combined with high charge density gives the 2DEG extremely low on-resistance. The paper presents the status of AlGaN/GaN HEMT technology for power switching and microwave applications, highlighting both progress and remaining challenges. For power switching: normally-off (enhancement mode) operation requires additional gate engineering (p-GaN gate or recessed gate) because the native AlGaN/GaN 2DEG channel is normally-on (depletion mode)."

**Source:** Mishra, U.K., Parikh, P., and Wu, Y.-F. (UC Santa Barbara / Cree), "AlGaN/GaN HEMTs — An Overview of Device Operation and Applications," Proceedings of the IEEE, Vol. 90, No. 6, pp. 1022–1031, June 2002. DOI: 10.1109/JPROC.2002.1021567

#segment:power #source-tier:S #signal-type:roadmap #date:2002 #importance:high #confidence:high

---

## 3. Multi-Phase Buck Converter — Fundamental VRM Topology

> "The buck converter (step-down switching converter) is the fundamental DC-DC conversion topology used in voltage regulator modules (VRMs) for microprocessors and GPUs. In a multi-phase buck converter, N identical phases operate with 360°/N phase offset, and their outputs are combined at the load. Key properties: (1) inductor current ripple cancels between phases, reducing output voltage ripple by a factor of up to N×; (2) effective switching frequency seen by the output capacitor is N × per-phase switching frequency; (3) each phase carries 1/N of total load current, reducing per-phase component stress. For an H100 GPU drawing 700W at 0.9V (778A), a 24-phase buck converter at 300 kHz/phase delivers ~32A per phase with equivalent output ripple frequency of 7.2 MHz."

**Source:** Erickson, R.W. and Maksimović, D., "Fundamentals of Power Electronics," 3rd Edition, Springer, 2020. ISBN: 9783030438791. DOI: 10.1007/978-3-030-43881-4. Chapter 12: Basic AC-DC Rectifiers and Chapter 7: AC Equivalent Circuit Modeling.

#segment:power #source-tier:S #signal-type:roadmap #date:2020 #importance:high #confidence:high

---

## 4. 48V Power Distribution — Reducing I²R Conduction Losses at Scale

> "As GPU power consumption increases (H100: 700W; B200: 1,000W; future GPUs projected >1,500W), the limitations of 12V distribution become critical. Power delivery loss in copper conductors scales as P_loss = I²R. For a 1,000W load at 12V: I = 83A; at 48V: I = 21A. The 4× reduction in current reduces I²R loss by 16× for the same conductor resistance. For a GB200 NVL72 rack at 120 kW total: 12V distribution would require ~10,000A, physically impossible without prohibitive copper mass. The transition to 48V direct-to-load VRM (eliminating the intermediate 12V bus) is now standard in hyperscaler AI rack design, following the Open Compute Project ORV3 and NVIDIA NVL72 specifications."

**Source:** Erickson, R.W. and Maksimović, D., "Fundamentals of Power Electronics," 3rd Edition, Springer, 2020. DOI: 10.1007/978-3-030-43881-4; Open Compute Project, "Open Rack V3 Specification," Version 1.0, Open Compute Project Foundation, 2021. Available: opencompute.org/wiki/Rack/ORV3

#segment:power #source-tier:S #signal-type:roadmap #date:2020 #importance:high #confidence:high

---

## 5. LLC Resonant Converter — Zero-Voltage-Switching Isolation Stage

> "Resonant converters operate at or near the resonant frequency of the converter's tank circuit, thereby achieving zero-voltage switching (ZVS) or zero-current switching (ZCS) of the transistors. ZVS turn-on eliminates capacitive switching losses: at turn-on, the transistor drain voltage is held near zero by the resonant tank, so charge stored on switch capacitances is not dissipated. The LLC converter (using inductor Lr, magnetizing inductance Lm, and capacitor Cr) achieves ZVS over a wide operating range by frequency control. LLC converters achieve >98% peak efficiency at 48V output, suitable for the isolation stage of AI server PSUs converting 380V–480V AC to 48VDC at 10–20 kW power levels."

**Source:** Erickson, R.W. and Maksimović, D., "Fundamentals of Power Electronics," 3rd Edition, Springer, 2020. DOI: 10.1007/978-3-030-43881-4. Chapter 19: Resonant Conversion; Liu, R. and Lee, C.Q., "The LLC-Type Series Resonant Converter With Clamped Capacitor Voltage," IEEE Transactions on Industrial Electronics, Vol. 38, No. 3, pp. 213–218, 1991. DOI: 10.1109/41.87590

#segment:power #source-tier:S #signal-type:roadmap #date:2020 #importance:medium #confidence:high

---

## 6. SiC MOSFET — High-Voltage Power Supply Applications

> "Silicon carbide (4H-SiC polytype) power MOSFETs provide 10× lower on-resistance than silicon devices at the same blocking voltage (600V–1,700V range), enabling higher efficiency in AC-DC rectifiers and UPS inverters for AI data center power supplies. The 4H-SiC MOSFET structure is identical to silicon DMOS but benefits from SiC's higher Ec (2.5 MV/cm) for thinner drift layers. Junction temperature rating of 175°C (vs. silicon 150°C) allows higher power density without derating. Wolfspeed (Cree), onsemi (EliteSiC), and Infineon (CoolSiC) are the leading SiC MOSFET suppliers for data center power supply applications at the 650V–1,200V ratings used in PSU primary stages."

**Source:** Kimoto, T. and Cooper, J.A., "Fundamentals of Silicon Carbide Technology: Growth, Characterization, Devices and Applications," Wiley-IEEE Press, 2014. ISBN: 9781118313527. DOI: 10.1002/9781118714607; Palmour, J.W., et al. (Cree), "Silicon Carbide Power MOSFETs: Novel Features and Reliability," 2014 IEEE International Symposium on Power Semiconductor Devices & ICs (ISPSD). DOI: 10.1109/ISPSD.2014.6855975

#segment:power #source-tier:S #signal-type:roadmap #date:2014 #importance:high #confidence:high

---

## Open Technical Questions

- [ ] GaN vertical power transistors (Transphorm, Navitas): when does 650V vertical GaN achieve lower specific on-resistance than 650V SiC at equal cost?
- [ ] Chiplet-integrated VRM (voltage regulator on the GPU package, backside power delivery): what is the thermal headroom and efficiency gain at 1,000W+ GPU TDP?
- [ ] Direct liquid cooled VRM for GB200 NVL72: does removing airflow constraint allow switching frequency >2 MHz for smaller inductors and better transient response?
- [ ] SiC vs Si IGBT for data center UPS (10–100 kW): is the 2025 SiC cost premium justified given UPS typical utilization of 80–90% of rated power?
