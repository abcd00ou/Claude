# Samsung Foundry

**Segment(s):** foundry  
**Role in AI SCM:** #2 global foundry by revenue; 3nm GAA in production; no confirmed major AI GPU customer  
**HQ:** South Korea  
**Ticker:** KRX:005930 (Samsung Electronics)  
**Last Updated:** 2025-04-30

---

## Company Overview

Samsung Foundry is the contract manufacturing division of Samsung Electronics, competing with TSMC for leading-edge logic production. It launched GAA (Gate-All-Around) transistor architecture at 3nm (SF3E) in 2022, ahead of TSMC's N3 node, but has reported persistent yield challenges relative to TSMC at equivalent nodes. No major AI GPU customer (NVIDIA, AMD, or Google TPU) has been confirmed at Samsung Foundry as of Q1 2025.

**Source:** Samsung Electronics Q1 2026 Earnings, 2026-04-30; TechInsights Foundry Yield Analysis, 2024-Q3

---

## Key Products & AI Relevance

| Product / Technology | AI Use Case | Market Position |
|---|---|---|
| SF3E (3nm GAA) | Mobile SoC, potential future AI inference | Challenger — yield below TSMC N3 |
| SF4X (4nm FinFET) | Mid-range SoC | Volume production; limited AI design wins |
| SF2 (2nm GAA) | Next-gen AI/mobile | Development phase; targeting volume 2025 |
| FOWLP / FOPLP | Advanced packaging | Competing with TSMC CoWoS; no major AI win |

**Source:** Samsung Foundry Technology Roadmap, 2024; TechInsights, 2024

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
| Foundry Revenue (est.) | ~$16–18B | CY2024 | TrendForce Foundry Market Report, 2024-Q4 |
| Foundry Market Share | ~13% | CY2026 est. | TrendForce, 2026-Q1 |
| DS Division OP (total) | KRW 53.7T | Q1 2026 | Samsung Q1 2026 Earnings, 2026-04-30 |
| Foundry Operating Loss | Reported loss | 2023–2024 | Samsung Annual Report 2024 |

---

## Supply Chain Position

Samsung Foundry competes directly with TSMC for leading-edge logic orders. Its primary customers for advanced nodes (3nm/4nm) include Qualcomm, Google (older TPU generations), IBM, and NVIDIA (legacy nodes only). NVIDIA's Blackwell architecture and AMD MI-series are manufactured exclusively at TSMC. Samsung Foundry's absence from the AI GPU supply chain is a confirmed structural gap.

**Key customers (publicly stated):** Qualcomm (SF4 mobile SoC), IBM (Z16 mainframe), Google (limited; older nodes), AMD (historical; MI-series now at TSMC)  
**Key suppliers (publicly stated):** ASML (EUV scanners), Tokyo Electron (deposition), Lam Research (etch)

**Source:** Samsung Foundry Ecosystem Partners, 2024; NVIDIA 10-K FY2025, 2025-02-26 (confirming TSMC sole-source)

---

## Technology Roadmap

| Milestone | Timeline | Status | Source |
|---|---|---|---|
| SF3E (3nm GAA) — first AI chip attempt | 2022-H2 | Volume (limited AI customers) | Samsung Foundry Forum 2022 |
| SF2 (2nm GAA) — next AI target | 2025 | Development / early sampling | Samsung Foundry Technology Roadmap, 2024 |
| FOPLP (fan-out panel level packaging) | 2025–2026 | Pilot; no AI GPU customer confirmed | Samsung Foundry, 2024 |
| 1.4nm (SF1.4) | 2027+ | R&D | Samsung Foundry Forum 2024 |

---

## Competitive Position

| Competitor | Segment | Key Differentiator (stated by company or analyst) | Source |
|---|---|---|---|
| TSMC | Foundry | N3/N2 yield superior; CoWoS fully integrated; sole AI GPU fab | TechInsights, 2024-Q3; NVIDIA 10-K FY2025 |
| Intel Foundry | Foundry | 18A RibbonFET competing with SF2; both in sampling phase | Intel Foundry Services, 2025 |

---

## Updates

### Update: 2025-04-30 — Q1 2026: DS Division OP KRW 53.7T; foundry yield gap ongoing

> Samsung Electronics Q1 2026 earnings disclosed DS (Device Solutions) operating profit of KRW 53.7T, with the foundry segment still reporting losses. Samsung noted that 2027 HBM shortage will be "more severe than 2026." No AI GPU foundry win was disclosed. SF3E yield gap versus TSMC N3 remains unquantified in official filings.

**Source:** Samsung Electronics Q1 2026 Earnings, 2026-04-30

#segment:foundry #source-tier:A #signal-type:supply #company:samsung_foundry #date:2025-04-30 #importance:high #confidence:high

### Update: 2024-Q3 — TechInsights: Samsung 3nm yield ~35–60% vs TSMC N3 ~70%+

> TechInsights analysis estimated Samsung SF3E (3nm GAA) wafer yield at approximately 35–60%, compared to TSMC N3's estimated 70%+ yield. The yield gap is cited as the primary reason NVIDIA and AMD have not qualified Samsung Foundry for AI GPU production. Samsung has publicly acknowledged ongoing yield improvement efforts.

**Source:** TechInsights Foundry Yield Comparison Report, 2024-Q3 (cited by multiple analyst notes)

#segment:foundry #source-tier:B #signal-type:supply #company:samsung_foundry #date:2024-Q3 #importance:high #confidence:medium #cross-ref

---

## Open Questions

- [ ] When (if ever) will Samsung Foundry win an AI GPU design at 3nm or 2nm?
- [ ] What is the exact yield rate for SF3E vs TSMC N3 in official or third-party verification?
- [ ] FOPLP vs CoWoS — will Samsung win any hyperscaler advanced packaging business?
- [ ] SF2 (2nm) customer pipeline — are any AI chip customers sampling?
