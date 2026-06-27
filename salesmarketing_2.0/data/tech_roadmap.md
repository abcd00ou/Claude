# Live Data — Tech Roadmap 2026 (HBM4 / HBM4E / LPDDR6 / DDR)

**Created:** 2026-06-24 · **Feeds:** Customer Tech (CT-T1/T2), future spec · **real sourced**

Real 2026 spec + mass-production status. Note JEDEC standards and company announcements come
out `verified`; press reports of samples/timing land lower.

## HBM4 / HBM4E

| item | spec / status | period | tier | status | conf | source |
|---|---|---|---|---|---|---|
| HBM4 standard | JEDEC JESD270-4, 2048-bit I/O, up to 8 GT/s, up to 2 TB/s, 4–16 high, 24/32Gb die, up to 64GB, 32 channels | std Apr 2025 | official | verified | 1.0 | [S1](#s1) |
| SK hynix HBM4 | mass production launched | Feb 2026 | official | verified | 0.9 | [S2](#s2) |
| SK hynix HBM4 | 10 GT/s (≈25% over 8 GT/s spec) | 2026 | official | verified | 0.9 | [S2](#s2) |
| SK hynix HBM4 | 16-layer variant MP target | Q3 2026 | analyst | reconciled | 0.7 | [S3](#s3) |
| Samsung HBM4 | 12-layer volume shipments | Feb 2026 | other | reconciled | 0.7 | [S4](#s4) |
| Samsung/SK hynix HBM4 | qualified with NVIDIA & AMD | 2026 | other | reconciled | 0.6 | [S4](#s4) |
| Samsung HBM4E | industry-first samples, 3.6 TB/s | May 2026 | other | unverified-needs-human | 0.5 | [S5](#s5) |

**Quote (HBM4 standard):** "HBM4 doubles interface width from 1024 to 2048 bits … up to 8 Gb/s …
total bandwidth up to 2 TB/s … capacities up to 64GB." (JEDEC JESD270-4)

## LPDDR6 / DDR

| item | spec / status | period | tier | status | conf | source |
|---|---|---|---|---|---|---|
| LPDDR6 standard | JEDEC JESD209-6 published | Jul 2025 | official | verified | 1.0 | [S6](#s6) |
| Micron LPDDR6 | 1-gamma 16Gb sampling to OEMs | Dec 2025 | official | verified | 0.8 | [S7](#s7) |
| SK hynix LPDDR6 | 1c LPDDR6 developed; shipments target | dev Mar 2026 / ship H2 2026 | official | verified | 0.8 | [S7](#s7) |
| LPDDR6 roadmap | JEDEC preview: x24 non-binary width, PIM, SOCAMM2, 512GB density on horizon | Apr 2026 | official | verified | 0.9 | [S8](#s8) |

**Quote (LPDDR6 roadmap):** "JEDEC previews LPDDR6 roadmap expanding LPDDR into data centers
and processing-in-memory." (JEDEC, Apr 2026)

## Roadmap → demand fit (real data version of sim/future_tech_spec)
- **HBM4 in MP Feb 2026, qualified with NVIDIA/AMD** → meets AI-accelerator HBM4 demand on time
  (contrast the sim's tight-timing scenario). `#importance:high`
- **LPDDR6 shipments H2 2026 (SK hynix)** → aligns to next mobile/edge platform design-in windows.

## Sources
- <a id="s1"></a>**S1** — "HBM roadmaps for Micron, Samsung, and SK hynix: To HBM4 and beyond", Tom's Hardware — https://www.tomshardware.com/tech-industry/semiconductors/hbm-roadmaps-for-micron-samsung-and-sk-hynix-to-hbm4-and-beyond
- <a id="s2"></a>**S2** — "SK hynix Completes World-First HBM4 Development and Readies Mass Production", SK hynix Newsroom — https://news.skhynix.com/sk-hynix-completes-worlds-first-hbm4-development-and-readies-mass-production/
- <a id="s3"></a>**S3** — "The HBM4 Era Begins: Samsung and SK Hynix Trigger Mass Production", FinancialContent, 2026-01-26 — https://www.financialcontent.com/article/tokenring-2026-1-26-the-hbm4-era-begins-samsung-and-sk-hynix-trigger-mass-production-for-next-gen-ai
- <a id="s4"></a>**S4** — "Samsung, SK Hynix reportedly accelerate HBM4 production to early 2026", Digitimes, 2025-12-26 — https://www.digitimes.com/news/a20251226PD223/samsung-sk-hynix-production-hbm4-2026.html
- <a id="s5"></a>**S5** — "Samsung Ships Industry-First HBM4E Samples: 3.6 TB/s", TechTimes, 2026-05-30 — https://www.techtimes.com/articles/317400/20260530/samsung-ships-industry-first-hbm4e-samples-36-tb-s-bandwidth-beats-sk-hynix-six-months.htm
- <a id="s6"></a>**S6** — "JEDEC Releases New LPDDR6 Standard", JEDEC — https://www.jedec.org/news/pressreleases/jedec%C2%AE-releases-new-lpddr6-standard-enhance-mobile-and-ai-memory-performance
- <a id="s7"></a>**S7** — "JEDEC Previews LPDDR6 Roadmap" (Micron/SK hynix sampling detail), Yahoo/JEDEC — https://finance.yahoo.com/sectors/technology/articles/jedec-previews-lpddr6-roadmap-expanding-170000672.html
- <a id="s8"></a>**S8** — "JEDEC Previews LPDDR6 Roadmap Expanding LPDDR into Data Centers and PIM", BusinessWire, 2026-04-22 — https://www.businesswire.com/news/home/20260422533176/en/JEDEC-Previews-LPDDR6-Roadmap-Expanding-LPDDR-into-Data-Centers-and-Processing-in-Memory
