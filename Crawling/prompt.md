# Price Intelligence System — 운영 가이드

## 시스템 목표
Samsung SSD 제품군(Portable/Internal/microSD) + 경쟁사(SanDisk, Lexar) 가격을
Amazon(US/JP/DE) 및 제조사 공식 사이트에서 하루 2회 자동 수집 → PostgreSQL 히스토리 DB → Streamlit 대시보드.

---

## 실행 방법

```bash
# 수동 실행 (US)
cd /Users/idongseong/Claude/Crawling
python run_pipeline.py --country US

# 다국가 실행
python run_pipeline.py --country US JP DE

# 특정 소스만
python run_pipeline.py --country US --source amazon

# 대시보드
streamlit run dashboard/app.py

# cron: 매일 09:00 / 21:00 자동 실행
# 0 9,21 * * * /Users/idongseong/Claude/Crawling/run_pipeline.sh
```

---

## 제품 카탈로그 현황

### Samsung (`catalog/samsung.json`) — 28 SKUs

| 카테고리 | 제품 | 용량 |
|---|---|---|
| Portable SSD | T9 | 1TB / 2TB / 4TB |
| Portable SSD | T7 Shield | 1TB / 2TB |
| Portable SSD | T7 | 500GB / 1TB / 2TB |
| Internal SSD | 9100 Pro (PCIe 5.0) | 1TB / 2TB / 4TB / 8TB |
| Internal SSD | 990 Pro (PCIe 4.0) | 1TB / 2TB / 4TB |
| Internal SSD | 990 Evo Plus | 1TB / 2TB / 4TB |
| microSD | EVO Select | 128GB / 256GB / 512GB |
| microSD | PRO Plus | 128GB / 256GB / 512GB |
| microSD | PRO Endurance | 128GB / 256GB |
| microSD | P9 Express | 256GB / 512GB |

**다국가 URL 현황:**
- T9 1TB: US Amazon ✅ / JP Amazon ✅ / DE Amazon ✅ / US 제조사 ✅
- T7 Shield 1TB: US Amazon ✅ / US 제조사 ✅
- 990 Pro 2TB: US Amazon ✅ / JP Amazon ✅ / DE Amazon ✅
- 9100 Pro 2TB: US Amazon ✅ / JP Amazon ✅
- 나머지 제품: US Amazon 위주

### 경쟁사 (`catalog/competitors.json`) — SanDisk + Lexar

#### SanDisk Portable SSD
| 제품 | 용량 |
|---|---|
| Extreme | 1TB / 2TB / 4TB |
| Extreme Pro | 1TB / 2TB / 4TB |

#### SanDisk Internal SSD (레거시 → Optimus 전환 중)
| 제품 | 용량 | 상태 |
|---|---|---|
| WD_BLACK SN850X | 1TB / 2TB / 4TB | 판매 중 (Optimus GX PRO 850X로 교체 예정) |
| WD_BLACK SN770 | 1TB / 2TB | 판매 중 (Optimus GX 7100으로 교체 예정) |
| **Optimus GX PRO 8100** (PCIe 5.0) | 1TB / 2TB / 4TB / 8TB | ✅ Amazon US 판매 중 (CES 2026 신제품, 9100 Pro 경쟁) |
| **Optimus GX PRO 850X** (PCIe 4.0) | 1TB / 2TB / 4TB | 4TB: Amazon US ✅ / 1TB·2TB: 제조사 직판만 |
| **Optimus GX 7100** (PCIe 4.0) | 1TB / 2TB | 제조사 직판만 (2026 H1 Amazon 출시 예정) |

#### SanDisk microSD
Extreme / Extreme Pro / Ultra (128GB ~ 1TB)

#### Lexar
| 카테고리 | 제품 |
|---|---|
| Portable SSD | SL500 (1TB/2TB), SL600 (1TB/2TB) |
| Internal SSD | NM790 (1TB/2TB/4TB), NM800 Pro (1TB/2TB) |
| microSD | PLAY (256GB/512GB/1TB), Professional 1800x, Gold |

---

## 파이프라인 8단계

```
CatalogValidation → FetchRaw → ParseExtract → Normalize → QualityGate → HITLTriage → LoadDB → Report
```

### 에이전트 역할 요약

| 에이전트 | 파일 | 역할 |
|---|---|---|
| Orchestrator | run_pipeline.py | DAG 실행, 단계 조율 |
| CatalogValidation | agents/catalog_validator.py | SKU↔URL 유효성 검사 |
| FetchRaw | agents/fetch_raw.py | Playwright 크롤링, HTML 저장, content_hash |
| ParseExtract | agents/parse_extract.py | HTML → 가격 데이터 추출 |
| Normalize | agents/normalizer.py | 통화/숫자/로케일 정규화 |
| QualityGate | agents/quality_gate.py | accept / quarantine 분리 |
| HITLTriage | agents/hitl_triage.py | P0/P1 큐 생성 |
| LoadDB | agents/load_db.py | PostgreSQL 멱등 적재 |

---

## 품질 게이트 규칙

| 조건 | 처리 |
|---|---|
| `parse_confidence < 0.7` | quarantine (P0 HITL) |
| `price <= 0` | quarantine (P0 HITL) |
| `currency is null` | quarantine (P0 HITL) |
| `±30% 급변` | flag + 통과 (P1 HITL) |

---

## 알려진 이슈 및 현재 상태

### Amazon 봇 차단 (가장 큰 이슈)
- **현상**: 전체 요청의 ~75% blocked_captcha (status 999)
- **완화책**:
  1. 요청 간 5~15초 랜덤 딜레이
  2. User-Agent 로테이션 (Chrome/Safari/Windows)
  3. Playwright 컨텍스트에 `i18n-prefs=USD` 쿠키 설정 (한국 IP에서 USD 강제)
- **미해결**: IP 기반 차단은 근본적으로 해결 불가 (VPN 또는 Keepa API 검토 필요)
- **Keepa API 고려**: Amazon 가격을 100% 안정적으로 수집 가능한 유료 API (~$19/월)

### 제조사 사이트 파싱
- Samsung.com: `.price-display`, JSON-LD 파서 구현됨 (URL 정확도 요검증)
- sandisk.com: `.pricing`, structured data 파서 구현됨
- lexar.com: `__NEXT_DATA__` JSON 파서 구현됨
- **주의**: 사이트 구조 변경 시 파싱 실패 → HITL 자동 라우팅

### 다국가 확장 현황
- **US**: 운영 중 (Amazon 기준 ~20-30% 수집 성공)
- **JP/DE**: 카탈로그에 일부 URL 추가됨, 파이프라인 `--country JP DE`로 실행 가능
- **KR**: Amazon.co.kr URL 미확보, 추후 추가 필요

---

## DB 스키마 주요 테이블

- `skus` — 제품 마스터 (sku_id, brand, category, model, capacity)
- `sku_urls` — URL 카탈로그 (sku_id × country × source)
- `price_observations` — 가격 히스토리 append-only
  - 멱등성 키: `(run_id, sku_id, country, source, content_hash)`
- `hitl_queue` — 검토 필요 항목 (P0/P1 우선순위)
- `run_log` — 실행 이력

---

## 멀티 에이전트 시스템 프롬프트

### 0. 공통 원칙
- 절대 추측 금지: 가격이 확실하지 않으면 confidence 낮게 설정
- offer_scope 과장 금지: buybox / top_offers / unknown 중 하나만
- raw evidence(content_hash, raw_path) 반드시 보존
- 데이터 불완전 시 HITL 라우팅

### 1. Orchestrator Agent
입력: RUN_CONTEXT (country, source, run_id)
출력: dag_plan, step_payloads, retry_policy, acceptance_criteria

### 2. Catalog Validation Agent
입력: catalog (samsung.json + competitors.json)
출력: missing_urls, duplicate_urls, suspicious_capacity_mismatch, ready_for_fetch

### 3. Fetch Raw Agent
- Playwright (Chromium, headless)
- Amazon: `i18n-prefs=USD` 쿠키 (한국 IP에서 USD 강제)
- 봇 차단 신호: api-services-support@amazon.com, Robot Check → status 999
- gzip 저장: raw_snapshots/YYYY-MM-DD/sku_id__country__source.html.gz
- content_hash: SHA256 앞 16자

### 4. Parse & Extract Agent
우선순위: JSON-LD → embedded JSON → DOM selector

**Amazon 셀렉터:**
```
span.a-price > span.a-offscreen
#corePriceDisplay_desktop_feature_div .a-offscreen
#apex_desktop .a-price .a-offscreen
.apexPriceToPay .a-offscreen
```

**제조사 파서:**
- samsung.com: `.price-display`, JSON-LD
- sandisk.com / westerndigital.com: `.pricing`, structured data
- lexar.com: `window.__NEXT_DATA__` JSON

### 5. Normalization Agent
통화 감지 순서: raw_string 기호(₩/$) → ISO 코드(KRW/USD) → country 기본값

### 6. Quality Gate Agent
accept 조건: confidence ≥ 0.7, price > 0, currency is not null

### 7. HITL Triage Agent
P0: currency 누락, 파싱 실패, SKU mismatch
P1: ±30% 이상 급격한 가격 변화

### 8. Load DB Agent
멱등성: INSERT ... ON CONFLICT (run_id, sku_id, country, source, content_hash) DO NOTHING

---

## 향후 개선 계획

1. **Keepa API 통합**: Amazon 가격 100% 안정 수집 (봇 차단 해결)
2. **KR Amazon/제조사 URL 추가**: amazon.co.kr + samsung.com/kr
3. **JP/DE 제조사 URL 추가**: amazon.co.jp 수집 품질 향상
4. **Optimus 7100 Amazon 등록 추적**: 2026 H1 출시 시 ASIN 추가
5. **Optimus 850X 1TB/2TB Amazon 추가**: 출시 확인 후 ASIN 추가
