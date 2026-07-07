# AI 공급망 현금흐름 Lead-Lag 시차 분석

**분석일:** 2026-07-07 · **데이터:** `panel_long` · **엔진:** `cashflow_map.py`

고객→공급사 현금 전이 시차. 각 엣지는 구매(COGS→매출)·투자(capex→매출)·수요(매출→매출) 채널 중 데이터가 가장 유의한 것으로 시차를 확정.


- 엣지 24 · 분석가능 16 · **유의 14**


## 엣지별 현금흐름 시차 (분석 변수 명시)

| 고객 | 공급사 | 채널 | 분석변수 (X→Y) | 시차(분기) | r | p | 유의 |
|---|---|---|---|---|---|---|---|
| Hyperscaler | AI Chip | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.626 | 0.0001 | ✅ |
| Server OEM | AI Chip | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.721 | 0.0 | ✅ |
| Server OEM | CPU | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.491 | 0.0037 | ✅ |
| Hyperscaler | CPU | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.393 | 0.0235 | ✅ |
| AI Chip | DRAM | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.486 | 0.0048 | ✅ |
| Hyperscaler | DRAM | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.739 | 0.0 | ✅ |
| Server OEM | DRAM | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.758 | 0.0 | ✅ |
| Hyperscaler | NAND | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.802 | 0.0 | ✅ |
| Server OEM | NAND | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.77 | 0.0 | ✅ |
| AI Chip | NAND | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.432 | 0.0121 | ✅ |
| Foundry | HW Equipment | — | — | — | — | — | 데이터부족 |
| DRAM | HW Equipment | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | +3 | 0.146 | 0.4414 | · |
| CPU | HW Equipment | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | +3 | 0.145 | 0.444 | · |
| AI Chip | OSAT/Packaging | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+2** | 0.406 | 0.0291 | ✅ |
| CPU | OSAT/Packaging | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+2** | 0.546 | 0.0022 | ✅ |
| Hyperscaler | Server Networking | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.786 | 0.0 | ✅ |
| Server OEM | Server Networking | 결제(QoQ) | `AP_GROWTH_QOQ→REVENUE_GROWTH_QOQ` | **+0** | 0.788 | 0.0 | ✅ |
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
- **AI Chip → DRAM → HW Equipment**: 누적 **3분기** (AI Chip→DRAM +0q, DRAM→HW Equipment +3q)

## 해석·한계

- 시차 = 고객 활동이 공급사 매출을 선행하는 분기 수 (양수=고객 선행).

- 채널은 데이터가 선택: 구매(COGS)·투자(capex)·수요(매출) 중 최유의.

- 섹터 집계는 커버리지 좋은 기업만 포함(전체 반영 대신 강한 관계 중심).

- Foundry·Server ODM은 데이터 부족으로 다수 엣지 분석 불가.
