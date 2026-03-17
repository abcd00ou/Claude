"""
crawler_agent.py — Reddit 공개 API + HackerNews 크롤러
인증 없이 동작 (Reddit 공개 JSON 엔드포인트 사용)
"""
import json
import time
import logging
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional

import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [CRAWLER] %(message)s")
log = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": config.REDDIT_USER_AGENT,
    "Accept": "application/json",
}


# ──────────────────────────────────────────────────────────────
# Reddit 공개 API 유틸
# ──────────────────────────────────────────────────────────────

def reddit_search(subreddit: str, query: str, after_utc: Optional[float] = None,
                  limit: int = 100, sort: str = "new") -> list[dict]:
    """Reddit 공개 JSON API로 서브레딧 검색"""
    url = f"https://www.reddit.com/r/{subreddit}/search.json"
    params = {
        "q": query,
        "sort": sort,
        "limit": min(limit, 100),
        "restrict_sr": "true",
        "t": "all",
    }
    posts = []
    after_token = None

    while True:
        if after_token:
            params["after"] = after_token

        try:
            resp = requests.get(url, headers=HEADERS, params=params, timeout=15)
            if resp.status_code == 429:
                log.warning("Rate limited. Sleeping 60s...")
                time.sleep(60)
                continue
            if resp.status_code != 200:
                log.warning(f"HTTP {resp.status_code} for r/{subreddit} q={query}")
                break
            data = resp.json()
        except Exception as e:
            log.error(f"Request error: {e}")
            break

        children = data.get("data", {}).get("children", [])
        if not children:
            break

        for child in children:
            p = child.get("data", {})
            created = p.get("created_utc", 0)

            # 증분 모드: after_utc 이전 포스트 → 중단
            if after_utc and created <= after_utc:
                return posts

            posts.append({
                "post_id":    p.get("id", ""),
                "source":     f"reddit/r/{subreddit}",
                "url":        f"https://www.reddit.com{p.get('permalink', '')}",
                "title":      p.get("title", ""),
                "body":       (p.get("selftext", "") or "")[:2000],
                "created_utc": created,
                "score":      p.get("score", 0),
                "num_comments": p.get("num_comments", 0),
                "subreddit":  subreddit,
                "query_matched": query,
                "relevant_comments": [],
                "keywords_matched": [],
                "demand_signal": None,
                "crawled_at": datetime.now(timezone.utc).isoformat(),
            })

        after_token = data.get("data", {}).get("after")
        if not after_token or len(posts) >= limit:
            break

        time.sleep(config.REQUEST_DELAY)

    return posts


def fetch_top_comments(post_id: str, subreddit: str, max_comments: int = 5) -> list[dict]:
    """포스트의 상위 댓글 수집"""
    url = f"https://www.reddit.com/r/{subreddit}/comments/{post_id}.json"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code != 200:
            return []
        data = resp.json()
        comments = []
        if len(data) < 2:
            return []
        for child in data[1].get("data", {}).get("children", [])[:max_comments]:
            c = child.get("data", {})
            body = c.get("body", "")
            if body and body != "[deleted]" and body != "[removed]":
                comments.append({
                    "body":        body[:1000],
                    "score":       c.get("score", 0),
                    "created_utc": c.get("created_utc", 0),
                })
        return comments
    except Exception:
        return []


# ──────────────────────────────────────────────────────────────
# HackerNews Algolia API
# ──────────────────────────────────────────────────────────────

def hn_search(query: str, after_utc: Optional[float] = None, limit: int = 100) -> list[dict]:
    """HackerNews Algolia API로 검색"""
    url = "https://hn.algolia.com/api/v1/search_by_date"
    params = {
        "query": query,
        "tags": "story",
        "hitsPerPage": min(limit, 100),
    }
    if after_utc:
        params["numericFilters"] = f"created_at_i>{int(after_utc)}"

    posts = []
    try:
        resp = requests.get(url, params=params, timeout=15)
        if resp.status_code != 200:
            return []
        data = resp.json()
        for hit in data.get("hits", []):
            title = hit.get("title", "") or ""
            story_text = hit.get("story_text", "") or ""
            posts.append({
                "post_id":    f"hn_{hit.get('objectID', '')}",
                "source":     "hackernews",
                "url":        hit.get("url", f"https://news.ycombinator.com/item?id={hit.get('objectID')}"),
                "title":      title,
                "body":       story_text[:2000],
                "created_utc": hit.get("created_at_i", 0),
                "score":      hit.get("points", 0),
                "num_comments": hit.get("num_comments", 0),
                "subreddit":  "hackernews",
                "query_matched": query,
                "relevant_comments": [],
                "keywords_matched": [],
                "demand_signal": None,
                "crawled_at": datetime.now(timezone.utc).isoformat(),
            })
    except Exception as e:
        log.error(f"HN search error: {e}")

    return posts


# ──────────────────────────────────────────────────────────────
# 키워드 매칭
# ──────────────────────────────────────────────────────────────

def match_keywords(text: str) -> list[str]:
    """텍스트에서 관련 키워드 추출"""
    text_lower = text.lower()
    matched = []
    all_keywords = config.KEYWORDS_SSD + config.KEYWORDS_LLM_STORAGE + config.KEYWORDS_PURCHASE
    for kw in all_keywords:
        if kw.lower() in text_lower:
            matched.append(kw)
    return list(set(matched))


def is_relevant(post: dict) -> bool:
    """SSD + LLM 맥락이 모두 있는지 확인"""
    text = f"{post['title']} {post['body']}".lower()
    has_ssd = any(kw.lower() in text for kw in config.KEYWORDS_SSD)
    has_llm_context = any(kw.lower() in text for kw in
                          ["llm", "llama", "model", "ai", "gpt", "local ai",
                           "ollama", "lm studio", "kobold", "oobabooga",
                           "inference", "quantiz", "gguf", "weights"])
    return has_ssd or has_llm_context


# ──────────────────────────────────────────────────────────────
# 메인 크롤러
# ──────────────────────────────────────────────────────────────

class CrawlerAgent:
    def __init__(self):
        self.posts_file = config.POSTS_FILE
        self.state_file = config.STATE_FILE
        self.existing_ids: set[str] = set()
        self.all_posts: list[dict] = []
        self._load_existing()

    def _load_existing(self):
        if self.posts_file.exists():
            with open(self.posts_file) as f:
                self.all_posts = json.load(f)
            self.existing_ids = {p["post_id"] for p in self.all_posts}
            log.info(f"기존 포스트 {len(self.all_posts)}개 로드")

    def _save(self):
        with open(self.posts_file, "w", encoding="utf-8") as f:
            json.dump(self.all_posts, f, ensure_ascii=False, indent=2)
        log.info(f"총 {len(self.all_posts)}개 포스트 저장")

    def _save_state(self, mode: str, new_count: int):
        state = {
            "last_run_utc": datetime.now(timezone.utc).timestamp(),
            "last_run_iso": datetime.now(timezone.utc).isoformat(),
            "mode": mode,
            "total_posts": len(self.all_posts),
            "new_posts_this_run": new_count,
        }
        with open(self.state_file, "w") as f:
            json.dump(state, f, indent=2)

    def _get_after_utc(self) -> Optional[float]:
        if self.state_file.exists():
            with open(self.state_file) as f:
                state = json.load(f)
            return state.get("last_run_utc")
        return None

    def _add_post(self, post: dict) -> bool:
        """중복 확인 후 추가. 추가됐으면 True"""
        if post["post_id"] in self.existing_ids:
            return False
        if not post["post_id"]:
            return False
        # 키워드 매칭
        full_text = f"{post['title']} {post['body']}"
        post["keywords_matched"] = match_keywords(full_text)
        self.all_posts.append(post)
        self.existing_ids.add(post["post_id"])
        return True

    def run(self, mode: str = "full"):
        """
        mode='full'  : 최근 6개월 전체 수집
        mode='incremental' : 마지막 실행 이후 신규만 수집
        """
        after_utc = None
        if mode == "incremental":
            after_utc = self._get_after_utc()
            if after_utc:
                log.info(f"증분 모드: {datetime.fromtimestamp(after_utc, tz=timezone.utc).isoformat()} 이후 수집")
            else:
                log.info("state 파일 없음 → full 모드로 전환")
                mode = "full"

        if mode == "full":
            cutoff = datetime.now(timezone.utc) - timedelta(days=config.FULL_CRAWL_MONTHS * 30)
            after_utc = cutoff.timestamp()
            log.info(f"Full 모드: {cutoff.isoformat()} 이후 수집")

        new_count = 0

        # ── Reddit 크롤링 ──────────────────────────────────────
        total_subs = len(config.SUBREDDITS)
        for i, sub in enumerate(config.SUBREDDITS, 1):
            log.info(f"[{i}/{total_subs}] r/{sub} 크롤링 중...")
            sub_new = 0

            for query in config.SEARCH_QUERIES:
                try:
                    posts = reddit_search(sub, query, after_utc=after_utc,
                                         limit=config.POSTS_PER_QUERY)
                    for p in posts:
                        if self._add_post(p):
                            sub_new += 1
                    time.sleep(config.REQUEST_DELAY)
                except Exception as e:
                    log.error(f"r/{sub} q={query} 오류: {e}")

            # 상위 포스트 댓글 보강 (score 상위 10개)
            sub_posts = [p for p in self.all_posts if p["source"] == f"reddit/r/{sub}"
                         and not p["relevant_comments"]]
            sub_posts_sorted = sorted(sub_posts, key=lambda x: x["score"], reverse=True)[:10]
            for p in sub_posts_sorted:
                comments = fetch_top_comments(p["post_id"], sub, config.MAX_COMMENTS)
                p["relevant_comments"] = comments
                if comments:
                    time.sleep(1)

            log.info(f"  r/{sub}: +{sub_new}개")
            new_count += sub_new

        # ── HackerNews 크롤링 ─────────────────────────────────
        log.info("HackerNews 크롤링 중...")
        hn_queries = [
            "local LLM SSD storage",
            "llama NVMe model weights",
            "local AI storage upgrade",
            "ollama disk space",
        ]
        hn_new = 0
        for query in hn_queries:
            posts = hn_search(query, after_utc=after_utc)
            for p in posts:
                if self._add_post(p):
                    hn_new += 1
            time.sleep(1)
        log.info(f"  HackerNews: +{hn_new}개")
        new_count += hn_new

        # ── 저장 ──────────────────────────────────────────────
        self._save()
        self._save_state(mode, new_count)
        log.info(f"크롤링 완료 — 신규 {new_count}개 / 누적 {len(self.all_posts)}개")
        return new_count


if __name__ == "__main__":
    import sys
    mode = sys.argv[1] if len(sys.argv) > 1 else "full"
    agent = CrawlerAgent()
    agent.run(mode)
