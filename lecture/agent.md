# Lecture Agent — AI 워크플로우 강의 자료 자동 생성 시스템

## 프로젝트 개요

"AI가 바꾸는 우리의 일하는 방식" 강의 PPT와 데모 자료를 자동 생성하는 에이전트 시스템.
대상: B2C 영업, 마케팅, 상품기획 담당자.
McKinsey/BCG 스타일 디자인, Claude API 기반 리서치, 실무 데모 3종 포함.

**실행 방법**
```bash
cd /Users/idongseong/Claude/lecture
python run_lecture.py              # 전체 파이프라인 실행 (PPT + 데일리 뉴스 + 데모)
python run_lecture.py --ppt-only   # PPT만 생성
python run_lecture.py --news-only  # 뉴스 브리핑만 생성
```

**산출물 경로**
```
lecture/output/AI_Workflow_Lecture_YYYYMMDD_HHMM.pptx   # 강의 PPT
lecture/output/daily/news_briefing_YYYYMMDD.docx         # 일일 AI 뉴스 브리핑
lecture/output/demos/                                     # 실무 데모 HTML 3종
lecture/website/index.html                               # 강의 소개 웹페이지
```

---

## 에이전트 구성

| 에이전트 | 파일 | 역할 |
|---------|------|------|
| Research Agent | `agents/research_agent.py` | Claude API로 챕터별 심층 리서치, `data/research_cache.json` 저장 |
| Slide Builder | `agents/slide_builder.py` | 리서치 데이터 기반 PPT 생성 (McKinsey 스타일) |
| News Agent | `agents/news_agent.py` | 일일 AI 뉴스 수집 및 브리핑 생성 |
| Demo Builder | `agents/demo_builder.py` | 실무 데모 HTML 3종 생성 |
| Word Builder | `agents/word_builder.py` | 데일리 뉴스 브리핑 Word 문서 생성 |

---

## 강의 구성 (5챕터)

| # | 챕터 | 핵심 내용 |
|---|------|---------|
| 1 | AI의 진화: 어떻게 여기까지 왔나 | 2022~2026 타임라인, Q&A → CLI 에이전트 진화 곡선 |
| 2 | 우리 업무는 어떻게 달라졌나 | B2C 영업/마케팅/상품기획 Before/After 워크플로우 |
| 3 | 실전 데모: AI로 만드는 콘텐츠 | HTML 랜딩페이지, 이미지 프롬프트, 에이전트 시연 |
| 4 | AI 에이전트: 자동화의 미래 | Tool + Memory + Orchestration, CLI 에이전트 설계 |
| 5 | 지금 당장 시작하는 AI 활용 | 30일 플랜, 주의사항, 직무별 첫 실습 가이드 |

---

## 실행 흐름 (`run_lecture.py`)

```
STEP 1 │ Research Agent — 챕터별 Claude API 리서치 → research_cache.json
STEP 2 │ Slide Builder  — PPT 생성 (5챕터 × 슬라이드)
           │  디자인: McKinsey 스타일, 네이비/화이트, 데이터 시각화 포함
           │  섹션: AI 타임라인, 워크플로우 변화, GPU/트랜스포머 데이터,
           │         Scaling Laws, VRAM/KV Cache, 멀티모달, 2026 전망
STEP 3 │ Demo Builder   — 실무 데모 HTML 3종
           │  demo1_landing_page.html  : 제품 소개 랜딩 페이지 (30초 생성 시연)
           │  demo2_image_prompts.html : 마케팅 이미지 프롬프트 비교
           │  demo3_agent_workflow.html: 에이전트 자동화 워크플로우
STEP 4 │ News Agent     — 최신 AI 뉴스 수집
STEP 5 │ Word Builder   — 뉴스 브리핑 Word 문서 생성
```

---

## 디자인 시스템 (`slide_builder.py`)

```python
# Professional Analyst Theme (McKinsey/BCG 인스파이어)
색상 팔레트:
  bg_dark    = "#0A1628"   # 딥 네이비 (표지/구분 슬라이드)
  navy       = "#0F2B4C"   # 기본 헤딩
  blue       = "#1D4ED8"   # 포인트 블루
  red        = "#C0392B"   # 데이터 하이라이트
  green      = "#0D6B4F"   # 긍정 지표
  amber      = "#B45309"   # 경고/주의

텍스트 계층:
  H1 = "#0F172A"  H2 = "#1E293B"  Body = "#334155"  Muted = "#64748B"
```

---

## 핵심 데이터 (`config.py` 기준)

**AI 타임라인 (AI_TIMELINE)**
- 2022: ChatGPT 3.5 (텍스트 Q&A)
- 2023: DALL-E, Midjourney, Sora (이미지/영상 생성)
- 2024: GPT Plugins, Claude Tools (에이전트/스킬)
- 2025~: Claude Code, Cursor (CLI 코드 에이전트)

**기술 데이터 섹션**
- `GPU_DATA`: GPU 성능 진화 (FLOPS 비교)
- `TRANSFORMER_DATA`: Transformer 아키텍처 설명
- `SCALING_LAWS_DATA`: 파라미터 vs 성능 스케일링
- `VRAM_KVCACHE_DATA`: VRAM/KV Cache 메모리 관리
- `MULTIMODAL_DATA`: 멀티모달 AI 발전 현황
- `AI_FRONTIER_2026`: 2026 AI 전망
- `THIRTY_DAY_PLAN`: 직무별 30일 AI 활용 플랜

---

## 외부 연동

- **Claude API (Anthropic)**: Research Agent가 챕터별 인사이트 생성에 사용
  - 환경변수: `ANTHROPIC_API_KEY`
  - 캐시: `data/research_cache.json` (재실행 시 재사용)
- **python-pptx**: PPT 생성
- **python-docx**: Word 브리핑 생성
- **PIL/Pillow**: 이미지 처리

---

## 파일 구조

```
lecture/
├── config.py                   # 강의 설정, 챕터 구성, 데이터 상수 전체
├── run_lecture.py              # 메인 실행 진입점
├── requirements.txt            # 의존성
├── agents/
│   ├── research_agent.py       # Claude API 리서치
│   ├── slide_builder.py        # PPT 생성 (McKinsey 스타일)
│   ├── news_agent.py           # AI 뉴스 수집
│   ├── demo_builder.py         # 데모 HTML 생성
│   └── word_builder.py         # Word 브리핑 생성
├── output/
│   ├── AI_Workflow_Lecture_*.pptx  # 생성된 PPT
│   ├── daily/news_briefing_*.docx  # 뉴스 브리핑
│   └── demos/                       # 실무 데모 HTML 3종
├── website/
│   └── index.html              # 강의 소개 페이지
└── data/
    └── research_cache.json     # API 리서치 캐시
```

---

## 주의사항

- Claude API 크레딧 필요 (Research Agent). 크레딧 없을 시 리서치 단계 스킵, 캐시 데이터 사용
- PPT 생성 시 PIL 없어도 동작 (텍스트 기반 대체)
- 생성된 PPT 파일명: `AI_Workflow_Lecture_YYYYMMDD_HHMM.pptx` (타임스탬프 포함)
