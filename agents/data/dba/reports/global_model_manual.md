# VECM Global Model — Formula 정식화 & 매뉴얼 (산출물 b)

**문서 유형:** 모형 정식화 + 사용 매뉴얼 (논문 §모형)
**기반:** `accounting_flow_theory.md`(회계 공적분 제약) · `universal.py`(보편 채널) · `vecm.py`(추정)
**최종 수정:** 2026-07-20

---

## 1. 개요

AI 반도체 공급망을 **하나의 연립 오차수정 시스템(VECM)** 으로 모형화한다. 각 공급사 섹터의
매출이 고객 섹터 매출에 대해 회계적 장기균형(거래 항등식)으로 오차수정하고, 충격이 밸류체인을
타고 전파된다. Oxford Economics GEM의 국가 방정식(ECM+무역 연결)을 **산업(섹터) 단위**로 이식한
mini-GEM이다.

- **단위:** 섹터 $s$ (고객·공급사), 사용자 정의 관계 `valuechain.RELATIONSHIPS` ($C\to S$).
- **주 변수:** $y_s=\log\text{Rev}_s$ (섹터 매출 로그). 보편성 검증(`universal`)에서 매출→매출이
  전 엣지 보편성 1.0으로 확인되어 시스템 backbone으로 채택.
- **외생(exogenous):** 최상류 고객 Hyperscaler·Server OEM (공급사로 등장하지 않음).
- **내생(endogenous):** AI Chip, CPU, DRAM, NAND, Server Networking, HW Equipment, OSAT.

---

## 2. 상태벡터와 분해

$$\mathbf{y}_t=\begin{bmatrix}\mathbf{y}^{x}_t\\ \mathbf{y}^{n}_t\end{bmatrix},\qquad
\mathbf{y}^{x}_t=\text{외생 섹터 log매출},\quad \mathbf{y}^{n}_t=\text{내생 섹터 log매출}$$

내생 섹터 수 $m$, 외생 섹터 수 $k$. 전체 $N=m+k$.

---

## 3. 장기 공적분 관계 (회계 제약)

이론 §5의 거래 항등식 $\text{Rev}_S=\sum_C\omega_{C\to S}\text{Purch}_C$ 를 로그-선형화하면, 각 내생
섹터 $s$마다 **하나의 공적분 벡터**가 존재한다:

$$\boxed{\;u_{s,t}=y_{s,t}-c_s-\sum_{c:\,c\to s}\theta_{s,c}\,y_{c,t}-\boldsymbol{\delta}_s'\mathbf{Q}_t\;}\tag{3.1}$$

- $\theta_{s,c}\ge 0$: 고객 $c$ 매출 1% → 공급사 $s$ 매출 장기 $\theta_{s,c}$% (수요 pass-through).
- $\mathbf{Q}_t$: 분기 계절더미(Q2,Q3,Q4), $\boldsymbol{\delta}_s$ 계수.
- $u_{s,t}$: 균형편차(disequilibrium). 공적분이면 $u_{s,t}\sim I(0)$ (정상).

행렬형: $\;\mathbf{u}_t=\boldsymbol\beta'\mathbf{y}_t-\mathbf{c}-\boldsymbol\Delta\mathbf{Q}_t$, 여기서
$\boldsymbol\beta'$는 각 행이 (3.1)의 공적분 벡터.

---

## 4. 단기 VECM (오차수정)

$$\boxed{\;\Delta y_{s,t}=\alpha_s\,u_{s,t-1}+\sum_{c:\,c\to s}\beta_{s,c}\,\Delta y_{c,t}+\eta_{s,t}\;}\tag{4.1}$$

- $\alpha_s<0$: **오차수정 속도**. 균형편차의 $-\alpha_s$ 비율이 매분기 교정됨. $\alpha_s<0$·유의이면
  장기균형이 복원(공적분 성립)됨을 뜻한다.
- $\beta_{s,c}$: 단기(즉시) 전달 탄력성.
- $\eta_{s,t}$: 구조 충격.
- **반감기:** $h_s=\ln(0.5)/\ln(1+\alpha_s)$ 분기 (조정 속도의 직관적 지표).

행렬형(내생 블록):
$$\Delta\mathbf{y}^{n}_t=\boldsymbol\alpha\,\mathbf{u}_{t-1}+\mathbf{B}\,\Delta\mathbf{y}_t+\boldsymbol\eta_t,
\qquad \boldsymbol\Pi=\boldsymbol\alpha\boldsymbol\beta'\ (\text{rank}=m)$$

---

## 5. 추정 (Engle–Granger 2단계, 다변량)

statsmodels 없이 numpy OLS로 추정 (`vecm.estimate_ecm_multi`):

1. **1단계 (장기):** (3.1)을 log-level + 계절더미로 OLS → $\hat\theta_{s,c},\hat c_s$, 잔차 $\hat u_{s}$.
2. **공적분 점검:** $\hat u_s$의 정상성(ADF). 표본 한계로 검정력 낮음 → $\hat\alpha_s$ 부호·유의 병행.
3. **2단계 (단기):** (4.1)을 $\Delta y_s$ 회귀 → $\hat\alpha_s,\hat\beta_{s,c}$.

> ⚠️ 표본 $\approx$40분기 + 2020–26 구조변화 → Johansen 다중공적분은 자유도 부족. 섹터별 단일
> 공적분(Engle–Granger)으로 축소하고, 향후 데이터 축적 시 Johansen VECM으로 확장한다.

---

## 6. 충격 전파 = 시뮬레이션 (comparative statics)

외생 섹터에 영구 충격 $\Delta y^{x}=\mathbf{e}$ (예: Hyperscaler $+\log(1.1)$)를 가할 때의
**새 장기균형**은 (3.1)에서 $u_s=0$ (균형)로 두고 재귀적으로 푼다:

$$y^{n}_s{}^{*}=\sum_{c}\theta_{s,c}\,y_c^{*}\quad\Longrightarrow\quad
\boxed{\;\mathbf{y}^{n*}=(\mathbf{I}-\boldsymbol\Theta_{nn})^{-1}\boldsymbol\Theta_{nx}\,\mathbf{e}\;}\tag{6.1}$$

- $\boldsymbol\Theta_{nn}$: 내생↔내생 $\theta$ 행렬, $\boldsymbol\Theta_{nx}$: 내생←외생 $\theta$ 행렬.
- **안정 조건:** $\rho(\boldsymbol\Theta_{nn})<1$ (스펙트럼 반경 <1)이면 (6.1) 수렴. 실제 $\theta\approx0.2\text{–}0.5$라
  성립. 매출 % 반응 $=\exp(y_s^*)-1$.
- **동적 IRF 주의:** (4.1)의 완전 동적 시뮬레이션은 40분기 표본에서 $\hat\beta$ 불안정으로 발산할 수
  있다. 따라서 **안정적인 장기균형(6.1) + 조정 반감기 $h_s$** 로 시뮬레이션을 정의한다.

---

## 7. 추정 결과 요약 (실측)

`vecm.build_system` 추정치 (상세: `reports/vecm_minigem.md`, `vecm.html`):

| 공급사(Y) | 고객(X) & θ | 조정 λ (t) | 오차수정 |
|---|---|---|---|
| DRAM | AI Chip 0.22 · OEM 0.46 · Hyp −0.09 | −0.32 (−2.1) | ✅ |
| NAND | OEM 0.34 · Hyp 0.19 · AIChip −0.05 | −0.26 (−2.0) | ✅ |
| HW Equipment | DRAM 0.30 · CPU −0.35 | −1.04 (−5.3) | ✅ |
| AI Chip | Hyp 0.31 · OEM 0.34 | 0.01 (0.1) | · |
| Server Networking | Hyp 0.28 · OEM 0.22 | −0.11 (−0.9) | · |
| OSAT | AI Chip 0.41 · CPU 0.58 | −0.27 (−1.3) | · |

**대표 시나리오 (Hyperscaler +10% 영구충격, 식 6.1):** AI Chip +3.0%, Server Networking +2.7%,
NAND +1.7%, OSAT +0.8% (하류 전파).

---

## 8. 사용 매뉴얼

```python
import panel as P, vecm as VE
long = P.load_long()                       # CSV 시작점
eqs, exog, logrev = VE.build_system(long)  # 시스템 추정

# 충격 시뮬레이션 (외생 섹터 +10%)
irf = VE.simulate(eqs, exog, "hyperscalers", shock_pct=10)   # 장기균형 전파 + 반감기
print(irf)                                                    # 섹터별 % 반응

# 리포트/HTML
VE.generate_md(eqs, exog, long, "reports/vecm_minigem.md")
VE.generate_html(eqs, exog, long, "vecm.html")
```

- 충격 섹터·크기 변경: `simulate(eqs, exog, "<sector>", shock_pct=N)`.
- 기업 단위 충격 시뮬레이션(특정 기업 분기 지표 → 장기추세)은 **산출물 c (`simulator.html`)** 의
  인터랙티브 UI로 제공.

---

## 9. 한계와 확장

- **식별:** 상관·오차수정은 통계적 관계. 실제 거래는 10-K 고객집중도로 교차확인.
- **표본:** 40분기 → 단일 공적분. 데이터 축적 시 Johansen VECM / BVAR로 확장.
- **커버리지:** Foundry·ODM 제외(데이터 부족). CSV에 데이터 쌓이면 CORE에 자동 편입.
- **비선형:** 회계 정책·가격 효과는 로그-선형 근사의 한계. 향후 상태의존(regime) 확장 여지.
