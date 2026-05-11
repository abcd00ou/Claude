"""
Dashboard Builder — reads all company JSON profiles and AI_SCM seed data,
inlines everything into a single self-contained HTML file.
Opens with file:// — no server required, no CORS issues.
Chart.js loaded from CDN (internet required for charts; text renders offline).
"""

import json
from datetime import datetime
from pathlib import Path

from config import TARGET_COMPANIES, DATA_DIR, DASHBOARD_DIR, AI_SCM_SEED


def load_profiles() -> list[dict]:
    profiles = []
    for company in TARGET_COMPANIES:
        path = DATA_DIR / f"{company['id']}.json"
        if path.exists():
            try:
                profiles.append(json.loads(path.read_text()))
            except Exception:
                pass
    return profiles


def load_hbm_market_share() -> dict:
    if not AI_SCM_SEED.exists():
        return {}
    try:
        seed = json.loads(AI_SCM_SEED.read_text())
        return seed.get("hbm_market", {}).get("market_share_annual", {})
    except Exception:
        return {}


def build_html(profiles: list[dict], hbm_share: dict) -> str:
    profiles_json = json.dumps(profiles, ensure_ascii=False)

    # HBM share chart data — latest year
    chart_labels, chart_data, chart_colors = [], [], []
    latest_year = max(
        (k for k in hbm_share if not k.startswith("_")), default=None
    )
    if latest_year:
        year_data = hbm_share[latest_year]
        label_map = {"SK_Hynix": "SK Hynix", "Samsung": "Samsung", "Micron": "Micron"}
        color_map = {"SK_Hynix": "#3182CE", "Samsung": "#2D3748", "Micron": "#E53E3E"}
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

    build_ts = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")
    company_ids = [c["id"] for c in TARGET_COMPANIES if
                   (DATA_DIR / f"{c['id']}.json").exists()]

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Company Intelligence Dashboard</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          background: #F7FAFC; color: #1A202C; display: flex; min-height: 100vh; }}

  /* Sidebar */
  #sidebar {{ width: 220px; min-width: 220px; background: #1A202C; padding: 20px 0;
              display: flex; flex-direction: column; }}
  #sidebar h2 {{ color: #63B3ED; font-size: 11px; text-transform: uppercase;
                 letter-spacing: 1px; padding: 0 16px 12px; border-bottom: 1px solid #2D3748; }}
  .company-btn {{ display: block; width: 100%; text-align: left; padding: 10px 16px;
                  background: none; border: none; color: #A0AEC0; cursor: pointer;
                  font-size: 13px; transition: all 0.15s; }}
  .company-btn:hover {{ background: #2D3748; color: #E2E8F0; }}
  .company-btn.active {{ background: #2B6CB0; color: white; font-weight: 600; }}
  #build-ts {{ color: #4A5568; font-size: 10px; padding: 12px 16px; margin-top: auto; }}

  /* Main */
  #main {{ flex: 1; padding: 24px; overflow-y: auto; }}
  .header-bar {{ display: flex; justify-content: space-between; align-items: center;
                  margin-bottom: 20px; }}
  .company-title {{ font-size: 22px; font-weight: 700; }}
  .ticker {{ font-size: 13px; color: #718096; margin-left: 8px; font-weight: 400; }}
  .last-updated {{ font-size: 12px; color: #718096;
                   background: #EDF2F7; padding: 4px 10px; border-radius: 4px; }}

  /* Cards */
  .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px; }}
  .grid-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 16px; margin-bottom: 16px; }}
  .card {{ background: white; border: 1px solid #E2E8F0; border-radius: 8px; padding: 16px; }}
  .card h3 {{ font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px;
               color: #718096; margin-bottom: 10px; }}
  .metric {{ font-size: 22px; font-weight: 700; color: #1A202C; }}
  .metric-label {{ font-size: 12px; color: #718096; margin-top: 2px; }}

  /* Snapshot row */
  .snapshot-grid {{ display: grid; grid-template-columns: repeat(4, 1fr);
                     gap: 12px; margin-bottom: 16px; }}
  .snap-card {{ background: white; border: 1px solid #E2E8F0; border-radius: 8px;
                padding: 14px 16px; }}
  .snap-val {{ font-size: 18px; font-weight: 700; }}
  .snap-lbl {{ font-size: 11px; color: #718096; margin-top: 3px; }}

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
  .status-sampling_2026H2 {{ background: #FEFCBF; color: #744210; }}
  .status-development {{ background: #E2E8F0; color: #4A5568; }}

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
  .comp-label {{ font-weight: 600; color: #4A5568; margin-bottom: 2px; font-size: 11px; }}

  /* Revenue chart */
  .chart-container {{ position: relative; height: 180px; }}

  /* Revenue trend */
  .trend-positive {{ color: #276749; }}
  .empty-state {{ color: #718096; font-size: 13px; font-style: italic; padding: 8px 0; }}
</style>
</head>
<body>

<div id="sidebar">
  <h2>Companies</h2>
  <div id="company-nav"></div>
  <div id="build-ts">Built {build_ts}</div>
</div>

<div id="main">
  <div id="content"></div>
</div>

<script>
const PROFILES = {profiles_json};
const HBM_CHART = {hbm_chart_json};
const COMPANY_IDS = {json.dumps(company_ids)};

let activeId = COMPANY_IDS[0] || null;

function getProfile(id) {{
  return PROFILES.find(p => p.company.toLowerCase().replace(/\\s+/g, '_') === id
    || id.includes(p.company.toLowerCase().split(' ')[0].toLowerCase())) || PROFILES[0];
}}

function statusClass(s) {{
  return 'status-' + (s || 'development').replace(/[^a-z0-9_]/gi, '_');
}}

function renderSnapshot(profile) {{
  const s = profile.snapshot || {{}};
  const items = [
    {{ val: s.revenue_qtr || '—', lbl: 'Latest Revenue' }},
    {{ val: s.op_margin_pct != null ? s.op_margin_pct + '%' : '—', lbl: 'Operating Margin' }},
    {{ val: s.hbm_market_share_pct != null ? s.hbm_market_share_pct + '%' : '—', lbl: 'HBM Market Share' }},
    {{ val: s.headcount ? s.headcount.toLocaleString() : '—', lbl: 'Headcount' }},
  ];
  return `<div class="snapshot-grid">${{items.map(i =>
    `<div class="snap-card"><div class="snap-val">${{i.val}}</div><div class="snap-lbl">${{i.lbl}}</div></div>`
  ).join('')}}</div>`;
}}

function renderRoadmap(profile) {{
  const items = profile.product_roadmap || [];
  if (!items.length) return '<p class="empty-state">No roadmap data yet.</p>';
  return `<table>
    <tr><th>Product</th><th>Status</th><th>Customer</th><th>Notes</th></tr>
    ${{items.map(r => `<tr>
      <td><strong>${{r.product}}</strong></td>
      <td><span class="status-badge ${{statusClass(r.status)}}">${{(r.status||'').replace(/_/g,' ')}}</span></td>
      <td>${{r.customer || '—'}}</td>
      <td>${{r.note || '—'}}</td>
    </tr>`).join('')}}
  </table>`;
}}

function renderHooks(profile) {{
  const hooks = profile.sales_hooks || [];
  if (!hooks.length) return '<p class="empty-state">No sales hooks yet.</p>';
  return hooks.map(h => `<div class="hook">${{h}}</div>`).join('');
}}

function renderNews(profile) {{
  const news = profile.recent_news || [];
  const flagged = new Set((profile.flagged_news || []).map(f => f.title));
  if (!news.length) return '<p class="empty-state">No news collected yet. Run python run.py to fetch.</p>';
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
  const items = [
    {{ label: 'HBM Rank', val: c.hbm_rank ? '#' + c.hbm_rank : '—' }},
    {{ label: 'vs SK Hynix', val: c.vs_sk_hynix || '—' }},
    {{ label: 'vs Samsung',  val: c.vs_samsung  || '—' }},
    {{ label: 'vs Micron',   val: c.vs_micron   || '—' }},
    {{ label: 'Moat',        val: c.moat        || '—' }},
  ].filter(i => i.val !== '—');
  if (!items.length) return '<p class="empty-state">No competitive data yet.</p>';
  return items.map(i =>
    `<div class="comp-item"><div class="comp-label">${{i.label}}</div>${{i.val}}</div>`
  ).join('');
}}

let revenueChart = null;
let hbmPieChart = null;

function renderCharts(profile) {{
  // Revenue trend chart
  const hist = profile.financials_history || {{}};
  const quarters = Object.entries(hist)
    .filter(([k]) => !k.startsWith('_'))
    .sort(([a],[b]) => a.localeCompare(b));

  if (quarters.length > 1) {{
    const ctx = document.getElementById('revenueChart');
    if (ctx) {{
      if (revenueChart) revenueChart.destroy();
      revenueChart = new Chart(ctx, {{
        type: 'bar',
        data: {{
          labels: quarters.map(([k]) => k.replace('_revenue_krw_t','').replace('_revenue_usd_bn','')),
          datasets: [{{ label: 'Revenue', data: quarters.map(([,v]) => v),
            backgroundColor: '#3182CE', borderRadius: 4 }}]
        }},
        options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }},
          scales: {{ y: {{ beginAtZero: false }} }} }}
      }});
    }}
  }}

  // HBM market share pie
  const pieCtx = document.getElementById('hbmPieChart');
  if (pieCtx && HBM_CHART.data.length) {{
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

function render(id) {{
  const profile = getProfile(id);
  const hist = profile.financials_history || {{}};
  const hasRevChart = Object.keys(hist).filter(k=>!k.startsWith('_')).length > 1;

  document.getElementById('content').innerHTML = `
    <div class="header-bar">
      <div>
        <span class="company-title">${{profile.company}}</span>
        <span class="ticker">${{profile.ticker || ''}}</span>
      </div>
      <div class="last-updated">Last updated: ${{profile.last_updated || 'N/A'}}</div>
    </div>

    ${{renderSnapshot(profile)}}

    <div class="grid-2">
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
        <h3>Revenue Trend</h3>
        <div class="chart-container"><canvas id="revenueChart"></canvas></div>
      </div>` : ''}}
      ${{HBM_CHART.data.length ? `<div class="card">
        <h3>HBM Market Share (${{HBM_CHART.year}})</h3>
        <div class="chart-container"><canvas id="hbmPieChart"></canvas></div>
      </div>` : ''}}
    </div>

    <div class="card">
      <h3>Recent News</h3>
      ${{renderNews(profile)}}
    </div>
  `;

  setTimeout(() => renderCharts(profile), 0);
}}

function init() {{
  const nav = document.getElementById('company-nav');
  COMPANY_IDS.forEach(id => {{
    const p = getProfile(id);
    const btn = document.createElement('button');
    btn.className = 'company-btn' + (id === activeId ? ' active' : '');
    btn.textContent = p ? p.company : id;
    btn.onclick = () => {{
      activeId = id;
      document.querySelectorAll('.company-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      render(id);
    }};
    nav.appendChild(btn);
  }});

  if (activeId) render(activeId);
}}

init();
</script>
</body>
</html>"""


def main():
    profiles = load_profiles()
    if not profiles:
        print("[build] no company profiles found in data/companies/")
        return

    hbm_share = load_hbm_market_share()

    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    html = build_html(profiles, hbm_share)

    out_path = DASHBOARD_DIR / "index.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"[build] wrote {out_path} ({len(html):,} bytes, {len(profiles)} companies)")


if __name__ == "__main__":
    main()
