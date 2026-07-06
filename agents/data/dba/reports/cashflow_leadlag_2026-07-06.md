# 현금흐름 병목 & Lead-Lag 분석 리포트

**분석일:** 2026-07-06 · **데이터:** `panel_long`(accounts_payable 포함) · **엔진:** `features.py` + `cashflow_leadlag.py` (가이드 문서 §4·§5·§9 구현)

**판정 규칙:** 상관 부호가 기대부호와 일치 + p<0.05 → **가설지지**. 부호만 일치 → 방향일치·약함. 부호 반대 → 부호불일치.


## 1. 기업 내부 (운전자본 병목 → 현금흐름)

- 분석 케이스 80 · 분석가능 76 · **가설지지 17건**

| 기업 | X(선행) | Y(후행) | 기대 | lag | Pearson | p | Granger | 판정 |
|---|---|---|---|---|---|---|---|---|
| NVIDIA | CCC | FCF_MARGIN | - | +2 | 0.925 | 0.0082 | nan | 부호불일치(기대 -, 실제 +) |
| NVIDIA | DIO | FCF_MARGIN | - | +2 | 0.823 | 0.044 | nan | 부호불일치(기대 -, 실제 +) |
| NVIDIA | DSO | OCF_MARGIN | - | +2 | 0.667 | 0.0497 | nan | 부호불일치(기대 -, 실제 +) |
| NVIDIA | DPO | OCF_MARGIN | + | +2 | 0.032 | 0.9355 | nan | 방향일치·약함 (lead 2q, r=0.032) |
| NVIDIA | AR_GROWTH_MINUS_REVENUE_GROWTH | OCF_MARGIN | - | +3 | -0.226 | 0.5905 | nan | 방향일치·약함 (lead 3q, r=-0.226) |
| NVIDIA | AP_GROWTH_MINUS_COGS_GROWTH | OCF_MARGIN | + | +2 | 0.455 | 0.2186 | nan | 방향일치·약함 (lead 2q, r=0.455) |
| NVIDIA | INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | FCF_MARGIN | - | +1 | -0.179 | 0.7003 | 0.0754 | 방향일치·약함 (lead 1q, r=-0.179) |
| NVIDIA | CAPEX_TO_OCF | FCF_MARGIN | - | +0 | -0.925 | 0.0004 | 0.88 | 가설지지 (lead 0q, r=-0.925, p=0.0004) |
| AMD | CCC | FCF_MARGIN | - | +4 | -0.494 | 0.2604 | nan | 방향일치·약함 (lead 4q, r=-0.494) |
| AMD | DIO | FCF_MARGIN | - | +4 | -0.774 | 0.0412 | nan | 가설지지 (lead 4q, r=-0.774, p=0.0412) |
| AMD | DSO | OCF_MARGIN | - | +4 | -0.287 | 0.5324 | nan | 방향일치·약함 (lead 4q, r=-0.287) |
| AMD | DPO | OCF_MARGIN | + | +2 | 0.468 | 0.2036 | nan | 방향일치·약함 (lead 2q, r=0.468) |
| AMD | AR_GROWTH_MINUS_REVENUE_GROWTH | OCF_MARGIN | - | +0 | -0.531 | 0.0926 | 0.3714 | 방향일치·약함 (lead 0q, r=-0.531) |
| AMD | AP_GROWTH_MINUS_COGS_GROWTH | OCF_MARGIN | + | +0 | 0.192 | 0.5716 | 0.8437 | 방향일치·약함 (lead 0q, r=0.192) |
| AMD | INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | FCF_MARGIN | - | +4 | -0.628 | 0.1309 | nan | 방향일치·약함 (lead 4q, r=-0.628) |
| AMD | CAPEX_TO_OCF | FCF_MARGIN | - | +0 | 0.525 | 0.0799 | 0.7257 | 부호불일치(기대 -, 실제 +) |
| Micron Technology | CCC | FCF_MARGIN | - | +0 | -0.649 | 0.0307 | 0.6745 | 가설지지 (lead 0q, r=-0.649, p=0.0307) |
| Micron Technology | DIO | FCF_MARGIN | - | +0 | -0.608 | 0.0473 | 0.4609 | 가설지지 (lead 0q, r=-0.608, p=0.0473) |
| Micron Technology | DSO | OCF_MARGIN | - | +0 | -0.495 | 0.1212 | 0.0073 | 방향일치·약함 (lead 0q, r=-0.495) |
| Micron Technology | DPO | OCF_MARGIN | + | +4 | 0.684 | 0.0903 | nan | 방향일치·약함 (lead 4q, r=0.684) |
| Micron Technology | AR_GROWTH_MINUS_REVENUE_GROWTH | OCF_MARGIN | - | +3 | -0.578 | 0.1333 | nan | 방향일치·약함 (lead 3q, r=-0.578) |
| Micron Technology | AP_GROWTH_MINUS_COGS_GROWTH | OCF_MARGIN | + | +3 | 0.503 | 0.2041 | nan | 방향일치·약함 (lead 3q, r=0.503) |
| Micron Technology | INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | FCF_MARGIN | - | +1 | -0.439 | 0.204 | 0.9502 | 방향일치·약함 (lead 1q, r=-0.439) |
| Micron Technology | CAPEX_TO_OCF | FCF_MARGIN | - | +0 | -0.956 | 0.0 | 0.8688 | 가설지지 (lead 0q, r=-0.956, p=0.0) |
| Intel | CCC | FCF_MARGIN | - | +2 | -0.068 | 0.862 | nan | 방향일치·약함 (lead 2q, r=-0.068) |
| Intel | DIO | FCF_MARGIN | - | +0 | -0.894 | 0.0002 | 0.0017 | 가설지지 (lead 0q, r=-0.894, p=0.0002) |
| Intel | DSO | OCF_MARGIN | - | +4 | -0.405 | 0.3669 | nan | 방향일치·약함 (lead 4q, r=-0.405) |
| Intel | DPO | OCF_MARGIN | + | +0 | -0.751 | 0.0077 | 0.0406 | 부호불일치(기대 +, 실제 -) |
| Intel | AR_GROWTH_MINUS_REVENUE_GROWTH | OCF_MARGIN | - | +0 | -0.074 | 0.8279 | 0.4254 | 방향일치·약함 (lead 0q, r=-0.074) |
| Intel | AP_GROWTH_MINUS_COGS_GROWTH | OCF_MARGIN | + | +3 | 0.211 | 0.6162 | nan | 방향일치·약함 (lead 3q, r=0.211) |
| Intel | INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | FCF_MARGIN | - | +2 | -0.288 | 0.452 | nan | 방향일치·약함 (lead 2q, r=-0.288) |
| Intel | CAPEX_TO_OCF | FCF_MARGIN | - | +4 | -0.486 | 0.222 | nan | 방향일치·약함 (lead 4q, r=-0.486) |
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

- 분석 케이스 161 · 분석가능 95 · **가설지지 21건**

| 고객 | 공급사 | X(선행) | Y(후행) | 기대 | lag | Pearson | p | 판정 |
|---|---|---|---|---|---|---|---|---|
| Hyperscaler | AI Chip | Hyperscaler·COGS_GROWTH_QOQ | AI Chip·REVENUE_GROWTH_QOQ | + | +0 | 0.197 | 0.2799 | 방향일치·약함 (lead 0q, r=0.197) |
| Hyperscaler | AI Chip | Hyperscaler·CAPEX_GROWTH_QOQ | AI Chip·REVENUE_GROWTH_QOQ | + | +3 | 0.135 | 0.4682 | 방향일치·약함 (lead 3q, r=0.135) |
| Hyperscaler | AI Chip | Hyperscaler·DPO | AI Chip·DSO | + | +0 | 0.537 | 0.0015 | 가설지지 (lead 0q, r=0.537, p=0.0015) |
| Hyperscaler | AI Chip | Hyperscaler·AP_TO_COGS | AI Chip·AR_TO_REVENUE | + | +0 | 0.593 | 0.0003 | 가설지지 (lead 0q, r=0.593, p=0.0003) |
| Hyperscaler | AI Chip | Hyperscaler·FCF_MARGIN | AI Chip·REVENUE_GROWTH_QOQ | + | +3 | 0.121 | 0.5154 | 방향일치·약함 (lead 3q, r=0.121) |
| Hyperscaler | AI Chip | AI Chip·DIO | Hyperscaler·REVENUE_GROWTH_QOQ | - | +2 | -0.04 | 0.8323 | 방향일치·약함 (lead 2q, r=-0.04) |
| Hyperscaler | AI Chip | AI Chip·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Hyperscaler·COGS_GROWTH_QOQ | ? | +2 | -0.579 | 0.0008 | 가설지지 (lead 2q, r=-0.579, p=0.0008) |
| Server OEM | AI Chip | Server OEM·COGS_GROWTH_QOQ | AI Chip·REVENUE_GROWTH_QOQ | + | +0 | 0.643 | 0.0 | 가설지지 (lead 0q, r=0.643, p=0.0) |
| Server OEM | AI Chip | Server OEM·CAPEX_GROWTH_QOQ | AI Chip·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Server OEM | AI Chip | Server OEM·DPO | AI Chip·DSO | + | +0 | -0.266 | 0.1291 | 부호불일치(기대 +, 실제 -) |
| Server OEM | AI Chip | Server OEM·AP_TO_COGS | AI Chip·AR_TO_REVENUE | + | +0 | 0.085 | 0.6254 | 방향일치·약함 (lead 0q, r=0.085) |
| Server OEM | AI Chip | Server OEM·FCF_MARGIN | AI Chip·REVENUE_GROWTH_QOQ | + | +3 | 0.354 | 0.286 | 방향일치·약함 (lead 3q, r=0.354) |
| Server OEM | AI Chip | AI Chip·DIO | Server OEM·REVENUE_GROWTH_QOQ | - | +3 | 0.286 | 0.1183 | 부호불일치(기대 -, 실제 +) |
| Server OEM | AI Chip | AI Chip·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Server OEM·COGS_GROWTH_QOQ | ? | +2 | -0.223 | 0.2197 | 방향일치·약함 (lead 2q, r=-0.223) |
| Server OEM | CPU | Server OEM·COGS_GROWTH_QOQ | CPU·REVENUE_GROWTH_QOQ | + | +0 | 0.188 | 0.2951 | 방향일치·약함 (lead 0q, r=0.188) |
| Server OEM | CPU | Server OEM·CAPEX_GROWTH_QOQ | CPU·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Server OEM | CPU | Server OEM·DPO | CPU·DSO | + | +1 | -0.645 | 0.0001 | 부호불일치(기대 +, 실제 -) |
| Server OEM | CPU | Server OEM·AP_TO_COGS | CPU·AR_TO_REVENUE | + | +1 | -0.494 | 0.0034 | 부호불일치(기대 +, 실제 -) |
| Server OEM | CPU | Server OEM·FCF_MARGIN | CPU·REVENUE_GROWTH_QOQ | + | +3 | 0.311 | 0.3822 | 방향일치·약함 (lead 3q, r=0.311) |
| Server OEM | CPU | CPU·DIO | Server OEM·REVENUE_GROWTH_QOQ | - | +2 | 0.297 | 0.1044 | 부호불일치(기대 -, 실제 +) |
| Server OEM | CPU | CPU·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Server OEM·COGS_GROWTH_QOQ | ? | +3 | 0.303 | 0.098 | 방향일치·약함 (lead 3q, r=0.303) |
| Hyperscaler | CPU | Hyperscaler·COGS_GROWTH_QOQ | CPU·REVENUE_GROWTH_QOQ | + | +1 | 0.198 | 0.2781 | 방향일치·약함 (lead 1q, r=0.198) |
| Hyperscaler | CPU | Hyperscaler·CAPEX_GROWTH_QOQ | CPU·REVENUE_GROWTH_QOQ | + | +3 | 0.184 | 0.331 | 방향일치·약함 (lead 3q, r=0.184) |
| Hyperscaler | CPU | Hyperscaler·DPO | CPU·DSO | + | +1 | 0.673 | 0.0 | 가설지지 (lead 1q, r=0.673, p=0.0) |
| Hyperscaler | CPU | Hyperscaler·AP_TO_COGS | CPU·AR_TO_REVENUE | + | +2 | 0.505 | 0.0032 | 가설지지 (lead 2q, r=0.505, p=0.0032) |
| Hyperscaler | CPU | Hyperscaler·FCF_MARGIN | CPU·REVENUE_GROWTH_QOQ | + | +2 | 0.229 | 0.2153 | 방향일치·약함 (lead 2q, r=0.229) |
| Hyperscaler | CPU | CPU·DIO | Hyperscaler·REVENUE_GROWTH_QOQ | - | +1 | -0.252 | 0.172 | 방향일치·약함 (lead 1q, r=-0.252) |
| Hyperscaler | CPU | CPU·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Hyperscaler·COGS_GROWTH_QOQ | ? | +2 | -0.588 | 0.0006 | 가설지지 (lead 2q, r=-0.588, p=0.0006) |
| AI Chip | DRAM | AI Chip·COGS_GROWTH_QOQ | DRAM·REVENUE_GROWTH_QOQ | + | +0 | 0.507 | 0.003 | 가설지지 (lead 0q, r=0.507, p=0.003) |
| AI Chip | DRAM | AI Chip·CAPEX_GROWTH_QOQ | DRAM·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| AI Chip | DRAM | AI Chip·DPO | DRAM·DSO | + | +0 | 0.153 | 0.4026 | 방향일치·약함 (lead 0q, r=0.153) |
| AI Chip | DRAM | AI Chip·AP_TO_COGS | DRAM·AR_TO_REVENUE | + | +0 | 0.234 | 0.1908 | 방향일치·약함 (lead 0q, r=0.234) |
| AI Chip | DRAM | AI Chip·FCF_MARGIN | DRAM·REVENUE_GROWTH_QOQ | + | +3 | 0.348 | 0.3589 | 방향일치·약함 (lead 3q, r=0.348) |
| AI Chip | DRAM | DRAM·DIO | AI Chip·REVENUE_GROWTH_QOQ | - | +1 | 0.126 | 0.491 | 부호불일치(기대 -, 실제 +) |
| AI Chip | DRAM | DRAM·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | AI Chip·COGS_GROWTH_QOQ | ? | +3 | -0.339 | 0.0619 | 방향일치·약함 (lead 3q, r=-0.339) |
| Hyperscaler | DRAM | Hyperscaler·COGS_GROWTH_QOQ | DRAM·REVENUE_GROWTH_QOQ | + | +0 | 0.251 | 0.1737 | 방향일치·약함 (lead 0q, r=0.251) |
| Hyperscaler | DRAM | Hyperscaler·CAPEX_GROWTH_QOQ | DRAM·REVENUE_GROWTH_QOQ | + | +3 | 0.285 | 0.1343 | 방향일치·약함 (lead 3q, r=0.285) |
| Hyperscaler | DRAM | Hyperscaler·DPO | DRAM·DSO | + | +0 | 0.558 | 0.0011 | 가설지지 (lead 0q, r=0.558, p=0.0011) |
| Hyperscaler | DRAM | Hyperscaler·AP_TO_COGS | DRAM·AR_TO_REVENUE | + | +0 | 0.449 | 0.0099 | 가설지지 (lead 0q, r=0.449, p=0.0099) |
| Hyperscaler | DRAM | Hyperscaler·FCF_MARGIN | DRAM·REVENUE_GROWTH_QOQ | + | +3 | 0.33 | 0.0803 | 방향일치·약함 (lead 3q, r=0.33) |
| Hyperscaler | DRAM | DRAM·DIO | Hyperscaler·REVENUE_GROWTH_QOQ | - | +3 | -0.031 | 0.8694 | 방향일치·약함 (lead 3q, r=-0.031) |
| Hyperscaler | DRAM | DRAM·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Hyperscaler·COGS_GROWTH_QOQ | ? | +2 | -0.2 | 0.29 | 방향일치·약함 (lead 2q, r=-0.2) |
| Hyperscaler | NAND | Hyperscaler·COGS_GROWTH_QOQ | NAND·REVENUE_GROWTH_QOQ | + | +0 | 0.533 | 0.0017 | 가설지지 (lead 0q, r=0.533, p=0.0017) |
| Hyperscaler | NAND | Hyperscaler·CAPEX_GROWTH_QOQ | NAND·REVENUE_GROWTH_QOQ | + | +3 | 0.165 | 0.3849 | 방향일치·약함 (lead 3q, r=0.165) |
| Hyperscaler | NAND | Hyperscaler·DPO | NAND·DSO | + | +0 | 0.658 | 0.0 | 가설지지 (lead 0q, r=0.658, p=0.0) |
| Hyperscaler | NAND | Hyperscaler·AP_TO_COGS | NAND·AR_TO_REVENUE | + | +0 | 0.584 | 0.0004 | 가설지지 (lead 0q, r=0.584, p=0.0004) |
| Hyperscaler | NAND | Hyperscaler·FCF_MARGIN | NAND·REVENUE_GROWTH_QOQ | + | +1 | 0.271 | 0.1335 | 방향일치·약함 (lead 1q, r=0.271) |
| Hyperscaler | NAND | NAND·DIO | Hyperscaler·REVENUE_GROWTH_QOQ | - | +2 | -0.326 | 0.1291 | 방향일치·약함 (lead 2q, r=-0.326) |
| Hyperscaler | NAND | NAND·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Hyperscaler·COGS_GROWTH_QOQ | ? | +1 | 0.192 | 0.3011 | 방향일치·약함 (lead 1q, r=0.192) |
| Server OEM | NAND | Server OEM·COGS_GROWTH_QOQ | NAND·REVENUE_GROWTH_QOQ | + | +0 | 0.767 | 0.0 | 가설지지 (lead 0q, r=0.767, p=0.0) |
| Server OEM | NAND | Server OEM·CAPEX_GROWTH_QOQ | NAND·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Server OEM | NAND | Server OEM·DPO | NAND·DSO | + | +0 | -0.411 | 0.0175 | 부호불일치(기대 +, 실제 -) |
| Server OEM | NAND | Server OEM·AP_TO_COGS | NAND·AR_TO_REVENUE | + | +0 | 0.121 | 0.497 | 방향일치·약함 (lead 0q, r=0.121) |
| Server OEM | NAND | Server OEM·FCF_MARGIN | NAND·REVENUE_GROWTH_QOQ | + | +3 | 0.382 | 0.2753 | 방향일치·약함 (lead 3q, r=0.382) |
| Server OEM | NAND | NAND·DIO | Server OEM·REVENUE_GROWTH_QOQ | - | +1 | 0.722 | 0.0 | 부호불일치(기대 -, 실제 +) |
| Server OEM | NAND | NAND·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Server OEM·COGS_GROWTH_QOQ | ? | +3 | 0.205 | 0.2695 | 방향일치·약함 (lead 3q, r=0.205) |
| AI Chip | NAND | AI Chip·COGS_GROWTH_QOQ | NAND·REVENUE_GROWTH_QOQ | + | +0 | 0.515 | 0.0022 | 가설지지 (lead 0q, r=0.515, p=0.0022) |
| AI Chip | NAND | AI Chip·CAPEX_GROWTH_QOQ | NAND·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| AI Chip | NAND | AI Chip·DPO | NAND·DSO | + | +1 | -0.209 | 0.2499 | 부호불일치(기대 +, 실제 -) |
| AI Chip | NAND | AI Chip·AP_TO_COGS | NAND·AR_TO_REVENUE | + | +2 | 0.019 | 0.9171 | 방향일치·약함 (lead 2q, r=0.019) |
| AI Chip | NAND | AI Chip·FCF_MARGIN | NAND·REVENUE_GROWTH_QOQ | + | +3 | 0.325 | 0.3592 | 방향일치·약함 (lead 3q, r=0.325) |
| AI Chip | NAND | NAND·DIO | AI Chip·REVENUE_GROWTH_QOQ | - | +2 | -0.085 | 0.6942 | 방향일치·약함 (lead 2q, r=-0.085) |
| AI Chip | NAND | NAND·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | AI Chip·COGS_GROWTH_QOQ | ? | +2 | 0.22 | 0.2262 | 방향일치·약함 (lead 2q, r=0.22) |
| Foundry | HW Equipment | Foundry·COGS_GROWTH_QOQ | HW Equipment·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Foundry | HW Equipment | Foundry·CAPEX_GROWTH_QOQ | HW Equipment·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Foundry | HW Equipment | Foundry·DPO | HW Equipment·DSO | + | nan | nan | nan | insufficient data |
| Foundry | HW Equipment | Foundry·AP_TO_COGS | HW Equipment·AR_TO_REVENUE | + | nan | nan | nan | insufficient data |
| Foundry | HW Equipment | Foundry·FCF_MARGIN | HW Equipment·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Foundry | HW Equipment | HW Equipment·DIO | Foundry·REVENUE_GROWTH_QOQ | - | nan | nan | nan | insufficient data |
| Foundry | HW Equipment | HW Equipment·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Foundry·COGS_GROWTH_QOQ | ? | nan | nan | nan | insufficient data |
| DRAM | HW Equipment | DRAM·COGS_GROWTH_QOQ | HW Equipment·REVENUE_GROWTH_QOQ | + | +0 | 0.251 | 0.1655 | 방향일치·약함 (lead 0q, r=0.251) |
| DRAM | HW Equipment | DRAM·CAPEX_GROWTH_QOQ | HW Equipment·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| DRAM | HW Equipment | DRAM·DPO | HW Equipment·DSO | + | +0 | 0.148 | 0.4184 | 방향일치·약함 (lead 0q, r=0.148) |
| DRAM | HW Equipment | DRAM·AP_TO_COGS | HW Equipment·AR_TO_REVENUE | + | +0 | 0.26 | 0.1446 | 방향일치·약함 (lead 0q, r=0.26) |
| DRAM | HW Equipment | DRAM·FCF_MARGIN | HW Equipment·REVENUE_GROWTH_QOQ | + | +2 | 0.102 | 0.7651 | 방향일치·약함 (lead 2q, r=0.102) |
| DRAM | HW Equipment | HW Equipment·DIO | DRAM·REVENUE_GROWTH_QOQ | - | +1 | -0.079 | 0.6715 | 방향일치·약함 (lead 1q, r=-0.079) |
| DRAM | HW Equipment | HW Equipment·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | DRAM·COGS_GROWTH_QOQ | ? | +1 | 0.049 | 0.7947 | 방향일치·약함 (lead 1q, r=0.049) |
| CPU | HW Equipment | CPU·COGS_GROWTH_QOQ | HW Equipment·REVENUE_GROWTH_QOQ | + | +1 | 0.039 | 0.8317 | 방향일치·약함 (lead 1q, r=0.039) |
| CPU | HW Equipment | CPU·CAPEX_GROWTH_QOQ | HW Equipment·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| CPU | HW Equipment | CPU·DPO | HW Equipment·DSO | + | +0 | 0.121 | 0.5174 | 방향일치·약함 (lead 0q, r=0.121) |
| CPU | HW Equipment | CPU·AP_TO_COGS | HW Equipment·AR_TO_REVENUE | + | +1 | 0.01 | 0.9577 | 방향일치·약함 (lead 1q, r=0.01) |
| CPU | HW Equipment | CPU·FCF_MARGIN | HW Equipment·REVENUE_GROWTH_QOQ | + | +2 | 0.44 | 0.1759 | 방향일치·약함 (lead 2q, r=0.44) |
| CPU | HW Equipment | HW Equipment·DIO | CPU·REVENUE_GROWTH_QOQ | - | +3 | -0.057 | 0.7643 | 방향일치·약함 (lead 3q, r=-0.057) |
| CPU | HW Equipment | HW Equipment·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | CPU·COGS_GROWTH_QOQ | ? | +2 | -0.101 | 0.5873 | 방향일치·약함 (lead 2q, r=-0.101) |
| AI Chip | OSAT/Packaging | AI Chip·COGS_GROWTH_QOQ | OSAT/Packaging·REVENUE_GROWTH_QOQ | + | +0 | 0.153 | 0.4115 | 방향일치·약함 (lead 0q, r=0.153) |
| AI Chip | OSAT/Packaging | AI Chip·CAPEX_GROWTH_QOQ | OSAT/Packaging·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| AI Chip | OSAT/Packaging | AI Chip·DPO | OSAT/Packaging·DSO | + | +2 | 0.363 | 0.0532 | 방향일치·약함 (lead 2q, r=0.363) |
| AI Chip | OSAT/Packaging | AI Chip·AP_TO_COGS | OSAT/Packaging·AR_TO_REVENUE | + | +0 | 0.498 | 0.0037 | 가설지지 (lead 0q, r=0.498, p=0.0037) |
| AI Chip | OSAT/Packaging | AI Chip·FCF_MARGIN | OSAT/Packaging·REVENUE_GROWTH_QOQ | + | +2 | 0.39 | 0.2992 | 방향일치·약함 (lead 2q, r=0.39) |
| AI Chip | OSAT/Packaging | OSAT/Packaging·DIO | AI Chip·REVENUE_GROWTH_QOQ | - | +1 | -0.214 | 0.2487 | 방향일치·약함 (lead 1q, r=-0.214) |
| AI Chip | OSAT/Packaging | OSAT/Packaging·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | AI Chip·COGS_GROWTH_QOQ | ? | +3 | 0.171 | 0.3573 | 방향일치·약함 (lead 3q, r=0.171) |
| CPU | OSAT/Packaging | CPU·COGS_GROWTH_QOQ | OSAT/Packaging·REVENUE_GROWTH_QOQ | + | +1 | 0.34 | 0.066 | 방향일치·약함 (lead 1q, r=0.34) |
| CPU | OSAT/Packaging | CPU·CAPEX_GROWTH_QOQ | OSAT/Packaging·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| CPU | OSAT/Packaging | CPU·DPO | OSAT/Packaging·DSO | + | +0 | 0.144 | 0.4381 | 방향일치·약함 (lead 0q, r=0.144) |
| CPU | OSAT/Packaging | CPU·AP_TO_COGS | OSAT/Packaging·AR_TO_REVENUE | + | +1 | 0.143 | 0.4435 | 방향일치·약함 (lead 1q, r=0.143) |
| CPU | OSAT/Packaging | CPU·FCF_MARGIN | OSAT/Packaging·REVENUE_GROWTH_QOQ | + | +4 | 0.441 | 0.235 | 방향일치·약함 (lead 4q, r=0.441) |
| CPU | OSAT/Packaging | OSAT/Packaging·DIO | CPU·REVENUE_GROWTH_QOQ | - | +1 | -0.336 | 0.065 | 방향일치·약함 (lead 1q, r=-0.336) |
| CPU | OSAT/Packaging | OSAT/Packaging·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | CPU·COGS_GROWTH_QOQ | ? | +2 | -0.276 | 0.1323 | 방향일치·약함 (lead 2q, r=-0.276) |
| Hyperscaler | Server Networking | Hyperscaler·COGS_GROWTH_QOQ | Server Networking·REVENUE_GROWTH_QOQ | + | +0 | 0.489 | 0.0045 | 가설지지 (lead 0q, r=0.489, p=0.0045) |
| Hyperscaler | Server Networking | Hyperscaler·CAPEX_GROWTH_QOQ | Server Networking·REVENUE_GROWTH_QOQ | + | +3 | 0.266 | 0.1477 | 방향일치·약함 (lead 3q, r=0.266) |
| Hyperscaler | Server Networking | Hyperscaler·DPO | Server Networking·DSO | + | +0 | 0.531 | 0.0018 | 가설지지 (lead 0q, r=0.531, p=0.0018) |
| Hyperscaler | Server Networking | Hyperscaler·AP_TO_COGS | Server Networking·AR_TO_REVENUE | + | +1 | 0.51 | 0.0024 | 가설지지 (lead 1q, r=0.51, p=0.0024) |
| Hyperscaler | Server Networking | Hyperscaler·FCF_MARGIN | Server Networking·REVENUE_GROWTH_QOQ | + | +1 | 0.197 | 0.2801 | 방향일치·약함 (lead 1q, r=0.197) |
| Hyperscaler | Server Networking | Server Networking·DIO | Hyperscaler·REVENUE_GROWTH_QOQ | - | +2 | -0.09 | 0.629 | 방향일치·약함 (lead 2q, r=-0.09) |
| Hyperscaler | Server Networking | Server Networking·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Hyperscaler·COGS_GROWTH_QOQ | ? | +1 | 0.514 | 0.0031 | 가설지지 (lead 1q, r=0.514, p=0.0031) |
| Server OEM | Server Networking | Server OEM·COGS_GROWTH_QOQ | Server Networking·REVENUE_GROWTH_QOQ | + | +0 | 0.829 | 0.0 | 가설지지 (lead 0q, r=0.829, p=0.0) |
| Server OEM | Server Networking | Server OEM·CAPEX_GROWTH_QOQ | Server Networking·REVENUE_GROWTH_QOQ | + | nan | nan | nan | insufficient data |
| Server OEM | Server Networking | Server OEM·DPO | Server Networking·DSO | + | +0 | -0.791 | 0.0 | 부호불일치(기대 +, 실제 -) |
| Server OEM | Server Networking | Server OEM·AP_TO_COGS | Server Networking·AR_TO_REVENUE | + | +2 | -0.244 | 0.172 | 부호불일치(기대 +, 실제 -) |
| Server OEM | Server Networking | Server OEM·FCF_MARGIN | Server Networking·REVENUE_GROWTH_QOQ | + | +3 | 0.357 | 0.2816 | 방향일치·약함 (lead 3q, r=0.357) |
| Server OEM | Server Networking | Server Networking·DIO | Server OEM·REVENUE_GROWTH_QOQ | - | +3 | 0.255 | 0.1654 | 부호불일치(기대 -, 실제 +) |
| Server OEM | Server Networking | Server Networking·INVENTORY_GROWTH_MINUS_REVENUE_GROWTH | Server OEM·COGS_GROWTH_QOQ | ? | +2 | -0.133 | 0.4677 | 방향일치·약함 (lead 2q, r=-0.133) |
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
