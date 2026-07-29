# DB 파이프라인 아키텍처 — AI 공급망 GEM 데이터 체계

**문서 유형:** 기술 아키텍처 레퍼런스  
**최종 수정:** 2026-07-29  
**담당:** DBA Agent (`agents/data/dba/`)

---

## 1. 전체 데이터 흐름

```
[수집]                      [원본 저장]                 [전처리]                  [분석]
edgar_financials.py    →   quarterly_financials    →   build_panel_long.py   →   panel_long (DB+CSV)
add_payables_edgar.py  →   (+ stock_prices)             │                         │
refresh_financials.py  →   (+ companies)                ├─ null_policy 적용        ├─ leadlag.py
                                                         ├─ features.py             ├─ vecm.py
                                                         │   (46종 파생지표)         ├─ ecm.py
                                                         └─ panel.py (접근 레이어)  └─ cashflow_leadlag.py
```

---

## 2. 물리 저장소

### 2.1 데이터베이스 파일

| 파일 | 역할 | 비고 |
|---|---|---|
| `financials.db` | 메인 분석 DB | SSOT (단일 진실 소스) |
| `intelligence.db` | 마켓 인텔리전스 (섹션별 점유율·가격) | 별도 관리 |
| `financials_YYYYMMDD.db.bak` | 날짜별 백업 | `build_panel_long.py` 실행 시 자동 생성 |

### 2.2 Export 파일 (분석 시작점)

| 파일 | 생성 | 용도 |
|---|---|---|
| `panel_long.csv` | `panel.export_csv()` | 분석 스크립트 기본 진입점 (CSV 없으면 DB fallback) |
| `panel_long_dataset.xlsx` | `export_excel.py` | 대외 공유·수동 검토 |

---

## 3. financials.db 테이블 구조

### 3.1 `companies` — 기업 마스터 (136행)

```sql
CREATE TABLE companies (
    ticker          TEXT,           -- 거래소 티커 (PK)
    slug            TEXT,           -- snake_case 슬러그
    name            TEXT,
    exchange        TEXT,
    segments        TEXT,           -- 소속 섹션 (20개 중 하나)
    hq_country      TEXT,
    is_public       INTEGER,
    fiscal_year_end TEXT            -- 결산월 ('DEC', 'JAN', ...)
)
```

**관리 규칙:** `company_universe.csv`가 정본. 신규 기업 추가 시 두 곳 모두 갱신.

### 3.2 `quarterly_financials` — 분기 재무 원본 (2,246행)

```sql
CREATE TABLE quarterly_financials (
    id                          INTEGER PRIMARY KEY,
    ticker                      TEXT,
    fiscal_year                 INTEGER,
    fiscal_quarter              INTEGER,
    period_end_date             TEXT,       -- 실제 분기말 날짜
    calendar_quarter            TEXT,       -- 'YYYY-QN' 캘린더 분기 (정렬 기준)
    -- P&L
    revenue_usd_m               REAL,
    revenue_ai_dc_usd_m         REAL,       -- AI/데이터센터 세그먼트 매출
    revenue_yoy_pct             REAL,
    gross_profit_usd_m          REAL,
    gross_margin_pct            REAL,
    operating_income_usd_m      REAL,
    net_income_usd_m            REAL,
    eps_diluted                 REAL,
    -- B/S
    cash_usd_m                  REAL,
    inventory_usd_m             REAL,
    receivables_usd_m           REAL,
    accounts_payable_usd_m      REAL,       -- 2026-03 EDGAR 보강 추가
    total_assets_usd_m          REAL,
    total_debt_usd_m            REAL,
    stockholders_equity_usd_m   REAL,
    -- Cash Flow
    capex_usd_m                 REAL,
    fcf_usd_m                   REAL,
    operating_cash_flow_usd_m   REAL,
    -- Guidance
    revenue_guidance_low_usd_m  REAL,
    revenue_guidance_high_usd_m REAL,
    -- 소스 추적
    source_tier     TEXT,       -- 'A' = SEC/IR, 'B' = 애널리스트
    source_doc      TEXT,
    source_date     TEXT,
    source_url      TEXT,
    signal_type     TEXT,
    importance      TEXT,
    confidence      TEXT,
    notes           TEXT,
    created_at      TEXT
)
```

**커버리지:** 121개사, 2016–2027, fiscal year 기준  
**알려진 공백:**
- `accounts_payable_usd_m`: 84행 NULL (~4%) — EDGAR 순차 보강 중
- `inventory_usd_m`: 404행 NULL (~18%) — 소프트웨어 기업 구조적 제로 포함

### 3.3 `stock_prices` — 일간 주가 (323,286행)

```sql
CREATE TABLE stock_prices (
    id              INTEGER PRIMARY KEY,
    ticker          TEXT,
    price_date      TEXT,
    open_usd        REAL,
    high_usd        REAL,
    low_usd         REAL,
    close_usd       REAL,
    adj_close_usd   REAL,
    volume          INTEGER,
    market_cap_usd_b REAL,
    currency        TEXT,
    source_tier     TEXT,
    source_doc      TEXT,
    source_date     TEXT
)
```

**커버리지:** 135개사, 2016-01-04 ~ 2026-06-16  
**분기 재무와의 갭:** quarterly 121개 vs stock_prices 135개 — 14개는 주가만 존재

### 3.4 `panel_long` — 분석용 장형(Long-format) 패널 (69,316행)

```sql
CREATE TABLE panel_long (
    ticker      TEXT NOT NULL,
    companyname TEXT,
    date        TEXT NOT NULL,  -- 정규화 캘린더 분기말 (Q1=03-31, Q2=06-30, ...)
    item        TEXT NOT NULL,  -- 아이템명 (하단 목록 참조)
    value       REAL,
    section     TEXT
)
-- 인덱스
CREATE INDEX ix_panel_tid ON panel_long(ticker, item, date)
CREATE INDEX ix_panel_item ON panel_long(item)
```

**`date` 설계 원칙:** 모든 기업이 동일한 캘린더 분기 그리드를 공유.  
NVDA(1월 결산), DELL(2월 결산) 등 비표준 결산 기업도 캘린더 기준으로 정렬되어  
크로스 기업 Lead-Lag 계산 시 회계연도 차이로 인한 허위 상관(spurious lag)을 방지.

### 3.5 `null_policy` — NULL 분류 테이블

```sql
CREATE TABLE null_policy (
    ticker      TEXT NOT NULL,
    item        TEXT NOT NULL,
    null_type   TEXT NOT NULL CHECK(null_type IN ('structural_zero','data_gap','not_applicable')),
    reason      TEXT,
    updated_at  TEXT DEFAULT (date('now')),
    PRIMARY KEY (ticker, item)
)
```

| null_type | 의미 | 처리 |
|---|---|---|
| `structural_zero` | 비즈니스 모델상 항목이 구조적으로 0 | build 시 NULL → 0 채우기 |
| `data_gap` | 데이터 미수집 | NULL 유지 |
| `not_applicable` | 해당 업종에 지표 자체가 무의미 | 기록용, NULL 유지 |

**현재 등록:** 23개 항목 (소프트웨어·유틸리티·SaaS 기업의 inventory/AP structural_zero)  
**초기화:** `python3 setup_null_policy.py`

### 3.6 `annual_financials` — 연간 재무 (882행)

quarterly_financials의 연간 집계. 장기 추세 분석 및 GEM 확장 시 사용.  
구조는 quarterly_financials와 동일 (fiscal_quarter 없음).

---

## 4. panel_long 아이템 목록 (46종)

### 4.1 원본 재무 (19종)
| item | 원천 컬럼 | 단위 |
|---|---|---|
| `revenue` | `revenue_usd_m` | USD M |
| `revenue_ai_dc` | `revenue_ai_dc_usd_m` | USD M |
| `revenue_yoy` | `revenue_yoy_pct` | % |
| `gross_profit` | `gross_profit_usd_m` | USD M |
| `gross_margin` | `gross_margin_pct` | % |
| `operating_income` | `operating_income_usd_m` | USD M |
| `net_income` | `net_income_usd_m` | USD M |
| `eps` | `eps_diluted` | USD |
| `cash` | `cash_usd_m` | USD M |
| `capex` | `capex_usd_m` | USD M |
| `fcf` | `fcf_usd_m` | USD M |
| `operating_cash_flow` | `operating_cash_flow_usd_m` | USD M |
| `inventory` | `inventory_usd_m` | USD M |
| `receivables` | `receivables_usd_m` | USD M |
| `accounts_payable` | `accounts_payable_usd_m` | USD M |
| `total_assets` | `total_assets_usd_m` | USD M |
| `total_debt` | `total_debt_usd_m` | USD M |
| `stockholders_equity` | `stockholders_equity_usd_m` | USD M |
| `stock_price` | `stock_prices.close_usd` | USD (분기말 as-of) |

### 4.2 파생 운전자본 (4종) — `features.py`가 산출
| item | 수식 | 전처리 가드 |
|---|---|---|
| `DIO` | avg(inventory) / COGS × 91.25 | [0, 500]일 범위 밖 → NaN |
| `DSO` | avg(receivables) / revenue × 91.25 | [0, 500]일 범위 밖 → NaN |
| `DPO` | avg(AP) / purchases × 91.25 | [0, 500]일 범위 밖 → NaN |
| `CCC` | DIO + DSO - DPO | 정제된 컴포넌트로 재산출; 음수 CCC는 정상 (AMZN, DELL 등) |

> **COGS 역산:** `cogs = revenue - gross_profit` (panel.py `DERIVED_ITEMS`)  
> **purchases proxy:** `cogs + Δinventory` (doc tbl5)

### 4.3 성장률 (11종) — 전처리 가드 포함
| 그룹 | 아이템 | 가드 |
|---|---|---|
| QoQ 성장 | REVENUE/COGS/AR/AP/INVENTORY/CAPEX `_GROWTH_QOQ` | ±500% 초과 → NaN |
| YoY 성장 | REVENUE/COGS/AR/AP/INVENTORY `_GROWTH_YOY` | ±500% 초과 → NaN |

### 4.4 미스매치 스프레드 (3종)
| item | 해석 |
|---|---|
| `AR_GROWTH_MINUS_REVENUE_GROWTH` | 양수 = 회수 지연(매출채권 병목) |
| `AP_GROWTH_MINUS_COGS_GROWTH` | 양수 = 현금 방어(지급 늦춤) |
| `INVENTORY_GROWTH_MINUS_REVENUE_GROWTH` | 양수 = 재고 적채 신호 |

### 4.5 비율·마진·현금여력 (9종)
| item | 수식 | get_feature() winsor |
|---|---|---|
| `AR_TO_REVENUE` | AR / revenue | 2%~98% |
| `AP_TO_COGS` | AP / COGS | 2%~98% |
| `OCF_MARGIN` | OCF / revenue | 2%~98% |
| `FCF_MARGIN` | FCF / revenue | 2%~98% |
| `OPERATING_MARGIN` | OP_INCOME / revenue | 2%~98% |
| `CAPEX_TO_OCF` | \|capex\| / OCF | 2%~98% |
| `CASH_CONVERSION_RATIO` | OCF / net_income | 2%~98% |
| `CASH_RUNWAY_QTR` | cash / max(-FCF, 0) | 2%~98% |
| `FCF_TO_OPERATING_INCOME` | FCF / OP_INCOME | 2%~98% |

---

## 5. 전처리 파이프라인 상세

### 5.1 빌드 순서 (`build_panel_long.py`)

```
1. _backup_db()                    ← 날짜 스탬프 백업 (당일 최초 1회)
2. quarterly_financials 로드
3. _apply_null_policy()            ← structural_zero → 0 채우기
4. 중복 (ticker, calendar_quarter) 처리  ← _coalesce: 후순위 비-NULL 우선
5. calendar_quarter → 정규화 date  ← Q1=03-31, Q2=06-30, Q3=09-30, Q4=12-31
6. melt → long_fin (원본 재무 long)
7. stock_prices: merge_asof by period_end_date (분기말 as-of 종가)
8. concat(long_fin + long_px) → panel_long 저장
9. _append_features()              ← features.compute_features() → 파생 46종 append
10. CREATE INDEX ix_panel_tid, ix_panel_item
11. panel.export_csv()             ← panel_long.csv 갱신
```

### 5.2 `features.compute_features()` 전처리 가드

| 대상 | 가드 | 이유 |
|---|---|---|
| `capex` | `.abs()` | 현금유출 부호 기업마다 상이 |
| DIO/DSO/DPO | `_clean_days()`: [0, 500]일 밖 → NaN | 음수 = 회계 아티팩트; >500 = 분모 근-0 아티팩트 |
| 성장률 QoQ/YoY | `_winsor_growth()`: \|x\| > 5.0 → NaN | 기준 분기 극소값에서 발생하는 수천% 스파이크 |
| ratio 계열 (9종) | `get_feature()` 호출 시 winsor=(0.02, 0.98) | 극단 분기 클리핑 (저장 시 적용 안 함) |

### 5.3 `panel.py` — 분석 접근 레이어

```python
# 기본 사용
long = P.load_long()                                  # CSV 우선, DB fallback
s    = P.get_series(long, 'NVDA', 'revenue')          # level (기본)

# transform 옵션 (2026-07-29 추가)
s_log = P.get_series(long, 'NVDA', 'revenue', transform='log')        # VECM용 log
s_zs  = P.get_series(long, 'NVDA', 'revenue', transform='zscore')     # 표준화
s_gq  = P.get_series(long, 'NVDA', 'revenue', transform='growth_qoq') # QoQ
s_gy  = P.get_series(long, 'NVDA', 'revenue', transform='growth_yoy') # YoY

# wide-format (2026-07-29 transform 파라미터 추가)
wide     = P.to_wide('revenue', transform='log')                       # 전체
balanced = P.to_wide_balanced('revenue', min_quarters=20, transform='log')  # 균형 패널
print(balanced.excluded)   # 제외된 ticker 목록
```

**`to_wide_balanced()` 기본값 min_quarters=20** = 5년치 분기 (VECM 최소 추정 가능 수준).  
현재 기준 121개사 중 60개사가 ≥20분기 커버리지 보유.

---

## 6. GEM 개발 로드맵과 데이터 상태

| Step | 목표 | 데이터 요구사항 | 상태 |
|---|---|---|---|
| **Step 0** | panel_long + features | 원본 재무 + 파생 46종 | ✅ 완료 |
| **Step 1** | Lead-lag 매트릭스 스캐너 | 정제된 features, calendar 정렬 | ✅ 완료 |
| **Step 2** | 방정식 명세 (`equations.py`) | Step 1 매트릭스 + 전처리 완결 | ⏭ 다음 |
| **Step 3** | VECM 시스템 추정 | `to_wide_balanced(transform='log')` | ⏳ |
| **Step 4** | 회계 항등식 Closure | FCF=OCF−capex 등 | ⏳ |
| **Step 5** | 시뮬레이션·검증 | 전체 파이프라인 재현 가능 | ⏳ |

---

## 7. 데이터 품질 현황 (2026-07-29 기준)

### 7.1 커버리지

| 지표 | 수치 |
|---|---|
| quarterly_financials 기업 수 | 121개사 |
| 분기 범위 | 2016 Q1 ~ 2027 Q1 |
| panel_long 총 행 수 | 69,316행 |
| stock_prices 기업 수 | 135개사 (14개 재무 미수집) |

### 7.2 알려진 NULL 현황

| 컬럼 | NULL 수 | 원인 | 처리 방침 |
|---|---|---|---|
| `accounts_payable_usd_m` | 84행 (~4%) | EDGAR 수집 미완료 | `add_payables_edgar.py` 순차 보강 |
| `inventory_usd_m` | 404행 (~18%) | 소프트웨어·유틸리티 구조적 제로 포함 | `null_policy` 적용 후 0 채우기 |

### 7.3 균형 패널 현황

`to_wide_balanced(min_quarters=20)` 기준:
- 포함: 60개사 (≥5년 데이터)
- 제외: 61개사 (신규 상장, 아시아 거래소 데이터 부족 등)

VECM Step 3에서는 **balanced 60개사 기준** 추정 권장.

---

## 8. 파일 역할 인덱스

| 파일 | 역할 | 실행 시점 |
|---|---|---|
| `edgar_financials.py` | SEC EDGAR API → quarterly_financials 수집 | 어닝 시즌 후 |
| `add_payables_edgar.py` | AP 컬럼 EDGAR 보강 | accounts_payable NULL 해소 |
| `refresh_financials.py` | 전체 재무 갱신 | 분기별 |
| `setup_null_policy.py` | null_policy 테이블 초기화 | 최초 1회 + 업데이트 시 |
| `build_panel_long.py` | **panel_long 전체 재빌드** | 재무 갱신 후 |
| `panel.py` | 분석 데이터 접근 레이어 | import로 사용 |
| `features.py` | 파생지표 계산 엔진 | import로 사용 |
| `leadlag.py` | 시차상관·Granger 공통 통계 | 분석 스크립트에서 import |
| `leadlag_matrix.py` | 전체 지표쌍 lead-lag 스캐너 | Step 1 |
| `vecm.py` | VECM 시스템 추정 | Step 3 |
| `ecm.py` | ECM 장·단기 탄력성 | Step 3 맹아 |

---

## 9. 운영 절차

### 어닝 시즌 후 데이터 갱신

```bash
cd agents/data/dba

# 1. 재무 데이터 수집
python3 edgar_financials.py        # SEC EDGAR 수집

# 2. AP 보강 (accounts_payable NULL 해소)
python3 add_payables_edgar.py

# 3. panel_long 재빌드 (백업 자동 생성)
python3 build_panel_long.py

# 4. 분석 재실행
python3 leadlag_matrix.py
python3 vecm.py
```

### null_policy 업데이트

```bash
# setup_null_policy.py의 POLICY 리스트 수정 후
python3 setup_null_policy.py
python3 build_panel_long.py        # null_policy 적용해 재빌드
```

### 데이터 품질 점검

```python
import sqlite3, pandas as pd
con = sqlite3.connect('financials.db')

# NULL 현황
pd.read_sql_query("""
    SELECT
        SUM(CASE WHEN revenue_usd_m IS NULL THEN 1 ELSE 0 END) rev_null,
        SUM(CASE WHEN accounts_payable_usd_m IS NULL THEN 1 ELSE 0 END) ap_null,
        SUM(CASE WHEN inventory_usd_m IS NULL THEN 1 ELSE 0 END) inv_null,
        COUNT(*) total
    FROM quarterly_financials
""", con)

# panel_long 균형 점검
pd.read_sql_query("""
    SELECT section, COUNT(DISTINCT ticker) companies,
           COUNT(DISTINCT date) quarters
    FROM panel_long WHERE item='revenue'
    GROUP BY section ORDER BY section
""", con)
```

---

## 10. 설계 원칙 요약

1. **단일 진실 소스(SSOT)**: `financials.db/panel_long`이 정본. CSV/xlsx는 export 산출물.
2. **계층 분리**: 원본(quarterly_financials) → 파생(panel_long) → 분석(leadlag, vecm). 계층 간 역방향 의존 없음.
3. **재현 가능성**: `build_panel_long.py` 한 번 실행으로 전체 panel_long 재생성. 스크립트 의존 순서: setup_null_policy → edgar_financials → add_payables → build_panel_long.
4. **전처리 가드**: 분석 결과를 오염시키는 아티팩트(음수 DIO, 수천% 성장률)는 저장 시점에 NaN 처리. 다운스트림 분석 코드는 이를 믿고 추가 처리 불필요.
5. **calendar 정렬 우선**: 모든 날짜는 캘린더 분기말로 정규화. 비표준 결산 기업도 동일 그리드.
