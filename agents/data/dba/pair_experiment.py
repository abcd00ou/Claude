"""
pair_experiment.py — reusable lead-lag engine for the notebook.

One entry point:  leadlag_experiment(x_company, x_var, y_company, y_var, ...)
where X is the candidate LEADER and Y is the candidate FOLLOWER. X and Y can be
different companies, or the SAME company with two different variables (e.g. does
NVDA capex lead NVDA revenue?).

Returns a `Result` (dataclass) carrying every number, plus:
    .stats_table()  -> pandas DataFrame (the statistics summary)
    .ccf_table()    -> pandas DataFrame (full cross-correlation function)
    .plot()         -> matplotlib Figure (4 panels), inline-friendly

Design mirrors experiment_two_companies.py but is parameterised on (company, variable)
and does NOT force matplotlib's Agg backend, so it renders inline in Jupyter.
"""
from __future__ import annotations
from dataclasses import dataclass, field

import numpy as np
import pandas as pd

import leadlag as ll
import panel as P                       # <-- single data-access layer (panel_long)

DB_DEFAULT = P.DB_DEFAULT

# Human labels for the items in the long table (item name = what you pass in).
_LABELS = {
    "revenue": "Revenue", "revenue_ai_dc": "Revenue (AI/DC)", "revenue_yoy": "Revenue YoY %",
    "gross_profit": "Gross profit", "gross_margin": "Gross margin %", "cogs": "COGS",
    "operating_income": "Operating income", "net_income": "Net income", "eps": "EPS",
    "capex": "Capex", "fcf": "Free cash flow", "operating_cash_flow": "Operating cash flow",
    "inventory": "Inventory", "receivables": "Receivables", "cash": "Cash",
    "total_assets": "Total assets", "total_debt": "Total debt",
    "stockholders_equity": "Stockholders' equity", "stock_price": "Stock price",
}
AVAILABLE_VARS = {it: _LABELS.get(it, it) for it in P.AVAILABLE_ITEMS}


# --------------------------------------------------------------------------- #
def list_companies(db=DB_DEFAULT) -> pd.DataFrame:
    return P.companies(db).rename(columns={"section": "segments", "revenue_quarters": "quarters"})


def _corr_p(r, n):
    """Two-sided p-value for Pearson r via t-test (t^2 ~ F(1,n-2))."""
    if n < 4 or abs(r) >= 1:
        return np.nan
    t2 = (r * r) * (n - 2) / (1 - r * r)
    return ll._f_sf(t2, 1, n - 2)


# --------------------------------------------------------------------------- #
@dataclass
class Result:
    x_company: str; x_var: str; x_label: str
    y_company: str; y_var: str; y_label: str
    x_name: str; y_name: str
    transform: str
    sig_x: pd.Series; sig_y: pd.Series
    raw_x: pd.Series; raw_y: pd.Series
    ccf: pd.DataFrame
    best_k: int; best_r: float; best_p: float; contemp_r: float
    lead: int; up_name: str; down_name: str
    up_sig: pd.Series; down_sig: pd.Series
    granger_xy: float; granger_yx: float
    beta: float; intercept: float; r2: float; n_reg: int
    verdict: str
    _meta: dict = field(default_factory=dict)

    # ---- tables -----------------------------------------------------------
    def stats_table(self) -> pd.DataFrame:
        def fmt(v): return "—" if v is None or (isinstance(v, float) and np.isnan(v)) else v
        rows = [
            ("X (leader candidate)", f"{self.x_name} · {self.x_label}"),
            ("Y (follower candidate)", f"{self.y_name} · {self.y_label}"),
            ("transform", self.transform),
            ("overlapping quarters", int(self._meta.get("n_overlap0", 0))),
            ("contemporaneous corr (k=0)", round(self.contemp_r, 3)),
            ("best lag k*", self.best_k),
            ("lead statement", self.verdict.split(".")[0]),
            ("peak correlation r", round(self.best_r, 3)),
            ("peak corr p-value", round(self.best_p, 4)),
            (f"Granger X→Y p ({self.x_company}→{self.y_company})", round(self.granger_xy, 4) if not np.isnan(self.granger_xy) else None),
            (f"Granger Y→X p ({self.y_company}→{self.x_company})", round(self.granger_yx, 4) if not np.isnan(self.granger_yx) else None),
            ("transmission β", round(self.beta, 3) if not np.isnan(self.beta) else None),
            ("transmission R²", round(self.r2, 3) if not np.isnan(self.r2) else None),
            ("regression n", self.n_reg),
        ]
        return pd.DataFrame([(k, fmt(v)) for k, v in rows], columns=["statistic", "value"])

    def ccf_table(self) -> pd.DataFrame:
        t = self.ccf.copy()
        t["significant_5pct"] = t["p_value"] < 0.05
        return t

    # ---- figure -----------------------------------------------------------
    def plot(self, figsize=(14, 10)):
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle(
            f"Lead-Lag: X={self.x_name}·{self.x_label}   →   Y={self.y_name}·{self.y_label}\n"
            f"{self.verdict}", fontsize=12, fontweight="bold")

        # (1) signals over time
        a = ax[0, 0]
        a.plot(self.sig_x.index, self.sig_x.values, "-o", ms=3, color="#1f77b4",
               label=f"X: {self.x_name} {self.x_label}")
        a.plot(self.sig_y.index, self.sig_y.values, "-o", ms=3, color="#d62728",
               label=f"Y: {self.y_name} {self.y_label}")
        a.axhline(0, color="grey", lw=0.6); a.legend(fontsize=8)
        a.set_title(f"(1) Signals over time ({self.transform})"); a.set_ylabel("z-score")
        _thin(a)

        # (2) cross-correlation function
        b = ax[0, 1]
        cc = self.ccf
        colors = ["#2ca02c" if k == self.best_k else "#9ecae1" for k in cc["lag_k"]]
        b.bar(cc["lag_k"], cc["corr"], color=colors)
        b.axhline(0, color="grey", lw=0.6); b.axvline(self.best_k, color="#2ca02c", ls="--", lw=1)
        b.set_title(f"(2) Cross-correlation function (peak k={self.best_k}, r={self.best_r:.2f})")
        b.set_xlabel(f"lag k  (k>0 ⇒ X leads Y)"); b.set_ylabel("Pearson r")
        for _, r in cc.iterrows():
            if pd.notna(r["corr"]):
                b.text(r["lag_k"], r["corr"] + (0.02 if r["corr"] >= 0 else -0.06),
                       f"{r['corr']:.2f}", ha="center", fontsize=7)

        # (3) aligned overlay
        c = ax[1, 0]
        if self.lead != 0:
            sh = self.up_sig.shift(self.lead)
            c.plot(self.down_sig.index, self.down_sig.values, "-o", ms=3, color="#d62728",
                   label=f"{self.down_name} (follower)")
            c.plot(sh.index, sh.values, "-o", ms=3, color="#1f77b4",
                   label=f"{self.up_name} shifted +{self.lead}q")
            c.set_title(f"(3) Aligned after shifting leader by {self.lead}q")
        else:
            c.plot(self.sig_x.index, self.sig_x.values, "-o", ms=3, label="X")
            c.plot(self.sig_y.index, self.sig_y.values, "-o", ms=3, label="Y")
            c.set_title("(3) Contemporaneous overlay")
        c.axhline(0, color="grey", lw=0.6); c.legend(fontsize=8); c.set_ylabel("z-score"); _thin(c)

        # (4) transmission scatter
        d = ax[1, 1]
        reg = pd.concat({"down": self.down_sig, "up": self.up_sig.shift(self.lead)}, axis=1).dropna()
        if len(reg) >= 3 and not np.isnan(self.beta):
            d.scatter(reg["up"], reg["down"], color="#6a3d9a", s=28)
            xs = np.linspace(reg["up"].min(), reg["up"].max(), 50)
            d.plot(xs, self.intercept + self.beta * xs, "k--",
                   label=f"β={self.beta:.2f}, R²={self.r2:.2f}")
            d.legend(fontsize=8)
        d.set_title(f"(4) Transmission {self.up_name}(t−{self.lead}) → {self.down_name}(t)")
        d.set_xlabel(f"{self.up_name} (leader, lagged)"); d.set_ylabel(f"{self.down_name} (follower)")

        fig.tight_layout(rect=[0, 0, 1, 0.93])
        return fig


def _thin(ax_):
    for i, lab in enumerate(ax_.get_xticklabels()):
        if i % 3 != 0:
            lab.set_visible(False)
    ax_.tick_params(axis="x", rotation=90, labelsize=7)


# --------------------------------------------------------------------------- #
def leadlag_experiment(x_company, x_var="revenue",
                       y_company=None, y_var=None,
                       max_lag=4, transform="yoy_z", db=DB_DEFAULT) -> Result:
    """
    X = candidate leader (x_company, x_var); Y = candidate follower (y_company, y_var).
    Reads exclusively from the long table `panel_long` via panel.py.
    transform: 'yoy_z' (YoY growth, z-scored — default, kills seasonality/units)
               'level_z' (z-scored levels), 'yoy' (raw YoY, no z-score).
    """
    y_company = y_company or x_company
    y_var = y_var or x_var
    for v in (x_var, y_var):
        if v not in AVAILABLE_VARS:
            raise ValueError(f"unknown variable {v!r}. options: {list(AVAILABLE_VARS)}")

    long = P.load_long(db, tickers=sorted({x_company, y_company}))
    x_name, y_name = P.company_name(long, x_company), P.company_name(long, y_company)
    raw_x, raw_y = P.get_series(long, x_company, x_var), P.get_series(long, y_company, y_var)
    if raw_x.empty or raw_y.empty:
        raise ValueError("no data for one of the (company, variable) pairs.")

    def tf(s):
        if transform == "level_z":
            return ll.zscore(s)
        if transform == "yoy":
            return ll.yoy(s)
        return ll.zscore(ll.yoy(s))          # yoy_z default
    sig_x, sig_y = tf(raw_x), tf(raw_y)

    # cross-correlation function (k>0 ⇒ X leads Y)
    rows = []
    for k in range(-max_lag, max_lag + 1):
        d = pd.concat([sig_x, sig_y.shift(-k)], axis=1).dropna()
        n = len(d)
        if n >= 6:
            r = float(np.corrcoef(d.iloc[:, 0], d.iloc[:, 1])[0, 1])
            rows.append((k, r, _corr_p(r, n), n))
        else:
            rows.append((k, np.nan, np.nan, n))
    ccf = pd.DataFrame(rows, columns=["lag_k", "corr", "p_value", "n_overlap"])

    pos = ccf[(ccf["corr"] > 0) & ccf["corr"].notna()]
    best = pos.loc[pos["corr"].idxmax()] if not pos.empty else ccf.loc[ccf["corr"].abs().idxmax()]
    best_k, best_r, best_p = int(best["lag_k"]), float(best["corr"]), float(best["p_value"])
    contemp_r = float(ccf.loc[ccf["lag_k"] == 0, "corr"].iloc[0])
    n_overlap0 = int(ccf.loc[ccf["lag_k"] == 0, "n_overlap"].iloc[0])

    # Granger both ways
    lg = max(1, min(abs(best_k), 2))
    g_xy = ll.granger_p(sig_x, sig_y, lag=lg)
    g_yx = ll.granger_p(sig_y, sig_x, lag=lg)

    # orient + transmission regression
    if best_k > 0:
        up, down, up_n, down_n, lead = sig_x, sig_y, x_name, y_name, best_k
    elif best_k < 0:
        up, down, up_n, down_n, lead = sig_y, sig_x, y_name, x_name, -best_k
    else:
        up, down, up_n, down_n, lead = sig_x, sig_y, x_name, y_name, 0
    reg = pd.concat({"down": down, "up": up.shift(lead)}, axis=1).dropna()
    beta = intercept = r2 = np.nan
    if len(reg) >= 6:
        X = np.hstack([np.ones((len(reg), 1)), reg[["up"]].to_numpy()])
        b, *_ = np.linalg.lstsq(X, reg["down"].to_numpy(), rcond=None)
        intercept, beta = float(b[0]), float(b[1])
        pred = X @ b
        ss_res = float(((reg["down"].to_numpy() - pred) ** 2).sum())
        ss_tot = float(((reg["down"].to_numpy() - reg["down"].mean()) ** 2).sum())
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else np.nan

    verdict = _verdict(up_n, down_n, lead, best_r, best_p, g_xy, g_yx, x_name, y_name, x_company, y_company)

    return Result(
        x_company=x_company, x_var=x_var, x_label=AVAILABLE_VARS[x_var],
        y_company=y_company, y_var=y_var, y_label=AVAILABLE_VARS[y_var],
        x_name=x_name, y_name=y_name, transform=transform,
        sig_x=sig_x, sig_y=sig_y, raw_x=raw_x, raw_y=raw_y, ccf=ccf,
        best_k=best_k, best_r=best_r, best_p=best_p, contemp_r=contemp_r,
        lead=lead, up_name=up_n, down_name=down_n, up_sig=up, down_sig=down,
        granger_xy=g_xy, granger_yx=g_yx, beta=beta, intercept=intercept, r2=r2,
        n_reg=int(len(reg)), verdict=verdict,
        _meta={"n_overlap0": n_overlap0},
    )


def _verdict(up_n, down_n, lead, r, p, g_fwd, g_rev, x_name, y_name, xc, yc):
    if lead == 0:
        return "No lead-lag: strongest co-movement is contemporaneous (k=0)."
    sig = "significant" if (not np.isnan(p) and p < 0.05) else "NOT significant at 5%"
    out = [f"{up_n} leads {down_n} by {lead}q (r={r:.2f}, {sig})."]
    if not np.isnan(g_fwd) and not np.isnan(g_rev):
        if g_fwd < 0.05 and g_fwd < g_rev:
            out.append(f"Granger confirms {x_name}→{y_name} (p={g_fwd:.3f} < reverse {g_rev:.3f}).")
        elif g_rev < 0.05 and g_rev < g_fwd:
            out.append(f"Granger points the other way {y_name}→{x_name} (p={g_rev:.3f}).")
        else:
            out.append("Granger inconclusive (no significant asymmetry).")
    return " ".join(out)
