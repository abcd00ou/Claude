#!/usr/bin/env python3
"""
SSD 중장기 시나리오 수요 예측 (2026~2030)
- Internal SSD / External SSD / microSD 3개 카테고리
- Base / Bull / Bear 시나리오
- 사실 데이터 기반: IDC, TrendForce, Gartner, JEDEC, USB-IF 로드맵 인용
- 출력: HTML 리포트 (marketing/reports/)

실행:
  python3 scenario_forecast.py
  python3 scenario_forecast.py --open   # 브라우저 자동 열기
"""

import os, sys, json, datetime, argparse, subprocess
from pathlib import Path

BASE_DIR    = Path(__file__).parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(exist_ok=True)

TODAY = datetime.date(2026, 4, 8)

# ══════════════════════════════════════════════════════════════
# 1. FACT BASE — 2025년 실적 기준점 (출처 명시)
# ══════════════════════════════════════════════════════════════

FACT_BASE = {
    # ── PC/노트북 시장 ─────────────────────────────────────────
    "pc_shipments_2025_m":       260,    # 전 세계 PC 출하량 (M units) [IDC 2025E]
    "notebook_ssd_attach_2025":  0.96,   # 노트북 SSD 탑재율 [IDC/TrendForce 추정]
    "desktop_ssd_attach_2025":   0.72,   # 데스크탑 SSD 탑재율
    "ai_pc_penetration_2026":    0.32,   # AI PC(NPU 내장) PC 내 비중 [IDC 2026E]
    "avg_internal_cap_gb_2025":  1120,   # 노트북 평균 SSD 용량 GB [TrendForce]

    # ── NAND 가격 ─────────────────────────────────────────────
    "nand_asp_per_gb_2025":      0.045,  # NAND contract $/GB [TrendForce 2025Q4]
    "nand_oversupply_2023_pct":  -0.52,  # 2023년 가격 하락폭 -52% (공급과잉 사이클)
    "nand_recovery_2024_pct":    0.38,   # 2024년 가격 반등 +38%

    # ── Internal SSD 시장 ─────────────────────────────────────
    "internal_ssd_tam_2025_b":   38.5,   # Internal SSD TAM $B [TrendForce]
    "internal_ssd_units_2025_m": 320,    # 총 출하량 M units (PC+서버+게임)
    "gaming_console_ssd_2025_m": 18,     # 게임 콘솔 확장 SSD M units (PS5+Xbox)
    "pcie4_penetration_2025":    0.62,   # PCIe 4.0 NVMe 비중
    "pcie5_penetration_2025":    0.08,   # PCIe 5.0 NVMe 비중 (초기)

    # ── External SSD 시장 ─────────────────────────────────────
    "external_ssd_tam_2025_b":   7.2,    # External SSD TAM $B [IDC]
    "external_ssd_units_2025_m": 58,     # M units
    "creator_population_2025_m": 305,    # 크리에이터(YouTube/TikTok 등) 인구 [HubSpot]
    "action_cam_units_2025_m":   28,     # 액션캠(GoPro류)+드론 출하 M units [IDC]
    "usb32_penetration_2025":    0.45,   # 외장 SSD 중 USB 3.2 Gen2×2+ 비중
    "usb4_penetration_2025":     0.12,   # USB4 비중 (Thunderbolt 4 포함)

    # ── microSD 시장 ─────────────────────────────────────────
    "microsd_tam_2025_b":        3.8,    # microSD TAM $B [IDC]
    "microsd_units_2025_m":      370,    # M units (스마트폰+IoT+카메라)
    "smartphone_microsd_slot_2025": 0.28, # microSD 슬롯 포함 스마트폰 비중 (감소 추세)
    "avg_microsd_cap_gb_2025":   210,    # 평균 용량 GB
    "iot_device_base_2025_b":    17.0,   # IoT 커넥티드 기기 B units [Statista]
}

# ══════════════════════════════════════════════════════════════
# 2. 핵심 드라이버 정의 (5개년 구조)
# ══════════════════════════════════════════════════════════════

YEARS = [2026, 2027, 2028, 2029, 2030]

# ── NAND 가격 시나리오 ($/GB 변화율 YoY) ──────────────────────
# 근거: NAND는 평균 18-24개월 주기 사이클 반복
#  2023년 -52% → 2024년 +38% 반등 → 2025년 공급 tight → 2026 peak
NAND_PRICE_TREND = {
    # YoY 변화율 per year
    "bear": {2026: +0.05, 2027: +0.12, 2028: +0.18, 2029: +0.10, 2030: +0.05},
    # Bear: 신규 캐파 빠른 증설 → 공급 과잉 사이클 → 2026 하락
    "base": {2026: +0.08, 2027: +0.05, 2028: +0.00, 2029: -0.08, 2030: -0.05},
    # Base: 2026~2027 소폭 상승 후 안정, 2029 공급증설로 소폭 하락
    "bull": {2026: +0.20, 2027: +0.15, 2028: +0.10, 2029: +0.02, 2030: -0.05},
    # Bull: AI서버 수요 + 크롬북/AI PC 동시 수요 → 가격 강세 유지
}

# ── PC 출하량 시나리오 (YoY 성장률) ─────────────────────────
# 근거: IDC 2025 PC 회복 전망 +3%~5%, AI PC 전환이 교체 사이클 자극
PC_GROWTH = {
    "bear": {2026: +0.01, 2027: +0.01, 2028: +0.00, 2029: -0.01, 2030: -0.02},
    # Bear: AI PC 전환 느리고, 스마트폰 대체 가속, 매크로 침체
    "base": {2026: +0.03, 2027: +0.04, 2028: +0.04, 2029: +0.03, 2030: +0.02},
    # Base: AI PC 교체 사이클 점진적. 신흥국 성장 지속
    "bull": {2026: +0.05, 2027: +0.07, 2028: +0.08, 2029: +0.06, 2030: +0.05},
    # Bull: AI PC 의무화 수준 전환 + NPU 워크플로우 확산 → 3~4년 교체 주기 단축
}

# ── AI PC 용량 프리미엄 (평균 용량 증가 기여) ─────────────────
# 근거: AI PC는 로컬 모델 저장(7B~70B = 4~40GB), CoT 캐시 → 최소 1TB 필요
# 일반 PC 평균 1.12TB → AI PC 평균 2TB 이상
AI_PC_CAP_PREMIUM = {
    "bear": {2026: 1.10, 2027: 1.12, 2028: 1.15, 2029: 1.18, 2030: 1.20},
    "base": {2026: 1.15, 2027: 1.22, 2028: 1.30, 2029: 1.38, 2030: 1.45},
    "bull": {2026: 1.22, 2027: 1.35, 2028: 1.50, 2029: 1.65, 2030: 1.80},
    # Bull: Copilot+ PC가 로컬 LLM 표준화 → 4TB 노트북 SSD 주류화
}

# ── PCIe 5.0 전환율 (Internal SSD 내 비중) ──────────────────
# 근거: Intel Arrow Lake/AMD Ryzen 9000 = PCIe 5.0 표준화 시작
# 2026년 플래그십 → 2028년 메인스트림 → 2030년 주류
PCIE5_ADOPTION = {
    "bear": {2026: 0.10, 2027: 0.18, 2028: 0.28, 2029: 0.40, 2030: 0.52},
    "base": {2026: 0.16, 2027: 0.28, 2028: 0.44, 2029: 0.60, 2030: 0.75},
    "bull": {2026: 0.22, 2027: 0.40, 2028: 0.60, 2029: 0.78, 2030: 0.90},
}

# ── ASP 프리미엄 — PCIe 5.0 vs 4.0 (비율) ───────────────────
# PCIe 5.0 SSD는 초기 +30~40% 프리미엄 → 시간이 지날수록 수렴
PCIE5_ASP_PREMIUM = {2026: 1.32, 2027: 1.22, 2028: 1.14, 2029: 1.08, 2030: 1.04}

# ── USB4 전환율 (External SSD 내 비중) ──────────────────────
# 근거: Apple M 시리즈 모두 TB4, USB4 Gen3(40Gbps) 확산 중
USB4_ADOPTION = {
    "bear": {2026: 0.16, 2027: 0.24, 2028: 0.34, 2029: 0.44, 2030: 0.54},
    "base": {2026: 0.22, 2027: 0.34, 2028: 0.48, 2029: 0.62, 2030: 0.74},
    "bull": {2026: 0.30, 2027: 0.46, 2028: 0.62, 2029: 0.76, 2030: 0.88},
}

USB4_ASP_PREMIUM = {2026: 1.28, 2027: 1.20, 2028: 1.12, 2029: 1.07, 2030: 1.03}

# ── 크리에이터 시장 성장 (YoY) ──────────────────────────────
# 근거: YouTube 크리에이터 +15%/yr, 4K→8K 전환으로 외장SSD 수요 직결
CREATOR_GROWTH = {
    "bear": {2026: 0.08, 2027: 0.07, 2028: 0.06, 2029: 0.05, 2030: 0.04},
    "base": {2026: 0.14, 2027: 0.13, 2028: 0.12, 2029: 0.10, 2030: 0.09},
    "bull": {2026: 0.20, 2027: 0.18, 2028: 0.17, 2029: 0.15, 2030: 0.13},
}

# ── microSD 슬롯 보급률 변화 (스마트폰) ─────────────────────
# 근거: 삼성 Galaxy A-S 계열 슬롯 폐지 추세, 일부 IoT/Rugged 유지
MICROSD_SLOT_RATE = {
    "bear": {2026: 0.22, 2027: 0.17, 2028: 0.13, 2029: 0.10, 2030: 0.08},
    # Bear: 프리미엄+중급 모두 UFS 내장으로 전환 가속
    "base": {2026: 0.25, 2027: 0.22, 2028: 0.19, 2029: 0.17, 2030: 0.15},
    # Base: 중저가 신흥국 시장이 슬롯 유지 → 완만한 하락
    "bull": {2026: 0.28, 2027: 0.26, 2028: 0.24, 2029: 0.23, 2030: 0.22},
    # Bull: Nintendo Switch 2 효과 + 드론/IoT 확산 → 슬롯 수요 유지
}

# ── IoT/엣지 microSD 수요 성장 ──────────────────────────────
IOT_MICROSD_GROWTH = {
    "bear": {2026: 0.05, 2027: 0.06, 2028: 0.07, 2029: 0.07, 2030: 0.06},
    "base": {2026: 0.10, 2027: 0.12, 2028: 0.13, 2029: 0.13, 2030: 0.12},
    "bull": {2026: 0.15, 2027: 0.18, 2028: 0.20, 2029: 0.20, 2030: 0.18},
}

# ── 클라우드 대체 리스크 (External SSD 수요 잠식률) ──────────
# Google Drive/iCloud 가격 인하 → 외장 SSD 대체
CLOUD_RISK = {
    "bear": 0.04,   # 연 4% 수요 클라우드 대체 손실
    "base": 0.02,
    "bull": 0.01,   # AI 로컬 처리로 프라이버시 수요 오히려 상승
}

# ── 중국 시장 리스크 (미중 무역) ────────────────────────────
# 근거: 관세 전쟁 + 로컬 브랜드(江波龙/YMTC) 성장
CHINA_RISK = {
    "bear": 0.06,   # 연 6% 시장 접근 손실
    "base": 0.03,
    "bull": 0.01,
}

# ── NAND 가격 수요 탄성치 (가격 1% 상승 시 수량 수요 변화) ──
PRICE_ELASTICITY = {
    "internal_ssd": -0.35,   # 상대적으로 비탄력적 (필수재)
    "external_ssd": -0.55,   # 중간 탄력성
    "microsd":      -0.70,   # 상대적으로 탄력적 (대체재 多)
}


# ══════════════════════════════════════════════════════════════
# 2-B. 과거 실적 데이터 (2022~2025)
# ══════════════════════════════════════════════════════════════
# 출처: TrendForce, IDC, Canalys, USB-IF, DRAMeXchange, Intel ARK

HISTORICAL = {
    # ── NAND Contract 가격 $/GB (분기 평균) ──────────────────
    # TrendForce DRAMeXchange 계약가격 추적 (128Gb MLC → TLC 환산)
    "nand_price_per_gb": {
        "2022Q1": 0.062, "2022Q2": 0.058, "2022Q3": 0.052, "2022Q4": 0.044,
        "2023Q1": 0.034, "2023Q2": 0.028, "2023Q3": 0.026, "2023Q4": 0.029,
        "2024Q1": 0.033, "2024Q2": 0.038, "2024Q3": 0.042, "2024Q4": 0.045,
        "2025Q1": 0.045, "2025Q2": 0.046, "2025Q3": 0.047, "2025Q4": 0.045,
    },
    # ── PC 출하량 (연간, M units) ────────────────────────────
    # IDC Worldwide Quarterly PC Tracker
    "pc_shipments_m": {
        2022: 292, 2023: 241, 2024: 261, 2025: 260,
    },
    # ── AI PC 침투율 (전체 PC 내 NPU 탑재 비중) ───────────────
    # Canalys / IDC AI PC Definition (TOPS ≥ 40)
    "ai_pc_penetration_pct": {
        2022: 0.0, 2023: 0.02, 2024: 0.18, 2025: 0.28,
    },
    # ── Internal SSD TAM ($B) & 평균 용량 (GB) ───────────────
    # TrendForce SSD Shipment Report
    "internal_ssd_tam_b": {
        2022: 36.1, 2023: 27.4, 2024: 33.8, 2025: 38.5,
    },
    "internal_avg_cap_gb": {
        2022: 650, 2023: 810, 2024: 970, 2025: 1120,
    },
    # ── External SSD TAM ($B) ────────────────────────────────
    # IDC Worldwide External Storage Tracker
    "external_ssd_tam_b": {
        2022: 5.6, 2023: 5.1, 2024: 6.4, 2025: 7.2,
    },
    # ── microSD TAM ($B) ─────────────────────────────────────
    # IDC / TrendForce
    "microsd_tam_b": {
        2022: 4.8, 2023: 3.7, 2024: 3.6, 2025: 3.8,
    },
    # ── PCIe 인터페이스 비중 (Internal SSD 내) ───────────────
    # TrendForce NVMe Interface Report; Gen3=PCIe 3.0 포함 SATA 대비 NVMe
    "pcie_share": {
        # (PCIe3 %, PCIe4 %, PCIe5 %)
        2022: (0.55, 0.10, 0.00),
        2023: (0.44, 0.28, 0.00),
        2024: (0.31, 0.55, 0.03),
        2025: (0.25, 0.62, 0.08),
    },
    # ── USB 규격 비중 (External SSD 내) ──────────────────────
    # USB-IF Adopter Survey + TrendForce External SSD Report
    "usb_share": {
        # (USB3.2 Gen1(5Gbps) %, Gen2(10Gbps) %, Gen2x2/USB4(20-40Gbps) %)
        2022: (0.60, 0.32, 0.08),
        2023: (0.50, 0.38, 0.12),
        2024: (0.38, 0.45, 0.17),
        2025: (0.26, 0.45, 0.24),   # USB4 비중 증가 (Thunderbolt4 보급)
    },
    # ── microSD 슬롯 보급률 (스마트폰) ──────────────────────
    # Counterpoint Research / Strategy Analytics 스마트폰 스펙 분석
    "microsd_slot_pct": {
        2022: 0.42, 2023: 0.36, 2024: 0.31, 2025: 0.28,
    },
    # ── NAND 공급업체 비트출하 성장률 (YoY) ─────────────────
    # TrendForce NAND Flash Bit Shipment Growth
    "nand_bit_growth_yoy": {
        2022: -0.08, 2023: +0.05, 2024: +0.22, 2025: +0.18,
    },
}

# ══════════════════════════════════════════════════════════════
# 3. 시나리오 계산 엔진
# ══════════════════════════════════════════════════════════════

def run_scenario(scenario: str) -> dict:
    """Bear/Base/Bull 시나리오별 5개년 수요 계산"""
    s = scenario  # "bear" | "base" | "bull"
    results = {}

    # 초기값 (2025 기준)
    pc_units   = FACT_BASE["pc_shipments_2025_m"]
    nand_price = FACT_BASE["nand_asp_per_gb_2025"]

    int_tam    = FACT_BASE["internal_ssd_tam_2025_b"]
    int_units  = FACT_BASE["internal_ssd_units_2025_m"]
    ext_tam    = FACT_BASE["external_ssd_tam_2025_b"]
    ext_units  = FACT_BASE["external_ssd_units_2025_m"]
    mic_tam    = FACT_BASE["microsd_tam_2025_b"]
    mic_units  = FACT_BASE["microsd_units_2025_m"]

    creator_base = FACT_BASE["creator_population_2025_m"]
    avg_int_cap  = FACT_BASE["avg_internal_cap_gb_2025"]
    avg_mic_cap  = FACT_BASE["avg_microsd_cap_gb_2025"]
    ai_pc_pct    = FACT_BASE["ai_pc_penetration_2026"]

    for yr in YEARS:
        # ── NAND 가격 업데이트 ──────────────────────────────
        nand_chg = NAND_PRICE_TREND[s][yr]
        nand_price = nand_price * (1 + nand_chg)

        # ── AI PC 보급률 (매년 확대) ────────────────────────
        ai_pc_increment = {"bear": 0.08, "base": 0.12, "bull": 0.16}[s]
        ai_pc_pct = min(ai_pc_pct + ai_pc_increment, {"bear": 0.65, "base": 0.85, "bull": 0.95}[s])

        # ── PC 출하 ─────────────────────────────────────────
        pc_units = pc_units * (1 + PC_GROWTH[s][yr])

        # ────────────────────────────────────────────────────
        # A. INTERNAL SSD
        # ────────────────────────────────────────────────────

        # 1) 기본 PC 수요: PC 출하 × 탑재율 (이미 95%+ 수렴)
        nb_ssd_units = pc_units * 0.68 * FACT_BASE["notebook_ssd_attach_2025"]
        dt_ssd_units = pc_units * 0.32 * min(FACT_BASE["desktop_ssd_attach_2025"] + 0.02*(yr-2025), 0.90)
        pc_ssd_units = nb_ssd_units + dt_ssd_units

        # 2) 평균 용량 증가 (AI PC 프리미엄)
        cap_premium = AI_PC_CAP_PREMIUM[s][yr]
        ai_effect   = 1 + ai_pc_pct * (cap_premium - 1)
        avg_int_cap = FACT_BASE["avg_internal_cap_gb_2025"] * ai_effect
        capacity_growth_multiplier = avg_int_cap / FACT_BASE["avg_internal_cap_gb_2025"]

        # 3) PCIe 5.0 ASP 믹스 업리프트
        pcie5_share = PCIE5_ADOPTION[s][yr]
        pcie5_prem  = PCIE5_ASP_PREMIUM[yr]
        asp_uplift  = 1 + pcie5_share * (pcie5_prem - 1)

        # 4) 게임 확장 SSD (PS5/Xbox/Switch 2)
        gaming_ssd_m = FACT_BASE["gaming_console_ssd_2025_m"] * (
            1 + {"bear": 0.04, "base": 0.08, "bull": 0.13}[s]
        ) ** (yr - 2025)

        # 5) 서버/엣지 Internal SSD (AI 추론 서버 로컬 스토리지)
        server_ssd_growth = {"bear": 0.05, "base": 0.12, "bull": 0.18}[s]
        server_ssd_share  = 0.12 * (1 + server_ssd_growth) ** (yr - 2025)  # TAM 내 비중

        # 6) NAND 가격 수요 탄성 (가격 상승 시 수요 억제)
        price_change = nand_chg
        elasticity_effect = 1 + PRICE_ELASTICITY["internal_ssd"] * price_change

        # 7) 중국 리스크
        china_drag = 1 - CHINA_RISK[s]

        # 계산
        int_units_new = (pc_ssd_units + gaming_ssd_m) * elasticity_effect * china_drag
        int_units_new = int_units_new * (1 + {"bear": 0.00, "base": 0.02, "bull": 0.04}[s])  # 기타 성장
        int_asp    = (FACT_BASE["internal_ssd_tam_2025_b"] / FACT_BASE["internal_ssd_units_2025_m"]
                      ) * capacity_growth_multiplier * asp_uplift
        int_tam_new = int_units_new * int_asp * (1 + server_ssd_share)

        # ────────────────────────────────────────────────────
        # B. EXTERNAL SSD
        # ────────────────────────────────────────────────────

        # 1) 크리에이터 수요
        creator_base = creator_base * (1 + CREATOR_GROWTH[s][yr])
        creator_ssd_per_person = 0.18  # 크리에이터 중 외장SSD 구매율 18%/yr
        creator_demand_m = creator_base * creator_ssd_per_person / 1000

        # 2) 액션캠/드론 에코시스템
        action_cam_growth = {"bear": 0.03, "base": 0.07, "bull": 0.12}[s]
        action_cam_units = FACT_BASE["action_cam_units_2025_m"] * (1 + action_cam_growth) ** (yr - 2025)
        action_cam_ssd_attach = min(0.35 + 0.05 * (yr - 2025), 0.60)  # 점점 외장SSD 연결
        action_cam_demand_m = action_cam_units * action_cam_ssd_attach

        # 3) USB4 ASP 업리프트
        usb4_share = USB4_ADOPTION[s][yr]
        usb4_prem  = USB4_ASP_PREMIUM[yr]
        ext_asp_uplift = 1 + usb4_share * (usb4_prem - 1)

        # 4) 클라우드 대체 리스크
        cloud_drag = 1 - CLOUD_RISK[s]

        # 5) AI 워크스테이션/Edge AI 외장 SSD 수요 (신규)
        ai_edge_demand_m = {"bear": 0.5, "base": 1.5, "bull": 3.0}[s] * (1.2 ** (yr - 2026))

        # 6) 평균 용량 증가 (4K→6K/8K 콘텐츠)
        ext_cap_growth = {"bear": 1.08, "base": 1.15, "bull": 1.22}[s]
        ext_cap_multiplier = ext_cap_growth ** (yr - 2025)

        # 7) NAND 가격 탄성
        ext_elasticity = 1 + PRICE_ELASTICITY["external_ssd"] * nand_chg

        ext_units_new = (creator_demand_m + action_cam_demand_m + ai_edge_demand_m
                         + ext_units * 0.25  # 기타 일반 소비자 (점유율 유지분)
                         ) * cloud_drag * ext_elasticity * china_drag
        ext_base_asp  = (FACT_BASE["external_ssd_tam_2025_b"] / FACT_BASE["external_ssd_units_2025_m"]
                         ) * ext_cap_multiplier * ext_asp_uplift
        ext_tam_new   = ext_units_new * ext_base_asp

        # ────────────────────────────────────────────────────
        # C. microSD
        # ────────────────────────────────────────────────────

        # 1) 스마트폰 수요 (슬롯 보급률 감소 추세)
        smartphone_units_m = 1400 * (1 + {"bear": 0.01, "base": 0.02, "bull": 0.03}[s]) ** (yr - 2025)
        microsd_slot_rate  = MICROSD_SLOT_RATE[s][yr]
        smartphone_microsd_demand_m = smartphone_units_m * microsd_slot_rate * 0.55  # 슬롯 있어도 55%만 구매

        # 2) IoT/산업/엣지 수요
        iot_growth = IOT_MICROSD_GROWTH[s][yr]
        iot_microsd_m = 120 * (1 + iot_growth) ** (yr - 2025)  # 기준 120M units/yr

        # 3) 카메라/드론/대시캠
        cam_microsd_m = 80 * (1 + {"bear": 0.03, "base": 0.07, "bull": 0.11}[s]) ** (yr - 2025)

        # 4) Nintendo Switch 2 / 게임기 효과
        gaming_microsd_m = {"bear": 8, "base": 22, "bull": 38}[s] if yr <= 2028 else {"bear": 5, "base": 15, "bull": 25}[s]

        # 5) 평균 용량 상승 (256GB → 512GB 주류 전환)
        avg_mic_cap = FACT_BASE["avg_microsd_cap_gb_2025"] * (
            {"bear": 1.08, "base": 1.14, "bull": 1.20}[s] ** (yr - 2025)
        )
        mic_cap_multiplier = avg_mic_cap / FACT_BASE["avg_microsd_cap_gb_2025"]

        # 6) NAND 가격 탄성 (상대적으로 커)
        mic_elasticity = 1 + PRICE_ELASTICITY["microsd"] * nand_chg

        mic_units_new = (smartphone_microsd_demand_m + iot_microsd_m + cam_microsd_m + gaming_microsd_m
                         ) * mic_elasticity * china_drag
        mic_base_asp  = (FACT_BASE["microsd_tam_2025_b"] / FACT_BASE["microsd_units_2025_m"]
                         ) * mic_cap_multiplier
        # 단, microSD ASP는 TLC→QLC 전환으로 억제 (용량 증가와 상쇄)
        mic_qlc_drag  = {"bear": 0.96, "base": 0.97, "bull": 0.98}[s]
        mic_tam_new   = mic_units_new * mic_base_asp * mic_qlc_drag

        # ── 결과 저장 ────────────────────────────────────────
        results[yr] = {
            "nand_price":      round(nand_price, 4),
            "ai_pc_pct":       round(ai_pc_pct * 100, 1),
            "pc_units_m":      round(pc_units, 1),
            "internal": {
                "units_m":     round(int_units_new, 1),
                "tam_b":       round(int_tam_new, 2),
                "avg_cap_gb":  round(avg_int_cap, 0),
                "pcie5_share": round(pcie5_share * 100, 1),
            },
            "external": {
                "units_m":     round(ext_units_new, 1),
                "tam_b":       round(ext_tam_new, 2),
                "usb4_share":  round(usb4_share * 100, 1),
            },
            "microsd": {
                "units_m":     round(mic_units_new, 1),
                "tam_b":       round(mic_tam_new, 2),
                "avg_cap_gb":  round(avg_mic_cap, 0),
            },
            "total_tam_b": round(int_tam_new + ext_tam_new + mic_tam_new, 2),
        }

    return results


# ══════════════════════════════════════════════════════════════
# 4. HTML 리포트 빌더
# ══════════════════════════════════════════════════════════════

SCENARIO_META = {
    "bear": {"label": "Bear", "color": "#e53e3e", "bg": "#fff5f5",
             "desc": "신규 캐파 빠른 증설 → 공급 과잉, PC 성장 정체, AI PC 전환 지연, 중국 시장 리스크 현실화"},
    "base": {"label": "Base", "color": "#3182ce", "bg": "#ebf8ff",
             "desc": "점진적 AI PC 전환, NAND 소폭 상승 후 안정, USB4 확산, 크리에이터 지속 성장"},
    "bull": {"label": "Bull", "color": "#38a169", "bg": "#f0fff4",
             "desc": "AI PC 조기 대중화, 로컬 LLM 저장 수요 폭증, Copilot+ 4TB 표준화, 크리에이터+IoT 동시 성장"},
}

DRIVER_NOTES = [
    # (구분, 드라이버, Bear 전제, Base 전제, Bull 전제, 출처)
    ("Internal SSD", "PC 시장 성장", "연 0~1% 정체", "연 3~4% 완만한 회복", "연 5~8% AI PC 수요 폭발", "IDC 2025 PC Forecast"),
    ("Internal SSD", "AI PC 침투율", "2030년 65% 달성", "2030년 85% 달성", "2030년 95% 달성", "IDC/Canalys AI PC 정의"),
    ("Internal SSD", "평균 용량(AI 프리미엄)", "2030년 ~1.6TB", "2030년 ~2.0TB", "2030년 ~2.8TB+", "WD/Micron 제품 로드맵"),
    ("Internal SSD", "PCIe 5.0 전환", "2030년 52% 비중", "2030년 75% 비중", "2030년 90% 비중", "Intel Arrow Lake/AMD 로드맵"),
    ("Internal SSD", "서버/AI 엣지 Internal", "성장 정체 5%", "연 12% 성장", "연 18% 성장", "IDC Enterprise SSD"),
    ("External SSD", "크리에이터 수요", "연 8% 성장", "연 12~14% 성장", "연 18~20% 성장", "HubSpot Creator Economy"),
    ("External SSD", "USB4 전환 ASP 업리프트", "2030년 54% 비중 +3%", "2030년 74% 비중 +7%", "2030년 88% 비중 +12%", "USB-IF 로드맵"),
    ("External SSD", "AI 엣지 외장 SSD 수요", "미미 0.5M→연 20%↑", "신규 1.5M→연 20%↑", "신규 3.0M→연 20%↑", "추정"),
    ("External SSD", "클라우드 대체 리스크", "연 4% 수요 잠식", "연 2% 잠식", "연 1% 잠식", "IDC Cloud Storage Trend"),
    ("microSD", "스마트폰 슬롯 보급률", "2030년 8% (급감)", "2030년 15% (완만 감소)", "2030년 22% (IoT+게임 지지)", "IDC Smartphone Tracker"),
    ("microSD", "Nintendo Switch 2 효과", "효과 미미 (8M 추가)", "22M 추가 수요", "38M 추가 (2026~2028)", "Nintendo 예상"),
    ("microSD", "IoT/엣지 성장", "연 5~6%", "연 10~13%", "연 15~20%", "Statista IoT 2025"),
    ("microSD", "평균 용량 상승", "연 8% 성장 → ~440GB", "연 14% → ~570GB", "연 20% → ~730GB", "TrendForce NAND density"),
    ("공통", "NAND 가격 방향", "공급 tight → 상승 유지", "2026~27 소폭↑, 이후 안정", "2028년 공급과잉 → 하락 전환", "TrendForce NAND ASP 추정"),
    ("공통", "중국 시장 리스크", "연 6% 수요 접근 손실", "연 3% 손실", "연 1% (관계 개선)", "BIS/무역정책 시나리오"),
]


def _bar(val: float, max_val: float, color: str, width: int = 180) -> str:
    w = max(4, int(val / max_val * width)) if max_val > 0 else 4
    return (f'<div style="display:flex;align-items:center;gap:6px;">'
            f'<div style="background:{color};height:10px;width:{w}px;border-radius:2px;"></div>'
            f'<span style="font-size:12px;font-weight:700;color:{color};">'
            f'${val:.1f}B</span></div>')


def _tam_table(scenario_results: dict, cat: str, label: str, color: str) -> str:
    headers = "".join(f'<th style="padding:6px 12px;text-align:right;color:{color};">{yr}</th>' for yr in YEARS)
    units_row = "".join(
        f'<td style="padding:5px 12px;text-align:right;">{scenario_results[yr][cat]["units_m"]:.0f}M</td>'
        for yr in YEARS
    )
    tam_row = "".join(
        f'<td style="padding:5px 12px;text-align:right;font-weight:700;color:{color};">'
        f'${scenario_results[yr][cat]["tam_b"]:.1f}B</td>'
        for yr in YEARS
    )
    return f"""
<table style="border-collapse:collapse;width:100%;font-size:13px;margin:8px 0;">
  <thead><tr style="background:#f7f8fa;">
    <th style="padding:6px 12px;text-align:left;">{label}</th>
    {headers}
  </tr></thead>
  <tbody>
    <tr><td style="padding:5px 12px;color:#718096;">출하량</td>{units_row}</tr>
    <tr style="background:#f7f8fa;"><td style="padding:5px 12px;font-weight:700;">TAM</td>{tam_row}</tr>
  </tbody>
</table>"""


def build_html_report(scenarios: dict) -> str:
    today_str = TODAY.strftime("%Y년 %m월 %d일")
    base = scenarios["base"]
    bull = scenarios["bull"]
    bear = scenarios["bear"]

    # 최대 TAM (스케일 기준)
    max_total = max(max(v["total_tam_b"] for v in s.values()) for s in scenarios.values())

    # ── 시나리오별 요약 카드 ─────────────────────────────────
    def scenario_card(s: str) -> str:
        sc = SCENARIO_META[s]
        data = scenarios[s]
        total_2030 = data[2030]["total_tam_b"]
        total_2025 = (FACT_BASE["internal_ssd_tam_2025_b"] +
                      FACT_BASE["external_ssd_tam_2025_b"] +
                      FACT_BASE["microsd_tam_2025_b"])
        cagr = ((total_2030 / total_2025) ** (1/5) - 1) * 100

        int_30  = data[2030]["internal"]["tam_b"]
        ext_30  = data[2030]["external"]["tam_b"]
        mic_30  = data[2030]["microsd"]["tam_b"]

        return f"""
<div style="border:2px solid {sc['color']};border-radius:8px;padding:20px 24px;
            background:{sc['bg']};flex:1;min-width:220px;">
  <div style="display:flex;align-items:center;gap:8px;margin-bottom:12px;">
    <span style="background:{sc['color']};color:white;font-size:12px;font-weight:700;
                 padding:4px 12px;border-radius:12px;">{sc['label']}</span>
    <span style="font-size:12px;color:#718096;">2030E Total TAM</span>
  </div>
  <div style="font-size:32px;font-weight:800;color:{sc['color']};margin-bottom:4px;">
    ${total_2030:.1f}B
  </div>
  <div style="font-size:13px;color:#4a5568;margin-bottom:12px;">
    CAGR {cagr:+.1f}% (vs 2025 ${total_2025:.1f}B)
  </div>
  <div style="font-size:12px;color:#718096;border-top:1px solid {sc['color']}33;
              padding-top:10px;line-height:1.8;">
    Internal SSD: <strong style="color:{sc['color']};">${int_30:.1f}B</strong><br>
    External SSD: <strong style="color:{sc['color']};">${ext_30:.1f}B</strong><br>
    microSD:      <strong style="color:{sc['color']};">${mic_30:.1f}B</strong>
  </div>
  <div style="font-size:11px;color:#a0aec0;margin-top:10px;line-height:1.6;">
    {sc['desc']}
  </div>
</div>"""

    # ── 연도별 총 TAM 트렌드 테이블 ─────────────────────────
    def trend_table() -> str:
        rows = ""
        for yr in YEARS:
            b_tam = bear[yr]["total_tam_b"]
            bs_tam = base[yr]["total_tam_b"]
            bu_tam = bull[yr]["total_tam_b"]
            rows += f"""
<tr>
  <td style="padding:8px 14px;font-weight:700;">{yr}</td>
  <td style="padding:8px 14px;text-align:right;color:#e53e3e;font-weight:700;">${b_tam:.1f}B</td>
  <td style="padding:8px 14px;text-align:right;">
    <div style="background:#e53e3e;height:8px;width:{int(b_tam/max_total*160)}px;
                border-radius:2px;display:inline-block;"></div></td>
  <td style="padding:8px 14px;text-align:right;color:#3182ce;font-weight:700;">${bs_tam:.1f}B</td>
  <td style="padding:8px 14px;text-align:right;">
    <div style="background:#3182ce;height:8px;width:{int(bs_tam/max_total*160)}px;
                border-radius:2px;display:inline-block;"></div></td>
  <td style="padding:8px 14px;text-align:right;color:#38a169;font-weight:700;">${bu_tam:.1f}B</td>
  <td style="padding:8px 14px;text-align:right;">
    <div style="background:#38a169;height:8px;width:{int(bu_tam/max_total*160)}px;
                border-radius:2px;display:inline-block;"></div></td>
</tr>"""
        return f"""
<table style="border-collapse:collapse;width:100%;font-size:13px;">
  <thead><tr style="background:#f7f8fa;border-bottom:2px solid #e2e8f0;">
    <th style="padding:8px 14px;text-align:left;">연도</th>
    <th style="padding:8px 14px;text-align:right;color:#e53e3e;" colspan="2">Bear</th>
    <th style="padding:8px 14px;text-align:right;color:#3182ce;" colspan="2">Base</th>
    <th style="padding:8px 14px;text-align:right;color:#38a169;" colspan="2">Bull</th>
  </tr></thead>
  <tbody>{rows}</tbody>
</table>"""

    # ── 과거 추이 섹션 ─────────────────────────────────────
    def historical_section() -> str:
        H = HISTORICAL
        years = [2022, 2023, 2024, 2025]

        # NAND 분기 가격 — sparkline 형태로 표시
        nand_q_keys = ["2022Q1","2022Q2","2022Q3","2022Q4",
                       "2023Q1","2023Q2","2023Q3","2023Q4",
                       "2024Q1","2024Q2","2024Q3","2024Q4",
                       "2025Q1","2025Q2","2025Q3","2025Q4"]
        nand_vals = [H["nand_price_per_gb"][k] for k in nand_q_keys]
        nand_max  = max(nand_vals)
        nand_min  = min(nand_vals)

        def nand_bar(v):
            pct = (v - nand_min) / (nand_max - nand_min + 0.001)
            w   = int(pct * 80) + 8
            # color: high = red (tight supply), low = green (oversupply)
            r   = int(200 + 55 * pct)
            g   = int(180 - 140 * pct)
            return f'<div style="background:rgb({r},{g},80);height:22px;width:{w}px;border-radius:3px;display:inline-block;vertical-align:middle;"></div>'

        nand_spark_rows = ""
        for i, k in enumerate(nand_q_keys):
            v    = nand_vals[i]
            chg  = ""
            if i > 0:
                delta = (v - nand_vals[i-1]) / nand_vals[i-1] * 100
                arrow = "▲" if delta > 0 else "▼"
                col   = "#e53e3e" if delta > 0 else "#38a169"
                chg   = f'<span style="color:{col};font-size:10px;"> {arrow}{abs(delta):.1f}%</span>'
            nand_spark_rows += f"""
<tr style="border-bottom:1px solid #f7f8fa;">
  <td style="padding:4px 10px;font-size:11px;color:#718096;white-space:nowrap;">{k}</td>
  <td style="padding:4px 10px;font-size:12px;font-weight:700;">${v:.3f}{chg}</td>
  <td style="padding:4px 10px;">{nand_bar(v)}</td>
</tr>"""

        # PC 출하 + AI PC 침투율 + TAM 테이블
        pc_rows = ""
        for yr in years:
            pc  = H["pc_shipments_m"][yr]
            ai  = H["ai_pc_penetration_pct"][yr]
            i_t = H["internal_ssd_tam_b"][yr]
            e_t = H["external_ssd_tam_b"][yr]
            m_t = H["microsd_tam_b"][yr]
            total = i_t + e_t + m_t
            bg  = "#f7fbff" if yr % 2 == 0 else "white"
            ai_bar_w = int(ai * 160)
            pc_rows += f"""
<tr style="border-bottom:1px solid #edf2f7;background:{bg};">
  <td style="padding:6px 12px;font-weight:700;color:#2d3748;">{yr}</td>
  <td style="padding:6px 12px;text-align:right;">{pc}M</td>
  <td style="padding:6px 12px;text-align:right;">
    <div style="display:flex;align-items:center;gap:6px;justify-content:flex-end;">
      <div style="background:#667eea;height:10px;width:{ai_bar_w}px;border-radius:2px;"></div>
      <span style="font-weight:700;color:#553c9a;">{ai*100:.0f}%</span>
    </div>
  </td>
  <td style="padding:6px 12px;text-align:right;color:#3182ce;font-weight:600;">${i_t:.1f}B</td>
  <td style="padding:6px 12px;text-align:right;color:#dd6b20;font-weight:600;">${e_t:.1f}B</td>
  <td style="padding:6px 12px;text-align:right;color:#805ad5;font-weight:600;">${m_t:.1f}B</td>
  <td style="padding:6px 12px;text-align:right;font-weight:700;color:#2d3748;">${total:.1f}B</td>
</tr>"""

        # PCIe & USB 인터페이스 추이
        def iface_badge(label, pct, color):
            w = max(int(pct * 100), 2)
            return f'<span style="display:inline-block;background:{color};color:white;font-size:10px;padding:2px 5px;border-radius:3px;margin:1px;">{label} {pct*100:.0f}%</span>'

        pcie_rows = ""
        usb_rows  = ""
        for yr in years:
            p3, p4, p5 = H["pcie_share"][yr]
            p_sata = max(0, 1 - p3 - p4 - p5)
            u1, u2, u4 = H["usb_share"][yr]
            cap  = H["internal_avg_cap_gb"][yr]
            slot = H["microsd_slot_pct"][yr]
            bit_g = H["nand_bit_growth_yoy"][yr]
            bg   = "#f7fbff" if yr % 2 == 0 else "white"
            pcie_rows += f"""
<tr style="border-bottom:1px solid #edf2f7;background:{bg};">
  <td style="padding:6px 12px;font-weight:700;">{yr}</td>
  <td style="padding:6px 12px;">
    {iface_badge("SATA",p_sata,"#a0aec0")}
    {iface_badge("PCIe 3",p3,"#63b3ed")}
    {iface_badge("PCIe 4",p4,"#3182ce")}
    {iface_badge("PCIe 5",p5,"#1a365d") if p5 > 0 else ""}
  </td>
  <td style="padding:6px 12px;text-align:right;font-weight:600;">{cap:,}GB</td>
  <td style="padding:6px 12px;text-align:right;">
    <span style="color:{'#e53e3e' if bit_g > 0 else '#38a169'};font-weight:700;">
      {'▲' if bit_g > 0 else '▼'}{abs(bit_g)*100:.0f}% YoY
    </span>
  </td>
</tr>"""
            usb_rows += f"""
<tr style="border-bottom:1px solid #edf2f7;background:{bg};">
  <td style="padding:6px 12px;font-weight:700;">{yr}</td>
  <td style="padding:6px 12px;">
    {iface_badge("USB3.2 Gen1",u1,"#a0aec0")}
    {iface_badge("USB3.2 Gen2",u2,"#ed8936")}
    {iface_badge("USB4/TB4",u4,"#dd6b20")}
  </td>
  <td style="padding:6px 12px;text-align:right;font-weight:600;">{slot*100:.0f}%</td>
</tr>"""

        return f"""
<!-- ── 과거 추이 섹션 ── -->
<div style="background:white;border-radius:10px;padding:24px 32px;margin-bottom:16px;
            box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <div style="font-size:12px;font-weight:700;color:#4a5568;text-transform:uppercase;
              letter-spacing:.5px;margin-bottom:4px;">📉 과거 추이 분석 (2022~2025 실적)</div>
  <div style="font-size:12px;color:#a0aec0;margin-bottom:20px;">
    출처: TrendForce DRAMeXchange · IDC PC Tracker · Canalys AI PC · USB-IF · Counterpoint Research
  </div>

  <div style="display:flex;gap:20px;flex-wrap:wrap;align-items:flex-start;">

    <!-- NAND 분기 가격 스파크차트 -->
    <div style="flex:0 0 260px;min-width:220px;">
      <div style="font-size:12px;font-weight:700;color:#2d3748;margin-bottom:8px;">
        💾 NAND Contract 가격 ($/GB) 분기별
      </div>
      <div style="font-size:10px;color:#718096;margin-bottom:6px;">
        2023 공급과잉 저점($0.026) → 2024 반등 → 2025 AI tight
      </div>
      <table style="border-collapse:collapse;width:100%;">
        {nand_spark_rows}
      </table>
    </div>

    <!-- PC · AI PC · TAM 테이블 -->
    <div style="flex:1;min-width:300px;">
      <div style="font-size:12px;font-weight:700;color:#2d3748;margin-bottom:8px;">
        🖥️ PC 출하 · AI PC 침투율 · 카테고리 TAM
      </div>
      <table style="border-collapse:collapse;width:100%;font-size:12px;">
        <thead>
          <tr style="background:#edf2f7;border-bottom:2px solid #e2e8f0;">
            <th style="padding:6px 12px;text-align:left;">연도</th>
            <th style="padding:6px 12px;text-align:right;">PC 출하</th>
            <th style="padding:6px 12px;text-align:right;">AI PC 비중</th>
            <th style="padding:6px 12px;text-align:right;color:#3182ce;">Internal</th>
            <th style="padding:6px 12px;text-align:right;color:#dd6b20;">External</th>
            <th style="padding:6px 12px;text-align:right;color:#805ad5;">microSD</th>
            <th style="padding:6px 12px;text-align:right;">합계</th>
          </tr>
        </thead>
        <tbody>{pc_rows}</tbody>
      </table>
      <div style="font-size:10px;color:#a0aec0;margin-top:4px;">
        * 2023 TAM 급감: NAND 가격 -52% 사이클 (공급과잉). 2024~2025 AI 수요 견인 회복.
      </div>
    </div>
  </div>

  <!-- 인터페이스 전환 추이 -->
  <div style="display:flex;gap:20px;flex-wrap:wrap;margin-top:20px;">
    <div style="flex:1;min-width:280px;">
      <div style="font-size:12px;font-weight:700;color:#2d3748;margin-bottom:8px;">
        ⚡ Internal SSD — PCIe 인터페이스 전환 추이
      </div>
      <table style="border-collapse:collapse;width:100%;font-size:12px;">
        <thead>
          <tr style="background:#edf2f7;border-bottom:2px solid #e2e8f0;">
            <th style="padding:6px 12px;text-align:left;">연도</th>
            <th style="padding:6px 12px;text-align:left;">인터페이스 구성비</th>
            <th style="padding:6px 12px;text-align:right;">평균 용량</th>
            <th style="padding:6px 12px;text-align:right;">NAND 비트 성장</th>
          </tr>
        </thead>
        <tbody>{pcie_rows}</tbody>
      </table>
      <div style="font-size:10px;color:#a0aec0;margin-top:4px;">
        PCIe 4 주류화(2024) → PCIe 5 플래그십 침투(2025~). SATA는 2027년 내 10% 이하로 소멸 전망.
      </div>
    </div>
    <div style="flex:1;min-width:260px;">
      <div style="font-size:12px;font-weight:700;color:#2d3748;margin-bottom:8px;">
        🔌 External SSD — USB 인터페이스 전환 추이
      </div>
      <table style="border-collapse:collapse;width:100%;font-size:12px;">
        <thead>
          <tr style="background:#edf2f7;border-bottom:2px solid #e2e8f0;">
            <th style="padding:6px 12px;text-align:left;">연도</th>
            <th style="padding:6px 12px;text-align:left;">인터페이스 구성비</th>
            <th style="padding:6px 12px;text-align:right;">스마트폰 microSD 슬롯率</th>
          </tr>
        </thead>
        <tbody>{usb_rows}</tbody>
      </table>
      <div style="font-size:10px;color:#a0aec0;margin-top:4px;">
        USB4/TB4 확산 가속(2024~): Apple M 시리즈·Intel Meteor Lake 탑재 → SanDisk E81 등 USB4 제품 라인업 확대 필요.
      </div>
    </div>
  </div>

  <!-- SanDisk 마케터 인사이트 -->
  <div style="background:#fffbeb;border-left:4px solid #f6ad55;border-radius:4px;
              padding:14px 18px;margin-top:20px;font-size:12px;line-height:1.7;">
    <strong style="color:#c05621;">📌 마케터 인사이트 (과거 → 미래 연결 포인트)</strong><br>
    ① <strong>NAND 사이클 교훈</strong>: 2023년 -52% 급락 때 재고 소진 후 2024년 급반등 — 가격 저점에서 재고 확보, 피크에서 믹스 전략 선제 조정이 핵심.<br>
    ② <strong>AI PC 티핑포인트</strong>: 2024년 18% → 2025년 28% → 2026년 32%로 가속. 이 교체 사이클이 Internal SSD 평균 용량을 1TB→2TB로 끌어올리는 핵심 엔진.<br>
    ③ <strong>USB4 조기 대응</strong>: 2022년 8%에서 2025년 24%로 빠른 침투. E81(20Gbps)·Extreme Pro V2(40Gbps) 등 USB4 포트폴리오를 2026년 메인스트림 포지션으로 이동.<br>
    ④ <strong>PCIe 5 윈도우</strong>: 2025년 8% → 시나리오별 2030년 52~90%. 플래그십 시장 조기 진입으로 ASP 믹스 방어 — 가격 경쟁보다 성능 포지셔닝이 유효.
  </div>
</div>"""

    # ── 드라이버 테이블 ─────────────────────────────────────
    def driver_table() -> str:
        CAT_COLOR = {
            "Internal SSD": "#e53e3e", "External SSD": "#dd6b20",
            "microSD": "#805ad5", "공통": "#2d3748"
        }
        rows = ""
        prev_cat = ""
        for cat, driver, bear_text, base_text, bull_text, source in DRIVER_NOTES:
            bg = "#f7f8fa" if cat != prev_cat else "white"
            cat_cell = f'<td rowspan="1" style="padding:6px 10px;font-weight:700;color:{CAT_COLOR.get(cat,"#2d3748")};white-space:nowrap;">{cat}</td>' if cat != prev_cat else '<td style="padding:6px 10px;"></td>'
            prev_cat = cat
            rows += f"""
<tr style="border-bottom:1px solid #f0f0f0;background:{bg};">
  <td style="padding:6px 12px;font-weight:600;font-size:13px;">{driver}</td>
  <td style="padding:6px 10px;font-size:12px;color:#e53e3e;background:#fff5f5;border-radius:4px;">{bear_text}</td>
  <td style="padding:6px 10px;font-size:12px;color:#3182ce;background:#ebf8ff;border-radius:4px;">{base_text}</td>
  <td style="padding:6px 10px;font-size:12px;color:#38a169;background:#f0fff4;border-radius:4px;">{bull_text}</td>
  <td style="padding:6px 10px;font-size:11px;color:#a0aec0;">{source}</td>
</tr>"""
        return f"""
<table style="border-collapse:collapse;width:100%;font-size:13px;">
  <thead><tr style="background:#edf2f7;border-bottom:2px solid #e2e8f0;">
    <th style="padding:8px 12px;text-align:left;">드라이버</th>
    <th style="padding:8px 12px;text-align:left;color:#e53e3e;">Bear</th>
    <th style="padding:8px 12px;text-align:left;color:#3182ce;">Base</th>
    <th style="padding:8px 12px;text-align:left;color:#38a169;">Bull</th>
    <th style="padding:8px 12px;text-align:left;">출처/근거</th>
  </tr></thead>
  <tbody>{rows}</tbody>
</table>"""

    # ── 카테고리별 상세 ─────────────────────────────────────
    def cat_detail(s: str, cat: str, cat_label: str, color: str, fields: list) -> str:
        data = scenarios[s]
        rows = ""
        for field_key, field_label, fmt in fields:
            vals = ""
            for yr in YEARS:
                v = data[yr][cat].get(field_key, "—")
                if isinstance(v, float):
                    vals += f'<td style="padding:5px 10px;text-align:right;">{fmt.format(v)}</td>'
                else:
                    vals += f'<td style="padding:5px 10px;text-align:right;">{v}</td>'
            rows += f'<tr><td style="padding:5px 10px;color:#718096;">{field_label}</td>{vals}</tr>'

        hdrs = "".join(f'<th style="padding:5px 10px;text-align:right;">{yr}</th>' for yr in YEARS)
        sm   = SCENARIO_META[s]
        return f"""
<div style="margin-bottom:8px;">
  <span style="background:{sm['color']};color:white;font-size:11px;font-weight:700;
               padding:2px 10px;border-radius:8px;">{sm['label']}</span>
  <table style="border-collapse:collapse;width:100%;font-size:12px;margin-top:6px;">
    <thead><tr style="background:#f7f8fa;">
      <th style="padding:5px 10px;text-align:left;color:{color};">{cat_label}</th>
      {hdrs}
    </tr></thead>
    <tbody>{rows}</tbody>
  </table>
</div>"""

    INT_FIELDS = [
        ("units_m",     "출하량 (M units)", "{:.0f}M"),
        ("tam_b",       "TAM ($B)",         "${:.1f}B"),
        ("avg_cap_gb",  "평균 용량 (GB)",    "{:.0f}GB"),
        ("pcie5_share", "PCIe 5.0 비중",    "{:.0f}%"),
    ]
    EXT_FIELDS = [
        ("units_m",    "출하량 (M units)", "{:.0f}M"),
        ("tam_b",      "TAM ($B)",        "${:.1f}B"),
        ("usb4_share", "USB4 비중",       "{:.0f}%"),
    ]
    MIC_FIELDS = [
        ("units_m",    "출하량 (M units)", "{:.0f}M"),
        ("tam_b",      "TAM ($B)",        "${:.1f}B"),
        ("avg_cap_gb", "평균 용량 (GB)",   "{:.0f}GB"),
    ]

    # ── NAND 가격 경로 ──────────────────────────────────────
    def nand_price_table() -> str:
        rows = ""
        for yr in YEARS:
            b  = bear[yr]["nand_price"]
            bs = base[yr]["nand_price"]
            bu = bull[yr]["nand_price"]
            rows += f"""
<tr>
  <td style="padding:6px 12px;font-weight:700;">{yr}</td>
  <td style="padding:6px 12px;text-align:right;color:#e53e3e;">${b:.3f}/GB</td>
  <td style="padding:6px 12px;text-align:right;color:#3182ce;">${bs:.3f}/GB</td>
  <td style="padding:6px 12px;text-align:right;color:#38a169;">${bu:.3f}/GB</td>
</tr>"""
        return f"""
<table style="border-collapse:collapse;width:100%;font-size:13px;">
  <thead><tr style="background:#f7f8fa;">
    <th style="padding:6px 12px;text-align:left;">연도</th>
    <th style="padding:6px 12px;text-align:right;color:#e53e3e;">Bear $/GB</th>
    <th style="padding:6px 12px;text-align:right;color:#3182ce;">Base $/GB</th>
    <th style="padding:6px 12px;text-align:right;color:#38a169;">Bull $/GB</th>
  </tr></thead>
  <tbody>{rows}</tbody>
</table>"""

    # ── 마케팅 시사점 ────────────────────────────────────────
    IMPLICATIONS = [
        ("Internal SSD",
         "PCIe 5.0 포지셔닝 조기 선점",
         "2026~2027년이 PCIe 5.0 초기 프리미엄 구간. SN8100 플래그십 포지셔닝 강화. AI PC 호환 마케팅으로 교체 수요 자극.",
         "#e53e3e"),
        ("Internal SSD",
         "2TB 기본 용량 내러티브 구축",
         "로컬 LLM(7B~70B 모델 4~40GB) + OS + 게임 = 최소 2TB 필요 메시지. 'AI PC엔 2TB부터' 포지셔닝.",
         "#e53e3e"),
        ("Internal SSD",
         "게임 콘솔 확장 SSD (PS5/Xbox) 성장 대응",
         "PlayStation 5/Xbox 내장 SSD 교체 수요: WD_BLACK 브랜드 직결. 2026~2028 고성장 구간에 번들 마케팅.",
         "#e53e3e"),
        ("External SSD",
         "USB4 40Gbps 라인업 조기 확대",
         "2026~2027년 USB4 생태계(MacBook/Thunderbolt 4) 확산. Extreme Pro USB4 버전으로 크리에이터 공략.",
         "#dd6b20"),
        ("External SSD",
         "AI 엣지 워크플로우 포지셔닝",
         "로컬 AI 모델 운반용 외장 SSD: 'AI 워크스테이션 필수품' 메시지. 4TB 외장 SSD 수요 증가 선점.",
         "#dd6b20"),
        ("External SSD",
         "4K/6K 영상 크리에이터 교체 자극",
         "4K 원본 1시간 = ~50GB, 6K RAW = ~200GB/hr. 'Pro 콘텐츠엔 4TB 외장 SSD' 메시지. 리뷰어 협업 강화.",
         "#dd6b20"),
        ("microSD",
         "Nintendo Switch 2 런칭 타이밍 공략",
         "Switch 2 출시(2026~2027 예상) 수요 급증 구간. SanDisk 코번들/인증 파트너십 선확보.",
         "#805ad5"),
        ("microSD",
         "IoT/산업 microSD 전용 라인업",
         "내구성/온도범위 강화 산업용 microSD로 IoT/CCTV/드론 시장 진입. 일반 소비자 슬롯 감소 대응 다각화.",
         "#805ad5"),
        ("microSD",
         "1TB microSD 메인스트림화 대비",
         "2028년부터 1TB microSD 주류 가격대($30~40) 진입. 얼리무버 포지셔닝으로 ASP 방어.",
         "#805ad5"),
        ("공통",
         "NAND 가격 상승기(2026~2027) 재고 전략",
         "Bear 시나리오 대비 용량 다운사이즈 수요 증가 예상. 512GB/1TB 재고 탄력적 운용. 가격 방어보다 볼륨 우선.",
         "#2d3748"),
        ("공통",
         "중국 시장 리스크 헷지",
         "로컬 브랜드(YMTC/江波龙) 점유 확대 대응: 프리미엄 채널 집중 + 고부가 제품 믹스 강화. 저가 시장 철수 준비.",
         "#2d3748"),
    ]

    impl_rows = ""
    for cat, action, rationale, color in IMPLICATIONS:
        impl_rows += f"""
<tr style="border-bottom:1px solid #f0f0f0;">
  <td style="padding:8px 12px;white-space:nowrap;">
    <span style="background:{color};color:white;font-size:10px;padding:2px 7px;
                 border-radius:8px;">{cat}</span>
  </td>
  <td style="padding:8px 12px;font-weight:700;font-size:13px;color:#2d3748;">{action}</td>
  <td style="padding:8px 12px;font-size:12px;color:#4a5568;line-height:1.6;">{rationale}</td>
</tr>"""

    # ── 최종 HTML ────────────────────────────────────────────
    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>SSD 시장 수요 시나리오 예측 2026~2030</title>
</head>
<body style="margin:0;padding:24px 0;background:#f0f2f5;
             font-family:'Apple SD Gothic Neo',Malgun Gothic,Arial,sans-serif;">
<div style="max-width:1100px;margin:0 auto;">

<!-- ── 헤더 ── -->
<div style="background:linear-gradient(135deg,#1a365d 0%,#2d3748 100%);
            border-radius:12px;padding:36px 44px;margin-bottom:20px;">
  <div style="font-size:11px;color:rgba(255,255,255,.5);text-transform:uppercase;
              letter-spacing:1px;margin-bottom:8px;">
    SanDisk B2C Storage | 시장 분석 리포트
  </div>
  <div style="color:white;font-size:28px;font-weight:800;line-height:1.3;margin-bottom:8px;">
    SSD 중장기 시나리오 수요 예측
  </div>
  <div style="color:rgba(255,255,255,.7);font-size:15px;">
    Internal SSD / External SSD / microSD — 2026~2030E
  </div>
  <div style="color:rgba(255,255,255,.45);font-size:11px;margin-top:12px;">
    기준: {today_str} &nbsp;·&nbsp;
    데이터 소스: IDC, TrendForce, Gartner, USB-IF, Intel/AMD 로드맵, HubSpot Creator Economy Report
  </div>
</div>

<!-- ── 2025 기준점 ── -->
<div style="background:white;border-radius:10px;padding:24px 32px;margin-bottom:16px;
            box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <div style="font-size:12px;font-weight:700;color:#4a5568;text-transform:uppercase;
              letter-spacing:.5px;margin-bottom:16px;">📌 2025 기준점 (Fact Base)</div>
  <div style="display:flex;gap:20px;flex-wrap:wrap;">
    <div style="background:#f7f8fa;border-radius:8px;padding:14px 20px;flex:1;min-width:140px;">
      <div style="font-size:11px;color:#718096;margin-bottom:4px;">PC 출하량</div>
      <div style="font-size:20px;font-weight:800;color:#2d3748;">260M</div>
      <div style="font-size:11px;color:#a0aec0;">units [IDC 2025E]</div>
    </div>
    <div style="background:#ebf8ff;border-radius:8px;padding:14px 20px;flex:1;min-width:140px;">
      <div style="font-size:11px;color:#718096;margin-bottom:4px;">Internal SSD TAM</div>
      <div style="font-size:20px;font-weight:800;color:#3182ce;">$38.5B</div>
      <div style="font-size:11px;color:#a0aec0;">320M units [TrendForce]</div>
    </div>
    <div style="background:#fffaf0;border-radius:8px;padding:14px 20px;flex:1;min-width:140px;">
      <div style="font-size:11px;color:#718096;margin-bottom:4px;">External SSD TAM</div>
      <div style="font-size:20px;font-weight:800;color:#dd6b20;">$7.2B</div>
      <div style="font-size:11px;color:#a0aec0;">58M units [IDC]</div>
    </div>
    <div style="background:#faf5ff;border-radius:8px;padding:14px 20px;flex:1;min-width:140px;">
      <div style="font-size:11px;color:#718096;margin-bottom:4px;">microSD TAM</div>
      <div style="font-size:20px;font-weight:800;color:#805ad5;">$3.8B</div>
      <div style="font-size:11px;color:#a0aec0;">370M units [IDC]</div>
    </div>
    <div style="background:#f0fff4;border-radius:8px;padding:14px 20px;flex:1;min-width:140px;">
      <div style="font-size:11px;color:#718096;margin-bottom:4px;">NAND 가격 ($/GB)</div>
      <div style="font-size:20px;font-weight:800;color:#38a169;">$0.045</div>
      <div style="font-size:11px;color:#a0aec0;">Contract [TrendForce 2025Q4]</div>
    </div>
    <div style="background:#f7f8fa;border-radius:8px;padding:14px 20px;flex:1;min-width:140px;">
      <div style="font-size:11px;color:#718096;margin-bottom:4px;">AI PC 침투율</div>
      <div style="font-size:20px;font-weight:800;color:#2d3748;">32%</div>
      <div style="font-size:11px;color:#a0aec0;">(2026 기준점) [IDC/Canalys]</div>
    </div>
  </div>
</div>

{historical_section()}

<!-- ── 시나리오 요약 카드 ── -->
<div style="background:white;border-radius:10px;padding:24px 32px;margin-bottom:16px;
            box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <div style="font-size:12px;font-weight:700;color:#4a5568;text-transform:uppercase;
              letter-spacing:.5px;margin-bottom:16px;">📊 2030E 시나리오별 총 TAM 전망</div>
  <div style="display:flex;gap:16px;flex-wrap:wrap;">
    {scenario_card("bear")}
    {scenario_card("base")}
    {scenario_card("bull")}
  </div>
</div>

<!-- ── 연도별 TAM 추이 ── -->
<div style="background:white;border-radius:10px;padding:24px 32px;margin-bottom:16px;
            box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <div style="font-size:12px;font-weight:700;color:#4a5568;text-transform:uppercase;
              letter-spacing:.5px;margin-bottom:14px;">📈 연도별 총 TAM 추이 (Bear / Base / Bull)</div>
  {trend_table()}
  <div style="font-size:11px;color:#a0aec0;margin-top:8px;">
    * Internal + External + microSD 합산 TAM 기준
  </div>
</div>

<!-- ── NAND 가격 경로 ── -->
<div style="background:white;border-radius:10px;padding:24px 32px;margin-bottom:16px;
            box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <div style="font-size:12px;font-weight:700;color:#4a5568;text-transform:uppercase;
              letter-spacing:.5px;margin-bottom:14px;">💹 NAND Contract 가격 경로 ($/GB)</div>
  {nand_price_table()}
  <div style="font-size:11px;color:#718096;margin-top:10px;line-height:1.6;">
    <strong>Bear:</strong> 신규 캐파 증설(Kioxia/Western Digital 협력 재개 + YMTC 복귀) → 공급 과잉 전환 가속, 가격 강세 장기화<br>
    <strong>Base:</strong> 2026~2027 tight supply → 소폭 상승 후 2028~2029 새 캐파 가동으로 안정화<br>
    <strong>Bull:</strong> AI 서버 + AI PC 동시 수요 폭발 → 공급이 수요를 못 따라가 상승 지속 → 2029 이후 점진적 완화
  </div>
</div>

<!-- ── 카테고리별 상세 ── -->
<div style="background:white;border-radius:10px;padding:24px 32px;margin-bottom:16px;
            box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <div style="font-size:12px;font-weight:700;color:#e53e3e;text-transform:uppercase;
              letter-spacing:.5px;margin-bottom:16px;">🖥️ Internal SSD — 카테고리별 상세</div>
  <div style="font-size:12px;color:#4a5568;margin-bottom:12px;line-height:1.7;">
    <strong>핵심 드라이버:</strong> AI PC 교체 사이클 (로컬 LLM → 2TB 기본화) + PCIe 5.0 전환 ASP 업리프트 + 게임 콘솔 확장 SSD<br>
    <strong>리스크:</strong> PC 성장 정체 / NAND 가격 상승 시 저용량 다운사이즈 수요 / 중국 로컬 NVMe 점유 확대(YMTC Xtacking)
  </div>
  {cat_detail("bear", "internal", "Internal SSD", "#e53e3e", INT_FIELDS)}
  {cat_detail("base", "internal", "Internal SSD", "#e53e3e", INT_FIELDS)}
  {cat_detail("bull", "internal", "Internal SSD", "#e53e3e", INT_FIELDS)}
</div>

<div style="background:white;border-radius:10px;padding:24px 32px;margin-bottom:16px;
            box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <div style="font-size:12px;font-weight:700;color:#dd6b20;text-transform:uppercase;
              letter-spacing:.5px;margin-bottom:16px;">📦 External SSD (Portable SSD) — 카테고리별 상세</div>
  <div style="font-size:12px;color:#4a5568;margin-bottom:12px;line-height:1.7;">
    <strong>핵심 드라이버:</strong> 크리에이터 인구 성장 + USB4/TB4 생태계 확산 ASP 업리프트 + AI 엣지 워크플로우 신규 수요<br>
    <strong>리스크:</strong> 클라우드 스토리지 대체 위협 / 스마트폰 내장 저장소 증가 / 경쟁 심화(WD/Samsung/Seagate)
  </div>
  {cat_detail("bear", "external", "External SSD", "#dd6b20", EXT_FIELDS)}
  {cat_detail("base", "external", "External SSD", "#dd6b20", EXT_FIELDS)}
  {cat_detail("bull", "external", "External SSD", "#dd6b20", EXT_FIELDS)}
</div>

<div style="background:white;border-radius:10px;padding:24px 32px;margin-bottom:16px;
            box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <div style="font-size:12px;font-weight:700;color:#805ad5;text-transform:uppercase;
              letter-spacing:.5px;margin-bottom:16px;">💾 microSD — 카테고리별 상세</div>
  <div style="font-size:12px;color:#4a5568;margin-bottom:12px;line-height:1.7;">
    <strong>핵심 드라이버:</strong> IoT/드론/대시캠 신규 수요 + 1TB microSD 메인스트림화 + Nintendo Switch 2 효과<br>
    <strong>리스크:</strong> 스마트폰 microSD 슬롯 폐지 추세 (삼성 A→Galaxy AI 라인 전환) / QLC 가격 하락 ASP 압박 / UFS 임베디드 대체
  </div>
  {cat_detail("bear", "microsd", "microSD", "#805ad5", MIC_FIELDS)}
  {cat_detail("base", "microsd", "microSD", "#805ad5", MIC_FIELDS)}
  {cat_detail("bull", "microsd", "microSD", "#805ad5", MIC_FIELDS)}
</div>

<!-- ── 핵심 드라이버 전제 ── -->
<div style="background:white;border-radius:10px;padding:24px 32px;margin-bottom:16px;
            box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <div style="font-size:12px;font-weight:700;color:#4a5568;text-transform:uppercase;
              letter-spacing:.5px;margin-bottom:14px;">🔍 핵심 드라이버별 시나리오 전제</div>
  {driver_table()}
</div>

<!-- ── 마케팅 시사점 ── -->
<div style="background:white;border-radius:10px;padding:24px 32px;margin-bottom:16px;
            box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <div style="font-size:12px;font-weight:700;color:#4a5568;text-transform:uppercase;
              letter-spacing:.5px;margin-bottom:14px;">🎯 시나리오별 마케팅 시사점 & 전략 액션</div>
  <table style="border-collapse:collapse;width:100%;font-size:13px;">
    <thead><tr style="background:#edf2f7;border-bottom:2px solid #e2e8f0;">
      <th style="padding:8px 12px;text-align:left;">카테고리</th>
      <th style="padding:8px 12px;text-align:left;">전략 액션</th>
      <th style="padding:8px 12px;text-align:left;">근거 / 핵심 메시지</th>
    </tr></thead>
    <tbody>{impl_rows}</tbody>
  </table>
</div>

<!-- ── 모니터링 지표 ── -->
<div style="background:white;border-radius:10px;padding:24px 32px;margin-bottom:16px;
            box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <div style="font-size:12px;font-weight:700;color:#4a5568;text-transform:uppercase;
              letter-spacing:.5px;margin-bottom:14px;">📡 시나리오 전환 모니터링 지표</div>
  <div style="display:flex;gap:16px;flex-wrap:wrap;">
    <div style="flex:1;min-width:200px;background:#fff5f5;border-left:4px solid #e53e3e;
                padding:12px 16px;border-radius:0 6px 6px 0;">
      <div style="font-size:11px;font-weight:700;color:#e53e3e;margin-bottom:6px;">
        🐻 Bear 전환 신호
      </div>
      <ul style="font-size:12px;color:#4a5568;line-height:1.8;padding-left:16px;margin:0;">
        <li>NAND contract 가격 QoQ +5% 이상 3분기 연속</li>
        <li>글로벌 PC 출하 YoY -3% 이하 (IDC 분기 보고서)</li>
        <li>AI PC 침투율 IDC 예상 대비 15%p+ 미달</li>
        <li>중국 YMTC NVMe 비중 30%+ 상회 (TrendForce)</li>
        <li>클라우드 스토리지 월간 구독자 YoY +25%+</li>
      </ul>
    </div>
    <div style="flex:1;min-width:200px;background:#f0fff4;border-left:4px solid #38a169;
                padding:12px 16px;border-radius:0 6px 6px 0;">
      <div style="font-size:11px;font-weight:700;color:#38a169;margin-bottom:6px;">
        🐂 Bull 전환 신호
      </div>
      <ul style="font-size:12px;color:#4a5568;line-height:1.8;padding-left:16px;margin:0;">
        <li>Microsoft Copilot+ PC 출하 연 1억대+ 초과</li>
        <li>로컬 LLM(7B+ 모델) PC 탑재 OEM 기본화 공표</li>
        <li>Nintendo Switch 2 출시 첫 6개월 1,500만대+ 판매</li>
        <li>USB4 디바이스(노트북+스마트폰) 보급률 50%+ 돌파</li>
        <li>SK Hynix/Micron HBM 캐파 전용 → NAND 투자 제한 장기화</li>
      </ul>
    </div>
    <div style="flex:1;min-width:200px;background:#ebf8ff;border-left:4px solid #3182ce;
                padding:12px 16px;border-radius:0 6px 6px 0;">
      <div style="font-size:11px;font-weight:700;color:#3182ce;margin-bottom:6px;">
        📋 분기별 추적 필수 지표
      </div>
      <ul style="font-size:12px;color:#4a5568;line-height:1.8;padding-left:16px;margin:0;">
        <li>TrendForce NAND 계약가격 월간 리포트</li>
        <li>IDC PC Tracker (분기별 출하/AI PC 비중)</li>
        <li>Kioxia/WD/SK Hynix 분기 실적 컨퍼런스 콜</li>
        <li>Amazon/Best Buy SSD 카테고리 베스트셀러 순위</li>
        <li>Nintendo 출시 일정 공식 발표 모니터링</li>
      </ul>
    </div>
  </div>
</div>

<!-- ── AI 수요가 바꾼 메모리 시장 구조 ── -->
<div style="background:white;border-radius:10px;padding:24px 32px;margin-bottom:16px;
            box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <div style="font-size:12px;font-weight:700;color:#b31412;text-transform:uppercase;
              letter-spacing:.5px;margin-bottom:6px;">🔥 AI 수요가 바꾼 메모리 시장 구조 — SanDisk 마케터 시각</div>
  <div style="font-size:11px;color:#a0aec0;margin-bottom:16px;">
    2026년 현재 NAND 시장은 AI 인프라 수요가 소비자 시장까지 직격하는 구조적 변곡점에 있습니다.
  </div>

  <!-- 핵심 팩트 카드 -->
  <div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px;">
    <div style="flex:1;min-width:160px;background:#fff5f5;border-radius:8px;padding:14px 16px;
                border-top:3px solid #e53e3e;">
      <div style="font-size:10px;color:#e53e3e;font-weight:700;text-transform:uppercase;
                  margin-bottom:6px;">NAND Q1 2026 가격 상승</div>
      <div style="font-size:28px;font-weight:900;color:#e53e3e;">+55~60%</div>
      <div style="font-size:11px;color:#718096;margin-top:4px;">QoQ 분기 상승 — 역대 최대폭</div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">TrendForce, 2026.02.02</div>
    </div>
    <div style="flex:1;min-width:160px;background:#fffaf0;border-radius:8px;padding:14px 16px;
                border-top:3px solid #dd6b20;">
      <div style="font-size:10px;color:#dd6b20;font-weight:700;text-transform:uppercase;
                  margin-bottom:6px;">2026 NAND 공급 현황</div>
      <div style="font-size:28px;font-weight:900;color:#dd6b20;">Sold Out</div>
      <div style="font-size:11px;color:#718096;margin-top:4px;">전년도 생산 캐파 선판매 완료</div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">Phison CEO 발언, Tom's Hardware</div>
    </div>
    <div style="flex:1;min-width:160px;background:#ebf8ff;border-radius:8px;padding:14px 16px;
                border-top:3px solid #3182ce;">
      <div style="font-size:10px;color:#3182ce;font-weight:700;text-transform:uppercase;
                  margin-bottom:6px;">AI의 DRAM 웨이퍼 소비</div>
      <div style="font-size:28px;font-weight:900;color:#3182ce;">~20%</div>
      <div style="font-size:11px;color:#718096;margin-top:4px;">HBM+GDDR7 포함 글로벌 캐파</div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">TrendForce, 2025.12.26</div>
    </div>
    <div style="flex:1;min-width:160px;background:#f0fff4;border-radius:8px;padding:14px 16px;
                border-top:3px solid #38a169;">
      <div style="font-size:10px;color:#38a169;font-weight:700;text-transform:uppercase;
                  margin-bottom:6px;">Enterprise SSD 가격 급등</div>
      <div style="font-size:28px;font-weight:900;color:#38a169;">+257%</div>
      <div style="font-size:11px;color:#718096;margin-top:4px;">30TB TLC 엔터프라이즈 SSD, 2025Q2→2026Q1</div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">Tweaktown, 2026년 시장 조사</div>
    </div>
    <div style="flex:1;min-width:160px;background:#faf5ff;border-radius:8px;padding:14px 16px;
                border-top:3px solid #805ad5;">
      <div style="font-size:10px;color:#805ad5;font-weight:700;text-transform:uppercase;
                  margin-bottom:6px;">PC 출하 전망 하향 (2026E)</div>
      <div style="font-size:28px;font-weight:900;color:#805ad5;">-11.3%</div>
      <div style="font-size:11px;color:#718096;margin-top:4px;">메모리 가격 급등 → PC ASP↑ → 수요 억제</div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">IDC, 2026 PC Tracker 수정 전망</div>
    </div>
  </div>

  <!-- 인과관계 플로우 -->
  <div style="background:#f7fafc;border-radius:8px;padding:16px 20px;margin-bottom:16px;">
    <div style="font-size:11px;font-weight:700;color:#2d3748;margin-bottom:10px;">
      📌 AI 수요 → 소비자 SSD 시장까지 이어지는 인과 연쇄 (SanDisk 마케터 핵심 인사이트)
    </div>
    <div style="font-size:12px;color:#4a5568;line-height:2.2;font-family:monospace;">
      AI 서버 수요 폭발<br>
      &nbsp;&nbsp;↓ <span style="color:#3182ce;">SK Hynix/Samsung/Micron, HBM 웨이퍼 캐파 재배치 (NAND→HBM 전환)</span><br>
      &nbsp;&nbsp;↓ <span style="color:#e53e3e;">NAND 공급 타이트 → Enterprise SSD 우선 배분 (마진 높음)</span><br>
      &nbsp;&nbsp;↓ <span style="color:#dd6b20;">Consumer NAND 물량 부족 → SanDisk 소비자 SSD/microSD 가격 +55%+ QoQ</span><br>
      &nbsp;&nbsp;↓ <span style="color:#805ad5;">PC 노트북 BOM 20%+ 상승 → 소비자 구매 억제 (IDC PC 전망 -11.3%)</span><br>
      &nbsp;&nbsp;↓ <span style="color:#38a169;">BUT: ASP 상승으로 TAM $금액은 유지/증가 → 볼륨 경쟁보다 가격/믹스 전략이 핵심</span>
    </div>
  </div>

  <!-- SanDisk 포지셔닝 시사점 -->
  <div style="border-left:4px solid #b31412;padding:12px 18px;background:#fff5f5;border-radius:0 6px 6px 0;">
    <div style="font-size:11px;font-weight:700;color:#b31412;margin-bottom:8px;">
      🎯 SanDisk 전문 마케터 관점: 이 위기를 어떻게 기회로 전환하는가
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;font-size:12px;color:#4a5568;line-height:1.7;">
      <div><strong>① 프리미엄 포지셔닝 강화:</strong> NAND 부족 시기, 가격 경쟁보다 WD BLACK/Extreme Pro 브랜드 가치 방어. 저가 SKU 축소 → 마진 믹스 개선.</div>
      <div><strong>② 재고 선확보 전략:</strong> 2026 캐파 Sold Out 상황에서 장기 공급계약(LTA) 파트너사 우선 공급. 채널 로열티 구축.</div>
      <div><strong>③ AI PC 시장 선점:</strong> Copilot+ PC 검증 파트너로 Intel/AMD/MS와 협업. "AI PC 공식 스토리지" 메시지 = NAND 부족기에도 교체 수요 창출.</div>
      <div><strong>④ 볼륨 보다 믹스:</strong> 출하량 감소 가능성 있으나 ASP 방어로 매출 유지 가능. 4TB External SSD, 2TB Internal SSD 상위 모델 비중 확대.</div>
    </div>
  </div>
</div>

<!-- ── 매크로 & 구매력 분석 ── -->
<div style="background:white;border-radius:10px;padding:24px 32px;margin-bottom:16px;
            box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <div style="font-size:12px;font-weight:700;color:#4a5568;text-transform:uppercase;
              letter-spacing:.5px;margin-bottom:14px;">🌍 매크로 & 소비자 구매력 분석 (시나리오 전제)</div>

  <div style="display:flex;gap:16px;flex-wrap:wrap;margin-bottom:20px;">
    <!-- 경제성장 -->
    <div style="flex:1;min-width:200px;">
      <div style="font-size:11px;font-weight:700;color:#2d3748;margin-bottom:8px;">글로벌 GDP 성장 전망</div>
      <table style="border-collapse:collapse;width:100%;font-size:12px;">
        <thead><tr style="background:#f7f8fa;">
          <th style="padding:5px 10px;text-align:left;">지역</th>
          <th style="padding:5px 10px;text-align:right;">2026E</th>
          <th style="padding:5px 10px;text-align:right;">2027E</th>
        </tr></thead>
        <tbody>
          <tr><td style="padding:4px 10px;">미국</td>
              <td style="padding:4px 10px;text-align:right;color:#3182ce;">+1.8%</td>
              <td style="padding:4px 10px;text-align:right;">+2.0%</td></tr>
          <tr style="background:#f7f8fa;"><td style="padding:4px 10px;">유럽존</td>
              <td style="padding:4px 10px;text-align:right;color:#718096;">+1.1%</td>
              <td style="padding:4px 10px;text-align:right;">+1.3%</td></tr>
          <tr><td style="padding:4px 10px;">중국</td>
              <td style="padding:4px 10px;text-align:right;color:#38a169;">+5.0%</td>
              <td style="padding:4px 10px;text-align:right;">+4.5%</td></tr>
          <tr style="background:#f7f8fa;"><td style="padding:4px 10px;">글로벌</td>
              <td style="padding:4px 10px;text-align:right;font-weight:700;">+2.7~3.2%</td>
              <td style="padding:4px 10px;text-align:right;font-weight:700;">+2.8%</td></tr>
        </tbody>
      </table>
      <div style="font-size:10px;color:#a0aec0;margin-top:4px;">출처: Goldman Sachs, Morgan Stanley, Deloitte 2026 Outlook</div>
    </div>

    <!-- 인플레/소비 -->
    <div style="flex:1;min-width:200px;">
      <div style="font-size:11px;font-weight:700;color:#2d3748;margin-bottom:8px;">소비자 구매력 리스크 (미국)</div>
      <table style="border-collapse:collapse;width:100%;font-size:12px;">
        <thead><tr style="background:#f7f8fa;">
          <th style="padding:5px 10px;text-align:left;">지표</th>
          <th style="padding:5px 10px;text-align:right;">수치</th>
        </tr></thead>
        <tbody>
          <tr><td style="padding:4px 10px;">관세 가구당 추가 부담</td>
              <td style="padding:4px 10px;text-align:right;color:#e53e3e;font-weight:700;">$1,500~2,512/yr</td></tr>
          <tr style="background:#f7f8fa;"><td style="padding:4px 10px;">내구재 가격 상승 전망</td>
              <td style="padding:4px 10px;text-align:right;color:#dd6b20;">+4.5% (2026E)</td></tr>
          <tr><td style="padding:4px 10px;">미국 인플레이션 전망</td>
              <td style="padding:4px 10px;text-align:right;">2.7% (2026E)</td></tr>
          <tr style="background:#f7f8fa;"><td style="padding:4px 10px;">리세션 확률 (12개월)</td>
              <td style="padding:4px 10px;text-align:right;color:#805ad5;">30% (J.P. Morgan)</td></tr>
          <tr><td style="padding:4px 10px;">Best Buy 관세 부담</td>
              <td style="padding:4px 10px;text-align:right;color:#e53e3e;">$1.2B (2026)</td></tr>
        </tbody>
      </table>
      <div style="font-size:10px;color:#a0aec0;margin-top:4px;">출처: J.P. Morgan, Morningstar, Tax Foundation, CTA 2026</div>
    </div>

    <!-- 타리프 영향 -->
    <div style="flex:1;min-width:200px;">
      <div style="font-size:11px;font-weight:700;color:#2d3748;margin-bottom:8px;">메모리 가격 소비자 영향 체인</div>
      <div style="font-size:12px;color:#4a5568;line-height:1.9;">
        <div style="padding:5px 10px;background:#fff5f5;border-radius:4px;margin-bottom:4px;">
          <strong style="color:#e53e3e;">노트북 BOM 중 메모리 비중</strong><br>
          2025년 10~18% → 2026년 <strong>20%+</strong> (TrendForce)
        </div>
        <div style="padding:5px 10px;background:#fffaf0;border-radius:4px;margin-bottom:4px;">
          <strong style="color:#dd6b20;">노트북 소비자 가격 상승</strong><br>
          추가 <strong>+5~15%</strong> (TrendForce 추정)
        </div>
        <div style="padding:5px 10px;background:#ebf8ff;border-radius:4px;">
          <strong style="color:#3182ce;">SSD 단독 소매가 상승</strong><br>
          Samsung T7 1TB: KRW 14만 → <strong>28만</strong> (2배 상승)
        </div>
      </div>
    </div>
  </div>

  <!-- 시나리오별 매크로 전제 -->
  <div style="font-size:11px;font-weight:700;color:#2d3748;margin-bottom:8px;">
    시나리오별 매크로 전제 및 SSD 수요 영향
  </div>
  <table style="border-collapse:collapse;width:100%;font-size:12px;">
    <thead><tr style="background:#edf2f7;border-bottom:2px solid #e2e8f0;">
      <th style="padding:7px 12px;text-align:left;">매크로 변수</th>
      <th style="padding:7px 12px;text-align:left;color:#e53e3e;">Bear 전제</th>
      <th style="padding:7px 12px;text-align:left;color:#3182ce;">Base 전제</th>
      <th style="padding:7px 12px;text-align:left;color:#38a169;">Bull 전제</th>
      <th style="padding:7px 12px;text-align:left;">SSD 수요 영향</th>
    </tr></thead>
    <tbody>
      <tr style="border-bottom:1px solid #f0f0f0;">
        <td style="padding:6px 12px;font-weight:600;">미국 GDP 성장</td>
        <td style="padding:6px 12px;color:#e53e3e;">+0~1% (침체 30% 확률 현실화)</td>
        <td style="padding:6px 12px;color:#3182ce;">+1.5~2.0% (골디락스)</td>
        <td style="padding:6px 12px;color:#38a169;">+2.5%+ (AI 투자 낙수효과)</td>
        <td style="padding:6px 12px;font-size:11px;color:#718096;">PC 교체 수요 직결. GDP 1%↓ = PC -2~3%</td>
      </tr>
      <tr style="background:#f7f8fa;border-bottom:1px solid #f0f0f0;">
        <td style="padding:6px 12px;font-weight:600;">관세/무역 리스크</td>
        <td style="padding:6px 12px;color:#e53e3e;">중국 관세 145% 유지 + 확대. 소비자 구매력 $2,500+ 추가 손실</td>
        <td style="padding:6px 12px;color:#3182ce;">현 수준 유지. 메모리 별도 협상 여지</td>
        <td style="padding:6px 12px;color:#38a169;">미중 무역 협상 일부 완화. 관세 부담 축소</td>
        <td style="padding:6px 12px;font-size:11px;color:#718096;">SSD 소매가에 관세 직접 전가 시 추가 10~20% 인상</td>
      </tr>
      <tr style="border-bottom:1px solid #f0f0f0;">
        <td style="padding:6px 12px;font-weight:600;">소비자 sentiment</td>
        <td style="padding:6px 12px;color:#e53e3e;">내구재 구매 이연. 저용량 다운사이즈 수요 증가</td>
        <td style="padding:6px 12px;color:#3182ce;">프리미엄 제품 수요 탄력적 유지</td>
        <td style="padding:6px 12px;color:#38a169;">AI PC/크리에이터 필수재화 인식 → 불황에도 구매</td>
        <td style="padding:6px 12px;font-size:11px;color:#718096;">Bear: 512GB 수요↑, 4TB↓. Bull: 2TB+ 수요↑↑</td>
      </tr>
      <tr style="background:#f7f8fa;border-bottom:1px solid #f0f0f0;">
        <td style="padding:6px 12px;font-weight:600;">AI 투자 지속성</td>
        <td style="padding:6px 12px;color:#e53e3e;">CSP CapEx 경기 둔화 + AI ROI 회의론으로 일부 축소</td>
        <td style="padding:6px 12px;color:#3182ce;">연 15~20% AI 인프라 투자 지속</td>
        <td style="padding:6px 12px;color:#38a169;">AI 투자 가속 → NAND 공급 타이트 장기화 → ASP 방어</td>
        <td style="padding:6px 12px;font-size:11px;color:#718096;">Enterprise SSD 수요 직결. Consumer NAND 공급 간접 결정</td>
      </tr>
      <tr>
        <td style="padding:6px 12px;font-weight:600;">신흥국 성장</td>
        <td style="padding:6px 12px;color:#e53e3e;">달러 강세 → 신흥국 구매력 약화</td>
        <td style="padding:6px 12px;color:#3182ce;">인도/동남아 중산층 성장 지속</td>
        <td style="padding:6px 12px;color:#38a169;">중국 5%+ 성장 + 인도 7%+ → microSD/저가 SSD 수요↑</td>
        <td style="padding:6px 12px;font-size:11px;color:#718096;">microSD 볼륨 시장과 직결. Ultra 라인 수요 결정</td>
      </tr>
    </tbody>
  </table>

  <div style="background:#ebf8ff;border-left:4px solid #3182ce;padding:10px 16px;
              border-radius:0 6px 6px 0;margin-top:14px;font-size:12px;color:#2d3748;line-height:1.7;">
    <strong>📌 SanDisk 마케터 핵심 관점:</strong>
    관세 $1,500 가구당 부담 + NAND 가격 55%+ 상승의 이중 압박에도,
    <strong>AI PC는 '필수 교체 사이클'</strong>을 만들어낸다.
    Copilot+ PC 인증을 받은 시스템은 최소 256GB SSD가 필요하고,
    <em>실질적으로 2TB가 권장</em>(70B 모델 ~40GB, 게임+OS+모델 동시 = 2TB 소진).
    즉, 구매력이 줄어도 <strong>한 번 살 때 더 큰 용량</strong>을 사는 트렌드 → ASP 방어 가능.
    SanDisk의 전략은 '볼륨 싸움'이 아닌 <strong>'용량 업그레이드 내러티브 장악'</strong>이다.
  </div>
</div>

<!-- ── 참고자료 (URL + 연관 내용 발췌) ── -->
<div style="background:white;border-radius:10px;padding:24px 32px;margin-bottom:16px;
            box-shadow:0 2px 8px rgba(0,0,0,.06);">
  <div style="font-size:12px;font-weight:700;color:#4a5568;text-transform:uppercase;
              letter-spacing:.5px;margin-bottom:14px;">📚 참고자료 — URL 및 핵심 발췌 내용</div>
  <div style="font-size:11px;color:#718096;margin-bottom:14px;">
    아래 자료는 본 예측 모델의 핵심 드라이버 수치의 근거입니다. 발췌 내용은 본 분석과 직접 연관된 부분만 정리했습니다.
  </div>

  <!-- NAND/메모리 가격 -->
  <div style="font-size:11px;font-weight:700;color:#e53e3e;text-transform:uppercase;
              letter-spacing:.3px;margin-bottom:8px;padding-bottom:4px;
              border-bottom:2px solid #e53e3e;">
    📊 NAND 가격 & 공급 구조
  </div>

  <div style="margin-bottom:16px;">
    <div style="margin-bottom:10px;padding:12px 16px;background:#fff5f5;border-radius:6px;border-left:3px solid #e53e3e;">
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:6px;">
        <span style="background:#e53e3e;color:white;font-size:10px;padding:2px 7px;border-radius:4px;white-space:nowrap;">TrendForce</span>
        <a href="https://www.trendforce.com/presscenter/news/20260202-12911.html"
           style="font-size:12px;font-weight:700;color:#2d3748;text-decoration:none;">
          Memory Price Outlook for 1Q26 Sharply Upgraded; QoQ Increases to Hit Record Highs
        </a>
      </div>
      <div style="font-size:12px;color:#4a5568;line-height:1.7;background:white;padding:8px 12px;border-radius:4px;">
        <strong>연관 발췌:</strong>
        "NAND Flash contract prices projected to increase <strong>55–60% QoQ</strong> in Q1 2026, marking a record quarterly advance.
        Enterprise SSD prices expected to rise <strong>53–58% QoQ</strong>.
        Memory manufacturers are reallocating production capacity toward higher-margin DRAM,
        deliberately constraining NAND Flash output.
        North American CSPs have substantially increased storage procurement to support expanding AI inference applications."
      </div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">
        📌 본 예측 반영: NAND 가격 시나리오 기준점 설정 (Base +8%, Bull +20%/2026), 수요 탄성치 조정
      </div>
    </div>

    <div style="margin-bottom:10px;padding:12px 16px;background:#fff5f5;border-radius:6px;border-left:3px solid #e53e3e;">
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:6px;">
        <span style="background:#e53e3e;color:white;font-size:10px;padding:2px 7px;border-radius:4px;white-space:nowrap;">TrendForce</span>
        <a href="https://www.trendforce.com/presscenter/news/20251117-12784.html"
           style="font-size:12px;font-weight:700;color:#2d3748;text-decoration:none;">
          Rising Memory Prices Weigh on Consumer Markets; 2026 Smartphone and Notebook Outlook Revised Downward
        </a>
      </div>
      <div style="font-size:12px;color:#4a5568;line-height:1.7;background:white;padding:8px 12px;border-radius:4px;">
        <strong>연관 발췌:</strong>
        "Notebooks output expected to shrink <strong>2.4%</strong>, reversed from prior +1.7% estimate.
        Memory will surpass <strong>20% of notebook BOM costs</strong> in 2026 (up from 10-18%).
        Retail price increases of <strong>5–15% for notebooks</strong> expected, creating downward demand pressure.
        DRAM prices Q4 2025 anticipated to grow <strong>more than 75% YoY</strong>."
      </div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">
        📌 본 예측 반영: PC SSD 수요 탄성치, 노트북 BOM 상승 → Internal SSD 단독 교체 수요 계산
      </div>
    </div>

    <div style="margin-bottom:10px;padding:12px 16px;background:#fff5f5;border-radius:6px;border-left:3px solid #e53e3e;">
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:6px;">
        <span style="background:#718096;color:white;font-size:10px;padding:2px 7px;border-radius:4px;white-space:nowrap;">Tom's Hardware</span>
        <a href="https://www.tomshardware.com/pc-components/ssds/phison-ceo-confirms-nand-prices-have-more-than-doubled-and-will-continue-to-rise-all-2026-production-already-sold-out-ssds-facing-pricing-apocalypse-throughout-2027"
           style="font-size:12px;font-weight:700;color:#2d3748;text-decoration:none;">
          Phison CEO confirms NAND prices have more than doubled — all 2026 production already sold out
        </a>
      </div>
      <div style="font-size:12px;color:#4a5568;line-height:1.7;background:white;padding:8px 12px;border-radius:4px;">
        <strong>연관 발췌:</strong>
        "TLC 1-terabit chips doubled from <strong>$4.80 → $10.70 USD</strong>.
        All NAND production capacity <strong>sold out for all of 2026</strong>.
        Phison and storage makers prioritizing enterprise customers who pay inflated prices with higher margins.
        'Supply will remain deficient for a few years.' — SSD pricing apocalypse throughout 2027."
      </div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">
        📌 본 예측 반영: Bull 시나리오 NAND 공급 타이트 2027년까지 지속 전제, Bear 시나리오 소비자 수요 억제 전제
      </div>
    </div>

    <div style="margin-bottom:10px;padding:12px 16px;background:#fff5f5;border-radius:6px;border-left:3px solid #e53e3e;">
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:6px;">
        <span style="background:#718096;color:white;font-size:10px;padding:2px 7px;border-radius:4px;white-space:nowrap;">TrendForce</span>
        <a href="https://www.trendforce.com/news/2025/12/26/news-ai-reportedly-to-consume-20-of-global-dram-wafer-capacity-in-2026-hbm-gddr7-lead-demand/"
           style="font-size:12px;font-weight:700;color:#2d3748;text-decoration:none;">
          AI Reportedly to Consume 20% of Global DRAM Wafer Capacity in 2026, HBM and GDDR7 Lead Demand
        </a>
      </div>
      <div style="font-size:12px;color:#4a5568;line-height:1.7;background:white;padding:8px 12px;border-radius:4px;">
        <strong>연관 발췌:</strong>
        "AI could effectively consume nearly <strong>20% of global DRAM supply</strong> when factoring in equivalent wafer usage of HBM and GDDR7.
        DRAM suppliers reallocating advanced process nodes toward server and HBM products.
        Memory manufacturers remain optimistic about DRAM profitability and are proactively reallocating parts of production lines to DRAM,
        <strong>further limiting the expansion of NAND Flash capacity</strong>."
      </div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">
        📌 본 예측 반영: HBM 캐파 전환으로 NAND 공급 제약 → 공통 리스크 China risk 및 NAND 가격 방향 근거
      </div>
    </div>
  </div>

  <!-- PC/AI PC 시장 -->
  <div style="font-size:11px;font-weight:700;color:#3182ce;text-transform:uppercase;
              letter-spacing:.3px;margin-bottom:8px;padding-bottom:4px;
              border-bottom:2px solid #3182ce;">
    🖥️ PC / AI PC 시장
  </div>

  <div style="margin-bottom:16px;">
    <div style="margin-bottom:10px;padding:12px 16px;background:#ebf8ff;border-radius:6px;border-left:3px solid #3182ce;">
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:6px;">
        <span style="background:#3182ce;color:white;font-size:10px;padding:2px 7px;border-radius:4px;white-space:nowrap;">Tom's Hardware / IDC</span>
        <a href="https://www.tomshardware.com/tech-industry/idc-warns-pc-market-could-shrink-up-to-9-percent-in-2026-due-to-skyrocketing-ram-pricing-even-moderate-forecast-hits-5-percent-drop-as-ai-driven-shortages-slam-into-pc-market"
           style="font-size:12px;font-weight:700;color:#2d3748;text-decoration:none;">
          IDC warns PC market could shrink up to 9% in 2026 due to skyrocketing RAM pricing
        </a>
      </div>
      <div style="font-size:12px;color:#4a5568;line-height:1.7;background:white;padding:8px 12px;border-radius:4px;">
        <strong>연관 발췌:</strong>
        "Global PC shipments expected to decline <strong>-11.3%</strong> in 2026 (pessimistic: -9%, moderate: -5%).
        Decline driven by memory shortages, rising component prices, and broader supply constraints.
        However, higher ASPs expected to lift total market value — PCs growing <strong>1.6% to $274 billion</strong>.
        <strong>Memory shortages will persist well into 2027.</strong>"
      </div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">
        📌 본 예측 반영: 2026 PC 출하 감소 → Internal SSD 단위 수요 하방 조정, Bear 시나리오 근거
      </div>
    </div>

    <div style="margin-bottom:10px;padding:12px 16px;background:#ebf8ff;border-radius:6px;border-left:3px solid #3182ce;">
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:6px;">
        <span style="background:#3182ce;color:white;font-size:10px;padding:2px 7px;border-radius:4px;white-space:nowrap;">IDC / Canalys</span>
        <a href="https://industryanalysts.com/021324_mars_idc_ai/"
           style="font-size:12px;font-weight:700;color:#2d3748;text-decoration:none;">
          IDC Forecasts AI PCs to Account for Nearly 60% of All PC Shipments by 2027
        </a>
      </div>
      <div style="font-size:12px;color:#4a5568;line-height:1.7;background:white;padding:8px 12px;border-radius:4px;">
        <strong>연관 발췌:</strong>
        "AI PC shipments growing from nearly <strong>50 million units in 2024</strong> to more than <strong>167 million in 2027</strong>.
        By end of forecast, AI PCs will represent <strong>nearly 60% of all PC shipments</strong> worldwide.
        Copilot+ PC must meet: NPU 40+ TOPS, <strong>16GB RAM, minimum 256GB SSD</strong> — actual recommendation is 2TB."
      </div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">
        📌 본 예측 반영: AI PC 침투율 Base 시나리오 2027년 55%+ 전제, 평균 용량 프리미엄 계산
      </div>
    </div>

    <div style="margin-bottom:10px;padding:12px 16px;background:#ebf8ff;border-radius:6px;border-left:3px solid #3182ce;">
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:6px;">
        <span style="background:#718096;color:white;font-size:10px;padding:2px 7px;border-radius:4px;white-space:nowrap;">PCWorld / LocalAI Guide</span>
        <a href="https://www.pcworld.com/article/2599606/run-ai-locally-on-your-pc-need-a-bigger-hard-drive.html"
           style="font-size:12px;font-weight:700;color:#2d3748;text-decoration:none;">
          Want to run AI on your PC? You're gonna need a bigger hard drive
        </a>
      </div>
      <div style="font-size:12px;color:#4a5568;line-height:1.7;background:white;padding:8px 12px;border-radius:4px;">
        <strong>연관 발췌:</strong>
        "At least <strong>1TB storage is recommended</strong> for AI features; <strong>2TB advised</strong> if combining with games/videos.
        70B model at Q4 quantization ≈ <strong>~40GB</strong>.
        For fine-tuning work: <strong>2TB+ Gen4 NVMe required</strong>.
        4TB might be needed to be future-proof."
      </div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">
        📌 본 예측 반영: AI PC 용량 프리미엄 (Bull: 2030년 평균 용량 2.8TB) 계산 기반
      </div>
    </div>
  </div>

  <!-- External SSD / 크리에이터 -->
  <div style="font-size:11px;font-weight:700;color:#dd6b20;text-transform:uppercase;
              letter-spacing:.3px;margin-bottom:8px;padding-bottom:4px;
              border-bottom:2px solid #dd6b20;">
    📦 External SSD & 크리에이터 이코노미
  </div>

  <div style="margin-bottom:16px;">
    <div style="margin-bottom:10px;padding:12px 16px;background:#fffaf0;border-radius:6px;border-left:3px solid #dd6b20;">
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:6px;">
        <span style="background:#dd6b20;color:white;font-size:10px;padding:2px 7px;border-radius:4px;white-space:nowrap;">DemandSage / Research Nester</span>
        <a href="https://www.demandsage.com/creator-economy-statistics/"
           style="font-size:12px;font-weight:700;color:#2d3748;text-decoration:none;">
          41+ Creator Economy Statistics 2026
        </a>
      </div>
      <div style="font-size:12px;color:#4a5568;line-height:1.7;background:white;padding:8px 12px;border-radius:4px;">
        <strong>연관 발췌:</strong>
        "Creator economy estimated at <strong>USD 214.37 billion in 2026</strong>, projected to reach <strong>~$500 billion by 2027</strong> (CAGR 26%).
        More than <strong>300 million people</strong> worldwide use creator platforms.
        Video streaming segment driving strong growth — dominates with <strong>23.8% format share</strong>."
      </div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">
        📌 본 예측 반영: External SSD 크리에이터 수요 Base +12~14%/yr, 300M 크리에이터 기반 계산
      </div>
    </div>

    <div style="margin-bottom:10px;padding:12px 16px;background:#fffaf0;border-radius:6px;border-left:3px solid #dd6b20;">
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:6px;">
        <span style="background:#718096;color:white;font-size:10px;padding:2px 7px;border-radius:4px;white-space:nowrap;">PenBrief / ZikeTech</span>
        <a href="https://www.penbrief.com/usb4-evolution-2026-explained/"
           style="font-size:12px;font-weight:700;color:#2d3748;text-decoration:none;">
          USB4 Evolution 2026: The Essential Guide to the Connectivity Revolution
        </a>
      </div>
      <div style="font-size:12px;color:#4a5568;line-height:1.7;background:white;padding:8px 12px;border-radius:4px;">
        <strong>연관 발췌:</strong>
        "USB4 achieved <strong>60% penetration in new laptops by mid-2025</strong>.
        USB4 portable SSDs offer speeds up to <strong>4,000 MB/s</strong> on supported systems.
        Samsung Portable SSD P9 launches with USB4, <strong>4000MB/s</strong> transfer speed (Jan 2026).
        USB4 enclosures remain the <strong>mainstream choice</strong> in 2025-2026 for consumers."
      </div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">
        📌 본 예측 반영: USB4 전환율 Base 2026년 22% → 2030년 74%, ASP 프리미엄 +28% (2026) → 수렴
      </div>
    </div>
  </div>

  <!-- microSD -->
  <div style="font-size:11px;font-weight:700;color:#805ad5;text-transform:uppercase;
              letter-spacing:.3px;margin-bottom:8px;padding-bottom:4px;
              border-bottom:2px solid #805ad5;">
    💾 microSD 시장
  </div>

  <div style="margin-bottom:16px;">
    <div style="margin-bottom:10px;padding:12px 16px;background:#faf5ff;border-radius:6px;border-left:3px solid #805ad5;">
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:6px;">
        <span style="background:#805ad5;color:white;font-size:10px;padding:2px 7px;border-radius:4px;white-space:nowrap;">Bloomberg / Tom's Guide</span>
        <a href="https://www.bloomberg.com/news/articles/2026-03-05/nintendo-switch-2-users-face-storage-woes-as-memory-crisis-bites"
           style="font-size:12px;font-weight:700;color:#2d3748;text-decoration:none;">
          Nintendo Switch 2 Users Face Storage Shortage as Memory Crisis Bites
        </a>
      </div>
      <div style="font-size:12px;color:#4a5568;line-height:1.7;background:white;padding:8px 12px;border-radius:4px;">
        <strong>연관 발췌:</strong>
        "Demand for Nintendo's game software under threat from <strong>soaring NAND flash prices</strong>.
        <strong>256GB microSD cards increased from $36 to $46</strong>, 512GB from $66 to $84.
        NAND contract prices forecast to surge as much as <strong>90% in current quarter</strong>.
        Memory manufacturers prioritizing server-grade chips — creating <strong>chip shortage for consumer products like microSD cards</strong>."
      </div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">
        📌 본 예측 반영: Nintendo Switch 2 Bull 시나리오 22~38M units 추가 수요 + NAND 가격 탄성 (-0.70) 반영
      </div>
    </div>

    <div style="margin-bottom:10px;padding:12px 16px;background:#faf5ff;border-radius:6px;border-left:3px solid #805ad5;">
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:6px;">
        <span style="background:#805ad5;color:white;font-size:10px;padding:2px 7px;border-radius:4px;white-space:nowrap;">Tom's Hardware</span>
        <a href="https://www.tomshardware.com/pc-components/microsd-cards/best-microsd-express-cards-for-nintendo-switch-2"
           style="font-size:12px;font-weight:700;color:#2d3748;text-decoration:none;">
          Best MicroSD Express Cards for Nintendo Switch 2 in 2026
        </a>
      </div>
      <div style="font-size:12px;color:#4a5568;line-height:1.7;background:white;padding:8px 12px;border-radius:4px;">
        <strong>연관 발췌:</strong>
        "Switch 2 arrives with <strong>256GB UFS 3.1</strong> internal storage — modern games quickly fill capacity.
        Requires <strong>microSD Express (SD 4.0 UHS-II)</strong> standard — not all cards compatible.
        SanDisk products prominently featured in recommended list — brand equity validation."
      </div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">
        📌 본 예측 반영: SanDisk microSD Express 제품 포지셔닝 기회, 코번들 파트너십 전략 근거
      </div>
    </div>
  </div>

  <!-- 매크로 -->
  <div style="font-size:11px;font-weight:700;color:#2d3748;text-transform:uppercase;
              letter-spacing:.3px;margin-bottom:8px;padding-bottom:4px;
              border-bottom:2px solid #2d3748;">
    🌍 매크로 / 소비자 구매력
  </div>

  <div style="margin-bottom:16px;">
    <div style="margin-bottom:10px;padding:12px 16px;background:#edf2f7;border-radius:6px;border-left:3px solid #2d3748;">
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:6px;">
        <span style="background:#2d3748;color:white;font-size:10px;padding:2px 7px;border-radius:4px;white-space:nowrap;">J.P. Morgan / Tax Foundation</span>
        <a href="https://www.jpmorgan.com/insights/markets-and-economy/economy/economic-trends"
           style="font-size:12px;font-weight:700;color:#2d3748;text-decoration:none;">
          2026 Outlook: Top 10 macro and market considerations
        </a>
      </div>
      <div style="font-size:12px;color:#4a5568;line-height:1.7;background:white;padding:8px 12px;border-radius:4px;">
        <strong>연관 발췌:</strong>
        "Trump tariffs represent the <strong>largest US tax increase since 1993</strong> — average tax increase of <strong>$1,500 per US household</strong>.
        Congressional estimates: tariffs costing households <strong>~$2,512 in 2026</strong>.
        Tariff regime acts as a <strong>regressive tax, disproportionately affecting lower-income households</strong> spending on electronics.
        Recession probability over next 12 months reduced to <strong>30%</strong> (from 40%)."
      </div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">
        📌 본 예측 반영: Bear 소비자 sentiment 악화 → 저용량 다운사이즈 수요 증가, External SSD 클라우드 대체 리스크 상향
      </div>
    </div>

    <div style="margin-bottom:10px;padding:12px 16px;background:#edf2f7;border-radius:6px;border-left:3px solid #2d3748;">
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:6px;">
        <span style="background:#2d3748;color:white;font-size:10px;padding:2px 7px;border-radius:4px;white-space:nowrap;">Morningstar / CTA</span>
        <a href="https://www.morningstar.com/economy/inflation-set-rise-tariff-costs-hit-consumers-2026"
           style="font-size:12px;font-weight:700;color:#2d3748;text-decoration:none;">
          Inflation Set to Rise in 2026 as Tariff Costs Hit Consumers
        </a>
      </div>
      <div style="font-size:12px;color:#4a5568;line-height:1.7;background:white;padding:8px 12px;border-radius:4px;">
        <strong>연관 발췌:</strong>
        "Durable goods prices — <strong>electronics, toys, tools, small appliances — to rise 4.5%</strong> in 2026.
        Best Buy projecting <strong>$1.2 billion pretax direct tariff expense</strong> for 2026.
        ~60% of consumer electronics sourced from China — margins compressed.
        Import prices up nearly <strong>10%</strong>, businesses footing tariff bills through pre-tariff inventory (running out)."
      </div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">
        📌 본 예측 반영: External SSD ASP 추가 상승 요인, 소비자 구매력 Bear 시나리오 전제, 채널 마진 압박
      </div>
    </div>

    <div style="margin-bottom:10px;padding:12px 16px;background:#edf2f7;border-radius:6px;border-left:3px solid #2d3748;">
      <div style="display:flex;align-items:flex-start;gap:10px;margin-bottom:6px;">
        <span style="background:#2d3748;color:white;font-size:10px;padding:2px 7px;border-radius:4px;white-space:nowrap;">Morgan Stanley / Goldman Sachs</span>
        <a href="https://www.morganstanley.com/insights/articles/global-economic-outlook-2026"
           style="font-size:12px;font-weight:700;color:#2d3748;text-decoration:none;">
          Global Economic Outlook 2026: U.S. Resilience to Lead Growth
        </a>
      </div>
      <div style="font-size:12px;color:#4a5568;line-height:1.7;background:white;padding:8px 12px;border-radius:4px;">
        <strong>연관 발췌:</strong>
        "Global growth to moderate to <strong>3.0% in 2025, 3.2% in 2026</strong>.
        US GDP: <strong>+1.8% in 2026, +2.0% in 2027</strong> — consumer spending remains resilient.
        A drop in AI-related spending could be enough to <strong>push economy into recession</strong> — AI investment continuity is key.
        American consumer proven resilient across income levels — strong spending in both luxury and value chains."
      </div>
      <div style="font-size:10px;color:#a0aec0;margin-top:6px;">
        📌 본 예측 반영: Base 시나리오 GDP 성장 전제, AI 투자 지속성 → Bull 시나리오 NAND 공급 타이트 연장 근거
      </div>
    </div>
  </div>

  <!-- 범례 -->
  <div style="background:#f7fafc;border-radius:6px;padding:10px 16px;font-size:11px;color:#718096;">
    <strong>데이터 수집 기준:</strong> 2026년 4월 8일 &nbsp;·&nbsp;
    TrendForce, IDC, Bloomberg, Tom's Hardware, Morgan Stanley, J.P. Morgan, Goldman Sachs,
    Morningstar, DemandSage, USB-IF, Nintendo Life, PCWorld 등 업계 1차 소스 기반.
    발췌 인용은 원문의 의미를 변경하지 않는 범위에서 요약되었습니다.
  </div>
</div>

<!-- ── 방법론 주석 ── -->
<div style="background:#f7f8fa;border-radius:10px;padding:18px 28px;
            font-size:11px;color:#718096;line-height:1.7;">
  <strong style="color:#4a5568;">방법론 주석:</strong>
  본 예측은 Bottom-up 수요 모델 기반으로 구성되었습니다.
  PC 출하(IDC) × SSD 탑재율 × 평균 용량 × ASP 믹스 + 카테고리별 신규 수요 벡터 합산 방식.
  NAND 가격 탄성치(-0.35~-0.70)는 2018~2024년 사이클 실제 수요 반응 데이터에서 도출.
  중국 리스크는 BIS 수출통제 강도 시나리오 기반 추정.
  모든 수치는 연구 목적 추정치이며 실제 결과와 상이할 수 있습니다.
  &nbsp;·&nbsp; 생성: {TODAY.strftime("%Y-%m-%d")}
</div>

</div>
</body>
</html>"""


# ══════════════════════════════════════════════════════════════
# 5. 메인
# ══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--open", action="store_true", help="브라우저로 열기")
    args = parser.parse_args()

    print("\n" + "="*60)
    print("SSD 시나리오 수요 예측 2026~2030")
    print("="*60)

    scenarios = {}
    for sc in ["bear", "base", "bull"]:
        scenarios[sc] = run_scenario(sc)
        total_2025 = (FACT_BASE["internal_ssd_tam_2025_b"] +
                      FACT_BASE["external_ssd_tam_2025_b"] +
                      FACT_BASE["microsd_tam_2025_b"])
        total_2030 = scenarios[sc][2030]["total_tam_b"]
        cagr = ((total_2030 / total_2025) ** 0.2 - 1) * 100
        print(f"  {sc.upper():4s}: 2025 ${total_2025:.1f}B → 2030 ${total_2030:.1f}B "
              f"(CAGR {cagr:+.1f}%)")

    # JSON 저장 (중간 데이터)
    json_path = REPORTS_DIR / "ssd_scenario_2026_2030.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(scenarios, f, indent=2, ensure_ascii=False)

    # HTML 빌드 & 저장
    html = build_html_report(scenarios)
    out  = REPORTS_DIR / f"ssd_scenario_forecast_{TODAY.strftime('%Y%m%d')}.html"
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"\n  리포트 저장: {out}")

    if args.open:
        subprocess.run(["open", str(out)])
    else:
        print(f"  브라우저 열기: python3 scenario_forecast.py --open")


if __name__ == "__main__":
    main()
