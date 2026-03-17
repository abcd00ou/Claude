"""
Price Intelligence — Samsung vs SanDisk 가격 분석
데이터: Crawling / PostgreSQL price_intel
"""
import sys
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(ROOT / "Crawling"))

st.set_page_config(page_title="Price Intelligence", page_icon="💰", layout="wide")
st.title("💰 Price Intelligence")
st.caption("Samsung vs SanDisk 실시간 가격 경쟁 분석")

BRAND_COLORS = {"samsung": "#1428A0", "sandisk": "#E2231A", "lexar": "#F7941D"}
BRAND_LABELS = {"samsung": "Samsung", "sandisk": "SanDisk", "lexar": "Lexar"}
CAT_LABELS   = {"portable_ssd": "Portable SSD", "internal_ssd": "Internal SSD", "microsd": "microSD"}

@st.cache_data(ttl=3600)  # 환율은 1시간 캐시
def fetch_fx_rates() -> dict:
    """당일 환율 조회 (USD 기준). 실패 시 폴백값 사용."""
    import requests
    fallback = {"USD": 1.0, "EUR": 1.09, "JPY": 0.0067}
    try:
        resp = requests.get(
            "https://api.frankfurter.app/latest?base=USD&symbols=EUR,JPY",
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            rates = data.get("rates", {})
            # frankfurter는 1USD 기준 → EUR/JPY 값
            # 우리가 원하는 건 1EUR/JPY → USD 이므로 역수
            return {
                "USD": 1.0,
                "EUR": round(1 / rates["EUR"], 6) if "EUR" in rates else fallback["EUR"],
                "JPY": round(1 / rates["JPY"], 6) if "JPY" in rates else fallback["JPY"],
            }
    except Exception:
        pass
    return fallback


@st.cache_data(ttl=180)
def load_all():
    import psycopg2
    conn = psycopg2.connect("dbname=price_intel")
    df = pd.read_sql("""
        SELECT p.id, p.observed_at, p.price, p.currency, p.country,
               s.brand, s.category, s.model, s.capacity
        FROM price_observations p
        JOIN skus s ON p.sku_id = s.sku_id
        WHERE p.is_accepted = true AND p.price > 0
        ORDER BY p.observed_at DESC
    """, conn)
    conn.close()
    df["observed_at"] = pd.to_datetime(df["observed_at"], utc=True)
    return df


def to_usd(df: pd.DataFrame, fx: dict) -> pd.DataFrame:
    """price 컬럼을 당일 환율 기준 USD로 환산, price_usd 컬럼 추가"""
    df = df.copy()
    df["fx_rate"]   = df["currency"].map(fx).fillna(1.0)
    df["price_usd"] = (df["price"] * df["fx_rate"]).round(2)
    return df

try:
    df = load_all()
    db_ok = True
except Exception as e:
    st.error(f"DB 연결 실패: {e}")
    db_ok = False
    st.stop()

# ── 환율 로드 & USD 환산 ─────────────────────────────────────
fx = fetch_fx_rates()
df = to_usd(df, fx)

# 사이드바에 환율 정보 표시
with st.sidebar:
    st.header("💱 적용 환율 (→ USD)")
    fx_date = datetime.now().strftime("%Y-%m-%d")
    for cur, rate in fx.items():
        if cur != "USD":
            st.metric(f"1 {cur}", f"${rate:.4f}", help="frankfurter.app 당일 환율")
    st.caption(f"기준일: {fx_date}")
    st.divider()

# ── 필터 ────────────────────────────────────────────────────
with st.sidebar:
    st.header("필터")
    cats = st.multiselect("카테고리", list(CAT_LABELS.keys()),
                          default=list(CAT_LABELS.keys()),
                          format_func=lambda x: CAT_LABELS[x])
    brands = st.multiselect("브랜드", list(BRAND_LABELS.keys()),
                             default=list(BRAND_LABELS.keys()),
                             format_func=lambda x: BRAND_LABELS[x])
    countries = df["country"].dropna().unique().tolist()
    sel_country = st.selectbox("국가", ["ALL"] + sorted(countries))
    days = st.slider("기간 (일)", 7, 90, 30)

fdf = df[df["category"].isin(cats) & df["brand"].isin(brands)]
if sel_country != "ALL":
    fdf = fdf[fdf["country"] == sel_country]
cutoff = datetime.now(tz=fdf["observed_at"].dt.tz) - timedelta(days=days)
fdf = fdf[fdf["observed_at"] >= cutoff]

if fdf.empty:
    st.warning("해당 조건의 데이터가 없습니다.")
    st.stop()

# ── KPI ─────────────────────────────────────────────────────
latest = fdf.sort_values("observed_at").groupby(["brand", "category", "model", "capacity"]).last().reset_index()

c1, c2, c3, c4 = st.columns(4)
sam_lat = latest[latest["brand"] == "samsung"]["price_usd"].mean()
san_lat = latest[latest["brand"] == "sandisk"]["price_usd"].mean()
gap     = san_lat - sam_lat
gap_pct = gap / sam_lat * 100 if sam_lat else 0
c1.metric("Samsung 평균가 (USD)", f"${sam_lat:.2f}")
c2.metric("SanDisk 평균가 (USD)", f"${san_lat:.2f}")
c3.metric("가격 갭 (SanDisk−Samsung)", f"${gap:+.2f}", f"{gap_pct:+.1f}%")
c4.metric("관측 데이터", f"{len(fdf):,}건", f"{days}일 기준")

st.divider()

# ── 탭 ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 Gap Overview", "📈 가격 추이", "⚔️ 용량별 비교", "📋 데이터 테이블"])

# Tab 1: Gap Overview
with tab1:
    fx_str = "  |  ".join(f"1 {c} = ${r:.4f}" for c, r in fx.items() if c != "USD")
    st.caption(f"💱 적용 환율: {fx_str}  (frankfurter.app 당일 기준, 1시간 캐시)")
    st.subheader("Samsung vs SanDisk — 카테고리별 평균 가격 갭 (USD 환산)")
    gap_rows = []
    for cat in cats:
        for cap in sorted(latest["capacity"].dropna().unique()):
            s = latest[(latest["brand"] == "samsung") & (latest["category"] == cat) & (latest["capacity"] == cap)]["price_usd"]
            d = latest[(latest["brand"] == "sandisk") & (latest["category"] == cat) & (latest["capacity"] == cap)]["price_usd"]
            if not s.empty and not d.empty:
                gap_rows.append({
                    "카테고리": CAT_LABELS.get(cat, cat),
                    "용량": cap,
                    "Samsung (USD)": round(s.mean(), 2),
                    "SanDisk (USD)": round(d.mean(), 2),
                    "갭 ($)": round(d.mean() - s.mean(), 2),
                    "갭 (%)": round((d.mean() - s.mean()) / s.mean() * 100, 1) if s.mean() else 0,
                })
    if gap_rows:
        gdf = pd.DataFrame(gap_rows).sort_values("갭 (%)")
        fig = go.Figure()
        fig.add_bar(x=gdf["카테고리"] + " " + gdf["용량"], y=gdf["Samsung (USD)"],
                    name="Samsung", marker_color=BRAND_COLORS["samsung"])
        fig.add_bar(x=gdf["카테고리"] + " " + gdf["용량"], y=gdf["SanDisk (USD)"],
                    name="SanDisk", marker_color=BRAND_COLORS["sandisk"])
        fig.update_layout(barmode="group", height=380,
                          yaxis_title="가격 (USD)", xaxis_title="",
                          legend=dict(orientation="h", y=1.05),
                          margin=dict(l=10, r=10, t=30, b=80),
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          font=dict(color="white"))
        st.plotly_chart(fig, use_container_width=True)

        st.dataframe(
            gdf.style.applymap(
                lambda v: "color: #ef4444" if isinstance(v, (int, float)) and v > 0 else
                          "color: #22c55e" if isinstance(v, (int, float)) and v < 0 else "",
                subset=["갭 ($)", "갭 (%)"]
            ),
            use_container_width=True, hide_index=True
        )

# Tab 2: 가격 추이
with tab2:
    st.subheader("시간별 가격 추이 (USD 환산)")
    st.caption(f"💱 {fx_str}")
    sel_cat2 = st.selectbox("카테고리", cats, format_func=lambda x: CAT_LABELS[x], key="t2cat")
    tdf = fdf[fdf["category"] == sel_cat2].copy()
    tdf["date"] = tdf["observed_at"].dt.date
    tdf["label"] = tdf["brand"].map(BRAND_LABELS) + " " + tdf["model"] + " " + tdf["capacity"].fillna("")
    daily = tdf.groupby(["date", "label", "brand"])["price_usd"].mean().reset_index()

    fig = px.line(daily, x="date", y="price_usd", color="label",
                  color_discrete_map={l: BRAND_COLORS.get(b, "#888")
                                      for l, b in zip(daily["label"], daily["brand"])},
                  markers=True, height=400)
    fig.update_layout(yaxis_title="가격 (USD)", xaxis_title="",
                      legend=dict(orientation="h", y=1.05),
                      plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: 용량별 비교
with tab3:
    st.subheader("용량별 1TB당 가격 비교 (USD/TB 환산)")
    st.caption(f"💱 {fx_str}")
    cap_map = {"1TB": 1, "2TB": 2, "4TB": 4, "500GB": 0.5, "256GB": 0.256}
    comp = latest.copy()
    comp["cap_tb"] = comp["capacity"].map(cap_map)
    comp["price_per_tb"] = comp.apply(
        lambda r: r["price_usd"] / r["cap_tb"] if r["cap_tb"] else None, axis=1)
    comp = comp.dropna(subset=["price_per_tb"])

    for cat in cats:
        cdf = comp[comp["category"] == cat]
        if cdf.empty:
            continue
        st.markdown(f"**{CAT_LABELS.get(cat, cat)}**")
        fig = px.bar(cdf.sort_values("capacity"),
                     x="capacity", y="price_per_tb", color="brand",
                     color_discrete_map=BRAND_COLORS,
                     barmode="group", height=280,
                     labels={"price_per_tb": "$/TB", "capacity": "용량", "brand": "브랜드"})
        fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          font=dict(color="white"), margin=dict(t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)

# Tab 4: 데이터 테이블
with tab4:
    st.subheader("원시 관측 데이터 (USD 환산 포함)")
    show = fdf[["observed_at", "brand", "category", "model", "capacity",
                "price", "currency", "fx_rate", "price_usd", "country"]].copy()
    show["brand"]    = show["brand"].map(BRAND_LABELS)
    show["category"] = show["category"].map(CAT_LABELS)
    show["observed_at"] = show["observed_at"].dt.strftime("%Y-%m-%d %H:%M")
    st.dataframe(show.rename(columns={
        "observed_at": "관측시각", "brand": "브랜드", "category": "카테고리",
        "model": "모델", "capacity": "용량", "price": "원가격",
        "currency": "통화", "fx_rate": "환율(→USD)",
        "price_usd": "USD 환산가", "country": "국가"
    }), use_container_width=True, hide_index=True)
