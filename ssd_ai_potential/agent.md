# SSD × AI 수요 잠재력 조사 — 커뮤니티 크롤링 에이전트 설계서

## 미션
Local LLM 커뮤니티의 SSD(내장/외장/포터블) 교체·확장·구매 수요 신호를 수집하고,
"Local LLM 실행이 실제로 SSD 구매를 유발하는가?"를 데이터로 검증한다.

### 핵심 3대 리서치 질문
1. **수요 존재 여부**: 교체·확장·구매 의향을 직접 표현한 포스트가 얼마나 되는가?
2. **인과 관계 검증**: Local LLM 실행과 SSD(용량·속도) 필요성이 실제로 직접 연결되어 언급되는가?
3. **기술 근거 & 고려 포인트**: 사람들이 SSD 필요성을 인식하는 이유(모델 가중치 크기, VRAM 오프로드, 스왑, I/O 속도 등)는 무엇인가?

---

## 에이전트 구성 (3종)

### 1. `crawler_agent.py` — 커뮤니티 크롤링 에이전트

**역할**: LocalLLM 관련 커뮤니티에서 SSD 관련 게시물·댓글을 수집

**수집 대상 커뮤니티**:
```json
{
  "reddit": [
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
    "OllamaAI"
  ],
  "other": [
    "HackerNews (hn.algolia.com API)",
    "GitHub Discussions (llama.cpp, ollama, LM Studio)"
  ]
}
```

**검색 키워드 조합** (`OR` 검색):
```
1차 (SSD 직접 언급): "SSD" OR "NVMe" OR "M.2" OR "portable SSD" OR "external SSD" OR "USB drive" OR "storage"
2차 (LLM + 스토리지 맥락): "model weights" OR "offload" OR "swap" OR "disk speed" OR "VRAM" OR "quantization" OR "gguf" OR "model size"
복합 (교체/구매 의도): "upgrade storage" OR "need more space" OR "bought SSD" OR "which SSD" OR "storage recommendation" OR "running out of space"
```

**수집 데이터 스키마**:
```json
{
  "post_id": "unique_id",
  "source": "reddit/r/LocalLLaMA",
  "url": "https://...",
  "title": "게시물 제목",
  "body": "본문 (최대 2000자)",
  "author": "익명처리",
  "created_utc": 1234567890,
  "score": 42,
  "num_comments": 15,
  "relevant_comments": [
    {
      "body": "댓글 내용",
      "score": 10,
      "created_utc": 1234567890
    }
  ],
  "keywords_matched": ["SSD", "model weights", "offload"],
  "demand_signal": "buy/upgrade/replace/none",
  "crawled_at": "2026-03-13T09:00:00Z"
}
```

**실행 모드**:
- `--mode full`: 최초 실행 — 최근 6개월치 전체 수집 (limit per sub: 최대 1000개)
- `--mode incremental`: 이후 실행 — `last_run_state.json`의 타임스탬프 이후 새 포스트만 수집

---

### 2. `analyzer_agent.py` — 수요 분석 에이전트

**역할**: 수집된 원시 데이터를 3대 질문 기준으로 분류·분석

**분석 파이프라인**:
1. **수요 신호 분류** (Claude API 호출)
   - `buy_intent`: "SSD 추천 받고 싶다", "어떤 걸 사야 하나" 등 구매 의향
   - `upgrade_intent`: "업그레이드 고민 중", "용량 부족하다" 등 교체/확장 의향
   - `technical_need`: LLM 실행을 위해 SSD가 필요하다는 기술적 언급
   - `no_signal`: 관련 없음
2. **기술 근거 추출**
   - 언급된 기술 포인트 태깅: `model_weight_size`, `vram_offload`, `swap_speed`, `io_bottleneck`, `portability`, `capacity`
3. **포터블 SSD 언급 분리 추적**
   - 외장/포터블 언급 비율 별도 집계

**출력 스키마**:
```json
{
  "analysis_date": "2026-03-13",
  "total_posts_analyzed": 850,
  "demand_signals": {
    "buy_intent": 124,
    "upgrade_intent": 87,
    "technical_need": 203,
    "no_signal": 436
  },
  "technical_factors": {
    "model_weight_size": 178,
    "vram_offload": 145,
    "swap_speed": 89,
    "io_bottleneck": 67,
    "portability": 43,
    "capacity": 201
  },
  "portable_ssd_mentions": 38,
  "top_posts": [...],
  "key_quotes": ["...", "..."]
}
```

---

### 3. `report_agent.py` — 분석 리포트 생성 에이전트

**역할**: 분석 결과를 HTML 리포트로 출력

**리포트 섹션**:
1. **Executive Summary** — 3대 질문에 대한 직접 답변 (Yes/No + 근거 수치)
2. **수요 신호 대시보드** — 시각화 차트 (수요 분류 비율, 시간대별 트렌드)
3. **기술 근거 TOP 10** — SSD 필요성을 언급한 핵심 이유와 대표 인용구
4. **포터블 SSD 특이점** — 포터블/외장 SSD 관련 언급 별도 분석
5. **원시 데이터 테이블** — 수요 신호 포스트 목록 (필터링 가능)
6. **마케팅 시사점** — Local LLM 유저 대상 메시지/포지셔닝 제안

---

## 실행 스케줄

| 실행 | 모드 | 시간 | 내용 |
|---|---|---|---|
| 최초 1회 | `full` | 즉시 | 최근 6개월 전체 수집 |
| 이후 매일 2회 | `incremental` | 09:00, 21:00 | 지난 12시간 신규 포스트만 수집 |
| 리포트 | 자동 | 매 실행 후 | 누적 데이터 기준 리포트 갱신 |

---

## 폴더 구조

```
ssd_ai_potential/
├── agent.md                    ← 이 파일 (설계서)
├── config.py                   ← API 키, 검색 키워드, 커뮤니티 목록
├── crawler_agent.py            ← Reddit/HN/GitHub 크롤링
├── analyzer_agent.py           ← 수요 신호 분류 + 기술 근거 추출
├── report_agent.py             ← HTML 리포트 생성
├── run_research.py             ← 전체 실행 진입점
├── data/
│   ├── crawled_posts.json      ← 수집된 원시 포스트 (누적)
│   ├── analysis_results.json   ← 분석 결과 (누적)
│   └── last_run_state.json     ← 마지막 크롤링 타임스탬프 (증분 기준)
└── outputs/
    └── reports/                ← HTML 리포트 (날짜별)
```

---

## API 의존성

| 서비스 | API | 비고 |
|---|---|---|
| Reddit | PRAW (Reddit API) | `reddit_client_id`, `reddit_client_secret` 필요 |
| HackerNews | Algolia HN API | 무료, 키 불필요 |
| GitHub | GitHub REST API | Public repo 기준 키 불필요 |
| 분석 | Anthropic Claude API | 수요 신호 분류용 |

---

## 다음 단계

1. `config.py` — Reddit API 키, 키워드 설정
2. `crawler_agent.py` — PRAW + HN API 크롤러 구현
3. `analyzer_agent.py` — Claude API 기반 분류기 구현
4. `report_agent.py` — HTML 리포트 생성
5. `run_research.py` — `--mode full/incremental` 진입점
6. launchd/cron 등록 — 09:00, 21:00 자동 실행

> **우선순위**: crawler → analyzer → report 순서로 구축
> (데이터 없이 분석/리포트 불가)
