"""
Price Intelligence Dashboard — Enhanced
경쟁사 가격 비교 + 시계열 분석 중심

탭 구성:
  1. 📊 Price Overview     — 최신 가격 현황 & 브랜드별 히트맵
  2. 📈 Time Series        — SKU별 가격 추이 (이동평균 포함)
  3. ⚔️  Competitor Compare — Samsung vs SanDisk vs Lexar 심층 비교
  4. 🔍 Price Gap Analysis  — Samsung 대비 프리미엄/할인 추이
  5. 🌍 Country Compare     — 국가별 동일 제품 가격 비교
  6. 🚨 Alerts             — 이상 변동 알림
"""
import json
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import DB_URL

# ── 페이지 설정 ──────────────────────────────────────────────
st.set_page_config(
    page_title="Price Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

BRAND_COLORS = {
    "samsung": "#1428A0",
    "sandisk": "#E2231A",
    "lexar":   "#F7941D",
    "wd":      "#FF6B35",
}
BRAND_LABELS = {
    "samsung": "Samsung",
    "sandisk": "SanDisk",
    "lexar":   "Lexar",
    "wd":      "WD",
}
CATEGORY_LABELS = {
    "portable_ssd": "Portable SSD",
    "internal_ssd": "Internal SSD",
    "microsd":      "microSD",
}

# ── DB 연결 ──────────────────────────────────────────────────
@st.cache_resource
def get_conn():
    import psycopg2
    return psycopg2.connect(DB_URL)


def db_conn():
    conn = get_conn()
    try:
        conn.cursor().execute("SELECT 1")
    except Exception:
        get_conn.clear()
        conn = get_conn()
    return conn


def safe_query(sql, params=()) -> pd.DataFrame:
    """DB 쿼리 실패 시 빈 DataFrame 반환."""
    try:
        conn = db_conn()
        cur = conn.cursor()
        cur.execute(sql, params)
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
        cur.close()
        return pd.DataFrame(rows, columns=cols)
    except Exception as e:
        st.warning(f"DB 연결 오류: {e}")
        return pd.DataFrame()


# ── 쿼리 함수들 ───────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_latest_prices(countries: list, categories: list) -> pd.DataFrame:
    return safe_query("""
        SELECT DISTINCT ON (p.sku_id, p.country, p.source)
            p.sku_id, s.brand, s.category, s.model, s.capacity,
            p.country, p.source, p.price, p.currency,
            p.original_price, p.availability, p.observed_at
        FROM price_observations p
        JOIN skus s ON p.sku_id = s.sku_id
        WHERE p.is_accepted = TRUE
          AND p.country = ANY(%s)
          AND s.category = ANY(%s)
        ORDER BY p.sku_id, p.country, p.source, p.observed_at DESC
    """, (countries, categories))


@st.cache_data(ttl=300)
def load_price_history(sku_ids: list, countries: list, days: int = 180) -> pd.DataFrame:
    return safe_query("""
        SELECT p.sku_id, s.brand, s.model, s.capacity,
               p.country, p.source, p.price, p.currency, p.observed_at
        FROM price_observations p
        JOIN skus s ON p.sku_id = s.sku_id
        WHERE p.sku_id = ANY(%s)
          AND p.country = ANY(%s)
          AND p.is_accepted = TRUE
          AND p.observed_at >= NOW() - INTERVAL '1 day' * %s
        ORDER BY p.observed_at
    """, (sku_ids, countries, days))


@st.cache_data(ttl=300)
def load_all_history(categories: list, countries: list, days: int = 180) -> pd.DataFrame:
    return safe_query("""
        SELECT p.sku_id, s.brand, s.category, s.model, s.capacity,
               p.country, p.source, p.price, p.currency, p.observed_at
        FROM price_observations p
        JOIN skus s ON p.sku_id = s.sku_id
        WHERE s.category = ANY(%s)
          AND p.country = ANY(%s)
          AND p.is_accepted = TRUE
          AND p.observed_at >= NOW() - INTERVAL '1 day' * %s
        ORDER BY p.observed_at
    """, (categories, countries, days))


@st.cache_data(ttl=300)
def load_all_skus() -> pd.DataFrame:
    return safe_query("""
        SELECT sku_id, brand, category, model, capacity
        FROM skus ORDER BY brand, category, model, capacity
    """)


@st.cache_data(ttl=300)
def load_price_alerts(threshold_pct: float = 10.0, days: int = 14) -> pd.DataFrame:
    return safe_query("""
        WITH ranked AS (
            SELECT
                p.sku_id, s.brand, s.model, s.capacity, p.country, p.source,
                p.price, p.currency, p.observed_at,
                LAG(p.price) OVER (
                    PARTITION BY p.sku_id, p.country, p.source
                    ORDER BY p.observed_at
                ) AS prev_price
            FROM price_observations p
            JOIN skus s ON p.sku_id = s.sku_id
            WHERE p.is_accepted = TRUE
              AND p.observed_at >= NOW() - INTERVAL '1 day' * %(days)s
        )
        SELECT *, ROUND(100.0*(price-prev_price)/NULLIF(prev_price,0), 1) AS change_pct
        FROM ranked
        WHERE prev_price IS NOT NULL AND prev_price > 0
          AND ABS((price-prev_price)/prev_price*100) >= %(threshold)s
        ORDER BY ABS((price-prev_price)/NULLIF(prev_price,0)) DESC
        LIMIT 100
    """, {"threshold": threshold_pct, "days": days})


@st.cache_data(ttl=300)
def load_category_timeseries(category: str, country: str, days: int = 180) -> pd.DataFrame:
    """카테고리 전체 가격 중앙값 시계열 (브랜드별)."""
    return safe_query("""
        SELECT
            DATE_TRUNC('day', p.observed_at) AS date,
            s.brand,
            PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY p.price) AS median_price,
            COUNT(DISTINCT p.sku_id) AS sku_count
        FROM price_observations p
        JOIN skus s ON p.sku_id = s.sku_id
        WHERE s.category = %s
          AND p.country = %s
          AND p.is_accepted = TRUE
          AND p.observed_at >= NOW() - INTERVAL '1 day' * %s
        GROUP BY 1, 2
        ORDER BY 1
    """, (category, country, days))


# ── 사이드바 필터 ─────────────────────────────────────────────
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/SanDisk_logo.svg/320px-SanDisk_logo.svg.png",
                 width=120, use_column_width=False)
st.sidebar.title("Price Intelligence")
st.sidebar.caption(f"Samsung · SanDisk · Lexar | {datetime.now().strftime('%Y-%m-%d %H:%M')}")

st.sidebar.divider()
selected_countries = st.sidebar.multiselect(
    "국가", ["US", "KR", "JP", "DE"], default=["US"]
)
selected_categories = st.sidebar.multiselect(
    "카테고리",
    list(CATEGORY_LABELS.keys()),
    format_func=lambda x: CATEGORY_LABELS[x],
    default=list(CATEGORY_LABELS.keys()),
)
selected_brands = st.sidebar.multiselect(
    "브랜드", ["samsung", "sandisk", "lexar"],
    format_func=lambda x: BRAND_LABELS.get(x, x),
    default=["samsung", "sandisk", "lexar"],
)
history_days = st.sidebar.selectbox("분석 기간", [30, 60, 90, 180, 365], index=2,
                                     format_func=lambda x: f"최근 {x}일")
primary_country = selected_countries[0] if selected_countries else "US"

if not selected_countries:
    selected_countries = ["US"]
if not selected_categories:
    selected_categories = list(CATEGORY_LABELS.keys())

# ── 탭 ───────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Price Overview",
    "📈 Time Series",
    "⚔️ Competitor Compare",
    "🔍 Price Gap Analysis",
    "🌍 Country Compare",
    "🚨 Alerts",
])


# ═══════════════════════════════════════════════════════════════
# Tab 1: Price Overview
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.header("최신 가격 현황")

    df_latest = load_latest_prices(selected_countries, selected_categories)
    if df_latest.empty:
        st.info("데이터 없음. `python run_pipeline.py` 실행 후 확인하세요.")
        st.stop()

    df_latest = df_latest[df_latest["brand"].isin(selected_brands)]

    # KPI 카드
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("전체 SKU", df_latest["sku_id"].nunique())
    c2.metric("Samsung", len(df_latest[df_latest["brand"] == "samsung"]["sku_id"].unique()))
    c3.metric("SanDisk",  len(df_latest[df_latest["brand"] == "sandisk"]["sku_id"].unique()))
    c4.metric("Lexar",    len(df_latest[df_latest["brand"] == "lexar"]["sku_id"].unique()))
    latest_ts = pd.to_datetime(df_latest["observed_at"]).max()
    c5.metric("마지막 수집", latest_ts.strftime("%m/%d %H:%M") if pd.notna(latest_ts) else "—")

    st.divider()

    # 카테고리별 최신 가격 테이블 + Amazon 기준 히트맵
    for cat in selected_categories:
        cat_df = df_latest[(df_latest["category"] == cat) &
                           (df_latest["source"] == "amazon") &
                           (df_latest["country"] == primary_country)].copy()
        if cat_df.empty:
            continue

        st.subheader(f"{CATEGORY_LABELS[cat]} — Amazon {primary_country}")

        # pivot: 제품 × 브랜드
        cat_df["product_label"] = cat_df["model"] + " " + cat_df["capacity"].fillna("")
        pivot = cat_df.pivot_table(
            index="product_label", columns="brand", values="price", aggfunc="min"
        ).reset_index()

        brands_present = [b for b in ["samsung", "sandisk", "lexar"] if b in pivot.columns]
        if brands_present:
            fig = go.Figure()
            for brand in brands_present:
                if brand in pivot.columns:
                    fig.add_trace(go.Bar(
                        name=BRAND_LABELS.get(brand, brand),
                        x=pivot["product_label"],
                        y=pivot[brand],
                        marker_color=BRAND_COLORS[brand],
                        text=pivot[brand].apply(lambda v: f"${v:,.0f}" if pd.notna(v) else ""),
                        textposition="outside",
                    ))
            fig.update_layout(
                barmode="group",
                height=380,
                margin=dict(t=20, b=60),
                legend=dict(orientation="h", y=1.05),
                xaxis_tickangle=-25,
            )
            st.plotly_chart(fig, use_container_width=True)

        # 데이터 테이블
        display_cols = ["product_label"] + [b for b in ["samsung", "sandisk", "lexar"] if b in pivot.columns]
        st.dataframe(
            pivot[display_cols].rename(columns={
                "product_label": "제품",
                "samsung": "Samsung ($)",
                "sandisk": "SanDisk ($)",
                "lexar": "Lexar ($)",
            }).style.format("{:.2f}", subset=[c for c in ["Samsung ($)", "SanDisk ($)", "Lexar ($)"] if c in pivot.columns], na_rep="—"),
            use_container_width=True, hide_index=True,
        )
        st.divider()


# ═══════════════════════════════════════════════════════════════
# Tab 2: Time Series
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.header("가격 추이 분석")

    skus_df = load_all_skus()
    if skus_df.empty:
        st.info("SKU 데이터 없음.")
    else:
        col_left, col_right = st.columns([3, 1])
        with col_left:
            sku_options = {
                row["sku_id"]: f"[{BRAND_LABELS.get(row['brand'], row['brand']).upper()}] {row['model']} {row['capacity']}"
                for _, row in skus_df[skus_df["brand"].isin(selected_brands)].iterrows()
            }
            selected_skus = st.multiselect(
                "SKU 선택 (최대 8개)",
                options=list(sku_options.keys()),
                format_func=lambda x: sku_options.get(x, x),
                max_selections=8,
                default=list(sku_options.keys())[:3],
            )
        with col_right:
            ts_country = st.selectbox("국가", selected_countries, key="ts_country")
            ma_window = st.selectbox("이동평균", [None, 7, 14, 30], index=2,
                                     format_func=lambda x: f"없음" if x is None else f"{x}일 MA")

        if selected_skus:
            hist = load_price_history(selected_skus, [ts_country], history_days)
            if hist.empty:
                st.info("가격 기록 없음.")
            else:
                hist["observed_at"] = pd.to_datetime(hist["observed_at"])
                hist["label"] = hist["brand"].apply(lambda b: BRAND_LABELS.get(b, b)) + " " + hist["model"] + " " + hist["capacity"].fillna("")
                hist = hist.sort_values("observed_at")

                # 이동평균 추가
                if ma_window:
                    ma_rows = []
                    for lbl, grp in hist.groupby("label"):
                        grp = grp.set_index("observed_at").sort_index()
                        grp[f"ma_{ma_window}"] = grp["price"].rolling(f"{ma_window}D").mean()
                        grp = grp.reset_index()
                        grp["label"] = lbl
                        ma_rows.append(grp)
                    hist = pd.concat(ma_rows)

                fig = go.Figure()
                colors = px.colors.qualitative.Plotly

                for i, (lbl, grp) in enumerate(hist.groupby("label")):
                    brand_key = grp["brand"].iloc[0]
                    color = BRAND_COLORS.get(brand_key, colors[i % len(colors)])
                    fig.add_trace(go.Scatter(
                        x=grp["observed_at"], y=grp["price"],
                        name=lbl, line=dict(color=color, width=1.5),
                        mode="lines+markers",
                        marker=dict(size=3),
                        opacity=0.7,
                    ))
                    if ma_window and f"ma_{ma_window}" in grp.columns:
                        fig.add_trace(go.Scatter(
                            x=grp["observed_at"], y=grp[f"ma_{ma_window}"],
                            name=f"{lbl} ({ma_window}일MA)",
                            line=dict(color=color, width=2.5, dash="solid"),
                            mode="lines",
                        ))

                fig.update_layout(
                    height=500,
                    hovermode="x unified",
                    xaxis_title="날짜",
                    yaxis_title="가격 (USD)",
                    margin=dict(t=20),
                    legend=dict(orientation="h", y=-0.3, yanchor="top"),
                )
                st.plotly_chart(fig, use_container_width=True)

                # 요약 통계
                summary = hist.groupby("label")["price"].agg(
                    최저가="min", 최고가="max", 현재가="last", 평균가="mean"
                ).round(2)
                st.dataframe(summary, use_container_width=True)

        # 카테고리 집계 추이
        st.divider()
        st.subheader("카테고리 중앙가 추이 (브랜드별)")
        for cat in selected_categories:
            ts = load_category_timeseries(cat, primary_country, history_days)
            if ts.empty:
                continue
            ts["date"] = pd.to_datetime(ts["date"])
            ts = ts[ts["brand"].isin(selected_brands)]

            fig2 = px.line(
                ts, x="date", y="median_price", color="brand",
                color_discrete_map=BRAND_COLORS,
                title=f"{CATEGORY_LABELS[cat]} — {primary_country} 중앙 가격 추이",
                labels={"date": "", "median_price": "중앙 가격 ($)", "brand": "브랜드"},
                height=320,
            )
            fig2.update_layout(margin=dict(t=40, b=20),
                               legend=dict(orientation="h", y=1.1))
            st.plotly_chart(fig2, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# Tab 3: Competitor Compare (심층)
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.header("경쟁사 심층 비교")
    st.caption("동일 카테고리 제품의 브랜드별 가격 포지셔닝")

    df_all = load_latest_prices(selected_countries, selected_categories)

    if df_all.empty:
        st.info("데이터 없음.")
    else:
        comp_country = st.selectbox("비교 국가", selected_countries, key="comp_country")
        comp_source = st.radio("출처", ["amazon", "manufacturer"], horizontal=True)

        for cat in selected_categories:
            cat_df = df_all[
                (df_all["category"] == cat) &
                (df_all["brand"].isin(selected_brands)) &
                (df_all["source"] == comp_source) &
                (df_all["country"] == comp_country)
            ].copy()
            if cat_df.empty:
                continue

            st.subheader(f"{CATEGORY_LABELS[cat]}")
            cat_df["product"] = cat_df["model"] + " " + cat_df["capacity"].fillna("")

            # 브랜드별 가격 scatter (capacity 기준 정렬)
            cat_df["cap_num"] = pd.to_numeric(cat_df["capacity"].str.replace("TB","000").str.replace("GB",""), errors="coerce")
            cat_df = cat_df.sort_values("cap_num")

            col_chart, col_gap = st.columns([3, 2])
            with col_chart:
                fig = go.Figure()
                for brand in [b for b in ["samsung", "sandisk", "lexar"] if b in cat_df["brand"].values]:
                    bdf = cat_df[cat_df["brand"] == brand]
                    fig.add_trace(go.Scatter(
                        x=bdf["cap_num"],
                        y=bdf["price"],
                        name=BRAND_LABELS.get(brand, brand),
                        mode="lines+markers+text",
                        text=bdf["price"].apply(lambda v: f"${v:,.0f}"),
                        textposition="top center",
                        marker=dict(size=12, color=BRAND_COLORS[brand]),
                        line=dict(color=BRAND_COLORS[brand], width=2),
                    ))
                fig.update_layout(
                    xaxis_title="용량 (GB)",
                    yaxis_title="가격 ($)",
                    height=350,
                    margin=dict(t=10, b=40),
                    legend=dict(orientation="h", y=1.1),
                    hovermode="x unified",
                )
                st.plotly_chart(fig, use_container_width=True)

            with col_gap:
                # Samsung 기준 가격 차이 계산
                sam_df = cat_df[cat_df["brand"] == "samsung"][["cap_num", "price"]].rename(columns={"price": "sam_price"})
                if not sam_df.empty:
                    gap_rows = []
                    for brand in [b for b in ["sandisk", "lexar"] if b in cat_df["brand"].values]:
                        bdf = cat_df[cat_df["brand"] == brand].merge(sam_df, on="cap_num", how="inner")
                        for _, row in bdf.iterrows():
                            gap_pct = (row["price"] - row["sam_price"]) / row["sam_price"] * 100
                            gap_rows.append({
                                "브랜드": BRAND_LABELS.get(brand, brand),
                                "제품": row["product"],
                                "용량(GB)": row["cap_num"],
                                "가격($)": row["price"],
                                "Sam 대비": f"{gap_pct:+.1f}%",
                                "gap_val": gap_pct,
                            })
                    if gap_rows:
                        gap_df = pd.DataFrame(gap_rows)
                        st.markdown("**Samsung 대비 가격 격차**")

                        def color_gap(v):
                            if isinstance(v, str) and "%" in v:
                                val = float(v.replace("%","").replace("+",""))
                                color = "#d4edda" if val < 0 else "#f8d7da"
                                return f"background-color: {color}"
                            return ""

                        styled = gap_df[["브랜드","제품","가격($)","Sam 대비"]].style.applymap(
                            color_gap, subset=["Sam 대비"]
                        ).format({"가격($)": "${:.2f}"})
                        st.dataframe(styled, use_container_width=True, hide_index=True)
                else:
                    st.info("Samsung 데이터 없음 (격차 계산 불가)")

            st.divider()

        # 브랜드별 평균 가격 비교 (전체)
        st.subheader("카테고리별 평균 가격 비교")
        avg_df = df_all[
            (df_all["brand"].isin(selected_brands)) &
            (df_all["country"] == comp_country) &
            (df_all["source"] == comp_source)
        ].groupby(["category", "brand"])["price"].mean().reset_index()
        avg_df["category_label"] = avg_df["category"].map(CATEGORY_LABELS)

        if not avg_df.empty:
            fig_avg = px.bar(
                avg_df, x="category_label", y="price", color="brand",
                barmode="group",
                color_discrete_map=BRAND_COLORS,
                labels={"category_label": "카테고리", "price": "평균 가격 ($)", "brand": "브랜드"},
                height=380,
            )
            fig_avg.update_layout(legend=dict(orientation="h", y=1.1), margin=dict(t=20))
            st.plotly_chart(fig_avg, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# Tab 4: Price Gap Analysis
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.header("Price Gap Analysis")
    st.caption("Samsung을 기준(100)으로 경쟁사 가격 지수 추이")

    hist_all = load_all_history(selected_categories, [primary_country], history_days)

    if hist_all.empty:
        st.info("시계열 데이터 없음.")
    else:
        hist_all["observed_at"] = pd.to_datetime(hist_all["observed_at"])
        hist_all["date"] = hist_all["observed_at"].dt.date

        gap_tab1, gap_tab2 = st.tabs(["📉 가격 지수 추이", "📊 프리미엄/할인 분포"])

        with gap_tab1:
            # 날짜별 브랜드 중앙가 계산 → Samsung = 100 기준 지수
            idx_rows = []
            for cat in selected_categories:
                cat_hist = hist_all[hist_all["category"] == cat]
                daily = cat_hist.groupby(["date", "brand"])["price"].median().reset_index()
                pivot_d = daily.pivot(index="date", columns="brand", values="price")

                if "samsung" not in pivot_d.columns:
                    continue

                for brand in [b for b in ["sandisk", "lexar"] if b in pivot_d.columns]:
                    idx_series = (pivot_d[brand] / pivot_d["samsung"] * 100).dropna()
                    for dt, val in idx_series.items():
                        idx_rows.append({
                            "date": dt, "brand": brand,
                            "category": cat, "index": val
                        })

            if idx_rows:
                idx_df = pd.DataFrame(idx_rows)
                idx_df = idx_df[idx_df["brand"].isin(selected_brands)]

                for cat in selected_categories:
                    cat_idx = idx_df[idx_df["category"] == cat]
                    if cat_idx.empty:
                        continue

                    fig_idx = go.Figure()
                    fig_idx.add_hline(y=100, line_dash="dot", line_color="navy",
                                      annotation_text="Samsung = 100")
                    fig_idx.add_hrect(y0=90, y1=110, fillcolor="lightblue", opacity=0.1,
                                      annotation_text="±10% 구간")

                    for brand in [b for b in ["sandisk", "lexar"] if b in cat_idx["brand"].values]:
                        bdf = cat_idx[cat_idx["brand"] == brand].sort_values("date")
                        # 7일 이동평균
                        bdf["ma7"] = bdf["index"].rolling(7, min_periods=1).mean()
                        fig_idx.add_trace(go.Scatter(
                            x=bdf["date"], y=bdf["index"],
                            name=BRAND_LABELS.get(brand, brand),
                            mode="lines", opacity=0.3,
                            line=dict(color=BRAND_COLORS[brand], width=1),
                            showlegend=False,
                        ))
                        fig_idx.add_trace(go.Scatter(
                            x=bdf["date"], y=bdf["ma7"],
                            name=f"{BRAND_LABELS.get(brand, brand)} (7일MA)",
                            mode="lines",
                            line=dict(color=BRAND_COLORS[brand], width=2.5),
                        ))

                    fig_idx.update_layout(
                        title=f"{CATEGORY_LABELS[cat]} — Samsung 기준 가격 지수 ({primary_country})",
                        yaxis_title="가격 지수 (Samsung=100)",
                        xaxis_title="",
                        height=380,
                        margin=dict(t=40, b=20),
                        hovermode="x unified",
                        legend=dict(orientation="h", y=-0.3, yanchor="top"),
                    )
                    st.plotly_chart(fig_idx, use_container_width=True)
            else:
                st.info("Samsung 데이터가 있어야 지수 계산이 가능합니다.")

        with gap_tab2:
            # 최신 시점 가격 격차 분포
            df_latest2 = load_latest_prices([primary_country], selected_categories)
            if not df_latest2.empty:
                sam_prices = df_latest2[df_latest2["brand"] == "samsung"][
                    ["category", "capacity", "price"]
                ].rename(columns={"price": "sam_price"})

                comp_prices = df_latest2[
                    (df_latest2["brand"].isin(["sandisk", "lexar"])) &
                    (df_latest2["source"] == "amazon")
                ]

                merged = comp_prices.merge(sam_prices, on=["category", "capacity"], how="inner")
                if not merged.empty:
                    merged["gap_pct"] = (merged["price"] - merged["sam_price"]) / merged["sam_price"] * 100
                    merged["category_label"] = merged["category"].map(CATEGORY_LABELS)

                    fig_box = px.box(
                        merged, x="category_label", y="gap_pct", color="brand",
                        color_discrete_map=BRAND_COLORS,
                        title="Samsung 대비 가격 격차 분포 (%) — Amazon 현재",
                        labels={"category_label": "카테고리", "gap_pct": "가격 격차 (%)", "brand": "브랜드"},
                        height=400,
                    )
                    fig_box.add_hline(y=0, line_dash="dot", line_color="navy")
                    fig_box.update_layout(legend=dict(orientation="h", y=1.1))
                    st.plotly_chart(fig_box, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# Tab 5: Country Compare
# ═══════════════════════════════════════════════════════════════
with tab5:
    st.header("국가별 가격 비교")
    st.caption("동일 제품의 국가별 가격 차이 (가격 정책, 환율 영향 포함)")

    skus_df2 = load_all_skus()
    if skus_df2.empty:
        st.info("SKU 데이터 없음.")
    else:
        sku_opts = {
            row["sku_id"]: f"[{BRAND_LABELS.get(row['brand'], row['brand']).upper()}] {row['model']} {row['capacity']}"
            for _, row in skus_df2[skus_df2["brand"].isin(selected_brands)].iterrows()
        }
        country_sku = st.selectbox("SKU 선택", list(sku_opts.keys()),
                                    format_func=lambda x: sku_opts.get(x, x))

        if country_sku:
            all_countries_hist = load_price_history([country_sku], ["US", "KR", "JP", "DE"], history_days)

            if all_countries_hist.empty:
                st.info("해당 SKU의 국가별 데이터 없음.")
            else:
                all_countries_hist["observed_at"] = pd.to_datetime(all_countries_hist["observed_at"])

                # 국가별 시계열
                fig_c = px.line(
                    all_countries_hist,
                    x="observed_at", y="price", color="country",
                    title=f"{sku_opts.get(country_sku, country_sku)} — 국가별 가격 추이",
                    labels={"observed_at": "", "price": "가격 (현지통화)", "country": "국가"},
                    height=400,
                )
                fig_c.update_layout(hovermode="x unified", margin=dict(t=40))
                st.plotly_chart(fig_c, use_container_width=True)

                # 국가별 최신 가격 요약
                latest_by_country = all_countries_hist.sort_values("observed_at").groupby(
                    ["country", "currency"]
                ).last().reset_index()[["country", "currency", "price", "observed_at"]]
                latest_by_country.columns = ["국가", "통화", "최신가격", "수집일시"]
                latest_by_country["최신가격"] = latest_by_country["최신가격"].apply(
                    lambda v: f"{v:,.2f}" if pd.notna(v) else "—"
                )
                st.dataframe(latest_by_country, use_container_width=True, hide_index=True)

                # 국가 간 가격 히트맵 (SKU × 국가)
                st.divider()
                st.subheader(f"카테고리 전체 국가별 가격 히트맵")
                cat_of_sku = skus_df2[skus_df2["sku_id"] == country_sku]["category"].values
                if len(cat_of_sku) > 0:
                    df_heatmap = load_latest_prices(["US", "KR", "JP", "DE"], [cat_of_sku[0]])
                    if not df_heatmap.empty:
                        df_hm = df_heatmap[
                            (df_heatmap["brand"].isin(selected_brands)) &
                            (df_heatmap["source"] == "amazon")
                        ].copy()
                        df_hm["product"] = df_hm["model"] + " " + df_hm["capacity"].fillna("")
                        pivot_hm = df_hm.pivot_table(
                            index="product", columns="country", values="price", aggfunc="min"
                        )
                        fig_hm = px.imshow(
                            pivot_hm, text_auto=".0f",
                            title=f"{CATEGORY_LABELS[cat_of_sku[0]]} Amazon 가격 히트맵 (현지통화)",
                            color_continuous_scale="RdYlGn_r",
                            height=350,
                        )
                        st.plotly_chart(fig_hm, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# Tab 6: Alerts
# ═══════════════════════════════════════════════════════════════
with tab6:
    st.header("가격 이상 변동 알림")

    col_t, col_d = st.columns(2)
    alert_threshold = col_t.slider("변동 임계값 (%)", 5, 50, 10)
    alert_days = col_d.selectbox("탐지 기간", [7, 14, 30], index=1, format_func=lambda x: f"최근 {x}일")

    alerts = load_price_alerts(alert_threshold, alert_days)

    if alerts.empty:
        st.success(f"최근 {alert_days}일 내 ±{alert_threshold}% 이상 변동 없음.")
    else:
        # 요약 메트릭
        up_alerts = alerts[alerts["change_pct"] > 0]
        dn_alerts = alerts[alerts["change_pct"] < 0]
        ca, cb, cc = st.columns(3)
        ca.metric("전체 이상 변동", len(alerts))
        cb.metric("🔴 가격 인상", len(up_alerts))
        cc.metric("🟢 가격 인하", len(dn_alerts))

        st.divider()

        # 폭포차트: 변동폭 순위
        alerts_sorted = alerts.sort_values("change_pct", key=abs, ascending=False).head(20)
        alerts_sorted["label"] = alerts_sorted["brand"] + " " + alerts_sorted["model"].fillna("") + " " + \
                                   alerts_sorted["capacity"].fillna("") + f"\n({alerts_sorted['country']})"
        fig_alert = go.Figure(go.Bar(
            x=alerts_sorted["change_pct"],
            y=alerts_sorted["label"],
            orientation="h",
            marker_color=alerts_sorted["change_pct"].apply(
                lambda v: "#d32f2f" if v > 0 else "#2e7d32"
            ),
            text=alerts_sorted["change_pct"].apply(lambda v: f"{v:+.1f}%"),
            textposition="outside",
        ))
        fig_alert.update_layout(
            title=f"가격 변동 Top {len(alerts_sorted)} (최근 {alert_days}일)",
            xaxis_title="변동률 (%)",
            height=max(300, len(alerts_sorted) * 28),
            margin=dict(l=200, r=80, t=40, b=20),
        )
        st.plotly_chart(fig_alert, use_container_width=True)

        # 상세 테이블
        display = alerts_sorted[[
            "brand", "model", "capacity", "country", "source",
            "prev_price", "price", "change_pct", "observed_at"
        ]].copy()
        display.columns = ["브랜드", "모델", "용량", "국가", "출처",
                            "이전가격($)", "현재가격($)", "변동률(%)", "수집일시"]
        display["수집일시"] = pd.to_datetime(display["수집일시"]).dt.strftime("%m/%d %H:%M")

        def highlight_change(row):
            val = row["변동률(%)"]
            if pd.isna(val):
                return [""] * len(row)
            color = "#ffd7d7" if val > 0 else "#d7ffd7"
            return [f"background-color: {color}" if col == "변동률(%)" else "" for col in row.index]

        st.dataframe(
            display.style.apply(highlight_change, axis=1),
            use_container_width=True, hide_index=True,
        )

# ── 푸터 ──────────────────────────────────────────────────────
st.sidebar.divider()
st.sidebar.caption(f"Powered by Crawling Pipeline\n© 2026 SanDisk Marketing Intelligence")
if st.sidebar.button("🔄 캐시 초기화"):
    st.cache_data.clear()
    st.rerun()
