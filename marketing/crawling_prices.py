"""
Crawling 프로젝트 실시간 가격 데이터 연계 모듈

PostgreSQL price_intel DB (Crawling 프로젝트)에서 Samsung vs SanDisk 가격 추세 조회.
이메일 리포트용 인라인 SVG 차트 생성.

DB: postgresql://localhost:5432/price_intel
테이블:
  price_observations (sku_id, country, source, price, currency, observed_at, is_accepted)
  skus (sku_id, brand, category, model, capacity)
"""
import json
from datetime import datetime, timedelta
from pathlib import Path

try:
    import psycopg2
    import psycopg2.extras
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "price_intel"

# Crawling 대시보드의 RIVAL_PAIRS와 동일한 경쟁 구도
RIVAL_PAIRS = [
    {
        "id": "portable_10g",
        "label": "Portable SSD — 10Gbps (T7 vs Extreme)",
        "samsung_models": ["T7", "T7 Shield"],
        "rival_brand": "sandisk",
        "rival_models": ["Extreme"],
    },
    {
        "id": "portable_20g",
        "label": "Portable SSD — 20Gbps (T9 vs Extreme Pro)",
        "samsung_models": ["T9"],
        "rival_brand": "sandisk",
        "rival_models": ["Extreme Pro"],
    },
    {
        "id": "internal_pcie4",
        "label": "Internal SSD — PCIe 4.0 (990 Pro vs SN850X)",
        "samsung_models": ["990 Pro"],
        "rival_brand": "sandisk",
        "rival_models": ["WD_BLACK SN850X"],
    },
]


def _get_conn():
    if not HAS_PSYCOPG2:
        print("  [CrawlingDB] psycopg2 미설치 — pip install psycopg2-binary")
        return None
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            connect_timeout=5,
        )
        return conn
    except Exception as e:
        print(f"  [CrawlingDB] DB 연결 실패: {e}")
        return None


def fetch_price_history(days: int = 30, country: str = "US") -> dict:
    """
    최근 N일간 Samsung vs SanDisk 가격 히스토리 반환.

    Returns:
        {
            "pairs": [{
                "id": str,
                "label": str,
                "samsung_models": list,
                "rival_models": list,
                "dates": [str, ...],          # YYYY-MM-DD
                "samsung_prices": [float|None, ...],
                "rival_prices": [float|None, ...],
                "latest_gap_usd": float,      # rival - samsung (양수 = Samsung 저렴)
                "latest_gap_pct": float,
            }, ...],
            "fetched_at": str,
            "source": "db" | "unavailable" | "error",
        }
    """
    conn = _get_conn()
    if conn is None:
        return {
            "pairs": [],
            "fetched_at": datetime.now().isoformat(),
            "source": "unavailable",
        }

    since = (datetime.now() - timedelta(days=days)).isoformat()

    try:
        pairs_result = []
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            for pair in RIVAL_PAIRS:
                # Samsung 일별 평균 가격
                cur.execute("""
                    SELECT date_trunc('day', o.observed_at)::date AS day,
                           AVG(o.price) AS avg_price
                    FROM price_observations o
                    JOIN skus s ON s.sku_id = o.sku_id
                    WHERE s.brand = 'samsung'
                      AND s.model = ANY(%s)
                      AND o.country = %s
                      AND o.is_accepted = true
                      AND o.observed_at >= %s
                    GROUP BY day
                    ORDER BY day
                """, (pair["samsung_models"], country, since))
                sam_rows = cur.fetchall()

                # Rival 일별 평균 가격
                cur.execute("""
                    SELECT date_trunc('day', o.observed_at)::date AS day,
                           AVG(o.price) AS avg_price
                    FROM price_observations o
                    JOIN skus s ON s.sku_id = o.sku_id
                    WHERE s.brand = %s
                      AND s.model = ANY(%s)
                      AND o.country = %s
                      AND o.is_accepted = true
                      AND o.observed_at >= %s
                    GROUP BY day
                    ORDER BY day
                """, (pair["rival_brand"], pair["rival_models"], country, since))
                rival_rows = cur.fetchall()

                if not sam_rows and not rival_rows:
                    continue

                sam_map = {str(r["day"]): float(r["avg_price"]) for r in sam_rows}
                rival_map = {str(r["day"]): float(r["avg_price"]) for r in rival_rows}
                all_dates = sorted(set(sam_map) | set(rival_map))

                sam_prices = [sam_map.get(d) for d in all_dates]
                rival_prices = [rival_map.get(d) for d in all_dates]

                latest_sam = next((p for p in reversed(sam_prices) if p is not None), None)
                latest_rival = next((p for p in reversed(rival_prices) if p is not None), None)
                gap_usd = round((latest_rival - latest_sam), 2) if (latest_rival and latest_sam) else 0.0
                gap_pct = round((gap_usd / latest_sam * 100), 1) if latest_sam else 0.0

                pairs_result.append({
                    "id": pair["id"],
                    "label": pair["label"],
                    "samsung_models": pair["samsung_models"],
                    "rival_models": pair["rival_models"],
                    "dates": all_dates,
                    "samsung_prices": sam_prices,
                    "rival_prices": rival_prices,
                    "latest_gap_usd": gap_usd,
                    "latest_gap_pct": gap_pct,
                })

        conn.close()
        return {
            "pairs": pairs_result,
            "fetched_at": datetime.now().isoformat(),
            "source": "db",
        }

    except Exception as e:
        print(f"  [CrawlingDB] 쿼리 실패: {e}")
        try:
            conn.close()
        except Exception:
            pass
        return {
            "pairs": [],
            "fetched_at": datetime.now().isoformat(),
            "source": "error",
        }


def build_price_chart_html(crawling_data: dict) -> str:
    """
    실시간 가격 추세 데이터를 이메일 삽입용 인라인 SVG 차트 HTML로 변환.
    외부 JS/CSS 라이브러리 불필요.
    """
    pairs = crawling_data.get("pairs", [])
    source = crawling_data.get("source", "unavailable")
    fetched_at = crawling_data.get("fetched_at", "")[:16].replace("T", " ")

    if source == "unavailable" or not pairs:
        return (
            '<div style="background:#fff8e1;border:1px solid #f9a825;border-radius:6px;'
            'padding:12px 16px;margin-bottom:16px;font-size:12px;color:#795548;">'
            '⚠️ Crawling DB 미연결 — 실시간 가격 데이터를 불러올 수 없습니다 '
            f'(postgresql://localhost:{DB_PORT}/{DB_NAME})'
            '</div>'
        )

    SAM_COLOR = "#1428A0"    # 삼성 블루
    RIVAL_COLOR = "#E8003D"  # SanDisk 레드

    charts_html = []
    for pair in pairs:
        dates = pair["dates"]
        sam = pair["samsung_prices"]
        rival = pair["rival_prices"]
        if not dates:
            continue

        all_vals = [v for v in sam + rival if v is not None]
        if not all_vals:
            continue

        W, H = 520, 170
        PAD_L, PAD_R, PAD_T, PAD_B = 52, 16, 28, 34
        plot_w = W - PAD_L - PAD_R
        plot_h = H - PAD_T - PAD_B
        n = len(dates)
        v_min = min(all_vals) * 0.95
        v_max = max(all_vals) * 1.05
        v_range = v_max - v_min or 1

        def to_x(i):
            return PAD_L + (i / max(n - 1, 1)) * plot_w

        def to_y(v):
            return PAD_T + (1 - (v - v_min) / v_range) * plot_h

        def polyline(vals, color):
            pts = " ".join(
                f"{to_x(i):.1f},{to_y(v):.1f}"
                for i, v in enumerate(vals)
                if v is not None
            )
            return (f'<polyline points="{pts}" fill="none" '
                    f'stroke="{color}" stroke-width="2" stroke-linejoin="round"/>') if pts else ""

        # Grid lines + Y labels (4 levels)
        grid = ""
        for frac in [0, 0.33, 0.67, 1.0]:
            v = v_min + frac * v_range
            y = PAD_T + (1 - frac) * plot_h
            grid += (f'<line x1="{PAD_L}" y1="{y:.1f}" x2="{W - PAD_R}" y2="{y:.1f}" '
                     f'stroke="#ebebeb" stroke-width="1"/>'
                     f'<text x="{PAD_L - 4}" y="{y + 3:.1f}" text-anchor="end" '
                     f'font-size="9" fill="#aaa">${v:.0f}</text>')

        # X axis labels (up to 5 evenly spaced dates)
        x_labels = ""
        label_indices = [0] + [round(i * (n - 1) / 4) for i in range(1, 4)] + [n - 1]
        label_indices = sorted(set(label_indices))
        for i in label_indices:
            if 0 <= i < n:
                lbl = dates[i][5:]  # MM-DD
                x_labels += (f'<text x="{to_x(i):.1f}" y="{H - 4}" text-anchor="middle" '
                              f'font-size="9" fill="#bbb">{lbl}</text>')

        gap_usd = pair["latest_gap_usd"]
        gap_pct = pair["latest_gap_pct"]
        gap_color = "#2e7d32" if gap_usd > 0 else "#c62828"
        sign = "+" if gap_usd > 0 else ""

        sam_lbl = " / ".join(pair["samsung_models"])
        rival_lbl = " / ".join(pair["rival_models"])

        svg = (
            f'<svg width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg" '
            f'style="background:#fafbff;border-radius:4px;display:block;">'
            f'{grid}'
            f'{polyline(sam, SAM_COLOR)}'
            f'{polyline(rival, RIVAL_COLOR)}'
            f'{x_labels}'
            f'<text x="{PAD_L}" y="18" font-size="9" fill="{SAM_COLOR}" font-weight="bold">'
            f'■ Samsung {sam_lbl}</text>'
            f'<text x="{PAD_L + 200}" y="18" font-size="9" fill="{RIVAL_COLOR}" font-weight="bold">'
            f'■ SanDisk {rival_lbl}</text>'
            f'</svg>'
        )

        charts_html.append(
            f'<div style="margin-bottom:14px">'
            f'<div style="font-size:12px;font-weight:600;color:#333;margin-bottom:4px">'
            f'{pair["label"]}'
            f'<span style="color:{gap_color};margin-left:10px;font-size:11px">'
            f'Gap {sign}${gap_usd:.2f} ({sign}{gap_pct:.1f}%)</span>'
            f'</div>'
            f'{svg}'
            f'</div>'
        )

    if not charts_html:
        return (
            '<div style="background:#f5f5f5;border-radius:6px;padding:12px 16px;'
            'font-size:12px;color:#999;">가격 데이터 없음 — DB에 데이터를 먼저 수집하세요.</div>'
        )

    return (
        '<div style="background:#fff;border:1px solid #e0e7ff;border-radius:8px;'
        'padding:16px;margin-bottom:20px">'
        '<div style="font-size:13px;font-weight:700;color:#1428A0;margin-bottom:12px">'
        f'📈 실시간 경쟁 가격 추세 (Samsung vs SanDisk · US · {fetched_at})'
        '</div>'
        + "".join(charts_html)
        + '</div>'
    )


if __name__ == "__main__":
    data = fetch_price_history()
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str))
