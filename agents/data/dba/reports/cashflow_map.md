# AI 공급망 현금흐름 Lead-Lag 시차 분석

**분석일:** 2026-07-09 · **데이터:** `panel_long` · **엔진:** `cashflow_map.py`

고객→공급사 현금 전이 시차. 각 엣지는 구매(COGS→매출)·투자(capex→매출)·수요(매출→매출) 채널 중 데이터가 가장 유의한 것으로 시차를 확정.


- 엣지 24 · 분석가능 16 · **유의 15**


## 엣지별 현금흐름 시차 (분석 변수 명시)

| 고객 | 공급사 | 채널 | 분석변수 (X→Y) | 시차(분기) | r | p | 유의 |
|---|---|---|---|---|---|---|---|
| Hyperscaler | AI Chip | 투자(YoY) | `CAPEX[growth_yoy]→REVENUE[growth_yoy]` | **+0** | 0.8 | 0.0 | ✅ |
| Server OEM | AI Chip | 수요(YoY) | `REVENUE_GROWTH_YOY→REVENUE_GROWTH_YOY` | **+0** | 0.822 | 0.0 | ✅ |
| Server OEM | CPU | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.491 | 0.0037 | ✅ |
| Hyperscaler | CPU | 지급→회수 | `DPO→DSO` | **+1** | 0.673 | 0.0 | ✅ |
| AI Chip | DRAM | 수요(YoY) | `REVENUE_GROWTH_YOY→REVENUE_GROWTH_YOY` | **+0** | 0.717 | 0.0 | ✅ |
| Hyperscaler | DRAM | 투자(YoY) | `CAPEX[growth_yoy]→REVENUE[growth_yoy]` | **+0** | 0.746 | 0.0 | ✅ |
| Server OEM | DRAM | 재고(YoY) | `INVENTORY_GROWTH_YOY→REVENUE_GROWTH_YOY` | **+0** | 0.821 | 0.0 | ✅ |
| Hyperscaler | NAND | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.802 | 0.0 | ✅ |
| Server OEM | NAND | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.77 | 0.0 | ✅ |
| AI Chip | NAND | 결제(YoY) | `AP_GROWTH_YOY→REVENUE_GROWTH_YOY` | **+0** | 0.693 | 0.0 | ✅ |
| Foundry | HW Equipment | — | — | — | — | — | 데이터부족 |
| DRAM | HW Equipment | 투자(YoY) | `CAPEX[growth_yoy]→REVENUE[growth_yoy]` | +4 | 0.788 | 0.0628 | · |
| CPU | HW Equipment | 수요(YoY) | `REVENUE_GROWTH_YOY→REVENUE_GROWTH_YOY` | **+4** | 0.472 | 0.015 | ✅ |
| AI Chip | OSAT/Packaging | 재고(QoQ) | `INVENTORY_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+2** | 0.585 | 0.0009 | ✅ |
| CPU | OSAT/Packaging | 현금여력 | `FCF_MARGIN→REVENUE_GROWTH_QOQ` | **+0** | 0.706 | 0.0151 | ✅ |
| Hyperscaler | Server Networking | 수요(QoQ) | `REVENUE_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.789 | 0.0 | ✅ |
| Server OEM | Server Networking | 구매(QoQ) | `COGS_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.829 | 0.0 | ✅ |
| AI Chip | Foundry | — | — | — | — | — | 데이터부족 |
| CPU | Foundry | — | — | — | — | — | 데이터부족 |
| Server Networking | Foundry | — | — | — | — | — | 데이터부족 |
| CPU | Server ODM | — | — | — | — | — | 데이터부족 |
| DRAM | Server ODM | — | — | — | — | — | 데이터부족 |
| NAND | Server ODM | — | — | — | — | — | 데이터부족 |
| AI Chip | Server ODM | — | — | — | — | — | 데이터부족 |

## 주요 현금전파 경로 (누적 시차)

- **Hyperscaler → AI Chip → DRAM**: 누적 **0분기** (Hyperscaler→AI Chip +0q, AI Chip→DRAM +0q)
- **Hyperscaler → AI Chip → NAND**: 누적 **0분기** (Hyperscaler→AI Chip +0q, AI Chip→NAND +0q)
- **Hyperscaler → AI Chip → OSAT/Packaging**: 누적 **2분기** (Hyperscaler→AI Chip +0q, AI Chip→OSAT/Packaging +2q)
- **Server OEM → AI Chip → DRAM**: 누적 **0분기** (Server OEM→AI Chip +0q, AI Chip→DRAM +0q)
- **AI Chip → DRAM → HW Equipment**: 누적 **4분기** (AI Chip→DRAM +0q, DRAM→HW Equipment +4q)

## 해석·한계

- 시차 = 고객 활동이 공급사 매출을 선행하는 분기 수 (양수=고객 선행).

- 채널은 데이터가 선택: 구매(COGS)·투자(capex)·수요(매출) 중 최유의.

- 섹터 집계는 커버리지 좋은 기업만 포함(전체 반영 대신 강한 관계 중심).

- Foundry·Server ODM은 데이터 부족으로 다수 엣지 분석 불가.
