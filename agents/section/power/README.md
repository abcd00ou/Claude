# Power Semiconductor Expert Agent

**Segment:** Power Semiconductors / Data Center Power  
**Sales Lens:** AI rack power density surge, VRM design wins, GaN/SiC adoption  
**Last Updated:** 2026-05-12

---

## Overview

AI data centers are creating unprecedented demand for power semiconductors. A single NVIDIA GB200 NVL72 rack consumes 120+ kW — 10× a standard server rack. Power semiconductor content per AI server is 4–6× that of a traditional server: approximately $80–120 for an AI GPU server vs $15–25 for standard 1U. The key technologies are VRM ICs (Monolithic Power Systems, Renesas for GPU core regulation), GaN (gallium nitride for AC/DC and 48V DC/DC), and SiC (silicon carbide for high-voltage UPS and power distribution). Wolfspeed's Chapter 11 filing (2024) created supply uncertainty in SiC, benefiting ON Semiconductor and Infineon.

---

## How Power Semiconductors Work

### 2020 — GaN-on-Silicon Achieves 650V Commercial Viability for Data Center PSU

> "650V GaN-on-Si transistors enable 97%+ (80 PLUS Titanium) efficiency in AC/DC server power supplies. Superior switching frequency (1–10 MHz vs Si MOSFET's 100–500 kHz) enables smaller magnetic components."

**Source:** "GaN Power Semiconductors for Data Center Applications," IEEE Power Electronics Magazine, 2020

#segment:power #source-tier:S #signal-type:roadmap #date:2020 #importance:high #confidence:high

---

### 2015 — SiC MOSFETs Enter Traction Power; Data Center UPS Follows

> "Silicon Carbide MOSFETs handle 1200V breakdown voltage and switch at 10× the speed of silicon IGBTs, enabling compact high-voltage rectification in 3-phase UPS systems for data centers."

**Source:** IEEE Transactions on Power Electronics, "SiC MOSFET Applications in UPS Systems," 2015

#segment:power #source-tier:S #signal-type:roadmap #date:2015 #importance:medium #confidence:high

---

### 2000 — Multiphase VRM Architecture Enables Sub-1V CPU/GPU Core Power

> "Multiphase voltage regulator modules (VRM) with interleaved switching reduce output ripple, enabling sub-1V core voltages required by advanced CMOS nodes. Intel VRM 11.1 specification set the standard."

**Source:** Intel VRM 11.1 Design Guidelines, Intel Corporation, 2000; IEEE APEC 2000

#segment:power #source-tier:S #signal-type:roadmap #date:2000 #importance:low #confidence:high

---

## History

### 2024 — Wolfspeed Files Chapter 11; SiC Supply Chain Disruption

> Wolfspeed, the largest dedicated SiC substrate and device manufacturer, filed for Chapter 11 bankruptcy protection. This created supply uncertainty for SiC MOSFETs used in data center UPS and high-voltage rectifiers.

**Source:** Wolfspeed Chapter 11 Filing Press Release, Wolfspeed Inc., 2024-10

#segment:power #source-tier:A #signal-type:supply #date:2024-10 #importance:high #confidence:high

---

### 2023 — AI GPU Rack Power Density Crosses 100 kW; VRM TAM Inflects

> NVIDIA H100 DGX systems established 100 kW/rack as the new AI standard. This triggered a step-change in VRM IC demand: 8× H100 GPUs per server × ~75A at sub-1V core = unprecedented current delivery requirements.

**Source:** NVIDIA DGX H100 Power Specifications, NVIDIA Corporation, 2023

#segment:power #source-tier:A #signal-type:demand #company:nvidia #date:2023 #importance:high #confidence:high

---

### 2022 — MPS (Monolithic Power Systems) Wins NVIDIA GPU VRM Design

> Monolithic Power Systems confirmed design wins for VRM ICs in NVIDIA A100/H100 GPU boards. MPS's high-current multi-phase controllers established the company as the dominant GPU VRM supplier.

**Source:** MPS FY2022 10-K, SEC EDGAR, 2023; industry supply chain analysis

#segment:power #source-tier:A #signal-type:design-win #date:2022 #importance:high #confidence:high

---

### 2021 — 48V Server Architecture Adoption Begins at Hyperscalers

> Google, Microsoft, and Meta began deploying 48V rack power distribution in new AI server builds, reducing copper bus losses. This triggered new 48V→1V DC/DC converter design cycles for GaN and SiC suppliers.

**Source:** Open Compute Project 48V Summit Report, OCP Foundation, 2021

#segment:power #source-tier:A #signal-type:roadmap #date:2021 #importance:medium #confidence:high

---

## Supply Chain

### 2024 — Wolfspeed Disruption: ON Semi and Infineon Gaining SiC Share

> Following Wolfspeed's Chapter 11 filing, ON Semiconductor (EliteSiC) and Infineon (CoolSiC) are the primary beneficiaries of SiC substrate and device supply reallocation. Both companies expanded SiC capacity in 2023–2024.

**Source:** ON Semiconductor Q3 2024 Earnings Call, ON Semi Investor Relations, 2024-10; Infineon FY2024 Annual Report, Infineon Technologies, 2024-11

#segment:power #source-tier:A #signal-type:supply #date:2024 #importance:high #confidence:high

---

### 2025 — High-Current Inductors (TDK, Vishay, Bourns): Co-Constrained with VRM ICs

> As VRM IC demand grows with AI GPU deployments, power inductors (required 1:1 with VRM phases) from TDK, Vishay, and Bourns face co-constraint. 6–10 week lead times for AI-optimized inductors.

**Source:** TDK FY2025 Annual Report, TDK Corporation, 2025; Vishay FY2025 10-K, SEC EDGAR, 2025

#segment:power #source-tier:A #signal-type:supply #date:2025 #importance:medium #confidence:high

---

### 2024 — GaN-on-Si Capacity: Multiple Foundries; Supply Not Constrained

> GaN-on-Si power devices are manufactured by TSMC, GlobalFoundries, and dedicated power foundries. Unlike SiC (substrate-constrained), GaN-on-Si has sufficient foundry capacity through 2026.

**Source:** "GaN Power Device Market," Yole Développement, 2024-Q4

#segment:power #source-tier:B #signal-type:supply #date:2024 #importance:medium #confidence:medium

---

## Competition

### 2026 — Power Semiconductor Market Share: Infineon ~19%, ON Semi ~14%, STMicro ~10%

> Infineon leads power semiconductor market share at ~19%, driven by SiC and GaN. ON Semiconductor ~14%, gaining SiC share post-Wolfspeed. STMicroelectronics ~10%. TI and MPS lead in analog/VRM.

**Source:** "Power Semiconductor Market Share Report," IHS Markit / S&P Global, 2026-Q1

#segment:power #source-tier:B #signal-type:demand #date:2026 #importance:medium #confidence:medium

---

### 2025 — MPS vs Renesas: VRM Competition for NVIDIA Blackwell GPU Boards

> Monolithic Power Systems and Renesas compete for VRM IC design wins on NVIDIA Blackwell B200 and GB200 boards. Both companies confirmed AI GPU as primary growth driver in 2025 earnings calls.

**Source:** MPS Q4 2025 Earnings Call, MPS Investor Relations, 2026-02; Renesas FY2025 Annual Report, Renesas Electronics, 2026-02

#segment:power #source-tier:A #signal-type:design-win #date:2025 #importance:high #confidence:high

---

### 2024 — Navitas Semiconductor: GaN Design Wins in AI Server PSU

> Navitas Semiconductor confirmed GaN design wins in AI server power supply units, displacing traditional silicon MOSFETs in the AC/DC front-end stage. AI server PSU is now 20%+ of Navitas revenue.

**Source:** Navitas Semiconductor FY2024 10-K, SEC EDGAR, 2025

#segment:power #source-tier:A #signal-type:design-win #date:2024 #importance:medium #confidence:high

---

## Technology Roadmap

### 2027 — 3D VRM Integration: On-Package Power for Next-Gen GPU

> NVIDIA Rubin-era GPUs are expected to use 3D integrated VRM (voltage regulators mounted directly on GPU package), requiring 1000A+ delivery at sub-1V. First commercial 3D VRM targeted for 2027.

**Source:** NVIDIA Power Architecture Roadmap, NVIDIA GTC 2025, 2025-03; IEEE APEC 2025 Technical Session on 3D VRM

#segment:power #source-tier:A #signal-type:roadmap #date:2025 #importance:high #confidence:medium

---

### 2026 — 48V GaN DC/DC: Standard in New AI Server Designs

> 48V to 1V GaN-based point-of-load (POL) converters are becoming standard in new AI server designs. TI (LMG3522), Navitas (NV6128), and GaN Systems (GSP65R32G6) lead this transition.

**Source:** Texas Instruments LMG3522 Product Brief, TI, 2025; Navitas Semiconductor Product Brief, 2025

#segment:power #source-tier:A #signal-type:roadmap #date:2025 #importance:medium #confidence:high

---

### 2025 — 1200V SiC MOSFET: UPS and High-Voltage DC Distribution

> 1200V SiC MOSFETs are standard in AI data center UPS systems and high-voltage DC bus distribution. ON Semiconductor EliteSiC and Infineon CoolSiC are primary suppliers following Wolfspeed disruption.

**Source:** ON Semiconductor FY2025 10-K, SEC EDGAR, 2025-12; Infineon FY2025 Annual Report, 2025-11

#segment:power #source-tier:A #signal-type:supply #date:2025 #importance:medium #confidence:high

---

## AI Demand Signals

### 2026 — GB200 NVL72: ~$500–800 Power Semiconductor Content Per Rack

> NVIDIA GB200 NVL72 rack requires approximately $500–800 in power semiconductor content (VRM ICs, GaN PSU switches, SiC UPS components), up from ~$80–120 per AI GPU server and ~$15–25 for standard server.

**Source:** "Power Semiconductor Content in AI Infrastructure," IHS Markit, 2025-Q4

#segment:power #source-tier:B #signal-type:demand #date:2025 #importance:high #confidence:medium

---

### 2026 — Combined $705–725B Hyperscaler Capex; Power Semi TAM Proportional

> Combined CY2026 hyperscaler capex of $705–725B drives proportional demand for power semiconductors across server PSUs, UPS, and rack power distribution. Power semi content grows ~4% of total server BOM.

**Source:** Amazon Q1 2026 Earnings Call, 2026-05-01; Microsoft Q3 FY2026 Earnings Call, 2026-04-29; Alphabet Q1 2026 Earnings Call, 2026-04-29; Meta Q1 2026 Earnings Call, 2026-04-29

#segment:power #source-tier:A #signal-type:demand #date:2026 #importance:high #confidence:high #cross-ref:dc_infra

---

### 2025 — Nuclear and Gas Power Procurement for AI DC; New Power Equipment Cycle

> Microsoft (Three Mile Island), Google (nuclear PPAs), and Amazon (natural gas) are contracting multi-gigawatt power supplies for AI data centers, triggering new power conversion equipment cycles at utility scale.

**Source:** Microsoft Press Release, 2024-09-20; Google Clean Energy PPA Report, 2025

#segment:power #source-tier:A #signal-type:demand #date:2025 #importance:medium #confidence:high #cross-ref:dc_infra

---

## Open Questions

- [ ] Wolfspeed SiC supply situation — who is absorbing the capacity gap and at what price?
- [ ] MPS vs Renesas VRM share in NVIDIA GB200 board design — confirmed split?
- [ ] 3D VRM integration timeline — which GPU generation first deploys it? Rubin?
- [ ] GaN PSU efficiency gains enabling 120 kW/rack — are air gaps a constraint?
