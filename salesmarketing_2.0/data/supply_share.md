# Live Data — HBM Share & Supply-Demand Balance 2026

**Created:** 2026-06-24 · **Feeds:** Product Supply Mgr (SM-T1) ⇄ MI supply · **real sourced**

Supply-side signals: vendor HBM share and the supply-demand balance for 2026.

| entity | metric | value | period | tier | status | conf | source |
|---|---|---|---|---|---|---|---|
| SK hynix | HBM market share | ~50–55% | 2026 | analyst | reconciled | 0.7 | [S1](#s1) [S2](#s2) |
| Samsung | HBM market share | ~35–40% | 2026 | analyst | reconciled | 0.7 | [S1](#s1) |
| Micron | HBM market share | ~5–10% | 2026 | analyst | reconciled | 0.7 | [S1](#s1) |
| HBM3E | supply vs demand | tight, supply lags demand | 2026 | analyst | verified | 0.7 | [S1](#s1) [S3](#s3) |
| DRAM (all) | capacity expansion | not before late 2027 | 2026–2027 | analyst | verified | 0.7 | [S4](#s4) |
| NVIDIA H200 | HBM3E content | 6 stacks / accelerator | 2026 | other | reconciled | 0.6 | [S3](#s3) |

**Quote (balance):** "HBM3E supply remains tight and continues to lag demand." (TrendForce /
SK hynix 2026 outlook)

## Notes
- The binding constraint is HBM capacity — share + tightness here pair with the `sim/capacity.md`
  ~zero-headroom scenario and the `customer_demand_request` HBM conflict. `#importance:high`
- H200 = 6 HBM3E stacks → each accelerator unit is a large HBM pull; ties capex (demand_capex.md)
  to stack demand.
- Vendor shares are analyst estimates (ranges) → `reconciled` at conf 0.7, not firm.

## Sources
- <a id="s1"></a>**S1** — "SK hynix 2026 Outlook: HBM3E Dominates, HBM4 Dual Strategy", TrendForce, 2026-01-05 — https://www.trendforce.com/news/2026/01/05/news-sk-hynix-2026-outlook-hbm3e-remains-mainstream-hbm4-dual-strategy-amid-triple-market-headwinds/
- <a id="s2"></a>**S2** — "Global DRAM and HBM Market Share: Quarterly", Counterpoint Research — https://counterpointresearch.com/en/insights/global-dram-and-hbm-market-share
- <a id="s3"></a>**S3** — "2026 Market Outlook: SK hynix's HBM to Fuel AI Memory Boom", SK hynix Newsroom — https://news.skhynix.com/2026-market-outlook-focus-on-the-hbm-led-memory-supercycle/
- <a id="s4"></a>**S4** — "AI Server Demand to Drive Memory Contract Price Increases in 2Q26", TrendForce, 2026-03-31 — https://www.trendforce.com/presscenter/news/20260331-12995.html
