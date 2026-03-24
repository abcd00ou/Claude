# AI 공급망 인텔리전스 시스템 (AI SCM)

## 프로젝트 개요

AI 공급망 인텔리전스 시스템은 토큰 수요에서 하드웨어 수요를 정량화하고,
공급망 병목을 탐지하며, 투자 시그널을 생성하는 6+2개 에이전트 시스템입니다.

**실행 방법**
```bash
cd /Users/idongseong/Claude/AI_SCM
python3 run.py --quick       # 빠른 실행 (seed data 기반)
python3 run.py               # 전체 실행 (웹 스크래핑 포함)
python3 run.py --report-only # 마지막 결과로 리포트 재생성
python3 run.py --db-only     # DB 저장만 실행
```

## 에이전트 구성

| 에이전트 | 파일 | 역할 | 출력 |
|---------|------|------|------|
| Data | agents/data_agent.py | 시장 데이터 수집 (Reuters 스크래핑 + seed fallback) | market_state.json |
| Mapping | agents/mapping_agent.py | 61개 회사 → 14개 레이어 매핑 + 투자 네트워크 그래프 | company_map + network_graph |
| Modeling | agents/modeling_agent.py | Token→GPU→HBM→Power 정량 모델 (3개 시나리오) | scenarios (2025-2028) |
| Bottleneck | agents/bottleneck_agent.py | 레이어별 가동률 스코어링, cascade 예측 | bottleneck + resolution 타임라인 |
| Strategy | agents/strategy_agent.py | 투자 시그널 10개, Phase 로드맵, 리스크 분석 | investment_signals |
| Report | agents/report_agent.py | HTML 대시보드 (D3.js 네트워크 그래프 포함) + PPT 8슬라이드 | HTML + PPTX |
| DB | agents/db_agent.py | PostgreSQL ai_scm DB 저장 (psycopg2 fallback) | DB 저장 |
| Word | agents/word_agent.py | 한국어 학습용 Word 문서 (7장) | DOCX |

## 파이프라인 흐름

```
Data → Mapping → Modeling → Bottleneck → Strategy → DB(저장) → Report(HTML+PPT) + Word
```

## 핵심 분석 수식

| 수식 | 공식 |
|------|------|
| Token → GPU | GPU = Tokens/day ÷ (tokens/sec × 가동률) |
| GPU → HBM | HBM(GB) = GPU 수 × GPU당 HBM |
| 메모리 압력 | KV Cache = 컨텍스트 × 사용자 × 2B × 2 |
| SSD 수요 | SSD = RAG 토큰 × 바이트/토큰 |
| 전력 수요 | MW = GPU × TDP × 1.3 × PUE ÷ 10⁶ |

## 2026년 Q1 현재 분석 결과 (기준일: 2026-03-24)

- **1차 병목**: HBM (92% 가동률) — SK Hynix 독점 수혜, GB200 NVL72 전용 공급
- **2차 병목**: Power_DC (85%) — 전력 인프라 병목 급부상, Vertiv/GE Vernova 수혜
- **3차 병목**: CoWoS 패키징 (88%) — TSMC 독점, 캐파 120K wpm(2026) 확대 중
- **투자 국면**: Phase 2~3 전환기 (HBM·패키징 → 전력 인프라)
- **Strong Buy**: SK Hynix, TSMC CoWoS, Vertiv, GE Vernova, Broadcom

## 산출물 경로

```
outputs/
├── reports/
│   ├── ai_scm_dashboard_YYYYMMDD.html  # D3.js 인터랙티브 대시보드
│   ├── latest.html                     # 최신 대시보드 링크
│   └── ai_scm_study_YYYYMMDD.docx      # 한국어 학습 Word 문서 (7장)
└── pptx/
    └── ai_scm_YYYYMMDD.pptx            # 임원 보고용 PPT (8슬라이드)
```

## PostgreSQL DB (ai_scm)

| 테이블 | 내용 |
|--------|------|
| companies | 회사 마스터 (레이어, 시가총액) |
| supply_chain_edges | 공급망 관계 (공급/투자/서비스) |
| network_nodes / network_edges | 투자 네트워크 그래프 스냅샷 |
| bottleneck_scores | 병목 점수 시계열 |
| investment_signals | 투자 시그널 히스토리 |
| model_results | 정량 모델 시나리오 결과 |
| hyperscaler_capex | 하이퍼스케일러 CapEx 데이터 |

연결: `postgresql://localhost:5432/ai_scm`
psycopg2 미설치 또는 DB 연결 실패 시 파일 기반으로 자동 fallback

## 참고 데이터 출처

- NVIDIA 실적: https://investor.nvidia.com/
- SK Hynix HBM: https://news.skhynix.com/hbm/
- TSMC CoWoS: https://ir.tsmc.com/english/annualReports
- Goldman DC 전력: https://www.goldmansachs.com/insights/articles/AI-poised-to-drive-160-increase-in-power-demand
- Bloomberg AI 네트워크: https://www.bloomberg.com/graphics/2025-ai-investment-chart/
- Sequoia AI 인프라: https://www.sequoiacap.com/article/ais-600b-question/
