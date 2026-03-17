---
name: market-sizing
description: >
  USE THIS SKILL when the user asks to size a market, estimate TAM/SAM/SOM,
  calculate addressable market, project market opportunity, estimate market
  potential, determine market size, build a market model, or quantify demand.
  Trigger terms: "market size", "TAM", "SAM", "SOM", "addressable market",
  "market opportunity", "how big is the market", "total market", "serviceable
  market", "market potential", "demand estimation", "market forecast".
---

# Market Sizing

Rigorous market sizing using dual TAM/SAM/SOM methodology (top-down and bottom-up) with reconciliation, sensitivity analysis, and growth projection.

---

## Required Inputs

| Input | Description | Required? |
|---|---|---|
| Industry / product category | What market is being sized | Yes |
| Geographic scope | Country, region, or global | Yes |
| Target customer segment(s) | Who buys this product/service | Yes |
| Product/service definition | What is being sold, at what price point | Yes |
| Time horizon | Current year and projection period (e.g., 2026-2031) | Yes |
| Company capabilities | Current reach, channels, capacity constraints | For SOM |
| Known data points | Any existing research, revenue figures, customer counts | If available |
| Currency | Reporting currency | Yes |

---

## Execution Steps

### Step 1: Define Market Boundaries

Establish precise definitions before any calculation:

1. **Product scope**: What products/services are included and excluded?
2. **Customer scope**: Which buyer segments (B2B, B2C, enterprise, SMB)?
3. **Geographic scope**: Which countries/regions? Regulatory differences?
4. **Value chain scope**: Which parts of the value chain (manufacturing, distribution, SaaS layer)?

Document boundary decisions explicitly — these are the #1 source of market sizing disagreements.

### Step 2: Top-Down Analysis

Start from the largest defensible number and narrow:

1. **Identify macro data sources** (in order of reliability):
   - Government statistics (Census, BLS, Eurostat, national statistical offices)
   - Industry association reports (trade bodies, industry groups)
   - Analyst reports (Gartner, IDC, Forrester, Statista, IBISWorld)
   - Public company filings (10-K revenue disclosures, earnings calls)
   - Academic research and published studies

2. **Calculate top-down TAM**:
   - Total industry revenue globally or in target geography
   - OR: Total number of potential buyers x average annual spend per buyer

3. **Apply segmentation filters for SAM**:
   - Filter by geography served
   - Filter by customer segment targeted
   - Filter by product/service fit (what portion of spend your offering addresses)
   - Filter by channel accessibility

4. **Apply penetration and capacity constraints for SOM**:
   - Realistic market share given competitive landscape (use analogues)
   - Channel and sales capacity limits
   - Brand awareness and reach constraints
   - Time-to-penetrate considerations

### Step 3: Bottom-Up Analysis

Build from unit economics upward:

1. **Count target customers**:
   - Identify the number of potential buyers in each segment
   - Use company registries, industry databases, demographic data

2. **Estimate purchase behavior**:
   - Average deal size / ticket price
   - Purchase frequency (annual, monthly, one-time)
   - Adoption rate by segment (early adopters vs. mainstream)

3. **Calculate bottom-up TAM**:
   ```
   TAM = Σ (Customers_in_segment × Price × Purchase_frequency) for all segments
   ```

4. **Calculate bottom-up SAM**:
   ```
   SAM = Σ (Reachable_customers × Price × Frequency) for served segments
   ```

5. **Calculate bottom-up SOM**:
   ```
   SOM = SAM × Expected_penetration_rate × Conversion_rate
   ```

### Step 4: Reconciliation

Compare top-down and bottom-up estimates:

1. **Calculate variance**: If top-down and bottom-up differ by >30%, investigate why
2. **Identify discrepancy sources**:
   - Pricing assumptions differ?
   - Customer count estimates differ?
   - Scope definitions misaligned?
3. **Triangulate**: Use a third method (e.g., analogue-based, value-theory) if gap persists
4. **Select final estimate**: State which approach is primary and why; use the other as a sanity check
5. **Document confidence level**: High (estimates within 15%), Medium (15-40% range), Low (>40% range)

### Step 5: Growth Rate Projection

Project market growth over the time horizon:

1. **Historical growth rate**: CAGR over last 3-5 years from industry data
2. **Driver-based growth model**:
   - Population/business formation growth
   - Penetration rate increase (adoption curve position)
   - Price changes (inflation, premiumization, commoditization)
   - Usage intensity changes
   - Regulatory tailwinds/headwinds
3. **Analogue comparison**: How did similar markets grow? (e.g., cloud adoption curve for AI SaaS)
4. **Adoption curve positioning**: Where on the S-curve is this market? (innovators → early majority → late majority)

| Growth Phase | Typical Annual Growth | Characteristics |
|---|---|---|
| Emerging | 30-80%+ | Pre-product/market fit, few players |
| High growth | 15-30% | Product/market fit proven, competition entering |
| Growth | 8-15% | Market maturing, consolidation beginning |
| Mature | 2-8% | Established players, GDP+ growth |
| Declining | <0% | Substitution, obsolescence |

### Step 6: Sensitivity Analysis

Test key assumptions:

1. **Identify the 3-5 variables with the highest impact** on market size (typically: customer count, price, adoption rate, growth rate)
2. **Define ranges** for each variable (pessimistic, base, optimistic)
3. **Build sensitivity table**: Show how TAM/SAM/SOM change as each variable moves
4. **Tornado chart inputs**: Rank variables by impact magnitude

---

## Output Template

### Market Sizing: [Industry/Product] — [Geography]

**Date**: [Date] | **Prepared for**: [Client/Project] | **Confidence Level**: [High/Medium/Low]

#### 1. Market Definition & Boundaries

| Dimension | Included | Excluded |
|---|---|---|
| Products/Services | [Specific offerings] | [Adjacent categories excluded] |
| Customer Segments | [Target segments] | [Non-target segments] |
| Geographies | [Countries/regions] | [Out-of-scope regions] |
| Value Chain | [Stages included] | [Stages excluded] |

#### 2. TAM / SAM / SOM Waterfall

| Metric | Top-Down Estimate | Bottom-Up Estimate | Reconciled Estimate | Confidence |
|---|---|---|---|---|
| **TAM** (Total Addressable Market) | $[X]B | $[X]B | **$[X]B** | [H/M/L] |
| **SAM** (Serviceable Addressable Market) | $[X]B | $[X]B | **$[X]B** | [H/M/L] |
| **SOM** (Serviceable Obtainable Market) | $[X]M | $[X]M | **$[X]M** | [H/M/L] |

**SAM as % of TAM**: [X]% — *[Explanation of narrowing factors]*
**SOM as % of SAM**: [X]% — *[Explanation of capture assumptions]*

#### 3. Top-Down Methodology

| Step | Value | Source | Notes |
|---|---|---|---|
| Global industry revenue | $[X]B | [Source, Year] | [Methodology note] |
| Geographic filter ([Region]) | $[X]B | [Source] | [X]% of global |
| Segment filter ([Segment]) | $[X]B | [Source] | [X]% of regional |
| Product relevance filter | $[X]B | [Assumption] | [X]% of segment spend |
| **Top-Down TAM** | **$[X]B** | | |

#### 4. Bottom-Up Methodology

| Segment | # of Customers | Avg. Annual Spend | Segment TAM |
|---|---|---|---|
| [Segment 1] | [N] | $[X] | $[X]M |
| [Segment 2] | [N] | $[X] | $[X]M |
| [Segment 3] | [N] | $[X] | $[X]M |
| **Total Bottom-Up TAM** | **[N]** | **$[X] avg** | **$[X]B** |

#### 5. Reconciliation

| Approach | TAM | SAM | SOM | Variance vs. Reconciled |
|---|---|---|---|---|
| Top-Down | $[X]B | $[X]B | $[X]M | [+/-X]% |
| Bottom-Up | $[X]B | $[X]B | $[X]M | [+/-X]% |
| **Reconciled** | **$[X]B** | **$[X]B** | **$[X]M** | — |

**Reconciliation notes**: [Explain why one approach is favored, what drove differences, how you resolved them]

#### 6. Market Growth Projection

| Year | TAM | Growth % | SAM | SOM |
|---|---|---|---|---|
| [Current] | $[X]B | — | $[X]B | $[X]M |
| [+1] | $[X]B | [X]% | $[X]B | $[X]M |
| [+2] | $[X]B | [X]% | $[X]B | $[X]M |
| [+3] | $[X]B | [X]% | $[X]B | $[X]M |
| [+5] | $[X]B | [X]% | $[X]B | $[X]M |

**Growth CAGR ([Current]-[+5])**: TAM [X]% | SAM [X]% | SOM [X]%

**Key growth drivers**:
1. [Driver 1 — quantified impact]
2. [Driver 2 — quantified impact]
3. [Driver 3 — quantified impact]

#### 7. Sensitivity Analysis

**Tornado Chart — Impact on TAM (Base: $[X]B)**

| Variable | Low Case | Base Case | High Case | TAM Range |
|---|---|---|---|---|
| [Variable 1] | [Low] | [Base] | [High] | $[X]B - $[X]B |
| [Variable 2] | [Low] | [Base] | [High] | $[X]B - $[X]B |
| [Variable 3] | [Low] | [Base] | [High] | $[X]B - $[X]B |
| [Variable 4] | [Low] | [Base] | [High] | $[X]B - $[X]B |

**Combined scenario range**: $[Low]B (pessimistic) → $[Base]B (base) → $[High]B (optimistic)

#### 8. Data Sources & Confidence Assessment

| Data Point | Source | Year | Confidence | Risk |
|---|---|---|---|---|
| [Data point 1] | [Source] | [Year] | [H/M/L] | [Key risk to accuracy] |
| [Data point 2] | [Source] | [Year] | [H/M/L] | [Key risk to accuracy] |

#### 9. Key Assumptions & Caveats

1. [Assumption 1 — impact if wrong]
2. [Assumption 2 — impact if wrong]
3. [Assumption 3 — impact if wrong]

---

## Quality Checks

- [ ] TAM, SAM, and SOM are each calculated using BOTH top-down and bottom-up approaches
- [ ] Top-down and bottom-up estimates are reconciled with variance explained
- [ ] Every data point cites a specific source with year
- [ ] Market boundaries (product, geography, customer, value chain) are explicitly defined
- [ ] SAM narrowing from TAM is explained with specific filters and percentages
- [ ] SOM includes realistic penetration assumptions, not aspirational targets
- [ ] Growth projections use driver-based methodology, not just trend extrapolation
- [ ] Sensitivity analysis tests at least 3 key variables with defined ranges
- [ ] Confidence level (High/Medium/Low) is stated for each major estimate
- [ ] Currency, time period, and geographic scope are stated in every table header
- [ ] No circular reasoning (not using own revenue targets to justify market size)
- [ ] Sanity checks applied: per-capita spend, comparison to adjacent markets, public company revenue benchmarks
