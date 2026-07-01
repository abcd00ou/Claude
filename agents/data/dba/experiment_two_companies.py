"""
experiment_two_companies.py — controlled lead-lag experiment on ANY two companies.

Isolates the pairwise lead-lag question from the full-panel pipeline so you can
inspect one relationship end-to-end: signals, the full cross-correlation function,
significance tests, Granger causality (both directions), and a 4-panel figure.

Usage:
    python3 experiment_two_companies.py                 # default NVDA vs MU
    python3 experiment_two_companies.py AVGO MU          # Broadcom vs Micron
    python3 experiment_two_companies.py AMAT LRCX --lag 6

Outputs (written next to this file):
    experiment_<A>_<B>.png        4-panel figure
    experiment_<A>_<B>_ccf.csv    the full cross-correlation table
    experiment_<A>_<B>_stats.md   the statistics summary table
"""
from __future__ import annotations
import argparse
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import leadlag as ll

HERE = Path(__file__).parent
DB = HERE / "financials.db"


# --------------------------------------------------------------------------- #
# helpers
# --------------------------------------------------------------------------- #
def qkey(s: str) -> int:
    y, q = s.split("-Q")
    return int(y) * 4 + int(q)


def load_series(con, ticker, col="revenue_usd_m"):
    df = pd.read_sql_query(
        "SELECT calendar_quarter cq, %s v FROM quarterly_financials "
        "WHERE ticker=? AND calendar_quarter IS NOT NULL AND %s IS NOT NULL" % (col, col),
        con, params=[ticker],
    )
    df = df.drop_duplicates("cq").sort_values("cq", key=lambda s: s.map(qkey))
    return df.set_index("cq")["v"]


def company_name(con, ticker):
    r = con.execute("SELECT name FROM companies WHERE ticker=?", [ticker]).fetchone()
    return r[0] if r else ticker


def corr_pvalue(r, n):
    """Two-sided p-value for a Pearson r (t-test; t^2 ~ F(1, n-2))."""
    if n < 4 or abs(r) >= 1:
        return np.nan
    t2 = (r * r) * (n - 2) / (1 - r * r)
    return ll._f_sf(t2, 1, n - 2)


# --------------------------------------------------------------------------- #
# experiment
# --------------------------------------------------------------------------- #
def run(tickA, tickB, max_lag=4, signal_col="revenue_usd_m"):
    con = sqlite3.connect(DB)
    nameA, nameB = company_name(con, tickA), company_name(con, tickB)
    rawA, rawB = load_series(con, tickA, signal_col), load_series(con, tickB, signal_col)
    con.close()

    # signal = YoY growth, z-scored (seasonality + unit neutral)
    sigA, sigB = ll.zscore(ll.yoy(rawA)), ll.zscore(ll.yoy(rawB))

    # ---- full cross-correlation function: k>0 => A leads B by k quarters ----
    rows = []
    for k in range(-max_lag, max_lag + 1):
        df = pd.concat([sigA, sigB.shift(-k)], axis=1).dropna()
        n = len(df)
        if n >= 6:
            r = float(np.corrcoef(df.iloc[:, 0], df.iloc[:, 1])[0, 1])
            rows.append((k, r, corr_pvalue(r, n), n))
        else:
            rows.append((k, np.nan, np.nan, n))
    ccf = pd.DataFrame(rows, columns=["lag_k", "corr", "p_value", "n_overlap"])

    # best positive-comovement lag (the demand-propagation peak)
    pos = ccf[(ccf["corr"] > 0) & ccf["corr"].notna()]
    best = pos.loc[pos["corr"].idxmax()] if not pos.empty else ccf.loc[ccf["corr"].abs().idxmax()]
    best_k, best_r, best_p = int(best["lag_k"]), float(best["corr"]), float(best["p_value"])
    contemp = ccf[ccf["lag_k"] == 0].iloc[0]

    # ---- Granger causality both directions at the best lag ----
    lag_for_granger = max(1, abs(best_k))
    if best_k >= 0:
        g_AtoB = ll.granger_p(sigA, sigB, lag=min(lag_for_granger, 2))
        g_BtoA = ll.granger_p(sigB, sigA, lag=min(lag_for_granger, 2))
    else:
        g_AtoB = ll.granger_p(sigA, sigB, lag=min(lag_for_granger, 2))
        g_BtoA = ll.granger_p(sigB, sigA, lag=min(lag_for_granger, 2))

    # ---- transmission regression at the best lag (leader -> follower) ----
    if best_k > 0:
        up, down, up_n, down_n, lead = sigA, sigB, nameA, nameB, best_k
    elif best_k < 0:
        up, down, up_n, down_n, lead = sigB, sigA, nameB, nameA, -best_k
    else:
        up, down, up_n, down_n, lead = sigA, sigB, nameA, nameB, 0
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

    verdict = _verdict(up_n, down_n, lead, best_r, best_p, g_AtoB, g_BtoA, nameA, nameB)

    stats = {
        "A": tickA, "B": tickB, "nameA": nameA, "nameB": nameB,
        "signal": signal_col, "quarters_A": int(rawA.shape[0]), "quarters_B": int(rawB.shape[0]),
        "contemp_corr": round(float(contemp["corr"]), 3) if pd.notna(contemp["corr"]) else None,
        "best_lag_k": best_k, "best_corr": round(best_r, 3), "best_corr_p": round(best_p, 4),
        "lead_statement": f"{up_n} leads {down_n} by {lead} quarter(s)" if lead else "contemporaneous",
        "granger_A_to_B_p": None if np.isnan(g_AtoB) else round(g_AtoB, 4),
        "granger_B_to_A_p": None if np.isnan(g_BtoA) else round(g_BtoA, 4),
        "transmission_beta": None if np.isnan(beta) else round(beta, 3),
        "transmission_r2": None if np.isnan(r2) else round(r2, 3),
        "n_regression": int(len(reg)),
        "verdict": verdict,
    }
    return dict(stats=stats, ccf=ccf, sigA=sigA, sigB=sigB, rawA=rawA, rawB=rawB,
                best_k=best_k, up=up, down=down, up_n=up_n, down_n=down_n, lead=lead,
                reg=reg, beta=beta, intercept=intercept, nameA=nameA, nameB=nameB)


def _verdict(up_n, down_n, lead, r, p, g_fwd, g_rev, nameA, nameB):
    if lead == 0:
        return "No lead-lag: strongest co-movement is contemporaneous."
    sig = "significant" if (not np.isnan(p) and p < 0.05) else "not significant at 5%"
    parts = [f"{up_n} leads {down_n} by {lead}q (r={r:.2f}, {sig})."]
    if not np.isnan(g_fwd) and not np.isnan(g_rev):
        if g_fwd < 0.05 and g_fwd < g_rev:
            parts.append(f"Granger CONFIRMS direction ({nameA}->{nameB} p={g_fwd:.3f} < reverse {g_rev:.3f}).")
        elif g_rev < 0.05 and g_rev < g_fwd:
            parts.append(f"Granger points the OTHER way ({nameB}->{nameA} p={g_rev:.3f}).")
        else:
            parts.append("Granger inconclusive (no significant asymmetry).")
    return " ".join(parts)


# --------------------------------------------------------------------------- #
# figure
# --------------------------------------------------------------------------- #
def make_figure(res, out_png):
    s = res["stats"]
    fig, ax = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle(
        f"Lead-Lag Experiment — {res['nameA']} ({s['A']}) vs {res['nameB']} ({s['B']})\n"
        f"signal = revenue YoY (z-scored)   |   {s['verdict']}",
        fontsize=12, fontweight="bold",
    )
    x = np.arange(len(res["sigA"].dropna().index.union(res["sigB"].dropna().index)))

    # (1) YoY time-series overlay
    a = ax[0, 0]
    a.plot(res["sigA"].index, res["sigA"].values, "-o", ms=3, label=res["nameA"], color="#1f77b4")
    a.plot(res["sigB"].index, res["sigB"].values, "-o", ms=3, label=res["nameB"], color="#d62728")
    a.axhline(0, color="grey", lw=0.6)
    a.set_title("(1) Signals over time (revenue YoY, z-scored)")
    a.set_ylabel("z-score"); a.legend(); _thin_xticks(a)

    # (2) cross-correlation function
    b = ax[0, 1]
    ccf = res["ccf"]
    colors = ["#2ca02c" if k == res["best_k"] else "#9ecae1" for k in ccf["lag_k"]]
    b.bar(ccf["lag_k"], ccf["corr"], color=colors)
    b.axhline(0, color="grey", lw=0.6)
    b.axvline(res["best_k"], color="#2ca02c", ls="--", lw=1)
    b.set_title(f"(2) Cross-correlation function  (peak at k={res['best_k']}, r={s['best_corr']})")
    b.set_xlabel(f"lag k  (k>0 ⇒ {res['nameA']} leads {res['nameB']})")
    b.set_ylabel("Pearson r")
    for _, row in ccf.iterrows():
        if pd.notna(row["corr"]):
            b.text(row["lag_k"], row["corr"] + (0.02 if row["corr"] >= 0 else -0.05),
                   f"{row['corr']:.2f}", ha="center", fontsize=7)

    # (3) aligned overlay: shift leader forward by best lag
    c = ax[1, 0]
    if res["lead"] != 0:
        up_shift = res["up"].shift(res["lead"])
        c.plot(res["down"].index, res["down"].values, "-o", ms=3, color="#d62728",
               label=f"{res['down_n']} (follower)")
        c.plot(up_shift.index, up_shift.values, "-o", ms=3, color="#1f77b4",
               label=f"{res['up_n']} shifted +{res['lead']}q (leader)")
        c.set_title(f"(3) Aligned after shifting leader by {res['lead']}q")
    else:
        c.plot(res["sigA"].index, res["sigA"].values, "-o", ms=3, label=res["nameA"])
        c.plot(res["sigB"].index, res["sigB"].values, "-o", ms=3, label=res["nameB"])
        c.set_title("(3) Contemporaneous overlay")
    c.axhline(0, color="grey", lw=0.6); c.legend(); c.set_ylabel("z-score"); _thin_xticks(c)

    # (4) scatter leader(t-k) vs follower(t) + regression line
    d = ax[1, 1]
    reg = res["reg"]
    if len(reg) >= 3 and not np.isnan(res["beta"]):
        d.scatter(reg["up"], reg["down"], color="#6a3d9a", s=28)
        xs = np.linspace(reg["up"].min(), reg["up"].max(), 50)
        d.plot(xs, res["intercept"] + res["beta"] * xs, "k--",
               label=f"β={s['transmission_beta']}, R²={s['transmission_r2']}")
        d.legend()
    d.set_title(f"(4) Transmission: {res['up_n']}(t−{res['lead']}) → {res['down_n']}(t)")
    d.set_xlabel(f"{res['up_n']} (leader, lagged)"); d.set_ylabel(f"{res['down_n']} (follower)")

    fig.tight_layout(rect=[0, 0, 1, 0.94])
    fig.savefig(out_png, dpi=130)
    plt.close(fig)


def _thin_xticks(ax_):
    labels = ax_.get_xticklabels()
    for i, lab in enumerate(labels):
        if i % 3 != 0:
            lab.set_visible(False)
    ax_.tick_params(axis="x", rotation=90, labelsize=7)


# --------------------------------------------------------------------------- #
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickerA", nargs="?", default="NVDA")
    ap.add_argument("tickerB", nargs="?", default="MU")
    ap.add_argument("--lag", type=int, default=4, help="max lag in quarters")
    ap.add_argument("--signal", default="revenue_usd_m")
    args = ap.parse_args()

    res = run(args.tickerA, args.tickerB, max_lag=args.lag, signal_col=args.signal)
    s = res["stats"]
    tag = f"{args.tickerA}_{args.tickerB}".replace(".", "")

    # ---- console: stats table ----
    print(f"\n{'='*74}\n LEAD-LAG EXPERIMENT:  {res['nameA']} ({s['A']})  vs  {res['nameB']} ({s['B']})\n{'='*74}")
    kv = [
        ("signal", s["signal"]),
        ("quarters available", f"{s['quarters_A']} ({s['A']}) / {s['quarters_B']} ({s['B']})"),
        ("contemporaneous corr (k=0)", s["contemp_corr"]),
        ("best lag k*", f"{s['best_lag_k']}  ({s['lead_statement']})"),
        ("peak correlation r", f"{s['best_corr']}  (p={s['best_corr_p']})"),
        (f"Granger {s['A']}→{s['B']} p", s["granger_A_to_B_p"]),
        (f"Granger {s['B']}→{s['A']} p", s["granger_B_to_A_p"]),
        ("transmission β", s["transmission_beta"]),
        ("transmission R²", s["transmission_r2"]),
        ("regression n", s["n_regression"]),
    ]
    for k, v in kv:
        print(f"  {k:<32} : {v}")
    print(f"\n  VERDICT: {s['verdict']}\n")

    print("  Cross-correlation function (k>0 ⇒ %s leads %s):" % (s["A"], s["B"]))
    print(res["ccf"].to_string(index=False,
          formatters={"corr": lambda x: f"{x:6.3f}" if pd.notna(x) else "   nan",
                      "p_value": lambda x: f"{x:6.3f}" if pd.notna(x) else "   nan"}))

    # ---- write artifacts ----
    ccf_path = HERE / f"experiment_{tag}_ccf.csv"
    png_path = HERE / f"experiment_{tag}.png"
    md_path = HERE / f"experiment_{tag}_stats.md"
    res["ccf"].to_csv(ccf_path, index=False)
    make_figure(res, png_path)

    md = [f"# Lead-Lag Experiment — {res['nameA']} ({s['A']}) vs {res['nameB']} ({s['B']})", "",
          f"**Signal:** {s['signal']} (YoY, z-scored)  |  **Date:** 2026-07-02", "",
          "| statistic | value |", "|---|---|"]
    for k, v in kv:
        md.append(f"| {k} | {v} |")
    md += ["", f"**Verdict:** {s['verdict']}", "",
           "## Cross-correlation function", "",
           "| lag k | corr | p-value | n |", "|---|---|---|---|"]
    for _, r in res["ccf"].iterrows():
        cc = f"{r['corr']:.3f}" if pd.notna(r["corr"]) else "nan"
        pp = f"{r['p_value']:.3f}" if pd.notna(r["p_value"]) else "nan"
        md.append(f"| {int(r['lag_k'])} | {cc} | {pp} | {int(r['n_overlap'])} |")
    md += ["", f"![figure](experiment_{tag}.png)", ""]
    md_path.write_text("\n".join(md))

    print(f"\n  [written] {png_path.name}\n  [written] {ccf_path.name}\n  [written] {md_path.name}")


if __name__ == "__main__":
    main()
