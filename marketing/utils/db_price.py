"""
PostgreSQL price_intel DB 쿼리 유틸리티
- Crawling 시스템 price_observations 테이블에서 최신 가격 추출
- DB 연결 실패 시 internal_sales.json amazon_real_prices로 폴백
"""
import os
import json
from pathlib import Path
from datetime import datetime, timedelta

DB_URL = os.getenv("DATABASE_URL", "postgresql://localhost:5432/price_intel")
DATA_DIR = Path(__file__).parent.parent / "data"


def _fallback_prices() -> dict:
    """internal_sales.json의 amazon_real_prices 데이터 반환."""
    with open(DATA_DIR / "internal_sales.json") as f:
        sales = json.load(f)
    prices = {}
    for key, val in sales.get("amazon_real_prices", {}).items():
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


def get_latest_prices(country: str = "US") -> dict:
    """
    PostgreSQL에서 SKU별 최신 수락 가격 조회.
    연결 실패 시 internal_sales.json 폴백.
    반환: {sku_id: {price, currency, observed_at, source, seller, ...}}
    """
    try:
        import psycopg2
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT ON (p.sku_id)
                p.sku_id,
                p.price,
                p.currency,
                p.observed_at,
                p.source,
                p.seller_name,
                p.availability,
                p.fulfillment,
                p.parse_confidence,
                s.brand,
                s.category,
                s.model,
                s.capacity
            FROM price_observations p
            LEFT JOIN skus s ON p.sku_id = s.sku_id
            WHERE p.country = %s
              AND p.is_accepted = TRUE
              AND p.price > 0
            ORDER BY p.sku_id, p.observed_at DESC
        """, (country,))
        rows = cur.fetchall()
        conn.close()

        result = {}
        for row in rows:
            result[row[0]] = {
                "price":        float(row[1]) if row[1] else None,
                "currency":     row[2],
                "observed_at":  str(row[3]),
                "source":       row[4],
                "seller":       row[5],
                "availability": row[6],
                "fulfillment":  row[7],
                "confidence":   float(row[8]) if row[8] else None,
                "brand":        row[9],
                "category":     row[10],
                "model":        row[11],
                "capacity":     row[12],
                "country":      country,
            }
        print(f"  [DB] price_observations: {len(result)}개 SKU 로드 (country={country})")
        return result
    except Exception as e:
        print(f"  [DB] 연결 실패 → 폴백 사용: {e}")
        return _fallback_prices()


def get_price_history(sku_ids: list, country: str = "US", days: int = 30) -> list:
    """SKU 목록의 가격 히스토리 (최근 N일) 반환."""
    try:
        import psycopg2
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("""
            SELECT sku_id, price, currency, observed_at, source
            FROM price_observations
            WHERE sku_id = ANY(%s)
              AND country = %s
              AND is_accepted = TRUE
              AND price > 0
              AND observed_at >= NOW() - INTERVAL '%s days'
            ORDER BY observed_at DESC
        """, (sku_ids, country, days))
        rows = cur.fetchall()
        conn.close()
        return [
            {"sku_id": r[0], "price": float(r[1]) if r[1] else None,
             "currency": r[2], "observed_at": str(r[3]), "source": r[4]}
            for r in rows
        ]
    except Exception:
        return []


def get_run_stats() -> dict:
    """최근 10개 run_log 실행 통계 반환."""
    try:
        import psycopg2
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("""
            SELECT run_id, started_at, completed_at, total_targets,
                   success_count, quarantine_count, hitl_count, status
            FROM run_log
            ORDER BY started_at DESC
            LIMIT 10
        """)
        rows = cur.fetchall()
        conn.close()
        return {
            "runs": [
                {
                    "run_id":           r[0],
                    "started_at":       str(r[1]),
                    "completed_at":     str(r[2]),
                    "total_targets":    r[3],
                    "success_count":    r[4],
                    "quarantine_count": r[5],
                    "hitl_count":       r[6],
                    "status":           r[7],
                }
                for r in rows
            ]
        }
    except Exception as e:
        return {"runs": [], "error": str(e)}


def get_price_comparison(country: str = "US") -> list:
    """
    Samsung vs SanDisk 카테고리별 가격 비교 데이터.
    동일 카테고리에서 양 브랜드 최신 가격 반환.
    """
    try:
        import psycopg2
        conn = psycopg2.connect(DB_URL)
        cur = conn.cursor()
        cur.execute("""
            SELECT DISTINCT ON (p.sku_id)
                s.brand, s.category, s.model, s.capacity,
                p.price, p.currency, p.observed_at, p.source
            FROM price_observations p
            JOIN skus s ON p.sku_id = s.sku_id
            WHERE p.country = %s
              AND p.is_accepted = TRUE
              AND p.price > 0
              AND s.brand IN ('Samsung', 'SanDisk', 'WD')
            ORDER BY p.sku_id, p.observed_at DESC
        """, (country,))
        rows = cur.fetchall()
        conn.close()
        return [
            {
                "brand": r[0], "category": r[1], "model": r[2],
                "capacity": r[3], "price": float(r[4]) if r[4] else None,
                "currency": r[5], "observed_at": str(r[6]), "source": r[7],
            }
            for r in rows
        ]
    except Exception:
        return []
