"""
Market Intelligence Module — NAND 시장 실시간 데이터 수집
매 시뮬레이션 실행 시 호출:
  1. DuckDuckGo로 NAND 가격/공급 뉴스 검색
  2. TrendForce 공개 페이지 스크래핑 시도
  3. 결과를 data/market_intel.json에 저장
  4. 시뮬레이션 파라미터 조정값 반환

반환 구조:
{
  "fetched_at": "2026-03-10T09:00:00",
  "nand_signal": "tight" | "loose" | "neutral",   # 공급 상황
  "price_trend": "up" | "down" | "flat",           # 가격 방향
  "price_change_pct": -3.2,                        # 전월 대비 추정 변화율
  "headlines": [...],                               # 수집된 뉴스 헤드라인
  "key_insights": [...],                            # 파싱된 핵심 인사이트
  "sim_adjustments": {                             # 시뮬레이션 보정값
      "nand_cost_delta_pct": -2.1,
      "demand_delta_pct": 1.5,
      "supply_risk": 0.15,
  },
  "source": "web" | "cache" | "default"
}
"""
import json
import re
import time
from datetime import datetime, timedelta
from pathlib import Path

import requests

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
INTEL_FILE = DATA_DIR / "market_intel.json"
CACHE_TTL_HOURS = 6  # 6시간 캐시

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# ── 키워드 시그널 분류 ─────────────────────────────────────────
POSITIVE_SUPPLY_KEYWORDS = [
    "oversupply", "glut", "excess inventory", "price decline", "price drop",
    "falling prices", "inventory buildup", "weak demand", "soft demand",
    "price war", "aggressive pricing", "undersupply easing",
]
NEGATIVE_SUPPLY_KEYWORDS = [
    "undersupply", "shortage", "tight supply", "supply constraint",
    "price increase", "price surge", "price hike", "supply cut",
    "production cut", "fab shutdown", "wafer shortage", "capacity cut",
    "surging demand", "strong demand",
]
PRICE_UP_KEYWORDS = [
    "price increase", "price surge", "price hike", "rising prices",
    "higher prices", "price recovery", "price rebound", "spot price up",
]
PRICE_DOWN_KEYWORDS = [
    "price decline", "price drop", "price fall", "lower prices",
    "falling prices", "price decrease", "spot price down", "price cut",
]


def _score_text(text: str, pos_kw: list, neg_kw: list) -> float:
    """텍스트에서 긍/부정 시그널 점수 추출. 양수=positive, 음수=negative."""
    t = text.lower()
    score = 0
    for kw in pos_kw:
        if kw in t:
            score += 1
    for kw in neg_kw:
        if kw in t:
            score -= 1
    return score


def _fetch_duckduckgo(query: str, max_results: int = 8) -> list[dict]:
    """DuckDuckGo 검색 결과 헤드라인 수집."""
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.news(query, max_results=max_results, timelimit="m"))  # 한 달 이내
        return [{"title": r.get("title",""), "body": r.get("body",""),
                 "url": r.get("url",""), "date": r.get("date","")} for r in results]
    except Exception as e:
        print(f"  [Intel] DuckDuckGo 검색 실패: {e}")
        return []


def _fetch_trendforce_summary() -> str:
    """TrendForce NAND 시장 요약 페이지 텍스트 추출."""
    url = "https://www.trendforce.com/news/category/dram-and-storage/"
    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code == 200:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(r.text, "html.parser")
            # 헤드라인 추출
            headlines = []
            for el in soup.select("h2, h3, .post-title, .entry-title, article h2"):
                txt = el.get_text(strip=True)
                if txt and len(txt) > 20:
                    headlines.append(txt)
            return " | ".join(headlines[:10])
    except Exception:
        pass
    return ""


def _fetch_anandtech_or_techpowerup() -> str:
    """SSD/NAND 뉴스에서 텍스트 추출."""
    urls = [
        "https://www.tomshardware.com/best-picks/ssd-price-index",
        "https://www.techpowerup.com/cat/storage/",
    ]
    for url in urls:
        try:
            r = requests.get(url, headers=HEADERS, timeout=8)
            if r.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(r.text, "html.parser")
                texts = []
                for el in soup.select("h1, h2, h3, p"):
                    txt = el.get_text(strip=True)
                    if "NAND" in txt or "SSD" in txt or "flash" in txt.lower() or "price" in txt.lower():
                        texts.append(txt)
                if texts:
                    return " ".join(texts[:15])
        except Exception:
            pass
    return ""


def _extract_price_change_pct(texts: list[str]) -> float | None:
    """텍스트에서 가격 변화율 숫자 추출 (예: 'fell 5%', 'up 3.2%')."""
    combined = " ".join(texts)
    # 패턴: "fell/rose/up/down X%" or "X% increase/decrease"
    patterns = [
        r"(?:fell|drop(?:ped)?|declin(?:ed?)|down)\s+(?:by\s+)?(\d+\.?\d*)%",
        r"(?:rose|increas(?:ed?)|up|surged?)\s+(?:by\s+)?(\d+\.?\d*)%",
        r"(\d+\.?\d*)%\s+(?:decrease|decline|drop|fall)",
        r"(\d+\.?\d*)%\s+(?:increase|rise|surge|gain)",
    ]
    direction = None
    pct = None
    for pattern in patterns:
        m = re.search(pattern, combined, re.IGNORECASE)
        if m:
            pct = float(m.group(1))
            if any(k in pattern for k in ["fell", "drop", "declin", "down", "decrease", "decline", "fall"]):
                direction = -1
            else:
                direction = 1
            break
    if pct and direction:
        return direction * pct
    return None


def _load_cache() -> dict | None:
    """캐시가 유효하면 반환."""
    if not INTEL_FILE.exists():
        return None
    try:
        with open(INTEL_FILE) as f:
            data = json.load(f)
        fetched = datetime.fromisoformat(data.get("fetched_at", "2000-01-01"))
        if datetime.now() - fetched < timedelta(hours=CACHE_TTL_HOURS):
            return data
    except Exception:
        pass
    return None


def _default_intel() -> dict:
    """웹 수집 실패 시 보수적 기본값."""
    return {
        "fetched_at": datetime.now().isoformat(),
        "nand_signal": "neutral",
        "price_trend": "down",
        "price_change_pct": -2.0,
        "headlines": [],
        "key_insights": ["기본값 사용 (웹 수집 불가)"],
        "sim_adjustments": {
            "nand_cost_delta_pct": -2.0,
            "demand_delta_pct": 0.0,
            "supply_risk": 0.10,
        },
        "market_context": "NAND 시장 데이터 수집 불가. 기본 트렌드(완만한 가격 하락) 적용.",
        "source": "default",
    }


def fetch_market_intel(force_refresh: bool = False) -> dict:
    """
    NAND 시장 인텔리전스 수집 메인 함수.
    캐시 유효 시 캐시 반환, 아니면 웹 수집.
    """
    if not force_refresh:
        cached = _load_cache()
        if cached:
            print(f"  [Intel] 캐시 사용 ({cached.get('source','?')}) — {cached.get('fetched_at','')[:16]}")
            return cached

    print("  [Intel] NAND 시장 데이터 수집 중...")
    all_texts = []
    headlines = []

    # 1. DuckDuckGo 뉴스 검색
    queries = [
        "NAND flash memory price 2025 market",
        "NAND flash supply shortage oversupply 2025",
        "SSD storage price trend March 2026",
    ]
    for q in queries:
        results = _fetch_duckduckgo(q, max_results=5)
        for r in results:
            txt = r["title"] + " " + r.get("body", "")
            all_texts.append(txt)
            if r["title"]:
                headlines.append({"title": r["title"], "date": r.get("date",""), "url": r.get("url","")})
        time.sleep(0.5)

    # 2. TrendForce
    tf_text = _fetch_trendforce_summary()
    if tf_text:
        all_texts.append(tf_text)

    # 3. 기타 소스
    other_text = _fetch_anandtech_or_techpowerup()
    if other_text:
        all_texts.append(other_text)

    if not all_texts:
        print("  [Intel] 웹 수집 실패 — 기본값 사용")
        intel = _default_intel()
        _save_intel(intel)
        return intel

    combined = " ".join(all_texts)

    # ── 시그널 분석 ────────────────────────────────────────────
    supply_score = _score_text(combined, POSITIVE_SUPPLY_KEYWORDS, NEGATIVE_SUPPLY_KEYWORDS)
    price_score  = _score_text(combined, PRICE_DOWN_KEYWORDS, PRICE_UP_KEYWORDS)

    # 공급 상황 판단
    if supply_score >= 2:
        nand_signal = "loose"     # 공급 과잉 → 가격 하락 압력
    elif supply_score <= -2:
        nand_signal = "tight"     # 공급 부족 → 가격 상승 압력
    else:
        nand_signal = "neutral"

    # 가격 방향
    if price_score >= 1:
        price_trend = "down"
    elif price_score <= -1:
        price_trend = "up"
    else:
        price_trend = "flat"

    # 가격 변화율 추출
    extracted_pct = _extract_price_change_pct(all_texts)
    if extracted_pct is not None:
        price_change_pct = extracted_pct
    else:
        # 시그널 기반 추정
        if nand_signal == "loose":
            price_change_pct = -4.0
        elif nand_signal == "tight":
            price_change_pct = +3.5
        else:
            price_change_pct = -1.5

    # 시뮬레이션 조정값 계산
    nand_cost_delta = price_change_pct * 0.8  # 원가는 가격보다 느리게 반응
    demand_delta = -price_change_pct * 0.3    # 가격 하락 → 수요 증가
    supply_risk = 0.25 if nand_signal == "tight" else (0.08 if nand_signal == "loose" else 0.12)

    # 핵심 인사이트 추출 (NAND 언급 문장)
    insights = []
    for text in all_texts[:5]:
        sentences = text.split(".")
        for sent in sentences:
            if any(kw in sent.lower() for kw in ["nand", "flash", "ssd", "storage price", "memory price"]):
                sent = sent.strip()
                if 20 < len(sent) < 200:
                    insights.append(sent)
                    if len(insights) >= 5:
                        break
        if len(insights) >= 5:
            break

    # 시장 컨텍스트 문자열
    signal_ko = {"loose": "공급 과잉", "tight": "공급 부족", "neutral": "균형"}
    trend_ko  = {"up": "상승", "down": "하락", "flat": "보합"}
    context = (f"NAND 시장: {signal_ko[nand_signal]} | "
               f"가격 트렌드: {trend_ko[price_trend]} "
               f"(추정 {price_change_pct:+.1f}%/월) | "
               f"공급 리스크: {supply_risk*100:.0f}%")

    intel = {
        "fetched_at": datetime.now().isoformat(),
        "nand_signal": nand_signal,
        "price_trend": price_trend,
        "price_change_pct": round(price_change_pct, 2),
        "headlines": headlines[:8],
        "key_insights": insights[:5],
        "sim_adjustments": {
            "nand_cost_delta_pct": round(nand_cost_delta, 2),
            "demand_delta_pct": round(demand_delta, 2),
            "supply_risk": round(supply_risk, 3),
        },
        "market_context": context,
        "supply_score": supply_score,
        "price_score": price_score,
        "source": "web",
    }

    _save_intel(intel)
    print(f"  [Intel] ✅ 수집 완료: {nand_signal} / {price_trend} / {price_change_pct:+.1f}%")
    print(f"  [Intel] {context}")
    return intel


def _save_intel(intel: dict):
    DATA_DIR.mkdir(exist_ok=True)
    with open(INTEL_FILE, "w") as f:
        json.dump(intel, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    result = fetch_market_intel(force_refresh=True)
    print(json.dumps(result, indent=2, ensure_ascii=False))
