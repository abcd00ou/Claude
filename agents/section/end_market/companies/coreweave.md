# CoreWeave — Neo-Cloud / GPU Cloud

**Segment(s):** end_market, dc_infra  
**Role in AI SCM:** Largest GPU-native cloud provider; primary NVIDIA H100/H200/B200 capacity outside hyperscalers; IPO 2025  
**HQ:** Roseland, New Jersey, USA  
**Last Updated:** 2025-04-01

---

## Company Overview

CoreWeave is the largest dedicated GPU cloud provider, holding approximately 100,000+ NVIDIA H100-equivalent GPUs as of late 2024. It is NVIDIA's preferred infrastructure partner and has received preferred GPU allocation. Microsoft is CoreWeave's largest customer, using CoreWeave capacity as overflow for Azure AI demand. CoreWeave completed its IPO in March 2025. OpenAI committed $11.9 billion to CoreWeave over 5 years (disclosed in CoreWeave S-1).

**Source:** CoreWeave S-1 Registration Statement, SEC EDGAR, 2025-03-01; CoreWeave IPO Prospectus, 2025-03-28

---

## Key Products & AI Relevance

| Service | AI Use Case | Status |
|---|---|---|
| CoreWeave Cloud (GPU compute) | AI training and inference rental | Primary service |
| NVIDIA H100/H200/B200 fleet | LLM training, inference | ~100K+ H100 equiv. as of 2024 |
| Managed Kubernetes (SUNK) | AI cluster orchestration | Enterprise AI deployment |
| HPC (scientific computing) | Simulation, rendering | Secondary segment |

---

## Financial Profile

| Metric | Value | Period | Source |
|---|---|---|---|
| Revenue | $1.92B | FY2024 | CoreWeave S-1, SEC EDGAR, 2025-03-01 |
| Revenue Growth | +737% YoY | FY2024 | CoreWeave S-1, SEC EDGAR, 2025-03-01 |
| Net Loss | -$863M | FY2024 | CoreWeave S-1, SEC EDGAR, 2025-03-01 |
| Committed Backlog | $15.1B | As of Dec 31, 2024 | CoreWeave S-1, SEC EDGAR, 2025-03-01 |
| IPO Valuation | ~$19B | March 2025 | CoreWeave IPO, NASDAQ:CRWV, 2025-03-28 |

---

## Supply Chain Position

CoreWeave is a pure compute infrastructure company — it does not design chips but is a major GPU buyer. NVIDIA is its sole AI chip supplier. CoreWeave's massive NVIDIA GPU orders give it preferred allocation, making it a proxy demand indicator for NVIDIA data center GPU supply.

**Key suppliers:** NVIDIA (100% of AI compute chips)  
**Key customers:** Microsoft (largest; ~35% of FY2024 revenue per S-1), OpenAI ($11.9B committed backlog), Meta

**Source:** CoreWeave S-1, SEC EDGAR, 2025-03-01

---

## Updates

### Update: 2025-03-01 — S-1: $15.1B Committed Backlog; OpenAI $11.9B; Microsoft 35% of Revenue

> "As of December 31, 2024, we had $15.1 billion of remaining performance obligations from signed customer contracts. Our largest customer [Microsoft] accounted for approximately 35% of our revenue in FY2024. OpenAI has committed approximately $11.9 billion in purchases over 5 years."

**Source:** CoreWeave S-1 Registration Statement, SEC EDGAR, 2025-03-01

#segment:end_market #source-tier:A #signal-type:demand #company:coreweave #date:2025-03-01 #importance:high #confidence:high #cross-ref:chip_maker

---

### Update: 2025-03-01 — S-1: FY2024 Revenue $1.92B (+737% YoY); NVIDIA Preferred Partner

> "Revenue for fiscal year 2024 was $1.92 billion, up 737% from $230M in FY2023. We have a strategic relationship with NVIDIA that provides us preferred access to NVIDIA GPU products, including next-generation products."

**Source:** CoreWeave S-1 Registration Statement, SEC EDGAR, 2025-03-01

#segment:end_market #source-tier:A #signal-type:demand #company:coreweave #date:2025-03-01 #importance:high #confidence:high #cross-ref:chip_maker

---

### Update: 2025-03-28 — CoreWeave IPO at ~$19B Valuation; NASDAQ:CRWV

> CoreWeave completed its initial public offering at $40/share, valuing the company at approximately $19 billion. The IPO raised approximately $1.5 billion to fund GPU purchases and data center expansion.

**Source:** CoreWeave IPO Prospectus, NASDAQ:CRWV, 2025-03-28

#segment:end_market #source-tier:A #signal-type:capex #company:coreweave #date:2025-03-28 #importance:high #confidence:high

---

### Update: 2026-03-30 — Post-IPO: NVIDIA $2B investment + $6.3B take-or-pay; $8.5B DDTL 4.0 closed (Moody's A3); $19.2B Meta backing; FY2026 guidance $12–13B revenue

> NVIDIA invested $2B in CoreWeave at $87.20/share (January 2026) and signed a $6.3B take-or-pay capacity backstop through April 2032. March 30, 2026: CoreWeave closed an $8.5B DDTL 4.0 financing facility — the first investment-grade GPU-backed financing, rated Moody's A3, backed by an expanded $19.2B Meta agreement (up from a prior $14.2B commitment). April 2026: Multi-year Anthropic agreement signed, adding a new anchor customer. FY2026 revenue guidance: $12–13B; Q2 2026 guidance: $2.45–2.60B; exit ARR $18–19B; FY2026 capex $31–35B.

**Source:** TechCrunch, January 26 2026; BusinessWire, March 30 2026, https://www.businesswire.com/news/home/20260330673736/en/CoreWeave-Closes-8.5-Billion-Delayed-Draw-Term-Loan-4.0; NVIDIA Newsroom

#segment:end_market #source-tier:A #signal-type:capex #company:coreweave #date:2026-03-30 #importance:high #confidence:high #cross-ref:chip_maker #cross-ref:dc_infra

---

## Open Questions

- [ ] CoreWeave GPU fleet composition in 2026 — what ratio of H100/H200/B200/GB200?
- [ ] Microsoft dependency risk — 35% customer concentration; is it declining vs. Meta/Anthropic growth?
- [ ] CoreWeave profitability path: FY2026 capex $31–35B vs. $12–13B revenue guidance — debt coverage sustainability?
