# 현금흐름 병목 & Lead-Lag 분석 리포트

**분석일:** 2026-07-06 · **데이터:** `panel_long`(accounts_payable 포함) · **엔진:** `features.py` + `cashflow_leadlag.py` (가이드 문서 §4·§5·§9 구현)

**판정 규칙:** 상관 부호가 기대부호와 일치 + p<0.05 → **가설지지**. 부호만 일치 → 방향일치·약함. 부호 반대 → 부호불일치.


## 1. 기업 내부 (운전자본 병목 → 현금흐름)

- 분석 케이스 80 · 분석가능 76 · **가설지지 15건**

| 기업 | X(선행) | Y(후행) | 기대 | lag | Pearson | p | Granger | 판정 |
|---|---|---|---|---|---|---|---|---|
| NVIDIA | CCC | FCF_MARGIN | - | +2 | 0.915 | 0.0106 | nan | 부호불일치(기대 -, 실제 +) |
| NVIDIA | DIO | FCF_MARGIN | - | +2 | 0.806 | 0.0528 | nan | 부호불일치(기대 -, 실제 +) |
| NVIDIA | DSO | OCF_MARGIN | - | +2 | 0.639 | 0.0637 | nan | 부호불일치(기대 -, 실제 +) |
| NVIDIA | DPO | OCF_MARGIN | + | +2 | 0.001 | 0.998 | nan | 방향일치·약함 (lead 2q, r=0.001) |
| NVIDIA | AR_GROWTH_MINUS_REVENUE_GROWTH | OCF_MARGIN | - | +3 | -0.196 | 0.6416 | nan | 방향일치·약함 (lead 3q, r=-0.196) |
| NVIDIA | AP_GROWTH_MINUS_COGS_GROWTH | OCF_MARGIN | + | +2 | 0.429 | 0.2498 | nan | 방향일치·약함 (lead 2q, r=0.429) |
| NVIDIA | INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | FCF_MARGIN | - | +1 | -0.192 | 0.6801 | 0.0862 | 방향일치·약함 (lead 1q, r=-0.192) |
| NVIDIA | CAPEX_TO_OCF | FCF_MARGIN | - | +0 | -0.942 | 0.0001 | 0.8973 | 가설지지 (lead 0q, r=-0.942, p=0.0001) |
| AMD | CCC | FCF_MARGIN | - | +4 | -0.501 | 0.3114 | nan | 방향일치·약함 (lead 4q, r=-0.501) |
| AMD | DIO | FCF_MARGIN | - | +4 | -0.803 | 0.0542 | nan | 방향일치·약함 (lead 4q, r=-0.803) |
| AMD | DSO | OCF_MARGIN | - | +4 | -0.299 | 0.5645 | nan | 방향일치·약함 (lead 4q, r=-0.299) |
| AMD | DPO | OCF_MARGIN | + | +2 | 0.478 | 0.2306 | nan | 방향일치·약함 (lead 2q, r=0.478) |
| AMD | AR_GROWTH_MINUS_REVENUE_GROWTH | OCF_MARGIN | - | +0 | -0.535 | 0.111 | 0.1569 | 방향일치·약함 (lead 0q, r=-0.535) |
| AMD | AP_GROWTH_MINUS_COGS_GROWTH | OCF_MARGIN | + | +0 | 0.209 | 0.5623 | 0.8862 | 방향일치·약함 (lead 0q, r=0.209) |
| AMD | INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | FCF_MARGIN | - | +4 | -0.764 | 0.0768 | nan | 방향일치·약함 (lead 4q, r=-0.764) |
| AMD | CAPEX_TO_OCF | FCF_MARGIN | - | +0 | 0.499 | 0.1184 | 0.7531 | 부호불일치(기대 -, 실제 +) |
| Micron Technology | CCC | FCF_MARGIN | - | +0 | -0.528 | 0.0952 | 0.6735 | 방향일치·약함 (lead 0q, r=-0.528) |
| Micron Technology | DIO | FCF_MARGIN | - | +0 | -0.449 | 0.1663 | 0.4595 | 방향일치·약함 (lead 0q, r=-0.449) |
| Micron Technology | DSO | OCF_MARGIN | - | +3 | -0.662 | 0.0737 | nan | 방향일치·약함 (lead 3q, r=-0.662) |
| Micron Technology | DPO | OCF_MARGIN | + | +4 | 0.829 | 0.0212 | nan | 가설지지 (lead 4q, r=0.829, p=0.0212) |
| Micron Technology | AR_GROWTH_MINUS_REVENUE_GROWTH | OCF_MARGIN | - | +3 | -0.389 | 0.3403 | nan | 방향일치·약함 (lead 3q, r=-0.389) |
| Micron Technology | AP_GROWTH_MINUS_COGS_GROWTH | OCF_MARGIN | + | +0 | 0.462 | 0.1527 | 0.8832 | 방향일치·약함 (lead 0q, r=0.462) |
| Micron Technology | INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | FCF_MARGIN | - | +1 | -0.435 | 0.2087 | 0.9608 | 방향일치·약함 (lead 1q, r=-0.435) |
| Micron Technology | CAPEX_TO_OCF | FCF_MARGIN | - | +0 | -0.955 | 0.0 | 0.8653 | 가설지지 (lead 0q, r=-0.955, p=0.0) |
| Intel | CCC | FCF_MARGIN | - | +2 | -0.185 | 0.6607 | nan | 방향일치·약함 (lead 2q, r=-0.185) |
| Intel | DIO | FCF_MARGIN | - | +0 | -0.883 | 0.0007 | 0.0056 | 가설지지 (lead 0q, r=-0.883, p=0.0007) |
| Intel | DSO | OCF_MARGIN | - | +4 | -0.444 | 0.3784 | nan | 방향일치·약함 (lead 4q, r=-0.444) |
| Intel | DPO | OCF_MARGIN | + | +2 | 0.083 | 0.8453 | nan | 방향일치·약함 (lead 2q, r=0.083) |
| Intel | AR_GROWTH_MINUS_REVENUE_GROWTH | OCF_MARGIN | - | +0 | -0.076 | 0.8354 | 0.6962 | 방향일치·약함 (lead 0q, r=-0.076) |
| Intel | AP_GROWTH_MINUS_COGS_GROWTH | OCF_MARGIN | + | +3 | 0.141 | 0.7628 | nan | 방향일치·약함 (lead 3q, r=0.141) |
| Intel | INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | FCF_MARGIN | - | +2 | -0.28 | 0.5022 | nan | 방향일치·약함 (lead 2q, r=-0.28) |
| Intel | CAPEX_TO_OCF | FCF_MARGIN | - | +4 | -0.447 | 0.3147 | nan | 방향일치·약함 (lead 4q, r=-0.447) |
| Applied Materials | CCC | FCF_MARGIN | - | +4 | -0.851 | 0.0153 | nan | 가설지지 (lead 4q, r=-0.851, p=0.0153) |
| Applied Materials | DIO | FCF_MARGIN | - | +1 | -0.275 | 0.4424 | 0.3523 | 방향일치·약함 (lead 1q, r=-0.275) |
| Applied Materials | DSO | OCF_MARGIN | - | +4 | -0.752 | 0.0514 | nan | 방향일치·약함 (lead 4q, r=-0.752) |
| Applied Materials | DPO | OCF_MARGIN | + | +4 | 0.087 | 0.8521 | nan | 방향일치·약함 (lead 4q, r=0.087) |
| Applied Materials | AR_GROWTH_MINUS_REVENUE_GROWTH | OCF_MARGIN | - | +0 | -0.347 | 0.2961 | 0.1134 | 방향일치·약함 (lead 0q, r=-0.347) |
| Applied Materials | AP_GROWTH_MINUS_COGS_GROWTH | OCF_MARGIN | + | +3 | 0.366 | 0.3722 | nan | 방향일치·약함 (lead 3q, r=0.366) |
| Applied Materials | INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | FCF_MARGIN | - | +4 | -0.7 | 0.0802 | nan | 방향일치·약함 (lead 4q, r=-0.7) |
| Applied Materials | CAPEX_TO_OCF | FCF_MARGIN | - | +0 | -0.8 | 0.0018 | 0.0104 | 가설지지 (lead 0q, r=-0.8, p=0.0018) |
| Lam Research | CCC | FCF_MARGIN | - | +1 | -0.19 | 0.5989 | 0.9884 | 방향일치·약함 (lead 1q, r=-0.19) |
| Lam Research | DIO | FCF_MARGIN | - | +1 | -0.093 | 0.7982 | 0.9586 | 방향일치·약함 (lead 1q, r=-0.093) |
| Lam Research | DSO | OCF_MARGIN | - | +3 | -0.401 | 0.3252 | nan | 방향일치·약함 (lead 3q, r=-0.401) |
| Lam Research | DPO | OCF_MARGIN | + | +0 | 0.44 | 0.1762 | 0.8731 | 방향일치·약함 (lead 0q, r=0.44) |
| Lam Research | AR_GROWTH_MINUS_REVENUE_GROWTH | OCF_MARGIN | - | +2 | -0.438 | 0.2389 | nan | 방향일치·약함 (lead 2q, r=-0.438) |
| Lam Research | AP_GROWTH_MINUS_COGS_GROWTH | OCF_MARGIN | + | +4 | 0.315 | 0.4913 | nan | 방향일치·약함 (lead 4q, r=0.315) |
| Lam Research | INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | FCF_MARGIN | - | +2 | -0.623 | 0.0732 | nan | 방향일치·약함 (lead 2q, r=-0.623) |
| Lam Research | CAPEX_TO_OCF | FCF_MARGIN | - | +0 | -0.859 | 0.0003 | 0.0127 | 가설지지 (lead 0q, r=-0.859, p=0.0003) |
| Amkor Technology | CCC | FCF_MARGIN | - | +4 | -0.089 | 0.8494 | nan | 방향일치·약함 (lead 4q, r=-0.089) |
| Amkor Technology | DIO | FCF_MARGIN | - | +4 | -0.294 | 0.5225 | nan | 방향일치·약함 (lead 4q, r=-0.294) |
| Amkor Technology | DSO | OCF_MARGIN | - | +0 | -0.791 | 0.0038 | 0.2699 | 가설지지 (lead 0q, r=-0.791, p=0.0038) |
| Amkor Technology | DPO | OCF_MARGIN | + | +2 | 0.417 | 0.2646 | nan | 방향일치·약함 (lead 2q, r=0.417) |
| Amkor Technology | AR_GROWTH_MINUS_REVENUE_GROWTH | OCF_MARGIN | - | +2 | -0.214 | 0.5802 | nan | 방향일치·약함 (lead 2q, r=-0.214) |
| Amkor Technology | AP_GROWTH_MINUS_COGS_GROWTH | OCF_MARGIN | + | +4 | 0.59 | 0.1629 | nan | 방향일치·약함 (lead 4q, r=0.59) |
| Amkor Technology | INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | FCF_MARGIN | - | +1 | -0.052 | 0.8867 | 0.0686 | 방향일치·약함 (lead 1q, r=-0.052) |
| Amkor Technology | CAPEX_TO_OCF | FCF_MARGIN | - | +0 | -0.818 | 0.0011 | 0.776 | 가설지지 (lead 0q, r=-0.818, p=0.0011) |
| Dell Technologies | CCC | FCF_MARGIN | - | +3 | -0.071 | 0.8934 | nan | 방향일치·약함 (lead 3q, r=-0.071) |
| Dell Technologies | DIO | FCF_MARGIN | - | +0 | 0.573 | 0.0835 | 0.0507 | 부호불일치(기대 -, 실제 +) |
| Dell Technologies | DSO | OCF_MARGIN | - | +3 | -0.895 | 0.0161 | nan | 가설지지 (lead 3q, r=-0.895, p=0.0161) |
| Dell Technologies | DPO | OCF_MARGIN | + | +1 | 0.1 | 0.8129 | 0.9141 | 방향일치·약함 (lead 1q, r=0.1) |
| Dell Technologies | AR_GROWTH_MINUS_REVENUE_GROWTH | OCF_MARGIN | - | +4 | -0.827 | 0.0425 | nan | 가설지지 (lead 4q, r=-0.827, p=0.0425) |
| Dell Technologies | AP_GROWTH_MINUS_COGS_GROWTH | OCF_MARGIN | + | +0 | 0.449 | 0.2256 | 0.9897 | 방향일치·약함 (lead 0q, r=0.449) |
| Dell Technologies | INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | FCF_MARGIN | - | +3 | -0.17 | 0.7153 | nan | 방향일치·약함 (lead 3q, r=-0.17) |
| Dell Technologies | CAPEX_TO_OCF | FCF_MARGIN | - | +1 | -0.116 | 0.7494 | 0.6228 | 방향일치·약함 (lead 1q, r=-0.116) |
| Broadcom | CCC | FCF_MARGIN | - | +1 | -0.459 | 0.2521 | 0.3 | 방향일치·약함 (lead 1q, r=-0.459) |
| Broadcom | DIO | FCF_MARGIN | - | +2 | -0.493 | 0.2607 | nan | 방향일치·약함 (lead 2q, r=-0.493) |
| Broadcom | DSO | OCF_MARGIN | - | +0 | -0.642 | 0.0621 | 0.1263 | 방향일치·약함 (lead 0q, r=-0.642) |
| Broadcom | DPO | OCF_MARGIN | + | +3 | 0.286 | 0.5827 | nan | 방향일치·약함 (lead 3q, r=0.286) |
| Broadcom | AR_GROWTH_MINUS_REVENUE_GROWTH | OCF_MARGIN | - | +2 | -0.89 | 0.0072 | nan | 가설지지 (lead 2q, r=-0.89, p=0.0072) |
| Broadcom | AP_GROWTH_MINUS_COGS_GROWTH | OCF_MARGIN | + | +2 | 0.681 | 0.0924 | nan | 방향일치·약함 (lead 2q, r=0.681) |
| Broadcom | INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | FCF_MARGIN | - | +3 | -0.617 | 0.1921 | nan | 방향일치·약함 (lead 3q, r=-0.617) |
| Broadcom | CAPEX_TO_OCF | FCF_MARGIN | - | +0 | -0.841 | 0.0045 | 0.8199 | 가설지지 (lead 0q, r=-0.841, p=0.0045) |
| Seagate Technology | CCC | FCF_MARGIN | - | nan | nan | nan | nan | insufficient data |
| Seagate Technology | DIO | FCF_MARGIN | - | nan | nan | nan | nan | insufficient data |
| Seagate Technology | DSO | OCF_MARGIN | - | +3 | -0.327 | 0.4291 | nan | 방향일치·약함 (lead 3q, r=-0.327) |
| Seagate Technology | DPO | OCF_MARGIN | + | nan | nan | nan | nan | insufficient data |
| Seagate Technology | AR_GROWTH_MINUS_REVENUE_GROWTH | OCF_MARGIN | - | +2 | -0.486 | 0.1846 | nan | 방향일치·약함 (lead 2q, r=-0.486) |
| Seagate Technology | AP_GROWTH_MINUS_COGS_GROWTH | OCF_MARGIN | + | nan | nan | nan | nan | insufficient data |
| Seagate Technology | INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | FCF_MARGIN | - | +0 | -0.695 | 0.0176 | 0.3572 | 가설지지 (lead 0q, r=-0.695, p=0.0176) |
| Seagate Technology | CAPEX_TO_OCF | FCF_MARGIN | - | +0 | -0.908 | 0.0 | 0.7811 | 가설지지 (lead 0q, r=-0.908, p=0.0) |

## 2. 기업 간 (고객↔공급사 전이)

- 분석 케이스 161 · 분석가능 95 · **가설지지 22건**

| 고객 | 공급사 | X(선행) | Y(후행) | 기대 | lag | Pearson | p | 판정 |
|---|---|---|---|---|---|---|---|---|
| Hyperscaler | AI Chip | Hyperscaler·COGS_GROWTH_QOQ | AI Chip·REVENUE_GROWTH_QOQ | + | +0 | 0.224 | 0.2169 | 방향일치·약함 (lead 0q, r=0.224) |
| Hyperscaler | AI Chip | Hyperscaler·CAPEX_GROWTH_QOQ | AI Chip·REVENUE_GROWTH_QOQ | + | +3 | 0.217 | 0.2401 | 방향일치·약함 (lead 3q, r=0.217) |
| Hyperscaler | AI Chip | Hyperscaler·DPO | AI Chip·DSO | + | +0 | 0.572 | 0.0006 | 가설지지 (lead 0q, r=0.572, p=0.0006) |
| Hyperscaler | AI Chip | Hyperscaler·AP_TO_COGS | AI Chip·AR_TO_REVENUE | + | +0 | 0.597 | 0.0002 | 가설지지 (lead 0q, r=0.597, p=0.0002) |
| Hyperscaler | AI Chip | Hyperscaler·FCF_MARGIN | AI Chip·REVENUE_GROWTH_QOQ | + | +3 | 0.158 | 0.3963 | 방향일치·약함 (lead 3q, r=0.158) |
| Hyperscaler | AI Chip | AI Chip·DIO | Hyperscaler·REVENUE_GROWTH_QOQ | - | +2 | -0.067 | 0.7194 | 방향일치·약함 (lead 2q, r=-0.067) |
| Hyperscaler | AI Chip | AI Chip·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Hyperscaler·COGS_GROWTH_QOQ | ? | +2 | -0.564 | 0.0012 | 가설지지 (lead 2q, r=-0.564, p=0.0012) |
| Server OEM | AI Chip | Server OEM·COGS_GROWTH_QOQ | AI Chip·REVENUE_GROWTH_QOQ | + | +0 | 0.653 | 0.0 | 가설지지 (lead 0q, r=0.653, p=0.0) |
| Server OEM | AI Chip | Server OEM·CAPEX_GROWTH_QOQ | AI Chip·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Server OEM | AI Chip | Server OEM·DPO | AI Chip·DSO | + | +0 | -0.397 | 0.02 | 부호불일치(기대 +, 실제 -) |
| Server OEM | AI Chip | Server OEM·AP_TO_COGS | AI Chip·AR_TO_REVENUE | + | +0 | 0.083 | 0.6343 | 방향일치·약함 (lead 0q, r=0.083) |
| Server OEM | AI Chip | Server OEM·FCF_MARGIN | AI Chip·REVENUE_GROWTH_QOQ | + | +3 | 0.354 | 0.286 | 방향일치·약함 (lead 3q, r=0.354) |
| Server OEM | AI Chip | AI Chip·DIO | Server OEM·REVENUE_GROWTH_QOQ | - | +3 | 0.218 | 0.2387 | 부호불일치(기대 -, 실제 +) |
| Server OEM | AI Chip | AI Chip·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Server OEM·COGS_GROWTH_QOQ | ? | +2 | -0.219 | 0.2288 | 방향일치·약함 (lead 2q, r=-0.219) |
| Server OEM | CPU | Server OEM·COGS_GROWTH_QOQ | CPU·REVENUE_GROWTH_QOQ | + | +0 | 0.176 | 0.3281 | 방향일치·약함 (lead 0q, r=0.176) |
| Server OEM | CPU | Server OEM·CAPEX_GROWTH_QOQ | CPU·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Server OEM | CPU | Server OEM·DPO | CPU·DSO | + | +0 | -0.687 | 0.0 | 부호불일치(기대 +, 실제 -) |
| Server OEM | CPU | Server OEM·AP_TO_COGS | CPU·AR_TO_REVENUE | + | +0 | -0.453 | 0.0072 | 부호불일치(기대 +, 실제 -) |
| Server OEM | CPU | Server OEM·FCF_MARGIN | CPU·REVENUE_GROWTH_QOQ | + | +3 | 0.311 | 0.3822 | 방향일치·약함 (lead 3q, r=0.311) |
| Server OEM | CPU | CPU·DIO | Server OEM·REVENUE_GROWTH_QOQ | - | +2 | 0.348 | 0.0599 | 부호불일치(기대 -, 실제 +) |
| Server OEM | CPU | CPU·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Server OEM·COGS_GROWTH_QOQ | ? | +3 | 0.309 | 0.0965 | 방향일치·약함 (lead 3q, r=0.309) |
| Hyperscaler | CPU | Hyperscaler·COGS_GROWTH_QOQ | CPU·REVENUE_GROWTH_QOQ | + | +1 | 0.244 | 0.179 | 방향일치·약함 (lead 1q, r=0.244) |
| Hyperscaler | CPU | Hyperscaler·CAPEX_GROWTH_QOQ | CPU·REVENUE_GROWTH_QOQ | + | +3 | 0.184 | 0.3309 | 방향일치·약함 (lead 3q, r=0.184) |
| Hyperscaler | CPU | Hyperscaler·DPO | CPU·DSO | + | +1 | 0.61 | 0.0002 | 가설지지 (lead 1q, r=0.61, p=0.0002) |
| Hyperscaler | CPU | Hyperscaler·AP_TO_COGS | CPU·AR_TO_REVENUE | + | +1 | 0.568 | 0.0006 | 가설지지 (lead 1q, r=0.568, p=0.0006) |
| Hyperscaler | CPU | Hyperscaler·FCF_MARGIN | CPU·REVENUE_GROWTH_QOQ | + | +2 | 0.275 | 0.1342 | 방향일치·약함 (lead 2q, r=0.275) |
| Hyperscaler | CPU | CPU·DIO | Hyperscaler·REVENUE_GROWTH_QOQ | - | +1 | -0.246 | 0.1895 | 방향일치·약함 (lead 1q, r=-0.246) |
| Hyperscaler | CPU | CPU·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Hyperscaler·COGS_GROWTH_QOQ | ? | +2 | -0.585 | 0.0007 | 가설지지 (lead 2q, r=-0.585, p=0.0007) |
| AI Chip | DRAM | AI Chip·COGS_GROWTH_QOQ | DRAM·REVENUE_GROWTH_QOQ | + | +1 | 0.518 | 0.0034 | 가설지지 (lead 1q, r=0.518, p=0.0034) |
| AI Chip | DRAM | AI Chip·CAPEX_GROWTH_QOQ | DRAM·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| AI Chip | DRAM | AI Chip·DPO | DRAM·DSO | + | +0 | 0.388 | 0.0308 | 가설지지 (lead 0q, r=0.388, p=0.0308) |
| AI Chip | DRAM | AI Chip·AP_TO_COGS | DRAM·AR_TO_REVENUE | + | +2 | -0.241 | 0.1997 | 부호불일치(기대 +, 실제 -) |
| AI Chip | DRAM | AI Chip·FCF_MARGIN | DRAM·REVENUE_GROWTH_QOQ | + | +1 | 0.648 | 0.0429 | 가설지지 (lead 1q, r=0.648, p=0.0429) |
| AI Chip | DRAM | DRAM·DIO | AI Chip·REVENUE_GROWTH_QOQ | - | +3 | -0.001 | 0.9944 | 방향일치·약함 (lead 3q, r=-0.001) |
| AI Chip | DRAM | DRAM·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | AI Chip·COGS_GROWTH_QOQ | ? | +2 | -0.299 | 0.1023 | 방향일치·약함 (lead 2q, r=-0.299) |
| Hyperscaler | DRAM | Hyperscaler·COGS_GROWTH_QOQ | DRAM·REVENUE_GROWTH_QOQ | + | +2 | 0.127 | 0.5107 | 방향일치·약함 (lead 2q, r=0.127) |
| Hyperscaler | DRAM | Hyperscaler·CAPEX_GROWTH_QOQ | DRAM·REVENUE_GROWTH_QOQ | + | +1 | 0.512 | 0.0038 | 가설지지 (lead 1q, r=0.512, p=0.0038) |
| Hyperscaler | DRAM | Hyperscaler·DPO | DRAM·DSO | + | +1 | 0.301 | 0.1062 | 방향일치·약함 (lead 1q, r=0.301) |
| Hyperscaler | DRAM | Hyperscaler·AP_TO_COGS | DRAM·AR_TO_REVENUE | + | +0 | 0.257 | 0.1548 | 방향일치·약함 (lead 0q, r=0.257) |
| Hyperscaler | DRAM | Hyperscaler·FCF_MARGIN | DRAM·REVENUE_GROWTH_QOQ | + | +3 | 0.151 | 0.4428 | 방향일치·약함 (lead 3q, r=0.151) |
| Hyperscaler | DRAM | DRAM·DIO | Hyperscaler·REVENUE_GROWTH_QOQ | - | +3 | -0.003 | 0.9864 | 방향일치·약함 (lead 3q, r=-0.003) |
| Hyperscaler | DRAM | DRAM·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Hyperscaler·COGS_GROWTH_QOQ | ? | +2 | -0.248 | 0.1858 | 방향일치·약함 (lead 2q, r=-0.248) |
| Hyperscaler | NAND | Hyperscaler·COGS_GROWTH_QOQ | NAND·REVENUE_GROWTH_QOQ | + | +0 | 0.551 | 0.0011 | 가설지지 (lead 0q, r=0.551, p=0.0011) |
| Hyperscaler | NAND | Hyperscaler·CAPEX_GROWTH_QOQ | NAND·REVENUE_GROWTH_QOQ | + | +3 | 0.165 | 0.3849 | 방향일치·약함 (lead 3q, r=0.165) |
| Hyperscaler | NAND | Hyperscaler·DPO | NAND·DSO | + | +0 | 0.668 | 0.0 | 가설지지 (lead 0q, r=0.668, p=0.0) |
| Hyperscaler | NAND | Hyperscaler·AP_TO_COGS | NAND·AR_TO_REVENUE | + | +0 | 0.595 | 0.0003 | 가설지지 (lead 0q, r=0.595, p=0.0003) |
| Hyperscaler | NAND | Hyperscaler·FCF_MARGIN | NAND·REVENUE_GROWTH_QOQ | + | +1 | 0.285 | 0.1133 | 방향일치·약함 (lead 1q, r=0.285) |
| Hyperscaler | NAND | NAND·DIO | Hyperscaler·REVENUE_GROWTH_QOQ | - | +2 | -0.331 | 0.1231 | 방향일치·약함 (lead 2q, r=-0.331) |
| Hyperscaler | NAND | NAND·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Hyperscaler·COGS_GROWTH_QOQ | ? | +1 | 0.264 | 0.1507 | 방향일치·약함 (lead 1q, r=0.264) |
| Server OEM | NAND | Server OEM·COGS_GROWTH_QOQ | NAND·REVENUE_GROWTH_QOQ | + | +0 | 0.767 | 0.0 | 가설지지 (lead 0q, r=0.767, p=0.0) |
| Server OEM | NAND | Server OEM·CAPEX_GROWTH_QOQ | NAND·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Server OEM | NAND | Server OEM·DPO | NAND·DSO | + | +0 | -0.411 | 0.0175 | 부호불일치(기대 +, 실제 -) |
| Server OEM | NAND | Server OEM·AP_TO_COGS | NAND·AR_TO_REVENUE | + | +0 | 0.121 | 0.497 | 방향일치·약함 (lead 0q, r=0.121) |
| Server OEM | NAND | Server OEM·FCF_MARGIN | NAND·REVENUE_GROWTH_QOQ | + | +3 | 0.382 | 0.2753 | 방향일치·약함 (lead 3q, r=0.382) |
| Server OEM | NAND | NAND·DIO | Server OEM·REVENUE_GROWTH_QOQ | - | +1 | 0.722 | 0.0 | 부호불일치(기대 -, 실제 +) |
| Server OEM | NAND | NAND·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Server OEM·COGS_GROWTH_QOQ | ? | +3 | 0.205 | 0.2695 | 방향일치·약함 (lead 3q, r=0.205) |
| AI Chip | NAND | AI Chip·COGS_GROWTH_QOQ | NAND·REVENUE_GROWTH_QOQ | + | +0 | 0.588 | 0.0003 | 가설지지 (lead 0q, r=0.588, p=0.0003) |
| AI Chip | NAND | AI Chip·CAPEX_GROWTH_QOQ | NAND·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| AI Chip | NAND | AI Chip·DPO | NAND·DSO | + | +0 | -0.329 | 0.0613 | 부호불일치(기대 +, 실제 -) |
| AI Chip | NAND | AI Chip·AP_TO_COGS | NAND·AR_TO_REVENUE | + | +2 | 0.105 | 0.5691 | 방향일치·약함 (lead 2q, r=0.105) |
| AI Chip | NAND | AI Chip·FCF_MARGIN | NAND·REVENUE_GROWTH_QOQ | + | +3 | 0.325 | 0.3592 | 방향일치·약함 (lead 3q, r=0.325) |
| AI Chip | NAND | NAND·DIO | AI Chip·REVENUE_GROWTH_QOQ | - | +2 | -0.176 | 0.4115 | 방향일치·약함 (lead 2q, r=-0.176) |
| AI Chip | NAND | NAND·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | AI Chip·COGS_GROWTH_QOQ | ? | +1 | 0.114 | 0.5281 | 방향일치·약함 (lead 1q, r=0.114) |
| Foundry | HW Equipment | Foundry·COGS_GROWTH_QOQ | HW Equipment·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Foundry | HW Equipment | Foundry·CAPEX_GROWTH_QOQ | HW Equipment·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Foundry | HW Equipment | Foundry·DPO | HW Equipment·DSO | + | nan | nan | nan | insufficient data |
| Foundry | HW Equipment | Foundry·AP_TO_COGS | HW Equipment·AR_TO_REVENUE | + | nan | nan | nan | insufficient data |
| Foundry | HW Equipment | Foundry·FCF_MARGIN | HW Equipment·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Foundry | HW Equipment | HW Equipment·DIO | Foundry·REVENUE_GROWTH_QOQ | - | nan | nan | nan | insufficient data |
| Foundry | HW Equipment | HW Equipment·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Foundry·COGS_GROWTH_QOQ | ? | nan | nan | nan | insufficient data |
| DRAM | HW Equipment | DRAM·COGS_GROWTH_QOQ | HW Equipment·REVENUE_GROWTH_QOQ | + | +0 | 0.05 | 0.7907 | 방향일치·약함 (lead 0q, r=0.05) |
| DRAM | HW Equipment | DRAM·CAPEX_GROWTH_QOQ | HW Equipment·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| DRAM | HW Equipment | DRAM·DPO | HW Equipment·DSO | + | +0 | 0.073 | 0.6966 | 방향일치·약함 (lead 0q, r=0.073) |
| DRAM | HW Equipment | DRAM·AP_TO_COGS | HW Equipment·AR_TO_REVENUE | + | +0 | 0.212 | 0.2442 | 방향일치·약함 (lead 0q, r=0.212) |
| DRAM | HW Equipment | DRAM·FCF_MARGIN | HW Equipment·REVENUE_GROWTH_QOQ | + | +2 | 0.102 | 0.7664 | 방향일치·약함 (lead 2q, r=0.102) |
| DRAM | HW Equipment | HW Equipment·DIO | DRAM·REVENUE_GROWTH_QOQ | - | +1 | -0.126 | 0.5079 | 방향일치·약함 (lead 1q, r=-0.126) |
| DRAM | HW Equipment | HW Equipment·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | DRAM·COGS_GROWTH_QOQ | ? | +1 | 0.049 | 0.7966 | 방향일치·약함 (lead 1q, r=0.049) |
| CPU | HW Equipment | CPU·COGS_GROWTH_QOQ | HW Equipment·REVENUE_GROWTH_QOQ | + | +1 | 0.034 | 0.8551 | 방향일치·약함 (lead 1q, r=0.034) |
| CPU | HW Equipment | CPU·CAPEX_GROWTH_QOQ | HW Equipment·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| CPU | HW Equipment | CPU·DPO | HW Equipment·DSO | + | +0 | 0.101 | 0.5953 | 방향일치·약함 (lead 0q, r=0.101) |
| CPU | HW Equipment | CPU·AP_TO_COGS | HW Equipment·AR_TO_REVENUE | + | +1 | 0.011 | 0.9505 | 방향일치·약함 (lead 1q, r=0.011) |
| CPU | HW Equipment | CPU·FCF_MARGIN | HW Equipment·REVENUE_GROWTH_QOQ | + | +2 | 0.491 | 0.1494 | 방향일치·약함 (lead 2q, r=0.491) |
| CPU | HW Equipment | HW Equipment·DIO | CPU·REVENUE_GROWTH_QOQ | - | +3 | -0.053 | 0.7798 | 방향일치·약함 (lead 3q, r=-0.053) |
| CPU | HW Equipment | HW Equipment·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | CPU·COGS_GROWTH_QOQ | ? | +2 | -0.095 | 0.6104 | 방향일치·약함 (lead 2q, r=-0.095) |
| AI Chip | OSAT/Packaging | AI Chip·COGS_GROWTH_QOQ | OSAT/Packaging·REVENUE_GROWTH_QOQ | + | +0 | 0.24 | 0.1931 | 방향일치·약함 (lead 0q, r=0.24) |
| AI Chip | OSAT/Packaging | AI Chip·CAPEX_GROWTH_QOQ | OSAT/Packaging·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| AI Chip | OSAT/Packaging | AI Chip·DPO | OSAT/Packaging·DSO | + | +2 | 0.363 | 0.0532 | 방향일치·약함 (lead 2q, r=0.363) |
| AI Chip | OSAT/Packaging | AI Chip·AP_TO_COGS | OSAT/Packaging·AR_TO_REVENUE | + | +0 | 0.559 | 0.0009 | 가설지지 (lead 0q, r=0.559, p=0.0009) |
| AI Chip | OSAT/Packaging | AI Chip·FCF_MARGIN | OSAT/Packaging·REVENUE_GROWTH_QOQ | + | +2 | 0.39 | 0.2991 | 방향일치·약함 (lead 2q, r=0.39) |
| AI Chip | OSAT/Packaging | OSAT/Packaging·DIO | AI Chip·REVENUE_GROWTH_QOQ | - | +1 | -0.171 | 0.3564 | 방향일치·약함 (lead 1q, r=-0.171) |
| AI Chip | OSAT/Packaging | OSAT/Packaging·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | AI Chip·COGS_GROWTH_QOQ | ? | +1 | -0.126 | 0.4998 | 방향일치·약함 (lead 1q, r=-0.126) |
| CPU | OSAT/Packaging | CPU·COGS_GROWTH_QOQ | OSAT/Packaging·REVENUE_GROWTH_QOQ | + | +1 | 0.34 | 0.066 | 방향일치·약함 (lead 1q, r=0.34) |
| CPU | OSAT/Packaging | CPU·CAPEX_GROWTH_QOQ | OSAT/Packaging·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| CPU | OSAT/Packaging | CPU·DPO | OSAT/Packaging·DSO | + | +1 | 0.052 | 0.7852 | 방향일치·약함 (lead 1q, r=0.052) |
| CPU | OSAT/Packaging | CPU·AP_TO_COGS | OSAT/Packaging·AR_TO_REVENUE | + | +1 | 0.143 | 0.4437 | 방향일치·약함 (lead 1q, r=0.143) |
| CPU | OSAT/Packaging | CPU·FCF_MARGIN | OSAT/Packaging·REVENUE_GROWTH_QOQ | + | +4 | 0.438 | 0.2378 | 방향일치·약함 (lead 4q, r=0.438) |
| CPU | OSAT/Packaging | OSAT/Packaging·DIO | CPU·REVENUE_GROWTH_QOQ | - | +1 | -0.349 | 0.0541 | 방향일치·약함 (lead 1q, r=-0.349) |
| CPU | OSAT/Packaging | OSAT/Packaging·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | CPU·COGS_GROWTH_QOQ | ? | +2 | -0.31 | 0.0896 | 방향일치·약함 (lead 2q, r=-0.31) |
| Hyperscaler | Server Networking | Hyperscaler·COGS_GROWTH_QOQ | Server Networking·REVENUE_GROWTH_QOQ | + | +0 | 0.506 | 0.0031 | 가설지지 (lead 0q, r=0.506, p=0.0031) |
| Hyperscaler | Server Networking | Hyperscaler·CAPEX_GROWTH_QOQ | Server Networking·REVENUE_GROWTH_QOQ | + | +3 | 0.281 | 0.1251 | 방향일치·약함 (lead 3q, r=0.281) |
| Hyperscaler | Server Networking | Hyperscaler·DPO | Server Networking·DSO | + | +0 | 0.592 | 0.0004 | 가설지지 (lead 0q, r=0.592, p=0.0004) |
| Hyperscaler | Server Networking | Hyperscaler·AP_TO_COGS | Server Networking·AR_TO_REVENUE | + | +1 | 0.524 | 0.0018 | 가설지지 (lead 1q, r=0.524, p=0.0018) |
| Hyperscaler | Server Networking | Hyperscaler·FCF_MARGIN | Server Networking·REVENUE_GROWTH_QOQ | + | +1 | 0.183 | 0.3155 | 방향일치·약함 (lead 1q, r=0.183) |
| Hyperscaler | Server Networking | Server Networking·DIO | Hyperscaler·REVENUE_GROWTH_QOQ | - | +2 | -0.094 | 0.616 | 방향일치·약함 (lead 2q, r=-0.094) |
| Hyperscaler | Server Networking | Server Networking·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Hyperscaler·COGS_GROWTH_QOQ | ? | +1 | 0.523 | 0.0025 | 가설지지 (lead 1q, r=0.523, p=0.0025) |
| Server OEM | Server Networking | Server OEM·COGS_GROWTH_QOQ | Server Networking·REVENUE_GROWTH_QOQ | + | +0 | 0.829 | 0.0 | 가설지지 (lead 0q, r=0.829, p=0.0) |
| Server OEM | Server Networking | Server OEM·CAPEX_GROWTH_QOQ | Server Networking·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Server OEM | Server Networking | Server OEM·DPO | Server Networking·DSO | + | +0 | -0.809 | 0.0 | 부호불일치(기대 +, 실제 -) |
| Server OEM | Server Networking | Server OEM·AP_TO_COGS | Server Networking·AR_TO_REVENUE | + | +2 | -0.243 | 0.1726 | 부호불일치(기대 +, 실제 -) |
| Server OEM | Server Networking | Server OEM·FCF_MARGIN | Server Networking·REVENUE_GROWTH_QOQ | + | +3 | 0.357 | 0.2816 | 방향일치·약함 (lead 3q, r=0.357) |
| Server OEM | Server Networking | Server Networking·DIO | Server OEM·REVENUE_GROWTH_QOQ | - | +3 | 0.273 | 0.1368 | 부호불일치(기대 -, 실제 +) |
| Server OEM | Server Networking | Server Networking·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Server OEM·COGS_GROWTH_QOQ | ? | +2 | -0.133 | 0.4691 | 방향일치·약함 (lead 2q, r=-0.133) |
| AI Chip | Foundry | AI Chip·COGS_GROWTH_QOQ | Foundry·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| AI Chip | Foundry | AI Chip·CAPEX_GROWTH_QOQ | Foundry·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| AI Chip | Foundry | AI Chip·DPO | Foundry·DSO | + | nan | nan | nan | insufficient data |
| AI Chip | Foundry | AI Chip·AP_TO_COGS | Foundry·AR_TO_REVENUE | + | nan | nan | nan | insufficient data |
| AI Chip | Foundry | AI Chip·FCF_MARGIN | Foundry·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| AI Chip | Foundry | Foundry·DIO | AI Chip·REVENUE_GROWTH_QOQ | - | nan | nan | nan | insufficient data |
| AI Chip | Foundry | Foundry·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | AI Chip·COGS_GROWTH_QOQ | ? | nan | nan | nan | insufficient data |
| CPU | Foundry | CPU·COGS_GROWTH_QOQ | Foundry·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| CPU | Foundry | CPU·CAPEX_GROWTH_QOQ | Foundry·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| CPU | Foundry | CPU·DPO | Foundry·DSO | + | nan | nan | nan | insufficient data |
| CPU | Foundry | CPU·AP_TO_COGS | Foundry·AR_TO_REVENUE | + | nan | nan | nan | insufficient data |
| CPU | Foundry | CPU·FCF_MARGIN | Foundry·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| CPU | Foundry | Foundry·DIO | CPU·REVENUE_GROWTH_QOQ | - | nan | nan | nan | insufficient data |
| CPU | Foundry | Foundry·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | CPU·COGS_GROWTH_QOQ | ? | nan | nan | nan | insufficient data |
| Server Networking | Foundry | Server Networking·COGS_GROWTH_QOQ | Foundry·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Server Networking | Foundry | Server Networking·CAPEX_GROWTH_QOQ | Foundry·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Server Networking | Foundry | Server Networking·DPO | Foundry·DSO | + | nan | nan | nan | insufficient data |
| Server Networking | Foundry | Server Networking·AP_TO_COGS | Foundry·AR_TO_REVENUE | + | nan | nan | nan | insufficient data |
| Server Networking | Foundry | Server Networking·FCF_MARGIN | Foundry·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Server Networking | Foundry | Foundry·DIO | Server Networking·REVENUE_GROWTH_QOQ | - | nan | nan | nan | insufficient data |
| Server Networking | Foundry | Foundry·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Server Networking·COGS_GROWTH_QOQ | ? | nan | nan | nan | insufficient data |
| CPU | Server ODM | CPU·COGS_GROWTH_QOQ | Server ODM·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| CPU | Server ODM | CPU·CAPEX_GROWTH_QOQ | Server ODM·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| CPU | Server ODM | CPU·DPO | Server ODM·DSO | + | nan | nan | nan | insufficient data |
| CPU | Server ODM | CPU·AP_TO_COGS | Server ODM·AR_TO_REVENUE | + | nan | nan | nan | insufficient data |
| CPU | Server ODM | CPU·FCF_MARGIN | Server ODM·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| CPU | Server ODM | Server ODM·DIO | CPU·REVENUE_GROWTH_QOQ | - | nan | nan | nan | insufficient data |
| CPU | Server ODM | Server ODM·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | CPU·COGS_GROWTH_QOQ | ? | nan | nan | nan | insufficient data |
| DRAM | Server ODM | DRAM·COGS_GROWTH_QOQ | Server ODM·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| DRAM | Server ODM | DRAM·CAPEX_GROWTH_QOQ | Server ODM·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| DRAM | Server ODM | DRAM·DPO | Server ODM·DSO | + | nan | nan | nan | insufficient data |
| DRAM | Server ODM | DRAM·AP_TO_COGS | Server ODM·AR_TO_REVENUE | + | nan | nan | nan | insufficient data |
| DRAM | Server ODM | DRAM·FCF_MARGIN | Server ODM·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| DRAM | Server ODM | Server ODM·DIO | DRAM·REVENUE_GROWTH_QOQ | - | nan | nan | nan | insufficient data |
| DRAM | Server ODM | Server ODM·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | DRAM·COGS_GROWTH_QOQ | ? | nan | nan | nan | insufficient data |
| NAND | Server ODM | NAND·COGS_GROWTH_QOQ | Server ODM·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| NAND | Server ODM | NAND·CAPEX_GROWTH_QOQ | Server ODM·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| NAND | Server ODM | NAND·DPO | Server ODM·DSO | + | nan | nan | nan | insufficient data |
| NAND | Server ODM | NAND·AP_TO_COGS | Server ODM·AR_TO_REVENUE | + | nan | nan | nan | insufficient data |
| NAND | Server ODM | NAND·FCF_MARGIN | Server ODM·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| NAND | Server ODM | Server ODM·DIO | NAND·REVENUE_GROWTH_QOQ | - | nan | nan | nan | insufficient data |
| NAND | Server ODM | Server ODM·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | NAND·COGS_GROWTH_QOQ | ? | nan | nan | nan | insufficient data |
| AI Chip | Server ODM | AI Chip·COGS_GROWTH_QOQ | Server ODM·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| AI Chip | Server ODM | AI Chip·CAPEX_GROWTH_QOQ | Server ODM·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| AI Chip | Server ODM | AI Chip·DPO | Server ODM·DSO | + | nan | nan | nan | insufficient data |
| AI Chip | Server ODM | AI Chip·AP_TO_COGS | Server ODM·AR_TO_REVENUE | + | nan | nan | nan | insufficient data |
| AI Chip | Server ODM | AI Chip·FCF_MARGIN | Server ODM·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| AI Chip | Server ODM | Server ODM·DIO | AI Chip·REVENUE_GROWTH_QOQ | - | nan | nan | nan | insufficient data |
| AI Chip | Server ODM | Server ODM·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | AI Chip·COGS_GROWTH_QOQ | ? | nan | nan | nan | insufficient data |

## 3. 해석 메모 (직접 작성)

> 아래에 가설지지된 쌍의 경제적 해석, 시차 안정성, 표본 한계 등을 적으세요.

- 
- 
- 


## 4. 방법·한계

- lag k>0 = X가 Y를 k분기 선행. 부호는 가이드 문서의 기대부호와 대조.

- 기업간은 섹션 구성사 feature의 분기 평균으로 집계(규모효과 완화).

- Foundry·Server ODM은 12분기 미만으로 데이터 부족.

- CAPEX_TO_OCF·CASH_RUNWAY 등 비율은 상하위 2% winsorize.

- 상관≠인과: 가설지지 쌍은 Granger·rolling·event study로 추가 검증 권장.
