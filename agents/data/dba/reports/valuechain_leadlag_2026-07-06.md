# AI 밸류체인 고객→공급사 Lead-Lag 분석 (현금흐름 관점)

**분석일:** 2026-07-06  ·  **데이터:** `panel_long` (분기 재무, 2016–2027)  ·  **엔진:** `valuechain.py` + `leadlag.py`

**방법:** 섹션 집계 신호(구성사 매출 합)의 YoY를 z-score → 시차상관(±4분기) + Granger 인과. 가설: **고객(customer)의 활동이 공급사(supplier) 매출을 선행**한다.

## 0. 요약

- 분석 대상 엣지: **23개** × 재무관점 **3종** = 69 케이스

- 데이터 부족(foundry·ODM 등)으로 분석 불가: **30 케이스**

- '고객 선행' 가설이 통계적으로 지지된 케이스(유의, lead>0): **9건**


## 1. 섹션 구성 (집계에 쓰인 회사)

| 섹션 | 집계 회사 | 상태 |
|---|---|---|
| Hyperscaler | AMZN, GOOGL, MSFT, ORCL | ✅ |
| AI Chip | AMD, MRVL, NVDA, QCOM | ✅ |
| CPU | INTC | ✅ |
| DRAM | MU | ✅ |
| NAND | STX, WDC | ✅ |
| Foundry | — | ⚠️ 데이터 부족 |
| HW Equipment | AMAT, FORM, KLAC, LRCX, MKSI, ONTO | ✅ |
| OSAT/Packaging | AMKR | ✅ |
| Server Networking | AAOI, ANET, AVGO, COHR, CRDO, CSCO, FN, LITE, MTSI, SMTC | ✅ |
| Server OEM | DELL, HPE, SMCI | ✅ |
| Server ODM | — | ⚠️ 데이터 부족 |

## 2. 관점: 매출→매출 (수요전달)  (`revenue`→`revenue`)

| 고객(X) | 공급사(Y) | best lag(분기) | 리더 | corr | p | Granger C→S | β | 판정 |
|---|---|---|---|---|---|---|---|---|
| Hyperscaler | AI Chip | **+2** | Hyperscaler | 0.392 | 0.0354 | 0.3266 | 0.332 | 고객 선행 (가설지지) |
| Server OEM | AI Chip | **+1** | Server OEM | 0.513 | 0.0038 | 0.0019 | 0.519 | 고객 선행 (가설지지) |
| Server OEM | CPU | +0 | — | 0.335 | 0.0819 | 0.9289 | 0.324 | 동시(리드 없음) |
| Hyperscaler | CPU | +1 | Hyperscaler | 0.375 | 0.0538 | 0.2113 | 1.29 | 고객 선행(약함) |
| AI Chip | DRAM | **+1** | AI Chip | 0.63 | 0.0004 | 0.3503 | 0.64 | 고객 선행 (가설지지) |
| Hyperscaler | DRAM | **+1** | Hyperscaler | 0.478 | 0.0117 | 0.4652 | 1.628 | 고객 선행 (가설지지) |
| Hyperscaler | NAND | +3 | Hyperscaler | 0.224 | 0.2606 | 0.8126 | 0.785 | 고객 선행(약함) |
| Server OEM | NAND | +4 | Server OEM | 0.06 | 0.7707 | 0.6994 | 0.091 | 고객 선행(약함) |
| AI Chip | NAND | — | — | — | — | — | — | 양(+)의 상관 피크 없음 |
| Foundry | HW Equipment | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| DRAM | HW Equipment | -3 | HW Equipment | 0.179 | 0.392 | 0.3222 | 0.169 | 공급사 선행(약함) |
| CPU | HW Equipment | +4 | CPU | 0.267 | 0.1875 | 0.7695 | 0.005 | 고객 선행(약함) |
| AI Chip | OSAT/Packaging | -1 | OSAT/Packaging | 0.224 | 0.2607 | 0.6242 | 0.219 | 공급사 선행(약함) |
| CPU | OSAT/Packaging | +3 | CPU | 0.358 | 0.0793 | 0.4208 | 0.337 | 고객 선행(약함) |
| Hyperscaler | Server Networking | **+2** | Hyperscaler | 0.757 | 0.0 | 0.0064 | 0.538 | 고객 선행 (가설지지) |
| Server OEM | Server Networking | +1 | Server OEM | 0.206 | 0.2745 | 0.1779 | 0.197 | 고객 선행(약함) |
| AI Chip | Foundry | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| CPU | Foundry | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| Server Networking | Foundry | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| CPU | Server ODM | — | — | — | — | — | — | Server ODM 데이터 부족(<12분기) |
| DRAM | Server ODM | — | — | — | — | — | — | Server ODM 데이터 부족(<12분기) |
| NAND | Server ODM | — | — | — | — | — | — | Server ODM 데이터 부족(<12분기) |
| AI Chip | Server ODM | — | — | — | — | — | — | Server ODM 데이터 부족(<12분기) |

## 2. 관점: 매출원가→매출 (구매흐름)  (`cogs`→`revenue`)

| 고객(X) | 공급사(Y) | best lag(분기) | 리더 | corr | p | Granger C→S | β | 판정 |
|---|---|---|---|---|---|---|---|---|
| Hyperscaler | AI Chip | **+0** | — | 0.709 | 0.0 | 0.0755 | 0.681 | 동시(리드 없음) |
| Server OEM | AI Chip | +2 | Server OEM | 0.071 | 0.7141 | 0.6227 | 0.07 | 고객 선행(약함) |
| Server OEM | CPU | +4 | Server OEM | 0.29 | 0.1695 | 0.5595 | 0.278 | 고객 선행(약함) |
| Hyperscaler | CPU | +4 | Hyperscaler | 0.191 | 0.3702 | 0.4722 | 1.405 | 고객 선행(약함) |
| AI Chip | DRAM | **+1** | AI Chip | 0.456 | 0.0169 | 0.7892 | 0.453 | 고객 선행 (가설지지) |
| Hyperscaler | DRAM | **+1** | Hyperscaler | 0.721 | 0.0 | 0.0409 | 0.701 | 고객 선행 (가설지지) |
| Hyperscaler | NAND | +4 | Hyperscaler | 0.227 | 0.2645 | 0.8935 | 1.759 | 고객 선행(약함) |
| Server OEM | NAND | **+4** | Server OEM | 0.439 | 0.0248 | 0.7764 | 0.427 | 고객 선행 (가설지지) |
| AI Chip | NAND | +1 | AI Chip | 0.018 | 0.925 | 0.8926 | 0.019 | 고객 선행(약함) |
| Foundry | HW Equipment | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| DRAM | HW Equipment | -3 | HW Equipment | 0.0 | 0.9985 | 0.0744 | 0.0 | 공급사 선행(약함) |
| CPU | HW Equipment | +3 | CPU | 0.262 | 0.1873 | 0.854 | 0.007 | 고객 선행(약함) |
| AI Chip | OSAT/Packaging | -2 | OSAT/Packaging | 0.305 | 0.1301 | 0.7598 | 0.308 | 공급사 선행(약함) |
| CPU | OSAT/Packaging | +0 | — | 0.371 | 0.057 | 0.2495 | 0.373 | 동시(리드 없음) |
| Hyperscaler | Server Networking | **+0** | — | 0.435 | 0.0184 | 0.0903 | 0.21 | 동시(리드 없음) |
| Server OEM | Server Networking | +3 | Server OEM | 0.301 | 0.12 | 0.1233 | 0.299 | 고객 선행(약함) |
| AI Chip | Foundry | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| CPU | Foundry | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| Server Networking | Foundry | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| CPU | Server ODM | — | — | — | — | — | — | Server ODM 데이터 부족(<12분기) |
| DRAM | Server ODM | — | — | — | — | — | — | Server ODM 데이터 부족(<12분기) |
| NAND | Server ODM | — | — | — | — | — | — | Server ODM 데이터 부족(<12분기) |
| AI Chip | Server ODM | — | — | — | — | — | — | Server ODM 데이터 부족(<12분기) |

## 2. 관점: capex→매출 (투자흐름)  (`capex`→`revenue`)

| 고객(X) | 공급사(Y) | best lag(분기) | 리더 | corr | p | Granger C→S | β | 판정 |
|---|---|---|---|---|---|---|---|---|
| Hyperscaler | AI Chip | **+0** | — | 0.667 | 0.0001 | 0.4135 | 0.641 | 동시(리드 없음) |
| Server OEM | AI Chip | +0 | — | 0.577 | 0.1342 | nan | 0.811 | 동시(리드 없음) |
| Server OEM | CPU | — | — | — | — | — | — | 양(+)의 상관 피크 없음 |
| Hyperscaler | CPU | -1 | CPU | 0.207 | 0.2996 | 0.6457 | 0.205 | 공급사 선행(약함) |
| AI Chip | DRAM | — | — | — | — | — | — | 양(+)의 상관 피크 없음 |
| Hyperscaler | DRAM | **+1** | Hyperscaler | 0.782 | 0.0 | 0.3206 | 0.809 | 고객 선행 (가설지지) |
| Hyperscaler | NAND | +1 | Hyperscaler | 0.363 | 0.0526 | 0.2709 | 0.387 | 고객 선행(약함) |
| Server OEM | NAND | — | — | — | — | — | — | 양(+)의 상관 피크 없음 |
| AI Chip | NAND | -4 | NAND | 0.215 | 0.6099 | nan | 0.236 | 공급사 선행(약함) |
| Foundry | HW Equipment | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| DRAM | HW Equipment | -3 | HW Equipment | 0.312 | 0.4526 | nan | 20.386 | 공급사 선행(약함) |
| CPU | HW Equipment | — | — | — | — | — | — | CPU 데이터 부족(<12분기) |
| AI Chip | OSAT/Packaging | **-1** | OSAT/Packaging | 0.709 | 0.0488 | nan | 0.813 | 공급사 선행 (역방향) |
| CPU | OSAT/Packaging | — | — | — | — | — | — | CPU 데이터 부족(<12분기) |
| Hyperscaler | Server Networking | **+0** | — | 0.637 | 0.0002 | 0.0581 | 0.308 | 동시(리드 없음) |
| Server OEM | Server Networking | **+0** | — | 0.911 | 0.0016 | nan | 0.419 | 동시(리드 없음) |
| AI Chip | Foundry | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| CPU | Foundry | — | — | — | — | — | — | CPU 데이터 부족(<12분기) |
| Server Networking | Foundry | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| CPU | Server ODM | — | — | — | — | — | — | CPU 데이터 부족(<12분기) |
| DRAM | Server ODM | — | — | — | — | — | — | Server ODM 데이터 부족(<12분기) |
| NAND | Server ODM | — | — | — | — | — | — | Server ODM 데이터 부족(<12분기) |
| AI Chip | Server ODM | — | — | — | — | — | — | Server ODM 데이터 부족(<12분기) |

## 3. 해석 가이드

- **best lag > 0** ⇒ 고객이 공급사를 그만큼 분기 선행 (수요가 먼저 → 매출로 전달).

- **p < 0.05** ⇒ 해당 시차의 상관이 통계적으로 유의.

- **Granger C→S < 0.05 이고 < S→C** ⇒ 인과 방향이 고객→공급사로 확인.

- **β** = 전달 강도(고객 1σ 변화가 공급사에 전달되는 비율).


## 4. 한계

- Foundry(TSM 등)·Server ODM(대만 ODM)은 이 DB에서 12분기 미만 → 신호 생성 불가, 해당 엣지 전부 '데이터 부족'.

- 섹션당 대표사가 1개인 경우(cpu=INTC, dram=MU, osat=AMKR) 집계=단일사.

- 지급어음(payables) 컬럼이 없어 순수 현금전환주기는 다루지 않음(별도 리포트 참조).

- lead-lag는 통계적 선행일 뿐 계약관계 증명이 아님 → 상위 후보는 SPLC/10-K로 교차검증.
