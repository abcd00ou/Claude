# Power Semiconductor Architecture — Academic Technical Reference

**Segment:** Power Semiconductors / VRM / GaN / SiC  
**Type:** Technical Architecture File  
**Last Updated:** 2026-05-12 (Cycle 5)  
**Sources:** IEEE Power Electronics Society (PELS) papers; JEDEC JEP106; Infineon, onsemi, TI application notes; IEEE APEC/ECCE conference proceedings

---

## 1. Multi-Phase Voltage Regulator Module (VRM) Architecture

### Multi-Phase Buck Converter Topology

> "A Voltage Regulator Module (VRM) delivers a regulated low-voltage (0.7–1.8V) supply to a GPU or CPU from a 12V or 48V bus. A multi-phase buck converter interleaves N identical phase legs operating at a phase shift of 360°/N from each other. Each phase leg consists of: (1) a high-side switch (MOSFET or GaN device) connected to the input voltage; (2) a low-side switch (synchronous rectifier); (3) an output inductor. Interleaving phases cancel output ripple — a 6-phase converter operating at 300 kHz per phase produces ripple at 1.8 MHz effective frequency, reducing output capacitor requirement by ~6×. AI GPU VRMs typically use 16–32 phases to deliver 500–1,000A output current at 0.9V to an H100 or B200 GPU."

**Source:** "Multiphase Buck Converter Design Guide," Texas Instruments SLVA662A, 2013; "High-Current Multiphase Voltage Regulators," IEEE Transactions on Power Electronics, 2018

#segment:power #source-tier:S #signal-type:roadmap #date:2013 #importance:high #confidence:high

---

### 48V Bus Architecture for AI Data Centers

> "Traditional data center power delivery uses a 12V bus from rack PDUs to server boards. AI GPU servers (NVIDIA DGX H100, GB200 NVL72) switch to a 48V bus to reduce I²R conduction losses. Power loss in a copper bus bar scales as P = I²R — at 48V vs 12V, delivering the same wattage (e.g., 1,000W) requires 4× less current (21A vs 83A), reducing resistive loss by 16×. For a 200 kW rack (GB200 NVL72), a 12V bus would require ~16,700A — physically impractical with copper busbars. 48V intermediate bus converters (IBCs) convert from rack-level 48V to board-level 12V or directly to VRMs via 48V-to-1V converters. NVIDIA GB200 NVL72 uses a 48V bus with direct 48V-to-GPU VRM (no 12V intermediate stage), reducing conversion losses."

**Source:** "48V Power Architecture for Next-Generation Data Centers," IEEE Transactions on Industry Applications, 2020; NVIDIA GB200 NVL72 Power Architecture, NVIDIA, 2024; "Open Rack V3 48V Standard," Open Compute Project, 2020

#segment:power #source-tier:S #signal-type:roadmap #date:2020 #importance:high #confidence:high

---

## 2. Wide-Bandgap Semiconductors: GaN and SiC

### Silicon vs GaN vs SiC — Semiconductor Physics

> "Power semiconductor performance is governed by Baliga's Figure of Merit (BFOM = ε × µ × Ec³, where Ec is critical electric field). GaN (Gallium Nitride) and SiC (Silicon Carbide) are wide-bandgap (WBG) semiconductors: (1) Si: bandgap 1.12 eV, Ec = 0.3 MV/cm, BFOM = 1 (reference); (2) SiC: bandgap 3.26 eV, Ec = 2.5 MV/cm, BFOM = 340; (3) GaN: bandgap 3.4 eV, Ec = 3.3 MV/cm, BFOM = 870. Higher Ec means GaN and SiC block the same voltage with a ~10× thinner drift region, dramatically reducing on-resistance (R_on) and conduction loss. This enables high-frequency, high-efficiency power conversion at voltages (600V–1,700V) where silicon is inadequate."

**Source:** "Wide Bandgap Power Semiconductor Devices," Baliga, B.J., Materials Science and Engineering: B, 1989; "GaN-Based Power Devices: Physics, Reliability, and Perspectives," IEEE JEDS, 2019

#segment:power #source-tier:S #signal-type:roadmap #date:1989 #importance:high #confidence:high

---

### GaN HEMT (High Electron Mobility Transistor) — AI VRM Application

> "GaN power transistors for AI VRM use the High Electron Mobility Transistor (HEMT) structure, exploiting the 2DEG (two-dimensional electron gas) at the AlGaN/GaN heterojunction interface. The 2DEG forms naturally due to spontaneous and piezoelectric polarization, providing a sheet charge density of ~1×10¹³ cm⁻² with electron mobility of ~1,500–2,000 cm²/V·s — 4× higher than bulk silicon MOSFET. Key GaN HEMT properties: (1) on-resistance R_on ~5–20 mΩ for 100V devices; (2) switching speed: turn-on/turn-off times <5 ns (vs Si MOSFET ~20–50 ns); (3) gate charge Qg ~4–10 nC (vs Si ~40–100 nC). The low Qg enables MHz-frequency switching, critical for 48V-to-1V VRMs serving AI GPUs. EPC (Efficient Power Conversion), GaN Systems (acquired by Infineon), and Texas Instruments supply GaN HEMTs for server VRMs."

**Source:** "GaN-on-Si Power Switching Transistors," IEEE Electron Device Letters, Braga et al., 2011; "High Frequency GaN Power Conversion," IEEE APEC, 2021; Infineon CoolGaN Product Brief, 2023

#segment:power #source-tier:S #signal-type:roadmap #date:2011 #importance:high #confidence:high

---

### SiC MOSFET — High-Voltage Power Supply Applications

> "SiC MOSFETs use the 4H-SiC polytype (hexagonal crystal structure) for the best combination of bandgap (3.26 eV) and electron mobility. SiC MOSFET structure is identical to Si DMOS (double-diffused MOSFET) but fabricated in SiC substrate. Key SiC advantages at 650V–1,700V ratings: (1) 10× lower on-resistance vs Si MOSFET at equivalent breakdown voltage; (2) body diode with low forward voltage (~2.5V vs Si ~0.7V, but SiC adds an antiparallel SiC Schottky diode in most modules); (3) junction temperature up to 175°C (vs Si ~150°C). For AI data center power supply units (PSUs): 48VDC rectifier stage and Uninterruptible Power Supply (UPS) inverter use SiC MOSFETs at 650V–1,200V. onsemi (EliteSiC), Wolfspeed (Cree), and Infineon (CoolSiC) are the leading SiC MOSFET suppliers."

**Source:** "4H-SiC Power Switching Devices," Kimoto and Cooper, Fundamentals of Silicon Carbide Technology, Wiley-IEEE Press, 2014; "SiC Power Devices for Data Center Applications," IEEE APEC Invited Paper, 2022; onsemi EliteSiC MOSFET Datasheet, 2023

#segment:power #source-tier:S #signal-type:roadmap #date:2014 #importance:high #confidence:high

---

## 3. Power Supply Architecture for AI Servers

### Totem-Pole PFC — High-Efficiency AC-to-DC

> "AI server PSUs use a Totem-Pole Power Factor Correction (TP-PFC) topology as the AC-to-DC front end. TP-PFC achieves >99% power factor and >98% efficiency at full load by using GaN HEMTs to switch at 200–500 kHz (vs Si-based PFC at 65–100 kHz). The high switching frequency reduces PFC inductor size by ~4× vs Si implementations. Bridgeless TP-PFC eliminates the input diode bridge (4 diodes) of traditional PFC, reducing conduction losses by approximately 0.5–1.0% efficiency. The OCP (Open Compute Project) Advanced Power Rack standard targets 48VDC at 97.5% peak efficiency for AI rack power, achievable with GaN TP-PFC."

**Source:** "High-Efficiency Totem-Pole PFC with GaN," IEEE Transactions on Power Electronics, 2020; "OCP Open Rack V3 Power Spec," Open Compute Project, 2022

#segment:power #source-tier:S #signal-type:roadmap #date:2020 #importance:high #confidence:high

---

### LLC Resonant Converter — 48V Bus Isolation Stage

> "The 48V bus requires galvanic isolation between the AC mains and the DC bus for safety and noise isolation. LLC resonant converters achieve soft switching (zero-voltage switching, ZVS) at high frequency by exploiting the resonance between the transformer leakage inductance (Lr), magnetizing inductance (Lm), and resonant capacitor (Cr). LLC converters: (1) achieve >98% peak efficiency at 48V output; (2) operate at 500 kHz–2 MHz with GaN devices (vs 100–200 kHz with Si); (3) near-zero switching losses due to ZVS; (4) simple frequency-controlled regulation. For an AI rack PSU delivering 12.5 kW at 48V from a 380V AC input (Facebook 380V open rack), the LLC stage handles the bulk conversion. SiC MOSFETs are used on the primary (high-voltage) side; GaN on the secondary (48V) side synchronous rectifier."

**Source:** "LLC Resonant Converter for Server Power," IEEE Transactions on Industrial Electronics, 2018; "High-Frequency LLC Converter with GaN Devices," IEEE APEC, 2023

#segment:power #source-tier:S #signal-type:roadmap #date:2018 #importance:medium #confidence:high

---

## 4. Current Sensing and Power Management IC (PMIC)

### Digital Pulse Width Modulation Controller

> "Modern multi-phase VRMs are controlled by a Digital PWM (DPWM) controller IC that: (1) monitors output voltage via high-speed ADC (12-bit, 10 MHz sampling); (2) runs a digital PID control loop to adjust duty cycle per phase; (3) implements current sharing between phases via I²C/PMBus telemetry; (4) reports per-phase current, temperature, and power to the BMC (Baseboard Management Controller) via PMBus. DPWM controllers (Renesas RAA2xxx, Monolithic Power Systems (MPS) MP2995) achieve transient response of <100µs for a 300A load step — critical for GPU workload burst transitions. For NVIDIA H100 GPU drawing up to 700W, the VRM must respond to GPU power steps of ~400W (57% of TDP) within 10µs to maintain voltage within ±2% regulation."

**Source:** "Digital Control of Multi-Phase Buck Converters," IEEE Transactions on Power Electronics, 2017; Renesas RAA229004 Datasheet, 2022; MPS MP2995 Product Brief, 2023

#segment:power #source-tier:A #signal-type:roadmap #date:2017 #importance:medium #confidence:high

---

## 5. Power Delivery to GPU — From Wall to Die

> "The AI GPU power delivery chain from utility power to silicon involves 5 conversion stages, each with efficiency loss: (1) Utility transformer (medium-voltage to 480V): ~99% efficient; (2) UPS inverter/bypass (480V to 480VAC): ~97%; (3) Server PSU AC-to-48VDC (480V to 48V via 3-phase rectifier): ~97%; (4) Intermediate Bus Converter (48V to 12V, if used): ~98% — GB200 NVL72 eliminates this stage; (5) VRM 48V-to-0.9V (multi-phase buck): ~92%. Cumulative efficiency (GB200 NVL72, no IBC): 0.99×0.97×0.97×0.92 = 85.7%. For a 1 MW data center cluster, ~143 kW is lost in power conversion. This is why the 48V direct-to-GPU architecture (eliminating the 12V bus) is adopted in GB200 NVL72."

**Source:** "Efficiency Analysis of Data Center Power Delivery," Google, IEEE APEC, 2019; NVIDIA GB200 NVL72 Power Architecture Brief, NVIDIA, 2024

#segment:power #source-tier:A #signal-type:roadmap #date:2019 #importance:high #confidence:high

---

## Open Technical Questions

- [ ] GaN vertical power transistors (Transphorm, Navitas): when will 650V GaN outperform SiC MOSFET for PSU primary switches?
- [ ] Direct liquid cooled VRM for GB200: does removing airflow constraint allow higher switching frequency (>2 MHz) for smaller inductors?
- [ ] Chiplet-integrated VRM (voltage regulator on the GPU package): what is the thermal constraint vs efficiency benefit?
- [ ] SiC vs Si IGBT for data center UPS (10–100 kW): is SiC cost premium justified for 2025 UPS replacement cycle?
