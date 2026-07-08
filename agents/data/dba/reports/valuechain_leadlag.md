# AI 밸류체인 고객→공급사 Lead-Lag 분석 (현금흐름 관점)

**분석일:** 2026-07-09  ·  **데이터:** `panel_long` (분기 재무, 2016–2027)  ·  **엔진:** `valuechain.py` + `leadlag.py`

**방법:** 섹션 집계 신호(구성사 매출 합)의 YoY를 z-score → 시차상관(±4분기) + Granger 인과. 가설: **고객(customer)의 활동이 공급사(supplier) 매출을 선행**한다.

## 0. 요약

- 분석 대상 엣지: **24개** × 재무관점 **3종** = 72 케이스

- 데이터 부족(foundry·ODM 등)으로 분석 불가: **28 케이스**

- '고객 선행' 가설이 통계적으로 지지된 케이스(유의, lead>0): **6건**


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
| Hyperscaler | AI Chip | **+1** | Hyperscaler | 0.437 | 0.0158 | 0.2649 | 0.383 | 고객 선행 (가설지지) |
| Server OEM | AI Chip | **+2** | Server OEM | 0.596 | 0.0007 | 0.0007 | 0.602 | 고객 선행 (가설지지) |
| Server OEM | CPU | +0 | — | 0.337 | 0.0791 | 0.9598 | 0.327 | 동시(리드 없음) |
| Hyperscaler | CPU | **-2** | CPU | 0.654 | 0.0003 | 0.8499 | 0.213 | 공급사 선행 (역방향) |
| AI Chip | DRAM | **+0** | — | 0.633 | 0.0002 | 0.2313 | 0.653 | 동시(리드 없음) |
| Hyperscaler | DRAM | +1 | Hyperscaler | 0.217 | 0.2669 | 0.6528 | 0.055 | 고객 선행(약함) |
| Server OEM | DRAM | **+1** | Server OEM | 0.612 | 0.0005 | 0.0017 | 0.575 | 고객 선행 (가설지지) |
| Hyperscaler | NAND | +2 | Hyperscaler | 0.328 | 0.0888 | 0.3561 | 0.976 | 고객 선행(약함) |
| Server OEM | NAND | +4 | Server OEM | 0.06 | 0.7707 | 0.6994 | 0.091 | 고객 선행(약함) |
| AI Chip | NAND | — | — | — | — | — | — | 양(+)의 상관 피크 없음 |
| Foundry | HW Equipment | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| DRAM | HW Equipment | -3 | HW Equipment | 0.297 | 0.1401 | 0.3718 | 0.283 | 공급사 선행(약함) |
| CPU | HW Equipment | +4 | CPU | 0.267 | 0.1875 | 0.7695 | 0.005 | 고객 선행(약함) |
| AI Chip | OSAT/Packaging | -1 | OSAT/Packaging | 0.182 | 0.3625 | 0.6242 | 0.179 | 공급사 선행(약함) |
| CPU | OSAT/Packaging | +3 | CPU | 0.358 | 0.0793 | 0.4208 | 0.336 | 고객 선행(약함) |
| Hyperscaler | Server Networking | **+1** | Hyperscaler | 0.801 | 0.0 | 0.0055 | 0.487 | 고객 선행 (가설지지) |
| Server OEM | Server Networking | -1 | Server Networking | 0.206 | 0.2751 | 0.1845 | 0.334 | 공급사 선행(약함) |
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
| Hyperscaler | AI Chip | **+0** | — | 0.659 | 0.0001 | 0.9291 | 0.636 | 동시(리드 없음) |
| Server OEM | AI Chip | +2 | Server OEM | 0.123 | 0.5242 | 0.4577 | 0.121 | 고객 선행(약함) |
| Server OEM | CPU | +4 | Server OEM | 0.299 | 0.1562 | 0.6288 | 0.286 | 고객 선행(약함) |
| Hyperscaler | CPU | +4 | Hyperscaler | 0.2 | 0.349 | 0.4929 | 1.465 | 고객 선행(약함) |
| AI Chip | DRAM | **+0** | — | 0.501 | 0.0056 | 0.4029 | 0.508 | 동시(리드 없음) |
| Hyperscaler | DRAM | **+0** | — | 0.653 | 0.0002 | 0.0218 | 0.651 | 동시(리드 없음) |
| Server OEM | DRAM | +4 | Server OEM | 0.368 | 0.0704 | 0.102 | 0.352 | 고객 선행(약함) |
| Hyperscaler | NAND | +4 | Hyperscaler | 0.227 | 0.2645 | 0.8935 | 1.759 | 고객 선행(약함) |
| Server OEM | NAND | **+4** | Server OEM | 0.439 | 0.0248 | 0.7764 | 0.427 | 고객 선행 (가설지지) |
| AI Chip | NAND | +2 | AI Chip | 0.014 | 0.9435 | 0.9013 | 0.014 | 고객 선행(약함) |
| Foundry | HW Equipment | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| DRAM | HW Equipment | -3 | HW Equipment | 0.178 | 0.3831 | 0.0701 | 0.156 | 공급사 선행(약함) |
| CPU | HW Equipment | +3 | CPU | 0.262 | 0.1873 | 0.9286 | 0.007 | 고객 선행(약함) |
| AI Chip | OSAT/Packaging | -2 | OSAT/Packaging | 0.345 | 0.0843 | 0.7598 | 0.348 | 공급사 선행(약함) |
| CPU | OSAT/Packaging | +0 | — | 0.371 | 0.0516 | 0.2465 | 0.371 | 동시(리드 없음) |
| Hyperscaler | Server Networking | **+0** | — | 0.434 | 0.0186 | 0.0598 | 0.21 | 동시(리드 없음) |
| Server OEM | Server Networking | +3 | Server OEM | 0.298 | 0.1241 | 0.1222 | 0.296 | 고객 선행(약함) |
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
| Hyperscaler | AI Chip | **+0** | — | 0.636 | 0.0002 | 0.6947 | 0.614 | 동시(리드 없음) |
| Server OEM | AI Chip | +0 | — | 0.485 | 0.2227 | nan | 0.69 | 동시(리드 없음) |
| Server OEM | CPU | — | — | — | — | — | — | 양(+)의 상관 피크 없음 |
| Hyperscaler | CPU | -1 | CPU | 0.233 | 0.243 | 0.9901 | 0.23 | 공급사 선행(약함) |
| AI Chip | DRAM | — | — | — | — | — | — | 양(+)의 상관 피크 없음 |
| Hyperscaler | DRAM | **+0** | — | 0.85 | 0.0 | 0.0698 | 0.862 | 동시(리드 없음) |
| Server OEM | DRAM | +0 | — | 0.372 | 0.3639 | nan | 0.524 | 동시(리드 없음) |
| Hyperscaler | NAND | **+1** | Hyperscaler | 0.393 | 0.0352 | 0.2292 | 0.417 | 고객 선행 (가설지지) |
| Server OEM | NAND | — | — | — | — | — | — | 양(+)의 상관 피크 없음 |
| AI Chip | NAND | -4 | NAND | 0.191 | 0.6502 | nan | 0.211 | 공급사 선행(약함) |
| Foundry | HW Equipment | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| DRAM | HW Equipment | -3 | HW Equipment | 0.312 | 0.4526 | nan | 20.386 | 공급사 선행(약함) |
| CPU | HW Equipment | +2 | CPU | 0.482 | 0.2263 | nan | 0.01 | 고객 선행(약함) |
| AI Chip | OSAT/Packaging | **-1** | OSAT/Packaging | 0.719 | 0.0442 | nan | 0.824 | 공급사 선행 (역방향) |
| CPU | OSAT/Packaging | -4 | OSAT/Packaging | 0.297 | 0.4749 | nan | 0.235 | 공급사 선행(약함) |
| Hyperscaler | Server Networking | **+0** | — | 0.674 | 0.0001 | 0.0453 | 0.326 | 동시(리드 없음) |
| Server OEM | Server Networking | **+0** | — | 0.908 | 0.0018 | nan | 0.423 | 동시(리드 없음) |
| AI Chip | Foundry | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| CPU | Foundry | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| Server Networking | Foundry | — | — | — | — | — | — | Foundry 데이터 부족(<12분기) |
| CPU | Server ODM | — | — | — | — | — | — | Server ODM 데이터 부족(<12분기) |
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
