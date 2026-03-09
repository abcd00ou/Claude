"""
제품 이미지 다운로더
- Crawling/catalog/ URL 참고 → 제조사 공식 사이트 og:image 추출
- 로컬 캐시: marketing/data/images/
- 실패 시 None 반환 (PPT에서 placeholder 사용)
"""
import re
import io
import json
import time
import requests
from pathlib import Path
from PIL import Image as PILImage

BASE_DIR     = Path(__file__).parent.parent
CACHE_DIR    = BASE_DIR / "data" / "images"
CATALOG_DIR  = BASE_DIR.parent / "Crawling" / "catalog"
CACHE_DIR.mkdir(parents=True, exist_ok=True)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# 주요 제품 manufacturer URL 하드코딩 (catalog 파싱 보완)
KNOWN_URLS = {
    "sd_extreme_1tb":    "https://www.sandisk.com/products/ssd/external-ssd/portable-ssd-sandisk-extreme-usb-3-2",
    "sd_extreme_2tb":    "https://www.sandisk.com/products/ssd/external-ssd/portable-ssd-sandisk-extreme-usb-3-2",
    "sd_extreme_pro_1tb":"https://www.sandisk.com/products/ssd/external-ssd/portable-ssd-sandisk-extreme-pro",
    "sd_extreme_pro_2tb":"https://www.sandisk.com/products/ssd/external-ssd/portable-ssd-sandisk-extreme-pro",
    "wd_sn850x_1tb":     "https://www.westerndigital.com/products/internal-drives/wd-black-sn850x-nvme-ssd",
    "wd_sn850x_2tb":     "https://www.westerndigital.com/products/internal-drives/wd-black-sn850x-nvme-ssd",
    "sd_extreme_micro_256g": "https://www.sandisk.com/products/memory-cards/microsd-cards/sandisk-extreme-microsd-uhs-i-card",
    "sd_extreme_micro_512g": "https://www.sandisk.com/products/memory-cards/microsd-cards/sandisk-extreme-microsd-uhs-i-card",
    "sd_pro_plus_micro_512g": "https://www.sandisk.com/products/memory-cards/microsd-cards/sandisk-pro-plus-microsd-card",
    "sam_t9_1tb":        "https://www.samsung.com/us/computing/memory-storage/portable-solid-state-drives/portable-ssd-t9-usb-3-2-1tb-black-mu-pg1t0b-am/",
    "sam_t9_2tb":        "https://www.samsung.com/us/computing/memory-storage/portable-solid-state-drives/portable-ssd-t9-usb-3-2-2tb-black-mu-pg2t0b-am/",
    "sam_990pro_2tb":    "https://www.samsung.com/us/computing/memory-storage/all-internal-hard-drives/990-pro-pcie-4-0-nvme-ssd-2tb-mz-v9p2t0b-am/",
}


def _load_catalog_urls() -> dict:
    """catalog JSON에서 URL 추출."""
    urls = {}
    for fname in ["samsung.json", "competitors.json"]:
        path = CATALOG_DIR / fname
        if not path.exists():
            continue
        try:
            data = json.load(open(path))
            url_section = data.get("urls", {})
            for sku_id, regions in url_section.items():
                us = regions.get("US", {})
                mfr = us.get("manufacturer")
                if mfr:
                    urls[sku_id] = mfr
        except Exception:
            pass
    return urls


def _fetch_og_image(url: str) -> str | None:
    """제조사 페이지에서 og:image URL 추출."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        if r.status_code != 200:
            return None
        html = r.text
        patterns = [
            r'<meta[^>]+property=["\']og:image["\'][^>]+content=["\']([^"\']+)["\']',
            r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image["\']',
            r'"image"\s*:\s*\[\s*"([^"]+\.(?:jpg|png|webp)[^"]*)"',
            r'"primaryImageOfPage"\s*:\s*\{\s*"url"\s*:\s*"([^"]+)"',
        ]
        for pattern in patterns:
            m = re.search(pattern, html, re.IGNORECASE)
            if m:
                return m.group(1)
    except Exception:
        pass
    return None


def _download_image(image_url: str, cache_key: str,
                    target_w: int = 800, target_h: int = 800) -> str | None:
    """이미지 다운로드 → JPEG 캐시 저장."""
    cache_path = CACHE_DIR / f"{cache_key}.jpg"
    if cache_path.exists() and cache_path.stat().st_size > 5_000:
        return str(cache_path)
    try:
        r = requests.get(image_url, headers=HEADERS, timeout=20)
        if r.status_code == 200 and len(r.content) > 5_000:
            img = PILImage.open(io.BytesIO(r.content)).convert("RGB")
            img.thumbnail((target_w, target_h), PILImage.LANCZOS)
            img.save(cache_path, "JPEG", quality=90)
            return str(cache_path)
    except Exception:
        pass
    return None


def get_product_image(sku_id: str) -> str | None:
    """
    SKU에 대한 제품 이미지 로컬 경로 반환.
    캐시 존재 시 즉시 반환, 없으면 웹에서 다운로드.
    """
    cache_path = CACHE_DIR / f"{sku_id}.jpg"
    if cache_path.exists() and cache_path.stat().st_size > 5_000:
        return str(cache_path)

    # URL 확인 (KNOWN_URLS 우선, 그 다음 catalog)
    catalog_urls = _load_catalog_urls()
    url = KNOWN_URLS.get(sku_id) or catalog_urls.get(sku_id)

    if not url:
        return None

    og_url = _fetch_og_image(url)
    if og_url:
        # 상대 URL 처리
        if og_url.startswith("//"):
            og_url = "https:" + og_url
        result = _download_image(og_url, sku_id)
        if result:
            return result

    time.sleep(0.5)
    return None


def prefetch_images(sku_ids: list[str], max_workers: int = 3) -> dict[str, str | None]:
    """여러 SKU 이미지 병렬 다운로드."""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    results = {}
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(get_product_image, sid): sid for sid in sku_ids}
        for f in as_completed(futures):
            sid = futures[f]
            try:
                results[sid] = f.result()
            except Exception:
                results[sid] = None
    return results


def add_product_image_to_slide(slide, sku_id: str,
                                x: float, y: float, w: float, h: float,
                                fallback_color: str = "1B2A4A") -> bool:
    """
    PPT 슬라이드에 제품 이미지 삽입.
    이미지 없으면 fallback_color 박스 삽입 후 False 반환.
    """
    from pptx.util import Inches
    from ppt_design import rect, tbox, C

    path = get_product_image(sku_id)
    if path:
        try:
            slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))
            return True
        except Exception:
            pass
    # Fallback: 색상 박스
    rect(slide, x, y, w, h, fallback_color)
    label = sku_id.replace("_", " ").upper()
    tbox(slide, label, x + 0.05, y + h/2 - 0.2, w - 0.1, 0.4,
         size=7, color=C.GRAY_400, align=__import__("pptx.enum.text", fromlist=["PP_ALIGN"]).PP_ALIGN.CENTER)
    return False
