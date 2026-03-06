"""
Price Intelligence Dashboard (Streamlit)

탭 구성:
  1. Overview      — 최신 가격 테이블 (브랜드/카테고리/국가 필터)
  2. Price History — SKU별 시계열 차트
  3. Competitor Comparison — Samsung vs SanDisk vs Lexar 나란히 비교
  4. Price Alerts  — ±15% 이상 변동 항목
  5. HITL Queue    — pending 항목 + Approve/Fix/Ignore
  6. Run Status    — 최근 실행 이력
"""
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import psycopg2
import streamlit as st

# dashboard/ 폴더에서 실행될 때 상위 Crawling/ 경로를 sys.path에 추가
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
}

CATEGORY_LABELS = {
    "portable_ssd": "Portable SSD",
    "internal_ssd": "Internal SSD",
    "microsd":      "microSD",
}


# ── DB 연결 ──────────────────────────────────────────────────
@st.cache_resource
def get_conn():
    return psycopg2.connect(DB_URL)


def db_conn():
    """stale 커넥션 자동 재연결."""
    conn = get_conn()
    try:
        conn.cursor().execute("SELECT 1")
    except Exception:
        get_conn.clear()
        conn = get_conn()
    return conn


@st.cache_data(ttl=300)
def load_latest_prices(countries: list[str], categories: list[str]) -> pd.DataFrame:
    conn = db_conn()
    cur  = conn.cursor()
    cur.execute("""
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
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    cur.close()
    return pd.DataFrame(rows, columns=cols)


@st.cache_data(ttl=300)
def load_price_history(sku_id: str, days: int = 90) -> pd.DataFrame:
    conn = db_conn()
    cur  = conn.cursor()
    cur.execute("""
        SELECT p.country, p.source, p.price, p.currency, p.observed_at
        FROM price_observations p
        WHERE p.sku_id = %s
          AND p.is_accepted = TRUE
          AND p.observed_at >= NOW() - INTERVAL '1 day' * %s
        ORDER BY p.observed_at
    """, (sku_id, days))
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    cur.close()
    return pd.DataFrame(rows, columns=cols)


@st.cache_data(ttl=300)
def load_price_alerts(threshold_pct: float = 15.0) -> pd.DataFrame:
    conn = db_conn()
    cur  = conn.cursor()
    cur.execute("""
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
              AND p.observed_at >= NOW() - INTERVAL '7 days'
        )
        SELECT *, ROUND(100.0*(price-prev_price)/prev_price, 1) AS change_pct
        FROM ranked
        WHERE prev_price IS NOT NULL
          AND prev_price > 0
          AND ABS((price-prev_price)/prev_price*100) >= %s
        ORDER BY ABS((price-prev_price)/prev_price) DESC
    """, (threshold_pct,))
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    cur.close()
    return pd.DataFrame(rows, columns=cols)


@st.cache_data(ttl=60)
def load_hitl_queue(status: str = "pending") -> pd.DataFrame:
    conn = db_conn()
    cur  = conn.cursor()
    cur.execute("""
        SELECT id, run_id, sku_id, country, source, priority, reason, evidence,
               status, human_note, created_at
        FROM hitl_queue
        WHERE status = %s
        ORDER BY
            CASE priority WHEN 'P0' THEN 0 ELSE 1 END,
            created_at DESC
        LIMIT 100
    """, (status,))
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    cur.close()
    return pd.DataFrame(rows, columns=cols)


@st.cache_data(ttl=120)
def load_run_log(limit: int = 20) -> pd.DataFrame:
    conn = db_conn()
    cur  = conn.cursor()
    cur.execute("""
        SELECT run_id, started_at, completed_at, total_targets,
               success_count, quarantine_count, hitl_count, status
        FROM run_log
        ORDER BY started_at DESC
        LIMIT %s
    """, (limit,))
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    cur.close()
    return pd.DataFrame(rows, columns=cols)


@st.cache_data(ttl=300)
def load_all_skus() -> pd.DataFrame:
    conn = db_conn()
    cur  = conn.cursor()
    cur.execute("SELECT sku_id, brand, category, model, capacity FROM skus ORDER BY brand, category, model, capacity")
    cols = [d[0] for d in cur.description]
    rows = cur.fetchall()
    cur.close()
    return pd.DataFrame(rows, columns=cols)


def update_hitl_status(item_id: int, status: str, note: str):
    conn = db_conn()
    cur  = conn.cursor()
    cur.execute("""
        UPDATE hitl_queue
        SET status=%s, human_note=%s, decided_at=NOW()
        WHERE id=%s
    """, (status, note, item_id))
    conn.commit()
    cur.close()
    st.cache_data.clear()


# ── 사이드바 필터 ─────────────────────────────────────────────
st.sidebar.title("📊 Price Intelligence")
st.sidebar.caption("Samsung vs Competitors")

selected_countries = st.sidebar.multiselect(
    "국가", ["US", "KR", "JP", "DE"], default=["US", "JP", "DE"]
)
selected_categories = st.sidebar.multiselect(
    "카테고리",
    list(CATEGORY_LABELS.keys()),
    format_func=lambda x: CATEGORY_LABELS[x],
    default=list(CATEGORY_LABELS.keys()),
)
selected_brands = st.sidebar.multiselect(
    "브랜드", ["samsung", "sandisk", "lexar"], default=["samsung", "sandisk", "lexar"]
)

if not selected_countries:
    selected_countries = ["US"]
if not selected_categories:
    selected_categories = list(CATEGORY_LABELS.keys())

# ── 탭 ───────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Overview",
    "📈 Price History",
    "⚔️ Competitor Compare",
    "🚨 Price Alerts",
    "🙋 HITL Queue",
    "⚙️ Run Status",
])


# ── Tab 1: Overview ──────────────────────────────────────────
with tab1:
    st.header("최신 가격 현황")
    df = load_latest_prices(selected_countries, selected_categories)

    if df.empty:
        st.info("데이터가 없습니다. 파이프라인을 먼저 실행하세요: `python run_pipeline.py`")
    else:
        # 브랜드 필터
        df = df[df["brand"].isin(selected_brands)]

        # 요약 메트릭
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("전체 SKU", df["sku_id"].nunique())
        col2.metric("Samsung SKU",  len(df[df["brand"] == "samsung"]["sku_id"].unique()))
        col3.metric("SanDisk SKU",  len(df[df["brand"] == "sandisk"]["sku_id"].unique()))
        col4.metric("Lexar SKU",    len(df[df["brand"] == "lexar"]["sku_id"].unique()))

        st.divider()

        for cat in selected_categories:
            cat_df = df[df["category"] == cat]
            if cat_df.empty:
                continue
            st.subheader(CATEGORY_LABELS[cat])

            display = cat_df[[
                "brand", "model", "capacity", "country", "source",
                "price", "currency", "availability", "observed_at"
            ]].copy()
            display["observed_at"] = pd.to_datetime(display["observed_at"], errors="coerce").dt.tz_convert("Asia/Seoul").dt.strftime("%m/%d %H:%M")
            display["price_display"] = display.apply(
                lambda r: f"{r['currency']} {r['price']:,.2f}" if r["price"] else "—", axis=1
            )
            display = display.drop(columns=["price", "currency"]).rename(
                columns={"price_display": "가격", "observed_at": "수집일시"}
            )
            display = display.sort_values(["brand", "model", "capacity", "country"])

            def highlight_brand(row):
                color = BRAND_COLORS.get(row["brand"], "#fff")
                return [f"background-color: {color}15"] * len(row)

            st.dataframe(
                display.style.apply(highlight_brand, axis=1),
                width="stretch",
                hide_index=True,
            )


# ── Tab 2: Price History ─────────────────────────────────────
with tab2:
    st.header("가격 추이 분석")

    skus_df = load_all_skus()
    if skus_df.empty:
        st.info("SKU 데이터 없음.")
    else:
        col1, col2 = st.columns([2, 1])
        with col1:
            sku_options = {
                row["sku_id"]: f"[{row['brand'].upper()}] {row['model']} {row['capacity']}"
                for _, row in skus_df.iterrows()
                if row["brand"] in selected_brands
            }
            selected_sku = st.selectbox(
                "SKU 선택",
                options=list(sku_options.keys()),
                format_func=lambda x: sku_options.get(x, x),
            )
        with col2:
            history_days = st.selectbox("기간", [30, 60, 90, 180], index=1)

        if selected_sku:
            hist = load_price_history(selected_sku, history_days)
            if hist.empty:
                st.info("해당 SKU의 가격 기록이 없습니다.")
            else:
                hist["label"] = hist["country"] + " / " + hist["source"]
                fig = px.line(
                    hist,
                    x="observed_at", y="price",
                    color="label",
                    title=f"{sku_options.get(selected_sku, selected_sku)} 가격 추이",
                    labels={"observed_at": "날짜", "price": "가격", "label": "출처"},
                )
                fig.update_layout(hovermode="x unified")
                st.plotly_chart(fig, width="stretch")


# ── Tab 3: Competitor Comparison ─────────────────────────────
with tab3:
    st.header("경쟁사 가격 비교")

    df_all = load_latest_prices(selected_countries, selected_categories)
    if df_all.empty:
        st.info("데이터 없음.")
    else:
        for cat in selected_categories:
            cat_df = df_all[
                (df_all["category"] == cat) &
                (df_all["brand"].isin(selected_brands)) &
                (df_all["source"] == "amazon")
            ].copy()
            if cat_df.empty:
                continue

            st.subheader(f"{CATEGORY_LABELS[cat]} — Amazon 가격 비교")

            # pivot: model+capacity vs brand
            cat_df["product"] = cat_df["model"] + " " + cat_df["capacity"].fillna("")
            pivot = cat_df.pivot_table(
                index="product",
                columns="brand",
                values="price",
                aggfunc="min",
            ).reset_index()

            # 막대 차트
            brands_present = [b for b in ["samsung", "sandisk", "lexar"] if b in pivot.columns]
            if brands_present:
                fig = go.Figure()
                for brand in brands_present:
                    if brand in pivot.columns:
                        fig.add_trace(go.Bar(
                            name=brand.capitalize(),
                            x=pivot["product"],
                            y=pivot[brand],
                            marker_color=BRAND_COLORS.get(brand),
                        ))
                fig.update_layout(
                    barmode="group",
                    title=f"{CATEGORY_LABELS[cat]} Amazon 가격 비교 (USD)",
                    xaxis_tickangle=-30,
                    height=450,
                )
                st.plotly_chart(fig, width="stretch")

            st.dataframe(pivot, width="stretch", hide_index=True)
            st.divider()


# ── Tab 4: Price Alerts ───────────────────────────────────────
with tab4:
    st.header("가격 변동 알림")

    alert_threshold = st.slider("변동 임계값 (%)", 5, 50, 15)
    alerts = load_price_alerts(alert_threshold)

    if alerts.empty:
        st.success(f"최근 7일 내 ±{alert_threshold}% 이상 변동 없음.")
    else:
        for _, row in alerts.iterrows():
            delta = row["change_pct"]
            color = "🟢" if delta < 0 else "🔴"
            with st.expander(
                f"{color} {row['model']} {row['capacity']} ({row['country']}/{row['source']}) "
                f"{'+' if delta > 0 else ''}{delta}%"
            ):
                col1, col2, col3 = st.columns(3)
                col1.metric("이전 가격",  f"{row['currency']} {row['prev_price']:,.2f}" if row["prev_price"] else "—")
                col2.metric("현재 가격",  f"{row['currency']} {row['price']:,.2f}" if row["price"] else "—",
                            delta=f"{delta:+.1f}%")
                col3.metric("수집 시각", str(row["observed_at"])[:16])


# ── Tab 5: HITL Queue ────────────────────────────────────────
with tab5:
    st.header("Human-in-the-Loop 검토 큐")

    status_filter = st.selectbox("상태 필터", ["pending", "approved", "fixed", "ignored"], index=0)
    hitl_df = load_hitl_queue(status_filter)

    if hitl_df.empty:
        st.success(f"'{status_filter}' 상태 항목 없음.")
    else:
        st.caption(f"총 {len(hitl_df)}건 (P0: {len(hitl_df[hitl_df['priority']=='P0'])}건)")

        for _, row in hitl_df.iterrows():
            priority_badge = "🔴 P0" if row["priority"] == "P0" else "🟡 P1"
            with st.expander(
                f"{priority_badge} | {row['sku_id']} | {row['country']}/{row['source']} | {row['reason'][:80]}"
            ):
                evidence = row["evidence"]
                if isinstance(evidence, str):
                    try:
                        evidence = json.loads(evidence)
                    except (json.JSONDecodeError, TypeError):
                        evidence = {}
                st.json(evidence if isinstance(evidence, dict) else {})

                if status_filter == "pending":
                    note = st.text_input(f"메모 (id={row['id']})", key=f"note_{row['id']}")
                    c1, c2, c3 = st.columns(3)
                    if c1.button("✅ Approve", key=f"approve_{row['id']}"):
                        update_hitl_status(row["id"], "approved", note)
                        st.rerun()
                    if c2.button("🔧 Fix", key=f"fix_{row['id']}"):
                        update_hitl_status(row["id"], "fixed", note)
                        st.rerun()
                    if c3.button("🚫 Ignore", key=f"ignore_{row['id']}"):
                        update_hitl_status(row["id"], "ignored", note)
                        st.rerun()


# ── Tab 6: Run Status ────────────────────────────────────────
with tab6:
    st.header("파이프라인 실행 현황")

    run_df = load_run_log()
    if run_df.empty:
        st.info("실행 기록 없음. `python run_pipeline.py` 실행 후 확인하세요.")
    else:
        latest = run_df.iloc[0]

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("마지막 실행",    str(latest["started_at"])[:16] if latest["started_at"] else "—")
        col2.metric("성공",           int(latest["success_count"] or 0))
        col3.metric("Quarantine",     int(latest["quarantine_count"] or 0))
        col4.metric("HITL",           int(latest["hitl_count"] or 0))

        st.divider()

        # 성공률 추이
        run_df["success_rate"] = (
            run_df["success_count"] / run_df["total_targets"].replace(0, 1) * 100
        ).round(1)
        run_df["started_at_str"] = pd.to_datetime(run_df["started_at"]).dt.strftime("%m/%d %H:%M")

        fig = px.bar(
            run_df.head(15).iloc[::-1],
            x="started_at_str",
            y="success_rate",
            color="status",
            color_discrete_map={"completed": "#1428A0", "partial": "#FFA500", "failed": "#E2231A"},
            title="최근 실행 성공률 (%)",
            labels={"started_at_str": "실행 시각", "success_rate": "성공률 (%)"},
        )
        st.plotly_chart(fig, width="stretch")

        st.dataframe(
            run_df[["run_id", "started_at", "total_targets", "success_count",
                    "quarantine_count", "hitl_count", "status"]],
            width="stretch",
            hide_index=True,
        )
