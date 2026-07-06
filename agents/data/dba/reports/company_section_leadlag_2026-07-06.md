# 기업·섹션 Lead-Lag 분석 (기업/섹션 위상 · 네트워크 · 병목)

**분석일:** 2026-07-06 · **데이터:** `panel_long` · **엔진:** `run_analysis.py` + `leadlag.py`

매출 YoY(z-score) 시차상관 기반. phase_score 음수=상류(선행), 양수=하류(후행).


## 1. 기업 위상 (선행 ↔ 후행)

| company | sector | phase_score | rank |
|---|---|---|---|
| AMD | AI Chip | -1.434 | 1 |
| Applied Mat | FabEquip | -1.022 | 2 |
| Amkor | Packaging | -0.84 | 3 |
| Micron | DRAM | -0.7 | 4 |
| Broadcom | AI Chip | -0.335 | 5 |
| Microsoft | Hyperscaler | -0.313 | 6 |
| Lam Research | FabEquip | -0.028 | 7 |
| Vertiv | Power | 0.0 | 8 |
| NVIDIA | AI Chip | 0.015 | 9 |
| Super Micro | Server OEM | 0.023 | 10 |
| Eaton | Power | 0.422 | 11 |
| Dell | Server OEM | 0.601 | 12 |
| Arista | Networking | 0.671 | 13 |
| Modine | Cooling | 1.275 | 14 |
| Marvell | AI Chip | 1.785 | 15 |

## 2. 섹션 위상 순서

| section | phase_score | rank |
|---|---|---|
| FabEquip | -0.757 | 1 |
| Packaging | -0.643 | 2 |
| Server OEM | -0.417 | 3 |
| DRAM | -0.215 | 4 |
| AI Chip | -0.102 | 5 |
| Hyperscaler | 0.079 | 6 |
| Networking | 0.336 | 7 |
| Power | 0.546 | 8 |
| Cooling | 1.499 | 9 |

## 3. Lead-Lag 네트워크 (상위 엣지)

| from_leader | to_follower | lead_quarters | peak_corr | granger_p_fwd | score |
|---|---|---|---|---|---|
| Applied Mat | Lam Research | 1.0 | 0.855 | 0.0 | 1.005 |
| Applied Mat | Marvell | 4.0 | 0.905 | nan | 1.005 |
| Arista | Modine | 2.0 | 0.652 | 0.001 | 0.902 |
| AMD | Lam Research | 1.0 | 0.644 | 0.018 | 0.894 |
| Amkor | Arista | 4.0 | 0.611 | 0.004 | 0.861 |
| Applied Mat | Arista | 2.0 | 0.587 | 0.006 | 0.837 |
| Amkor | Applied Mat | 1.0 | 0.574 | 0.019 | 0.824 |
| AMD | Marvell | 4.0 | 0.792 | nan | 0.792 |
| Lam Research | Marvell | 3.0 | 0.678 | nan | 0.778 |
| Lam Research | Dell | 1.0 | 0.524 | 0.072 | 0.774 |
| Applied Mat | Dell | 3.0 | 0.505 | 0.014 | 0.755 |
| Amkor | Marvell | 4.0 | 0.654 | nan | 0.754 |
| Amkor | Lam Research | 2.0 | 0.503 | 0.012 | 0.753 |
| Micron | Marvell | 4.0 | 0.641 | nan | 0.741 |
| Applied Mat | Modine | 4.0 | 0.595 | 0.001 | 0.695 |

## 4. 운전자본 병목 (OC=DIO+DSO)

| company | status | recent_OC_days | OC_yoy_recent | congested_Q_of_last4 | driver | internal_congestion |
|---|---|---|---|---|---|---|
| Microsoft | Healthy | 95.5 | 0.067 | 0.0 | - | False |
| Vertiv | insufficient data | nan | nan | nan | nan | nan |
| Eaton | insufficient data | nan | nan | nan | nan | nan |
| Modine | Healthy | 137.4 | -0.045 | 0.0 | - | False |
| Applied Mat | Healthy | 222.3 | 0.041 | 0.0 | - | False |
| Lam Research | Healthy | 228.7 | -0.099 | 0.0 | - | False |
| NVIDIA | Healthy | 163.0 | 0.069 | 0.0 | - | False |
| AMD | Congestion Warning | 272.7 | -0.036 | 1.0 | Inventory build-up (DIO) | True |
| Broadcom | Congestion Warning | 86.5 | 0.304 | 2.0 | Receivables build-up (DSO) | True |
| Marvell | Congestion Warning | 239.6 | 0.496 | 3.0 | Receivables build-up (DSO) | True |
| Micron | Healthy | 201.9 | -0.21 | 0.0 | - | False |
| Amkor | Congestion Warning | 127.9 | 0.348 | 1.0 | Inventory build-up (DIO) | True |
| Arista | Healthy | 367.3 | 0.02 | 0.0 | - | False |
| Super Micro | Healthy | 146.4 | -0.215 | 0.0 | - | False |
| Dell | Congestion Warning | 120.3 | 0.323 | 4.0 | Inventory build-up (DIO) | True |

## 5. 통합 병목 매트릭스

| company | internal_congestion_A | transmission_block_B | diagnosis | prescription |
|---|---|---|---|---|
| Microsoft | False | False | Healthy | - |
| Vertiv | False | False | Healthy | - |
| Eaton | False | False | Healthy | - |
| Modine | False | False | Healthy | - |
| Applied Mat | False | False | Healthy | - |
| Lam Research | False | True | Transmission bottleneck | Re-interpret upstream demand |
| NVIDIA | False | False | Healthy | - |
| AMD | True | False | Internal bottleneck | Production / collection management |
| Broadcom | True | False | Internal bottleneck | Production / collection management |
| Marvell | True | False | Internal bottleneck | Production / collection management |
| Micron | False | False | Healthy | - |
| Amkor | True | False | Internal bottleneck | Production / collection management |
| Arista | False | True | Transmission bottleneck | Re-interpret upstream demand |
| Super Micro | False | False | Healthy | - |
| Dell | True | True | Compound bottleneck | Demand-supply realignment |

## 6. 한계
- 표본 ~40분기, 상관 1차·Granger 2차. 섹션 위상은 구성사 얇으면 노이즈.
