"""
Local AI × SSD 수요 분석
데이터: ssd_ai_potential / analysis_results.json + crawled_posts.json
"""
import json
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

ROOT = Path(__file__).parent.parent.parent

st.set_page_config(page_title="AI × SSD 수요", page_icon="🤖", layout="wide")
st.title("🤖 Local AI × SSD 수요 분석")
st.caption("Local LLM 커뮤니티의 SSD 교체·확장·구매 수요 신호 분석 | Reddit 15개 서브레딧 + HackerNews")

SIGNAL_LABELS = {
    "buy_intent":     "구매 의향",
    "upgrade_intent": "교체/확장 의향",
    "technical_need": "기술적 필요",
    "co_mention":     "동시 언급",
    "no_signal":      "무관",
}
SIGNAL_COLORS = {
    "buy_intent":     "#ef4444",
    "upgrade_intent": "#f97316",
    "technical_need": "#3b82f6",
    "co_mention":     "#a855f7",
    "no_signal":      "#374151",
}
FACTOR_LABELS = {
    "model_weight_size": "모델 파일 용량",
    "portability":       "포터블 이동 실행",
    "io_bottleneck":     "I/O 병목",
    "vram_offload":      "VRAM 오프로드",
    "capacity":          "단순 용량 부족",
    "swap_speed":        "스왑 속도",
    "speed_matters":     "NVMe 속도 중요",
}

@st.cache_data(ttl=120)
def load_history():
    f = ROOT / "ssd_ai_potential" / "data" / "analysis_results.json"
    if not f.exists():
        return []
    with open(f) as fp:
        return json.load(fp)

@st.cache_data(ttl=120)
def load_posts():
    f = ROOT / "ssd_ai_potential" / "data" / "crawled_posts.json"
    if not f.exists():
        return []
    with open(f) as fp:
        return json.load(fp)

history = load_history()
if not history:
    st.error("분석 데이터 없음 — run_research.py를 먼저 실행하세요")
    st.stop()

latest = history[-1]
signals = latest["demand_signals"]
factors = latest.get("technical_factors", {})

# ── KPI ─────────────────────────────────────────────────────
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("분석 포스트", f"{latest['total_posts']:,}개")
c2.metric("수요 신호", f"{latest['demand_total']}건",
          f"{latest['demand_rate_pct']}%")
c3.metric("구매 의향", f"{signals.get('buy_intent',0)}건")
c4.metric("교체/확장", f"{signals.get('upgrade_intent',0)}건")
c5.metric("포터블 SSD 언급", f"{latest.get('portable_ssd_mentions',0)}건",
          f"{latest.get('portable_ssd_pct',0)}%")

st.divider()

# ── 3대 질문 ─────────────────────────────────────────────────
st.markdown("### 3대 핵심 질문 답변")
q1, q2, q3 = st.columns(3)

total  = latest["total_posts"]
demand = latest["demand_total"]
rate   = latest["demand_rate_pct"]
tech   = signals.get("technical_need", 0)
tech_r = round(tech / total * 100, 1) if total else 0

with q1:
    level = "🔴 강함" if rate > 10 else "🟡 중간" if rate > 3 else "🟢 약함"
    st.info(f"**Q1. SSD 수요 존재하는가?**\n\n✅ 존재함\n수요 신호 {demand}건 ({rate}%)\n강도: {level}")

with q2:
    conn = "✅ 직접 연관 확인" if tech > 20 else "⚠️ 부분 연관" if tech > 5 else "❌ 연관 약함"
    st.info(f"**Q2. LLM↔SSD 직접 연관?**\n\n{conn}\n기술적 필요 명시: {tech}건 ({tech_r}%)")

with q3:
    top_f = max(factors, key=factors.get) if factors else "—"
    top_label = FACTOR_LABELS.get(top_f, top_f)
    st.info(f"**Q3. 주요 기술 근거?**\n\n1위: **{top_label}** ({factors.get(top_f,0)}건)\n포터블 이동 실행 수요 주목")

st.divider()

# ── 탭 ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📊 수요 분포", "🔬 기술 근거", "📈 트렌드", "📋 상위 포스트"])

# Tab 1: 수요 분포
with tab1:
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader("수요 신호 분류")
        labels = [SIGNAL_LABELS.get(k, k) for k in signals]
        values = list(signals.values())
        colors = [SIGNAL_COLORS.get(k, "#888") for k in signals]
        fig = go.Figure(go.Pie(
            labels=labels, values=values,
            hole=0.55, marker_colors=colors,
            textinfo="label+percent",
        ))
        fig.update_layout(
            height=350, margin=dict(l=10, r=10, t=10, b=10),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"), showlegend=False,
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.subheader("커뮤니티별 수요율")
        by_source = latest.get("by_source", {})
        src_data = []
        for src, cnt in by_source.items():
            rate_s = round(cnt["demand"] / cnt["total"] * 100, 1) if cnt["total"] else 0
            src_data.append({
                "커뮤니티": src.replace("reddit/r/", "r/"),
                "수요율(%)": rate_s,
                "수요건": cnt["demand"],
                "전체": cnt["total"],
            })
        src_df = pd.DataFrame(src_data).sort_values("수요율(%)", ascending=False).head(12)
        fig2 = px.bar(src_df, x="수요율(%)", y="커뮤니티", orientation="h",
                      color="수요율(%)", color_continuous_scale=["#1e3a8a", "#ef4444"],
                      text="수요율(%)", height=380)
        fig2.update_layout(
            coloraxis_showscale=False,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"), margin=dict(l=10, r=10, t=10, b=10),
            yaxis=dict(autorange="reversed"),
        )
        st.plotly_chart(fig2, use_container_width=True)

# Tab 2: 기술 근거
with tab2:
    st.subheader("기술 근거 TOP 요인 — 사람들이 SSD가 필요하다고 인식하는 이유")
    if factors:
        items = sorted(factors.items(), key=lambda x: -x[1])
        f_df  = pd.DataFrame([(FACTOR_LABELS.get(k, k), v) for k, v in items],
                             columns=["요인", "언급 건수"])
        fig = px.bar(f_df, x="언급 건수", y="요인", orientation="h",
                     color="언급 건수", color_continuous_scale=["#1e3a8a", "#3b82f6"],
                     text="언급 건수", height=380)
        fig.update_traces(textposition="outside")
        fig.update_layout(
            coloraxis_showscale=False,
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"), margin=dict(l=10, r=10, t=10, b=10),
            yaxis=dict(autorange="reversed"),
        )
        st.plotly_chart(fig, use_container_width=True)

        # 요인별 설명
        explanations = {
            "model_weight_size": "LLM 모델 파일(GGUF 등)이 수~수십 GB에 달해 대용량 스토리지가 필요",
            "portability":       "외장/포터블 SSD에 모델을 담아 여러 PC/기기에서 실행하려는 수요",
            "io_bottleneck":     "모델 로딩 시 디스크 I/O 속도가 병목 → NVMe SSD 필요",
            "vram_offload":      "VRAM 부족 시 모델 레이어를 디스크로 오프로드 → SSD 속도 중요",
            "capacity":          "여러 모델(7B~70B)을 동시 보유하면서 용량 부족 발생",
            "swap_speed":        "RAM/VRAM 부족 시 스왑으로 활용 → 고속 SSD 필요",
            "speed_matters":     "추론 속도 개선을 위해 NVMe SSD 속도가 중요하다는 인식",
        }
        st.markdown("**요인별 상세 설명**")
        for k, v in items[:5]:
            label = FACTOR_LABELS.get(k, k)
            exp   = explanations.get(k, "")
            st.markdown(f"- **{label}** ({v}건): {exp}")

# Tab 3: 트렌드
with tab3:
    st.subheader("수요 신호 누적 트렌드")
    if len(history) > 1:
        dates   = [h["analysis_date"][:10] for h in history]
        totals  = [h["total_posts"] for h in history]
        demands = [h["demand_total"] for h in history]
        portables = [h.get("portable_ssd_mentions", 0) for h in history]
        rates   = [h["demand_rate_pct"] for h in history]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=dates, y=totals, name="전체 포스트",
                                  line=dict(color="#64748b", width=1.5, dash="dot")))
        fig.add_trace(go.Scatter(x=dates, y=demands, name="수요 신호",
                                  line=dict(color="#ef4444", width=2.5)))
        fig.add_trace(go.Scatter(x=dates, y=portables, name="포터블 SSD",
                                  line=dict(color="#38bdf8", width=2)))
        fig.update_layout(
            height=350, yaxis_title="포스트 수",
            legend=dict(orientation="h", y=1.05),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"), margin=dict(l=10, r=10, t=30, b=10),
        )
        st.plotly_chart(fig, use_container_width=True)

        # 증감 테이블
        tbl = pd.DataFrame({
            "날짜": dates,
            "전체 포스트": totals,
            "수요 신호": demands,
            "수요율(%)": rates,
            "포터블 SSD": portables,
        })
        st.dataframe(tbl, use_container_width=True, hide_index=True)
    else:
        st.info("트렌드는 2회 이상 분석 후 표시됩니다. 현재 데이터 누적 중...")
        st.metric("현재 분석 횟수", f"{len(history)}회")

# Tab 4: 상위 포스트
with tab4:
    st.subheader("수요 신호 상위 포스트 (score 순)")
    top_posts = latest.get("top_demand_posts", [])
    if top_posts:
        with st.sidebar:
            sig_filter = st.multiselect(
                "신호 유형 필터",
                ["buy_intent", "upgrade_intent", "technical_need"],
                default=["buy_intent", "upgrade_intent", "technical_need"],
                format_func=lambda x: SIGNAL_LABELS.get(x, x),
                key="sig_filter",
            )
        filtered = [p for p in top_posts if p.get("signal") in sig_filter]

        badge_map = {
            "buy_intent":     "🔴 구매의향",
            "upgrade_intent": "🟠 교체의향",
            "technical_need": "🔵 기술필요",
        }
        for p in filtered[:25]:
            sig    = p.get("signal", "")
            badge  = badge_map.get(sig, sig)
            title  = p.get("title", "")
            quote  = p.get("key_quote", "")
            src    = p.get("source", "").replace("reddit/r/", "r/")
            score  = p.get("score", 0)
            url    = p.get("url", "#")
            ftags  = [FACTOR_LABELS.get(f, f) for f in p.get("technical_factors", [])]

            with st.expander(f"{badge}  [{title[:70]}]  — {src}  ⬆{score}"):
                st.markdown(f"🔗 [{url}]({url})")
                if quote:
                    st.markdown(f"> _{quote}_")
                if ftags:
                    st.markdown("기술 근거: " + " · ".join(ftags))
    else:
        st.info("수요 신호 포스트 없음")
