# 밸류체인 보편 현금흐름 관계 발굴

**분석일:** 2026-07-08 · **데이터:** `panel_long.csv` · **엔진:** `universal.py`

각 변수쌍×변환이 밸류체인 엣지에서 기업쌍 유의로 얼마나 보편적으로 성립하는지. 보편성 = 성립 엣지 / 분석가능 엣지. 높을수록 전 섹터 적용 가능(→ VECM 채널 후보).


## 보편성 랭킹

| 채널 | X | Y | 보편성 | 성립/가능 엣지 | 유의쌍/전체 | 평균 r | 평균시차 |
|---|---|---|---|---|---|---|---|
| 수요 매출→매출 [rolling_yoy] | `REVENUE[rolling_yoy]` | `REVENUE[rolling_yoy]` | **1.0** | 15/15 | 96/137 | 0.625 | 2.26 |
| 결제 AP→매출 [qoq] | `AP[growth_qoq]` | `REVENUE[growth_qoq]` | **1.0** | 15/15 | 91/147 | 0.577 | 1.39 |
| 결제 AP→매출 [rolling_yoy] | `AP[rolling_yoy]` | `REVENUE[rolling_yoy]` | **1.0** | 15/15 | 89/137 | 0.66 | 1.98 |
| 재고→매출 [rolling_yoy] | `INVENTORY[rolling_yoy]` | `REVENUE[rolling_yoy]` | **1.0** | 15/15 | 87/120 | 0.672 | 1.98 |
| 수요 매출→매출 [yoy] | `REVENUE[growth_yoy]` | `REVENUE[growth_yoy]` | **1.0** | 15/15 | 76/144 | 0.532 | 1.74 |
| 재고→매출 [yoy] | `INVENTORY[growth_yoy]` | `REVENUE[growth_yoy]` | **1.0** | 15/15 | 69/123 | 0.577 | 2.06 |
| 재고→매출 [qoq] | `INVENTORY[growth_qoq]` | `REVENUE[growth_qoq]` | **1.0** | 15/15 | 64/130 | 0.492 | 1.51 |
| 구매 COGS→매출 [rolling_yoy] | `COGS[rolling_yoy]` | `REVENUE[rolling_yoy]` | **1.0** | 13/13 | 51/69 | 0.652 | 2.43 |
| 미지급→미수 | `AP_TO_COGS[level]` | `AR_TO_REVENUE[level]` | **1.0** | 13/13 | 32/70 | 0.517 | 1.34 |
| 투자 capex→매출 [rolling_yoy] | `CAPEX[rolling_yoy]` | `REVENUE[rolling_yoy]` | **1.0** | 5/5 | 28/46 | 0.671 | 1.42 |
| 투자 capex→매출 [yoy] | `CAPEX[growth_yoy]` | `REVENUE[growth_yoy]` | **1.0** | 5/5 | 23/49 | 0.627 | 0.92 |
| 결제 AP→매출 [yoy] | `AP[growth_yoy]` | `REVENUE[growth_yoy]` | **0.933** | 14/15 | 80/144 | 0.584 | 1.58 |
| 구매 COGS→매출 [yoy] | `COGS[growth_yoy]` | `REVENUE[growth_yoy]` | **0.923** | 12/13 | 38/71 | 0.548 | 1.48 |
| 수요 매출→매출 [qoq] | `REVENUE[growth_qoq]` | `REVENUE[growth_qoq]` | **0.867** | 13/15 | 104/147 | 0.538 | 0.68 |
| 지급→회수 DPO→DSO | `DPO[level]` | `DSO[level]` | **0.846** | 11/13 | 35/70 | 0.533 | 1.36 |
| 투자 capex→매출 [qoq] | `CAPEX[growth_qoq]` | `REVENUE[growth_qoq]` | **0.8** | 4/5 | 32/50 | 0.6 | 0.45 |
| 현금여력→매출 | `FCF_MARGIN[level]` | `REVENUE[growth_yoy]` | **0.8** | 4/5 | 8/34 | 0.583 | 1.65 |
| 구매 COGS→매출 [qoq] | `COGS[growth_qoq]` | `REVENUE[growth_qoq]` | **0.692** | 9/13 | 43/76 | 0.582 | 0.97 |

## 해석

- **보편성 1.0** = 분석가능한 모든 엣지에서 유의 기업쌍 존재 → 전 밸류체인 공통 채널.

- 평균시차 = 유의 기업쌍들의 평균 선행 분기.

- 상위 채널이 전체 공급망 자금흐름 해석 + VECM mini-GEM(5)의 방정식 우변 후보.


## 한계
- 기업쌍 표본 24~34분기, 실제 거래 미확인(SPLC 없음). 다중비교 주의.
- Foundry·ODM은 데이터 부족(나중에 쌓이면 자동 반영).
