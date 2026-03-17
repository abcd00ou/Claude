# Marketing Agent — SanDisk B2C Storage Marketing Team

## 프로젝트 개요

SanDisk / WD_BLACK 스토리지 제품(내장 SSD, 외장 SSD, microSD)의 B2C 마케팅 전략을 시뮬레이션하고 VP급 보고서를 자동 생성하는 멀티 에이전트 시스템.

**실행 방법**
```bash
cd /Users/idongseong/Claude/marketing
python run_simulation.py        # 6시간 게이트 포함 시뮬 실행 (메인)
python run_daily.py             # 게이트 없이 전체 에이전트 강제 실행
```

**자동 스케줄**: launchd — 6시간마다 `run_simulation.py` 실행

---

## 에이전트 구성

| 에이전트 | 파일 | 역할 | 산출물 |
|---------|------|------|--------|
| 생산 에이전트 | `agents/production_agent.py` | BiCS NAND capa 관리, 제품별 생산량 할당 | `production_simulation.xlsx` |
| 공급 에이전트 | `agents/supply_agent.py` | 재고 관리, 채널별 공급 계획, SCM | `supply_plan.xlsx` |
| 수요예측 에이전트 | `agents/demand_forecast_agent.py` | TAM/SAM 분석, 분기별 수요 예측 | `demand_forecast.xlsx` + VP PPT |
| 마케팅 전략 에이전트 | `agents/marketing_strategy_agent.py` | 제품 mix, 가격전략, P&L | `marketing_strategy.xlsx` + VP PPT |
| MarCom 에이전트 | `agents/marcom_agent.py` | 광고·캠페인·브랜드 awareness | VP PPT |

**PPT 빌더** (VP급, 10슬라이드씩)
- `ppt_demand_forecast.py` → `demand_forecast_vp.pptx`
- `ppt_marketing_strategy.py` → `marketing_strategy_vp.pptx`
- `ppt_marcom.py` → `marcom_plan_vp.pptx`
- `ppt_product_mix.py` → `product_mix_vp.pptx`

---

## 실행 흐름 (`run_simulation.py`)

```
STEP 0 │ 6시간 게이트 확인 (미경과 시 조기 종료)
STEP 1 │ NAND 시장 실시간 데이터 수집 (market_intel.py → web search)
STEP 2 │ 시뮬레이션 1개월 전진 (simulation_engine.py)
STEP 3 │ Crawling DB 실시간 가격 데이터 수집 (crawling_prices.py → PostgreSQL price_intel)
STEP 4 │ 5개 에이전트 + 4종 VP PPT 생성
STEP 5 │ 이메일 리포트 전송 (email_reporter.py → abcd00ou@gmail.com)
```

---

## 제품 포트폴리오

### Internal SSD (WD_BLACK)
| 라인 | NAND | 용량 | 티어 |
|------|------|------|------|
| SN8100 | BiCS8 (218L) | 1/2/4TB | Flagship |
| SN850X | BiCS6 (162L) | 1/2/4TB | Flagship |
| SN7100 | BiCS8 (218L) | 1/2TB | Midrange |
| SN770 | BiCS5 (112L) | 1/2TB | Midrange |

### External SSD (SanDisk / WD)
| 라인 | NAND | 용량 | 티어 |
|------|------|------|------|
| Extreme Pro | BiCS8 | 1/2/4TB | Premium |
| Extreme | BiCS6 | 1/2/4TB | Mainstream |
| My Passport | BiCS5 | 1/2TB | Value |

### microSD (SanDisk)
- Extreme Pro / Extreme / Ultra — 128GB ~ 1TB

---

## 핵심 설정값 (`config.py`)

```python
NAND_COST_PER_GB = {
    "BiCS5": 0.055,   # 112L TLC — 성숙 공정
    "BiCS6": 0.042,   # 162L TLC — 주력 공정
    "BiCS8": 0.038,   # 218L TLC — 최신 공정
}

REGIONS   = ["NA", "EMEA", "APAC", "Japan", "China"]
CHANNELS  = ["E-commerce", "Retail", "B2B/Corporate"]
QUARTERS  = ["2025Q1" ~ "2026Q4"]

# NAND 가격 상승 시 저용량 선호 가중치
CAPACITY_DEMAND_WEIGHT = {128: 1.35, 256: 1.20, 512: 1.00, 1000: 0.85, 2000: 0.65, 4000: 0.40}
```

---

## 데이터 파이프라인

```
web search (NAND 뉴스)
    └→ market_intel.py  →  data/market_intel.json  (nand_signal / price_trend / headlines)
           │
           ↓
simulation_engine.py  →  data/sim_state.json  (history[], 월별 KPI 누적)
           │
PostgreSQL price_intel (Crawling 프로젝트)
    └→ crawling_prices.py  →  실시간 Samsung vs SanDisk 가격 갭
           │
           ↓
agents/*.py  →  outputs/excel/*.xlsx
ppt_*.py     →  outputs/pptx/*_vp.pptx
email_reporter.py  →  Gmail (abcd00ou@gmail.com)
```

---

## 산출물 경로

```
marketing/
├── data/
│   ├── sim_state.json       # 시뮬 히스토리 (월별 KPI 전체)
│   ├── market_intel.json    # NAND 시장 인텔리전스
│   └── internal_sales.json  # 내부 영업 데이터
├── outputs/
│   ├── excel/               # .xlsx 5종
│   └── pptx/                # VP PPT 4종
├── logs/
│   ├── simulation.log
│   └── daily_run.log
└── reports/
```

---

## 외부 연동

- **PostgreSQL `price_intel` DB**: Crawling 프로젝트가 수집한 Samsung/SanDisk 실시간 가격
- **Gmail SMTP**: 시뮬 완료 후 자동 이메일 리포트
- **frankfurter.app**: USD 환율 (Dashboard에서 사용)
- **Web Search**: NAND 시장 뉴스 수집 (market_intel.py)

---

## Dashboard 연동

`/Users/idongseong/Claude/dashboard/pages/3_📈_Marketing_Sim.py`가 아래 파일을 실시간으로 읽어 표시:
- `data/sim_state.json` → 월매출, GM%, 시장점유율, SKU별 실적
- `data/market_intel.json` → NAND 시그널, 가격 트렌드, 헤드라인
- `data/internal_sales.json` → 내부 영업 실적

Dashboard 실행: `cd /Users/idongseong/Claude/dashboard && streamlit run app.py --server.port 8502`
