# VECM mini-GEM — 연립 ECM 시스템 (밸류체인 보편관계 기반)

**분석일:** 2026-07-09 · **데이터:** `panel_long.csv` · **엔진:** `vecm.py`

각 공급사 섹터 매출(log)이 고객 섹터 매출에 오차수정하는 다변량 ECM을 연립. 충격을 외생 섹터에 주면 시스템 전체로 전파(연결적 해석).


- 방정식 섹터: 7 · 외생(최상류) 섹터: Hyperscaler, Server OEM


## 방정식 (장기 탄력성 θ · 조정속도 λ)

| 공급사 (Y) | 고객 (X) | θ (장기탄력성) | λ (조정) | 오차수정 | 장기R² |
|---|---|---|---|---|---|
| AI Chip | Hyperscaler, Server OEM | Hyperscaler=0.31, Server OEM=0.34 | 0.014 (t=0.12) | · | 0.339 |
| CPU | Server OEM, Hyperscaler | Server OEM=0.24, Hyperscaler=-0.08 | -0.17 (t=-1.37) | · | 0.311 |
| DRAM | AI Chip, Hyperscaler, Server OEM | AI Chip=0.22, Hyperscaler=-0.09, Server OEM=0.46 | -0.324 (t=-2.14) | ✅ | 0.565 |
| NAND | Hyperscaler, Server OEM, AI Chip | Hyperscaler=0.19, Server OEM=0.34, AI Chip=-0.05 | -0.259 (t=-1.98) | ✅ | 0.245 |
| Server Networking | Hyperscaler, Server OEM | Hyperscaler=0.28, Server OEM=0.22 | -0.112 (t=-0.91) | · | 0.639 |
| HW Equipment | DRAM, CPU | DRAM=0.3, CPU=-0.35 | -1.043 (t=-5.33) | ✅ | 0.077 |
| OSAT/Packaging | AI Chip, CPU | AI Chip=0.41, CPU=0.58 | -0.266 (t=-1.31) | · | 0.738 |

## 시나리오: Hyperscaler 매출 영구 +10% → 장기 전파 (comparative statics)

| 섹터 | 장기 매출반응 % | 조정 반감기(분기) | 역할 |
|---|---|---|---|
| Hyperscaler | 10.0 | nan | 외생(충격) |
| AI Chip | 2.99 | nan | 방정식 |
| Server Networking | 2.73 | 5.84 | 방정식 |
| NAND | 1.65 | 2.31 | 방정식 |
| OSAT/Packaging | 0.8 | 2.24 | 방정식 |
| HW Equipment | 0.19 | nan | 방정식 |
| Server OEM | 0.0 | nan | 외생 |
| DRAM | -0.2 | 1.77 | 방정식 |
| CPU | -0.72 | 3.72 | 방정식 |

## 해석

- θ = 고객 매출 1% → 공급사 매출 장기 θ%. λ<0·유의 = 오차수정(장기균형 복원).

- 시나리오: 외생 충격이 밸류체인을 타고 하류로 전파되는 연결적 경로.


## 한계

- 표본 ~40분기 + AI붐 구조변화 → 공적분 검정력 낮음. θ·λ 부호로 신뢰도 판단.

- Engle-Granger 다변량 근사(단일 공적분 가정). Johansen VECM은 향후 확장.

- Foundry·ODM 데이터 부족으로 시스템 제외(데이터 쌓이면 CORE에 추가).
