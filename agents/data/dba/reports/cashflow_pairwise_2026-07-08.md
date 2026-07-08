# 기업간(bottom-up) 가중 현금흐름 Lead-Lag

**분석일:** 2026-07-08 · **채널:** `AP_GROWTH→REVENUE` · **가중:** `composite`

섹터 집계 대신 기업쌍(고객사×공급사) lead-lag를 구해 가중 종합. 가중시차 = 유의 기업쌍들의 가중평균 시차.


- 엣지 24 · 종합가능 15 · 유의쌍 2+ 11


| 고객 | 공급사 | 가중시차(분기) | 가중 r | 유의쌍/전체 | 대표 기업쌍 |
|---|---|---|---|---|---|
| Hyperscaler | AI Chip | **0.22** | 0.612 | 8/16 | ORCL→NVDA |
| Server OEM | AI Chip | **1.06** | 0.631 | 5/12 | SMCI→NVDA |
| Server OEM | CPU | — | — | — | no significant pair |
| Hyperscaler | CPU | 2.0 | 0.485 | 1/4 | GOOGL→INTC |
| AI Chip | DRAM | 0.0 | 0.729 | 1/4 | NVDA→MU |
| Hyperscaler | DRAM | **0.0** | 0.733 | 2/4 | ORCL→MU |
| Server OEM | DRAM | **0.0** | 0.688 | 2/3 | SMCI→MU |
| Hyperscaler | NAND | **0.0** | 0.725 | 5/8 | ORCL→WDC |
| Server OEM | NAND | **0.87** | 0.675 | 6/6 | SMCI→WDC |
| AI Chip | NAND | **0.0** | 0.626 | 4/8 | NVDA→WDC |
| Foundry | HW Equipment | — | — | — | insufficient data |
| DRAM | HW Equipment | **2.31** | 0.464 | 3/6 | MU→LRCX |
| CPU | HW Equipment | **2.29** | 0.489 | 3/6 | INTC→KLAC |
| AI Chip | OSAT/Packaging | 2.0 | 0.401 | 1/4 | NVDA→AMKR |
| CPU | OSAT/Packaging | 2.0 | 0.546 | 1/1 | INTC→AMKR |
| Hyperscaler | Server Networking | **0.19** | 0.566 | 25/36 | MSFT→AVGO |
| Server OEM | Server Networking | **0.7** | 0.593 | 18/27 | DELL→AVGO |
| AI Chip | Foundry | — | — | — | insufficient data |
| CPU | Foundry | — | — | — | insufficient data |
| Server Networking | Foundry | — | — | — | insufficient data |
| CPU | Server ODM | — | — | — | insufficient data |
| DRAM | Server ODM | — | — | — | insufficient data |
| NAND | Server ODM | — | — | — | insufficient data |
| AI Chip | Server ODM | — | — | — | insufficient data |

## 가중치 방식
- equal 동일 · corr |상관| · size 공급사규모 · composite |상관|×log(규모)[기본]

## 한계
- 실제 거래 여부는 미상(SPLC 없음) → 통계적 기업쌍. 상위 후보는 10-K 고객집중도로 확인.
- 기업쌍 표본 24~34분기, 개별은 노이즈 → 가중 종합으로 완화.
