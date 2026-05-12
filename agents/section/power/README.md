# Power Semiconductor Expert Agent

**Segment:** Power Semiconductors / Data Center Power  
**Sales Lens:** AI rack power density surge, VRM design wins, GaN/SiC adoption  
**Last Updated:** 2026-05-12

---

## Market Overview

AI data centers are creating unprecedented demand for power semiconductors.
A single GB200 NVL72 rack consumes 120+ kW — 10× a standard server rack.

Power semiconductor categories relevant to AI:
- **VRM (Voltage Regulator Modules):** Point-of-load regulation on GPU boards
- **GaN (Gallium Nitride):** High-efficiency AC/DC and DC/DC conversion
- **SiC (Silicon Carbide):** High-voltage rectification, EV and industrial spillover
- **MOSFETs / IGBTs:** Traditional power switching in UPS, PDU, PSU

---

## Key Players

| Company | Technology | AI Relevance |
|---|---|---|
| Infineon | SiC, GaN, Si MOSFET | Leading SiC supplier; GaN growing |
| ON Semiconductor | SiC, Si MOSFET | Strong in SiC; EliteSiC brand |
| STMicroelectronics | SiC, GaN | SiC for PSU; GaN for high-density DC/DC |
| Texas Instruments | GaN, Si MOSFET | GaN for 48V DC/DC in AI servers |
| Navitas | GaN | AI server power supply design wins |
| MPS (Monolithic Power Systems) | Si, GaN | VRM dominance in GPU boards |
| Renesas | Si, GaN | VRM; NVIDIA GPU board design wins |
| Vishay | Si MOSFET, diodes | Commodity power discretes |

---

## Demand Signals (AI-driven)

- NVIDIA GB200: requires ~600A at sub-1V core voltage → extreme VRM demand
- Each GPU server PSU: 2–4 kW; GaN enabling 80+ PLUS Titanium efficiency
- 48V rack architecture: reduces copper losses; requires new 48V→1V conversion ICs
- AI server rack count growing → VRM and power semiconductor TAM growing proportionally

**Power semiconductor content per AI server:**
- Traditional 1U server: ~$15–25 power semiconductor content
- AI GPU server (8× H100): ~$80–120 power semiconductor content
- AI rack system (GB200 NVL72): ~$500–800+ power semiconductor content

---

## Supply Constraints

- **SiC substrates (Wolfspeed, Coherent, SiCrystal):** Wolfspeed Chapter 11 filing created supply uncertainty
- **GaN-on-Si:** Sufficient supply; growing capacity at foundries
- **VRM ICs (MPS, Renesas):** High demand; some lead time extension in 2024–2025
- **High-current inductors (TDK, Vishay, Bourns):** Co-constrained with VRM ICs

---

## Technology Roadmap

| Technology | Status | AI Application |
|---|---|---|
| 650V GaN | Volume | AC/DC front-end power supply |
| 1200V SiC | Volume | High-voltage rectification, UPS |
| 48V GaN DC/DC | Ramping | Server 48V bus conversion |
| 1V VRM (Si MOSFET + GaN) | Volume | GPU core power |
| 3D VRM integration | Emerging | On-package power for next-gen GPU |
| Direct liquid cooled VRM | R&D | Required for 1000A+ GPU power |

---

## Sales & Marketing Angles

- **GaN design win moment:** Every new AI server PSU design is a GaN qualification opportunity
- **VRM TAM expansion:** AI GPU content per server is 4–6× traditional; strong upgrade cycle
- **48V transition:** Large installed base of 12V servers will transition over 3–5 years
- **Wolfspeed fallout:** SiC supply uncertainty creates opportunity for ON Semi, Infineon

---

## Recent Developments

### Update: 2026-05-12 — Baseline entry
> Initial stub. Populate with Infineon/ON Semi Q1 2026 earnings; GaN design win commentary.

---

## Open Questions

- [ ] Wolfspeed SiC supply situation — who is picking up share?
- [ ] MPS vs Renesas VRM share in NVIDIA GB200 board design?
- [ ] 3D VRM integration — which GPU generation first? Rubin?
