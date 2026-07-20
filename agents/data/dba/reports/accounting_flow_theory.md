# 회계 기반 기업간 Lead-Lag 이론 — 돈의 흐름 구조

**문서 유형:** 이론 (논문 §이론 섹션)
**목적:** 복식부기 항등식으로 기업간·기업내 회계지표의 lead-lag를 도출한다.
회계 전문가가 동의 가능한 수준의 정확한 자금흐름 구조를 정의하고, 검증가능한
lead-lag 가설(P1–P5)을 유도한다. 이 구조가 VECM global model의 공적분 제약이 된다.

**표기:** 기업 $i$, 분기 $t$. $C$=고객(customer), $S$=공급사(supplier). 관계 $C\to S$는
"$C$가 $S$로부터 구매"(사용자 정의 `valuechain.RELATIONSHIPS`).

---

## 1. 기업간 거래의 회계적 양면성 (cross-firm double entry)

고객 $C$가 공급사 $S$로부터 재화를 인도받는 단일 거래는 양사 장부에 **동시에** 기록된다.

| 공급사 $S$ (매출측) | 고객 $C$ (매입측) |
|---|---|
| (차) 매출채권 AR ⟋ (대) 매출 Revenue | (차) 재고 Inventory ⟋ (대) 매입채무 AP |

인도시점 = 수령시점이므로 **매출 인식과 매입 인식은 동일 분기**에 일어난다. 이로부터:

**정의 1 (거래 항등식).** 공급사 매출은 그 공급사에서 구매한 고객들의 매입액 합이다.
$$\text{Rev}_{S,t} \;=\; \sum_{C:\,C\to S} \omega_{C\to S}\,\text{Purch}_{C,t}, \qquad
\text{Purch}_{C,t} = \text{COGS}_{C,t} + \Delta\text{Inv}_{C,t}$$
여기서 $\omega_{C\to S}\in[0,1]$는 고객 $C$의 매입 중 공급사 $S$가 차지하는 비중(거래 shares,
$\sum_S \omega_{C\to S}\le 1$). 매입 $\text{Purch}$는 회계상 $\text{COGS}+\Delta\text{Inventory}$
(당기 소비 + 재고 순증)로 정의된다.

**정의 2 (거울 항등식, balance-sheet mirror).** 동일 미결제 거래에 대해 고객의 미지급은
공급사의 미수와 같다.
$$\text{AP}^{(C\to S)}_{C,t} \;=\; \text{AR}^{(C\to S)}_{S,t}$$

> ⚠️ 실증 한계: 공시 재무제표는 거래처별 분해($\omega$, 거래별 AR/AP)를 제공하지 않는다.
> 따라서 위 항등식은 **집계 수준의 근사**로 검증한다(고객 총매입 vs 공급사 총매출). $\omega$는
> 기업쌍 상관가중(`pairwise_cashflow`)으로 추정한다. 이는 논문의 측정오차 논의 대상이다.

---

## 2. 기업내 운전자본 → 현금 전환 (within-firm cash conversion)

발생주의 매출이 현금으로 전환되는 데는 운전자본 사이클만큼의 시차가 있다.

**정의 3 (운전자본 사이클, 일수).**
$$\text{DIO}=\frac{\overline{\text{Inv}}}{\text{COGS}}\cdot d,\quad
\text{DSO}=\frac{\overline{\text{AR}}}{\text{Rev}}\cdot d,\quad
\text{DPO}=\frac{\overline{\text{AP}}}{\text{Purch}}\cdot d,\quad d=91.25$$
$$\boxed{\text{CCC}=\text{DIO}+\text{DSO}-\text{DPO}}$$
($\overline{X}=(X_t+X_{t-1})/2$ 평균잔액.)

**정의 4 (매출채권 동학).** $\text{AR}_t=\text{AR}_{t-1}+\text{Rev}_t-\text{Collect}_t$.
평균 회수기간이 DSO이므로 현금회수 $\text{Collect}_t$는 매출을 약 $\text{DSO}/d$ 분기 후행한다.

**정의 5 (영업현금흐름 항등식).**
$$\text{OCF}_t = \text{NI}_t + \text{D\&A}_t - \Delta\text{NWC}_t,\qquad
\Delta\text{NWC}_t=\Delta\text{Inv}_t+\Delta\text{AR}_t-\Delta\text{AP}_t$$
$$\text{FCF}_t=\text{OCF}_t-\text{Capex}_t$$
매출 급증기에는 $\Delta\text{AR}>0$로 $\Delta\text{NWC}>0$가 되어 **OCF가 매출을 후행**한다
(성장의 현금 흡수). 이것이 DSO·CCC가 OCF/FCF를 음(−)의 방향으로 선행하는 회계적 근거다.

---

## 3. 현금의 기업간 전이 (cross-firm cash transfer)

정의 2에 의해, 고객의 현금 유출(매입채무 결제)은 곧 공급사의 현금 유입(매출채권 회수)이다.
$$\text{CashPaid}^{(C\to S)}_{C,t+\text{DPO}_C/d}\;=\;\text{CashCollected}^{(C\to S)}_{S,t+\text{DSO}_S/d}$$
같은 거래라면 이상적으로 $\text{DPO}_C=\text{DSO}_S$이나, 협상력 차이로 벌어질 수 있다(공급망 금융의
지표). 따라서 **고객 DPO 상승은 공급사 DSO 상승을 선행**한다(지급지연의 회수지연 전이).

---

## 4. 검증가능 Lead-Lag 가설 (P1–P5)

위 항등식에서 다음의 방향·시차·기대부호가 **연역적으로** 도출된다. 이것이 실증(산출물 a)과
VECM 제약(산출물 b)의 대상이다.

| # | 관계 | 경로 (from → to) | 회계 근거 | 예상 시차 | 장기탄력성/부호 |
|---|---|---|---|---|---|
| **P1** | 기업간 | $\text{Purch}_C$(≈COGS) → $\text{Rev}_S$ | 정의 1 거래 항등식 | 0–1q | $\theta\approx\omega$ (+) |
| **P2** | 기업내 | $\text{Rev}_S$ → $\text{AR}_S$ | 정의 4 | 0q | $\approx 1$ (+) |
| **P3** | 기업내 | $\text{Rev}_S$ → $\text{OCF}_S$ | 정의 5 (ΔNWC) | +DSO/d q | (+), 단 성장기 지연 |
| **P4** | 기업간 | $\text{Rev}_C$ → $\text{Purch}_C$ → $\text{Rev}_S$ | 수요→매입→매출 2단계 | 0–2q | (+) |
| **P5** | 기업간 | $\text{AP}_C$ → $\text{AR}_S$ | 정의 2 거울 항등식 | 0–1q | (+), mirror |
| **P6** | 기업간 | $\text{DPO}_C$ → $\text{DSO}_S$ | §3 현금전이 | 0–2q | (+) |
| **P7** | 기업내 | $\text{CCC}_S$ → $\text{FCF}_S$ | 정의 3·5 | 0–1q | (−) |

**핵심 논리 체인 (돈의 흐름):**
$$\underbrace{\text{Rev}_C}_{\text{고객 수요}}\xrightarrow{\text{P4}}\underbrace{\text{Purch}_C}_{\text{구매}}
\xrightarrow{\text{P1}}\underbrace{\text{Rev}_S}_{\text{공급사 매출}}\xrightarrow{\text{P2}}\underbrace{\text{AR}_S}_{\text{외상}}
\xrightarrow{\text{P3}}\underbrace{\text{OCF}_S}_{\text{현금}}\xrightarrow{}\underbrace{\text{FCF}_S}_{\text{잉여현금}}$$
그리고 결제측 거울 흐름: $\text{AP}_C \xleftrightarrow{\text{P5}} \text{AR}_S$, $\text{DPO}_C \xrightarrow{\text{P6}} \text{DSO}_S$.

---

## 5. VECM 공적분 제약으로의 연결

정의 1·4는 **로그-레벨 장기균형(공적분)**을 함의한다. 공급사 $S$에 대해:
$$\log\text{Rev}_{S,t} = c_S + \sum_{C:\,C\to S}\theta_{S,C}\log\text{Rev}_{C,t} + u_{S,t}
\qquad(\theta_{S,C}\ \text{는 수요 pass-through}, \ u_S\ \text{정상})$$
$$\log\text{AR}_{S,t} = \log\text{Rev}_{S,t} + \log(\text{DSO}_S/d) + \varepsilon \quad(\text{정의 4})$$
오차수정항 $u_{S,t}$가 정상(공적분)이면, 단기 VECM은
$$\Delta\log\text{Rev}_{S,t} = \alpha_S\,u_{S,t-1} + \sum_C\beta_{S,C}\,\Delta\log\text{Rev}_{C,t} + \eta_t,\quad \alpha_S<0$$
$\alpha_S<0$(오차수정)은 매출이 장기균형으로 복원됨을 뜻한다. 이 구조를 전 공급사에 연립한 것이
**VECM global model**(산출물 b)이며, 충격 $\eta$의 전파가 시뮬레이션(산출물 c)이다.

---

## 6. 측정·식별 한계 (논문 §한계)

1. **거래처별 분해 부재**: $\omega_{C\to S}$·거래별 AR/AP는 공시에 없어 집계 근사·상관가중으로 추정.
2. **표본**: 분기 ~40개 + 2020–26 AI붐 구조변화 → 공적분 검정력 낮음. θ 유의성+α 부호로 판단.
3. **상관≠거래**: lead-lag는 통계적 선행. 실제 거래는 10-K 고객집중도/SPLC로 교차확인.
4. **데이터 커버리지**: Foundry(TSMC)·ODM(대만)은 분기 이력 부족 → 시스템에서 제외(데이터 축적 시 편입).
5. **회계 정책 차이**: 수익인식 기준(ASC 606)·재고평가 차이는 기업간 항등식에 잡음을 준다.

*이 이론이 산출물 a(실증 lead-lag), b(VECM formula), c(시뮬레이션)의 공통 기반이다.*
