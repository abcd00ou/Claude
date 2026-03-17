"""
SSD × AI 수요 조사 에이전트 — 설정
"""
import os
from pathlib import Path

BASE_DIR    = Path(__file__).parent
DATA_DIR    = BASE_DIR / "data"
OUTPUT_DIR  = BASE_DIR / "outputs" / "reports"

for d in [DATA_DIR, OUTPUT_DIR]:
    d.mkdir(parents=True, exist_ok=True)

# ── API 키 ──────────────────────────────────────────────────────
# Reddit 공개 API: 키 불필요 (read-only, 10 req/min)
# 정식 Reddit API 사용 시 아래 환경변수 설정:
REDDIT_CLIENT_ID     = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")
REDDIT_USER_AGENT    = "SSD-AI-Demand-Research/1.0 (research bot)"

# Claude API — 수요 신호 AI 분류용 (없으면 키워드 기반 폴백)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL      = "claude-sonnet-4-6"

# ── 크롤링 대상 커뮤니티 ────────────────────────────────────────
SUBREDDITS = [
    "LocalLLaMA",
    "LocalAI",
    "SelfHosted",
    "homelab",
    "hardware",
    "buildapc",
    "singularity",
    "MachineLearning",
    "nvidia",
    "linux",
    "AIAssistants",
    "OllamaAI",
    "StableDiffusion",   # 이미지 AI도 모델 용량 큼
    "Oobabooga",
    "KoboldAI",
]

# ── 검색 키워드 ─────────────────────────────────────────────────
# 레이어 1: SSD 직접 언급
KEYWORDS_SSD = [
    "SSD", "NVMe", "M.2", "m2 drive", "portable SSD", "external SSD",
    "external drive", "USB SSD", "storage upgrade", "disk space",
    "hard drive", "flash drive", "thumb drive",
]

# 레이어 2: LLM + 스토리지 맥락
KEYWORDS_LLM_STORAGE = [
    "model weights", "offload", "swap", "disk speed", "VRAM offload",
    "quantization", "gguf", "model size", "llm storage", "model files",
    "out of vram", "out of memory", "load model", "model loading",
    "ggml", "exllama", "unsloth",
]

# 레이어 3: 구매/교체 의도
KEYWORDS_PURCHASE = [
    "upgrade storage", "need more space", "bought SSD", "which SSD",
    "storage recommendation", "running out of space", "recommend storage",
    "what SSD", "best SSD", "buying SSD", "need SSD", "get SSD",
    "more storage", "bigger drive", "expand storage",
]

# 전체 검색 쿼리 (OR 조합)
SEARCH_QUERIES = [
    "SSD storage NVMe",
    "model weights storage disk",
    "offload VRAM swap SSD",
    "storage upgrade local llm",
    "portable SSD local AI",
    "external drive model files",
    "NVMe speed model loading",
    "disk space model weights",
]

# ── 크롤링 파라미터 ─────────────────────────────────────────────
FULL_CRAWL_MONTHS   = 6       # full mode: 최근 N개월
POSTS_PER_QUERY     = 100     # 쿼리당 최대 포스트
MAX_COMMENTS        = 5       # 포스트당 최대 댓글 수
REQUEST_DELAY       = 2.0     # 요청 간 딜레이 (초)

# ── 데이터 파일 경로 ────────────────────────────────────────────
POSTS_FILE      = DATA_DIR / "crawled_posts.json"
ANALYSIS_FILE   = DATA_DIR / "analysis_results.json"
STATE_FILE      = DATA_DIR / "last_run_state.json"
