"""
Fetch Raw Agent
- Playwright로 URL 요청 → HTML 저장(.html.gz) + content_hash 생성
- Amazon 차단 감지 → fetch_notes: "blocked" 기록
- 요청 간 랜덤 딜레이로 봇 감지 우회
"""
import asyncio
import gzip
import hashlib
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout

from config import (
    RAW_SNAPSHOTS, FETCH_TIMEOUT_SEC,
    AMAZON_DELAY_MIN_SEC, AMAZON_DELAY_MAX_SEC,
    USER_AGENTS, MAX_RETRIES, COUNTRY_AMAZON_DOMAIN,
)


def _snapshot_path(sku_id: str, country: str, source: str, run_date: str) -> Path:
    day_dir = RAW_SNAPSHOTS / run_date
    day_dir.mkdir(parents=True, exist_ok=True)
    fname = f"{sku_id}__{country}__{source}.html.gz"
    return day_dir / fname


def _content_hash(html: str) -> str:
    return hashlib.sha256(html.encode("utf-8")).hexdigest()[:16]


def _is_amazon_blocked(html: str, url: str) -> bool:
    blocked_signals = [
        "api-services-support@amazon.com",
        "To discuss automated access",
        "Robot Check",
        "Enter the characters you see below",
        "Sorry, we just need to make sure",
    ]
    return any(sig in html for sig in blocked_signals)


def _is_amazon_url(url: str) -> bool:
    return any(domain in url for domain in COUNTRY_AMAZON_DOMAIN.values())


async def fetch_one(
    page,
    target: dict,
    run_date: str,
) -> dict:
    """
    단일 URL 요청 → raw snapshot dict 반환.

    target: { sku_id, country, source, url }
    """
    sku_id  = target["sku_id"]
    country = target["country"]
    source  = target["source"]
    url     = target["url"]
    observed_at = datetime.utcnow().isoformat() + "Z"

    result = {
        "sku_id":      sku_id,
        "country":     country,
        "source":      source,
        "url":         url,
        "observed_at": observed_at,
        "http_status": None,
        "final_url":   url,
        "content_hash": None,
        "raw_path":    None,
        "fetch_notes": None,
    }

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            # Amazon 요청 간 딜레이
            if _is_amazon_url(url) and attempt == 1:
                await asyncio.sleep(
                    random.uniform(AMAZON_DELAY_MIN_SEC, AMAZON_DELAY_MAX_SEC)
                )

            ua = random.choice(USER_AGENTS)
            if "amazon.co.jp" in url:
                accept_lang = "ja-JP,ja;q=0.9,en;q=0.8"
            elif "amazon.de" in url:
                accept_lang = "de-DE,de;q=0.9,en;q=0.8"
            else:
                accept_lang = "en-US,en;q=0.9"
            await page.set_extra_http_headers({
                "User-Agent":      ua,
                "Accept-Language": accept_lang,
            })

            # 한국 IP에서 각 Amazon 마켓플레이스 통화 강제
            fetch_url = url
            if _is_amazon_url(url):
                sep = "&" if "?" in url else "?"
                if "amazon.co.jp" in url:
                    fetch_url = url + sep + "language=ja_JP&currency=JPY"
                elif "amazon.de" in url:
                    fetch_url = url + sep + "language=de_DE&currency=EUR"
                elif "amazon.com" in url:
                    fetch_url = url + sep + "language=en_US&currency=USD"

            resp = await page.goto(
                fetch_url,
                timeout=FETCH_TIMEOUT_SEC * 1000,
                wait_until="domcontentloaded",
            )
            result["http_status"] = resp.status if resp else 0
            result["final_url"]   = page.url

            html = await page.content()

            # Amazon 봇 차단 체크
            if _is_amazon_url(url) and _is_amazon_blocked(html, url):
                result["http_status"] = 999
                result["fetch_notes"] = "blocked_captcha"
                return result

            # 성공 — 저장
            snap_path = _snapshot_path(sku_id, country, source, run_date)
            with gzip.open(snap_path, "wt", encoding="utf-8") as f:
                f.write(html)

            result["content_hash"] = _content_hash(html)
            result["raw_path"]     = str(snap_path)
            return result

        except PlaywrightTimeout:
            result["fetch_notes"] = f"timeout_attempt_{attempt}"
            if attempt == MAX_RETRIES:
                result["http_status"] = 408
        except Exception as e:
            result["fetch_notes"] = f"error: {type(e).__name__}: {str(e)[:120]}"
            if attempt == MAX_RETRIES:
                result["http_status"] = 0

        await asyncio.sleep(3)

    return result


async def fetch_all(targets: list[dict], run_date: str) -> list[dict]:
    """
    모든 타겟 URL 순차 요청 (단일 브라우저 컨텍스트 재사용).
    Amazon과 non-Amazon을 섞어 처리하여 패턴 감지 완화.
    """
    results = []
    random.shuffle(targets)  # 순서 랜덤화

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            locale="en-US",
        )
        # 한국 IP에서 Amazon이 KRW로 표시하는 것을 각 마켓플레이스 통화로 강제
        await context.add_cookies([
            {"name": "i18n-prefs", "value": "USD", "domain": ".amazon.com",    "path": "/"},
            {"name": "i18n-prefs", "value": "EUR", "domain": ".amazon.de",     "path": "/"},
            {"name": "i18n-prefs", "value": "JPY", "domain": ".amazon.co.jp",  "path": "/"},
        ])
        page = await context.new_page()

        for target in targets:
            res = await fetch_one(page, target, run_date)
            results.append(res)
            print(
                f"  fetch [{res['http_status']}] {res['sku_id']} "
                f"{res['country']} {res['source']} "
                f"{'OK' if res['raw_path'] else res.get('fetch_notes','?')}"
            )

        await browser.close()

    return results


def load_raw_html(raw_path: str) -> Optional[str]:
    """저장된 .html.gz 파일에서 HTML 문자열 반환."""
    try:
        with gzip.open(raw_path, "rt", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None
