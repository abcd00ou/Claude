"""
Marketing Simulation — 마케팅 시뮬레이션 + NAND 인텔
데이터: marketing / sim_state.json + market_intel.json + internal_sales.json
"""
import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).parent.parent.parent

st.set_page_config(page_title="Marketing Sim", page_icon="📈", layout="wide")
st.title("📈 마케팅 시뮬레이션")
st.caption("SanDisk B2C 마케팅 시뮬레이션 + NAND 시장 인텔리전스")

CAT_LABELS = {"external_ssd": "External SSD", "internal_ssd": "Internal SSD", "microsd": "microSD"}
CAT_COLORS = {"external_ssd": "#E2231A", "internal_ssd": "#1428A0", "microsd": "#22c55e"}

@st.cache_data(ttl=60)
def load_data():
    out = {}
    for name, fname in [("sim", "sim_state.json"), ("intel", "market_intel.json"),
                        ("sales", "internal_sales.json")]:
        f = ROOT / "marketing" / "data" / fname
        if f.exists():
            with open(f) as fp:
                out[name] = json.load(fp)
    return out

data  = load_data()
sim   = data.get("sim", {})
intel = data.get("intel", {})
sales = data.get("sales", {})
hist  = sim.get("history", [])
last  = hist[-1] if hist else {}

# ── KPI ─────────────────────────────────────────────────────
nand_signal = intel.get("nand_signal", "unknown")
nand_icon   = {"tight": "🔴", "loose": "🟢", "neutral": "🟡"}.get(nand_signal, "⚪")

# market_share_pct: {cat: pct}
ms       = last.get("market_share_pct", {})
ms_avg   = round(sum(ms.values()) / len(ms), 1) if ms else 0
sim_month_num = sim.get("sim_month", 0)
sim_year      = sim.get("sim_year", "—")
sim_month_label = f"{sim_year}년 {sim_month_num % 12 or 12}월"

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("시뮬레이션 시점", sim_month_label)
c2.metric("월 매출", f"${last.get('total_rev_m', 0):.1f}M")
c3.metric("블렌디드 GM", f"{last.get('blended_gm_pct', 0):.1f}%")
c4.metric("평균 시장점유율", f"{ms_avg:.1f}%")
c5.metric(f"NAND {nand_icon}", nand_signal.upper(),
          f"{intel.get('price_change_pct', 0):+.1f}% 가격변동")

st.divider()

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["📊 매출 추이", "🌍 NAND 인텔", "💼 채널/카테고리", "🏭 SKU 분석", "📋 분기 실적"]
)

# ────────────────────────────────────────────────────────────
# Tab 1: 매출 추이
# ────────────────────────────────────────────────────────────
with tab1:
    if not hist:
        st.info("시뮬레이션 히스토리 없음")
    else:
        df = pd.DataFrame([{
            "sim_date":        r["sim_date"],
            "total_rev_m":     r.get("total_rev_m", 0),
            "blended_gm_pct":  r.get("blended_gm_pct", 0),
            "gross_margin_pct":r.get("gross_margin_pct", 0),
            # nand_cost_per_gb: dict → 평균
            "nand_avg":        round(
                sum(r["nand_cost_per_gb"].values()) / len(r["nand_cost_per_gb"]), 4
            ) if isinstance(r.get("nand_cost_per_gb"), dict) and r["nand_cost_per_gb"] else 0,
            # market_share_pct: dict → 평균
            "ms_avg": round(
                sum(r["market_share_pct"].values()) / len(r["market_share_pct"]), 1
            ) if isinstance(r.get("market_share_pct"), dict) and r["market_share_pct"] else 0,
            # sku_revenue: 카테고리별 합산
            "ext_rev": sum(
                v["rev_m"] for v in r.get("sku_revenue", {}).values()
                if isinstance(v, dict) and v.get("cat") == "external_ssd"
            ),
            "int_rev": sum(
                v["rev_m"] for v in r.get("sku_revenue", {}).values()
                if isinstance(v, dict) and v.get("cat") == "internal_ssd"
            ),
            "event": r.get("event", ""),
            "promo": r.get("promo", ""),
        } for r in hist])

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader("월 매출 추이 ($M)")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df["sim_date"], y=df["ext_rev"],
                name="External SSD", stackgroup="one",
                fillcolor="rgba(226,35,26,0.7)", line=dict(color="#E2231A"),
            ))
            fig.add_trace(go.Scatter(
                x=df["sim_date"], y=df["int_rev"],
                name="Internal SSD", stackgroup="one",
                fillcolor="rgba(20,40,160,0.7)", line=dict(color="#1428A0"),
            ))
            fig.update_layout(height=300, yaxis_title="$M",
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"), margin=dict(l=10,r=10,t=10,b=10),
                legend=dict(orientation="h", y=1.05))
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            st.subheader("GM% & 시장점유율 추이")
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(
                x=df["sim_date"], y=df["blended_gm_pct"],
                name="Blended GM%", line=dict(color="#4B9CD3", width=2),
            ))
            fig2.add_trace(go.Scatter(
                x=df["sim_date"], y=df["ms_avg"],
                name="점유율(%)", line=dict(color="#fbbf24", width=2, dash="dot"),
                yaxis="y2",
            ))
            fig2.update_layout(
                height=300,
                yaxis=dict(title="GM (%)"),
                yaxis2=dict(title="점유율 (%)", overlaying="y", side="right"),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"), margin=dict(l=10,r=10,t=10,b=10),
                legend=dict(orientation="h", y=1.05),
            )
            st.plotly_chart(fig2, use_container_width=True)

        # NAND 비용 추이
        st.subheader("NAND 비용 추이 ($/GB 평균)")
        fig3 = go.Figure()
        fig3.add_trace(go.Scatter(
            x=df["sim_date"], y=df["nand_avg"],
            name="NAND avg $/GB", line=dict(color="#a855f7", width=2),
            fill="tozeroy", fillcolor="rgba(168,85,247,0.1)",
        ))
        fig3.update_layout(
            height=220, yaxis_title="$/GB",
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"), margin=dict(l=10,r=10,t=10,b=10),
        )
        st.plotly_chart(fig3, use_container_width=True)

        # 이벤트 로그
        events = [(r["sim_date"], r["event"], r["promo"]) for _, r in df.iterrows()
                  if r["event"] or r["promo"]]
        if events:
            st.subheader("이벤트 / 프로모 로그")
            for d, ev, pr in events[-10:]:
                if ev: st.markdown(f"- `{d}` 📌 {ev}")
                if pr: st.markdown(f"- `{d}` 🎯 {pr}")

# ────────────────────────────────────────────────────────────
# Tab 2: NAND 인텔
# ────────────────────────────────────────────────────────────
with tab2:
    if not intel:
        st.info("NAND 인텔 데이터 없음")
    else:
        col_a, col_b = st.columns([1, 2])
        with col_a:
            nand_c = {"tight":"#ef4444","loose":"#22c55e","neutral":"#fbbf24"}.get(nand_signal,"#94a3b8")
            st.markdown(f"""
<div style="background:{nand_c}22;border:1px solid {nand_c};border-radius:8px;padding:1rem;margin-bottom:0.8rem">
  <div style="font-size:2rem;font-weight:700;color:{nand_c}">{nand_icon} {nand_signal.upper()}</div>
  <div style="color:#94a3b8;font-size:0.8rem">NAND 공급 신호</div>
</div>""", unsafe_allow_html=True)
            st.metric("가격 트렌드", intel.get("price_trend","—").upper())
            st.metric("가격 변화율", f"{intel.get('price_change_pct',0):+.1f}%")
            st.metric("공급 점수", f"{intel.get('supply_score',0):.0f}/100")
            st.metric("가격 점수", f"{intel.get('price_score',0):.0f}/100")
            fetched = intel.get("fetched_at","")[:16].replace("T"," ")
            st.caption(f"업데이트: {fetched}")

            # NAND 세대별 현재 비용
            nand_cost = last.get("nand_cost_per_gb", {})
            if isinstance(nand_cost, dict) and nand_cost:
                st.subheader("NAND 세대별 $/GB")
                for gen, cost in sorted(nand_cost.items()):
                    st.metric(gen, f"${cost:.4f}")

        with col_b:
            st.subheader("최신 헤드라인")
            for h in intel.get("headlines", [])[:8]:
                title = h.get("title","")
                date  = h.get("date","")[:10]
                url   = h.get("url","#")
                st.markdown(f"- [{title}]({url}) `{date}`")

            st.subheader("시장 인사이트")
            for ins in intel.get("key_insights", []):
                st.markdown(f"- {ins}")
            mc = intel.get("market_context","")
            if mc:
                st.info(mc)

        # 시뮬레이션 조정값
        adj = intel.get("sim_adjustments", {})
        if adj:
            st.subheader("시뮬레이션 자동 조정값")
            adj_df = pd.DataFrame([{"항목":k,"조정값":v} for k,v in adj.items()])
            st.dataframe(adj_df, use_container_width=True, hide_index=True)

# ────────────────────────────────────────────────────────────
# Tab 3: 채널/카테고리
# ────────────────────────────────────────────────────────────
with tab3:
    col_a, col_b = st.columns(2)

    # 현재 시뮬 채널 믹스 (카테고리별)
    ch_now = last.get("channel_mix_pct", {})
    with col_a:
        st.subheader(f"현재 채널 믹스 — {sim_month_label}")
        if ch_now:
            for cat, channels in ch_now.items():
                cat_label = CAT_LABELS.get(cat, cat)
                ch_df = pd.DataFrame([{"채널": k, "비중(%)": v} for k,v in channels.items()])
                fig = go.Figure(go.Pie(
                    labels=ch_df["채널"], values=ch_df["비중(%)"],
                    hole=0.45, textinfo="label+percent",
                    title=cat_label,
                ))
                fig.update_layout(
                    height=240, margin=dict(l=10,r=10,t=40,b=10),
                    plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white"), showlegend=False,
                )
                st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("카테고리별 시장점유율")
        if ms:
            ms_df = pd.DataFrame([
                {"카테고리": CAT_LABELS.get(k,k), "점유율(%)": v}
                for k,v in ms.items()
            ])
            fig = px.bar(ms_df, x="카테고리", y="점유율(%)",
                         color="카테고리",
                         color_discrete_map={CAT_LABELS.get(k,k): v for k,v in CAT_COLORS.items()},
                         text="점유율(%)", height=300)
            fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig.update_layout(showlegend=False,
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"), margin=dict(l=10,r=10,t=10,b=10))
            st.plotly_chart(fig, use_container_width=True)

        # 점유율 트렌드
        if len(hist) > 1:
            st.subheader("시장점유율 추이")
            ms_hist = []
            for r in hist:
                row = {"날짜": r["sim_date"]}
                row.update({CAT_LABELS.get(k,k): v
                            for k,v in r.get("market_share_pct",{}).items()})
                ms_hist.append(row)
            ms_df2 = pd.DataFrame(ms_hist)
            cats_cols = [c for c in ms_df2.columns if c != "날짜"]
            fig2 = go.Figure()
            for col in cats_cols:
                fig2.add_trace(go.Scatter(
                    x=ms_df2["날짜"], y=ms_df2[col], name=col,
                    line=dict(width=2),
                ))
            fig2.update_layout(height=250, yaxis_title="점유율 (%)",
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"), margin=dict(l=10,r=10,t=10,b=10),
                legend=dict(orientation="h", y=1.05))
            st.plotly_chart(fig2, use_container_width=True)

# ────────────────────────────────────────────────────────────
# Tab 4: SKU 분석
# ────────────────────────────────────────────────────────────
with tab4:
    sku_rev = last.get("sku_revenue", {})
    if not sku_rev:
        st.info("SKU 데이터 없음")
    else:
        rows = []
        for sku_id, v in sku_rev.items():
            if not isinstance(v, dict): continue
            rows.append({
                "SKU": sku_id,
                "카테고리": CAT_LABELS.get(v.get("cat",""), v.get("cat","")),
                "라인": v.get("line",""),
                "용량(GB)": v.get("cap_gb", 0),
                "ASP($)": v.get("asp", 0),
                "매출($M)": round(v.get("rev_m", 0), 2),
                "판매량(K)": round(v.get("units_k", 0), 1),
                "GM(%)": v.get("gm_pct", 0),
            })
        sku_df = pd.DataFrame(rows).sort_values("매출($M)", ascending=False)

        col_a, col_b = st.columns(2)
        with col_a:
            st.subheader(f"SKU별 월 매출 TOP20 — {sim_month_label}")
            fig = px.bar(sku_df.head(20), x="매출($M)", y="SKU",
                         orientation="h", color="카테고리",
                         color_discrete_map={v: CAT_COLORS.get(k,k) for k,v in CAT_LABELS.items()},
                         text="매출($M)", height=520)
            fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
            fig.update_layout(
                yaxis=dict(autorange="reversed"),
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"), margin=dict(l=10,r=80,t=10,b=10),
                legend=dict(orientation="h", y=1.02),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_b:
            st.subheader("SKU 수익성 (ASP vs GM%)")
            fig2 = px.scatter(sku_df, x="ASP($)", y="GM(%)",
                              size="매출($M)", color="카테고리",
                              color_discrete_map={v: CAT_COLORS.get(k,k) for k,v in CAT_LABELS.items()},
                              hover_name="SKU", height=320,
                              size_max=40)
            fig2.update_layout(
                plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="white"), margin=dict(l=10,r=10,t=10,b=10),
                legend=dict(orientation="h", y=1.02),
            )
            st.plotly_chart(fig2, use_container_width=True)

            # 카테고리 합산
            cat_sum = sku_df.groupby("카테고리").agg(
                매출합계=("매출($M)","sum"),
                평균GM=("GM(%)","mean"),
                SKU수=("SKU","count")
            ).round(1).reset_index()
            st.dataframe(cat_sum, use_container_width=True, hide_index=True)

        st.subheader("전체 SKU 테이블")
        st.dataframe(sku_df, use_container_width=True, hide_index=True)

# ────────────────────────────────────────────────────────────
# Tab 5: 분기 실적 (internal_sales)
# ────────────────────────────────────────────────────────────
with tab5:
    q_rev = sales.get("quarterly_revenue_usd_m", {})
    if not q_rev:
        st.info("분기 실적 데이터 없음")
    else:
        qrows = []
        for q, cats in q_rev.items():
            row = {"분기": q}
            row.update({CAT_LABELS.get(k,k): v for k,v in cats.items() if k != "total"})
            row["합계($M)"] = cats.get("total", 0)
            qrows.append(row)
        q_df = pd.DataFrame(qrows)

        st.subheader("분기별 카테고리 매출 ($M)")
        cat_cols = [c for c in q_df.columns if c not in ("분기","합계($M)")]
        fig = go.Figure()
        for col in cat_cols:
            fig.add_trace(go.Bar(
                x=q_df["분기"], y=q_df[col], name=col,
                marker_color=CAT_COLORS.get(
                    next((k for k,v in CAT_LABELS.items() if v==col), ""), "#888")
            ))
        fig.add_trace(go.Scatter(
            x=q_df["분기"], y=q_df["합계($M)"],
            name="합계", mode="lines+markers",
            line=dict(color="white", width=2, dash="dot"),
        ))
        fig.update_layout(barmode="stack", height=380,
            yaxis_title="$M", xaxis_tickangle=-45,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"), margin=dict(l=10,r=10,t=10,b=80),
            legend=dict(orientation="h", y=1.05))
        st.plotly_chart(fig, use_container_width=True)

        # 연도별 합산
        q_df["연도"] = q_df["분기"].str[:4]
        yr = q_df.groupby("연도")["합계($M)"].sum().reset_index()
        yr["YoY(%)"] = yr["합계($M)"].pct_change() * 100
        yr["합계($M)"] = yr["합계($M)"].round(0)
        yr["YoY(%)"] = yr["YoY(%)"].round(1)
        st.subheader("연도별 합산")
        st.dataframe(yr, use_container_width=True, hide_index=True)

        # 지역 믹스
        geo = sales.get("geo_mix_pct", {})
        if geo:
            latest_year = sorted(geo.keys())[-1]
            geo_data = geo[latest_year]
            st.subheader(f"지역별 매출 비중 ({latest_year})")
            geo_cols = st.columns(len(geo_data))
            for i, (cat, regions) in enumerate(geo_data.items()):
                with geo_cols[i]:
                    fig = go.Figure(go.Pie(
                        labels=list(regions.keys()),
                        values=list(regions.values()),
                        hole=0.45, textinfo="label+percent",
                        title=CAT_LABELS.get(cat, cat),
                    ))
                    fig.update_layout(
                        height=220, margin=dict(l=5,r=5,t=35,b=5),
                        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                        font=dict(color="white", size=10), showlegend=False,
                    )
                    st.plotly_chart(fig, use_container_width=True)
