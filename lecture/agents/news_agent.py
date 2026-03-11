"""
lecture/agents/news_agent.py — 일일 AI 뉴스 수집 에이전트

동작 방식:
  1. RSS 피드에서 최근 24시간 AI 뉴스 수집 (feedparser, 무료)
  2. Claude API로 각 뉴스 분석 — 요약·강의 연관성·트렌드 추출
  3. data/news_cache.json 에 중복 제거 후 저장
  4. 새 뉴스가 5건 이상이면 has_significant_updates=True 반환

실행:
  python3 news_agent.py              # 오늘 뉴스 수집
  python3 news_agent.py --refresh    # 캐시 무시하고 재수집
"""

import hashlib
import json
import pathlib
import sys
import time
from datetime import datetime, timedelta, timezone

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from config import DATA_DIR

try:
    import feedparser
    FEEDPARSER_AVAILABLE = True
except ImportError:
    FEEDPARSER_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False


# ─────────────────────────────────────────────────────────────────
# RSS 피드 소스 (무료 · API 키 불필요)
# ─────────────────────────────────────────────────────────────────
RSS_FEEDS = [
    {
        "url": "https://techcrunch.com/feed/",
        "source": "TechCrunch",
        "filter_keywords": ["AI", "artificial intelligence", "LLM", "GPT", "Claude", "Gemini",
                            "machine learning", "OpenAI", "Anthropic", "Google DeepMind"],
    },
    {
        "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",
        "source": "The Verge AI",
        "filter_keywords": [],  # AI 전용 피드, 필터 불필요
    },
    {
        "url": "https://feeds.arstechnica.com/arstechnica/index",
        "source": "Ars Technica",
        "filter_keywords": ["AI", "artificial intelligence", "LLM", "language model",
                            "OpenAI", "Anthropic", "Claude", "GPT"],
    },
    {
        "url": "https://news.google.com/rss/search?q=AI+인공지능+LLM&hl=ko&gl=KR&ceid=KR:ko",
        "source": "Google News KR",
        "filter_keywords": [],
    },
    {
        "url": "https://news.google.com/rss/search?q=ChatGPT+Claude+Gemini+2026&hl=en&gl=US&ceid=US:en",
        "source": "Google News EN",
        "filter_keywords": [],
    },
]

CACHE_FILE = DATA_DIR / "news_cache.json"
SIGNIFICANT_NEW_THRESHOLD = 5  # 신규 뉴스 5건 이상이면 문서 생성


# ─────────────────────────────────────────────────────────────────
# 캐시 관리
# ─────────────────────────────────────────────────────────────────

def get_cached_news() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"last_updated": None, "items": []}


def save_news_cache(data: dict) -> None:
    DATA_DIR.mkdir(exist_ok=True)
    CACHE_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _item_id(title: str, url: str) -> str:
    return hashlib.md5(f"{title}{url}".encode()).hexdigest()[:12]


# ─────────────────────────────────────────────────────────────────
# RSS 수집
# ─────────────────────────────────────────────────────────────────

def _parse_date(entry) -> datetime | None:
    """feedparser entry에서 날짜 추출."""
    for attr in ("published_parsed", "updated_parsed"):
        t = getattr(entry, attr, None)
        if t:
            try:
                return datetime(*t[:6], tzinfo=timezone.utc)
            except Exception:
                pass
    return None


def fetch_rss_news(days: int = 1) -> list[dict]:
    """RSS 피드에서 최근 N일 AI 뉴스 수집."""
    if not FEEDPARSER_AVAILABLE:
        print("  [경고] feedparser 미설치 — pip3 install feedparser")
        return []

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    items = []

    for feed_cfg in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_cfg["url"])
            source = feed_cfg["source"]
            keywords = [k.lower() for k in feed_cfg["filter_keywords"]]

            for entry in feed.entries:
                title = getattr(entry, "title", "").strip()
                link = getattr(entry, "link", "").strip()
                summary = getattr(entry, "summary", getattr(entry, "description", "")).strip()

                if not title or not link:
                    continue

                # 날짜 필터
                pub_date = _parse_date(entry)
                if pub_date and pub_date < cutoff:
                    continue

                # 키워드 필터 (필터 목록이 있는 경우만)
                if keywords:
                    combined = (title + " " + summary).lower()
                    if not any(k in combined for k in keywords):
                        continue

                items.append({
                    "id": _item_id(title, link),
                    "title": title,
                    "url": link,
                    "source": source,
                    "summary_raw": summary[:500],
                    "date": pub_date.isoformat() if pub_date else datetime.now(timezone.utc).isoformat(),
                    "analyzed": False,
                })

            print(f"  ✓ {source}: {len([e for e in feed.entries])}건 처리")
            time.sleep(0.3)  # 피드 서버 부하 방지

        except Exception as e:
            print(f"  [오류] {feed_cfg['source']}: {e}")

    # 중복 제거 (id 기준)
    seen = set()
    unique = []
    for item in items:
        if item["id"] not in seen:
            seen.add(item["id"])
            unique.append(item)

    print(f"  → 수집 완료: {len(unique)}건 (중복 제거 후)")
    return unique


# ─────────────────────────────────────────────────────────────────
# Claude API 분석
# ─────────────────────────────────────────────────────────────────

def analyze_with_claude(items: list[dict]) -> dict:
    """Claude API로 뉴스 분석 — 요약·강의 연관성·트렌드."""
    if not ANTHROPIC_AVAILABLE:
        print("  [경고] anthropic 미설치 — 기본 분석으로 대체")
        return _fallback_analysis(items)

    if not items:
        return _fallback_analysis([])

    client = anthropic.Anthropic()

    # 뉴스 목록을 텍스트로 정리
    news_text = "\n\n".join([
        f"[{i+1}] [{item['source']}] {item['title']}\n{item['summary_raw'][:300]}"
        for i, item in enumerate(items[:20])  # 최대 20건
    ])

    prompt = f"""당신은 AI 산업 분석가입니다. 오늘 수집된 AI 관련 뉴스를 분석해주세요.

수집된 뉴스:
{news_text}

강의 주제: B2C 영업·마케팅·상품기획 담당자를 위한 AI 워크플로우 활용 강의

다음 형식으로 JSON만 응답해주세요 (다른 텍스트 없이):
{{
  "top_news": [
    {{
      "rank": 1,
      "title": "뉴스 제목",
      "source": "출처",
      "summary": "2~3문장 한국어 요약",
      "lecture_relevance": "높음/보통/낮음",
      "lecture_note": "이 뉴스를 강의에 어떻게 활용할 수 있는지 1~2문장",
      "slide_idea": "추가할 수 있는 슬라이드 아이디어 (없으면 null)"
    }}
  ],
  "trend_summary": "이번 주 AI 트렌드를 3~4문장으로 요약",
  "key_developments": ["주요 개발 사항 1", "주요 개발 사항 2", "주요 개발 사항 3"],
  "recommended_additions": ["강의 자료에 추가할 내용 1", "내용 2"],
  "urgency": "높음/보통/낮음"
}}"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}],
        )
        text = response.content[0].text.strip()
        # JSON 블록 추출
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except Exception as e:
        print(f"  [오류] Claude 분석 실패: {e}")
        return _fallback_analysis(items)


def _fallback_analysis(items: list[dict]) -> dict:
    """Claude API 없이 기본 분석 생성."""
    top_news = [
        {
            "rank": i + 1,
            "title": item["title"],
            "source": item["source"],
            "summary": item["summary_raw"][:200] if item.get("summary_raw") else "요약 없음",
            "lecture_relevance": "보통",
            "lecture_note": "강의 자료 업데이트 검토 필요",
            "slide_idea": None,
        }
        for i, item in enumerate(items[:5])
    ]
    return {
        "top_news": top_news,
        "trend_summary": f"오늘 {len(items)}건의 AI 뉴스가 수집되었습니다. Claude API 분석 없이 기본 요약만 제공됩니다.",
        "key_developments": [item["title"] for item in items[:3]],
        "recommended_additions": [],
        "urgency": "보통",
    }


# ─────────────────────────────────────────────────────────────────
# 새 뉴스 판별
# ─────────────────────────────────────────────────────────────────

def has_significant_new_content(new_items: list[dict], cache: dict) -> bool:
    """캐시 대비 신규 뉴스가 N건 이상이면 True."""
    cached_ids = {item["id"] for item in cache.get("items", [])}
    new_count = sum(1 for item in new_items if item["id"] not in cached_ids)
    print(f"  신규 뉴스: {new_count}건 (기준: {SIGNIFICANT_NEW_THRESHOLD}건)")
    return new_count >= SIGNIFICANT_NEW_THRESHOLD


# ─────────────────────────────────────────────────────────────────
# 메인 진입점
# ─────────────────────────────────────────────────────────────────

def run_news_agent(force_refresh: bool = False, days: int = 1) -> dict:
    """
    뉴스 수집 + Claude 분석 + 캐시 업데이트.
    반환: {
      "new_items": [...],
      "analysis": {...},
      "has_significant_updates": bool,
      "total_collected": int,
    }
    """
    print("\n📡 뉴스 수집 시작...")
    cache = get_cached_news()

    # 오늘 이미 수집했으면 스킵 (--refresh가 아닌 경우)
    if not force_refresh and cache.get("last_updated"):
        last = datetime.fromisoformat(cache["last_updated"])
        if (datetime.now(timezone.utc) - last).total_seconds() < 3600 * 6:
            print(f"  캐시 재사용 (마지막 수집: {last.strftime('%Y-%m-%d %H:%M')})")
            return {
                "new_items": [],
                "analysis": cache.get("last_analysis", _fallback_analysis([])),
                "has_significant_updates": False,
                "total_collected": len(cache.get("items", [])),
            }

    # 뉴스 수집
    new_items = fetch_rss_news(days=days)
    significant = has_significant_new_content(new_items, cache)

    # 분석 (신규가 있을 때만)
    analysis = {}
    if new_items:
        print("\n🧠 Claude API 분석 중...")
        analysis = analyze_with_claude(new_items)
    else:
        analysis = _fallback_analysis([])

    # 캐시 업데이트 (기존 + 신규, 최근 200건 유지)
    all_items = new_items + cache.get("items", [])
    seen = set()
    deduped = []
    for item in all_items:
        if item["id"] not in seen:
            seen.add(item["id"])
            deduped.append(item)
    deduped = deduped[:200]

    updated_cache = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "items": deduped,
        "last_analysis": analysis,
    }
    save_news_cache(updated_cache)
    print(f"  ✅ 캐시 저장 완료 ({len(deduped)}건)")

    return {
        "new_items": new_items,
        "analysis": analysis,
        "has_significant_updates": significant,
        "total_collected": len(deduped),
    }


def print_news_summary(result: dict) -> None:
    """수집 결과 출력."""
    analysis = result.get("analysis", {})
    print(f"\n  신규 수집: {len(result.get('new_items', []))}건")
    print(f"  누적 보관: {result.get('total_collected', 0)}건")
    print(f"  문서 생성 필요: {'예' if result.get('has_significant_updates') else '아니오'}")

    if analysis.get("trend_summary"):
        print(f"\n  📊 트렌드 요약:")
        print(f"  {analysis['trend_summary']}")

    top = analysis.get("top_news", [])[:3]
    if top:
        print(f"\n  📰 주요 뉴스 TOP {len(top)}:")
        for item in top:
            print(f"  [{item.get('lecture_relevance', '-')}] {item.get('title', '')}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="AI 뉴스 수집 에이전트")
    parser.add_argument("--refresh", action="store_true", help="캐시 무시하고 재수집")
    parser.add_argument("--days", type=int, default=1, help="최근 N일 뉴스 수집 (기본: 1)")
    args = parser.parse_args()

    result = run_news_agent(force_refresh=args.refresh, days=args.days)
    print_news_summary(result)
