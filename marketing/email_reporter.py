"""
Email Reporter — Dynamic HTML Report + VP PPT 첨부
상황(이벤트 타입, NAND 시장, 계절)에 따라 리포트 구성과 강조점이 자동 변경됨

첨부: *_vp.pptx 파일만 (VP급 4종)
수신: abcd00ou@gmail.com
"""
import os
import random as _rnd
import smtplib
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

RECIPIENT = "abcd00ou@gmail.com"
SENDER = os.getenv("GMAIL_SENDER", "abcd00ou@gmail.com")
BASE_DIR = Path(__file__).parent
PPTX_DIR = BASE_DIR / "outputs" / "pptx"

# ── 이벤트별 리포트 설정 ──────────────────────────────────────
EVENT_CONFIG = {
    "competitor_price_cut": {
        "badge_color": "#c62828",
        "badge_text": "⚠️ 경쟁사 가격 인하 감지",
        "priority": "긴급",
        "focus_title": "경쟁 대응 전략",
        "focus_icon": "⚔️",
        "action_items": [
            "Amazon 3P 가격 모니터링 강화 (일 2회 → 4회)",
            "Extreme Pro 시리즈 프리미엄 정당화 캠페인 즉시 검토",
            "주요 SKU 가격 방어선 설정 및 VP 승인 요청",
            "채널 파트너 가격 보호 정책 발동 여부 검토",
        ],
        "analysis_focus": "competitive_response",
    },
    "nand_cost_spike": {
        "badge_color": "#e65100",
        "badge_text": "🔴 NAND 원가 급등",
        "priority": "긴급",
        "focus_title": "원가 관리 및 가격 전략 조정",
        "focus_icon": "💰",
        "action_items": [
            "BiCS8 전환 가속화로 원가 하락분 선점",
            "원가 급등 SKU 판가 인상 시나리오 준비 (VP 보고)",
            "공급 계약 재검토 — 고정가 비중 확대",
            "제품 믹스를 고마진(BiCS8) 쪽으로 즉시 전환",
        ],
        "analysis_focus": "cost_management",
    },
    "market_share_gain": {
        "badge_color": "#2e7d32",
        "badge_text": "✅ 시장점유율 상승",
        "priority": "기회",
        "focus_title": "모멘텀 가속화 전략",
        "focus_icon": "📈",
        "action_items": [
            "점유율 상승 주도 SKU 생산량 증대 요청",
            "성공 채널 마케팅 예산 추가 배정 제안",
            "경쟁사 이탈 고객 타겟 리텐션 캠페인 기획",
            "다음 분기 점유율 목표 상향 조정 검토",
        ],
        "analysis_focus": "momentum",
    },
    "promo_opportunity": {
        "badge_color": "#1565c0",
        "badge_text": "🎯 프로모션 기회",
        "priority": "액션 필요",
        "focus_title": "프로모션 실행 계획",
        "focus_icon": "🛒",
        "action_items": [
            "캠페인 크리에이티브 제작 즉시 착수 (리드타임 3주)",
            "Amazon 딜 페이지 사전 예약 및 배너 슬롯 확보",
            "소셜 인플루언서 브리핑 완료",
            "물류/재고 사전 배치 — 물류팀 협업",
        ],
        "analysis_focus": "promo_execution",
    },
    "supply_constraint": {
        "badge_color": "#6a1b9a",
        "badge_text": "⚠️ 공급 제약",
        "priority": "리스크 관리",
        "focus_title": "재고 및 공급망 관리",
        "focus_icon": "📦",
        "action_items": [
            "고마진 SKU 우선 배정 (낮은 마진 SKU 할당 축소)",
            "납기 지연 가능성 채널 파트너에 사전 통보",
            "대체 소싱 옵션 긴급 검토",
            "재고 가시성 강화 — SCM 시스템 일일 업데이트",
        ],
        "analysis_focus": "supply_risk",
    },
    "none": {
        "badge_color": "#37474f",
        "badge_text": "📊 정기 월간 리포트",
        "priority": "정기",
        "focus_title": "주요 KPI 현황",
        "focus_icon": "📋",
        "action_items": [
            "월간 실적 vs 목표 갭 분석 완료",
            "다음 달 수요 예측 리뷰 및 생산 계획 동기화",
            "채널별 재고 현황 점검",
            "마케팅 캠페인 ROI 트래킹",
        ],
        "analysis_focus": "standard",
    },
}

# ── NAND 시장 상황별 분석 섹션 ────────────────────────────────
NAND_SIGNAL_ANALYSIS = {
    "loose": {
        "title": "NAND 시장: 공급 과잉 → 원가 절감 기회",
        "color": "#1b5e20",
        "bg": "#e8f5e9",
        "body": (
            "현재 NAND 시장은 공급 과잉 국면으로, 스팟 가격이 하락세를 유지하고 있습니다. "
            "이는 WD/SanDisk에게 두 가지 기회를 의미합니다: "
            "(1) 원가 하락분을 GM 개선에 활용하거나 "
            "(2) 전략적 가격 인하로 경쟁사 대비 가격 포지션 개선. "
            "BiCS8 전환 속도를 높여 원가 이점을 극대화할 것을 권장합니다."
        ),
        "recommendation": "BiCS8 생산 비중 확대 + 고마진 SKU 중심 믹스 최적화",
    },
    "tight": {
        "title": "NAND 시장: 공급 부족 → 가격 상승 압력",
        "color": "#b71c1c",
        "bg": "#ffebee",
        "body": (
            "NAND 공급 부족 신호가 감지되고 있습니다. 스팟 가격 상승이 예상되며, "
            "이는 원가 압박으로 이어질 수 있습니다. "
            "현 재고 수준을 점검하고, 고정가 구매 계약 비중을 높여 리스크를 헤지해야 합니다. "
            "또한 가격 인상 가능성에 대해 채널 파트너와 사전 협의를 시작해야 합니다."
        ),
        "recommendation": "재고 선매입 검토 + 고정가 계약 비중 확대 + 판가 인상 시나리오 준비",
    },
    "neutral": {
        "title": "NAND 시장: 균형 상태",
        "color": "#1565c0",
        "bg": "#e3f2fd",
        "body": (
            "NAND 시장은 현재 공급·수요 균형 상태입니다. "
            "분기 CAGR 기반 원가 하락 트렌드는 유지되며, "
            "급격한 가격 변동 가능성은 낮습니다. "
            "계획된 제품 로드맵과 프로모션 일정을 예정대로 진행하되, "
            "TrendForce 월간 보고서를 통해 시장 변화를 모니터링하세요."
        ),
        "recommendation": "현 전략 유지 + 분기별 가격 정책 검토",
    },
}

# ── 계절별 강조 메시지 ─────────────────────────────────────────
SEASON_CONTEXT = {
    range(1, 4):   ("Q1 비수기", "회계연도 시작 — 연간 계획 검토 및 파이프라인 점검"),
    range(4, 7):   ("Q2 준비기", "BTS 시즌 준비 시작 — 7~8월 캠페인 크리에이티브 착수"),
    range(7, 10):  ("Q3 BTS 시즌", "Back-to-School 캠페인 최고조 — 재고 충분 여부 확인"),
    range(10, 13): ("Q4 홀리데이", "최대 매출 시즌 — 재고, 물류, 광고 풀 가동"),
}


# ── 이벤트별 액션 아이템 풀 (8개 → 시뮬 월 기반 4개 랜덤 선택) ──────────
EVENT_ACTION_POOL = {
    "competitor_price_cut": [
        "Amazon 3P 가격 모니터링 강화 (일 2회 → 4회 체크)",
        "Extreme Pro 시리즈 프리미엄 정당화 콘텐츠 즉시 업데이트",
        "주요 SKU 가격 방어선 설정 및 VP 승인 요청",
        "채널 파트너 가격 보호 정책 발동 여부 검토",
        "경쟁사 핵심 셀링포인트 분석 — 대응 메시지 개발",
        "번들 구성으로 직접적 가격 비교 회피 전략 수립",
        "고ASP·고마진 SKU 집중 홍보로 포트폴리오 믹스 방어",
        "리테일 파트너 MDF 활용 공동 캠페인 기획",
    ],
    "nand_cost_spike": [
        "BiCS8 전환 가속화로 원가 이점 선점",
        "원가 급등 SKU 판가 인상 시나리오 VP 보고 준비",
        "공급 계약 재검토 — 고정가(fixed-price) 비중 확대",
        "BiCS8 고마진 SKU 중심으로 즉시 믹스 전환",
        "단기 재고 선매입 여부 CFO와 긴급 협의",
        "SKU별 원가 민감도 분석 — 손익분기 판가 재계산",
        "BiCS5 잔여 재고 소진 가속 — 저마진 SKU 프로모 검토",
        "생산팀과 Q/Q 원가 변화율 공유 후 생산계획 재조정",
    ],
    "market_share_gain": [
        "점유율 상승 주도 SKU 생산량 즉시 증대 요청",
        "성공 채널 마케팅 예산 추가 배정 제안서 작성",
        "경쟁사 이탈 고객 타겟 리텐션 캠페인 기획",
        "다음 분기 점유율 목표 상향 조정 검토",
        "점유율 상승 채널·SKU별 기여도 분해 분석",
        "핵심 리테일 파트너 추가 선반 공간 협상 착수",
        "모멘텀 가시화 VP 보고서 — 성공 사례 문서화",
        "경쟁사 대응 프로모션 타이밍 사전 파악",
    ],
    "promo_opportunity": [
        "캠페인 크리에이티브 제작 착수 (리드타임 3주 확보)",
        "Amazon 딜 페이지 예약 및 프라임 배너 슬롯 확보",
        "소셜 인플루언서 브리핑 완료 및 서포트 요청",
        "프로모 기간 재고 사전 배치 — 물류팀 즉시 협업",
        "한정 번들 SKU 구성 및 가격 구조 확정",
        "성과 KPI 사전 정의 (노출·CTR·전환율·ROI 목표)",
        "경쟁사 프로모 캘린더 확인 — 겹치지 않도록 조정",
        "프로모 예산 CFO 사전 승인 (리드타임 1주 필요)",
    ],
    "supply_constraint": [
        "고마진 SKU 우선 배정, 저마진 SKU 할당 축소",
        "채널 파트너에 납기 지연 가능성 사전 통보",
        "대체 소싱 옵션 긴급 검토 — SCM팀 협업",
        "재고 가시성 강화 — SCM 시스템 일일 업데이트",
        "고객 주문 우선순위 매트릭스 재설정 (GM 기준)",
        "공급 제약 해소 타임라인 생산팀과 공유",
        "채널별 allocation cap 설정으로 쏠림 방지",
        "3PL 창고 입출고 우선순위 긴급 조정 요청",
    ],
    "none": [
        "월간 실적 vs 분기 목표 갭 분석 리뷰 완료",
        "수요 예측 → 생산 계획 동기화 (다음 달 준비)",
        "채널별 재고 현황 점검 — 과다/부족 SKU 식별",
        "진행 중 마케팅 캠페인 ROI 중간 집계",
        "분기 P&L 중간 점검 — VP 에스컬레이션 필요 여부 판단",
        "SKU별 sell-through rate 업데이트 및 이상치 확인",
        "경쟁사 신제품 출시 모니터링 — 영향도 분석",
        "Amazon 리뷰 평점 추이 확인 — 품질 이슈 조기 포착",
    ],
}


def _pick_actions(event_type: str, sim_month: int) -> list[str]:
    """시뮬 월을 시드로 액션 아이템 풀에서 4개 랜덤 선택 (매월 다른 조합)."""
    pool = EVENT_ACTION_POOL.get(event_type, EVENT_ACTION_POOL["none"])
    rng = _rnd.Random(sim_month * 13 + abs(hash(event_type)) % 97)
    return rng.sample(pool, min(4, len(pool)))


def _sku_label(sku: str) -> str:
    """SKU ID → 읽기 쉬운 짧은 이름."""
    return (sku
            .replace("WD_BLACK_", "")
            .replace("SD_PRO_PLUS_MICRO_", "Extreme Pro microSD ")
            .replace("SD_EXTREME_MICRO_", "Extreme microSD ")
            .replace("SD_ULTRA_MICRO_", "Ultra microSD ")
            .replace("SD_EXTREME_PRO_", "Extreme Pro ")
            .replace("SD_EXTREME_", "Extreme ")
            .replace("WD_MY_PASSPORT_", "My Passport ")
            .replace("_", " "))


def _cap_str(gb: int) -> str:
    return f"{gb}GB" if gb < 1000 else f"{gb // 1000}TB"


def _nand_body_dynamic(nand_signal: str, price_change_pct: float,
                        supply_risk: float, nand_cost_delta_pct: float) -> str:
    """NAND 시장 분석 본문 — 실제 수치를 삽입해 매번 다르게 생성."""
    if nand_signal == "loose":
        return (
            f"현재 NAND 시장은 공급 과잉 국면으로, 스팟 가격이 월 약 "
            f"{abs(price_change_pct):.1f}% 하락세를 유지하고 있습니다. "
            f"원가 절감 효과는 약 {abs(nand_cost_delta_pct):.1f}%/월로 추정되며, "
            "공급 리스크는 낮습니다. "
            "이는 WD/SanDisk에게 두 가지 기회를 제공합니다: "
            "(1) 원가 하락분을 GM 개선에 활용하거나, "
            "(2) 전략적 가격 인하로 경쟁사 대비 가격 포지션을 개선할 수 있습니다. "
            "BiCS8 전환 속도를 높여 원가 이점을 극대화할 것을 권장합니다."
        )
    elif nand_signal == "tight":
        risk_level = "높음 🔴" if supply_risk > 0.20 else "보통 🟡"
        return (
            f"NAND 공급 부족 신호가 감지되고 있습니다. "
            f"스팟 가격 월 약 +{abs(price_change_pct):.1f}% 상승이 예상되며, "
            f"공급 리스크 지수 {supply_risk * 100:.0f}%({risk_level})입니다. "
            "원가 압박이 예상되므로 현 재고 수준 점검과 "
            "고정가(fixed-price) 구매 계약 비중 확대가 필요합니다. "
            f"저용량(≤512GB) SKU 수요 강세가 예상되므로, "
            "생산 우선순위를 1TB 이하 SKU 중심으로 조정할 것을 권장합니다."
        )
    else:
        direction = "완만한 하락" if price_change_pct < 0 else "소폭 상승"
        return (
            f"NAND 시장은 현재 공급·수요 균형 상태입니다. "
            f"가격 변화율은 약 {price_change_pct:+.1f}%/월({direction}) 추세로, "
            "급격한 변동 가능성은 낮습니다. "
            "계획된 제품 로드맵과 프로모션 일정을 예정대로 진행하되, "
            "TrendForce 월간 보고서를 통해 시장 변화를 지속 모니터링하세요."
        )


def _build_spotlight(sim_data: dict, history: list, nand_signal: str) -> str:
    """
    SKU 데이터 + 시뮬 히스토리 기반으로 매월 다른 '이달의 하이라이트' HTML 생성.
    - 매출 1위 SKU, 최고 수익성 SKU, 저조 SKU, MoM 변화, NAND 신호별 인사이트,
      microSD 판매량 1위 등 7가지 후보 중 시뮬 월 기반으로 4개 선택.
    """
    sku_rev   = sim_data.get("sku_revenue", {})
    sim_month = sim_data.get("sim_month", 1)
    mi        = sim_data.get("market_intel", {})
    price_chg = mi.get("nand_cost_delta_pct", -2.0)

    bullets: list[str] = []

    # ① MoM 매출 변화 (항상 포함)
    if len(history) >= 2:
        curr     = sim_data.get("total_rev_m", 0)
        prev_r   = history[-2].get("total_rev_m", curr)
        prev_gm  = history[-2].get("blended_gm_pct", sim_data.get("blended_gm_pct", 0))
        curr_gm  = sim_data.get("blended_gm_pct", 0)
        if prev_r > 0:
            chg = (curr - prev_r) / prev_r * 100
            col = "#2e7d32" if chg > 0 else "#c62828"
            sym = "▲" if chg > 0 else "▼"
            gm_chg = curr_gm - prev_gm
            gm_col = "#2e7d32" if gm_chg > 0 else "#c62828"
            bullets.append(
                f"📊 <strong>전월 대비:</strong> 총 매출 "
                f"<span style='color:{col};font-weight:700'>{sym}{abs(chg):.1f}%</span> "
                f"(${prev_r:.1f}M→${curr:.1f}M) | GM "
                f"<span style='color:{gm_col}'>{gm_chg:+.1f}%p</span>"
            )

    if sku_rev:
        all_rev = sum(d["rev_m"] for d in sku_rev.values()) or 1

        # ② 매출 1위 SKU
        top_s, top_d = max(sku_rev.items(), key=lambda x: x[1]["rev_m"])
        bullets.append(
            f"🥇 <strong>월 매출 1위:</strong> {_sku_label(top_s)} {_cap_str(top_d['cap_gb'])} — "
            f"${top_d['rev_m']:.1f}M / {top_d['units_k']:.0f}K units / ASP ${top_d['asp']:.0f}"
        )

        # ③ 최고 수익성 SKU
        gm_s, gm_d = max(sku_rev.items(), key=lambda x: x[1]["gm_pct"])
        bullets.append(
            f"💎 <strong>최고 수익성:</strong> {_sku_label(gm_s)} {_cap_str(gm_d['cap_gb'])} — "
            f"GM {gm_d['gm_pct']:.1f}% (매출 ${gm_d['rev_m']:.1f}M)"
        )

        # ④ NAND 신호별 용량 인사이트
        if nand_signal == "tight":
            low_rev = sum(d["rev_m"] for d in sku_rev.values() if d["cap_gb"] <= 512)
            pct = low_rev / all_rev * 100
            bullets.append(
                f"⚠️ <strong>NAND Tight 영향:</strong> ≤512GB SKU 비중 {pct:.1f}% — "
                f"저용량 집중 현상 관찰 중, 생산 배분 조정 권장"
            )
        elif nand_signal == "loose":
            high_rev = sum(d["rev_m"] for d in sku_rev.values() if d["cap_gb"] >= 2000)
            pct = high_rev / all_rev * 100
            bullets.append(
                f"🟢 <strong>NAND Loose 효과:</strong> 2TB+ 고용량 비중 {pct:.1f}% — "
                f"가격 하락으로 고용량 수요 회복 중"
            )
        else:
            # neutral: SN8100 vs SN850X 비교
            sn8100_rev = sum(d["rev_m"] for s, d in sku_rev.items() if "SN8100" in s)
            sn850x_rev = sum(d["rev_m"] for s, d in sku_rev.items() if "SN850X" in s)
            if sn8100_rev and sn850x_rev:
                ratio = sn8100_rev / sn850x_rev * 100
                bullets.append(
                    f"🔄 <strong>신구 플래그십 전환:</strong> SN8100 매출이 SN850X의 {ratio:.0f}% 수준 — "
                    f"BiCS8 신제품 전환 속도 {'가속' if ratio > 80 else '진행 중'}"
                )

        # ⑤ microSD 판매량 1위
        msd = {s: d for s, d in sku_rev.items() if d["cat"] == "microsd"}
        if msd:
            vol_s, vol_d = max(msd.items(), key=lambda x: x[1]["units_k"])
            bullets.append(
                f"📦 <strong>microSD 판매량 1위:</strong> {_sku_label(vol_s)} {_cap_str(vol_d['cap_gb'])} — "
                f"{vol_d['units_k']:.0f}K units / ASP ${vol_d['asp']:.0f} / GM {vol_d['gm_pct']:.1f}%"
            )

        # ⑥ 주의 필요 SKU (매출 최하위, 단 microSD 1TB 등 원래 작은 SKU 제외)
        big_skus = {s: d for s, d in sku_rev.items() if d["cat"] != "microsd" or d["cap_gb"] >= 1000}
        if big_skus:
            low_s, low_d = min(big_skus.items(), key=lambda x: x[1]["rev_m"])
            bullets.append(
                f"🔻 <strong>저조 SKU 주의:</strong> {_sku_label(low_s)} {_cap_str(low_d['cap_gb'])} — "
                f"${low_d['rev_m']:.1f}M / {low_d['units_k']:.0f}K units (재고·프로모 검토 권장)"
            )

        # ⑦ BiCS8 원가 동향
        nand_costs = sim_data.get("nand_cost_per_gb", {})
        if "BiCS8" in nand_costs and "BiCS6" in nand_costs:
            gap_pct = (nand_costs["BiCS6"] - nand_costs["BiCS8"]) / nand_costs["BiCS6"] * 100
            bullets.append(
                f"⚙️ <strong>BiCS8 원가 우위:</strong> ${nand_costs['BiCS8']:.4f}/GB — "
                f"BiCS6 대비 {gap_pct:.1f}% 저렴 (원가 {price_chg:+.1f}%/월 조정 반영)"
            )

    if not bullets:
        return ""

    # 시뮬 월 기반으로 셔플 후 4개 선택 (①MoM은 항상 포함)
    rng = _rnd.Random(sim_month * 19 + 5)
    fixed   = bullets[:1]          # MoM 항상 첫 번째
    rotated = bullets[1:]
    rng.shuffle(rotated)
    selected = fixed + rotated[:3]

    items = "".join(
        f'<li style="margin-bottom:8px;font-size:12px;color:#333;line-height:1.6">{b}</li>'
        for b in selected
    )
    return (
        '<div class="section-title">🔎 이달의 하이라이트</div>'
        '<div style="background:#f8f9ff;border:1px solid #dde4ff;border-radius:8px;'
        'padding:14px 18px;margin:12px 0">'
        f'<ul style="margin:0;padding-left:20px">{items}</ul>'
        '</div>'
    )


def _get_season_context(month: int) -> tuple[str, str]:
    for r, ctx in SEASON_CONTEXT.items():
        if month in r:
            return ctx
    return ("", "")


def _prev_month_delta(sim_data: dict, history: list) -> dict:
    """이전 달 대비 변화율 계산."""
    if not history or len(history) < 2:
        return {}
    prev = history[-2] if len(history) >= 2 else {}
    curr_rev = sim_data.get("total_rev_m", 0)
    prev_rev = prev.get("total_rev_m", curr_rev)
    curr_gm  = sim_data.get("blended_gm_pct", 0)
    prev_gm  = prev.get("blended_gm_pct", curr_gm)
    rev_chg  = (curr_rev - prev_rev) / prev_rev * 100 if prev_rev else 0
    gm_chg   = curr_gm - prev_gm
    return {"rev_chg": round(rev_chg, 1), "gm_chg": round(gm_chg, 2)}


def _delta_arrow(val: float, unit: str = "%") -> str:
    if val > 0.1:
        return f"<span style='color:#2e7d32'>▲ {val:+.1f}{unit}</span>"
    elif val < -0.1:
        return f"<span style='color:#c62828'>▼ {val:+.1f}{unit}</span>"
    return f"<span style='color:#666'>→ {val:+.1f}{unit}</span>"


def _build_html(sim_data: dict, agent_results: dict,
                market_intel: dict | None, history: list) -> str:
    """상황 기반 동적 HTML 리포트 생성."""

    sim_date    = sim_data.get("sim_date", "N/A")
    total_rev   = sim_data.get("total_rev_m", 0)
    blended_gm  = sim_data.get("blended_gm_pct", 0)
    rev         = sim_data.get("revenue_m", {})
    gm          = sim_data.get("gross_margin_pct", {})
    mshare      = sim_data.get("market_share_pct", {})
    nand        = sim_data.get("nand_cost_per_gb", {})
    event_data  = sim_data.get("event", {})
    promo       = sim_data.get("promo")
    mi          = sim_data.get("market_intel", {})
    sim_month   = sim_data.get("sim_month", 1)

    event_type  = event_data.get("type", "none")
    event_desc  = event_data.get("description", "")
    cfg         = EVENT_CONFIG.get(event_type, EVENT_CONFIG["none"])

    nand_signal = mi.get("nand_signal", "neutral")
    price_trend = mi.get("price_trend", "flat")
    nand_analysis = NAND_SIGNAL_ANALYSIS.get(nand_signal, NAND_SIGNAL_ANALYSIS["neutral"])

    season_label, season_msg = _get_season_context(sim_month)
    deltas = _prev_month_delta(sim_data, history)
    rev_arrow = _delta_arrow(deltas.get("rev_chg", 0), "%")
    gm_arrow  = _delta_arrow(deltas.get("gm_chg", 0), "%p")

    success_cnt = sum(1 for v in agent_results.values() if v)
    total_cnt   = len(agent_results)
    now_str     = datetime.now().strftime("%Y-%m-%d %H:%M KST")

    # ── 뉴스 헤드라인 (시장 인텔 있을 때만) ──────────────────────
    headlines_html = ""
    if market_intel and market_intel.get("headlines"):
        hl_items = "".join(
            f'<li style="margin-bottom:4px;font-size:12px;color:#444">'
            f'<a href="{h.get("url","#")}" style="color:#1565c0;text-decoration:none">'
            f'{h["title"][:100]}</a>'
            f'<span style="color:#999;margin-left:6px">{h.get("date","")[:10]}</span></li>'
            for h in market_intel["headlines"][:5]
        )
        headlines_html = f"""
        <div class="section-title">📰 NAND 시장 뉴스 (실시간)</div>
        <ul style="margin:0 0 16px;padding-left:18px">{hl_items}</ul>"""

    # ── SKU 세분화 테이블 ────────────────────────────────────────
    sku_data = sim_data.get("sku_revenue", {})
    _cat_order  = ["internal_ssd", "external_ssd", "microsd"]
    _cat_header = {
        "internal_ssd": "▸ Internal SSD — WD_BLACK",
        "external_ssd": "▸ External SSD — SanDisk",
        "microsd":      "▸ microSD — SanDisk",
    }
    _line_order = {
        "internal_ssd": ["SN8100", "SN850X", "SN7100", "SN770"],
        "external_ssd": ["Extreme Pro", "Extreme", "My Passport"],
        "microsd":      ["Extreme Pro", "Extreme", "Ultra"],
    }

    def _cap_label(gb: int) -> str:
        return f"{gb}GB" if gb < 1000 else f"{gb // 1000}TB"

    sku_rows = ""
    for cat in _cat_order:
        skus_in_cat = [(s, d) for s, d in sku_data.items() if d.get("cat") == cat]
        if not skus_in_cat:
            continue
        sku_rows += (f'<tr style="background:#e8eaf6">'
                     f'<td colspan="6" style="padding:7px 12px;font-weight:700;font-size:12px;'
                     f'color:#283593">{_cat_header[cat]}</td></tr>')
        for line_name in _line_order.get(cat, []):
            line_skus = sorted(
                [(s, d) for s, d in skus_in_cat if d.get("line") == line_name],
                key=lambda x: x[1]["cap_gb"]
            )
            if not line_skus:
                continue
            line_rev_total   = sum(d["rev_m"] for _, d in line_skus)
            line_units_total = sum(d["units_k"] for _, d in line_skus)
            for i, (sku, d) in enumerate(line_skus):
                line_cell = f'<strong>{line_name}</strong>' if i == 0 else ""
                cap       = _cap_label(d["cap_gb"])
                # NAND tight 시 저용량 강조
                row_bg = ""
                if nand_signal == "tight" and d["cap_gb"] <= 256:
                    row_bg = "background:#fff8e1;"
                elif nand_signal == "tight" and d["cap_gb"] <= 512:
                    row_bg = "background:#fffde7;"
                sku_rows += (
                    f'<tr style="{row_bg}">'
                    f'<td style="padding:5px 12px;border-bottom:1px solid #f0f0f0;font-size:12px">{line_cell}</td>'
                    f'<td style="padding:5px 12px;border-bottom:1px solid #f0f0f0;font-size:12px">{cap}</td>'
                    f'<td style="padding:5px 12px;border-bottom:1px solid #f0f0f0;text-align:right;font-size:12px">${d["rev_m"]:.1f}M</td>'
                    f'<td style="padding:5px 12px;border-bottom:1px solid #f0f0f0;text-align:right;font-size:12px">{d["units_k"]:.1f}K</td>'
                    f'<td style="padding:5px 12px;border-bottom:1px solid #f0f0f0;text-align:right;font-size:12px">${d["asp"]:.0f}</td>'
                    f'<td style="padding:5px 12px;border-bottom:1px solid #f0f0f0;text-align:right;font-size:12px">{d["gm_pct"]:.1f}%</td>'
                    f'</tr>'
                )
            # 라인 소계
            sku_rows += (
                f'<tr style="background:#f5f5f5">'
                f'<td colspan="2" style="padding:4px 12px;font-size:11px;color:#777;border-bottom:1px solid #e0e0e0">'
                f'  {line_name} 소계</td>'
                f'<td style="padding:4px 12px;text-align:right;font-size:11px;color:#555;border-bottom:1px solid #e0e0e0">${line_rev_total:.1f}M</td>'
                f'<td style="padding:4px 12px;text-align:right;font-size:11px;color:#555;border-bottom:1px solid #e0e0e0">{line_units_total:.1f}K</td>'
                f'<td colspan="2" style="border-bottom:1px solid #e0e0e0"></td></tr>'
            )

    # NAND tight 저용량 강조 안내
    tight_notice = ""
    if nand_signal == "tight":
        tight_notice = ('<div style="font-size:11px;color:#c62828;padding:4px 0 8px">'
                        '⚠️ NAND Tight — 저용량(≤512GB) 노란색 강조: 현재 시장 강세 SKU</div>')

    # ── 카테고리 합계 (하단 소계) ───────────────────────────────
    cat_labels = {"external_ssd": "External SSD", "internal_ssd": "Internal SSD", "microsd": "microSD"}
    cat_rows = ""
    for cat, label in cat_labels.items():
        r  = rev.get(cat, 0)
        g  = gm.get(cat, 0)
        ms = mshare.get(cat, 0)
        cat_rows += f"""<tr>
          <td style="padding:8px 12px;border-bottom:1px solid #eee;font-weight:600">{label}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:right">${r:.1f}M</td>
          <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:right">{g:.1f}%</td>
          <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:right">{ms:.1f}%</td>
        </tr>"""

    # ── NAND 원가 ─────────────────────────────────────────────
    nand_rows = "".join(
        f'<tr><td style="padding:6px 12px;border-bottom:1px solid #eee">{gen}</td>'
        f'<td style="padding:6px 12px;border-bottom:1px solid #eee;text-align:right">${cost:.4f}/GB</td></tr>'
        for gen, cost in nand.items()
    )

    # ── Action Items (시뮬 월 기반 풀에서 4개 랜덤 선택) ────────────
    action_items_html = "".join(
        f'<li style="margin-bottom:6px;font-size:13px">{item}</li>'
        for item in _pick_actions(event_type, sim_month)
    )

    # ── 이달의 하이라이트 (SKU 데이터 기반 동적 생성) ──────────────
    spotlight_html = _build_spotlight(sim_data, history, nand_signal)

    # ── NAND 분석 본문 (실제 수치 삽입) ─────────────────────────────
    nand_body_text = _nand_body_dynamic(
        nand_signal,
        market_intel.get("price_change_pct", mi.get("nand_cost_delta_pct", -2.0)) if market_intel else mi.get("nand_cost_delta_pct", -2.0),
        mi.get("supply_risk", 0.10),
        mi.get("nand_cost_delta_pct", -2.0),
    )

    # ── 프로모 섹션 ──────────────────────────────────────────────
    promo_html = ""
    if promo:
        ptype = "Holiday" if promo["type"] == "holiday" else "BTS"
        promo_html = f"""
        <div style="background:#e8f5e9;border-left:4px solid #4caf50;padding:12px 16px;margin:12px 0;border-radius:4px">
          <strong>🎯 프로모션 기회: {ptype} 캠페인</strong><br>
          추천 투자: ${promo['invest_m']:.1f}M &nbsp;→&nbsp;
          예상 추가 매출: ${promo['incremental_rev_m']:.1f}M &nbsp;|&nbsp;
          ROI: <strong>{promo['roi']:.2f}×</strong>
        </div>"""

    # ── 에이전트 상태 ────────────────────────────────────────────
    agent_labels = {
        "production": "생산 에이전트",
        "supply": "공급 에이전트",
        "demand_excel": "수요예측 Excel",
        "demand_pptx_vp": "수요예측 VP PPT",
        "strategy_excel": "마케팅 전략 Excel",
        "strategy_pptx_vp": "마케팅 전략 VP PPT",
        "marcom_pptx_vp": "MarCom VP PPT",
        "product_mix_pptx_vp": "Product Mix VP PPT",
    }
    agent_rows = "".join(
        f'<tr><td style="padding:5px 12px;border-bottom:1px solid #f0f0f0;font-size:12px">{agent_labels.get(k, k)}</td>'
        f'<td style="padding:5px 12px;border-bottom:1px solid #f0f0f0;text-align:center">{"✅" if v else "❌"}</td></tr>'
        for k, v in agent_results.items()
    )

    price_trend_ko = {"up": "상승↑", "down": "하락↓", "flat": "보합→"}

    html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', sans-serif;
         margin:0; background:#f0f2f5; color:#222; }}
  .wrap {{ max-width:700px; margin:20px auto; }}
  .header {{ background:linear-gradient(135deg,#0d1b6e 0%,#1428A0 60%,#1565c0 100%);
             color:#fff; padding:28px 32px; border-radius:12px 12px 0 0; }}
  .header h1 {{ margin:0 0 6px; font-size:20px; font-weight:700; letter-spacing:-.3px; }}
  .header .meta {{ opacity:.8; font-size:12px; margin-top:4px; }}
  .event-banner {{ background:{cfg['badge_color']}; color:#fff;
                   padding:10px 32px; font-weight:700; font-size:13px;
                   display:flex; align-items:center; gap:10px; }}
  .priority-tag {{ background:rgba(255,255,255,.25); border-radius:4px;
                   padding:2px 8px; font-size:11px; }}
  .body {{ background:#fff; padding:28px 32px; }}
  .kpi-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:24px; }}
  .kpi {{ background:#f7f9ff; border:1px solid #dde3ff; border-radius:8px;
          padding:14px 16px; text-align:center; }}
  .kpi-value {{ font-size:22px; font-weight:700; color:#1428A0; }}
  .kpi-sub {{ font-size:11px; color:#888; margin-top:2px; }}
  .kpi-label {{ font-size:11px; color:#555; margin-top:6px; }}
  table {{ width:100%; border-collapse:collapse; margin-bottom:16px; font-size:13px; }}
  th {{ background:#f0f2ff; padding:8px 12px; text-align:left; font-size:11px;
        color:#444; font-weight:700; text-transform:uppercase; letter-spacing:.4px; }}
  th:not(:first-child) {{ text-align:right; }}
  .section-title {{ font-size:12px; font-weight:700; color:#1428A0; margin:20px 0 8px;
                    text-transform:uppercase; letter-spacing:.6px; border-bottom:2px solid #e0e4ff;
                    padding-bottom:4px; }}
  .nand-box {{ background:{nand_analysis['bg']}; border-left:4px solid {nand_analysis['color']};
               padding:12px 16px; margin:12px 0; border-radius:0 6px 6px 0; }}
  .nand-box strong {{ color:{nand_analysis['color']}; }}
  .action-box {{ background:#fff8e1; border:1px solid #ffe082; border-radius:8px;
                 padding:14px 18px; margin:12px 0; }}
  .season-banner {{ background:#e8eaf6; border-radius:6px; padding:8px 14px;
                    font-size:12px; color:#3949ab; margin-bottom:16px; }}
  .footer {{ background:#f0f2ff; padding:14px 32px; border-radius:0 0 12px 12px;
             font-size:10px; color:#999; }}
  a {{ color:#1428A0; }}
</style>
</head>
<body>
<div class="wrap">

<div class="header">
  <h1>SanDisk B2C Marketing Intelligence</h1>
  <div class="meta">
    시뮬레이션 월: <strong>{sim_date}</strong> &nbsp;|&nbsp;
    {season_label} &nbsp;|&nbsp;
    에이전트: {success_cnt}/{total_cnt} &nbsp;|&nbsp;
    {now_str}
  </div>
</div>

<div class="event-banner">
  {cfg['badge_text']}
  <span class="priority-tag">{cfg['priority']}</span>
  {'&nbsp;&nbsp;' + event_desc if event_desc else ''}
</div>

<div class="body">

  <!-- 계절 컨텍스트 -->
  <div class="season-banner">📅 {season_label}: {season_msg}</div>

  <!-- KPI -->
  <div class="kpi-grid">
    <div class="kpi">
      <div class="kpi-value">${total_rev:.1f}M</div>
      <div class="kpi-sub">{rev_arrow}</div>
      <div class="kpi-label">월 총 매출</div>
    </div>
    <div class="kpi">
      <div class="kpi-value">{blended_gm:.1f}%</div>
      <div class="kpi-sub">{gm_arrow}</div>
      <div class="kpi-label">블렌딩 GM%</div>
    </div>
    <div class="kpi">
      <div class="kpi-value">{mshare.get('external_ssd',0):.1f}%</div>
      <div class="kpi-sub">SSD 시장</div>
      <div class="kpi-label">External SSD 점유율</div>
    </div>
  </div>

  <!-- NAND 시장 분석 -->
  <div class="section-title">🔬 NAND 시장 분석 (실시간)</div>
  <div class="nand-box">
    <strong>{nand_analysis['title']}</strong><br>
    <span style="font-size:12px;color:#333;margin-top:6px;display:block">
      가격 트렌드: <strong>{price_trend_ko.get(price_trend,'—')}</strong>
      &nbsp;|&nbsp;
      원가 보정: <strong>{mi.get('nand_cost_delta_pct', -2.0):+.1f}%</strong>/월
      &nbsp;|&nbsp;
      공급 리스크: <strong>{mi.get('supply_risk', 0.10)*100:.0f}%</strong>
    </span>
    <p style="margin:8px 0 4px;font-size:12px;color:#444">{nand_body_text}</p>
    <div style="font-size:11px;font-weight:700;color:{nand_analysis['color']}">
      → {nand_analysis['recommendation']}
    </div>
  </div>

  {headlines_html}

  <!-- 이번 달 Focus -->
  <div class="section-title">{cfg['focus_icon']} {cfg['focus_title']} — 이번 달 우선순위</div>
  <div class="action-box">
    <strong style="font-size:13px">✅ Action Items</strong>
    <ol style="margin:8px 0 0;padding-left:18px">{action_items_html}</ol>
  </div>

  {promo_html}

  {spotlight_html}

  <!-- SKU 세분화 실적 -->
  <div class="section-title">📦 제품 라인 × 용량별 월간 실적 (SKU 세분화)</div>
  {tight_notice}
  <table>
    <tr>
      <th>제품 라인</th><th>용량</th><th>월 매출</th>
      <th>판매량(K)</th><th>ASP</th><th>GM%</th>
    </tr>
    {sku_rows}
    <tr style="background:#eef;font-weight:700">
      <td style="padding:8px 12px" colspan="2">전체 합계</td>
      <td style="padding:8px 12px;text-align:right">${total_rev:.1f}M</td>
      <td style="padding:8px 12px;text-align:right">—</td>
      <td style="padding:8px 12px;text-align:right">—</td>
      <td style="padding:8px 12px;text-align:right">{blended_gm:.1f}%</td>
    </tr>
  </table>

  <!-- 카테고리 요약 -->
  <div class="section-title">📊 카테고리 요약</div>
  <table>
    <tr><th>카테고리</th><th>매출</th><th>GM%</th><th>점유율</th></tr>
    {cat_rows}
    <tr style="background:#f7f9ff;font-weight:700">
      <td style="padding:8px 12px">합계</td>
      <td style="padding:8px 12px;text-align:right">${total_rev:.1f}M</td>
      <td style="padding:8px 12px;text-align:right">{blended_gm:.1f}%</td>
      <td style="padding:8px 12px;text-align:right">—</td>
    </tr>
  </table>

  <!-- NAND 원가 -->
  <div class="section-title">⚙️ NAND 원가 현황</div>
  <table>
    <tr><th>NAND 세대</th><th>$/GB</th></tr>
    {nand_rows}
  </table>

  <!-- 에이전트 -->
  <div class="section-title">🤖 에이전트 실행 결과</div>
  <table>
    <tr><th>에이전트</th><th style="text-align:center">상태</th></tr>
    {agent_rows}
  </table>

  <div style="background:#e3f2fd;border-radius:6px;padding:10px 14px;font-size:12px;color:#1565c0;margin-top:16px">
    📎 <strong>VP급 PPT {_count_vp_pptx()}종 첨부</strong>:
    수요예측 · 마케팅전략 · MarCom · Product Mix
  </div>

</div>

<div class="footer">
  SanDisk B2C Marketing AI Agent System — 시뮬레이션 자료 (1h=1month)<br>
  실시간 NAND 시장 데이터 연동 | {now_str}
</div>

</div>
</body>
</html>"""
    return html


def _count_vp_pptx() -> int:
    if not PPTX_DIR.exists():
        return 0
    return len(list(PPTX_DIR.glob("*_vp.pptx")))


def send_report(sim_data: dict, agent_results: dict,
                market_intel: dict | None = None,
                history: list | None = None) -> bool:
    """
    동적 HTML 리포트 + VP PPT만 첨부하여 이메일 전송.
    """
    app_password = os.getenv("GMAIL_APP_PASSWORD", "")
    if not app_password:
        print("  [Email] ⚠️  GMAIL_APP_PASSWORD 미설정 — 건너뜀")
        return False

    sim_date   = sim_data.get("sim_date", "N/A")
    total_rev  = sim_data.get("total_rev_m", 0)
    event_type = sim_data.get("event", {}).get("type", "none")
    cfg        = EVENT_CONFIG.get(event_type, EVENT_CONFIG["none"])

    subject = (f"[SanDisk MktgAI] {sim_date} | {cfg['badge_text']} | "
               f"Rev ${total_rev:.1f}M | GM {sim_data.get('blended_gm_pct',0):.1f}%")

    msg = MIMEMultipart("mixed")
    msg["From"]    = SENDER
    msg["To"]      = RECIPIENT
    msg["Subject"] = subject

    html_content = _build_html(sim_data, agent_results,
                                market_intel, history or [])
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    # VP PPT만 첨부 (*_vp.pptx)
    attached = 0
    if PPTX_DIR.exists():
        for pptx in sorted(PPTX_DIR.glob("*_vp.pptx")):
            try:
                with open(pptx, "rb") as f:
                    part = MIMEBase("application",
                                    "vnd.openxmlformats-officedocument.presentationml.presentation")
                    part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header("Content-Disposition", "attachment",
                                filename=f"{sim_date}_{pptx.name}")
                msg.attach(part)
                attached += 1
            except Exception as e:
                print(f"  [Email] PPT 첨부 실패 {pptx.name}: {e}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER, app_password.replace(" ", ""))
            server.sendmail(SENDER, RECIPIENT, msg.as_string())
        print(f"  [Email] ✅ 전송 완료 → {RECIPIENT} | VP PPT {attached}종 첨부")
        return True
    except smtplib.SMTPAuthenticationError:
        print("  [Email] ❌ Gmail 앱 비밀번호 오류")
        return False
    except Exception as e:
        print(f"  [Email] ❌ 전송 실패: {e}")
        return False
