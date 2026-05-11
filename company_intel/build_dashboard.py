"""
Dashboard Builder — reads all company JSON profiles and AI_SCM seed data,
inlines everything into a single self-contained HTML file.
Opens with file:// — no server required, no CORS issues.
Chart.js loaded from CDN (internet required for charts; text renders offline).
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from config import TARGET_COMPANIES, DATA_DIR, DASHBOARD_DIR, AI_SCM_SEED


# SCM layer order for sidebar grouping
LAYER_ORDER = ["HBM", "GPU", "ASIC", "Foundry", "Hyperscaler", "Power", "China"]
LAYER_LABELS = {
    "HBM": "HBM Memory",
    "GPU": "GPU",
    "ASIC": "Custom ASIC",
    "Foundry": "Foundry / Packaging",
    "Hyperscaler": "Hyperscalers",
    "Power": "Power & Infrastructure",
    "China": "China AI Supply Chain",
}


def load_profiles() -> list[dict]:
    profiles = []
    for company in TARGET_COMPANIES:
        path = DATA_DIR / f"{company['id']}.json"
        if path.exists():
            try:
                p = json.loads(path.read_text())
                p["_layer"] = company.get("layer", "Other")
                p["_id"] = company["id"]
                profiles.append(p)
            except Exception:
                pass
    return profiles


def load_seed_data() -> dict:
    if not AI_SCM_SEED.exists():
        return {}
    try:
        return json.loads(AI_SCM_SEED.read_text())
    except Exception:
        return {}


def load_hbm_market_share(seed: dict) -> dict:
    return seed.get("hbm_market", {}).get("market_share_annual", {})


def load_hyperscaler_capex(seed: dict) -> dict:
    return seed.get("hyperscaler_capex_usd_bn", {})


def build_html(profiles: list[dict], hbm_share: dict, capex_annual: dict) -> str:
    profiles_json = json.dumps(profiles, ensure_ascii=False)

    # HBM share chart data — latest year
    chart_labels, chart_data, chart_colors = [], [], []
    latest_year = max(
        (k for k in hbm_share if not k.startswith("_")), default=None
    )
    if latest_year:
        year_data = hbm_share[latest_year]
        label_map = {"SK_Hynix": "SK Hynix", "Samsung": "Samsung", "Micron": "Micron"}
        color_map = {"SK_Hynix": "#3182CE", "Samsung": "#1A365D", "Micron": "#E53E3E"}
        for k, label in label_map.items():
            if k in year_data:
                chart_labels.append(label)
                chart_data.append(round(year_data[k] * 100, 1))
                chart_colors.append(color_map.get(k, "#718096"))

    hbm_chart_year = latest_year or "2026E"
    hbm_chart_json = json.dumps({
        "labels": chart_labels,
        "data": chart_data,
        "colors": chart_colors,
        "year": hbm_chart_year,
    })

    # Hyperscaler CapEx trend chart data (latest 4 years)
    capex_chart_labels, capex_chart_datasets = [], []
    capex_companies = ["MSFT", "GOOGL", "AMZN", "META"]
    capex_colors = {"MSFT": "#0078D4", "GOOGL": "#34A853", "AMZN": "#FF9900", "META": "#1877F2"}
    capex_display = {"MSFT": "Microsoft", "GOOGL": "Google", "AMZN": "Amazon", "META": "Meta"}
    if capex_annual:
        all_years = sorted(
            set(y for k in capex_companies for y in capex_annual.get(k, {}) if not y.startswith("_")),
            reverse=True
        )[:5]
        all_years = sorted(all_years)
        capex_chart_labels = all_years
        for k in capex_companies:
            vals = [capex_annual.get(k, {}).get(y) for y in all_years]
            if any(v is not None for v in vals):
                capex_chart_datasets.append({
                    "label": capex_display[k],
                    "data": vals,
                    "borderColor": capex_colors[k],
                    "backgroundColor": capex_colors[k] + "22",
                    "tension": 0.3,
                    "fill": False,
                })

    capex_chart_json = json.dumps({
        "labels": capex_chart_labels,
        "datasets": capex_chart_datasets,
    })

    build_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # Group companies by layer for sidebar
    layers_with_companies = {}
    for company in TARGET_COMPANIES:
        cid = company["id"]
        layer = company.get("layer", "Other")
        if (DATA_DIR / f"{cid}.json").exists():
            layers_with_companies.setdefault(layer, []).append(cid)

    company_ids_by_layer = {
        layer: layers_with_companies.get(layer, [])
        for layer in LAYER_ORDER
        if layer in layers_with_companies
    }

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI SCM Intelligence Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          background: #F7FAFC; color: #1A202C; display: flex; min-height: 100vh; }}

  /* Sidebar */
  #sidebar {{ width: 230px; min-width: 230px; background: #1A202C; padding: 16px 0;
              display: flex; flex-direction: column; overflow-y: auto; }}
  #sidebar .logo {{ color: #63B3ED; font-size: 13px; font-weight: 700;
                    padding: 0 16px 14px; border-bottom: 1px solid #2D3748; letter-spacing: 0.3px; }}
  .layer-label {{ color: #4A5568; font-size: 10px; text-transform: uppercase;
                  letter-spacing: 1px; padding: 14px 16px 4px; }}
  .company-btn {{ display: block; width: 100%; text-align: left; padding: 8px 16px;
                  background: none; border: none; color: #A0AEC0; cursor: pointer;
                  font-size: 13px; transition: all 0.15s; }}
  .company-btn:hover {{ background: #2D3748; color: #E2E8F0; }}
  .company-btn.active {{ background: #2B6CB0; color: white; font-weight: 600; }}
  #build-ts {{ color: #4A5568; font-size: 10px; padding: 12px 16px; margin-top: auto;
               border-top: 1px solid #2D3748; }}

  /* Overview tab */
  .overview-btn {{ display: block; width: 100%; text-align: left; padding: 10px 16px;
                   background: none; border: none; border-bottom: 1px solid #2D3748;
                   color: #68D391; cursor: pointer; font-size: 12px; font-weight: 600;
                   letter-spacing: 0.3px; }}
  .overview-btn:hover, .overview-btn.active {{ background: #276749; color: white; }}

  /* Main */
  #main {{ flex: 1; padding: 24px; overflow-y: auto; }}
  .header-bar {{ display: flex; justify-content: space-between; align-items: center;
                  margin-bottom: 20px; flex-wrap: wrap; gap: 8px; }}
  .company-title {{ font-size: 22px; font-weight: 700; }}
  .ticker {{ font-size: 13px; color: #718096; margin-left: 8px; font-weight: 400; }}
  .layer-badge {{ font-size: 11px; padding: 3px 8px; border-radius: 10px;
                  margin-left: 8px; font-weight: 600; }}
  .badge-HBM {{ background: #BEE3F8; color: #2C5282; }}
  .badge-GPU {{ background: #C6F6D5; color: #22543D; }}
  .badge-ASIC {{ background: #B2F5EA; color: #234E52; }}
  .badge-Foundry {{ background: #FAF089; color: #744210; }}
  .badge-Hyperscaler {{ background: #E9D8FD; color: #44337A; }}
  .badge-Power {{ background: #FED7D7; color: #9B2C2C; }}
  .badge-China {{ background: #FFF5F5; color: #C53030; border: 1px solid #FC8181; }}
  .last-updated {{ font-size: 12px; color: #718096;
                   background: #EDF2F7; padding: 4px 10px; border-radius: 4px; }}

  /* Snapshot grid — adapts to content */
  .snapshot-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
                     gap: 12px; margin-bottom: 16px; }}
  .snap-card {{ background: white; border: 1px solid #E2E8F0; border-radius: 8px;
                padding: 14px 16px; }}
  .snap-val {{ font-size: 18px; font-weight: 700; }}
  .snap-lbl {{ font-size: 11px; color: #718096; margin-top: 3px; }}

  /* Cards */
  .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }}
  .card {{ background: white; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; }}
  .card h3 {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;
               color: #718096; margin-bottom: 10px; }}

  /* SCM chain graphic */
  .scm-chain {{ display: flex; align-items: center; gap: 0; margin-bottom: 20px;
                background: white; border: 1px solid #E2E8F0; border-radius: 8px;
                padding: 16px; overflow-x: auto; }}
  .scm-node {{ text-align: center; min-width: 120px; cursor: pointer; }}
  .scm-node .icon {{ font-size: 24px; }}
  .scm-node .node-name {{ font-size: 11px; font-weight: 600; color: #2D3748; margin-top: 4px; }}
  .scm-node .node-role {{ font-size: 10px; color: #718096; }}
  .scm-arrow {{ color: #CBD5E0; font-size: 20px; margin: 0 4px; flex-shrink: 0; }}
  .scm-group {{ text-align: center; }}
  .scm-group-label {{ font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px;
                      color: #718096; margin-bottom: 6px; }}
  .scm-group-nodes {{ display: flex; gap: 4px; }}

  /* Sales hooks */
  .hook {{ background: #EBF8FF; border-left: 3px solid #3182CE;
           padding: 10px 14px; margin-bottom: 8px; border-radius: 0 4px 4px 0;
           font-size: 13px; line-height: 1.5; }}

  /* Roadmap table */
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{ background: #F7FAFC; text-align: left; padding: 8px 12px;
        font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;
        color: #718096; border-bottom: 2px solid #E2E8F0; }}
  td {{ padding: 9px 12px; border-bottom: 1px solid #F0F0F0; vertical-align: top; }}
  tr:last-child td {{ border-bottom: none; }}
  .status-badge {{ display: inline-block; padding: 2px 8px; border-radius: 10px;
                    font-size: 11px; font-weight: 600; }}
  .status-mass_production {{ background: #C6F6D5; color: #22543D; }}
  .status-sampling {{ background: #FEFCBF; color: #744210; }}
  .status-sampling_2026H2 {{ background: #FEFCBF; color: #744210; }}
  .status-development {{ background: #E2E8F0; color: #4A5568; }}
  .status-deployed {{ background: #BEE3F8; color: #2C5282; }}
  .status-ga {{ background: #C6F6D5; color: #22543D; }}
  .status-ramping {{ background: #FAF089; color: #744210; }}
  .status-construction {{ background: #FBD38D; color: #7B341E; }}
  .status-mass_production_2025 {{ background: #C6F6D5; color: #22543D; }}

  /* News */
  .news-item {{ display: flex; gap: 10px; padding: 8px 0;
                border-bottom: 1px solid #F0F0F0; align-items: flex-start; }}
  .news-item:last-child {{ border-bottom: none; }}
  .news-date {{ font-size: 11px; color: #718096; white-space: nowrap; min-width: 72px; }}
  .news-title a {{ color: #2B6CB0; text-decoration: none; font-size: 13px;
                    line-height: 1.4; display: block; }}
  .news-title a:hover {{ text-decoration: underline; }}
  .news-source {{ font-size: 11px; color: #718096; margin-top: 2px; }}
  .flagged-badge {{ background: #FED7D7; color: #9B2C2C; font-size: 10px;
                     padding: 1px 6px; border-radius: 3px; margin-left: 6px; }}

  /* Competitive */
  .comp-item {{ margin-bottom: 8px; font-size: 13px; line-height: 1.5; }}
  .comp-label {{ font-weight: 600; color: #4A5568; margin-bottom: 2px; font-size: 11px;
                 text-transform: uppercase; letter-spacing: 0.3px; }}

  /* Charts */
  .chart-container {{ position: relative; height: 200px; }}
  .empty-state {{ color: #718096; font-size: 13px; font-style: italic; padding: 8px 0; }}

  /* Lead time pipeline */
  .pipeline {{ display: flex; align-items: stretch; gap: 0; overflow-x: auto; margin-bottom: 12px; }}
  .pipe-stage {{ flex: 1; min-width: 110px; padding: 10px 8px; background: #F7FAFC;
                 border: 1px solid #E2E8F0; text-align: center; position: relative; }}
  .pipe-stage:not(:last-child)::after {{ content: '→'; position: absolute; right: -13px; top: 50%;
    transform: translateY(-50%); color: #CBD5E0; font-size: 18px; z-index: 1; }}
  .pipe-stage:not(:first-child) {{ border-left: none; }}
  .pipe-stage.bottleneck {{ background: #FFF5F5; border-color: #FC8181; border-width: 2px; }}
  .pipe-stage .ps-stage {{ font-size: 11px; font-weight: 600; color: #2D3748; margin-bottom: 4px; line-height: 1.3; }}
  .pipe-stage .ps-weeks {{ font-size: 16px; font-weight: 700; color: #3182CE; }}
  .pipe-stage.bottleneck .ps-weeks {{ color: #E53E3E; }}
  .pipe-stage .ps-unit {{ font-size: 10px; color: #718096; }}
  .pipe-stage .ps-owner {{ font-size: 10px; color: #718096; margin-top: 3px; background: #EDF2F7;
                            padding: 2px 5px; border-radius: 3px; display: inline-block; }}
  .pipe-stage.bottleneck .ps-owner {{ background: #FED7D7; color: #9B2C2C; }}

  /* Event timeline */
  .timeline-list {{ list-style: none; padding: 0; position: relative; }}
  .timeline-list::before {{ content: ''; position: absolute; left: 72px; top: 0; bottom: 0;
                             width: 2px; background: #E2E8F0; }}
  .tl-item {{ display: flex; gap: 0; align-items: flex-start; margin-bottom: 10px; position: relative; }}
  .tl-date {{ min-width: 62px; font-size: 11px; color: #718096; padding-top: 2px; text-align: right; padding-right: 10px; }}
  .tl-dot {{ width: 10px; height: 10px; border-radius: 50%; margin-top: 4px; flex-shrink: 0; z-index: 1; }}
  .tl-body {{ padding-left: 10px; font-size: 13px; line-height: 1.4; flex: 1; }}
  .tl-cat {{ font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px;
              padding: 1px 5px; border-radius: 3px; margin-left: 6px; vertical-align: middle; }}
  .cat-product {{ color: #2C5282; background: #BEE3F8; }}
  .cat-financial {{ color: #22543D; background: #C6F6D5; }}
  .cat-capacity {{ color: #744210; background: #FEFCBF; }}
  .cat-risk {{ color: #9B2C2C; background: #FED7D7; }}
  .cat-org {{ color: #4A5568; background: #E2E8F0; }}
  .cat-strategy {{ color: #44337A; background: #E9D8FD; }}
  .dot-product {{ background: #3182CE; }}
  .dot-financial {{ background: #38A169; }}
  .dot-capacity {{ background: #D69E2E; }}
  .dot-risk {{ background: #E53E3E; }}
  .dot-org {{ background: #718096; }}
  .dot-strategy {{ background: #805AD5; }}
  .sig-high {{ font-weight: 600; }}

  /* Global timeline filter */
  .tl-filter-bar {{ display: flex; flex-wrap: wrap; gap: 6px; margin-bottom: 14px; }}
  .tl-filter-btn {{ padding: 4px 10px; border: 1px solid #E2E8F0; border-radius: 12px;
                    background: white; font-size: 11px; cursor: pointer; color: #4A5568; }}
  .tl-filter-btn.active {{ background: #2B6CB0; color: white; border-color: #2B6CB0; }}
  .global-tl-item {{ display: flex; gap: 8px; padding: 8px 0; border-bottom: 1px solid #F0F0F0;
                     align-items: flex-start; }}
  .global-tl-item:last-child {{ border-bottom: none; }}
  .gtl-date {{ min-width: 62px; font-size: 11px; color: #718096; white-space: nowrap; padding-top:2px; }}
  .gtl-company {{ min-width: 110px; font-size: 11px; font-weight: 600; color: #2D3748; padding-top:2px; }}
  .gtl-body {{ flex: 1; font-size: 13px; line-height: 1.4; }}

  /* Overview table */
  .overview-table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  .overview-table th {{ background: #F7FAFC; text-align: left; padding: 10px 12px;
        font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;
        color: #718096; border-bottom: 2px solid #E2E8F0; }}
  .overview-table td {{ padding: 10px 12px; border-bottom: 1px solid #F0F0F0; vertical-align: top; }}
  .overview-table tr:hover td {{ background: #F7FAFC; }}
  .clickable {{ cursor: pointer; color: #2B6CB0; font-weight: 600; }}
  .clickable:hover {{ text-decoration: underline; }}
</style>
</head>
<body>

<div id="sidebar">
  <div class="logo">AI SCM Intelligence</div>
  <button class="overview-btn" id="overview-btn" onclick="showOverview()">Supply Chain Overview</button>
  <div id="company-nav"></div>
  <div id="build-ts">Built {build_ts}</div>
</div>

<div id="main">
  <div id="content"></div>
</div>

<script>
const PROFILES = {profiles_json};
const HBM_CHART = {hbm_chart_json};
const CAPEX_CHART = {capex_chart_json};
const LAYERS_WITH_COMPANIES = {json.dumps(company_ids_by_layer)};
const LAYER_LABELS = {json.dumps(LAYER_LABELS)};

let activeId = null;
let revenueChart = null;
let hbmPieChart = null;
let capexLineChart = null;

function getProfile(id) {{
  return PROFILES.find(p => p._id === id) || PROFILES[0];
}}

function statusClass(s) {{
  if (!s) return 'status-development';
  return 'status-' + s.replace(/[^a-z0-9_]/gi, '_');
}}

function renderSnapshot(profile) {{
  const s = profile.snapshot || {{}};
  const layer = profile._layer;
  let items = [];

  if (layer === 'HBM') {{
    items = [
      {{ val: s.revenue_qtr || '—', lbl: 'Latest Revenue' }},
      {{ val: s.op_margin_pct != null ? s.op_margin_pct + '%' : '—', lbl: 'Operating Margin' }},
      {{ val: s.hbm_market_share_pct != null ? s.hbm_market_share_pct + '%' : '—', lbl: 'HBM Market Share' }},
      {{ val: s.headcount ? s.headcount.toLocaleString() : '—', lbl: 'Headcount' }},
    ];
  }} else if (layer === 'GPU') {{
    items = [
      {{ val: s.revenue_qtr || '—', lbl: 'Latest Revenue' }},
      {{ val: s.datacenter_revenue_qtr_usd || '—', lbl: 'Datacenter Revenue' }},
      {{ val: s.op_margin_pct != null ? s.op_margin_pct + '%' : '—', lbl: 'Operating Margin' }},
      {{ val: s.market_cap_usd_bn ? '$' + s.market_cap_usd_bn + 'B' : '—', lbl: 'Market Cap' }},
    ];
  }} else if (layer === 'Foundry') {{
    items = [
      {{ val: s.revenue_qtr || '—', lbl: 'Latest Revenue' }},
      {{ val: s.op_margin_pct != null ? s.op_margin_pct + '%' : '—', lbl: 'Operating Margin' }},
      {{ val: s.headcount ? s.headcount.toLocaleString() : '—', lbl: 'Headcount' }},
      {{ val: s.market_cap_usd_bn ? '$' + s.market_cap_usd_bn + 'B' : '—', lbl: 'Market Cap' }},
    ];
  }} else if (layer === 'ASIC') {{
    items = [
      {{ val: s.revenue_qtr || '—', lbl: 'Latest Revenue' }},
      {{ val: s.ai_revenue_qtr_usd || s.datacenter_revenue_qtr_usd || '—', lbl: 'AI Revenue' }},
      {{ val: s.op_margin_pct != null ? s.op_margin_pct + '%' : '—', lbl: 'Operating Margin' }},
      {{ val: s.market_cap_usd_bn ? '$' + s.market_cap_usd_bn + 'B' : '—', lbl: 'Market Cap' }},
    ];
  }} else if (layer === 'Power') {{
    items = [
      {{ val: s.revenue_qtr || '—', lbl: 'Latest Revenue' }},
      {{ val: s.op_margin_pct != null ? s.op_margin_pct + '%' : '—', lbl: 'Operating Margin' }},
      {{ val: s.nuclear_capacity_gw ? s.nuclear_capacity_gw + ' GW' : (s.headcount ? s.headcount.toLocaleString() : '—'), lbl: s.nuclear_capacity_gw ? 'Nuclear Capacity' : 'Headcount' }},
      {{ val: s.market_cap_usd_bn ? '$' + s.market_cap_usd_bn + 'B' : '—', lbl: 'Market Cap' }},
    ];
  }} else if (layer === 'China') {{
    items = [
      {{ val: s.revenue_qtr || '—', lbl: 'Latest Revenue' }},
      {{ val: s.op_margin_pct != null ? s.op_margin_pct + '%' : '—', lbl: 'Operating Margin' }},
      {{ val: s.hbm_china_market_share_pct != null ? s.hbm_china_market_share_pct + '%' : (s.headcount ? s.headcount.toLocaleString() : '—'), lbl: s.hbm_china_market_share_pct != null ? 'China HBM Share' : 'Headcount' }},
      {{ val: s.cloud_ai_revenue_2025_usd || '—', lbl: 'AI Revenue Est.' }},
    ];
  }} else {{
    // Hyperscaler
    items = [
      {{ val: s.revenue_qtr || '—', lbl: 'Latest Revenue' }},
      {{ val: s.capex_qtr_usd || '—', lbl: 'Q CapEx' }},
      {{ val: s.capex_2026_guidance_usd ? '$' + s.capex_2026_guidance_usd + 'B' : '—', lbl: '2026 CapEx Guide' }},
      {{ val: s.market_cap_usd_bn ? '$' + s.market_cap_usd_bn + 'B' : '—', lbl: 'Market Cap' }},
    ];
  }}
  return `<div class="snapshot-grid">${{items.map(i =>
    `<div class="snap-card"><div class="snap-val">${{i.val}}</div><div class="snap-lbl">${{i.lbl}}</div></div>`
  ).join('')}}</div>`;
}}

function renderRoadmap(profile) {{
  const items = profile.product_roadmap || [];
  if (!items.length) return '<p class="empty-state">No roadmap data yet.</p>';
  const layer = profile._layer;

  if (layer === 'HBM') {{
    return `<table>
      <tr><th>Product</th><th>Status</th><th>Customer</th><th>BW (TB/s)</th><th>Notes</th></tr>
      ${{items.map(r => `<tr>
        <td><strong>${{r.product}}</strong></td>
        <td><span class="status-badge ${{statusClass(r.status)}}">${{(r.status||'').replace(/_/g,' ')}}</span></td>
        <td>${{r.customer || '—'}}</td>
        <td>${{r.bandwidth_tbps || '—'}}</td>
        <td>${{r.note || '—'}}</td>
      </tr>`).join('')}}
    </table>`;
  }} else if (layer === 'GPU') {{
    return `<table>
      <tr><th>Product</th><th>Status</th><th>HBM Supplier</th><th>HBM/GPU (GB)</th><th>Notes</th></tr>
      ${{items.map(r => `<tr>
        <td><strong>${{r.product}}</strong></td>
        <td><span class="status-badge ${{statusClass(r.status)}}">${{(r.status||'').replace(/_/g,' ')}}</span></td>
        <td>${{r.hbm_supplier || '—'}}</td>
        <td>${{r.hbm_per_gpu_gb || '—'}}</td>
        <td>${{r.note || '—'}}</td>
      </tr>`).join('')}}
    </table>`;
  }} else if (layer === 'Foundry') {{
    return `<table>
      <tr><th>Product</th><th>Status</th><th>Capacity (WPM)</th><th>Notes</th></tr>
      ${{items.map(r => `<tr>
        <td><strong>${{r.product}}</strong></td>
        <td><span class="status-badge ${{statusClass(r.status)}}">${{(r.status||'').replace(/_/g,' ')}}</span></td>
        <td>${{r.capacity_wpm ? r.capacity_wpm.toLocaleString() : '—'}}</td>
        <td>${{r.note || '—'}}</td>
      </tr>`).join('')}}
    </table>`;
  }} else {{
    // Hyperscaler / ASIC / Power / China — generic table with HBM supplier or customer column
    const hasHbm = items.some(r => r.hbm_supplier);
    const hasCust = items.some(r => r.customer);
    const col3label = hasHbm ? 'HBM Supplier' : (hasCust ? 'Customer' : 'Details');
    const col3val = r => r.hbm_supplier || r.customer || r.note || '—';
    return `<table>
      <tr><th>Product / Program</th><th>Status</th><th>${{col3label}}</th><th>Notes</th></tr>
      ${{items.map(r => `<tr>
        <td><strong>${{r.product}}</strong></td>
        <td><span class="status-badge ${{statusClass(r.status)}}">${{(r.status||'').replace(/_/g,' ')}}</span></td>
        <td>${{col3val(r)}}</td>
        <td>${{r.note || '—'}}</td>
      </tr>`).join('')}}
    </table>`;
  }}
}}

function renderScmEngagement(profile) {{
  const eng = profile.scm_engagement;
  if (!eng) return '<p class="empty-state">No SCM detail yet.</p>';

  // Server products table
  const prods = eng.server_products || [];
  const prodRows = prods.map(p => {{
    const extra = p.hbm || p.bandwidth || p.output || p.process || p.cooling_capacity || '';
    return `<tr>
      <td><strong>${{p.name}}</strong></td>
      <td><span style="font-size:11px;color:#4A5568">${{p.type}}</span></td>
      <td style="font-size:12px">${{p.used_in || '—'}}</td>
      <td style="font-size:12px;color:#2B6CB0">${{extra || '—'}}</td>
      <td style="font-size:12px">${{p.note || '—'}}</td>
    </tr>`;
  }}).join('');

  // Upstream / downstream
  const up = (eng.upstream_from || []).map(x => `<span style="background:#FED7D7;color:#9B2C2C;padding:2px 7px;border-radius:10px;font-size:11px;margin:2px;display:inline-block">${{x}}</span>`).join(' ');
  const dn = (eng.downstream_to || []).map(x => `<span style="background:#C6F6D5;color:#22543D;padding:2px 7px;border-radius:10px;font-size:11px;margin:2px;display:inline-block">${{x}}</span>`).join(' ');

  return `
    <div style="background:#EBF8FF;border-left:3px solid #3182CE;padding:10px 14px;border-radius:0 4px 4px 0;font-size:13px;line-height:1.6;margin-bottom:12px">
      ${{eng.scm_role || ''}}
    </div>
    <div style="margin-bottom:6px;font-size:11px;color:#718096;text-transform:uppercase;letter-spacing:0.5px">SCM Position</div>
    <div style="background:#F7FAFC;padding:6px 10px;border-radius:4px;font-size:12px;margin-bottom:12px;font-weight:600;color:#2D3748">${{eng.scm_position || '—'}}</div>

    <div style="margin-bottom:6px;font-size:11px;color:#718096;text-transform:uppercase;letter-spacing:0.5px">Upstream Dependencies</div>
    <div style="margin-bottom:12px">${{up || '<span style="color:#718096;font-size:12px">—</span>'}}</div>

    <div style="margin-bottom:6px;font-size:11px;color:#718096;text-transform:uppercase;letter-spacing:0.5px">Downstream Customers</div>
    <div style="margin-bottom:16px">${{dn || '<span style="color:#718096;font-size:12px">—</span>'}}</div>

    <div style="margin-bottom:8px;font-size:11px;color:#718096;text-transform:uppercase;letter-spacing:0.5px">Server-Level Products (${{prods.length}})</div>
    <table>
      <tr><th>Product</th><th>Type</th><th>Used In</th><th>Key Spec</th><th>Notes</th></tr>
      ${{prodRows || '<tr><td colspan="5" style="color:#718096;font-style:italic">No server products listed yet.</td></tr>'}}
    </table>
  `;
}}

function renderLeadTime(profile) {{
  const lt = profile.lead_time;
  if (!lt) return '';
  const pipeline = lt.pipeline || [];
  const bottleneck = (lt.bottleneck || '').toLowerCase();

  const stageHtml = pipeline.map(s => {{
    const isBottleneck = bottleneck.toLowerCase().includes(s.stage.split(' ')[0].toLowerCase()) ||
                         bottleneck.includes(s.owner ? s.owner.toLowerCase() : '___');
    return `<div class="pipe-stage${{isBottleneck ? ' bottleneck' : ''}}">
      <div class="ps-stage">${{s.stage}}</div>
      <div class="ps-weeks">${{s.weeks}}</div>
      <div class="ps-unit">weeks</div>
      <div class="ps-owner">${{s.owner || ''}}</div>
    </div>`;
  }}).join('');

  return `
    <div style="margin-bottom:10px">
      <span style="font-size:22px;font-weight:700;color:#2D3748">${{lt.total_months_to_token}}</span>
      <span style="font-size:12px;color:#718096;margin-left:4px">months: action → AI tokens served</span>
      ${{lt.bottleneck ? `<div style="margin-top:6px;font-size:12px;background:#FFF5F5;border-left:3px solid #FC8181;padding:6px 10px;border-radius:0 4px 4px 0;color:#9B2C2C">⚠ Bottleneck: ${{lt.bottleneck}}</div>` : ''}}
      ${{lt.description ? `<div style="margin-top:6px;font-size:12px;color:#718096;line-height:1.5">${{lt.description}}</div>` : ''}}
    </div>
    <div class="pipeline">${{stageHtml}}</div>
  `;
}}

function renderTimeline(profile) {{
  const events = (profile.key_events || []).slice().sort((a, b) => a.date.localeCompare(b.date));
  if (!events.length) return '<p class="empty-state">No events yet.</p>';
  const items = events.map(e => {{
    const cat = e.category || 'product';
    const sig = e.significance === 'high' ? ' sig-high' : '';
    return `<li class="tl-item">
      <div class="tl-date">${{e.date}}</div>
      <div class="tl-dot dot-${{cat}}"></div>
      <div class="tl-body${{sig}}">${{e.event}}<span class="tl-cat cat-${{cat}}">${{cat}}</span></div>
    </li>`;
  }}).join('');
  return `<ul class="timeline-list">${{items}}</ul>`;
}}

function renderHooks(profile) {{
  const hooks = profile.sales_hooks || [];
  if (!hooks.length) return '<p class="empty-state">No sales hooks yet.</p>';
  return hooks.map(h => `<div class="hook">${{h}}</div>`).join('');
}}

function renderNews(profile) {{
  const news = profile.recent_news || [];
  const flagged = new Set((profile.flagged_news || []).map(f => f.title));
  if (!news.length) return '<p class="empty-state">No news collected yet. Run <code>python run.py</code> to fetch.</p>';
  return news.slice(0, 8).map(n => {{
    const isFlagged = flagged.has(n.title);
    return `<div class="news-item">
      <div class="news-date">${{n.date}}</div>
      <div class="news-title">
        <a href="${{n.url}}" target="_blank" rel="noopener">${{n.title}}${{isFlagged ? '<span class="flagged-badge">★ relevant</span>' : ''}}</a>
        <div class="news-source">${{n.source}}</div>
      </div>
    </div>`;
  }}).join('');
}}

function renderCompetitive(profile) {{
  const c = profile.competitive_position || {{}};
  const entries = Object.entries(c).filter(([k]) => !k.startsWith('_'));
  if (!entries.length) return '<p class="empty-state">No competitive data yet.</p>';
  return entries.map(([k, v]) =>
    `<div class="comp-item"><div class="comp-label">${{k.replace(/_/g,' ')}}</div>${{v}}</div>`
  ).join('');
}}

function renderCharts(profile) {{
  const hist = profile.financials_history || {{}};
  const layer = profile._layer;

  // Revenue / CapEx trend chart
  let quarters = Object.entries(hist)
    .filter(([k]) => !k.startsWith('_'))
    .sort(([a],[b]) => a.localeCompare(b));

  if (quarters.length > 1) {{
    const ctx = document.getElementById('revenueChart');
    if (ctx) {{
      if (revenueChart) revenueChart.destroy();
      const cleanLabel = k => k
        .replace(/_revenue_krw_t$/,'').replace(/_revenue_nt_bn$/,'')
        .replace(/_revenue_usd_bn$/,'').replace(/_capex_usd_bn$/,'')
        .replace(/_dc_revenue_usd_bn$/,'').replace(/_ds_revenue_krw_t$/,'')
        .replace(/_ds_revenue_krw_t_est$/,' est').replace(/^_/,'');
      const isCapex = layer === 'Hyperscaler';
      revenueChart = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: quarters.map(([k]) => cleanLabel(k)),
          datasets: [{{ label: isCapex ? 'CapEx' : 'Revenue',
            data: quarters.map(([,v]) => v),
            backgroundColor: isCapex ? '#9F7AEA' : '#3182CE', borderRadius: 4 }}]
        }},
        options: {{ responsive: true, maintainAspectRatio: false,
          plugins: {{ legend: {{ display: false }} }},
          scales: {{ y: {{ beginAtZero: false }} }} }}
      }});
    }}
  }}

  // HBM market share pie (for HBM layer)
  if (layer === 'HBM' && HBM_CHART.data.length) {{
    const pieCtx = document.getElementById('hbmPieChart');
    if (pieCtx) {{
      if (hbmPieChart) hbmPieChart.destroy();
      hbmPieChart = new Chart(pieCtx, {{
        type: 'doughnut',
        data: {{
          labels: HBM_CHART.labels,
          datasets: [{{ data: HBM_CHART.data, backgroundColor: HBM_CHART.colors, borderWidth: 2 }}]
        }},
        options: {{ responsive: true, maintainAspectRatio: false, cutout: '60%',
          plugins: {{ legend: {{ position: 'right', labels: {{ font: {{ size: 11 }} }} }} }} }}
      }});
    }}
  }}

  // Hyperscaler CapEx comparison line chart
  if (layer === 'Hyperscaler' && CAPEX_CHART.datasets && CAPEX_CHART.datasets.length) {{
    const lineCtx = document.getElementById('capexLineChart');
    if (lineCtx) {{
      if (capexLineChart) capexLineChart.destroy();
      capexLineChart = new Chart(lineCtx, {{
        type: 'line',
        data: CAPEX_CHART,
        options: {{ responsive: true, maintainAspectRatio: false,
          plugins: {{ legend: {{ position: 'bottom', labels: {{ font: {{ size: 11 }} }} }} }},
          scales: {{ y: {{ beginAtZero: true, title: {{ display: true, text: 'CapEx ($B)' }} }} }} }}
      }});
    }}
  }}
}}

function render(id) {{
  activeId = id;
  const profile = getProfile(id);
  const hist = profile.financials_history || {{}};
  const hasRevChart = Object.keys(hist).filter(k=>!k.startsWith('_')).length > 1;
  const isHBM = profile._layer === 'HBM';
  const isHyperscaler = profile._layer === 'Hyperscaler';

  document.getElementById('content').innerHTML = `
    <div class="header-bar">
      <div>
        <span class="company-title">${{profile.company}}</span>
        <span class="ticker">${{profile.ticker || ''}}</span>
        <span class="layer-badge badge-${{profile._layer}}">${{profile._layer}}</span>
      </div>
      <div class="last-updated">Last updated: ${{profile.last_updated || 'N/A'}}</div>
    </div>

    ${{renderSnapshot(profile)}}

    <div class="card" style="margin-bottom:16px">
      <h3>SCM Engagement — Role, Products & Dependencies</h3>
      ${{renderScmEngagement(profile)}}
    </div>

    ${{profile.lead_time ? `<div class="card" style="margin-bottom:16px">
      <h3>Lead Time to AI Token Throughput</h3>
      ${{renderLeadTime(profile)}}
    </div>` : ''}}

    ${{profile.key_events && profile.key_events.length ? `<div class="card" style="margin-bottom:16px">
      <h3>Company Timeline — Key Events</h3>
      ${{renderTimeline(profile)}}
    </div>` : ''}}

    <div class="grid-2" style="margin-bottom:16px">
      <div class="card" style="grid-column: span 2">
        <h3>Sales Hooks — Conversation Starters</h3>
        ${{renderHooks(profile)}}
      </div>
    </div>

    <div class="grid-2" style="margin-bottom:16px">
      <div class="card">
        <h3>Product Roadmap</h3>
        ${{renderRoadmap(profile)}}
      </div>
      <div class="card">
        <h3>Competitive Position</h3>
        ${{renderCompetitive(profile)}}
      </div>
    </div>

    <div class="grid-2" style="margin-bottom:16px">
      ${{hasRevChart ? `<div class="card">
        <h3>${{isHyperscaler ? 'CapEx Trend' : 'Revenue Trend'}}</h3>
        <div class="chart-container"><canvas id="revenueChart"></canvas></div>
      </div>` : ''}}
      ${{isHBM && HBM_CHART.data.length ? `<div class="card">
        <h3>HBM Market Share (${{HBM_CHART.year}})</h3>
        <div class="chart-container"><canvas id="hbmPieChart"></canvas></div>
      </div>` : ''}}
      ${{isHyperscaler && CAPEX_CHART.datasets && CAPEX_CHART.datasets.length ? `<div class="card">
        <h3>Hyperscaler CapEx Comparison ($B)</h3>
        <div class="chart-container"><canvas id="capexLineChart"></canvas></div>
      </div>` : ''}}
    </div>

    <div class="card">
      <h3>Recent News</h3>
      ${{renderNews(profile)}}
    </div>
  `;

  setTimeout(() => renderCharts(profile), 0);
}}

function showOverview() {{
  activeId = '__overview__';
  document.querySelectorAll('.company-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('overview-btn').classList.add('active');

  // Build overview table rows grouped by layer
  const rows = [];
  for (const [layer, ids] of Object.entries(LAYERS_WITH_COMPANIES)) {{
    ids.forEach(id => {{
      const p = getProfile(id);
      if (!p) return;
      const s = p.snapshot || {{}};
      const isHBM = p._layer === 'HBM';
      const isHyperscaler = p._layer === 'Hyperscaler';
      const lt = p.lead_time;
      rows.push(`<tr>
        <td><span class="clickable" onclick="selectCompany('${{id}}')">${{p.company}}</span></td>
        <td><span class="layer-badge badge-${{p._layer}}">${{p._layer}}</span></td>
        <td>${{s.revenue_qtr || '—'}}</td>
        <td>${{isHBM ? (s.hbm_market_share_pct != null ? s.hbm_market_share_pct + '%' : '—') :
              isHyperscaler ? (s.capex_qtr_usd || '—') : '—'}}</td>
        <td>${{s.op_margin_pct != null ? s.op_margin_pct + '%' : '—'}}</td>
        <td>${{lt ? `<span style="font-weight:600;color:${{lt.total_months_to_token<=6?'#22543D':lt.total_months_to_token<=18?'#744210':'#9B2C2C'}}">${{lt.total_months_to_token}}mo</span>` : '—'}}</td>
        <td>${{p.last_updated || '—'}}</td>
      </tr>`);
    }});
  }}

  document.getElementById('content').innerHTML = `
    <div class="header-bar">
      <div><span class="company-title">AI Supply Chain Overview</span></div>
    </div>

    <div class="card" style="margin-bottom:16px; padding: 20px 24px; overflow-x:auto;">
      <h3 style="margin-bottom:16px">AI Supply Chain Flow</h3>

      <div style="display:flex; gap:16px; align-items:flex-start; min-width:900px;">

        <!-- Power layer (vertical) -->
        <div style="display:flex; flex-direction:column; gap:4px; align-items:center;">
          <div style="font-size:10px; color:#718096; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">Power</div>
          <div style="padding:7px 10px; background:#FED7D7; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600; text-align:center" onclick="selectCompany('constellation_energy')">Constellation<br><span style="font-weight:400;color:#718096">Nuclear</span></div>
          <div style="padding:7px 10px; background:#FED7D7; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600; text-align:center" onclick="selectCompany('ge_vernova')">GE Vernova<br><span style="font-weight:400;color:#718096">Grid/Gas</span></div>
          <div style="padding:7px 10px; background:#FED7D7; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600; text-align:center" onclick="selectCompany('vertiv')">Vertiv<br><span style="font-weight:400;color:#718096">Power/Cool</span></div>
        </div>

        <div style="color:#CBD5E0; font-size:18px; padding-top:40px;">⬇</div>

        <!-- Hyperscalers -->
        <div style="display:flex; flex-direction:column; gap:4px; align-items:center;">
          <div style="font-size:10px; color:#718096; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">Hyperscalers</div>
          <div style="display:flex; gap:4px;">
            <div style="padding:7px 10px; background:#E9D8FD; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600; text-align:center" onclick="selectCompany('microsoft')">MSFT</div>
            <div style="padding:7px 10px; background:#E9D8FD; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600; text-align:center" onclick="selectCompany('google')">GOOGL</div>
            <div style="padding:7px 10px; background:#E9D8FD; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600; text-align:center" onclick="selectCompany('amazon')">AMZN</div>
            <div style="padding:7px 10px; background:#E9D8FD; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600; text-align:center" onclick="selectCompany('meta')">META</div>
          </div>
          <div style="font-size:10px; color:#718096; margin-top:2px;">$710B+ CapEx 2026</div>
        </div>

        <div style="color:#CBD5E0; font-size:18px; padding-top:30px;">→</div>

        <!-- GPU + ASIC split -->
        <div style="display:flex; flex-direction:column; gap:8px;">
          <div style="display:flex; flex-direction:column; gap:4px; align-items:center;">
            <div style="font-size:10px; color:#718096; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">GPU</div>
            <div style="padding:8px 14px; background:#C6F6D5; border-radius:6px; cursor:pointer; font-size:12px; font-weight:700" onclick="selectCompany('nvidia')">NVIDIA</div>
            <div style="padding:6px 10px; background:#C6F6D5; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600" onclick="selectCompany('amd')">AMD</div>
          </div>
          <div style="display:flex; flex-direction:column; gap:4px; align-items:center;">
            <div style="font-size:10px; color:#718096; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">Custom ASIC</div>
            <div style="padding:6px 10px; background:#B2F5EA; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600" onclick="selectCompany('broadcom')">Broadcom</div>
            <div style="padding:6px 10px; background:#B2F5EA; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600" onclick="selectCompany('marvell')">Marvell</div>
          </div>
        </div>

        <div style="color:#CBD5E0; font-size:18px; padding-top:30px;">→</div>

        <!-- Foundry / Packaging -->
        <div style="display:flex; flex-direction:column; gap:4px; align-items:center;">
          <div style="font-size:10px; color:#718096; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">Foundry</div>
          <div style="padding:8px 14px; background:#FAF089; border-radius:6px; cursor:pointer; font-size:12px; font-weight:700" onclick="selectCompany('tsmc')">TSMC<br><span style="font-size:10px; font-weight:400; color:#718096">CoWoS 95%</span></div>
        </div>

        <div style="color:#CBD5E0; font-size:18px; padding-top:30px;">→</div>

        <!-- HBM Suppliers -->
        <div style="display:flex; flex-direction:column; gap:4px; align-items:center;">
          <div style="font-size:10px; color:#718096; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:4px;">HBM Memory</div>
          <div style="padding:8px 12px; background:#BEE3F8; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600; text-align:center" onclick="selectCompany('sk_hynix')">SK Hynix<br><span style="font-weight:400;color:#2C5282">50%</span></div>
          <div style="padding:8px 12px; background:#BEE3F8; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600; text-align:center" onclick="selectCompany('samsung_semiconductor')">Samsung<br><span style="font-weight:400;color:#2C5282">35%</span></div>
          <div style="padding:8px 12px; background:#BEE3F8; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600; text-align:center" onclick="selectCompany('micron')">Micron<br><span style="font-weight:400;color:#2C5282">15%</span></div>
        </div>

        <!-- China parallel chain -->
        <div style="border-left: 2px dashed #FC8181; padding-left:16px; margin-left:8px;">
          <div style="font-size:10px; color:#FC8181; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:8px; font-weight:700;">🇨🇳 China Alt Chain</div>
          <div style="display:flex; flex-direction:column; gap:4px;">
            <div style="padding:7px 10px; background:#FFF5F5; border:1px solid #FC8181; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600; text-align:center" onclick="selectCompany('huawei')">Huawei<br><span style="font-size:10px;color:#718096">Ascend (GPU)</span></div>
            <div style="padding:7px 10px; background:#FFF5F5; border:1px solid #FC8181; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600; text-align:center" onclick="selectCompany('smic')">SMIC<br><span style="font-size:10px;color:#718096">Foundry</span></div>
            <div style="padding:7px 10px; background:#FFF5F5; border:1px solid #FC8181; border-radius:6px; cursor:pointer; font-size:11px; font-weight:600; text-align:center" onclick="selectCompany('cxmt')">CXMT<br><span style="font-size:10px;color:#718096">HBM Alt</span></div>
          </div>
        </div>

      </div>
    </div>

    <div class="card" style="margin-bottom:16px">
      <h3 style="margin-bottom:12px">All Companies</h3>
      <table class="overview-table">
        <tr>
          <th>Company</th><th>Layer</th><th>Latest Revenue</th>
          <th>HBM Share / Q CapEx</th><th>Op Margin</th><th>Months→Token</th><th>Updated</th>
        </tr>
        ${{rows.join('')}}
      </table>
    </div>

    <div class="card" id="global-timeline-card">
      <h3 style="margin-bottom:12px">Global Supply Chain Timeline — 2023–2026</h3>
      <div class="tl-filter-bar" id="gtl-filters"></div>
      <div id="gtl-events" style="max-height:520px;overflow-y:auto;"></div>
    </div>
  `;

  // Build global timeline
  (function() {{
    const allEvents = [];
    const layerSet = new Set();
    const catSet = new Set();
    PROFILES.forEach(p => {{
      const layer = p._layer || 'Other';
      layerSet.add(layer);
      (p.key_events || []).forEach(e => {{
        catSet.add(e.category || 'product');
        allEvents.push({{
          date: e.date,
          event: e.event,
          category: e.category || 'product',
          significance: e.significance || 'medium',
          company: p.company,
          companyId: p._id,
          layer: layer,
        }});
      }});
    }});
    allEvents.sort((a, b) => a.date.localeCompare(b.date));

    let activeLayer = null;
    let activeCat = null;

    function renderGlobalEvents() {{
      const filtered = allEvents.filter(e =>
        (!activeLayer || e.layer === activeLayer) &&
        (!activeCat || e.category === activeCat)
      );
      const el = document.getElementById('gtl-events');
      if (!el) return;
      if (!filtered.length) {{ el.innerHTML = '<p class="empty-state">No events match filter.</p>'; return; }}
      el.innerHTML = filtered.map(e => {{
        const sig = e.significance === 'high' ? ' sig-high' : '';
        return `<div class="global-tl-item">
          <div class="gtl-date">${{e.date}}</div>
          <div class="gtl-company"><span class="clickable" onclick="selectCompany('${{e.companyId}}')">${{e.company}}</span>
            <span class="layer-badge badge-${{e.layer}}" style="font-size:9px;padding:1px 5px;">${{e.layer}}</span>
          </div>
          <div class="gtl-body${{sig}}">${{e.event}}<span class="tl-cat cat-${{e.category}}">${{e.category}}</span></div>
        </div>`;
      }}).join('');
    }}

    function renderFilters() {{
      const bar = document.getElementById('gtl-filters');
      if (!bar) return;
      let html = `<button class="tl-filter-btn${{!activeLayer && !activeCat ? ' active' : ''}}" onclick="_gtlClear()">All</button>`;
      html += '<span style="color:#CBD5E0;font-size:11px;padding:4px 2px">Layer:</span>';
      [...layerSet].forEach(l => {{
        html += `<button class="tl-filter-btn${{activeLayer===l ? ' active' : ''}}" onclick="_gtlLayer('${{l}}')">${{l}}</button>`;
      }});
      html += '<span style="color:#CBD5E0;font-size:11px;padding:4px 6px">Category:</span>';
      [...catSet].forEach(c => {{
        html += `<button class="tl-filter-btn${{activeCat===c ? ' active' : ''}}" onclick="_gtlCat('${{c}}')">${{c}}</button>`;
      }});
      bar.innerHTML = html;
    }}

    window._gtlClear = () => {{ activeLayer = null; activeCat = null; renderFilters(); renderGlobalEvents(); }};
    window._gtlLayer = l => {{ activeLayer = (activeLayer === l) ? null : l; activeCat = null; renderFilters(); renderGlobalEvents(); }};
    window._gtlCat = c => {{ activeCat = (activeCat === c) ? null : c; renderFilters(); renderGlobalEvents(); }};

    renderFilters();
    renderGlobalEvents();
  }})();
}}

function selectCompany(id) {{
  activeId = id;
  document.querySelectorAll('.company-btn').forEach(b => {{
    b.classList.toggle('active', b.dataset.id === id);
  }});
  document.getElementById('overview-btn').classList.remove('active');
  render(id);
}}

function init() {{
  const nav = document.getElementById('company-nav');

  for (const [layer, ids] of Object.entries(LAYERS_WITH_COMPANIES)) {{
    if (!ids.length) continue;
    const layerDiv = document.createElement('div');
    layerDiv.innerHTML = `<div class="layer-label">${{LAYER_LABELS[layer] || layer}}</div>`;
    ids.forEach(id => {{
      const p = getProfile(id);
      const btn = document.createElement('button');
      btn.className = 'company-btn';
      btn.dataset.id = id;
      btn.textContent = p ? p.company : id;
      btn.onclick = () => selectCompany(id);
      layerDiv.appendChild(btn);
    }});
    nav.appendChild(layerDiv);
  }}

  showOverview();
}}

init();
</script>
</body>
</html>"""


def main():
    seed = load_seed_data()
    profiles = load_profiles()
    if not profiles:
        print("[build] no company profiles found in data/companies/")
        return

    hbm_share = load_hbm_market_share(seed)
    capex_annual = load_hyperscaler_capex(seed)

    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    html = build_html(profiles, hbm_share, capex_annual)

    out_path = DASHBOARD_DIR / "index.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"[build] wrote {out_path} ({len(html):,} bytes, {len(profiles)} companies)")


if __name__ == "__main__":
    main()
