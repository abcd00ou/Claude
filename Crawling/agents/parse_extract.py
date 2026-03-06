"""
Parse & Extract Agent
HTML에서 가격 정보를 구조화하여 추출.

우선순위:
  1) JSON-LD (application/ld+json)
  2) Embedded JSON (_next_data, 제조사 SPA)
  3) DOM selector (Amazon buybox 등)
"""
import gzip
import json
import re
from typing import Optional

from bs4 import BeautifulSoup

from agents.fetch_raw import load_raw_html


# ── Amazon 파서 ──────────────────────────────────────────────

def _parse_amazon(soup: BeautifulSoup, url: str) -> dict:
    result = {
        "raw_price_string": None,
        "raw_shipping_string": None,
        "detected_currency": None,
        "availability_signal": None,
        "seller_name": None,
        "fulfillment": None,
        "condition": "new",
        "offer_scope": "unknown",
        "parse_confidence": 0.0,
        "parse_notes": None,
    }

    # ── 1) JSON-LD ───────────────────────────────────────────
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "")
            if isinstance(data, list):
                data = data[0]
            if data.get("@type") in ("Product", "Offer"):
                offers = data.get("offers", data)
                if isinstance(offers, list):
                    offers = offers[0]
                price = offers.get("price") or offers.get("lowPrice")
                currency = offers.get("priceCurrency")
                avail = offers.get("availability", "")
                if price:
                    result["raw_price_string"]  = str(price)
                    result["detected_currency"] = currency
                    result["availability_signal"] = (
                        "in_stock" if "InStock" in avail else
                        "out_of_stock" if "OutOfStock" in avail else "unknown"
                    )
                    result["offer_scope"]        = "buybox"
                    result["parse_confidence"]   = 0.9
                    return result
        except Exception:
            pass

    # ── 2) Amazon buybox DOM ─────────────────────────────────
    # 선택자를 순서대로 시도 — select_one()에 쉼표로 합치면 문서 순서로 첫 매치가 반환되어
    # 카루셀·액세서리 가격을 잘못 집는 문제 발생. 우선순위 순으로 하나씩 시도.
    _BUYBOX_SELECTORS = [
        ".apex-pricetopay-value .a-offscreen",                  # Amazon JP/US 최신 buybox (apex-pricetopay-value)
        "#corePriceDisplay_desktop_feature_div .a-offscreen",   # 메인 buybox (데스크톱)
        ".apexPriceToPay .a-offscreen",                         # 구형 apex 영역
        "#apex_desktop .a-price .a-offscreen",                  # apex 데스크톱
        "#priceblock_ourprice",                                  # 구형 레이아웃
        "#priceblock_dealprice",
        "#price_inside_buybox",
        "#buybox .a-price .a-offscreen",                        # buybox 컨테이너 안
    ]
    price_whole = None
    for _sel in _BUYBOX_SELECTORS:
        el = soup.select_one(_sel)
        # 요소가 존재하고 실제 텍스트가 있을 때만 사용 (empty span 건너뜀)
        if el and el.get_text(strip=True):
            price_whole = el
            break

    if price_whole:
        price_text = price_whole.get_text(strip=True)
        # currency symbol detection
        if price_text.startswith("$"):
            result["detected_currency"] = "USD"
        elif price_text.startswith("₩"):
            result["detected_currency"] = "KRW"
        elif price_text.startswith("¥"):
            result["detected_currency"] = "JPY"
        elif price_text.startswith("€"):
            result["detected_currency"] = "EUR"

        result["raw_price_string"]  = price_text
        result["offer_scope"]       = "buybox"
        result["parse_confidence"]  = 0.75

    # Availability (EN / JP / DE / KR 다국어 지원)
    avail_el = soup.select_one("#availability span, #outOfStock")
    if avail_el:
        av_text = avail_el.get_text(strip=True)
        av_lower = av_text.lower()
        if any(s in av_lower for s in ("in stock", "auf lager", "en stock")) \
                or "在庫あり" in av_text or "재고 있음" in av_text \
                or "通常" in av_text:   # 通常X日以内に発送 = "usually ships in X days"
            result["availability_signal"] = "in_stock"
        elif any(s in av_lower for s in ("out of stock", "nicht auf lager", "currently unavailable")) \
                or "在庫切れ" in av_text or "品切れ" in av_text or "품절" in av_text:
            result["availability_signal"] = "out_of_stock"
        else:
            result["availability_signal"] = "limited"

    # Fulfillment (FBA vs 3P)
    fulfilled_el = soup.select_one("#fulfilledByThirdParty, #SSOFulfillment")
    if fulfilled_el:
        result["fulfillment"] = "FBM"
    else:
        result["fulfillment"] = "FBA"

    # Seller
    sold_by = soup.select_one("#sellerProfileTriggerId, #merchant-info a")
    if sold_by:
        result["seller_name"] = sold_by.get_text(strip=True)

    # Shipping
    ship_el = soup.select_one("#price-shipping-message, .shipping-message")
    if ship_el:
        result["raw_shipping_string"] = ship_el.get_text(strip=True)

    if not result["raw_price_string"]:
        result["parse_notes"] = "no_price_found"
        result["parse_confidence"] = 0.0

    return result


# ── Samsung 제조사 파서 ──────────────────────────────────────

def _parse_samsung(soup: BeautifulSoup, url: str) -> dict:
    result = {
        "raw_price_string": None,
        "raw_shipping_string": None,
        "detected_currency": "USD",
        "availability_signal": None,
        "seller_name": "Samsung",
        "fulfillment": "official",
        "condition": "new",
        "offer_scope": "buybox",
        "parse_confidence": 0.0,
        "parse_notes": None,
    }

    # JSON-LD
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "")
            if isinstance(data, list):
                data = data[0]
            offers = data.get("offers", {})
            if isinstance(offers, list):
                offers = offers[0]
            price = offers.get("price")
            if price:
                result["raw_price_string"]  = str(price)
                result["detected_currency"] = offers.get("priceCurrency", "USD")
                result["parse_confidence"]  = 0.9
                return result
        except Exception:
            pass

    # DOM: .price-display, [data-price], .buy-price
    for selector in [".price-display", "[data-price]", ".buy-price", ".pdp-price"]:
        el = soup.select_one(selector)
        if el:
            result["raw_price_string"] = el.get_text(strip=True)
            result["parse_confidence"] = 0.7
            break

    if not result["raw_price_string"]:
        result["parse_notes"] = "no_price_found"

    return result


# ── WesternDigital (SanDisk) 파서 ───────────────────────────

def _parse_westerndigital(soup: BeautifulSoup, url: str) -> dict:
    result = {
        "raw_price_string": None,
        "raw_shipping_string": None,
        "detected_currency": "USD",
        "availability_signal": None,
        "seller_name": "Western Digital",
        "fulfillment": "official",
        "condition": "new",
        "offer_scope": "buybox",
        "parse_confidence": 0.0,
        "parse_notes": None,
    }

    # JSON-LD
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "")
            if isinstance(data, list):
                data = data[0]
            offers = data.get("offers", {})
            if isinstance(offers, list):
                offers = offers[0]
            price = offers.get("price")
            if price:
                result["raw_price_string"]  = str(price)
                result["detected_currency"] = offers.get("priceCurrency", "USD")
                result["parse_confidence"]  = 0.9
                return result
        except Exception:
            pass

    # __NEXT_DATA__ (Next.js)
    next_data = soup.find("script", id="__NEXT_DATA__")
    if next_data:
        try:
            nd = json.loads(next_data.string or "")
            # 경로는 WD 사이트 구조에 따라 다를 수 있음
            props = nd.get("props", {}).get("pageProps", {})
            price = (
                props.get("product", {}).get("price") or
                props.get("productData", {}).get("price")
            )
            if price:
                result["raw_price_string"] = str(price)
                result["parse_confidence"] = 0.8
                return result
        except Exception:
            pass

    # DOM fallback
    for selector in [".pricing", ".product-price", "[data-price]", ".price"]:
        el = soup.select_one(selector)
        if el:
            result["raw_price_string"] = el.get_text(strip=True)
            result["parse_confidence"] = 0.65
            break

    if not result["raw_price_string"]:
        result["parse_notes"] = "no_price_found"

    return result


# ── Lexar 파서 ───────────────────────────────────────────────

def _parse_lexar(soup: BeautifulSoup, url: str) -> dict:
    result = {
        "raw_price_string": None,
        "raw_shipping_string": None,
        "detected_currency": "USD",
        "availability_signal": None,
        "seller_name": "Lexar",
        "fulfillment": "official",
        "condition": "new",
        "offer_scope": "buybox",
        "parse_confidence": 0.0,
        "parse_notes": None,
    }

    # __NEXT_DATA__
    next_data = soup.find("script", id="__NEXT_DATA__")
    if next_data:
        try:
            nd = json.loads(next_data.string or "")
            props = nd.get("props", {}).get("pageProps", {})
            product = props.get("product", props.get("productData", {}))
            price = (
                product.get("price") or
                product.get("salePrice") or
                product.get("regularPrice")
            )
            if price:
                result["raw_price_string"] = str(price)
                result["parse_confidence"] = 0.85
                return result
        except Exception:
            pass

    # JSON-LD
    for tag in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(tag.string or "")
            if isinstance(data, list):
                data = data[0]
            offers = data.get("offers", {})
            if isinstance(offers, list):
                offers = offers[0]
            price = offers.get("price")
            if price:
                result["raw_price_string"]  = str(price)
                result["detected_currency"] = offers.get("priceCurrency", "USD")
                result["parse_confidence"]  = 0.9
                return result
        except Exception:
            pass

    # DOM
    for selector in [".price", ".product-price", "[data-price]"]:
        el = soup.select_one(selector)
        if el:
            result["raw_price_string"] = el.get_text(strip=True)
            result["parse_confidence"] = 0.6
            break

    if not result["raw_price_string"]:
        result["parse_notes"] = "no_price_found"

    return result


# ── 라우터 ───────────────────────────────────────────────────

def _select_parser(url: str):
    if "amazon." in url:
        return _parse_amazon
    if "samsung.com" in url:
        return _parse_samsung
    if "westerndigital.com" in url:
        return _parse_westerndigital
    if "lexar.com" in url:
        return _parse_lexar
    return _parse_amazon  # default


def extract_price(snapshot: dict) -> dict:
    """
    raw_snapshot dict를 받아 extracted_record dict 반환.
    raw_path에서 HTML 로드 → 파서 선택 → 추출.
    """
    base = {
        "sku_id":              snapshot["sku_id"],
        "country":             snapshot["country"],
        "source":              snapshot["source"],
        "observed_at":         snapshot["observed_at"],
        "evidence": {
            "http_status":  snapshot.get("http_status"),
            "content_hash": snapshot.get("content_hash"),
            "raw_path":     snapshot.get("raw_path"),
            "fetch_notes":  snapshot.get("fetch_notes"),
            "final_url":    snapshot.get("final_url"),
        },
    }

    # fetch 실패
    if not snapshot.get("raw_path"):
        base.update({
            "raw_price_string": None,
            "detected_currency": None,
            "raw_shipping_string": None,
            "availability_signal": None,
            "seller_name": None,
            "fulfillment": None,
            "condition": "new",
            "offer_scope": "unknown",
            "parse_confidence": 0.0,
            "parse_notes": snapshot.get("fetch_notes", "fetch_failed"),
        })
        return base

    html = load_raw_html(snapshot["raw_path"])
    if not html:
        base.update({
            "raw_price_string": None,
            "detected_currency": None,
            "raw_shipping_string": None,
            "availability_signal": None,
            "seller_name": None,
            "fulfillment": None,
            "condition": "new",
            "offer_scope": "unknown",
            "parse_confidence": 0.0,
            "parse_notes": "raw_file_unreadable",
        })
        return base

    soup = BeautifulSoup(html, "lxml")
    url  = snapshot.get("final_url") or snapshot["url"]
    parser_fn = _select_parser(url)
    parsed = parser_fn(soup, url)

    base.update(parsed)
    return base


def extract_all(snapshots: list[dict]) -> list[dict]:
    return [extract_price(s) for s in snapshots]
