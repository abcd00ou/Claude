# Analysis Report — Cycle 7

**Date:** 2026-05-13  
**Cycle:** 7  
**Agent:** Analysis Agent  
**Input signals:** C7-01 through C7-19 (19 new signals)  
**Cumulative signal count:** 51 (32 from Cycles 1–6 + 19 from Cycle 7)

---

## 1. HBM Supply Chain — Market Structure Solidifying

**Observation:**  
Samsung's HBM3E NVIDIA qualification (Sept 2025) and confirmed ~30% HBM4 allocation for Vera Rubin closes the previously open flag. The HBM4 market is now a confirmed duopoly for NVIDIA's highest-priority platform: SK Hynix (~70%) and Samsung (~30%). Micron is excluded from Vera Rubin HBM4.

**2026 HBM4 market structure (Counterpoint forecast):** SK Hynix 54%, Samsung 28%, Micron 18%.

**SK Hynix ramp constraint:** The HBM4 mass production ramp delayed from Q2 to Q3 2026 because HBM3E demand is so persistently high that SK Hynix is maintaining HBM3E lines longer than planned. This delays volume HBM4 availability for platforms beyond Vera Rubin.

**Sales angle:** Customers evaluating HBM4 supply for H2 2026 programs should factor in the ramp delay. Samsung's recovery to ~28-30% share is a positive diversification signal for NVIDIA; supply security for Vera Rubin is now better than it was during the Blackwell era.

---

## 2. NVIDIA Platform Transition — Blackwell to Rubin Accelerating

**GB300 (Blackwell Ultra):** Shipping since January 2026, ahead of schedule. 129% YoY growth projected; ~60,000 racks in 2026. Microsoft deployed the first large-scale GB300 NVL72 cluster (4,608 GPUs) for OpenAI workloads in February 2026.

**Vera Rubin (NVL72):** Full production confirmed, ahead of schedule. All 8 named cloud providers (AWS, GCP, Azure, OCI, CoreWeave, Lambda, Nebius, Nscale) confirmed H2 2026 deployment. NVIDIA's order backlog disclosed as "at least $1 trillion" through 2027 at Q4 FY2026 earnings.

**Interpretation:** The overlap between GB300 ramp and Rubin deployment in H2 2026 creates simultaneous demand pressure on HBM, CoWoS packaging, and NVLink fabric capacity. No historical precedent for two major platform ramps in the same calendar year.

---

## 3. Advanced Packaging — TSMC CoWoS Monopoly Breaking Down

**TSMC CoWoS:** Targeting 130,000–150,000 WPM by end of 2026 (from ~35,000 WPM end of 2024). NVIDIA holds >60% of total allocation.

**OSAT overflow now confirmed at scale:** TSMC outsourcing 240K-270K CoWoS wafers/year to Amkor (~180K-190K) and SPIL/ASE (~60K-80K). Amkor formally MOU'd with TSMC for CoWoS/InFO in Arizona. This is a structural change: CoWoS is no longer a TSMC-exclusive process in terms of volume. However, TSMC-originated CoWoS still dominates for leading-edge AI GPU packaging in 2026.

**Emerging alternatives:**  
- Powertech: panel-level glass substrate ~30% cheaper than CoWoS-L; attracting U.S. AI chipmakers through 2027  
- ASE CoWoP: 20K-25K WPM target by end 2026; NVIDIA CoWoP project with SPIL  
- Intel EMIB: evaluated by second-tier ASIC vendors

**Interpretation:** The moat protecting TSMC's CoWoS pricing power is narrowing. Powertech and ASE CoWoP create real cost competition for mid-tier AI chip packaging by 2027, though not for Vera Rubin-class leading-edge work in 2026.

---

## 4. AI Networking — Ethernet Has Won the Volume Battle

**Dell'Oro Group:** Ethernet accounts for >2/3 of AI cluster switch sales in FY2025 — a reversal from InfiniBand's 80% share just two years earlier. Named Ethernet adopters: Amazon, Microsoft, Meta, Oracle, xAI.

**UE 1.0 status:** Oracle is the first confirmed production deployment (AMD Pensando Pollara + MI350X). AWS and Google have not confirmed production UE 1.0 deployment. UE 1.0.1 released September 2025; working on three 2026 technical priorities.

**NVLink Fusion:** NVIDIA's strategic response to Ethernet competition is not to fight it — instead, NVIDIA is embedding its interconnect (NVLink) inside hyperscaler ASIC designs. The $2B Marvell investment and Arm's NVLink Fusion membership create a structural path where NVIDIA's fabric survives even as hyperscalers build custom compute silicon.

**1.6 Tbps switches:** Volume production expected H2 2026 — will drive a new round of Ethernet share gains.

---

## 5. U.S. Power Infrastructure — Critical Path Is Getting Longer

**Current state:** Lead times 128 weeks on average (Wood Mackenzie), up to 4 years in some segments (pv magazine, May 11, 2026). Generator step-up transformers: 144 weeks. Power transformer prices up 77% since 2019.

**Supply additions:** ~$1.8B announced, but no new plant comes online before Q1 2027 at the earliest (Siemens Charlotte NC). Hitachi Energy's largest plant (South Boston VA, $457M) not until 2028.

**Impact now:** Up to 50% of U.S. data centers planned for 2026 delayed; only 1/3 of 12 GW planned for 2026 under construction as of April 2026. Grid interconnection queues in some U.S. regions stretched to 7+ years.

**Hyperscaler response:** Building on-site "energy islands" (dedicated power generation bypassing the public grid). This represents a structural shift in how hyperscalers relate to utilities — from grid customers to quasi-utilities themselves.

**Sales angle:** Power delivery equipment suppliers with in-stock or short-lead-time alternatives (smaller distribution transformers, solid-state transformers, modular power systems) have pricing power in 2026–2027. This is a multi-year constraint — not a 2026-only issue.

---

## 6. Custom ASIC / Hyperscaler Silicon — Scale-Up Has Arrived

**Meta:** Four-chip MTIA roadmap (300/400/450/500), 4 chips in 2 years on ~6-month cadence. First TSMC N2 AI chip is MTIA (next-gen). 1 GW initial deployment. Broadcom is the design partner across all MTIA generations.

**AMD-Meta deal:** 6 GW of MI450 GPUs over 5 years (~$60B), with Meta taking 10% AMD equity stake. This is the most significant competitive challenge to NVIDIA's GPU monopoly in the hyperscaler segment since the NVIDIA-hyperscaler relationship was established.

**xAI:** 555K GPUs at Memphis ($18B), new $20B Southaven MS site. Scale trajectory: targeting 1M GPUs at Memphis; 50M H100-equivalents over 5 years.

**Trainium4:** NVLink Fusion confirmed — this means AWS's custom ASIC strategy is now explicitly compatible with NVIDIA's interconnect ecosystem. Not a displacement play; a coexistence play.

---

## 7. Total Hyperscaler Capex — Scale Now in Macroeconomic Territory

**2026 capex (post-Q1 earnings):**
| Company | 2026 Capex | YoY Growth |
|---|---|---|
| Amazon | ~$200-230B | ~50-70% |
| Alphabet | $180-190B | ~100%+ |
| Microsoft | ~$190B | ~61% |
| Meta | $125-145B | ~85% |
| Oracle | ~$50B | ~136% |
| **Total US Big 4** | **~$695-755B** | |
| **Top 9 CSPs (TrendForce)** | **$830B** | |

At $830B, the total 2026 AI infrastructure investment by the top 9 cloud providers is larger than the GDP of most countries. The binding constraint is no longer capital — it is physical supply chain: CoWoS wafers, HBM stacks, transformers, and grid interconnection slots.

---

## Open Questions for Cycle 8

1. When do Vera Rubin NVL72 instances become available at AWS, Google Cloud, and Microsoft Azure specifically — Q3 or Q4 2026?
2. Will AMD MI450 ramp on schedule (Q3 2026 small volume, Q4 2026 majority) given TSMC N2 early ramp constraints?
3. Is Samsung's ~30% Vera Rubin HBM4 allocation secure, or are there further NVIDIA qualification risks?
4. Which named U.S. AI chipmaker formally adopts Powertech glass substrate for volume production?
5. Does any AWS/Google/Microsoft confirm a production UE 1.0 deployment by end of 2026?
6. Does Wolfspeed Mohawk Valley fab maintain market share post-restructuring, or do Infineon and onsemi capture share faster than expected?
