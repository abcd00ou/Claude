# Sales Workers — detailed task specs

**Created:** 2026-06-23 · **Team:** Sales

Task spec shape: **Trigger · Sources · Method · Output (payload) · Cadence · Importance · Notes.**
All tasks emit canonical records (shared schema + trust model).

---

## Product Allocator (worker — internal-heavy, public-context only in v1)

### AL-T1 · Customer demand-context tracking
- **Trigger:** quarterly + customer earnings events.
- **Sources:** customer earnings/10-K (capex, stated volume), build-out press.
- **Method:** fetch → snapshot → 2 extractors → cross-check → normalize → status/confidence.
- **Output:** `demand_signal_type ∈ {capex, datacenter_buildout, product_ramp, stated_volume}`
  records by customer/product_family/period.
- **Cadence:** quarterly. **Importance:** high.
- **Notes:** context for "is this allocation ask backed by visible demand?" — NOT an allocation.

### AL-T2 · Allocation-vs-demand reconciliation brief (internal-gated)
- **Trigger:** on allocation-cycle / leader request.
- **Sources:** AL-T1 public demand records + (internal allocation data — NOT accessible in v1).
- **Output:** a brief that pairs public demand context with internal allocation — internal side
  entirely `unverified-needs-human` (`status_reason: license-blocked`/internal) until governance.
- **Cadence:** on-demand. **Importance:** high.
- **Notes:** v1 produces only the public-demand column; the human allocator supplies the rest.

---

## Customer Relation Manager (worker — mixed, strong public half)

### CRM-T1 · Customer account-news watch
- **Trigger:** weekly + event (earnings, announcements).
- **Sources:** customer earnings/IR, press releases, trade press.
- **Output:** `signal_type ∈ {news, earnings, exec_change, product_launch, capex_signal}`
  records by customer.
- **Cadence:** weekly. **Importance:** high.
- **Notes:** rumor without primary citation → `needs-human`.

### CRM-T2 · Pre-meeting customer brief
- **Trigger:** on scheduled customer meeting (meeting-driven).
- **Sources:** CRM-T1 records + the customer's latest public context (no new crawl if fresh).
- **Method:** select usable records for that customer, recency-weighted, into a brief pack the
  Sales leader's customer-meeting deck consumes.
- **Output:** a per-customer brief pack.
- **Cadence:** per meeting. **Importance:** high. `#importance:high`

### CRM-T3 · Customer sentiment digest
- **Trigger:** weekly.
- **Sources:** public commentary, analyst notes on the customer.
- **Output:** `signal_type = sentiment` records (qualitative, source-cited).
- **Cadence:** weekly. **Importance:** medium.
- **Notes:** sentiment is soft — keep tier honest (`analyst`/`other`), most lands lower-confidence.
