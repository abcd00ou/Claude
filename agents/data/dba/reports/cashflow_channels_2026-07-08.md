# 현금흐름 Lead-Lag — 채널 전체 스캔 (여러 방면)

**분석일:** 2026-07-08 · **데이터:** `panel_long` · **엔진:** `cashflow_map.py`

고객→공급사 24개 엣지 × 13개 현금흐름 채널(결제/구매/투자/재고/현금여력/수요, QoQ·YoY) = 312 조합. 분석가능 197 · **유의 98**.


> ⚠️ 다중비교: 채널을 많이 시도하면 우연 유의가 늘어난다. 경제적 방향과 시차 안정성, YoY/QoQ 교차확인을 함께 볼 것.


## 1. 채널별 요약 (유의 엣지 수 · 평균시차 · 평균 r)

| 채널 | 유의 엣지 | 평균 시차(분기) | 평균 r |
|---|---|---|---|
| 결제(QoQ) | 14 | 0.29 | 0.62 |
| 수요(QoQ) | 11 | 0.27 | 0.66 |
| 수요(YoY) | 10 | 0.7 | 0.59 |
| 결제(YoY) | 9 | 0.0 | 0.67 |
| 구매(YoY) | 9 | 0.44 | 0.57 |
| 재고(QoQ) | 9 | 0.78 | 0.52 |
| 구매(QoQ) | 8 | 0.0 | 0.62 |
| 미지급→미수 | 7 | 0.57 | 0.52 |
| 재고(YoY) | 6 | 0.0 | 0.55 |
| 지급→회수 | 5 | 1.0 | 0.62 |
| 투자(QoQ) | 5 | 0.0 | 0.68 |
| 투자(YoY) | 4 | 0.0 | 0.66 |
| 현금여력 | 1 | 0.0 | 0.71 |

## 2. 시차>0 (고객이 실제로 선행하는) 유의 관계

| 고객 | 공급사 | 채널 | 분석변수 (X→Y) | 시차 | r | p |
|---|---|---|---|---|---|---|
| CPU | HW Equipment | 구매(YoY) | `COGS_GROWTH_YOY→REVENUE_GROWTH_YOY` | 4q | 0.458 | 0.0187 |
| CPU | HW Equipment | 수요(YoY) | `REVENUE_GROWTH_YOY→REVENUE_GROWTH_YOY` | 4q | 0.472 | 0.015 |
| Hyperscaler | Server Networking | 지급→회수 | `DPO→DSO` | 4q | 0.65 | 0.0001 |
| Hyperscaler | CPU | 미지급→미수 | `AP_TO_COGS→AR_TO_REVENUE` | 3q | 0.575 | 0.0007 |
| Hyperscaler | NAND | 수요(YoY) | `REVENUE_GROWTH_YOY→REVENUE_GROWTH_YOY` | 3q | 0.496 | 0.0085 |
| CPU | OSAT/Packaging | 수요(QoQ) | `REVENUE_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | 3q | 0.442 | 0.0185 |
| Server OEM | Server Networking | 재고(QoQ) | `INVENTORY_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | 3q | 0.58 | 0.0006 |
| AI Chip | OSAT/Packaging | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | 2q | 0.406 | 0.0291 |
| AI Chip | OSAT/Packaging | 재고(QoQ) | `INVENTORY_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | 2q | 0.585 | 0.0009 |
| CPU | OSAT/Packaging | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | 2q | 0.546 | 0.0022 |
| CPU | OSAT/Packaging | 재고(QoQ) | `INVENTORY_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | 2q | 0.411 | 0.0269 |
| Hyperscaler | CPU | 지급→회수 | `DPO→DSO` | 1q | 0.673 | 0.0 |
| Hyperscaler | Server Networking | 미지급→미수 | `AP_TO_COGS→AR_TO_REVENUE` | 1q | 0.51 | 0.0024 |

## 3. 채널 정의

| 채널 | X (고객) | Y (공급사) | 의미 |
|---|---|---|---|
| 결제(QoQ) | `AP_GROWTH_QOQ` | `REVENUE_GROWTH_QOQ` | 고객이 아직 안 낸 돈(AP)이 공급사 매출/미수로 |
| 결제(YoY) | `AP_GROWTH_YOY` | `REVENUE_GROWTH_YOY` | 고객이 아직 안 낸 돈(AP)이 공급사 매출/미수로 |
| 지급→회수 | `DPO` | `DSO` | 고객 지급기간이 공급사 회수기간으로 전이 |
| 미지급→미수 | `AP_TO_COGS` | `AR_TO_REVENUE` | 고객 미지급 부담이 공급사 미수 부담으로 |
| 구매(QoQ) | `COGS_GROWTH_QOQ` | `REVENUE_GROWTH_QOQ` | 고객 매출원가(구매)가 공급사 매출로 |
| 구매(YoY) | `COGS_GROWTH_YOY` | `REVENUE_GROWTH_YOY` | 고객 매출원가(구매)가 공급사 매출로 |
| 투자(QoQ) | `CAPEX_GROWTH_QOQ` | `REVENUE_GROWTH_QOQ` | 고객 capex가 공급사 매출로 |
| 투자(YoY) | `CAPEX[growth_yoy]` | `REVENUE[growth_yoy]` | 고객 capex가 공급사 매출로 |
| 재고(QoQ) | `INVENTORY_GROWTH_QOQ` | `REVENUE_GROWTH_QOQ` | 고객 재고 축적/소진이 공급사 주문으로 |
| 재고(YoY) | `INVENTORY_GROWTH_YOY` | `REVENUE_GROWTH_YOY` | 고객 재고 축적/소진이 공급사 주문으로 |
| 현금여력 | `FCF_MARGIN` | `REVENUE_GROWTH_QOQ` | 고객 FCF마진(현금여력)이 공급사 매출로 |
| 수요(QoQ) | `REVENUE_GROWTH_QOQ` | `REVENUE_GROWTH_QOQ` | 고객 최종 매출이 공급사 매출로 |
| 수요(YoY) | `REVENUE_GROWTH_YOY` | `REVENUE_GROWTH_YOY` | 고객 최종 매출이 공급사 매출로 |

## 4. 해석 메모 (직접 작성)
> 
- 


## 5. 한계
- QoQ는 단기·즉시전이, YoY는 계절제거·구조시차 포착(문서 §6).
- 전체 조합 데이터는 동봉 CSV 참조. Foundry·ODM은 데이터 부족.
