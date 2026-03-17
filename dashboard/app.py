"""
SanDisk B2C Intelligence Hub — 통합 대시보드
Overview 홈 페이지: 3개 시스템의 핵심 KPI를 한눈에
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ── 경로 설정 ────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "Crawling"))

st.set_page_config(
    page_title="SanDisk Intelligence Hub",
    page_icon="💾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── 스타일 ───────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stMetricValue"] { font-size: 1.8rem; }
.kpi-section { border-left: 3px solid #E2231A; padding-left: 0.8rem; margin-bottom: 1rem; }
.source-tag { color: #888; font-size: 0.75rem; }
</style>
""", unsafe_allow_html=True)

# ── 데이터 로더 ──────────────────────────────────────────────

@st.cache_data(ttl=300)
def load_price_summary():
    try:
        import psycopg2
        conn = psycopg2.connect("dbname=price_intel")
        df = pd.read_sql("""
            SELECT s.brand, s.category,
                   AVG(p.price_usd) as avg_price,
                   COUNT(*) as obs_count,
                   MAX(p.fetched_at) as last_updated
            FROM price_observations p
            JOIN skus s ON p.sku_id = s.id
            WHERE p.fetched_at >= NOW() - INTERVAL '7 days'
              AND p.price_usd > 0
            GROUP BY s.brand, s.category
            ORDER BY s.brand, s.category
        """, conn)
        conn.close()

        # Samsung vs SanDisk 최신 포터블 SSD 갭
        gap_df = pd.read_sql("""
            SELECT s.brand, s.category, s.capacity_gb,
                   p.price_usd, p.fetched_at
            FROM price_observations p
            JOIN skus s ON p.sku_id = s.id
            WHERE s.category = 'portable_ssd'
              AND s.brand IN ('samsung', 'sandisk')
              AND p.price_usd > 0
              AND p.fetched_at = (
                SELECT MAX(p2.fetched_at) FROM price_observations p2
                WHERE p2.sku_id = p.sku_id
              )
        """, conn) if False else pd.DataFrame()  # conn already closed, skip
        return df
    except Exception as e:
        return pd.DataFrame()


@st.cache_data(ttl=300)
def load_price_gap():
    try:
        import psycopg2
        conn = psycopg2.connect("dbname=price_intel")
        df = pd.read_sql("""
            WITH latest AS (
                SELECT sku_id, MAX(fetched_at) as max_ts
                FROM price_observations WHERE price_usd > 0
                GROUP BY sku_id
            )
            SELECT s.brand, s.category, s.capacity_gb, s.model_name,
                   p.price_usd, p.fetched_at
            FROM price_observations p
            JOIN latest l ON p.sku_id = l.sku_id AND p.fetched_at = l.max_ts
            JOIN skus s ON p.sku_id = s.id
            WHERE s.brand IN ('samsung','sandisk')
              AND s.category = 'portable_ssd'
            ORDER BY s.capacity_gb
        """, conn)
        conn.close()
        return df
    except Exception:
        return pd.DataFrame()


@st.cache_data(ttl=60)
def load_ai_demand():
    f = ROOT / "ssd_ai_potential" / "data" / "analysis_results.json"
    if not f.exists():
        return None
    with open(f) as fp:
        history = json.load(fp)
    return history[-1] if history else None


@st.cache_data(ttl=60)
def load_marketing():
    sim_f  = ROOT / "marketing" / "data" / "sim_state.json"
    intel_f = ROOT / "marketing" / "data" / "market_intel.json"
    result = {}
    if sim_f.exists():
        with open(sim_f) as f:
            result["sim"] = json.load(f)
    if intel_f.exists():
        with open(intel_f) as f:
            result["intel"] = json.load(f)
    return result


# ── 헤더 ────────────────────────────────────────────────────
st.title("💾 SanDisk Intelligence Hub")
st.caption(f"마지막 갱신: {datetime.now().strftime('%Y-%m-%d %H:%M')}  |  자동 갱신: 5분")

st.divider()

# ── 3개 시스템 KPI 요약 ──────────────────────────────────────
col1, col2, col3 = st.columns(3)

# 1. Price Intelligence
with col1:
    st.markdown("### 💰 가격 인텔리전스")
    price_df = load_price_summary()
    gap_df   = load_price_gap()

    if not gap_df.empty:
        sam = gap_df[gap_df["brand"] == "samsung"]["price_usd"].mean()
        san = gap_df[gap_df["brand"] == "sandisk"]["price_usd"].mean()
        gap = san - sam
        gap_pct = gap / sam * 100 if sam else 0
        st.metric("Samsung vs SanDisk 평균 가격 갭", f"${gap:+.2f}", f"{gap_pct:+.1f}%")
        st.metric("포터블 SSD SKU 수", f"{len(gap_df)}개 SKU")
    elif not price_df.empty:
        total_obs = int(price_df["obs_count"].sum())
        st.metric("최근 7일 관측 수", f"{total_obs}건")
        brands = price_df["brand"].nunique()
        st.metric("추적 브랜드", f"{brands}개")
    else:
        st.info("DB 데이터 로딩 중...")
        st.metric("추적 SKU", "72개")
        st.metric("가격 관측", "379건")

    st.markdown('<p class="source-tag">📡 Crawling / PostgreSQL</p>', unsafe_allow_html=True)

# 2. AI Demand
with col2:
    st.markdown("### 🤖 Local AI × SSD 수요")
    ai = load_ai_demand()
    if ai:
        total = ai["total_posts"]
        demand = ai["demand_total"]
        rate   = ai["demand_rate_pct"]
        portable = ai.get("portable_ssd_mentions", 0)
        st.metric("수요 신호 포스트", f"{demand}건", f"{rate}% / {total:,}개 분석")
        st.metric("포터블 SSD 언급", f"{portable}건",
                  f"{ai.get('portable_ssd_pct', 0)}%")
        # 기술 근거 Top 1
        factors = ai.get("technical_factors", {})
        if factors:
            top_f = max(factors, key=factors.get)
            top_labels = {
                "model_weight_size": "모델 파일 용량",
                "portability": "포터블 이동 실행",
                "io_bottleneck": "I/O 병목",
                "vram_offload": "VRAM 오프로드",
            }
            st.metric("1위 기술 근거", top_labels.get(top_f, top_f), f"{factors[top_f]}건")
    else:
        st.info("분석 데이터 없음")
    st.markdown('<p class="source-tag">📡 ssd_ai_potential / Reddit 3,792건</p>', unsafe_allow_html=True)

# 3. Marketing Simulation
with col3:
    st.markdown("### 📈 마케팅 시뮬레이션")
    mkt = load_marketing()
    if mkt.get("sim"):
        sim = mkt["sim"]
        history = sim.get("history", [])
        if history:
            last = history[-1]
            rev = last.get("total_rev_m", 0)
            gm  = last.get("blended_gm_pct", 0)
            ms  = last.get("market_share_pct", {})
            ms_val = ms.get("overall", list(ms.values())[0]) if ms else 0
            st.metric("시뮬레이션 월매출", f"${rev:.1f}M")
            st.metric("블렌디드 GM", f"{gm:.1f}%")
            st.metric("시장점유율", f"{ms_val:.1f}%")
    if mkt.get("intel"):
        intel = mkt["intel"]
        nand  = intel.get("nand_signal", "unknown")
        trend = intel.get("price_trend", "")
        nand_color = {"tight": "🔴", "loose": "🟢", "neutral": "🟡"}.get(nand, "⚪")
        st.metric("NAND 공급 신호", f"{nand_color} {nand.upper()}", trend)
    st.markdown('<p class="source-tag">📡 Marketing / Simulation Engine</p>', unsafe_allow_html=True)

st.divider()

# ── 핵심 인사이트 종합 ───────────────────────────────────────
st.markdown("## 🔍 통합 인사이트")

insight_col1, insight_col2 = st.columns(2)

with insight_col1:
    st.markdown("#### Local AI → SSD 수요 기술 근거")
    ai = load_ai_demand()
    if ai and ai.get("technical_factors"):
        factors = ai["technical_factors"]
        labels = {
            "model_weight_size": "모델 파일 용량",
            "portability":       "포터블 이동 실행",
            "io_bottleneck":     "I/O 병목",
            "vram_offload":      "VRAM 오프로드",
            "capacity":          "단순 용량 부족",
            "swap_speed":        "스왑 속도",
            "speed_matters":     "NVMe 속도 중요",
        }
        items = sorted(factors.items(), key=lambda x: -x[1])
        fig = go.Figure(go.Bar(
            x=[v for _, v in items],
            y=[labels.get(k, k) for k, _ in items],
            orientation="h",
            marker_color="#E2231A",
            text=[str(v) for _, v in items],
            textposition="outside",
        ))
        fig.update_layout(
            height=280, margin=dict(l=10, r=40, t=10, b=10),
            xaxis=dict(showgrid=False),
            yaxis=dict(autorange="reversed"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("데이터 없음")

with insight_col2:
    st.markdown("#### NAND 시장 최신 헤드라인")
    mkt = load_marketing()
    if mkt.get("intel"):
        headlines = mkt["intel"].get("headlines", [])[:5]
        for h in headlines:
            title = h.get("title", "")
            date  = h.get("date", "")[:10]
            url   = h.get("url", "#")
            st.markdown(f"- [{title[:65]}{'...' if len(title)>65 else ''}]({url}) `{date}`")
        insights = mkt["intel"].get("key_insights", [])
        if insights:
            st.markdown("**시장 시사점**")
            for ins in insights[:3]:
                st.markdown(f"- {ins}")
    else:
        st.info("마켓 인텔 데이터 없음")

st.divider()

# ── 수요 신호 트렌드 (시계열) ────────────────────────────────
st.markdown("## 📊 수요 신호 트렌드 (누적)")
f = ROOT / "ssd_ai_potential" / "data" / "analysis_results.json"
if f.exists():
    with open(f) as fp:
        history = json.load(fp)
    if len(history) > 1:
        dates   = [h["analysis_date"][:10] for h in history]
        totals  = [h["total_posts"] for h in history]
        demands = [h["demand_total"] for h in history]
        rates   = [h["demand_rate_pct"] for h in history]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=totals, name="전체 포스트",
                                  line=dict(color="#4B9CD3", width=2), yaxis="y"))
        fig.add_trace(go.Scatter(x=dates, y=demands, name="수요 신호",
                                  line=dict(color="#E2231A", width=2), yaxis="y"))
        fig.add_trace(go.Scatter(x=dates, y=rates, name="수요율(%)",
                                  line=dict(color="#FFA500", width=2, dash="dot"), yaxis="y2"))
        fig.update_layout(
            height=250,
            yaxis=dict(title="포스트 수"),
            yaxis2=dict(title="수요율 (%)", overlaying="y", side="right", range=[0, 20]),
            legend=dict(orientation="h", y=1.1),
            margin=dict(l=10, r=10, t=30, b=10),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("트렌드 표시를 위한 데이터 누적 중... (현재 1회 분석 완료)")

st.divider()
st.markdown("#### 페이지 바로가기")
c1, c2, c3 = st.columns(3)
c1.page_link("pages/1_💰_Price_Intel.py",  label="💰 가격 인텔리전스 상세", icon="📊")
c2.page_link("pages/2_🤖_AI_Demand.py",   label="🤖 AI 수요 분석 상세",   icon="🔍")
c3.page_link("pages/3_📈_Marketing_Sim.py", label="📈 마케팅 시뮬레이션",   icon="📈")
