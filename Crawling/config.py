"""
Price Intelligence System — 설정
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent

# ── PostgreSQL ──────────────────────────────────────────────
# .env 또는 환경변수로 오버라이드 가능
DB_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://localhost:5432/price_intel"
)

# ── 경로 ────────────────────────────────────────────────────
CATALOG_DIR    = BASE_DIR / "catalog"
RAW_SNAPSHOTS  = BASE_DIR / "raw_snapshots"
LOGS_DIR       = BASE_DIR / "logs"

RAW_SNAPSHOTS.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# ── 크롤링 ──────────────────────────────────────────────────
FETCH_TIMEOUT_SEC    = 30
AMAZON_DELAY_MIN_SEC = 5
AMAZON_DELAY_MAX_SEC = 15
MAX_RETRIES          = 2

# User-Agent 풀 (Amazon 차단 우회용 로테이션)
USER_AGENTS = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.3 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
]

# ── 품질 게이트 ─────────────────────────────────────────────
QUALITY_RULES = {
    "min_confidence": 0.7,       # 이하 → quarantine
    "price_change_flag_pct": 30, # ±% 이상 → anomaly flag
}

# ── 스케줄 ──────────────────────────────────────────────────
SCHEDULE_HOURS = [9, 21]  # cron: 0 9,21 * * *

# ── 지원 국가 ────────────────────────────────────────────────
SUPPORTED_COUNTRIES = ["US", "KR", "JP", "DE"]
DEFAULT_COUNTRIES   = ["US"]  # 초기 실행 기본값

# ── 통화 매핑 ────────────────────────────────────────────────
COUNTRY_CURRENCY = {
    "US": "USD",
    "KR": "KRW",
    "JP": "JPY",
    "DE": "EUR",
}

COUNTRY_AMAZON_DOMAIN = {
    "US": "www.amazon.com",
    "KR": "www.amazon.co.kr",
    "JP": "www.amazon.co.jp",
    "DE": "www.amazon.de",
}
