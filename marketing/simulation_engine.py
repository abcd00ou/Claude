"""
Marketing Simulation Engine
6시간 = 1개월 시뮬레이션

- sim_state.json에 현재 시뮬레이션 상태 저장
- 6시간마다 1개월 전진 (이전 실행 후 6시간 미만이면 스킵)
- 실시간 NAND 시장 데이터(market_intel.py)로 파라미터 보정
- 계절성 + 성장 트렌드 + 시장 조건 + 노이즈로 더미 데이터 생성
- internal_sales.json 업데이트 (에이전트들이 참조)
"""
import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# ── 시뮬 시간 설정 ───────────────────────────────────────────────
HOURS_PER_SIM_MONTH = 6  # 실제 6시간 = 시뮬 1개월

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
SIM_STATE_FILE = DATA_DIR / "sim_state.json"
SALES_FILE = DATA_DIR / "internal_sales.json"

# ── 월별 계절 지수 ──────────────────────────────────────────────
SEASONAL_INDEX = {
    1: 0.82,  2: 0.85,  3: 0.92,   # Q1 (낮은 시즌)
    4: 0.95,  5: 0.97,  6: 0.98,   # Q2
    7: 1.00,  8: 1.08,  9: 1.12,   # Q3 (BTS)
    10: 1.18, 11: 1.32, 12: 1.48,  # Q4 (홀리데이)
}

QUARTER_MAP = {
    1: "Q1", 2: "Q1", 3: "Q1",
    4: "Q2", 5: "Q2", 6: "Q2",
    7: "Q3", 8: "Q3", 9: "Q3",
    10: "Q4", 11: "Q4", 12: "Q4",
}

# ── 베이스라인 (2024 연간 → 월 환산) ─────────────────────────────
BASE_MONTHLY_REV = {
    "external_ssd": 950 / 12,   # $79.2M/월
    "internal_ssd": 760 / 12,   # $63.3M/월
    "microsd":     1520 / 12,   # $126.7M/월
}

BASE_GM = {
    "external_ssd": 44.8,
    "internal_ssd": 38.5,
    "microsd":      57.3,
}

# 카테고리별 연간 성장률 (CAGR)
ANNUAL_GROWTH = {
    "external_ssd": 0.091,
    "internal_ssd": 0.161,
    "microsd":      0.059,
}

# NAND 원가 (분기당 ~4% 하락 트렌드 = 기회)
BASE_NAND_COST = {
    "BiCS5": 0.055,
    "BiCS6": 0.042,
    "BiCS8": 0.038,
}

# ── SKU 기준 데이터 (2024 연간 $M, ASP $, GM%, 용량 GB) ──────────────────
_CAP_WEIGHT = {128: 1.35, 256: 1.20, 512: 1.00, 1000: 0.85, 2000: 0.65, 4000: 0.40}

SKU_META = {
    # Internal SSD — WD_BLACK
    "WD_BLACK_SN8100_1TB":    ("internal_ssd", 120,  84.9, 55.2, 1000, "SN8100"),
    "WD_BLACK_SN8100_2TB":    ("internal_ssd", 140, 149.9, 53.1, 2000, "SN8100"),
    "WD_BLACK_SN8100_4TB":    ("internal_ssd",  75, 279.9, 51.8, 4000, "SN8100"),
    "WD_BLACK_SN850X_1TB":    ("internal_ssd", 162,  77.1, 42.8, 1000, "SN850X"),
    "WD_BLACK_SN850X_2TB":    ("internal_ssd", 194, 140.6, 45.2, 2000, "SN850X"),
    "WD_BLACK_SN850X_4TB":    ("internal_ssd",  98, 266.3, 47.1, 4000, "SN850X"),
    "WD_BLACK_SN7100_1TB":    ("internal_ssd",  95,  54.9, 38.5, 1000, "SN7100"),
    "WD_BLACK_SN7100_2TB":    ("internal_ssd",  72,  94.9, 37.2, 2000, "SN7100"),
    "WD_BLACK_SN770_1TB":     ("internal_ssd", 138,  61.6, 34.5, 1000, "SN770"),
    "WD_BLACK_SN770_2TB":     ("internal_ssd", 110, 107.8, 36.2, 2000, "SN770"),
    # External SSD — SanDisk
    "SD_EXTREME_PRO_1TB":     ("external_ssd", 148, 119.4, 52.3, 1000, "Extreme Pro"),
    "SD_EXTREME_PRO_2TB":     ("external_ssd", 137, 201.5, 54.7, 2000, "Extreme Pro"),
    "SD_EXTREME_PRO_4TB":     ("external_ssd",  62, 329.9, 57.2, 4000, "Extreme Pro"),
    "SD_EXTREME_1TB":         ("external_ssd", 215,  86.0, 45.2, 1000, "Extreme"),
    "SD_EXTREME_2TB":         ("external_ssd", 198, 154.7, 46.1, 2000, "Extreme"),
    "SD_EXTREME_4TB":         ("external_ssd",  88, 303.4, 49.8, 4000, "Extreme"),
    "WD_MY_PASSPORT_1TB":     ("external_ssd", 106,  71.6, 38.2, 1000, "My Passport"),
    "WD_MY_PASSPORT_2TB":     ("external_ssd",  58, 123.4, 40.1, 2000, "My Passport"),
    # microSD — SanDisk
    "SD_PRO_PLUS_MICRO_256G": ("microsd", 195,  33.6, 63.2,  256, "Extreme Pro"),
    "SD_PRO_PLUS_MICRO_512G": ("microsd", 165,  57.7, 64.8,  512, "Extreme Pro"),
    "SD_EXTREME_MICRO_128G":  ("microsd", 142,  22.5, 56.3,  128, "Extreme"),
    "SD_EXTREME_MICRO_256G":  ("microsd", 378,  25.5, 58.4,  256, "Extreme"),
    "SD_EXTREME_MICRO_512G":  ("microsd", 312,  43.3, 62.1,  512, "Extreme"),
    "SD_EXTREME_MICRO_1TB":   ("microsd",  39,  90.7, 65.2, 1000, "Extreme"),
    "SD_ULTRA_MICRO_128G":    ("microsd", 182,  11.5, 48.7,  128, "Ultra"),
    "SD_ULTRA_MICRO_256G":    ("microsd", 248,  18.8, 52.3,  256, "Ultra"),
    "SD_ULTRA_MICRO_512G":    ("microsd", 180,  32.5, 55.1,  512, "Ultra"),
}

# 카테고리별 라인 순서 (이메일 표 정렬용)
SKU_LINE_ORDER = {
    "internal_ssd": ["SN8100", "SN850X", "SN7100", "SN770"],
    "external_ssd": ["Extreme Pro", "Extreme", "My Passport"],
    "microsd":      ["Extreme Pro", "Extreme", "Ultra"],
}

# 카테고리 베이스 GM (SKU GM 조정 기준)
_CAT_BASE_GM = {"internal_ssd": 38.5, "external_ssd": 44.8, "microsd": 57.3}


def _generate_sku_breakdown(cat_rev: dict, cat_gm: dict,
                             months_elapsed: int, nand_signal: str) -> dict:
    """카테고리 총 매출을 SKU별로 배분. NAND 시그널 반영."""
    def cap_weight(cap_gb: int) -> float:
        base = _CAP_WEIGHT.get(cap_gb, 1.0)
        if nand_signal == "tight":
            if cap_gb <= 256:    return base * 1.20
            elif cap_gb >= 2000: return base * 0.85
        elif nand_signal == "loose":
            if cap_gb <= 256:    return base * 0.93
            elif cap_gb >= 2000: return base * 1.12
        return base

    # 카테고리별 SKU 그룹화
    cat_skus: dict = {}
    for sku, meta in SKU_META.items():
        cat_skus.setdefault(meta[0], []).append(sku)

    result = {}
    for cat, skus in cat_skus.items():
        total_monthly = cat_rev.get(cat, 0)
        cat_gm_val    = cat_gm.get(cat, _CAT_BASE_GM.get(cat, 44.0))

        # 가중치: 기준 연매출 × 용량 수요 가중치 × 제품 성숙도
        weights = {}
        for sku in skus:
            meta = SKU_META[sku]
            base_rev, cap, line = meta[1], meta[4], meta[5]
            # 신제품(SN8100/SN7100) 성장, 기존(SN850X/SN770) 점진 하락
            if line in ("SN8100", "SN7100"):
                maturity = 1 + months_elapsed * 0.015
            elif line in ("SN850X", "SN770"):
                maturity = max(0.70, 1 - months_elapsed * 0.010)
            else:
                maturity = 1.0
            weights[sku] = base_rev * cap_weight(cap) * maturity

        total_w = sum(weights.values()) or 1.0

        for sku in skus:
            meta = SKU_META[sku]
            _, base_rev, asp, base_gm, cap, line = meta
            share      = weights[sku] / total_w
            rev_m      = round(total_monthly * share, 2)
            units_k    = round(rev_m * 1000 / asp, 1) if asp > 0 else 0
            gm_delta   = cat_gm_val - _CAT_BASE_GM.get(cat, 44.0)
            sku_gm     = round(base_gm + gm_delta * 0.8, 1)
            result[sku] = {
                "rev_m":   rev_m,
                "units_k": units_k,
                "asp":     asp,
                "gm_pct":  sku_gm,
                "cap_gb":  cap,
                "line":    line,
                "cat":     cat,
            }

    return result


# 경쟁 이벤트 확률
EVENTS = [
    ("competitor_price_cut",  0.15, "SanDisk 경쟁사 가격 인하 — 대응 필요"),
    ("nand_cost_spike",       0.08, "NAND 원가 급등 (공급 이슈)"),
    ("market_share_gain",     0.20, "시장 점유율 +0.5%p 상승"),
    ("promo_opportunity",     0.25, "프로모션 기회 (예상 ROI 2.8×)"),
    ("supply_constraint",     0.10, "공급 제약 — 재고 주의"),
    ("none",                  0.22, ""),
]


def _load_state() -> dict:
    """현재 시뮬레이션 상태 로드 (없으면 초기화)."""
    if SIM_STATE_FILE.exists():
        with open(SIM_STATE_FILE) as f:
            return json.load(f)

    # 초기 상태 — 2025년 1월부터 시작
    state = {
        "sim_month": 0,
        "sim_year": 2025,
        "sim_month_num": 1,
        "start_year": 2025,
        "start_month": 1,
        "last_run_real": None,
        "history": [],
    }
    _save_state(state)
    return state


def _save_state(state: dict):
    DATA_DIR.mkdir(exist_ok=True)
    with open(SIM_STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def _months_since_start(state: dict) -> int:
    return state["sim_month"]


def _generate_monthly_data(state: dict, noise_seed: int = None,
                            market_intel: dict = None) -> dict:
    """현재 시뮬 월의 더미 데이터 생성 (실시간 NAND 시장 데이터 반영)."""
    if noise_seed is not None:
        random.seed(noise_seed)

    year = state["sim_year"]
    month = state["sim_month_num"]
    months_elapsed = state["sim_month"]  # 2025-01 기준 경과 월수

    seasonal = SEASONAL_INDEX[month]
    quarter = QUARTER_MAP[month]

    # 시장 인텔 보정값 추출 (기본값 먼저 설정 후 실시간 데이터로 덮어씀)
    adj: dict = {}
    market_context: str = "시장 데이터 미적용"
    nand_signal: str = "neutral"
    price_trend: str = "flat"
    supply_risk: float = 0.10

    if market_intel:
        adj = market_intel.get("sim_adjustments", {})
        market_context = market_intel.get("market_context", market_context)
        nand_signal = market_intel.get("nand_signal", nand_signal)
        price_trend  = market_intel.get("price_trend", price_trend)
        supply_risk  = adj.get("supply_risk", supply_risk)

    nand_cost_delta_pct = adj.get("nand_cost_delta_pct", -2.0) / 100
    demand_delta_pct    = adj.get("demand_delta_pct", 0.0) / 100

    rev = {}
    gm = {}

    for cat, base in BASE_MONTHLY_REV.items():
        # 성장률 (월 환산 CAGR)
        monthly_growth = (1 + ANNUAL_GROWTH[cat]) ** (months_elapsed / 12)
        # 계절 + 시장 수요 보정 + 노이즈 (±4%)
        noise = 1 + random.gauss(0, 0.04)
        market_demand_adj = 1 + demand_delta_pct
        monthly_rev = base * monthly_growth * seasonal * market_demand_adj * noise
        rev[cat] = round(monthly_rev, 1)

        # GM: NAND 원가 하락으로 분기당 0.3%p 기본 개선
        # + 실시간 시장 반영 (공급 과잉 → 추가 원가 하락 기회)
        gm_base_delta = (months_elapsed // 3) * 0.3
        market_gm_delta = abs(nand_cost_delta_pct) * 100 * 0.6  # 원가 절감의 60% GM 반영
        if price_trend == "up":
            market_gm_delta = -market_gm_delta * 0.5  # 가격 상승 시 GM 일부 압박
        gm_noise = random.gauss(0, 0.5)
        gm[cat] = round(BASE_GM[cat] + gm_base_delta + market_gm_delta + gm_noise, 1)

    # NAND 원가: 기본 분기당 4% 하락 + 시장 실정 반영
    quarters_elapsed = months_elapsed // 3
    base_decay = 0.96 ** quarters_elapsed
    market_nand_adj = 1 + nand_cost_delta_pct  # 실시간 시장 반영
    nand_costs = {
        gen: round(cost * base_decay * market_nand_adj, 4)
        for gen, cost in BASE_NAND_COST.items()
    }

    # 시장 점유율 (완만한 상승)
    mshare = {
        "external_ssd": round(22 + months_elapsed * 0.05 + random.gauss(0, 0.2), 1),
        "internal_ssd": round(17 + months_elapsed * 0.06 + random.gauss(0, 0.2), 1),
        "microsd":      round(32 + months_elapsed * 0.04 + random.gauss(0, 0.2), 1),
    }
    mshare = {k: min(v, 45) for k, v in mshare.items()}  # 45% cap

    # 랜덤 이벤트
    event_roll = random.random()
    cumulative = 0
    event = EVENTS[-1]
    for ev in EVENTS:
        cumulative += ev[1]
        if event_roll < cumulative:
            event = ev
            break

    # 채널 믹스 (점진적 이커머스 전환)
    ecomm_shift = months_elapsed * 0.15
    channel_mix = {
        "external_ssd": {
            "ecommerce": round(52 + ecomm_shift, 1),
            "retail":    round(38 - ecomm_shift * 0.7, 1),
            "b2b":       round(10 - ecomm_shift * 0.3, 1),
        },
        "internal_ssd": {
            "ecommerce": round(58 + ecomm_shift, 1),
            "retail":    round(27 - ecomm_shift * 0.7, 1),
            "b2b":       round(15 - ecomm_shift * 0.3, 1),
        },
        "microsd": {
            "ecommerce": round(42 + ecomm_shift, 1),
            "retail":    round(48 - ecomm_shift * 0.7, 1),
            "b2b":       round(10 - ecomm_shift * 0.3, 1),
        },
    }

    # 프로모 성과
    promo = None
    if month in [11, 12]:  # 홀리데이
        invest = round(random.uniform(38, 55), 1)
        roi = round(random.uniform(2.8, 3.4), 2)
        promo = {"invest_m": invest, "incremental_rev_m": round(invest * roi, 1), "roi": roi, "type": "holiday"}
    elif month in [7, 8]:  # BTS
        invest = round(random.uniform(14, 22), 1)
        roi = round(random.uniform(2.5, 3.1), 2)
        promo = {"invest_m": invest, "incremental_rev_m": round(invest * roi, 1), "roi": roi, "type": "bts"}

    # SKU 세분화 (제품 라인 × 용량별 배분)
    sku_rev = _generate_sku_breakdown(rev, gm, months_elapsed, nand_signal)

    return {
        "sim_date": f"{year}-{month:02d}",
        "sim_year": year,
        "sim_month": month,
        "quarter": f"{year}{quarter}",
        "real_time": datetime.now().isoformat(),
        "revenue_m": rev,
        "total_rev_m": round(sum(rev.values()), 1),
        "gross_margin_pct": gm,
        "blended_gm_pct": round(
            sum(rev[c] * gm[c] for c in rev) / sum(rev.values()) if sum(rev.values()) > 0 else 0, 1
        ),
        "market_share_pct": mshare,
        "nand_cost_per_gb": nand_costs,
        "channel_mix_pct": channel_mix,
        "event": {"type": event[0], "description": event[2]},
        "promo": promo,
        "sku_revenue": sku_rev,
        # 시장 인텔 메타데이터
        "market_intel": {
            "nand_signal": nand_signal,
            "price_trend": price_trend,
            "supply_risk": supply_risk,
            "market_context": market_context,
            "nand_cost_delta_pct": round(nand_cost_delta_pct * 100, 2),
            "demand_delta_pct": round(demand_delta_pct * 100, 2),
        },
    }


def _update_sales_json(state: dict, latest: dict):
    """internal_sales.json을 최신 시뮬 데이터로 업데이트."""
    with open(SALES_FILE) as f:
        sales = json.load(f)

    # 분기별 매출 업데이트 (최근 2분기)
    quarter_key = latest["quarter"]
    sales.setdefault("quarterly_revenue_usd_m", {})
    # 해당 분기 누적 (월 → 분기 환산: ×3 approximation)
    existing = sales["quarterly_revenue_usd_m"].get(quarter_key, {})
    if existing:
        # 기존 분기 데이터에 합산 (동일 분기 3회 누적)
        for cat in ["external_ssd", "internal_ssd", "microsd"]:
            existing[cat] = round(existing.get(cat, 0) * 0.7 + latest["revenue_m"][cat] * 3 * 0.3, 1)
        existing["total"] = round(sum(existing[c] for c in ["external_ssd", "internal_ssd", "microsd"]), 1)
    else:
        # 신규 분기: 월 × 3
        sales["quarterly_revenue_usd_m"][quarter_key] = {
            cat: round(latest["revenue_m"][cat] * 3, 1)
            for cat in ["external_ssd", "internal_ssd", "microsd"]
        }
        sales["quarterly_revenue_usd_m"][quarter_key]["total"] = round(
            sum(latest["revenue_m"][cat] * 3 for cat in ["external_ssd", "internal_ssd", "microsd"]), 1
        )

    # 연간 매출 추정 업데이트
    year_key = str(latest["sim_year"]) + "E"
    annual_monthly_avg = {
        cat: sum(
            h["revenue_m"][cat] for h in state["history"]
            if h.get("sim_year") == latest["sim_year"]
        ) / max(1, len([h for h in state["history"] if h.get("sim_year") == latest["sim_year"]]))
        for cat in ["external_ssd", "internal_ssd", "microsd"]
    }
    if annual_monthly_avg["external_ssd"] > 0:
        sales["annual_revenue_usd_m"][year_key] = {
            cat: round(v * 12, 0)
            for cat, v in annual_monthly_avg.items()
        }
        sales["annual_revenue_usd_m"][year_key]["total_btoc"] = round(
            sum(sales["annual_revenue_usd_m"][year_key][c] for c in annual_monthly_avg), 0
        )

    # GM 업데이트
    year_str = str(latest["sim_year"]) + "E"
    sales.setdefault("gross_margin_pct", {})
    sales["gross_margin_pct"][year_str] = {
        **latest["gross_margin_pct"],
        "blended": latest["blended_gm_pct"],
    }

    # 시장 점유율 업데이트
    sales["market_share_pct"][f"{latest['sim_year']}_latest"] = latest["market_share_pct"]

    # NAND 원가 업데이트
    nand_key = f"{latest['sim_year']}Q{(latest['sim_month'] - 1) // 3 + 1}_sim"
    # 블렌딩 비율 가중치로 단일 $/GB 계산
    blended_nand = round(
        latest["nand_cost_per_gb"]["BiCS5"] * 0.3 +
        latest["nand_cost_per_gb"]["BiCS6"] * 0.5 +
        latest["nand_cost_per_gb"]["BiCS8"] * 0.2, 4
    )
    sales["nand_cost_per_gb_usd"][nand_key] = blended_nand

    # 채널 믹스 업데이트
    sales["channel_mix_pct"][year_str] = latest["channel_mix_pct"]

    # 프로모 업데이트
    if latest["promo"]:
        promo_key = f"{latest['sim_date']}_{latest['promo']['type']}"
        sales["promo_impact_usd_m"][promo_key] = {
            "invest": latest["promo"]["invest_m"],
            "incremental_rev": latest["promo"]["incremental_rev_m"],
            "roi": latest["promo"]["roi"],
        }

    sales["_sim_last_updated"] = latest["real_time"]
    sales["_sim_date"] = latest["sim_date"]

    with open(SALES_FILE, "w") as f:
        json.dump(sales, f, indent=2, ensure_ascii=False)


def advance_month(market_intel: dict = None) -> dict:
    """
    시뮬레이션 1개월 전진.
    market_intel: market_intel.py fetch_market_intel() 반환값 (실시간 NAND 시장 데이터)
    반환: 이번 달 시뮬 데이터 dict (스킵 시 최신 히스토리 반환)
    """
    state = _load_state()

    # ── 6시간 게이트: 마지막 실행 후 HOURS_PER_SIM_MONTH시간 미만이면 스킵 ──
    last_run = state.get("last_run_real")
    if last_run:
        elapsed = datetime.now() - datetime.fromisoformat(last_run)
        if elapsed < timedelta(hours=HOURS_PER_SIM_MONTH):
            remaining = timedelta(hours=HOURS_PER_SIM_MONTH) - elapsed
            hours_left = int(remaining.total_seconds() // 3600)
            mins_left = int((remaining.total_seconds() % 3600) // 60)
            print(f"  [Sim] ⏭  스킵 — 다음 실행까지 {hours_left}h {mins_left}m 남음 "
                  f"(마지막: {last_run[:16]})")
            # 최신 히스토리 반환 (없으면 None)
            return state["history"][-1] if state.get("history") else None

    # 다음 달로 이동
    state["sim_month"] += 1
    month = state["sim_month_num"] + 1
    year = state["sim_year"]
    if month > 12:
        month = 1
        year += 1
    state["sim_month_num"] = month
    state["sim_year"] = year
    state["last_run_real"] = datetime.now().isoformat()

    # 데이터 생성 (실시간 시장 데이터 반영)
    latest = _generate_monthly_data(state, noise_seed=state["sim_month"],
                                    market_intel=market_intel)

    # 히스토리 추가 (중복 sim_date 제거 후 최근 24개월만 보관)
    state["history"] = [h for h in state["history"] if h.get("sim_date") != latest["sim_date"]]
    state["history"].append(latest)
    if len(state["history"]) > 24:
        state["history"] = state["history"][-24:]

    # 상태 저장 + sales.json 업데이트
    _save_state(state)
    _update_sales_json(state, latest)

    print(f"  [Sim] {latest['sim_date']} 시뮬 완료 | Rev ${latest['total_rev_m']:.1f}M | "
          f"GM {latest['blended_gm_pct']:.1f}% | Event: {latest['event']['type']}")
    return latest


def get_current_state() -> dict:
    return _load_state()


def get_history_df():
    """히스토리를 pandas DataFrame으로 반환."""
    import pandas as pd
    state = _load_state()
    rows = []
    for h in state["history"]:
        row = {
            "sim_date": h["sim_date"],
            "total_rev_m": h["total_rev_m"],
            "blended_gm_pct": h["blended_gm_pct"],
        }
        for cat in ["external_ssd", "internal_ssd", "microsd"]:
            row[f"rev_{cat}"] = h["revenue_m"].get(cat, 0)
            row[f"gm_{cat}"] = h["gross_margin_pct"].get(cat, 0)
        for k, v in h["market_share_pct"].items():
            row[f"mshare_{k}"] = v
        rows.append(row)
    return pd.DataFrame(rows)


if __name__ == "__main__":
    data = advance_month()
    print(json.dumps(data, indent=2, ensure_ascii=False))
