# 기업간 상관가중 매출합 현금흐름 Lead-Lag

**분석일:** 2026-07-08 · **채널:** 고객 `AP_GROWTH_YOY` → 공급사 `REVENUE_GROWTH_YOY`

섹터 단순합 대신, 공급사 각 기업의 매출을 **고객과의 상관값으로 가중합**해 관계 재정리. 고객은 섹터 매출 1위 기업. 가중치 = max(상관, 0).


- 엣지 24 · 분석가능 13 · 유의 6


## 섹터 엣지 (상관가중 매출합)

| 고객(대표) | 공급사 | 시차(분기) | r | p | 공급사수 |
|---|---|---|---|---|---|
| Hyperscaler(AMZN) | AI Chip | +3 | 0.4 | 0.0584 | 2 |
| Server OEM(DELL) | AI Chip | +4 | -0.3 | 0.2593 | 1 |
| Server OEM | CPU | — | — | — | insufficient supplier data |
| Hyperscaler(AMZN) | CPU | **+2** | 0.55 | 0.0036 | 1 |
| AI Chip(NVDA) | DRAM | +0 | 0.804 | 0.0 | 1 |
| Hyperscaler(AMZN) | DRAM | +3 | 0.23 | 0.2576 | 1 |
| Server OEM | DRAM | — | — | — | insufficient supplier data |
| Hyperscaler(AMZN) | NAND | +3 | 0.46 | 0.0546 | 2 |
| Server OEM(DELL) | NAND | **+0** | 0.737 | 0.0007 | 1 |
| AI Chip(NVDA) | NAND | **+2** | 0.587 | 0.0132 | 2 |
| Foundry | HW Equipment | — | — | — | insufficient customer data |
| DRAM(MU) | HW Equipment | +1 | 0.101 | 0.6145 | 3 |
| CPU(INTC) | HW Equipment | +4 | -0.31 | 0.141 | 4 |
| AI Chip(NVDA) | OSAT/Packaging | +2 | 0.387 | 0.0619 | 1 |
| CPU | OSAT/Packaging | — | — | — | insufficient supplier data |
| Hyperscaler(AMZN) | Server Networking | **+1** | 0.56 | 0.0102 | 5 |
| Server OEM(DELL) | Server Networking | **+0** | 0.66 | 0.0039 | 5 |
| AI Chip | Foundry | — | — | — | insufficient supplier data |
| CPU | Foundry | — | — | — | insufficient supplier data |
| Server Networking | Foundry | — | — | — | insufficient supplier data |
| CPU | Server ODM | — | — | — | insufficient supplier data |
| DRAM | Server ODM | — | — | — | insufficient supplier data |
| NAND | Server ODM | — | — | — | insufficient supplier data |
| AI Chip | Server ODM | — | — | — | insufficient supplier data |

## 엣지별 공급사 기여 (상관 가중치)

- **Hyperscaler→AI Chip**: AMD(AMD) r=0.577 w=0.649, Qualcomm(QCOM) r=0.312 w=0.351
- **Server OEM→AI Chip**: Qualcomm(QCOM) r=0.259 w=1.0
- **Hyperscaler→CPU**: Intel(INTC) r=0.55 w=1.0
- **AI Chip→DRAM**: Micron Technology(MU) r=0.804 w=1.0
- **Hyperscaler→DRAM**: Micron Technology(MU) r=0.23 w=1.0
- **Hyperscaler→NAND**: Western Digital(WDC) r=0.55 w=0.69, Seagate Technology(STX) r=0.247 w=0.31
- **Server OEM→NAND**: Western Digital(WDC) r=0.737 w=1.0
- **AI Chip→NAND**: Seagate Technology(STX) r=0.703 w=0.542, Western Digital(WDC) r=0.595 w=0.458
- **DRAM→HW Equipment**: Lam Research(LRCX) r=0.193 w=0.385, FormFactor(FORM) r=0.155 w=0.309, Onto Innovation(ONTO) r=0.153 w=0.305
- **CPU→HW Equipment**: Onto Innovation(ONTO) r=0.432 w=0.404, KLA(KLAC) r=0.371 w=0.347, Lam Research(LRCX) r=0.158 w=0.148, MKS Instruments(MKSI) r=0.107 w=0.1
- **AI Chip→OSAT/Packaging**: Amkor Technology(AMKR) r=0.387 w=1.0
- **Hyperscaler→Server Networking**: Coherent Corp(COHR) r=0.548 w=0.314, Lumentum(LITE) r=0.449 w=0.257, Applied Optoelectronics(AAOI) r=0.336 w=0.192, Fabrinet(FN) r=0.276 w=0.158, MACOM Technology(MTSI) r=0.139 w=0.08
- **Server OEM→Server Networking**: Cisco(CSCO) r=0.491 w=0.283, Arista Networks(ANET) r=0.427 w=0.246, Lumentum(LITE) r=0.404 w=0.233, Semtech(SMTC) r=0.247 w=0.142, Coherent Corp(COHR) r=0.166 w=0.096

## 한계
- 공급사 상관가중합은 '통계적 거래처 비중'. 실제 매출 비중/거래는 10-K로 확인.
- Foundry·Server ODM(대만)은 5분기뿐이라 불가.
