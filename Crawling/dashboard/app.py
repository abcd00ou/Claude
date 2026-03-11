"""
Price Intelligence Dashboard — v2
Samsung vs SanDisk 실시간 가격 Gap 중심

탭 구성:
  1. 📊 Gap Overview       — Samsung vs SanDisk 핵심 경쟁 가격 Gap (기본 화면)
  2. 📈 Time Series        — SKU별 실시간 가격 추이
  3. ⚔️  Rival Matchup     — 제품 대 제품 심층 비교 (용량별)
  4. 🔍 Price Gap Trend    — Samsung 대비 가격 지수 추이
  5. 🌍 Country Compare    — 국가별 동일 제품 가격 비교
  6. 🚨 Alerts             — 이상 변동 알림
"""
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
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

# ── 상수 ─────────────────────────────────────────────────────
BRAND_COLORS = {
    "samsung": "#1428A0",
    "sandisk": "#E2231A",
    "lexar":   "#F7941D",
}
BRAND_LABELS = {
    "samsung": "Samsung",
    "sandisk": "SanDisk",
    "lexar":   "Lexar",
}
BRAND_ORDER = ["samsung", "sandisk", "lexar"]  # 고정 순서

CATEGORY_LABELS = {
    "portable_ssd": "Portable SSD",
    "internal_ssd": "Internal SSD",
    "microsd":      "microSD",
}

# ── 제품 대 제품 경쟁 매핑 ────────────────────────────────────
RIVAL_PAIRS = [
    {
        "id":             "portable_10g",
        "category":       "portable_ssd",
        "tier":           "Portable SSD — 10Gbps 티어",
        "samsung_models": ["T7", "T7 Shield"],
        "rival_brand":    "sandisk",
        "rival_models":   ["Extreme"],
        "note":           "T7·T7 Shield (USB 3.2 Gen2, IP65) vs SanDisk Extreme (USB 3.2 Gen2, IP55)",
    },
    {
        "id":             "portable_20g",
        "category":       "portable_ssd",
        "tier":           "Portable SSD — 20Gbps 티어",
        "samsung_models": ["T9"],
        "rival_brand":    "sandisk",
        "rival_models":   ["Extreme Pro"],
        "note":           "T9 (USB 3.2 Gen2×2, 2000 MB/s) vs SanDisk Extreme Pro (USB 3.2 Gen2×2, 2000 MB/s)",
    },
    {
        "id":             "internal_pcie4",
        "category":       "internal_ssd",
        "tier":           "Internal SSD — PCIe 4.0 (PS5 호환)",
        "samsung_models": ["990 Pro"],
        "rival_brand":    "sandisk",
        "rival_models":   ["WD_BLACK SN850X"],
        "note":           "990 Pro (PCIe 4.0, 7450 MB/s) vs WD_BLACK SN850X (PCIe 4.0, 7300 MB/s)",
    },
]

# ── Plotly 공통 레이아웃 ─────────────────────────────────────
def _chart_layout(**kwargs):
    base = dict(
        font=dict(family="Inter, system-ui, sans-serif", size=12, color="#1a1a2e"),
        paper_bgcolor="white",
        plot_bgcolor="#F8FAFF",
        margin=dict(t=48, b=48, l=60, r=24),
        legend=dict(orientation="h", y=1.12, x=0, bgcolor="rgba(0,0,0,0)",
                    bordercolor="rgba(0,0,0,0.1)", borderwidth=1),
        hovermode="x unified",
        hoverlabel=dict(bgcolor="white", bordercolor="#dee2e6", font_size=12),
        xaxis=dict(gridcolor="#E8EDF5", linecolor="#dee2e6"),
        yaxis=dict(gridcolor="#E8EDF5", linecolor="#dee2e6"),
    )
    base.update(kwargs)
    return base


def _gap_color(v: float) -> str:
    """양수(SanDisk 비쌈)=초록, 음수(SanDisk 쌈)=빨강."""
    return "#d4edda" if v > 0 else "#f8d7da"


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


# ── 헬퍼: capacity → 숫자 정렬용 ──────────────────────────────
def cap_to_num(cap_series: pd.Series) -> pd.Series:
    return pd.to_numeric(
        cap_series.str.replace("TB", "000", regex=False)
                  .str.replace("GB", "", regex=False),
        errors="coerce"
    )


# ── 헬퍼: rival pair gap 테이블 생성 ────────────────────────
def build_gap_table(df: pd.DataFrame, pair: dict, country: str, source: str = "amazon") -> pd.DataFrame:
    """RIVAL_PAIR 기준으로 용량별 Samsung vs Rival 가격 비교 테이블 반환."""
    df_c = df[(df["category"] == pair["category"]) &
              (df["country"] == country) &
              (df["source"] == source)].copy()
    if df_c.empty:
        return pd.DataFrame()

    df_c["cap_num"] = cap_to_num(df_c["capacity"])

    sam = df_c[
        (df_c["brand"] == "samsung") &
        (df_c["model"].isin(pair["samsung_models"]))
    ][["model", "capacity", "cap_num", "price"]].copy()
    sam.columns = ["sam_model", "capacity", "cap_num", "sam_price"]

    rival = df_c[
        (df_c["brand"] == pair["rival_brand"]) &
        (df_c["model"].isin(pair["rival_models"]))
    ][["model", "capacity", "cap_num", "price"]].copy()
    rival.columns = ["rival_model", "capacity", "cap_num", "rival_price"]

    merged = pd.merge(sam, rival, on=["capacity", "cap_num"], how="inner")
    if merged.empty:
        return pd.DataFrame()

    merged["gap_usd"] = merged["rival_price"] - merged["sam_price"]
    merged["gap_pct"] = merged["gap_usd"] / merged["sam_price"] * 100
    return merged.sort_values("cap_num")


# ── 사이드바 ──────────────────────────────────────────────────
st.sidebar.title("📊 Price Intelligence")
st.sidebar.caption(f"Samsung · SanDisk · Lexar  |  {datetime.now().strftime('%Y-%m-%d %H:%M')}")
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
    "브랜드", BRAND_ORDER,
    format_func=lambda x: BRAND_LABELS.get(x, x),
    default=BRAND_ORDER,
)
history_days = st.sidebar.selectbox(
    "분석 기간", [30, 60, 90, 180, 365], index=2,
    format_func=lambda x: f"최근 {x}일"
)
primary_country = selected_countries[0] if selected_countries else "US"

if not selected_countries:
    selected_countries = ["US"]
if not selected_categories:
    selected_categories = list(CATEGORY_LABELS.keys())

# ── 탭 ───────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Gap Overview",
    "📈 Time Series",
    "⚔️ Rival Matchup",
    "🔍 Gap Trend",
    "🌍 Country Compare",
    "🚨 Alerts",
])


# ═══════════════════════════════════════════════════════════════
# Tab 1: Gap Overview — Samsung vs SanDisk 실시간 가격 Gap
# ═══════════════════════════════════════════════════════════════
with tab1:
    st.header("Samsung vs SanDisk 실시간 가격 Gap")
    st.caption(f"기준: Amazon {primary_country} 최신 가격")

    df_latest = load_latest_prices(selected_countries, selected_categories)
    if df_latest.empty:
        st.info("데이터 없음. `python run_pipeline.py` 실행 후 확인하세요.")
        st.stop()

    # KPI 카드
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("전체 SKU", df_latest["sku_id"].nunique())
    c2.metric("Samsung SKU", len(df_latest[df_latest["brand"] == "samsung"]["sku_id"].unique()))
    c3.metric("SanDisk SKU", len(df_latest[df_latest["brand"] == "sandisk"]["sku_id"].unique()))
    c4.metric("Lexar SKU",   len(df_latest[df_latest["brand"] == "lexar"]["sku_id"].unique()))
    latest_ts = pd.to_datetime(df_latest["observed_at"]).max()
    c5.metric("마지막 수집", latest_ts.strftime("%m/%d %H:%M") if pd.notna(latest_ts) else "—")

    st.divider()

    # ── 핵심 경쟁 쌍별 Gap 비교 ───────────────────────────────
    for pair in RIVAL_PAIRS:
        if pair["category"] not in selected_categories:
            continue

        rival_label = BRAND_LABELS.get(pair["rival_brand"], pair["rival_brand"])
        sam_models_str = " / ".join(pair["samsung_models"])
        rival_models_str = " / ".join(pair["rival_models"])

        st.subheader(f"Samsung {sam_models_str}  vs  {rival_label} {rival_models_str}")
        st.caption(pair["note"])

        gap_df = build_gap_table(df_latest, pair, primary_country, "amazon")

        if gap_df.empty:
            st.info(f"데이터 없음 — {pair['tier']}")
            st.divider()
            continue

        col_chart, col_tbl = st.columns([3, 2])

        with col_chart:
            fig = go.Figure()
            # Samsung bars (각 모델별 색상 구분)
            for sam_model in gap_df["sam_model"].unique():
                sub = gap_df[gap_df["sam_model"] == sam_model]
                fig.add_trace(go.Bar(
                    name=f"Samsung {sam_model}",
                    x=sub["capacity"],
                    y=sub["sam_price"],
                    marker_color=BRAND_COLORS["samsung"],
                    marker_line=dict(color="white", width=1),
                    text=sub["sam_price"].apply(lambda v: f"${v:,.0f}"),
                    textposition="outside",
                    textfont=dict(size=11),
                ))
            # Rival bars
            for rival_model in gap_df["rival_model"].unique():
                sub = gap_df[gap_df["rival_model"] == rival_model]
                fig.add_trace(go.Bar(
                    name=f"{rival_label} {rival_model}",
                    x=sub["capacity"],
                    y=sub["rival_price"],
                    marker_color=BRAND_COLORS[pair["rival_brand"]],
                    marker_line=dict(color="white", width=1),
                    text=sub["rival_price"].apply(lambda v: f"${v:,.0f}"),
                    textposition="outside",
                    textfont=dict(size=11),
                ))
            fig.update_layout(
                **_chart_layout(
                    barmode="group",
                    height=340,
                    xaxis_title="용량",
                    yaxis_title="가격 (USD)",
                    title=f"{pair['tier']}",
                    title_font=dict(size=13),
                )
            )
            fig.update_yaxes(rangemode="tozero")
            st.plotly_chart(fig, use_container_width=True)

        with col_tbl:
            st.markdown("**용량별 가격 Gap**")
            rows = []
            for _, r in gap_df.iterrows():
                rows.append({
                    "용량":                r["capacity"],
                    f"Samsung ({r['sam_model']})":  f"${r['sam_price']:,.2f}",
                    f"SanDisk ({r['rival_model']})": f"${r['rival_price']:,.2f}",
                    "Gap ($)":             f"{r['gap_usd']:+,.2f}",
                    "Gap (%)":             f"{r['gap_pct']:+.1f}%",
                    "_gap_val":            r["gap_pct"],
                })
            tbl_df = pd.DataFrame(rows)

            def _style_gap(row):
                styles = [""] * len(row)
                idx_gap = list(tbl_df.columns).index("Gap (%)")
                v = row["_gap_val"]
                color = _gap_color(v)
                styles[idx_gap - 1] = f"background-color: {color}"
                styles[idx_gap] = f"background-color: {color}"
                return styles

            display_df = tbl_df.drop(columns=["_gap_val"])
            st.dataframe(
                display_df.style.apply(
                    lambda row: [
                        f"background-color: {_gap_color(tbl_df.loc[row.name, '_gap_val'])}"
                        if col in ("Gap ($)", "Gap (%)")
                        else ""
                        for col in display_df.columns
                    ],
                    axis=1,
                ),
                use_container_width=True,
                hide_index=True,
            )
            # Gap 요약
            if not gap_df.empty:
                avg_gap = gap_df["gap_pct"].mean()
                direction = "SanDisk가 평균 더 비쌈 ▲" if avg_gap > 0 else "SanDisk가 평균 더 쌈 ▼"
                st.info(f"평균 Gap: **{avg_gap:+.1f}%** — {direction}")

        st.divider()

    # ── Lexar 포함 전체 카테고리 개요 (보조) ─────────────────────
    with st.expander("📋 전체 카테고리 가격 개요 (Samsung · SanDisk · Lexar)", expanded=False):
        for cat in selected_categories:
            cat_df = df_latest[
                (df_latest["category"] == cat) &
                (df_latest["source"] == "amazon") &
                (df_latest["country"] == primary_country)
            ].copy()
            if cat_df.empty:
                continue
            st.subheader(f"{CATEGORY_LABELS[cat]} — Amazon {primary_country}")
            cat_df["product_label"] = cat_df["model"] + " " + cat_df["capacity"].fillna("")
            cat_df["cap_num"] = cap_to_num(cat_df["capacity"])
            cat_df = cat_df.sort_values("cap_num")

            pivot = cat_df.pivot_table(
                index="product_label", columns="brand", values="price", aggfunc="min"
            ).reset_index()
            brands_present = [b for b in BRAND_ORDER if b in pivot.columns]
            if brands_present:
                fig = go.Figure()
                for brand in brands_present:
                    fig.add_trace(go.Bar(
                        name=BRAND_LABELS.get(brand, brand),
                        x=pivot["product_label"],
                        y=pivot[brand],
                        marker_color=BRAND_COLORS[brand],
                        marker_line=dict(color="white", width=1),
                        text=pivot[brand].apply(lambda v: f"${v:,.0f}" if pd.notna(v) else ""),
                        textposition="outside",
                        textfont=dict(size=10),
                    ))
                fig.update_layout(**_chart_layout(barmode="group", height=360,
                                                  xaxis_tickangle=-25))
                st.plotly_chart(fig, use_container_width=True)

            display_cols = ["product_label"] + [b for b in BRAND_ORDER if b in pivot.columns]
            rename_map = {
                "product_label": "제품",
                "samsung": "Samsung ($)",
                "sandisk": "SanDisk ($)",
                "lexar": "Lexar ($)",
            }
            st.dataframe(
                pivot[display_cols].rename(columns=rename_map)
                .style.format(
                    "{:.2f}",
                    subset=[v for k, v in rename_map.items() if k != "product_label" and v in pivot.rename(columns=rename_map).columns],
                    na_rep="—",
                ),
                use_container_width=True, hide_index=True,
            )


# ═══════════════════════════════════════════════════════════════
# Tab 2: Time Series — 실시간 가격 추이 (이동평균 없음)
# ═══════════════════════════════════════════════════════════════
with tab2:
    st.header("실시간 가격 추이")

    skus_df = load_all_skus()
    if skus_df.empty:
        st.info("SKU 데이터 없음.")
    else:
        col_left, col_right = st.columns([3, 1])
        with col_left:
            # Brand order: Samsung → SanDisk → Lexar
            ordered_skus = skus_df[skus_df["brand"].isin(selected_brands)].copy()
            ordered_skus["brand_order"] = ordered_skus["brand"].map(
                {b: i for i, b in enumerate(BRAND_ORDER)}
            )
            ordered_skus = ordered_skus.sort_values(["brand_order", "model", "capacity"])
            sku_options = {
                row["sku_id"]: f"[{BRAND_LABELS.get(row['brand'], row['brand'])}] {row['model']} {row['capacity']}"
                for _, row in ordered_skus.iterrows()
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

        if selected_skus:
            hist = load_price_history(selected_skus, [ts_country], history_days)
            if hist.empty:
                st.info("가격 기록 없음.")
            else:
                hist["observed_at"] = pd.to_datetime(hist["observed_at"])
                hist["label"] = (
                    hist["brand"].apply(lambda b: BRAND_LABELS.get(b, b))
                    + " " + hist["model"]
                    + " " + hist["capacity"].fillna("")
                )
                hist = hist.sort_values("observed_at")

                fig = go.Figure()
                for lbl, grp in hist.groupby("label", sort=False):
                    brand_key = grp["brand"].iloc[0]
                    color = BRAND_COLORS.get(brand_key, "#888")
                    fig.add_trace(go.Scatter(
                        x=grp["observed_at"], y=grp["price"],
                        name=lbl,
                        line=dict(color=color, width=2),
                        mode="lines+markers",
                        marker=dict(size=4, color=color),
                    ))

                fig.update_layout(
                    **_chart_layout(
                        height=520,
                        xaxis_title="날짜",
                        yaxis_title="가격 (USD)",
                    )
                )
                st.plotly_chart(fig, use_container_width=True)

                # 요약 통계
                summary = hist.groupby("label")["price"].agg(
                    최저가="min", 최고가="max", 현재가="last", 평균가="mean"
                ).round(2)
                st.dataframe(summary, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# Tab 3: Rival Matchup — 제품 대 제품 심층 비교
# ═══════════════════════════════════════════════════════════════
with tab3:
    st.header("제품 대 제품 심층 비교")
    st.caption("Samsung 제품 vs 지정 경쟁 제품 — 용량별 가격 및 Gap")

    df_all = load_latest_prices(selected_countries, selected_categories)

    if df_all.empty:
        st.info("데이터 없음.")
    else:
        col_country, col_source = st.columns(2)
        comp_country = col_country.selectbox("비교 국가", selected_countries, key="comp_country")
        comp_source  = col_source.radio("출처", ["amazon", "manufacturer"], horizontal=True)

        # ── 핵심 경쟁 쌍 ─────────────────────────────────────
        st.subheader("핵심 경쟁 쌍 비교")
        for pair in RIVAL_PAIRS:
            if pair["category"] not in selected_categories:
                continue

            rival_label = BRAND_LABELS.get(pair["rival_brand"], pair["rival_brand"])
            sam_models_str  = " / ".join(pair["samsung_models"])
            rival_models_str = " / ".join(pair["rival_models"])

            with st.container():
                st.markdown(
                    f"### Samsung **{sam_models_str}**  ←→  {rival_label} **{rival_models_str}**"
                )
                st.caption(pair["note"])

                gap_df = build_gap_table(df_all, pair, comp_country, comp_source)

                if gap_df.empty:
                    st.info(f"데이터 없음 — 출처: {comp_source}")
                    st.divider()
                    continue

                col_bar, col_gap = st.columns([3, 2])

                with col_bar:
                    fig = go.Figure()
                    for sam_model in gap_df["sam_model"].unique():
                        sub = gap_df[gap_df["sam_model"] == sam_model]
                        fig.add_trace(go.Bar(
                            name=f"Samsung {sam_model}",
                            x=sub["capacity"],
                            y=sub["sam_price"],
                            marker_color=BRAND_COLORS["samsung"],
                            marker_line=dict(color="white", width=1.5),
                            text=sub["sam_price"].apply(lambda v: f"${v:,.0f}"),
                            textposition="outside",
                            textfont=dict(size=11, color=BRAND_COLORS["samsung"]),
                        ))
                    for rival_model in gap_df["rival_model"].unique():
                        sub = gap_df[gap_df["rival_model"] == rival_model]
                        fig.add_trace(go.Bar(
                            name=f"{rival_label} {rival_model}",
                            x=sub["capacity"],
                            y=sub["rival_price"],
                            marker_color=BRAND_COLORS[pair["rival_brand"]],
                            marker_line=dict(color="white", width=1.5),
                            text=sub["rival_price"].apply(lambda v: f"${v:,.0f}"),
                            textposition="outside",
                            textfont=dict(size=11, color=BRAND_COLORS[pair["rival_brand"]]),
                        ))
                    fig.update_layout(
                        **_chart_layout(
                            barmode="group",
                            height=360,
                            xaxis_title="용량",
                            yaxis_title="가격 (USD)",
                        )
                    )
                    fig.update_yaxes(rangemode="tozero")
                    st.plotly_chart(fig, use_container_width=True)

                with col_gap:
                    # Gap 워터폴 스타일 바
                    fig_gap = go.Figure()
                    colors = [BRAND_COLORS["sandisk"] if v > 0 else BRAND_COLORS["samsung"]
                              for v in gap_df["gap_pct"]]
                    fig_gap.add_trace(go.Bar(
                        x=gap_df["capacity"],
                        y=gap_df["gap_pct"],
                        marker_color=colors,
                        marker_line=dict(color="white", width=1),
                        text=gap_df["gap_pct"].apply(lambda v: f"{v:+.1f}%"),
                        textposition="outside",
                        textfont=dict(size=12),
                    ))
                    fig_gap.add_hline(y=0, line_dash="dot", line_color="#888")
                    fig_gap.update_layout(
                        **_chart_layout(
                            height=200,
                            xaxis_title="용량",
                            yaxis_title="Gap (%)",
                            title="SanDisk 가격 차이 (Samsung 대비, + = SanDisk 더 비쌈)",
                            title_font=dict(size=11),
                            showlegend=False,
                        )
                    )
                    st.plotly_chart(fig_gap, use_container_width=True)

                    # 상세 수치 테이블
                    tbl_rows = []
                    for _, r in gap_df.iterrows():
                        tbl_rows.append({
                            "용량": r["capacity"],
                            f"Samsung ({r['sam_model']})": f"${r['sam_price']:,.2f}",
                            f"SanDisk ({r['rival_model']})": f"${r['rival_price']:,.2f}",
                            "Gap $": f"{r['gap_usd']:+,.2f}",
                            "Gap %": f"{r['gap_pct']:+.1f}%",
                            "_v": r["gap_pct"],
                        })
                    tbl = pd.DataFrame(tbl_rows)
                    disp = tbl.drop(columns=["_v"])
                    st.dataframe(
                        disp.style.apply(
                            lambda row: [
                                f"background-color: {_gap_color(tbl.loc[row.name, '_v'])}"
                                if col in ("Gap $", "Gap %") else ""
                                for col in disp.columns
                            ],
                            axis=1,
                        ),
                        use_container_width=True, hide_index=True,
                    )

            st.divider()

        # ── Lexar 포함 전체 카테고리 비교 ────────────────────
        st.subheader("전체 브랜드 용량별 가격 비교")
        for cat in [c for c in selected_categories if c in df_all["category"].values]:
            cat_df = df_all[
                (df_all["category"] == cat) &
                (df_all["brand"].isin(selected_brands)) &
                (df_all["source"] == comp_source) &
                (df_all["country"] == comp_country)
            ].copy()
            if cat_df.empty:
                continue

            st.markdown(f"**{CATEGORY_LABELS[cat]}**")
            cat_df["cap_num"] = cap_to_num(cat_df["capacity"])
            cat_df = cat_df.sort_values("cap_num")

            fig_all = go.Figure()
            for brand in [b for b in BRAND_ORDER if b in cat_df["brand"].values]:
                bdf = cat_df[cat_df["brand"] == brand]
                fig_all.add_trace(go.Scatter(
                    x=bdf["cap_num"],
                    y=bdf["price"],
                    name=BRAND_LABELS.get(brand, brand),
                    mode="lines+markers+text",
                    text=bdf["model"] + " " + bdf["capacity"].fillna(""),
                    textposition="top center",
                    textfont=dict(size=10),
                    marker=dict(size=10, color=BRAND_COLORS[brand]),
                    line=dict(color=BRAND_COLORS[brand], width=2),
                ))
            fig_all.update_layout(
                **_chart_layout(
                    height=360,
                    xaxis_title="용량 (GB)",
                    yaxis_title="가격 ($)",
                )
            )
            st.plotly_chart(fig_all, use_container_width=True)


# ═══════════════════════════════════════════════════════════════
# Tab 4: Price Gap Trend
# ═══════════════════════════════════════════════════════════════
with tab4:
    st.header("Price Gap Trend")
    st.caption("Samsung을 기준(100)으로 경쟁사 가격 지수 추이")

    hist_all = load_all_history(selected_categories, [primary_country], history_days)

    if hist_all.empty:
        st.info("시계열 데이터 없음.")
    else:
        hist_all["observed_at"] = pd.to_datetime(hist_all["observed_at"])
        hist_all["date"] = hist_all["observed_at"].dt.date

        gap_tab1, gap_tab2 = st.tabs(["📉 가격 지수 추이", "📊 프리미엄/할인 분포"])

        with gap_tab1:
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
                    fig_idx.add_hrect(y0=90, y1=110, fillcolor="lightblue", opacity=0.08)

                    for brand in [b for b in ["sandisk", "lexar"] if b in cat_idx["brand"].values]:
                        bdf = cat_idx[cat_idx["brand"] == brand].sort_values("date")
                        fig_idx.add_trace(go.Scatter(
                            x=bdf["date"], y=bdf["index"],
                            name=BRAND_LABELS.get(brand, brand),
                            mode="lines",
                            line=dict(color=BRAND_COLORS[brand], width=2.5),
                        ))

                    fig_idx.update_layout(
                        **_chart_layout(
                            title=f"{CATEGORY_LABELS[cat]} — Samsung 기준 가격 지수 ({primary_country})",
                            yaxis_title="가격 지수 (Samsung=100)",
                            height=380,
                        )
                    )
                    st.plotly_chart(fig_idx, use_container_width=True)
            else:
                st.info("Samsung 데이터가 있어야 지수 계산이 가능합니다.")

        with gap_tab2:
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
                    # Samsung → SanDisk → Lexar 순 정렬
                    merged["brand_order"] = merged["brand"].map({b: i for i, b in enumerate(BRAND_ORDER)})
                    merged = merged.sort_values("brand_order")

                    fig_box = go.Figure()
                    for brand in [b for b in ["sandisk", "lexar"] if b in merged["brand"].values]:
                        bm = merged[merged["brand"] == brand]
                        fig_box.add_trace(go.Box(
                            x=bm["category_label"],
                            y=bm["gap_pct"],
                            name=BRAND_LABELS.get(brand, brand),
                            marker_color=BRAND_COLORS[brand],
                            boxmean=True,
                        ))
                    fig_box.add_hline(y=0, line_dash="dot", line_color="navy")
                    fig_box.update_layout(
                        **_chart_layout(
                            title="Samsung 대비 가격 격차 분포 (%) — Amazon 현재",
                            yaxis_title="가격 격차 (%)",
                            height=420,
                            boxmode="group",
                        )
                    )
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
        # Brand order: Samsung → SanDisk → Lexar
        ordered2 = skus_df2[skus_df2["brand"].isin(selected_brands)].copy()
        ordered2["brand_order"] = ordered2["brand"].map({b: i for i, b in enumerate(BRAND_ORDER)})
        ordered2 = ordered2.sort_values(["brand_order", "model", "capacity"])
        sku_opts = {
            row["sku_id"]: f"[{BRAND_LABELS.get(row['brand'], row['brand'])}] {row['model']} {row['capacity']}"
            for _, row in ordered2.iterrows()
        }
        country_sku = st.selectbox("SKU 선택", list(sku_opts.keys()),
                                   format_func=lambda x: sku_opts.get(x, x))

        if country_sku:
            all_countries_hist = load_price_history([country_sku], ["US", "KR", "JP", "DE"], history_days)

            if all_countries_hist.empty:
                st.info("해당 SKU의 국가별 데이터 없음.")
            else:
                all_countries_hist["observed_at"] = pd.to_datetime(all_countries_hist["observed_at"])

                fig_c = go.Figure()
                for country, grp in all_countries_hist.groupby("country"):
                    grp = grp.sort_values("observed_at")
                    fig_c.add_trace(go.Scatter(
                        x=grp["observed_at"], y=grp["price"],
                        name=country, mode="lines+markers",
                        marker=dict(size=4),
                        line=dict(width=2),
                    ))
                fig_c.update_layout(
                    **_chart_layout(
                        title=f"{sku_opts.get(country_sku, country_sku)} — 국가별 가격 추이",
                        height=420,
                        yaxis_title="가격 (현지통화)",
                    )
                )
                st.plotly_chart(fig_c, use_container_width=True)

                latest_by_country = all_countries_hist.sort_values("observed_at").groupby(
                    ["country", "currency"]
                ).last().reset_index()[["country", "currency", "price", "observed_at"]]
                latest_by_country.columns = ["국가", "통화", "최신가격", "수집일시"]
                latest_by_country["최신가격"] = latest_by_country["최신가격"].apply(
                    lambda v: f"{v:,.2f}" if pd.notna(v) else "—"
                )
                st.dataframe(latest_by_country, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
# Tab 6: Alerts
# ═══════════════════════════════════════════════════════════════
with tab6:
    st.header("가격 이상 변동 알림")

    col_t, col_d = st.columns(2)
    alert_threshold = col_t.slider("변동 임계값 (%)", 5, 50, 10)
    alert_days = col_d.selectbox("탐지 기간", [7, 14, 30], index=1,
                                  format_func=lambda x: f"최근 {x}일")

    alerts = load_price_alerts(alert_threshold, alert_days)

    if alerts.empty:
        st.success(f"최근 {alert_days}일 내 ±{alert_threshold}% 이상 변동 없음.")
    else:
        up_alerts = alerts[alerts["change_pct"] > 0]
        dn_alerts = alerts[alerts["change_pct"] < 0]
        ca, cb, cc = st.columns(3)
        ca.metric("전체 이상 변동", len(alerts))
        cb.metric("🔴 가격 인상", len(up_alerts))
        cc.metric("🟢 가격 인하", len(dn_alerts))

        st.divider()

        alerts_sorted = alerts.sort_values("change_pct", key=abs, ascending=False).head(20)
        alerts_sorted = alerts_sorted.copy()
        alerts_sorted["label"] = (
            alerts_sorted["brand"] + " " + alerts_sorted["model"].fillna("")
            + " " + alerts_sorted["capacity"].fillna("")
            + " (" + alerts_sorted["country"] + ")"
        )
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
            **_chart_layout(
                title=f"가격 변동 Top {len(alerts_sorted)} (최근 {alert_days}일)",
                xaxis_title="변동률 (%)",
                height=max(320, len(alerts_sorted) * 30),
                showlegend=False,
                margin=dict(l=220, r=80, t=48, b=20),
            )
        )
        st.plotly_chart(fig_alert, use_container_width=True)

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
st.sidebar.caption("Powered by Crawling Pipeline\n© 2026 SanDisk Marketing Intelligence")
if st.sidebar.button("🔄 캐시 초기화"):
    st.cache_data.clear()
    st.rerun()
