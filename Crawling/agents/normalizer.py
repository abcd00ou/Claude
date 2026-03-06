"""
Normalization Agent
extracted_record → 표준 PriceObservation 변환.

- 로케일 숫자 포맷 처리 ($1,299.00 / ₩159,000 / ¥12,800 / 1.299,00€)
- 통화 기호 → ISO 코드 매핑
- shipping_price 추출
- price <= 0 → normalization_warning
"""
import re
from typing import Optional

from config import COUNTRY_CURRENCY


# ── 통화 기호 → ISO 코드 ─────────────────────────────────────
CURRENCY_SYMBOLS = {
    "$":   "USD",
    "US$": "USD",
    "₩":   "KRW",
    "￦":   "KRW",
    "¥":   "JPY",
    "￥":   "JPY",
    "€":   "EUR",
    "£":   "GBP",
}

# ISO 텍스트 코드 직접 감지 (e.g. "KRW 248,129", "USD 89.99")
CURRENCY_CODES = {"USD", "KRW", "JPY", "EUR", "GBP", "CAD", "AUD", "CNY"}

# Amazon 도메인 → 기본 통화 (소스가 amazon이면 무조건 이걸로 override)
AMAZON_COUNTRY_CURRENCY = {
    "US": "USD",
    "KR": "KRW",
    "JP": "JPY",
    "DE": "EUR",
    "GB": "GBP",
}


def _detect_currency_from_string(raw: str) -> Optional[str]:
    if not raw:
        return None
    # 기호 우선
    for sym, code in CURRENCY_SYMBOLS.items():
        if sym in raw:
            return code
    # ISO 텍스트 코드 감지 (e.g. "KRW 248,129")
    upper = raw.upper()
    for code in CURRENCY_CODES:
        if code in upper:
            return code
    return None


def _clean_number(raw: str, currency: Optional[str] = None) -> Optional[float]:
    """
    '$1,299.00' → 1299.00
    '₩159,000'  → 159000.0
    '1.299,00'  → 1299.00  (EU format)
    '12,800'    → 12800.0
    """
    if not raw:
        return None

    # 기호 및 ISO 코드 제거
    s = raw.strip()
    for sym in CURRENCY_SYMBOLS:
        s = s.replace(sym, "")
    for code in CURRENCY_CODES:
        s = s.replace(code, "")
    s = s.strip()

    # EU 포맷 감지
    if re.search(r"\d\.\d{3},\d{2}$", s):
        # Case 1: 1.299,99 (점=천단위, 쉼표=소수)
        s = s.replace(".", "").replace(",", ".")
    elif currency in ("EUR", "GBP") and re.search(r"^\d{1,3},\d{2}$", s):
        # Case 2: 137,99 EUR — 천단위 없이 쉼표=소수 (€1000 미만)
        s = s.replace(",", ".")
    else:
        # US/JPY 포맷: 쉼표=천단위 (1,299.00 / 18,990)
        s = s.replace(",", "")

    # 숫자만 추출
    match = re.search(r"[\d.]+", s)
    if match:
        try:
            return float(match.group())
        except ValueError:
            return None
    return None


def _parse_shipping(raw_shipping: Optional[str]) -> Optional[float]:
    if not raw_shipping:
        return None
    text = raw_shipping.lower()
    if "free" in text or "무료" in text or "送料無料" in text:
        return 0.0
    return _clean_number(raw_shipping)


def normalize_record(record: dict) -> tuple[dict, list[str]]:
    """
    extracted_record → price_observation + warnings 리스트 반환.
    """
    warnings = []
    country  = record.get("country", "US")

    # 통화 확정 순서: raw_string → detected_currency → country 기본값
    currency = (
        _detect_currency_from_string(record.get("raw_price_string") or "") or
        record.get("detected_currency") or
        COUNTRY_CURRENCY.get(country)
    )

    price = _clean_number(record.get("raw_price_string"), currency)
    shipping = _parse_shipping(record.get("raw_shipping_string"))

    # original_price (할인 전 가격) — 파서에서 별도로 넘겨올 수도 있음
    original_price = _clean_number(record.get("raw_original_price_string"))

    if price is None:
        warnings.append(f"price_null: {record['sku_id']} {country}")
    elif price <= 0:
        warnings.append(f"price_nonpositive: {record['sku_id']} {country} price={price}")

    if currency is None:
        warnings.append(f"currency_null: {record['sku_id']} {country}")

    obs = {
        "run_id":           record.get("run_id"),
        "sku_id":           record["sku_id"],
        "country":          country,
        "source":           record["source"],
        "observed_at":      record["observed_at"],
        "price":            price,
        "currency":         currency,
        "original_price":   original_price,
        "shipping_price":   shipping,
        "availability":     record.get("availability_signal", "unknown"),
        "seller_name":      record.get("seller_name"),
        "fulfillment":      record.get("fulfillment"),
        "condition":        record.get("condition", "new"),
        "offer_scope":      record.get("offer_scope", "unknown"),
        "content_hash":     record.get("evidence", {}).get("content_hash"),
        "raw_path":         record.get("evidence", {}).get("raw_path"),
        "parse_confidence": record.get("parse_confidence", 0.0),
        "parse_notes":      record.get("parse_notes"),
    }
    return obs, warnings


def normalize_all(records: list[dict]) -> tuple[list[dict], list[str]]:
    all_obs  = []
    all_warn = []
    for rec in records:
        obs, warns = normalize_record(rec)
        all_obs.append(obs)
        all_warn.extend(warns)
    return all_obs, all_warn
