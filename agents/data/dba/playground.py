"""
playground.py — panel_long_dataset.xlsx 기반 자립형(self-contained) Lead-Lag Playground 엔진
================================================================================================

이 파일 하나 + `panel_long_dataset.xlsx` 하나면 모든 분석이 돌아갑니다.
(다른 프로젝트 모듈 import 없음 — 표준 라이브러리 + pandas/numpy/matplotlib 만 사용)

■ 데이터 (분석의 시작점)
  `panel_long_dataset.xlsx` 의 `panel_long` 시트. 롱포맷(long format):
      ticker · companyname · date · item · value · section · quarter
  - 한 행 = "어떤 기업(ticker)의 / 어떤 분기(date·quarter)에 / 어떤 회계지표(item)가 / 얼마(value)"
  - item 에는 원천지표(revenue, inventory, accounts_payable, ...)와
    파생지표(DIO, DSO, DPO, CCC, OCF_MARGIN, REVENUE_GROWTH_YOY, ...)가 이미 다 들어있음.
    → 파생을 새로 계산할 필요 없이 item 이름으로 바로 조회하면 됩니다.

■ 이 엔진이 제공하는 것 (아래 함수들)
  1) 로드/조회 : load_panel · list_items · list_companies · get_series
  2) 변환      : transform  (level / QoQ / YoY / rolling / change / z-score)
  3) 통계      : lagged_xcorr(시차상관) · corr_pvalue · spearman · lead_lag(종합 검정)
  4) 시각화    : plot_series · plot_pair (시계열 + 시차상관 2패널)

■ 용어
  - lead-lag(선후행): 변수 X 가 변수 Y 보다 k분기 "앞서" 움직이면 "X 가 Y 를 k분기 선행(lead)".
  - 시차상관(cross-correlation): X(t) 와 Y(t+k) 의 상관을 여러 k 에 대해 계산한 것.
    가장 강한 상관을 주는 k* 가 "추정 시차".

사용 예:
  >>> import playground as pg
  >>> long = pg.load_panel()                              # 데이터 로드
  >>> r = pg.lead_lag(long, "NVDA", "revenue", "MU", "revenue")   # NVDA매출 → MU매출
  >>> print(r["verdict"]); pg.plot_pair(long, "NVDA","revenue","MU","revenue")
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 이 파일과 같은 폴더의 xlsx 를 기본 데이터로 사용
XLSX_DEFAULT = Path(__file__).parent / "panel_long_dataset.xlsx"


# ============================================================================ #
# 1. 데이터 로드 / 조회
# ============================================================================ #
def load_panel(xlsx: str | Path = XLSX_DEFAULT, sheet: str = "panel_long") -> pd.DataFrame:
    """
    엑셀(panel_long 시트)을 롱포맷 DataFrame 으로 읽어온다. 모든 분석의 출발점.

    Parameters
    ----------
    xlsx : 엑셀 파일 경로 (기본: 같은 폴더의 panel_long_dataset.xlsx)
    sheet: 시트 이름 (기본: 'panel_long')

    Returns
    -------
    DataFrame[ticker, companyname, date, item, value, section, quarter]
        quarter('YYYY-QN') 컬럼이 없으면 date 로부터 자동 생성한다.
    """
    df = pd.read_excel(xlsx, sheet_name=sheet)
    df["ticker"] = df["ticker"].astype(str)
    # quarter 컬럼 보정: 정규화된 분기말 date('YYYY-MM-DD') → 'YYYY-QN'
    if "quarter" not in df.columns:
        m2q = {3: 1, 6: 2, 9: 3, 12: 4}          # 분기말 월 → 분기번호
        df["quarter"] = df["date"].astype(str).str.slice(0, 10).apply(
            lambda d: f"{d[:4]}-Q{m2q[int(d[5:7])]}")
    return df


def qkey(q: str) -> int:
    """분기 문자열 'YYYY-QN' 을 정렬용 정수로. 예: '2024-Q3' → 2024*4+3."""
    y, n = q.split("-Q")
    return int(y) * 4 + int(n)


def list_items(long: pd.DataFrame) -> pd.DataFrame:
    """사용 가능한 지표(item) 목록과 각 지표의 데이터 행 수(=커버리지)를 반환."""
    g = long.groupby("item")["value"].size().sort_values(ascending=False)
    return g.rename("rows").reset_index()


def list_companies(long: pd.DataFrame, section: str | None = None) -> pd.DataFrame:
    """
    기업 목록(ticker·회사명·섹션·매출 분기수)을 반환. section 을 주면 그 섹터만 필터.
    revenue_quarters 는 데이터 충분성(분석 가능 여부)을 가늠하는 지표.
    """
    d = long if section is None else long[long["section"] == section]
    rev = (d[d["item"] == "revenue"].groupby("ticker")["quarter"].nunique()
           .rename("revenue_quarters"))
    meta = d.drop_duplicates("ticker").set_index("ticker")[["companyname", "section"]]
    out = meta.join(rev).reset_index().fillna({"revenue_quarters": 0})
    out["revenue_quarters"] = out["revenue_quarters"].astype(int)
    return out.sort_values(["section", "revenue_quarters"], ascending=[True, False])


def get_series(long: pd.DataFrame, ticker: str, item: str) -> pd.Series:
    """
    한 기업(ticker)의 한 지표(item)를 '분기 인덱스 시계열'로 뽑는다.

    Returns
    -------
    pd.Series (index='YYYY-QN', 오름차순 정렬, 중복분기 제거)
        해당 조합이 없으면 빈 시리즈.
    """
    d = long[(long["ticker"] == ticker) & (long["item"] == item)]
    if d.empty:
        return pd.Series(dtype=float, name=f"{ticker}:{item}")
    s = (d.drop_duplicates("quarter")
           .sort_values("quarter", key=lambda x: x.map(qkey))
           .set_index("quarter")["value"])
    s.name = f"{ticker}:{item}"
    return s


# ============================================================================ #
# 2. 변환 (해석가능한 파생 변환)
# ============================================================================ #
def transform(s: pd.Series, how: str = "level", winsor: tuple | None = None) -> pd.Series:
    """
    시계열에 변환을 적용한다. 지표 특성에 맞는 변환을 골라 쓴다.

    how 종류
    --------
    'level'        원값 그대로.
    'qoq'          전분기 대비 증감률  s/s.shift(1)-1        (단기 모멘텀)
    'yoy'          전년동기 대비 증감률 s/s.shift(4)-1       (계절성 제거)
    'change_qoq'   전분기 대비 차이     s - s.shift(1)       (일수·비율 변수에 적합)
    'change_yoy'   전년동기 대비 차이   s - s.shift(4)
    'rolling_qoq'  4분기 이동평균의 QoQ (노이즈 제거된 단기)
    'rolling_yoy'  4분기 이동평균의 YoY (노이즈 제거된 구조적 성장)  ← 가장 안정적
    'zscore'       표준화 (x-평균)/표준편차                  (기업간 스케일 통일)

    winsor : (lo, hi) 분위수로 극단치 clip (예: (0.02,0.98)). 비율 지표의 튐 방지.
    """
    s = s.astype(float)
    if winsor:
        s = s.clip(s.quantile(winsor[0]), s.quantile(winsor[1]))
    if how == "level":
        return s
    if how == "qoq":
        return s / s.shift(1) - 1
    if how == "yoy":
        return s / s.shift(4) - 1
    if how == "change_qoq":
        return s - s.shift(1)
    if how == "change_yoy":
        return s - s.shift(4)
    if how == "rolling_qoq":
        return s.rolling(4).mean() / s.rolling(4).mean().shift(1) - 1
    if how == "rolling_yoy":
        return s.rolling(4).mean() / s.rolling(4).mean().shift(4) - 1
    if how == "zscore":
        sd = s.std(ddof=0)
        return (s - s.mean()) / sd if sd else s * 0.0
    raise ValueError(f"알 수 없는 변환 how={how!r}")


# ============================================================================ #
# 3. 통계 (시차상관 · 유의성 · 종합 lead-lag 검정)
# ============================================================================ #
def _align(a: pd.Series, b: pd.Series):
    """두 시계열을 공통 분기에서만 정렬해 (a값, b값) numpy 배열로 반환."""
    d = pd.concat([a, b], axis=1).dropna()
    return d.iloc[:, 0].to_numpy(), d.iloc[:, 1].to_numpy()


def corr_pvalue(r: float, n: int) -> float:
    """
    Pearson 상관계수 r 의 양측 p-value (t-검정).
    t = r*sqrt(n-2)/sqrt(1-r^2) 가 자유도 n-2 의 t분포를 따른다는 사실을 이용.
    scipy 없이 t분포 생존함수를 정규근사로 계산(표본 충분하면 충분히 정확).
    """
    if n < 4 or abs(r) >= 1:
        return np.nan
    t = abs(r) * np.sqrt((n - 2) / (1 - r * r))
    # t(df) 의 양측 p 를 표준정규 근사 + 소표본 보정(자유도 반영)로 계산
    df = n - 2
    # Fisher 근사보다 안정적인 정규 근사: t → z 변환 (Wilson–Hilferty 유사)
    z = t * (1 - 1 / (4 * df)) / np.sqrt(1 + t * t / (2 * df))
    # 표준정규 양측 p = 2*(1-Φ(z)), Φ 는 erf 로 계산
    from math import erf, sqrt
    p = 2 * (1 - 0.5 * (1 + erf(z / sqrt(2))))
    return float(min(max(p, 0.0), 1.0))


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    """Spearman 순위상관 (비선형·단조 관계 확인용). 값을 순위로 바꾼 Pearson."""
    ar = pd.Series(a).rank().to_numpy()
    br = pd.Series(b).rank().to_numpy()
    if np.std(ar) == 0 or np.std(br) == 0:
        return np.nan
    return float(np.corrcoef(ar, br)[0, 1])


def lagged_xcorr(x: pd.Series, y: pd.Series, max_lag: int = 4,
                 min_overlap: int = 6) -> pd.DataFrame:
    """
    시차상관 함수(CCF): k = 0,1,...,max_lag 에 대해 corr( X(t), Y(t+k) ) 를 계산.

    - k>0 이고 상관이 크면 "X 가 Y 를 k분기 선행".
    - k=0 이면 동시(같은 분기) 동행.
    (여기서는 X→Y 방향, 즉 X 선행만 스캔한다. 반대 방향은 x,y 를 바꿔 호출.)

    Returns
    -------
    DataFrame[lag_k, pearson, spearman, p_value, n]
        각 시차별 상관·유의성. min_overlap 미만 겹침이면 그 시차는 제외.
    """
    rows = []
    for k in range(0, max_lag + 1):
        a, b = _align(x, y.shift(-k))       # X(t) 와 Y(t+k) 정렬
        n = len(a)
        if n >= min_overlap and np.std(a) > 0 and np.std(b) > 0:
            r = float(np.corrcoef(a, b)[0, 1])
            rows.append((k, r, spearman(a, b), corr_pvalue(r, n), n))
    return pd.DataFrame(rows, columns=["lag_k", "pearson", "spearman", "p_value", "n"])


def lead_lag(long: pd.DataFrame, x_ticker: str, x_item: str, y_ticker: str, y_item: str,
             x_tf: str = "yoy", y_tf: str = "yoy", max_lag: int = 4,
             expected: str = "+") -> dict:
    """
    ★ 핵심 함수 ★  두 (기업, 지표) 사이의 lead-lag 를 종합 검정한다.

    X = (x_ticker, x_item) 을 x_tf 로 변환한 시계열,
    Y = (y_ticker, y_item) 을 y_tf 로 변환한 시계열.
    시차상관을 스캔해 '가장 강한(부호가 expected 와 맞는) 시차'를 고르고,
    그 시차의 상관·Spearman·p값·표본수·유의여부를 정리해 돌려준다.

    Parameters
    ----------
    x_tf, y_tf : 변환 (transform 참고). 기본 'yoy'.
    expected   : 기대 부호 '+' 또는 '-'. 해당 부호의 상관 중 |상관| 최대인 시차를 선택.
                 (예: 매출→매출은 '+', CCC→FCF마진은 '-')

    Returns
    -------
    dict: {status, best_lag, pearson, spearman, p_value, n, significant, verdict, table, x, y}
        - best_lag>0 : X 가 Y 를 best_lag 분기 선행
        - significant: |상관|의 p<0.05 이고 부호가 expected 와 일치
        - table      : 전체 시차상관 DataFrame
    """
    x = transform(get_series(long, x_ticker, x_item), x_tf)
    y = transform(get_series(long, y_ticker, y_item), y_tf)
    tbl = lagged_xcorr(x, y, max_lag)
    xlab, ylab = f"{x_ticker}:{x_item}[{x_tf}]", f"{y_ticker}:{y_item}[{y_tf}]"
    if tbl.empty:
        return dict(status="insufficient data", x=xlab, y=ylab, table=tbl)

    # 기대부호와 일치하는 시차 중 |상관| 최대를 선택 (없으면 전체에서 |상관| 최대)
    cand = tbl[tbl["pearson"] > 0] if expected == "+" else \
        tbl[tbl["pearson"] < 0] if expected == "-" else tbl
    pick = (cand if not cand.empty else tbl).iloc[
        (cand if not cand.empty else tbl)["pearson"].abs().argmax()]

    lag = int(pick["lag_k"])
    r, p = float(pick["pearson"]), float(pick["p_value"])
    sig = (not np.isnan(p)) and p < 0.05 and (
        (expected == "+" and r > 0) or (expected == "-" and r < 0) or expected not in "+-")
    verdict = (f"{xlab} 가 {ylab} 를 {lag}분기 선행 "
               f"(r={r:.2f}, p={p:.3f}, {'유의' if sig else '비유의'})"
               if lag > 0 else
               f"{xlab} 와 {ylab} 는 동시 동행 (r={r:.2f}, {'유의' if sig else '비유의'})")
    return dict(status="ok", x=xlab, y=ylab, best_lag=lag, pearson=round(r, 3),
                spearman=round(float(pick["spearman"]), 3) if not np.isnan(pick["spearman"]) else None,
                p_value=round(p, 4) if not np.isnan(p) else None, n=int(pick["n"]),
                significant=bool(sig), verdict=verdict, table=tbl)


# ============================================================================ #
# 4. 시각화
# ============================================================================ #
def plot_series(long: pd.DataFrame, pairs: list[tuple[str, str]], tf: str = "level",
                figsize=(11, 3.5)):
    """
    여러 (기업, 지표)의 시계열을 한 그래프에 겹쳐 그린다.
    pairs 예: [("NVDA","revenue"), ("MU","revenue")]. tf 로 변환 적용.
    """
    fig, ax = plt.subplots(figsize=figsize)
    for tk, it in pairs:
        s = transform(get_series(long, tk, it), tf)
        ax.plot(s.index, s.values, "-o", ms=3, label=f"{tk}:{it}")
    ax.axhline(0, color="grey", lw=.6)
    ax.set_title(f"시계열 ({tf})"); ax.legend(fontsize=8)
    _thin_xticks(ax)
    return fig


def plot_pair(long: pd.DataFrame, x_ticker: str, x_item: str, y_ticker: str, y_item: str,
              x_tf: str = "yoy", y_tf: str = "yoy", max_lag: int = 4, expected: str = "+",
              figsize=(13, 4.5)):
    """
    두 변수의 lead-lag 를 2패널로 시각화:
      (1) 두 시계열 겹쳐 그리기
      (2) 시차상관 막대 (가장 강한 시차를 초록으로 강조)
    lead_lag() 결과의 판정(verdict)을 제목에 표시한다.
    """
    res = lead_lag(long, x_ticker, x_item, y_ticker, y_item, x_tf, y_tf, max_lag, expected)
    x = transform(get_series(long, x_ticker, x_item), x_tf)
    y = transform(get_series(long, y_ticker, y_item), y_tf)

    fig, ax = plt.subplots(1, 2, figsize=figsize)
    fig.suptitle(res.get("verdict", res["status"]), fontsize=11, fontweight="bold")
    # (1) 시계열
    ax[0].plot(x.index, x.values, "-o", ms=3, color="#1f77b4", label=f"X: {x_ticker}:{x_item}")
    ax[0].plot(y.index, y.values, "-o", ms=3, color="#d62728", label=f"Y: {y_ticker}:{y_item}")
    ax[0].axhline(0, color="grey", lw=.6); ax[0].legend(fontsize=8)
    ax[0].set_title(f"(1) 시계열  X[{x_tf}] · Y[{y_tf}]"); _thin_xticks(ax[0])
    # (2) 시차상관
    tbl = res.get("table")
    if tbl is not None and not tbl.empty:
        best = res.get("best_lag")
        colors = ["#2ca02c" if k == best else "#9ecae1" for k in tbl["lag_k"]]
        ax[1].bar(tbl["lag_k"], tbl["pearson"], color=colors)
        for _, r in tbl.iterrows():
            ax[1].text(r["lag_k"], r["pearson"] + (.02 if r["pearson"] >= 0 else -.06),
                       f"{r['pearson']:.2f}", ha="center", fontsize=8)
    ax[1].axhline(0, color="grey", lw=.6)
    ax[1].set_title("(2) 시차상관 (k>0 ⇒ X 선행)")
    ax[1].set_xlabel("시차 k (분기)"); ax[1].set_ylabel("Pearson r")
    fig.tight_layout(rect=[0, 0, 1, 0.92])
    return fig


def _thin_xticks(ax):
    """분기 라벨이 빽빽할 때 3개마다 하나만 보여 겹침을 막는다(내부 헬퍼)."""
    for i, lab in enumerate(ax.get_xticklabels()):
        if i % 3 != 0:
            lab.set_visible(False)
    ax.tick_params(axis="x", rotation=90, labelsize=7)
