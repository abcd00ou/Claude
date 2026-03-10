"""
SanDisk B2C Storage Marketing Team — 설정
팀 리더: Claude (Marketing Team Lead)
"""
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR    = BASE_DIR / "data"
OUTPUT_DIR  = BASE_DIR / "outputs"
EXCEL_DIR   = OUTPUT_DIR / "excel"
PPTX_DIR    = OUTPUT_DIR / "pptx"
REPORTS_DIR = BASE_DIR / "reports"

for d in [DATA_DIR, EXCEL_DIR, PPTX_DIR, REPORTS_DIR]:
    d.mkdir(exist_ok=True)

# ── 제품 포트폴리오 ─────────────────────────────────────────────
PRODUCT_CATEGORIES = ["internal_ssd", "external_ssd", "microsd"]

PRODUCTS = {
    # ── Internal SSD ────────────────────────────────────────────
    # SN8100 — BiCS8 최신 플래그십 (신규)
    "WD_BLACK_SN8100_1TB":  {"cat": "internal_ssd", "brand": "WD_BLACK", "line": "SN8100", "nand": "BiCS8", "capacity_gb": 1000, "tier": "flagship"},
    "WD_BLACK_SN8100_2TB":  {"cat": "internal_ssd", "brand": "WD_BLACK", "line": "SN8100", "nand": "BiCS8", "capacity_gb": 2000, "tier": "flagship"},
    "WD_BLACK_SN8100_4TB":  {"cat": "internal_ssd", "brand": "WD_BLACK", "line": "SN8100", "nand": "BiCS8", "capacity_gb": 4000, "tier": "flagship"},
    # SN850X — BiCS6 현행 플래그십
    "WD_BLACK_SN850X_1TB":  {"cat": "internal_ssd", "brand": "WD_BLACK", "line": "SN850X", "nand": "BiCS6", "capacity_gb": 1000, "tier": "flagship"},
    "WD_BLACK_SN850X_2TB":  {"cat": "internal_ssd", "brand": "WD_BLACK", "line": "SN850X", "nand": "BiCS6", "capacity_gb": 2000, "tier": "flagship"},
    "WD_BLACK_SN850X_4TB":  {"cat": "internal_ssd", "brand": "WD_BLACK", "line": "SN850X", "nand": "BiCS6", "capacity_gb": 4000, "tier": "flagship"},
    # SN7100 — BiCS8 미드레인지 (신규)
    "WD_BLACK_SN7100_1TB":  {"cat": "internal_ssd", "brand": "WD_BLACK", "line": "SN7100", "nand": "BiCS8", "capacity_gb": 1000, "tier": "midrange"},
    "WD_BLACK_SN7100_2TB":  {"cat": "internal_ssd", "brand": "WD_BLACK", "line": "SN7100", "nand": "BiCS8", "capacity_gb": 2000, "tier": "midrange"},
    # SN770 — BiCS5 미드레인지 (현행)
    "WD_BLACK_SN770_1TB":   {"cat": "internal_ssd", "brand": "WD_BLACK", "line": "SN770",  "nand": "BiCS5", "capacity_gb": 1000, "tier": "midrange"},
    "WD_BLACK_SN770_2TB":   {"cat": "internal_ssd", "brand": "WD_BLACK", "line": "SN770",  "nand": "BiCS5", "capacity_gb": 2000, "tier": "midrange"},

    # ── External SSD ────────────────────────────────────────────
    # Extreme Pro — BiCS8 프리미엄
    "SD_EXTREME_PRO_1TB":   {"cat": "external_ssd", "brand": "SanDisk", "line": "Extreme Pro", "nand": "BiCS8", "capacity_gb": 1000, "tier": "premium"},
    "SD_EXTREME_PRO_2TB":   {"cat": "external_ssd", "brand": "SanDisk", "line": "Extreme Pro", "nand": "BiCS8", "capacity_gb": 2000, "tier": "premium"},
    "SD_EXTREME_PRO_4TB":   {"cat": "external_ssd", "brand": "SanDisk", "line": "Extreme Pro", "nand": "BiCS8", "capacity_gb": 4000, "tier": "premium"},
    # Extreme — BiCS6 메인스트림
    "SD_EXTREME_1TB":       {"cat": "external_ssd", "brand": "SanDisk", "line": "Extreme",     "nand": "BiCS6", "capacity_gb": 1000, "tier": "mainstream"},
    "SD_EXTREME_2TB":       {"cat": "external_ssd", "brand": "SanDisk", "line": "Extreme",     "nand": "BiCS6", "capacity_gb": 2000, "tier": "mainstream"},
    "SD_EXTREME_4TB":       {"cat": "external_ssd", "brand": "SanDisk", "line": "Extreme",     "nand": "BiCS6", "capacity_gb": 4000, "tier": "mainstream"},
    # My Passport — WD 보급형
    "WD_MY_PASSPORT_1TB":   {"cat": "external_ssd", "brand": "WD",      "line": "My Passport",  "nand": "BiCS5", "capacity_gb": 1000, "tier": "value"},
    "WD_MY_PASSPORT_2TB":   {"cat": "external_ssd", "brand": "WD",      "line": "My Passport",  "nand": "BiCS5", "capacity_gb": 2000, "tier": "value"},

    # ── microSD ─────────────────────────────────────────────────
    # Extreme Pro — 최고급
    "SD_PRO_PLUS_MICRO_256G": {"cat": "microsd", "brand": "SanDisk", "line": "Extreme Pro", "nand": "BiCS6", "capacity_gb": 256, "tier": "premium"},
    "SD_PRO_PLUS_MICRO_512G": {"cat": "microsd", "brand": "SanDisk", "line": "Extreme Pro", "nand": "BiCS6", "capacity_gb": 512, "tier": "premium"},
    # Extreme — 고급 (저용량 강세)
    "SD_EXTREME_MICRO_128G":  {"cat": "microsd", "brand": "SanDisk", "line": "Extreme",     "nand": "BiCS5", "capacity_gb": 128, "tier": "mainstream"},
    "SD_EXTREME_MICRO_256G":  {"cat": "microsd", "brand": "SanDisk", "line": "Extreme",     "nand": "BiCS5", "capacity_gb": 256, "tier": "mainstream"},
    "SD_EXTREME_MICRO_512G":  {"cat": "microsd", "brand": "SanDisk", "line": "Extreme",     "nand": "BiCS5", "capacity_gb": 512, "tier": "mainstream"},
    "SD_EXTREME_MICRO_1TB":   {"cat": "microsd", "brand": "SanDisk", "line": "Extreme",     "nand": "BiCS6", "capacity_gb": 1000, "tier": "mainstream"},
    # Ultra — 보급형 (저용량 최강세)
    "SD_ULTRA_MICRO_128G":    {"cat": "microsd", "brand": "SanDisk", "line": "Ultra",       "nand": "BiCS5", "capacity_gb": 128, "tier": "value"},
    "SD_ULTRA_MICRO_256G":    {"cat": "microsd", "brand": "SanDisk", "line": "Ultra",       "nand": "BiCS5", "capacity_gb": 256, "tier": "value"},
    "SD_ULTRA_MICRO_512G":    {"cat": "microsd", "brand": "SanDisk", "line": "Ultra",       "nand": "BiCS5", "capacity_gb": 512, "tier": "value"},
}

# ── 제품 라인별 그룹 (리포트/PPT용) ────────────────────────────────
PRODUCT_LINES = {
    "internal_ssd": ["SN8100", "SN850X", "SN7100", "SN770"],
    "external_ssd": ["Extreme Pro", "Extreme", "My Passport"],
    "microsd":      ["Extreme Pro", "Extreme", "Ultra"],
}

# ── 저용량 선호 시장 시그널 (용량별 수요 가중치) ───────────────────
# 값이 클수록 현재 시장에서 잘 팔림 (NAND 가격 상승 시 저용량 선호)
CAPACITY_DEMAND_WEIGHT = {
    128:  1.35,   # 저용량 강세
    256:  1.20,
    512:  1.00,   # 기준
    1000: 0.85,
    2000: 0.65,
    4000: 0.40,
}

# ── NAND 원가 (BiCS 세대별 $/GB — 2025 추정) ──────────────────
NAND_COST_PER_GB = {
    "BiCS5": 0.055,   # 112L TLC — 성숙 공정
    "BiCS6": 0.042,   # 162L TLC — 주력 공정
    "BiCS8": 0.038,   # 218L TLC — 최신 공정 (낮은 원가)
}

# ── 지역 ───────────────────────────────────────────────────────
REGIONS = ["NA", "EMEA", "APAC", "Japan", "China"]

# ── 채널 ───────────────────────────────────────────────────────
CHANNELS = ["E-commerce", "Retail", "B2B/Corporate"]

# ── 분기 ───────────────────────────────────────────────────────
QUARTERS = ["2025Q1", "2025Q2", "2025Q3", "2025Q4",
            "2026Q1", "2026Q2", "2026Q3", "2026Q4"]

# ── 에이전트 팀 ────────────────────────────────────────────────
AGENTS = {
    "production":    "생산 에이전트 — BiCS NAND capa 관리, 제품별 생산량 할당",
    "supply":        "공급 에이전트 — 재고 관리, 채널별 공급 계획, SCM",
    "demand_fc":     "수요예측 에이전트 — TAM/SAM 분석, 분기별 수요 예측",
    "mkt_strategy":  "마케팅 전략 에이전트 — 제품 mix, 가격전략, P&L",
    "marcom":        "마케팅 커뮤니케이션 에이전트 — 광고, 캠페인, 브랜드 awareness",
}
