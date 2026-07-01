"""
leadlag.py — Lead-Lag & Money-Flow Blockage analysis across the AI value chain.

Implements the methodology in agents/Scope_Document_LeadLag_EN.md against the REAL
panel in financials.db (company x item x quarter).

Real-data adaptations vs. the synthetic scope test (documented, not hidden):
  * DRAM node = Micron (MU): SK hynix / Samsung have only ~5 quarters (KRW, no
    receivables) in this DB, so they cannot carry a 24-quarter lead-lag.
  * No accounts_payable / cogs columns exist. COGS = revenue - gross_profit.
    CCC therefore reduces to the OPERATING CYCLE  OC = DIO + DSO  (DPO unavailable).
    This is stated in every CCC/congestion output.
  * Primary lead-lag signal = revenue YoY growth (universally populated). capex is
    only densely populated for MSFT/AMZN, so it is used as a demand-origin cross-check,
    not the backbone signal.

Only pandas + numpy are used (scipy/statsmodels are not installed in this env);
the Granger F-test and OLS are implemented directly with numpy.linalg.
"""

from __future__ import annotations
import numpy as np
import pandas as pd

QUARTER_DAYS = 91.25


# --------------------------------------------------------------------------- #
# Signal construction
# --------------------------------------------------------------------------- #
def yoy(series: pd.Series) -> pd.Series:
    """Year-over-year growth (t vs t-4 quarters). Kills seasonality + unit scale."""
    return series / series.shift(4) - 1.0


def zscore(series: pd.Series) -> pd.Series:
    s = series.dropna()
    if s.std(ddof=0) == 0 or len(s) < 2:
        return series * 0.0
    return (series - s.mean()) / s.std(ddof=0)


def _aligned(a: pd.Series, b: pd.Series):
    df = pd.concat([a, b], axis=1).dropna()
    return df.iloc[:, 0].to_numpy(), df.iloc[:, 1].to_numpy()


def _corr(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) < 3 or np.std(a) == 0 or np.std(b) == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


# --------------------------------------------------------------------------- #
# Pairwise lagged cross-correlation  (core of Output ③)
# --------------------------------------------------------------------------- #
def lagged_xcorr(leader: pd.Series, follower: pd.Series, max_lag: int = 4,
                 signed: bool = True, min_overlap: int = 8):
    """
    Scan lags k = -K..K. k>0 means `leader` leads `follower` by k quarters, i.e.
    corr( leader(t) , follower(t+k) ). Returns (best_lag, best_corr, table).

    For a demand value chain we want POSITIVE co-movement (a leader whose growth
    PRECEDES the follower's growth), so by default the peak is the strongest
    positive correlation, not the largest |corr| — this rejects anti-phase
    artifacts that otherwise dominate at the extreme +/-4q lags of short series.
    `min_overlap` drops lags with too few overlapping quarters to be trustworthy.
    """
    rows = []
    for k in range(-max_lag, max_lag + 1):
        # shift follower back by k so that leader(t) aligns with follower(t+k)
        a, b = _aligned(leader, follower.shift(-k))
        c = _corr(a, b) if len(a) >= min_overlap else np.nan
        rows.append((k, c, len(a)))
    tbl = pd.DataFrame(rows, columns=["lag", "corr", "n"])
    valid = tbl.dropna(subset=["corr"])
    if signed:
        valid = valid[valid["corr"] > 0]
    if valid.empty:
        return np.nan, np.nan, tbl
    key = valid["corr"] if signed else valid["corr"].abs()
    best = valid.loc[key.idxmax()]
    return int(best["lag"]), float(best["corr"]), tbl


def granger_p(leader: pd.Series, follower: pd.Series, lag: int = 1) -> float:
    """
    Minimal Granger causality F-test (leader -> follower) at a single lag.
    H0: past `leader` adds nothing beyond past `follower`. Lower p = more causal.
    numpy OLS; returns p-value (or nan if too few points).
    """
    df = pd.concat(
        {"y": follower, "y_l": follower.shift(lag), "x_l": leader.shift(lag)}, axis=1
    ).dropna()
    n = len(df)
    if n < 3 * (lag + 1) + 2:
        return np.nan
    y = df["y"].to_numpy()

    def ols_rss(X):
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X @ beta
        return float(resid @ resid)

    ones = np.ones((n, 1))
    X_r = np.hstack([ones, df[["y_l"]].to_numpy()])        # restricted
    X_u = np.hstack([ones, df[["y_l", "x_l"]].to_numpy()])  # unrestricted
    rss_r, rss_u = ols_rss(X_r), ols_rss(X_u)
    if rss_u <= 0 or rss_r <= rss_u:
        return 1.0
    q = 1                      # one restriction
    dfe = n - X_u.shape[1]
    F = ((rss_r - rss_u) / q) / (rss_u / dfe)
    # F(1, dfe) survival via incomplete beta (implemented w/o scipy)
    return _f_sf(F, q, dfe)


def _f_sf(F, d1, d2):
    """P(F_{d1,d2} > F) using the regularized incomplete beta function."""
    if F <= 0:
        return 1.0
    x = d2 / (d2 + d1 * F)
    return _betainc(d2 / 2.0, d1 / 2.0, x)


def _betainc(a, b, x):
    """Regularized incomplete beta I_x(a,b) via continued fraction (Numerical Recipes)."""
    from math import lgamma, exp, log
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = lgamma(a) + lgamma(b) - lgamma(a + b)
    front = exp(a * log(x) + b * log(1 - x) - lbeta) / a

    def cf():
        c, d = 1.0, 1.0 - (a + b) * x / (a + 1)
        d = 1e-30 if abs(d) < 1e-30 else d
        d = 1.0 / d
        h = d
        for m in range(1, 200):
            m2 = 2 * m
            num = m * (b - m) * x / ((a - 1 + m2) * (a + m2))
            d = 1 + num * d
            d = 1e-30 if abs(d) < 1e-30 else d
            c = 1 + num / c
            c = 1e-30 if abs(c) < 1e-30 else c
            d = 1.0 / d
            h *= d * c
            num = -(a + m) * (a + b + m) * x / ((a + m2) * (a + 1 + m2))
            d = 1 + num * d
            d = 1e-30 if abs(d) < 1e-30 else d
            c = 1 + num / c
            c = 1e-30 if abs(c) < 1e-30 else c
            d = 1.0 / d
            delta = d * c
            h *= delta
            if abs(delta - 1) < 1e-8:
                break
        return h

    if x < (a + 1) / (a + b + 2):
        return front * cf()
    # symmetry
    return 1.0 - _betainc_front(b, a, 1 - x)


def _betainc_front(a, b, x):
    from math import lgamma, exp, log
    lbeta = lgamma(a) + lgamma(b) - lgamma(a + b)
    front = exp(a * log(x) + b * log(1 - x) - lbeta) / a

    def cf():
        c, d = 1.0, 1.0 - (a + b) * x / (a + 1)
        d = 1e-30 if abs(d) < 1e-30 else d
        d = 1.0 / d
        h = d
        for m in range(1, 200):
            m2 = 2 * m
            num = m * (b - m) * x / ((a - 1 + m2) * (a + m2))
            d = 1 + num * d; d = 1e-30 if abs(d) < 1e-30 else d
            c = 1 + num / c; c = 1e-30 if abs(c) < 1e-30 else c
            d = 1.0 / d; h *= d * c
            num = -(a + m) * (a + b + m) * x / ((a + m2) * (a + 1 + m2))
            d = 1 + num * d; d = 1e-30 if abs(d) < 1e-30 else d
            c = 1 + num / c; c = 1e-30 if abs(c) < 1e-30 else c
            d = 1.0 / d; delta = d * c; h *= delta
            if abs(delta - 1) < 1e-8:
                break
        return h
    return front * cf()


# --------------------------------------------------------------------------- #
# Directional score + network  (Output ③)
# --------------------------------------------------------------------------- #
def pairwise_leadlag(name_i, sig_i, sec_i, name_j, sig_j, sec_j,
                     stage_gap=0.0, max_lag=4, corr_floor=0.35):
    """
    Combine lag sign, correlation strength, stage prior and Granger asymmetry into a
    single directed score. Returns dict describing leader->follower (or None if weak).
    """
    lag, corr, _ = lagged_xcorr(sig_i, sig_j, max_lag)
    if np.isnan(corr) or abs(corr) < corr_floor or lag == 0:
        return None
    # orient so that leader precedes follower
    if lag > 0:
        leader, follower = name_i, name_j
        lsec, fsec = sec_i, sec_j
        lead_q = lag
        g_fwd = granger_p(sig_i, sig_j, lag=min(lag, 2))
        g_rev = granger_p(sig_j, sig_i, lag=min(lag, 2))
    else:
        leader, follower = name_j, name_i
        lsec, fsec = sec_j, sec_i
        lead_q = -lag
        g_fwd = granger_p(sig_j, sig_i, lag=min(-lag, 2))
        g_rev = granger_p(sig_i, sig_j, lag=min(-lag, 2))

    granger_bonus = 0.0
    if not np.isnan(g_fwd) and not np.isnan(g_rev):
        if g_fwd < 0.10 and g_fwd < g_rev:
            granger_bonus = 0.15
    stage_bonus = 0.10 if stage_gap > 0 else 0.0
    score = abs(corr) + granger_bonus + stage_bonus
    return {
        "from_leader": leader, "to_follower": follower,
        "sector_from": lsec, "sector_to": fsec,
        "lead_quarters": float(lead_q), "peak_corr": round(corr, 3),
        "granger_p_fwd": None if np.isnan(g_fwd) else round(g_fwd, 3),
        "granger_p_rev": None if np.isnan(g_rev) else round(g_rev, 3),
        "score": round(score, 3),
    }


def build_leadlag_network(signals: dict, sectors: dict, stage: dict,
                          max_lag=4, corr_floor=0.35):
    """signals: {name: yoy series}. Returns edge DataFrame sorted by score."""
    names = list(signals)
    edges = []
    for i in range(len(names)):
        for j in range(i + 1, len(names)):
            a, b = names[i], names[j]
            e = pairwise_leadlag(
                a, signals[a], sectors[a], b, signals[b], sectors[b],
                stage_gap=stage.get(b, 0) - stage.get(a, 0),
                max_lag=max_lag, corr_floor=corr_floor,
            )
            if e:
                edges.append(e)
    cols = ["from_leader", "to_follower", "sector_from", "sector_to",
            "lead_quarters", "peak_corr", "granger_p_fwd", "granger_p_rev", "score"]
    return pd.DataFrame(edges, columns=cols).sort_values("score", ascending=False)


# --------------------------------------------------------------------------- #
# Sector phase order  (Output ②)
# --------------------------------------------------------------------------- #
def sector_phase_order(sector_signals: dict, max_lag=4):
    """
    sector_signals: {sector: yoy series}. phase_score = -mean_j(lead_ij * |corr|):
    a sector that consistently LEADS others gets a more-negative (upstream) score.
    """
    secs = list(sector_signals)
    acc = {s: [] for s in secs}
    for i in range(len(secs)):
        for j in range(i + 1, len(secs)):
            si, sj = secs[i], secs[j]
            lag, corr, _ = lagged_xcorr(sector_signals[si], sector_signals[sj], max_lag)
            if np.isnan(corr) or lag == 0:
                continue
            w = lag * abs(corr)         # >0 => si leads sj
            acc[si].append(-w)          # leading => upstream => negative
            acc[sj].append(+w)
    rows = []
    for s in secs:
        score = float(np.mean(acc[s])) if acc[s] else 0.0
        rows.append((s, round(score, 3)))
    df = pd.DataFrame(rows, columns=["section", "phase_score"]).sort_values("phase_score")
    df.insert(2, "rank", range(1, len(df) + 1))
    return df.reset_index(drop=True)


# --------------------------------------------------------------------------- #
# Working-capital congestion  (Output ④)  — operating cycle (no DPO in this DB)
# --------------------------------------------------------------------------- #
def working_capital_congestion(panel: pd.DataFrame, name: str):
    """
    panel indexed by quarter with columns revenue, cogs, inventory, receivables.
    Computes DIO, DSO and OC = DIO + DSO (DPO unavailable -> stated as caveat).
    Flags a quarter when YoY OC growth > 0.15 and (dDIO>0 or dDSO>0).
    """
    need = {"revenue", "cogs", "inventory", "receivables"}
    if not need.issubset(panel.columns) or panel[list(need)].dropna().shape[0] < 8:
        return {"company": name, "status": "insufficient data"}, pd.DataFrame()
    df = panel.copy()
    df["DIO"] = df["inventory"] / df["cogs"] * QUARTER_DAYS
    df["DSO"] = df["receivables"] / df["revenue"] * QUARTER_DAYS
    df["OC"] = df["DIO"] + df["DSO"]
    df["OC_yoy"] = yoy(df["OC"])
    df["DIO_yoy"] = yoy(df["DIO"])
    df["DSO_yoy"] = yoy(df["DSO"])
    df["flagged"] = (df["OC_yoy"] > 0.15) & ((df["DIO_yoy"] > 0) | (df["DSO_yoy"] > 0))
    last4 = df.tail(4)
    n_flag = int(last4["flagged"].sum())
    recent = df.dropna(subset=["OC_yoy"]).iloc[-1] if df["OC_yoy"].notna().any() else None
    if recent is None:
        return {"company": name, "status": "insufficient data"}, df
    driver = ("Inventory build-up (DIO)"
              if (recent["DIO_yoy"] or 0) >= (recent["DSO_yoy"] or 0)
              else "Receivables build-up (DSO)")
    status = "Congestion Warning" if n_flag >= 1 else "Healthy"
    summary = {
        "company": name, "status": status,
        "recent_OC_days": round(float(recent["OC"]), 1),
        "OC_yoy_recent": round(float(recent["OC_yoy"]), 3),
        "congested_Q_of_last4": n_flag,
        "driver": driver if status == "Congestion Warning" else "-",
        "internal_congestion": status == "Congestion Warning",
    }
    return summary, df


# --------------------------------------------------------------------------- #
# Transmission gap  (Output ⑤)
# --------------------------------------------------------------------------- #
def transmission_gap(up_sig: pd.Series, down_sig: pd.Series, lag: int,
                     up_name: str, down_name: str):
    """
    Fit down(t) = a + b*up(t-lag) + e; flag sustained undershoot (gap_z<-1).
    Stability guard: suspend if |corr|<0.2 or upstream variance ~0.
    """
    df = pd.concat({"down": down_sig, "up": up_sig.shift(lag)}, axis=1).dropna()
    if len(df) < 6:
        return {"upstream": up_name, "downstream": down_name,
                "status": "insufficient data"}
    up, down = df["up"].to_numpy(), df["down"].to_numpy()
    if np.std(up) < 1e-6 or abs(_corr(up, down)) < 0.2:
        return {"upstream": up_name, "downstream": down_name, "lag_q": lag,
                "status": "relationship unclear (guard)"}
    X = np.hstack([np.ones((len(up), 1)), up.reshape(-1, 1)])
    beta, *_ = np.linalg.lstsq(X, down, rcond=None)
    pred = X @ beta
    resid = down - pred
    sigma = resid.std(ddof=1) if len(resid) > 2 else resid.std()
    gap_z = resid / sigma if sigma > 0 else resid * 0
    df = df.assign(gap=resid, gap_z=gap_z)
    last4 = df.tail(4)
    blocked = int((last4["gap_z"] < -1.0).sum())
    status = "TRANSMISSION BREAK" if blocked >= 2 else "Normal transmission"
    return {
        "upstream": up_name, "downstream": down_name, "lag_q": lag,
        "transmission_beta": round(float(beta[1]), 3),
        "recent_gap_z": round(float(df["gap_z"].iloc[-1]), 2),
        "blocked_Q_of_last4": blocked,
        "status": status,
        "transmission_block": status == "TRANSMISSION BREAK",
    }


# --------------------------------------------------------------------------- #
# Integrated blockage matrix  (Output ⑥)
# --------------------------------------------------------------------------- #
def blockage_matrix(congestion: dict, transmission_as_down: dict):
    """Cross A (internal congestion) x B (transmission break) -> diagnosis/Rx."""
    A = bool(congestion.get("internal_congestion", False))
    B = bool(transmission_as_down.get("transmission_block", False)) if transmission_as_down else False
    if not A and not B:
        diag, rx = "Healthy", "-"
    elif A and not B:
        diag, rx = "Internal bottleneck", "Production / collection management"
    elif not A and B:
        diag, rx = "Transmission bottleneck", "Re-interpret upstream demand"
    else:
        diag, rx = "Compound bottleneck", "Demand-supply realignment"
    return {"company": congestion.get("company"),
            "internal_congestion_A": A, "transmission_block_B": B,
            "diagnosis": diag, "prescription": rx}
