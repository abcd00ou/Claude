# AI 공급망 현금흐름 Lead-Lag 시차 분석

**분석일:** 2026-07-07 · **데이터:** `panel_long` · **엔진:** `cashflow_map.py`

고객→공급사 현금 전이 시차. 각 엣지는 구매(COGS→매출)·투자(capex→매출)·수요(매출→매출) 채널 중 데이터가 가장 유의한 것으로 시차를 확정.


- 엣지 24 · 분석가능 16 · **유의 12**


## 엣지별 현금흐름 시차

| 고객 | 공급사 | 채널 | 시차(분기) | r | p | 유의 |
|---|---|---|---|---|---|---|
| Hyperscaler | AI Chip | 투자흐름 | **+0** | 0.698 | 0.0 | ✅ |
| Server OEM | AI Chip | 수요흐름 | **+0** | 0.653 | 0.0 | ✅ |
| Server OEM | CPU | 수요흐름 | +3 | 0.27 | 0.1497 | · |
| Hyperscaler | CPU | 투자흐름 | **+0** | 0.516 | 0.0025 | ✅ |
| AI Chip | DRAM | 수요흐름 | **+0** | 0.586 | 0.0004 | ✅ |
| Hyperscaler | DRAM | 투자흐름 | **+0** | 0.744 | 0.0 | ✅ |
| Server OEM | DRAM | 구매흐름 | **+0** | 0.659 | 0.0 | ✅ |
| Hyperscaler | NAND | 수요흐름 | **+0** | 0.738 | 0.0 | ✅ |
| Server OEM | NAND | 구매흐름 | **+0** | 0.767 | 0.0 | ✅ |
| AI Chip | NAND | 수요흐름 | **+0** | 0.556 | 0.0008 | ✅ |
| Foundry | HW Equipment | — | — | — | — | 데이터부족 |
| DRAM | HW Equipment | 구매흐름 | +0 | 0.251 | 0.1655 | · |
| CPU | HW Equipment | 수요흐름 | +1 | 0.231 | 0.2041 | · |
| AI Chip | OSAT/Packaging | 수요흐름 | +0 | 0.184 | 0.321 | · |
| CPU | OSAT/Packaging | 수요흐름 | **+3** | 0.442 | 0.0185 | ✅ |
| Hyperscaler | Server Networking | 수요흐름 | **+0** | 0.789 | 0.0 | ✅ |
| Server OEM | Server Networking | 구매흐름 | **+0** | 0.829 | 0.0 | ✅ |
| AI Chip | Foundry | — | — | — | — | 데이터부족 |
| CPU | Foundry | — | — | — | — | 데이터부족 |
| Server Networking | Foundry | — | — | — | — | 데이터부족 |
| CPU | Server ODM | — | — | — | — | 데이터부족 |
| DRAM | Server ODM | — | — | — | — | 데이터부족 |
| NAND | Server ODM | — | — | — | — | 데이터부족 |
| AI Chip | Server ODM | — | — | — | — | 데이터부족 |

## 주요 현금전파 경로 (누적 시차)

- **Hyperscaler → AI Chip → DRAM**: 누적 **0분기** (Hyperscaler→AI Chip +0q, AI Chip→DRAM +0q)
- **Hyperscaler → AI Chip → NAND**: 누적 **0분기** (Hyperscaler→AI Chip +0q, AI Chip→NAND +0q)
- **Hyperscaler → AI Chip → OSAT/Packaging**: 누적 **0분기** (Hyperscaler→AI Chip +0q, AI Chip→OSAT/Packaging +0q)
- **Server OEM → AI Chip → DRAM**: 누적 **0분기** (Server OEM→AI Chip +0q, AI Chip→DRAM +0q)
- **AI Chip → DRAM → HW Equipment**: 누적 **0분기** (AI Chip→DRAM +0q, DRAM→HW Equipment +0q)

## 해석·한계

- 시차 = 고객 활동이 공급사 매출을 선행하는 분기 수 (양수=고객 선행).

- 채널은 데이터가 선택: 구매(COGS)·투자(capex)·수요(매출) 중 최유의.

- 섹터 집계는 커버리지 좋은 기업만 포함(전체 반영 대신 강한 관계 중심).

- Foundry·Server ODM은 데이터 부족으로 다수 엣지 분석 불가.
