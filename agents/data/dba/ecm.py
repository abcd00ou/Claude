"""
ecm.py — Error-Correction (long-run + short-run elasticity) engine for the
AI-supply-chain "mini-GEM". Guide-style ECM applied to value-chain relationships.

For a customer→supplier edge we model the SUPPLIER's revenue as error-correcting
toward a long-run equilibrium with the CUSTOMER's activity (revenue / capex / cogs):

  1) 장기 (Engle-Granger 1단계, log-level + 계절더미):
        log(Y_t) = c + θ·log(X_t) + Σ δ_q·Qdum + u_t
     θ = long-run elasticity;  u_t = 균형편차(disequilibrium).
  2) 공적분: ADF(u_t) — λ가 의미 있으려면 u_t가 정상이어야 함.
  3) 단기 (ECM 2단계):
        Δlog(Y_t) = α + β·Δlog(X_t) + λ·u_{t-1} + ε_t
     β = 즉각 전달(단기 탄력성);  λ∈(-2,0) = 조정속도;  반감기 = ln0.5/ln(1+λ).

Scenario: a permanent +s% shock to X propagates to Y with long-run θ·s% and a
transition path governed by λ (recursive simulation of the ECM).

Pure numpy (no statsmodels). Reads panel_long via panel.py; reuses value-chain
relationships from valuechain.py. Small-sample (≈40 q) caveats are surfaced, not hidden.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import panel as P
import valuechain as V

# Engle-Granger residual ADF critical values (2 vars, constant; MacKinnon approx)
EG_CRIT = {"1%": -3.90, "5%": -3.34, "10%": -3.04}
_MONTH_Q = {1: "Q1", 2: "Q2", 3: "Q3", 4: "Q4"}


# --------------------------------------------------------------------------- #
def _ols(X, y):
    """OLS with classic SEs. X includes its own intercept column if wanted."""
    X = np.asarray(X, float); y = np.asarray(y, float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    n, k = X.shape
    dof = max(n - k, 1)
    s2 = float(resid @ resid) / dof
    xtx_inv = np.linalg.pinv(X.T @ X)
    se = np.sqrt(np.diag(s2 * xtx_inv))
    t = np.divide(beta, se, out=np.zeros_like(beta), where=se > 0)
    sst = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - float(resid @ resid) / sst if sst > 0 else np.nan
    return dict(beta=beta, se=se, t=t, resid=resid, r2=r2, n=n, dof=dof)


def _season_dummies(index):
    """Q2/Q3/Q4 dummies from 'YYYY-QN' index (Q1 = baseline)."""
    q = pd.Series(index, index=index).map(lambda s: int(s.split("-Q")[1]))
    return np.column_stack([(q == 2).astype(float), (q == 3).astype(float),
                            (q == 4).astype(float)])


def adf_resid(u, max_lag=1):
    """
    ADF on a regression residual (no constant/trend): Δu = ρ·u_{t-1} + Σφ Δu_{t-i} + e.
    Returns (adf_t, rho, used_lag, verdict). Small samples => low power; reported as-is.
    """
    u = pd.Series(u).dropna().reset_index(drop=True)
    du = u.diff()
    best = None
    for L in range(max_lag, -1, -1):
        rows = pd.DataFrame({"du": du, "u_l": u.shift(1)})
        for i in range(1, L + 1):
            rows[f"du_l{i}"] = du.shift(i)
        rows = rows.dropna()
        if len(rows) < 6 + L:
            continue
        y = rows["du"].to_numpy()
        X = rows.drop(columns="du").to_numpy()
        res = _ols(X, y)
        adf_t = res["t"][0]
        best = (adf_t, float(res["beta"][0]), L)
        break
    if best is None:
        return dict(adf_t=np.nan, rho=np.nan, lag=None, cointegrated=None)
    adf_t, rho, L = best
    coint = adf_t < EG_CRIT["10%"]
    return dict(adf_t=round(adf_t, 3), rho=round(rho, 3), lag=L, cointegrated=bool(coint),
                crit=EG_CRIT)


# --------------------------------------------------------------------------- #
def section_level(long, section, item, min_q=16, log=True):
    """섹션 집계 레벨 시리즈: 구성사 item 합(capex는 abs), 필요시 log."""
    d = long[long.section == section]
    members = []
    ser = {}
    for tk in d.ticker.unique():
        s = P.get_series(long, tk, item)
        if item == "capex":
            s = s.abs()
        if s.dropna().shape[0] >= min_q:
            ser[tk] = s; members.append(tk)
    if not ser:
        return None, []
    agg = pd.DataFrame(ser).sum(axis=1, min_count=1).dropna()
    agg = agg[agg > 0] if log else agg
    agg = agg.loc[sorted(agg.index, key=P.qkey)]
    out = np.log(agg) if log else agg
    return out, members


def estimate_ecm(y, x):
    """
    Full Engle-Granger 2-step ECM on aligned log-level series y (supplier), x (customer).
    Returns long-run θ, cointegration test, short-run β, adjustment λ, half-life.
    """
    df = pd.concat({"y": y, "x": x}, axis=1).dropna()
    if len(df) < 12:
        return dict(status="insufficient data", n=len(df))
    idx = df.index
    # --- 1단계: 장기 (log-level + 계절더미) ---
    Xl = np.column_stack([np.ones(len(df)), df["x"].to_numpy(), _season_dummies(idx)])
    lr = _ols(Xl, df["y"].to_numpy())
    theta = float(lr["beta"][1]); theta_t = float(lr["t"][1])
    u = pd.Series(lr["resid"], index=idx)                      # 균형편차
    coint = adf_resid(u.to_numpy())

    # --- 2단계: 단기 ECM ---
    dY = df["y"].diff(); dX = df["x"].diff(); ec = u.shift(1)
    e = pd.concat({"dY": dY, "dX": dX, "ec": ec}, axis=1).dropna()
    if len(e) < 8:
        return dict(status="short-run insufficient", n=len(df), theta=round(theta, 3))
    Xs = np.column_stack([np.ones(len(e)), e["dX"].to_numpy(), e["ec"].to_numpy()])
    sr = _ols(Xs, e["dY"].to_numpy())
    beta_sr = float(sr["beta"][1]); beta_t = float(sr["t"][1])
    lam = float(sr["beta"][2]); lam_t = float(sr["t"][2])
    half = np.log(0.5) / np.log(1 + lam) if -2 < lam < 0 else np.nan

    valid_ec = (lam < 0) and (lam_t < -1.6)                    # 음수·유의 조정
    return dict(status="ok", n=len(df),
                long_run_elasticity=round(theta, 3), theta_t=round(theta_t, 2),
                cointegrated=coint["cointegrated"], adf_t=coint["adf_t"],
                short_run_beta=round(beta_sr, 3), beta_t=round(beta_t, 2),
                adjustment_lambda=round(lam, 3), lambda_t=round(lam_t, 2),
                half_life_q=round(half, 2) if not np.isnan(half) else None,
                error_correcting=bool(valid_ec), lr_r2=round(lr["r2"], 3),
                sr_r2=round(sr["r2"], 3), _resid=u, _short=e, _lr_beta=lr["beta"])


# --------------------------------------------------------------------------- #
def estimate_edge(long, cust, supp, x_item="revenue", y_item="revenue"):
    """One customer→supplier ECM (supplier Y error-corrects toward customer X)."""
    base = dict(customer=V.SECTIONS.get(cust, cust), supplier=V.SECTIONS.get(supp, supp),
                x_item=x_item, y_item=y_item)
    x, mx = section_level(long, cust, x_item)
    y, my = section_level(long, supp, y_item)
    if x is None or y is None:
        miss = cust if x is None else supp
        return {**base, "status": "insufficient data",
                "note": f"{V.SECTIONS.get(miss,miss)} 데이터 부족"}
    r = estimate_ecm(y, x)
    return {**base, **r}


def run_ecm(long, relationships=None, x_item="revenue", y_item="revenue"):
    relationships = relationships or V.RELATIONSHIPS
    rows = [estimate_edge(long, c, s, x_item, y_item) for c, s in relationships]
    cols = ["customer", "supplier", "x_item", "y_item", "status", "n",
            "long_run_elasticity", "theta_t", "cointegrated", "adf_t",
            "short_run_beta", "beta_t", "adjustment_lambda", "lambda_t",
            "half_life_q", "error_correcting", "lr_r2", "sr_r2"]
    df = pd.DataFrame(rows)
    return df[[c for c in cols if c in df.columns]]


# --------------------------------------------------------------------------- #
def generate_md(long, path, date="2026-07-06"):
    """ECM 리포트: revenue/capex 드라이버 장·단기 탄력성 + 시나리오 + 해석 여백."""
    from pathlib import Path
    L = ["# AI 공급망 ECM (장·단기 탄력성) — 미니 GEM 리포트\n",
         f"**분석일:** {date} · **데이터:** `panel_long` · **엔진:** `ecm.py` "
         "(Engle-Granger 2단계, numpy)\n",
         "**모형:** 공급사 매출 Y가 고객 활동 X에 오차수정. "
         "θ=장기탄력성, λ=조정속도(<0·유의해야 오차수정), 반감기=ln0.5/ln(1+λ).\n"]
    for xi, lab in [("revenue", "고객 매출"), ("capex", "고객 capex")]:
        df = run_ecm(long, x_item=xi, y_item="revenue")
        ok = df[df.status == "ok"]
        ec = ok[ok.error_correcting == True]
        L.append(f"\n## 드라이버: X = {lab}  (`{xi}` → 공급사 `revenue`)\n")
        L.append(f"- 분석가능 {len(ok)}/{len(df)} · 공적분검출 {(ok.cointegrated==True).sum()} · "
                 f"**오차수정(λ<0·유의) {len(ec)}건**\n")
        L.append("| 고객 | 공급사 | 장기θ | θ_t | λ(조정) | λ_t | 반감기(분기) | 오차수정 | n |")
        L.append("|---|---|---|---|---|---|---|---|---|")
        for _, r in ok.iterrows():
            star = "**" if r.error_correcting else ""
            hl = r.half_life_q if pd.notna(r.half_life_q) else "—"
            L.append(f"| {r.customer} | {r.supplier} | {star}{r.long_run_elasticity}{star} | "
                     f"{r.theta_t} | {r.adjustment_lambda} | {r.lambda_t} | {hl} | "
                     f"{'✅' if r.error_correcting else '·'} | {int(r.n)} |")
    L += ["\n## 시나리오 해석 예시\n",
          "고객 활동 영구 +10% 충격 시 공급사 매출은 장기적으로 θ×10% 로 수렴하며, "
          "속도는 λ가 결정합니다. (노트북 Step 4에서 `scenario_irf`로 곡선 확인)\n",
          "\n## 해석 메모 (직접 작성)\n> \n- \n- \n",
          "\n## 방법·한계\n",
          "- **표본 ≈40분기 + 2020~26 AI붐 구조변화** → 정식 공적분(ADF) 검출력은 낮음. "
          "θ 유의성과 λ 부호·유의를 함께 보고 신뢰도를 판단.\n",
          "- 섹션 매출/capex 합의 log-level + 계절더미. Foundry·ODM은 데이터 부족.\n",
          "- Engle-Granger 2단계(단일 공적분 가정). 다중 공적분/약외생성은 향후 Johansen·VECM로 확장.\n",
          "- 상관·오차수정은 통계적 관계 → 밸류체인 사전지식과 함께 해석.\n"]
    Path(path).write_text("\n".join(L))
    return path


def plot_ecm(long, cust, supp, x_item="revenue", y_item="revenue",
             shock_pct=10.0, horizon=8, figsize=(13, 4.5)):
    """Inline 2-panel: (1) 균형편차 u_t (오차수정 대상), (2) 시나리오 IRF."""
    import matplotlib.pyplot as plt
    r = estimate_edge(long, cust, supp, x_item, y_item)
    fig, ax = plt.subplots(1, 2, figsize=figsize)
    cl, sl = V.SECTIONS.get(cust, cust), V.SECTIONS.get(supp, supp)
    if r.get("status") != "ok":
        fig.suptitle(f"{cl}→{sl}: {r.get('status')}"); return fig
    fig.suptitle(f"ECM  {cl}·{x_item} → {sl}·revenue   |   "
                 f"장기θ={r['long_run_elasticity']} (t={r['theta_t']}), "
                 f"λ={r['adjustment_lambda']} (t={r['lambda_t']}), "
                 f"오차수정={'✅' if r['error_correcting'] else '·'}",
                 fontsize=10.5, fontweight="bold")
    u = r["_resid"]
    ax[0].plot(u.index, u.values, "-o", ms=3, color="#6a3d9a")
    ax[0].axhline(0, color="grey", lw=.8)
    ax[0].set_title("(1) 균형편차 uₜ (0으로 회귀 = 오차수정)"); ax[0].set_ylabel("log 편차")
    [l.set_visible(i % 3 == 0) for i, l in enumerate(ax[0].get_xticklabels())]
    ax[0].tick_params(axis="x", rotation=90, labelsize=7)
    irf = scenario_irf(r, shock_pct, horizon)
    ax[1].plot(irf["quarter_ahead"], irf["Y_response_pct"], "-o", color="#2ca02c")
    ax[1].axhline(r["long_run_elasticity"] * shock_pct, color="#d62728", ls="--",
                  label=f"장기 {r['long_run_elasticity']*shock_pct:.1f}%")
    ax[1].set_title(f"(2) 시나리오: {cl} {x_item} 영구 +{shock_pct:.0f}% → {sl} 매출 반응")
    ax[1].set_xlabel("분기 후"); ax[1].set_ylabel("Y 반응 %"); ax[1].legend(fontsize=8)
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    return fig


def scenario_irf(ecm_result, shock_pct=10.0, horizon=8):
    """
    Permanent +shock_pct% shock to X: simulate supplier Y's % response path via the
    ECM. Long-run response → θ·shock_pct%; transition governed by λ.
    Returns DataFrame(quarter_ahead, Y_response_pct).
    """
    if ecm_result.get("status") != "ok":
        return pd.DataFrame()
    theta = ecm_result["long_run_elasticity"]
    beta = ecm_result["short_run_beta"]
    lam = ecm_result["adjustment_lambda"]
    dx = np.log1p(shock_pct / 100.0)          # permanent log change in X at h=0
    # y,x in logs; start at equilibrium (level 0). x jumps by dx at h>=1 (permanent).
    y = 0.0; x_prev = 0.0; x = 0.0
    path = [(0, 0.0)]
    lr_const = 0.0  # equilibrium: y* = theta * x
    for h in range(1, horizon + 1):
        x = dx                                # permanent shock level
        dX = x - x_prev
        ec = y - (lr_const + theta * x_prev)  # last-period disequilibrium
        dY = beta * dX + lam * ec
        y = y + dY
        path.append((h, (np.expm1(y)) * 100.0))
        x_prev = x
    return pd.DataFrame(path, columns=["quarter_ahead", "Y_response_pct"]).round(3)
