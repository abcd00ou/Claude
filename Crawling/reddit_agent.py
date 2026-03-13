"""
Reddit SSD 시장 인텔리전스 에이전트

Reddit 공개 JSON API를 사용해 LocalLLaMA 및 관련 서브레딧에서
PC/Portable SSD 관련 게시물·댓글을 수집하고 분석합니다.

대상 서브레딧:
  r/LocalLLaMA    — AI 모델 스토리지용 SSD 수요 (핵심)
  r/hardware      — PC 하드웨어 일반
  r/buildapc      — PC 빌드 조언
  r/SSD           — SSD 전문 커뮤니티
  r/DataHoarder   — 대용량 스토리지 수요
  r/hardware      — 하드웨어 뉴스

API 키 불필요 — Reddit 공개 JSON 엔드포인트 사용
결과: Crawling/data/reddit_ssd_<YYYYMMDD>.json
"""
import json
import time
import re
from datetime import datetime
from pathlib import Path
from collections import Counter, defaultdict

import requests

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "reddit"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ── 설정 ──────────────────────────────────────────────────────────
HEADERS = {
    "User-Agent": "SSD-Market-Research-Bot/1.0 (market analysis; contact: research@example.com)"
}
FETCH_DELAY = 2.0   # Reddit rate limit: 60 req/min

SUBREDDITS = [
    {"name": "LocalLLaMA",  "priority": "high",   "reason": "LLM 모델 저장용 NVMe/SSD 대용량 수요"},
    {"name": "SSD",         "priority": "high",   "reason": "SSD 전문 커뮤니티"},
    {"name": "buildapc",    "priority": "medium", "reason": "NVMe/SSD 구매 의사결정"},
    {"name": "hardware",    "priority": "medium", "reason": "하드웨어 뉴스 및 리뷰"},
    {"name": "DataHoarder", "priority": "medium", "reason": "대용량 스토리지 수요"},
]

# 검색 쿼리 (서브레딧별 검색)
SEARCH_QUERIES = [
    "SSD",
    "NVMe",
    "portable SSD",
    "Samsung SSD",
    "Samsung 990 Pro",
    "Samsung 9100",
    "Samsung T9",
    "Samsung T7",
    "storage recommendation",
    "best SSD",
]

# 브랜드/제품 감지 패턴
PRODUCT_PATTERNS = {
    # Samsung
    "samsung_990pro":   r"\b990\s*pro\b",
    "samsung_9100pro":  r"\b9100\s*pro\b",
    "samsung_t9":       r"\bsamsung\s*t9\b|\bt9\s*(portable|ssd|drive)\b",
    "samsung_t7":       r"\bsamsung\s*t7\b|\bt7\s*(portable|ssd|drive)\b",
    "samsung_evo":      r"\bsamsung\s*(evo|qvo)\b",
    "samsung_general":  r"\bsamsung\s+(ssd|nvme|storage)\b",
    # SanDisk / WD
    "sandisk_extreme":  r"\bextreme\s*(pro|v2|portable)?\b",
    "wd_black":         r"\bwd[\s_]?black\b|\bsn8[0-9]{2}x?\b|\bsn7[0-9]{2}\b",
    "wd_my_passport":   r"\bmy\s*passport\b",
    # Competitors
    "seagate":          r"\bseagate\b|\bfirecuda\b|\bbarracuda\b",
    "crucial":          r"\bcrucial\b|\bp3\s*plus\b|\bmx\d+\b",
    "lexar":            r"\blexar\b",
    "kingston":         r"\bkingston\b|\bnv[2-3]\b",
    "sk_hynix":         r"\bsk\s*hynix\b|\bplatinum\s*p\d+\b",
    "corsair":          r"\bcorsair\b|\bmp\d+\b",
    # General capacity
    "capacity_4tb":     r"\b4\s*tb\b",
    "capacity_2tb":     r"\b2\s*tb\b",
    "capacity_1tb":     r"\b1\s*tb\b",
    "capacity_large":   r"\b[5-9]\s*tb\b|\b\d{2,}\s*tb\b",
}

# 감성 키워드
POSITIVE_KW = [
    "great", "excellent", "amazing", "love", "perfect", "best", "fast",
    "recommend", "worth", "reliable", "solid", "happy", "impressed",
    "fantastic", "awesome", "good value", "great deal",
]
NEGATIVE_KW = [
    "slow", "terrible", "avoid", "broken", "failed", "died", "bad",
    "overpriced", "disappointing", "waste", "regret", "problem",
    "issue", "defective", "returned", "rma", "dead", "failure",
    "throttling", "overheat", "hot",
]

# LocalLLaMA 특화: LLM 스토리지 맥락 키워드
LLAMA_STORAGE_KW = [
    "model storage", "weights", "llama", "mistral", "ollama",
    "local llm", "vram", "offload", "gguf", "hugging face",
    "inference", "nvme speed", "fast storage",
]


def _reddit_get(url: str, params: dict = None) -> dict | None:
    """Reddit JSON API GET 요청."""
    try:
        r = requests.get(url, headers=HEADERS, params=params, timeout=15)
        if r.status_code == 429:
            print(f"  [Reddit] Rate limited — 30초 대기")
            time.sleep(30)
            r = requests.get(url, headers=HEADERS, params=params, timeout=15)
        if r.status_code == 200:
            return r.json()
        print(f"  [Reddit] HTTP {r.status_code}: {url}")
    except Exception as e:
        print(f"  [Reddit] 요청 실패: {e}")
    return None


def fetch_subreddit_search(subreddit: str, query: str,
                           sort: str = "relevance", time_filter: str = "month",
                           limit: int = 25) -> list[dict]:
    """서브레딧 검색 결과 수집."""
    url = f"https://www.reddit.com/r/{subreddit}/search.json"
    params = {
        "q": query,
        "sort": sort,
        "t": time_filter,
        "limit": limit,
        "restrict_sr": "true",
    }
    data = _reddit_get(url, params)
    if not data:
        return []
    posts = []
    for item in data.get("data", {}).get("children", []):
        d = item.get("data", {})
        posts.append({
            "id":         d.get("id", ""),
            "subreddit":  d.get("subreddit", subreddit),
            "title":      d.get("title", ""),
            "selftext":   d.get("selftext", "")[:500],
            "score":      d.get("score", 0),
            "upvote_ratio": d.get("upvote_ratio", 0),
            "num_comments": d.get("num_comments", 0),
            "url":        f"https://reddit.com{d.get('permalink', '')}",
            "created_utc": d.get("created_utc", 0),
            "author":     d.get("author", ""),
            "flair":      d.get("link_flair_text", ""),
        })
    return posts


def fetch_post_comments(post_id: str, subreddit: str, limit: int = 30) -> list[str]:
    """게시물 상위 댓글 텍스트 수집."""
    url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json"
    data = _reddit_get(url, {"limit": limit})
    if not data or len(data) < 2:
        return []
    comments = []
    for item in data[1].get("data", {}).get("children", []):
        body = item.get("data", {}).get("body", "")
        if body and body != "[deleted]" and len(body) > 20:
            comments.append(body[:300])
    return comments


def detect_products(text: str) -> list[str]:
    """텍스트에서 언급된 제품/브랜드 감지."""
    text_lower = text.lower()
    found = []
    for product, pattern in PRODUCT_PATTERNS.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            found.append(product)
    return found


def score_sentiment(text: str) -> float:
    """감성 점수 계산. -1(부정) ~ +1(긍정)."""
    text_lower = text.lower()
    pos = sum(1 for kw in POSITIVE_KW if kw in text_lower)
    neg = sum(1 for kw in NEGATIVE_KW if kw in text_lower)
    total = pos + neg
    if total == 0:
        return 0.0
    return round((pos - neg) / total, 3)


def is_llama_storage_context(text: str) -> bool:
    """LocalLLaMA에서 LLM 스토리지 맥락인지 확인."""
    text_lower = text.lower()
    return any(kw in text_lower for kw in LLAMA_STORAGE_KW)


def analyze_posts(posts: list[dict], fetch_comments: bool = True) -> list[dict]:
    """게시물 분석 (제품 감지 + 감성 분석 + 댓글)."""
    analyzed = []
    for i, post in enumerate(posts):
        full_text = post["title"] + " " + post["selftext"]

        # 댓글 수집 (상위 인게이지먼트 포스트만)
        comments = []
        if fetch_comments and post["num_comments"] > 3 and post["score"] > 5:
            comments = fetch_post_comments(post["id"], post["subreddit"])
            if comments:
                time.sleep(FETCH_DELAY)
            full_text_with_comments = full_text + " " + " ".join(comments)
        else:
            full_text_with_comments = full_text

        products = detect_products(full_text_with_comments)
        sentiment = score_sentiment(full_text_with_comments)
        is_llm_ctx = is_llama_storage_context(full_text_with_comments)

        # Samsung 제품 언급 여부
        has_samsung = any(p.startswith("samsung") for p in products)
        # 경쟁사 언급
        competitors_mentioned = [p for p in products
                                 if not p.startswith("samsung") and not p.startswith("capacity")]

        analyzed.append({
            **post,
            "products_mentioned": products,
            "has_samsung": has_samsung,
            "competitors_mentioned": competitors_mentioned,
            "sentiment": sentiment,
            "is_llm_storage_context": is_llm_ctx,
            "comment_count_fetched": len(comments),
            "top_comments": comments[:5],
        })

        if (i + 1) % 5 == 0:
            print(f"    분석 {i + 1}/{len(posts)}...")

    return analyzed


def run_reddit_agent(subreddits: list = None,
                     queries: list = None,
                     time_filter: str = "month",
                     fetch_comments: bool = True) -> dict:
    """
    Reddit SSD 시장 인텔리전스 에이전트 메인 실행.

    Args:
        subreddits: 크롤링할 서브레딧 목록 (None = 기본값)
        queries: 검색 쿼리 목록 (None = 기본값)
        time_filter: 기간 필터 (day/week/month/year)
        fetch_comments: 댓글 수집 여부

    Returns:
        수집/분석 결과 dict
    """
    if subreddits is None:
        subreddits = [s["name"] for s in SUBREDDITS]
    if queries is None:
        queries = SEARCH_QUERIES

    print(f"\n{'='*60}")
    print(f"  Reddit SSD 시장 인텔리전스 — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"  서브레딧: {', '.join(subreddits)}")
    print(f"  기간: {time_filter} | 쿼리: {len(queries)}개")
    print(f"{'='*60}")

    all_posts = []
    seen_ids = set()

    for sub in subreddits:
        print(f"\n▶ r/{sub} 수집 중...")
        sub_count = 0
        for query in queries:
            posts = fetch_subreddit_search(sub, query,
                                           time_filter=time_filter, limit=15)
            for p in posts:
                if p["id"] not in seen_ids:
                    seen_ids.add(p["id"])
                    all_posts.append(p)
                    sub_count += 1
            time.sleep(FETCH_DELAY)

        print(f"  → {sub_count}개 포스트 수집")

    print(f"\n총 {len(all_posts)}개 포스트 수집 완료")

    # ── 분석 ────────────────────────────────────────────────────
    print("\n▶ 분석 중...")
    analyzed = analyze_posts(all_posts, fetch_comments=fetch_comments)

    # ── 집계 ────────────────────────────────────────────────────
    product_counter   = Counter()
    sentiment_by_prod = defaultdict(list)
    samsung_posts     = [p for p in analyzed if p["has_samsung"]]
    llm_storage_posts = [p for p in analyzed if p["is_llm_storage_context"]]
    high_engagement   = sorted(analyzed, key=lambda x: x["score"], reverse=True)[:20]

    for p in analyzed:
        for prod in p["products_mentioned"]:
            product_counter[prod] += 1
            sentiment_by_prod[prod].append(p["sentiment"])

    # 제품별 평균 감성
    product_sentiment = {
        prod: round(sum(scores) / len(scores), 3)
        for prod, scores in sentiment_by_prod.items()
        if scores
    }

    # Samsung vs 경쟁사 언급 비교
    samsung_mentions = sum(1 for p in analyzed
                           if any(p2.startswith("samsung") for p2 in p["products_mentioned"]))
    sandisk_wd_mentions = sum(1 for p in analyzed
                              if any(p2 in ["sandisk_extreme", "wd_black", "wd_my_passport"]
                                     for p2 in p["products_mentioned"]))

    # 서브레딧별 Samsung 언급률
    sub_samsung = defaultdict(lambda: {"total": 0, "samsung": 0})
    for p in analyzed:
        sub_samsung[p["subreddit"]]["total"] += 1
        if p["has_samsung"]:
            sub_samsung[p["subreddit"]]["samsung"] += 1

    sub_summary = {
        sub: {
            "total_posts": v["total"],
            "samsung_mentions": v["samsung"],
            "samsung_rate_pct": round(v["samsung"] / v["total"] * 100, 1) if v["total"] else 0,
        }
        for sub, v in sub_samsung.items()
    }

    # ── 인사이트 생성 ────────────────────────────────────────────
    insights = []

    # LocalLLaMA SSD 수요 분석
    llama_total = sum(1 for p in analyzed if p["subreddit"] == "LocalLLaMA")
    llama_ssd   = sum(1 for p in analyzed
                      if p["subreddit"] == "LocalLLaMA" and p["is_llm_storage_context"])
    if llama_total > 0:
        insights.append(
            f"r/LocalLLaMA에서 {llama_total}개 포스트 중 {llama_ssd}개({llama_ssd/llama_total*100:.0f}%)가 "
            f"LLM 모델 스토리지 맥락 — AI 워크로드용 고용량 NVMe 수요 확인"
        )

    # Samsung 감성
    sam_sentiment = product_sentiment.get("samsung_general", None)
    for key in ["samsung_990pro", "samsung_9100pro", "samsung_t9", "samsung_t7"]:
        if key in product_sentiment:
            insights.append(
                f"{key.replace('_', ' ').title()} 평균 감성: "
                f"{'긍정' if product_sentiment[key] > 0 else '부정'} ({product_sentiment[key]:+.2f})"
            )

    # 4TB 수요
    tb4_count = product_counter.get("capacity_4tb", 0)
    tb2_count = product_counter.get("capacity_2tb", 0)
    if tb4_count > 0:
        insights.append(f"4TB 용량 언급 {tb4_count}회 — LLM 모델 저장 수요로 대용량 선호 증가")

    # 경쟁사 비교
    if sandisk_wd_mentions > 0:
        ratio = samsung_mentions / sandisk_wd_mentions if sandisk_wd_mentions else 0
        insights.append(
            f"Samsung {samsung_mentions}회 vs SanDisk/WD {sandisk_wd_mentions}회 언급 "
            f"(Samsung 언급 비율: {ratio:.1f}x)"
        )

    result = {
        "fetched_at":          datetime.now().isoformat(),
        "time_filter":         time_filter,
        "total_posts":         len(analyzed),
        "subreddits_searched": subreddits,
        "summary": {
            "samsung_post_count":     samsung_mentions,
            "sandisk_wd_post_count":  sandisk_wd_mentions,
            "llm_storage_posts":      len(llm_storage_posts),
            "avg_sentiment_overall":  round(
                sum(p["sentiment"] for p in analyzed) / len(analyzed), 3
            ) if analyzed else 0,
        },
        "product_mentions":    dict(product_counter.most_common(20)),
        "product_sentiment":   product_sentiment,
        "subreddit_summary":   sub_summary,
        "insights":            insights,
        "top_posts": [
            {
                "subreddit": p["subreddit"],
                "title":     p["title"],
                "score":     p["score"],
                "comments":  p["num_comments"],
                "products":  p["products_mentioned"],
                "sentiment": p["sentiment"],
                "is_llm":    p["is_llm_storage_context"],
                "url":       p["url"],
            }
            for p in high_engagement[:15]
        ],
        "samsung_posts": [
            {
                "subreddit": p["subreddit"],
                "title":     p["title"],
                "score":     p["score"],
                "products":  p["products_mentioned"],
                "sentiment": p["sentiment"],
                "top_comments": p["top_comments"][:3],
                "url":       p["url"],
            }
            for p in sorted(samsung_posts, key=lambda x: x["score"], reverse=True)[:20]
        ],
        "llm_storage_posts": [
            {
                "subreddit": p["subreddit"],
                "title":     p["title"],
                "score":     p["score"],
                "products":  p["products_mentioned"],
                "url":       p["url"],
            }
            for p in sorted(llm_storage_posts, key=lambda x: x["score"], reverse=True)[:15]
        ],
    }

    # ── 저장 ────────────────────────────────────────────────────
    date_str = datetime.now().strftime("%Y%m%d_%H%M")
    out_file = DATA_DIR / f"reddit_ssd_{date_str}.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    print(f"\n  ✅ 저장: {out_file}")

    # ── 콘솔 요약 ────────────────────────────────────────────────
    _print_summary(result)

    return result


def _print_summary(result: dict):
    s = result["summary"]
    print(f"\n{'='*60}")
    print("  📊 분석 결과 요약")
    print(f"{'='*60}")
    print(f"  총 포스트       : {result['total_posts']}개")
    print(f"  Samsung 언급    : {s['samsung_post_count']}개")
    print(f"  SanDisk/WD 언급 : {s['sandisk_wd_post_count']}개")
    print(f"  LLM 스토리지 맥락: {s['llm_storage_posts']}개")
    print(f"  전체 평균 감성  : {s['avg_sentiment_overall']:+.3f}")

    print(f"\n  📦 제품 언급 Top 10:")
    for prod, cnt in list(result["product_mentions"].items())[:10]:
        sentiment = result["product_sentiment"].get(prod, 0)
        bar = "▓" * min(cnt, 20)
        print(f"    {prod:<25} {bar} {cnt:>3}회  감성:{sentiment:+.2f}")

    print(f"\n  🔥 서브레딧별 Samsung 언급률:")
    for sub, info in result["subreddit_summary"].items():
        print(f"    r/{sub:<15} {info['samsung_mentions']:>3}/{info['total_posts']:>3}  "
              f"({info['samsung_rate_pct']:.0f}%)")

    if result["insights"]:
        print(f"\n  💡 핵심 인사이트:")
        for ins in result["insights"]:
            print(f"    • {ins}")

    print(f"\n  🏆 Samsung 언급 상위 포스트:")
    for p in result["samsung_posts"][:5]:
        print(f"    [{p['score']:>4}↑] r/{p['subreddit']} — {p['title'][:60]}")

    print()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Reddit SSD 시장 인텔리전스 에이전트")
    parser.add_argument("--time",     default="month",
                        choices=["day", "week", "month", "year"],
                        help="수집 기간 (default: month)")
    parser.add_argument("--sub",      nargs="+",
                        help="서브레딧 지정 (default: 전체)")
    parser.add_argument("--no-comments", action="store_true",
                        help="댓글 수집 건너뜀 (빠른 실행)")
    args = parser.parse_args()

    run_reddit_agent(
        subreddits=args.sub,
        time_filter=args.time,
        fetch_comments=not args.no_comments,
    )
