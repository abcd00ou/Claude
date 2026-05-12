# Orchestrator Cycle Log

Running log of all completed intelligence cycles. Updated at end of each cycle.

---

## Cycle 5 — 2026-05-12

**Status:** Complete  
**Synthesis:** `synthesis/2026-05-12_cycle5.md`  
**Type:** Research Cycle (external web agents — 2 agents, standard mode)  
**Update logs created:** All 10 sections (dram, storage, chip_maker, foundry, power, substrate, dc_infra, network, asic, end_market) — Q2–Q3 2025 through Q1 2026  
**Company files updated:** NVIDIA (Vera Rubin CES specs), SK Hynix (Q2 2025 HBM share + HBM4 qual), Samsung (HBM collapse to 17%), Vertiv (Q1 2026 backlog), Google TPU (Ironwood GA), Amazon Trainium (Trainium3 full specs)  
**Signals generated:** 5 new cross-segment signals (Signals 22–26)

**Key findings:**
- Samsung HBM market share collapsed to 17% in Q2 2025 (NVIDIA qualification failure); Micron rose to #2 at 21%; SK Hynix extended lead to 62%
- NVIDIA Vera Rubin: 288 GB HBM4 per GPU, 22 TB/s bandwidth, 50 PFLOPS per chip — single platform drives HBM TAM from $35B to $58B+ in 2026
- Samsung Foundry SF2P hit 70% yield (January 2026) — first credible 2nm AI chip path; AMD in negotiations for Venice EPYC on SF2
- Power transformer lead times: 128 weeks (2.5 years) in U.S. — AI DC buildout constrained by grid infrastructure, not just chip supply
- All four hyperscalers (Google Ironwood GA Nov 2025, Amazon Trainium3 Dec 2025, Meta MTIA Gen 2, Microsoft Maia 200) now have production AI ASIC at scale

**Open flags carried to Cycle 6:**
- Samsung NVIDIA HBM3E re-qualification result
- AMD Venice on Samsung SF2P — final confirmation
- Vera Rubin NVL72 specific volume production quarter (H2 2026)
- U.S. transformer manufacturing capacity response
- Ultra Ethernet 1.0 first named hyperscaler production deployment
- Google Ironwood TSMC node confirmation
- Wolfspeed SiC split — Infineon vs onsemi still unquantified
- Ibiden ¥500B investment quarterly capacity timeline
- Amkor CoWoS qualification

---

## Cycle 4 — 2026-05-12

**Status:** Complete  
**Synthesis:** `synthesis/2026-05-12_cycle4.md`  
**New company files:** Samsung Foundry, Intel Foundry (foundry); Western Digital/SanDisk (storage); NVIDIA Networking (network); AT&S, Shinko Electric (substrate); Google TPU, Amazon Trainium (asic)  
**New market files:** `foundry/market/packaging.md`, `network/market/roadmap.md`  
**New update logs:** `foundry/updates/2025-Q1.md`, `storage/updates/2025-Q1.md`, `network/updates/2025-Q2.md`  
**Signals generated:** 5 new cross-segment signals (Signals 17–21)

**Key findings:**
- TSMC foundry monopoly on AI GPU manufacturing structurally hardened — Samsung Foundry yield gap (35–60% vs TSMC 70%+) and Intel Foundry losses (-$2.3B Q1 2025) leave no qualified backup for AI GPU production
- WD/Kioxia JV controls ~32–34% of global NAND bits post-SanDisk spin-off (Feb 2025) — second-largest NAND concentration after Samsung
- OSAT packaging (ASE/Amkor) not yet qualified for CoWoS-class advanced packaging; Amkor talks with TSMC unconfirmed; TSMC CoWoS remains only path for AI GPU packaging
- Ultra Ethernet 1.0 spec ratified in 2024 but not yet in production at any hyperscaler; NVIDIA InfiniBand NDR dominance extends into 2026
- Google TPU 8t/8i (N3) + Amazon Trainium3 at scale; both on TSMC N3 — compounding TSMC foundry pressure alongside NVIDIA B200

**Open flags carried to Cycle 5:**
- Amkor CoWoS overflow qualification timeline
- Samsung SF2 AI GPU customer sampling
- Ultra Ethernet 1.0 first production deployment
- Google Ironwood specs (TFLOPS, HBM, TSMC node)
- Trainium3 volume production timeline and specs
- Wolfspeed SiC gap absorption split (Infineon vs onsemi) — still unquantified
- Vera Rubin HBM4 configuration
- AT&S Kulim 2 exact capacity addition

---

## Cycle 2 — 2026-05-12

**Status:** Complete  
**Synthesis:** `synthesis/2026-05-12_cycle2.md`  
**Segments updated:** network, power, substrate (all 3 previously unpopulated)  
**Companies added:** Marvell, Broadcom, Arista, MPS, Infineon, ON Semi, Ibiden, Unimicron  
**Signals generated:** 5 new cross-segment signals (Signals 8–12)

**Key findings:**
- Marvell + Broadcom have divided the hyperscaler ASIC design market; combined AI run-rate ~$5.5B/Q
- Ethernet winning AI cluster fabric; Broadcom raised AI TAM to $60–90B by FY2027
- Power semiconductor content 4–6× per AI server; VRM design wins on critical path
- ABF substrate (Ibiden + Unimicron) fully allocated; no new capacity until FY2027
- TSMC is single point of dependency across 9 of 10 supply chain segments

**Open flags carried to Cycle 3:**
- Ultra Ethernet 1.0 production deployments — which hyperscalers in 2026?
- Wolfspeed SiC gap absorption split (Infineon vs onsemi) — not quantified
- Ibiden FY2027 capacity — exact quarterly timeline and units
- Unimicron Hsinchu Phase 2 Q4 2025 qualification — confirmed or delayed?
- MPS vs Renesas VRM split on NVIDIA GB200 board

---

## Cycle 1 — 2026-05-12

**Status:** Complete  
**Synthesis:** `synthesis/2026-05-12.md`  
**Segments updated:** dram, storage, foundry, chip_maker, asic, end_market, dc_infra (7 of 10)  
**Companies added:** SK Hynix, Samsung, Micron (dram+storage), TSMC, NVIDIA, AMD, Microsoft, Google, Amazon, Meta  
**Signals generated:** 7 cross-segment signals (Signals 1–7)

**Key findings:**
- All 2026 HBM supply fully committed across all 3 suppliers; 2027 "more severe"
- Component pricing inflating hyperscaler capex: Microsoft +$25B, Meta +$10B (closed-loop confirmed)
- Combined 4-hyperscaler CY2026 capex $705–725B; Alphabet +107% YoY
- NVIDIA CoWoS dependency confirmed in 10-K; CoWoS remains tightest AI constraint
- HBM4 mass production begun; HBM4E + Vera Rubin define 2027 challenge
- AMD: 6 GW commitments from Meta + OpenAI for MI450
- Agentic AI driving new inference demand shape (KV-SSD, continuous workloads)

---

## Cycle 3 — 2026-05-12

**Status:** Complete  
**Synthesis:** `synthesis/2026-05-12_cycle3.md`  
**New company files:** Intel (chip_maker), CoreWeave (end_market), Vertiv (dc_infra), Kioxia (storage), Renesas (power)  
**New market files:** chip_maker/market/roadmap.md, dram/market/pricing.md  
**Signals generated:** 4 new cross-segment signals (Signals 13–16)

**Key findings:**
- NVIDIA Q1 FY2026: $39.1B DC revenue; Blackwell exceeded Hopper revenue for first time; demand still exceeds supply
- CoreWeave S-1: $15.1B backlog, $11.9B OpenAI commitment, Microsoft 35% of revenue — neo-cloud is structural
- Intel effectively excluded from AI GPU market; Gaudi revenue not disclosed
- Vertiv DLC lead times improving (40–52wk → 28–36wk); cooling constraint easing but transformer still 52–65wk
- Cumulative signal count: 16 cross-segment signals across all 3 cycles

**Open flags carried to Cycle 4:**
- TSMC CoWoS capacity figures — still not in formal filings
- Ultra Ethernet 1.0 production deployments
- Wolfspeed SiC gap absorption split not quantified
- Vera Rubin HBM configuration not disclosed
- AMD MI450 specs (Meta vs OpenAI) not confirmed
- CoreWeave GPU fleet composition in 2025
