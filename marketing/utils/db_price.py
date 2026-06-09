"""
Price DB 쿼리 유틸리티
연결 우선순위: PostgreSQL → SQLite (price_intel.db) → JSON 폴백
"""
import os
import json
import sqlite3
from pathlib import Path

DB_URL      = os.getenv("DATABASE_URL", "")
DATA_DIR    = Path(__file__).parent.parent / "data"
SQLITE_PATH = DATA_DIR / "price_intel.db"


# ── SQLite helpers ─────────────────────────────────────────────────────────

def _sqlite_conn() -> sqlite3.Connection:
    c = sqlite3.connect(SQLITE_PATH)
    c.row_factory = sqlite3.Row
    return c


def _sqlite_available() -> bool:
    return SQLITE_PATH.exists()


# ── JSON fallback ──────────────────────────────────────────────────────────

def _fallback_prices() -> dict:
    with open(DATA_DIR / "internal_sales.json") as f:
        sales = json.load(f)
    prices = {}
    for key, val in sales.get("amazon_real_prices", {}).items():
        if key.startswith("_"):
            continue
        sku_key = key.lower().replace("_usd", "")
        prices[sku_key] = {
            "price":       val["crawled"],
            "msrp":        val.get("msrp"),
            "premium_pct": val.get("premium_pct"),
            "currency":    "USD",
            "observed_at": "2026-03-09",
            "source":      "amazon",
            "seller":      "3P",
            "country":     "US",
        }
    return prices


# ── Public API ─────────────────────────────────────────────────────────────

def get_latest_prices(country: str = "US") -> dict:
    """SKU별 최신 수락 가격 조회. PostgreSQL → SQLite → JSON 순으로 시도."""
    # 1. PostgreSQL
    if DB_URL:
        try:
            import psycopg2
            con = psycopg2.connect(DB_URL)
            cur = con.cursor()
            cur.execute("""
                SELECT DISTINCT ON (p.sku_id)
                    p.sku_id, p.price, p.currency, p.observed_at,
                    p.source, p.seller_name, p.availability, p.fulfillment,
                    p.parse_confidence, s.brand, s.category, s.model, s.capacity
                FROM price_observations p
                LEFT JOIN skus s ON p.sku_id = s.sku_id
                WHERE p.country = %s AND p.is_accepted = TRUE AND p.price > 0
                ORDER BY p.sku_id, p.observed_at DESC
            """, (country,))
            rows = cur.fetchall()
            con.close()
            result = {r[0]: {
                "price": float(r[1]) if r[1] else None, "currency": r[2],
                "observed_at": str(r[3]), "source": r[4], "seller": r[5],
                "availability": r[6], "fulfillment": r[7],
                "confidence": float(r[8]) if r[8] else None,
                "brand": r[9], "category": r[10], "model": r[11],
                "capacity": r[12], "country": country,
            } for r in rows}
            print(f"  [DB:postgres] price_observations: {len(result)}개 SKU 로드 (country={country})")
            return result
        except Exception:
            pass

    # 2. SQLite
    if _sqlite_available():
        try:
            con = _sqlite_conn()
            cur = con.execute("""
                SELECT p.sku_id, p.price, p.currency, p.observed_at,
                       p.source, p.seller_name, p.availability, p.fulfillment,
                       p.parse_confidence, s.brand, s.category, s.model, s.capacity,
                       p.msrp, p.premium_pct
                FROM price_observations p
                LEFT JOIN skus s ON p.sku_id = s.sku_id
                WHERE p.country = ? AND p.is_accepted = 1 AND p.price > 0
                ORDER BY p.sku_id, p.observed_at DESC
            """, (country,))
            seen = set()
            result = {}
            for r in cur.fetchall():
                if r[0] in seen:
                    continue
                seen.add(r[0])
                result[r[0]] = {
                    "price": r[1], "currency": r[2], "observed_at": r[3],
                    "source": r[4], "seller": r[5], "availability": r[6],
                    "fulfillment": r[7], "confidence": r[8],
                    "brand": r[9], "category": r[10], "model": r[11],
                    "capacity": r[12], "country": country,
                    "msrp": r[13], "premium_pct": r[14],
                }
            con.close()
            print(f"  [DB] price_observations: {len(result)}개 SKU 로드 (country={country})")
            return result
        except Exception as e:
            print(f"  [DB:sqlite] 오류 → JSON 폴백: {e}")

    # 3. JSON fallback
    prices = _fallback_prices()
    print(f"  [DB] JSON 폴백: {len(prices)}개 SKU 로드")
    return prices


def get_price_history(sku_ids: list, country: str = "US", days: int = 30) -> list:
    """SKU 목록의 가격 히스토리 (최근 N일) 반환."""
    if DB_URL:
        try:
            import psycopg2
            con = psycopg2.connect(DB_URL)
            cur = con.cursor()
            cur.execute("""
                SELECT sku_id, price, currency, observed_at, source
                FROM price_observations
                WHERE sku_id = ANY(%s) AND country = %s
                  AND is_accepted = TRUE AND price > 0
                  AND observed_at >= NOW() - INTERVAL '%s days'
                ORDER BY observed_at DESC
            """, (sku_ids, country, days))
            rows = cur.fetchall()
            con.close()
            return [{"sku_id": r[0], "price": float(r[1]) if r[1] else None,
                     "currency": r[2], "observed_at": str(r[3]), "source": r[4]}
                    for r in rows]
        except Exception:
            pass

    if _sqlite_available():
        try:
            placeholders = ",".join("?" * len(sku_ids))
            con = _sqlite_conn()
            cur = con.execute(f"""
                SELECT sku_id, price, currency, observed_at, source
                FROM price_observations
                WHERE sku_id IN ({placeholders}) AND country = ?
                  AND is_accepted = 1 AND price > 0
                ORDER BY observed_at DESC
            """, (*sku_ids, country))
            rows = cur.fetchall()
            con.close()
            return [{"sku_id": r[0], "price": r[1], "currency": r[2],
                     "observed_at": r[3], "source": r[4]} for r in rows]
        except Exception:
            pass

    return []


def get_run_stats() -> dict:
    """최근 10개 run_log 실행 통계 반환."""
    if DB_URL:
        try:
            import psycopg2
            con = psycopg2.connect(DB_URL)
            cur = con.cursor()
            cur.execute("""
                SELECT run_id, started_at, completed_at, total_targets,
                       success_count, quarantine_count, hitl_count, status
                FROM run_log ORDER BY started_at DESC LIMIT 10
            """)
            rows = cur.fetchall()
            con.close()
            return {"runs": [{"run_id": r[0], "started_at": str(r[1]),
                               "completed_at": str(r[2]), "total_targets": r[3],
                               "success_count": r[4], "quarantine_count": r[5],
                               "hitl_count": r[6], "status": r[7]} for r in rows]}
        except Exception:
            pass

    if _sqlite_available():
        try:
            con = _sqlite_conn()
            cur = con.execute("""
                SELECT run_id, started_at, completed_at, total_targets,
                       success_count, quarantine_count, hitl_count, status
                FROM run_log ORDER BY started_at DESC LIMIT 10
            """)
            rows = cur.fetchall()
            con.close()
            return {"runs": [{"run_id": r[0], "started_at": r[1],
                               "completed_at": r[2], "total_targets": r[3],
                               "success_count": r[4], "quarantine_count": r[5],
                               "hitl_count": r[6], "status": r[7]} for r in rows]}
        except Exception as e:
            return {"runs": [], "error": str(e)}

    return {"runs": []}


def get_price_comparison(country: str = "US") -> list:
    """Samsung vs SanDisk 카테고리별 가격 비교."""
    if DB_URL:
        try:
            import psycopg2
            con = psycopg2.connect(DB_URL)
            cur = con.cursor()
            cur.execute("""
                SELECT DISTINCT ON (p.sku_id)
                    s.brand, s.category, s.model, s.capacity,
                    p.price, p.currency, p.observed_at, p.source
                FROM price_observations p
                JOIN skus s ON p.sku_id = s.sku_id
                WHERE p.country = %s AND p.is_accepted = TRUE AND p.price > 0
                  AND s.brand IN ('Samsung', 'SanDisk', 'WD')
                ORDER BY p.sku_id, p.observed_at DESC
            """, (country,))
            rows = cur.fetchall()
            con.close()
            return [{"brand": r[0], "category": r[1], "model": r[2], "capacity": r[3],
                     "price": float(r[4]) if r[4] else None, "currency": r[5],
                     "observed_at": str(r[6]), "source": r[7]} for r in rows]
        except Exception:
            pass

    if _sqlite_available():
        try:
            con = _sqlite_conn()
            cur = con.execute("""
                SELECT s.brand, s.category, s.model, s.capacity,
                       p.price, p.currency, p.observed_at, p.source
                FROM price_observations p
                JOIN skus s ON p.sku_id = s.sku_id
                WHERE p.country = ? AND p.is_accepted = 1 AND p.price > 0
                  AND s.brand IN ('Samsung', 'SanDisk', 'WD')
                ORDER BY p.sku_id, p.observed_at DESC
            """, (country,))
            rows = cur.fetchall()
            con.close()
            return [{"brand": r[0], "category": r[1], "model": r[2], "capacity": r[3],
                     "price": r[4], "currency": r[5], "observed_at": r[6], "source": r[7]}
                    for r in rows]
        except Exception:
            pass

    return []
