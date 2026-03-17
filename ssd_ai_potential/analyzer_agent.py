"""
analyzer_agent.py — 수요 신호 분류 + 기술 근거 추출
Claude API 사용 가능 시: AI 분류 / 없을 시: 키워드 기반 규칙 분류
"""
import json
import re
import logging
from datetime import datetime, timezone
from typing import Optional

import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [ANALYZER] %(message)s")
log = logging.getLogger(__name__)

# ──────────────────────────────────────────────────────────────
# 키워드 기반 규칙 분류 (폴백)
# ──────────────────────────────────────────────────────────────

BUY_INTENT_PATTERNS = [
    r"\b(buy|bought|purchase|order|get)\b.{0,30}\b(ssd|nvme|storage|drive)\b",
    r"\b(which|what|recommend|best)\b.{0,30}\b(ssd|nvme|storage|drive)\b",
    r"\bneed.{0,20}(ssd|nvme|storage|drive)\b",
    r"\b(ssd|nvme|storage|drive).{0,30}(recommend|suggestion|advice)\b",
    r"looking for.{0,30}(ssd|storage|drive)",
    r"(considering|thinking about).{0,30}(ssd|nvme|storage)",
]

UPGRADE_INTENT_PATTERNS = [
    r"\b(upgrade|expand|add more|increase).{0,30}(storage|disk|drive|ssd)\b",
    r"\b(running out of|not enough|limited|insufficient).{0,30}(space|storage|disk)\b",
    r"\b(full|filled up|maxed out).{0,30}(drive|disk|storage|ssd)\b",
    r"\b(storage|disk|ssd).{0,30}(upgrade|expansion|more space)\b",
    r"need more.{0,20}(space|storage|disk|gb|tb)",
    r"(replace|swap out|switch).{0,30}(hard drive|hdd|ssd)",
]

TECHNICAL_NEED_PATTERNS = [
    r"\b(model weights?|gguf|ggml|checkpoint).{0,40}(ssd|nvme|storage|disk|drive)\b",
    r"\b(ssd|nvme|storage|disk).{0,40}(model weights?|gguf|inference|loading)\b",
    r"\b(offload|vram offload|cpu offload).{0,40}(ssd|disk|nvme|storage)\b",
    r"\b(ssd|disk|nvme).{0,40}(offload|vram|swap)\b",
    r"\b(swap|virtual memory|page file).{0,30}(ssd|nvme|fast|speed)\b",
    r"\b(io|i/o|read speed|write speed|sequential).{0,30}(model|inference|loading)\b",
    r"\b(model|llm|ai).{0,30}(too large|too big|doesn.t fit|won.t fit)\b",
    r"\b(disk speed|io speed|nvme speed).{0,30}(matter|important|affect|bottleneck)\b",
    r"\bportable.{0,30}(llm|model|ai|inference)\b",
    r"\b(llm|model|ai).{0,30}portable.{0,20}(ssd|drive)\b",
]

PORTABLE_SSD_PATTERNS = [
    r"\b(portable|external|usb).{0,20}(ssd|drive|storage)\b",
    r"\b(ssd|drive|storage).{0,20}(portable|external|usb)\b",
    r"\bsandisk.{0,20}(portable|extreme)\b",
    r"\bsamsung.{0,20}(t7|t5|x5|portable)\b",
    r"\bseagate.{0,20}(portable|one touch)\b",
]


def classify_by_keywords(text: str) -> str:
    """규칙 기반 수요 신호 분류"""
    t = text.lower()
    if any(re.search(p, t) for p in TECHNICAL_NEED_PATTERNS):
        return "technical_need"
    if any(re.search(p, t) for p in BUY_INTENT_PATTERNS):
        return "buy_intent"
    if any(re.search(p, t) for p in UPGRADE_INTENT_PATTERNS):
        return "upgrade_intent"
    # 최소한 SSD + LLM 키워드가 둘 다 있으면 잠재 신호
    has_ssd = any(kw.lower() in t for kw in config.KEYWORDS_SSD)
    has_llm = any(kw.lower() in t for kw in ["llm", "llama", "local ai", "model", "ollama",
                                               "inference", "gguf", "weights", "quantiz"])
    if has_ssd and has_llm:
        return "co_mention"   # SSD + LLM 동시 언급 (약한 신호)
    return "no_signal"


def extract_technical_factors(text: str) -> list[str]:
    """기술 근거 태그 추출"""
    t = text.lower()
    factors = []
    checks = {
        "model_weight_size": [r"model.{0,20}(size|large|big|gb|tb)", r"(gguf|weights).{0,20}(space|storage|disk)"],
        "vram_offload":      [r"(vram|gpu memory).{0,30}(offload|overflow|not enough)", r"offload.{0,20}(disk|ssd|nvme)"],
        "swap_speed":        [r"\bswap\b.{0,20}(ssd|nvme|speed|fast)", r"(virtual memory|page file).{0,20}(ssd|fast)"],
        "io_bottleneck":     [r"(io|i/o|read speed).{0,20}(bottleneck|slow|matter|affect)", r"(loading|inference).{0,20}(slow|speed|disk)"],
        "portability":       [r"(portable|external|usb).{0,20}(ssd|drive|model|llm)", r"run.{0,20}model.{0,20}(different|multiple|another).{0,20}(pc|computer|machine)"],
        "capacity":          [r"(not enough|running out|need more).{0,20}(space|storage|gb|tb)", r"(multiple|many|several).{0,20}(models?|gguf).{0,20}(storage|space|disk)"],
        "speed_matters":     [r"nvme.{0,20}(faster|better|matter|important)", r"(ssd|nvme).{0,20}(faster|speed|performance).{0,20}(inference|loading|model)"],
    }
    for factor, patterns in checks.items():
        if any(re.search(p, t) for p in patterns):
            factors.append(factor)
    return factors


def has_portable_ssd(text: str) -> bool:
    t = text.lower()
    return any(re.search(p, t) for p in PORTABLE_SSD_PATTERNS)


# ──────────────────────────────────────────────────────────────
# Claude API 분류 (배치)
# ──────────────────────────────────────────────────────────────

def classify_with_claude(posts: list[dict]) -> list[dict]:
    """Claude API로 20개씩 배치 분류"""
    if not config.ANTHROPIC_API_KEY:
        return posts

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
    except Exception:
        log.warning("Anthropic 초기화 실패 → 키워드 분류 사용")
        return posts

    BATCH_SIZE = 20
    for i in range(0, len(posts), BATCH_SIZE):
        batch = posts[i:i + BATCH_SIZE]
        items_text = "\n\n".join([
            f"[{j}] 출처: {p['source']}\n제목: {p['title']}\n본문: {p['body'][:500]}"
            for j, p in enumerate(batch)
        ])

        prompt = f"""아래 커뮤니티 포스트들을 분석하여 SSD 구매·교체·확장 수요 신호를 분류하세요.

분류 기준:
- buy_intent: SSD/스토리지 구매 의향 직접 표현 (추천 요청, 구매 고민 등)
- upgrade_intent: 용량 부족, 업그레이드 고민, 기존 드라이브 교체 언급
- technical_need: Local LLM/AI 실행을 위해 SSD가 필요하다는 기술적 언급 (모델 용량, VRAM 오프로드, 스왑 속도, I/O 병목 등)
- co_mention: SSD와 LLM을 동시에 언급하지만 직접적 수요 신호는 없음
- no_signal: 위 어디에도 해당 없음

각 포스트에 대해 JSON 배열로 응답하세요:
{{"results": [{{"index": 0, "demand_signal": "...", "technical_factors": ["..."], "portable_ssd": false, "confidence": "high/medium/low", "key_quote": "핵심 인용구 (한 문장)"}}]}}

포스트 목록:
{items_text}

JSON만 반환하세요."""

        try:
            msg = client.messages.create(
                model=config.CLAUDE_MODEL,
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            raw = msg.content[0].text.strip()
            # JSON 추출
            json_match = re.search(r'\{.*\}', raw, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
                for r in result.get("results", []):
                    idx = r.get("index", -1)
                    if 0 <= idx < len(batch):
                        batch[idx]["demand_signal"]      = r.get("demand_signal", "no_signal")
                        batch[idx]["technical_factors"]  = r.get("technical_factors", [])
                        batch[idx]["portable_ssd"]       = r.get("portable_ssd", False)
                        batch[idx]["claude_confidence"]  = r.get("confidence", "")
                        batch[idx]["key_quote"]          = r.get("key_quote", "")
        except Exception as e:
            log.error(f"Claude API 배치 오류: {e}")

    return posts


# ──────────────────────────────────────────────────────────────
# 분석 집계
# ──────────────────────────────────────────────────────────────

def aggregate(posts: list[dict]) -> dict:
    """분석 결과 집계"""
    signal_counts = {
        "buy_intent": 0, "upgrade_intent": 0,
        "technical_need": 0, "co_mention": 0, "no_signal": 0
    }
    factor_counts: dict[str, int] = {}
    portable_count = 0
    top_posts = []

    for p in posts:
        sig = p.get("demand_signal") or "no_signal"
        signal_counts[sig] = signal_counts.get(sig, 0) + 1

        for f in (p.get("technical_factors") or []):
            factor_counts[f] = factor_counts.get(f, 0) + 1

        if p.get("portable_ssd"):
            portable_count += 1

        # 수요 신호 있는 포스트 수집
        if sig in ("buy_intent", "upgrade_intent", "technical_need"):
            top_posts.append({
                "source": p["source"],
                "title": p["title"],
                "url": p["url"],
                "signal": sig,
                "score": p.get("score", 0),
                "key_quote": p.get("key_quote", ""),
                "technical_factors": p.get("technical_factors", []),
            })

    # score 기준 상위 30개
    top_posts.sort(key=lambda x: x["score"], reverse=True)
    top_posts = top_posts[:30]

    total = len(posts)
    demand_total = sum(signal_counts[s] for s in ("buy_intent", "upgrade_intent", "technical_need"))

    # 서브레딧별 집계
    by_source: dict[str, dict] = {}
    for p in posts:
        src = p.get("source", "unknown")
        if src not in by_source:
            by_source[src] = {"total": 0, "demand": 0}
        by_source[src]["total"] += 1
        if p.get("demand_signal") in ("buy_intent", "upgrade_intent", "technical_need"):
            by_source[src]["demand"] += 1

    return {
        "analysis_date": datetime.now(timezone.utc).isoformat(),
        "total_posts": total,
        "demand_signals": signal_counts,
        "demand_total": demand_total,
        "demand_rate_pct": round(demand_total / total * 100, 1) if total else 0,
        "technical_factors": dict(sorted(factor_counts.items(), key=lambda x: -x[1])),
        "portable_ssd_mentions": portable_count,
        "portable_ssd_pct": round(portable_count / total * 100, 1) if total else 0,
        "top_demand_posts": top_posts,
        "by_source": dict(sorted(by_source.items(), key=lambda x: -x[1]["demand"])),
    }


# ──────────────────────────────────────────────────────────────
# 메인 분석기
# ──────────────────────────────────────────────────────────────

class AnalyzerAgent:
    def __init__(self):
        self.posts_file   = config.POSTS_FILE
        self.analysis_file = config.ANALYSIS_FILE

    def run(self):
        if not self.posts_file.exists():
            log.error("crawled_posts.json 없음 — 크롤러 먼저 실행하세요")
            return None

        with open(self.posts_file, encoding="utf-8") as f:
            posts = json.load(f)
        log.info(f"{len(posts)}개 포스트 분석 시작")

        # 1단계: 키워드 미분류 포스트 처리
        unclassified = [p for p in posts if p.get("demand_signal") is None]
        log.info(f"키워드 미분류: {len(unclassified)}개")
        for p in unclassified:
            full_text = f"{p['title']} {p['body']} " + \
                        " ".join(c["body"] for c in p.get("relevant_comments", []))
            p["demand_signal"]     = classify_by_keywords(full_text)
            p["technical_factors"] = extract_technical_factors(full_text)
            p["portable_ssd"]      = has_portable_ssd(full_text)
            p["classified_by"]     = "keyword"

        # 2단계: Claude API 정밀 분류
        # - 키워드로 분류됐지만 Claude 검증 안 된 것 (classified_by == "keyword")
        # - no_signal 제외, co_mention 포함
        if config.ANTHROPIC_API_KEY:
            candidate = [p for p in posts
                         if p.get("classified_by") == "keyword"
                         and p.get("demand_signal") != "no_signal"]
            log.info(f"Claude API 정밀 분류 대상: {len(candidate)}개")
            classify_with_claude(candidate)
            # 분류 완료 표시
            for p in candidate:
                p["classified_by"] = "claude"
        else:
            log.info("ANTHROPIC_API_KEY 없음 → 키워드 분류만 사용")

        # 분류된 결과 원본에 반영
        id_to_post = {p["post_id"]: p for p in unclassified}
        for p in posts:
            if p["post_id"] in id_to_post:
                p.update(id_to_post[p["post_id"]])

        # 저장
        with open(self.posts_file, "w", encoding="utf-8") as f:
            json.dump(posts, f, ensure_ascii=False, indent=2)

        # 집계
        result = aggregate(posts)

        # 기존 결과에 누적
        history = []
        if self.analysis_file.exists():
            with open(self.analysis_file, encoding="utf-8") as f:
                history = json.load(f)
        history.append(result)
        with open(self.analysis_file, "w", encoding="utf-8") as f:
            json.dump(history, f, ensure_ascii=False, indent=2)

        log.info(f"분석 완료 — 수요 신호: {result['demand_total']}개 ({result['demand_rate_pct']}%)")
        return result


if __name__ == "__main__":
    agent = AnalyzerAgent()
    result = agent.run()
    if result:
        print(json.dumps(result, ensure_ascii=False, indent=2))
