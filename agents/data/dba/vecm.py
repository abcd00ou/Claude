"""
vecm.py — (5) VECM 기반 mini-GEM: 밸류체인 보편관계를 연립 ECM 시스템으로.

universal.py가 찾은 보편 채널(매출→매출이 전 엣지 보편성 1.0)을 시스템으로 엮는다.
각 공급사 섹터의 매출(log)이 고객 섹터들의 매출에 오차수정하는 다변량 ECM을 추정하고,
방정식들을 하나의 시스템으로 묶어 충격을 전파시킨다(연결적 해석 = GEM의 핵심).

  장기(공적분): log(Y_s) = c + Σ_c θ_{s,c}·log(X_c) + 계절 + u_s
  단기(VECM):   Δlog(Y_s) = α_s + λ_s·u_{s,t-1} + Σ_c β_{s,c}·Δlog(X_c) + ε
  시스템:       위 방정식을 전 공급사 섹터에 대해 연립 → 충격 IRF 시뮬레이션

최상류 고객(Hyperscaler, Server OEM)은 방정식이 없는 외생 섹터. 충격을 여기에 주면
전 밸류체인으로 전파된다. Engle-Granger 다변량 근사(numpy), statsmodels 불요.

reuse: ecm.section_level(log 매출) · ecm._ols · ecm._season_dummies · valuechain.RELATIONSHIPS.
"""
from __future__ import annotations
from pathlib import Path

import numpy as np
import pandas as pd

import panel as P
import valuechain as V
import ecm as E

HERE = Path(__file__).parent

# 데이터 충분 + 밸류체인 중심 섹터 (foundry·odm 제외 — 데이터 부족)
CORE = ["hyperscalers", "server_oem", "ai_chip", "cpu", "dram", "nand",
        "server_networking", "hw_equipment", "osat_packaging"]


# --------------------------------------------------------------------------- #
def estimate_ecm_multi(y, Xdict):
    """다변량 Engle-Granger 2단계 ECM. y, X_c 는 log-level 시리즈."""
    cols = {"y": y, **{f"x_{c}": s for c, s in Xdict.items()}}
    df = pd.concat(cols, axis=1).dropna()
    if len(df) < 8 + len(Xdict):
        return None
    idx = df.index
    xcols = [f"x_{c}" for c in Xdict]
    # 1단계 장기: y = c0 + Σθ X + 계절더미
    Xl = np.column_stack([np.ones(len(df)), df[xcols].to_numpy(), E._season_dummies(idx)])
    lr = E._ols(Xl, df["y"].to_numpy())
    theta = {c: float(lr["beta"][1 + i]) for i, c in enumerate(Xdict)}
    u = pd.Series(lr["resid"], index=idx)
    c0 = float(lr["beta"][0])
    # 2단계 단기: Δy = α + λ u_{-1} + Σβ ΔX
    d = pd.concat({"dy": df["y"].diff(), "ec": u.shift(1),
                   **{f"dx_{c}": df[f"x_{c}"].diff() for c in Xdict}}, axis=1).dropna()
    if len(d) < 6 + len(Xdict):
        return None
    Xs = np.column_stack([np.ones(len(d)), d["ec"].to_numpy(),
                          d[[f"dx_{c}" for c in Xdict]].to_numpy()])
    sr = E._ols(Xs, d["dy"].to_numpy())
    lam = float(sr["beta"][1])
    beta = {c: float(sr["beta"][2 + i]) for i, c in enumerate(Xdict)}
    return dict(custs=list(Xdict), c0=c0, theta=theta, season=list(lr["beta"][1 + len(Xdict):]),
                alpha=float(sr["beta"][0]), lam=round(lam, 3), beta=beta,
                lam_t=round(float(sr["t"][1]), 2), lr_r2=round(lr["r2"], 3),
                sr_r2=round(sr["r2"], 3), n=len(df),
                error_correcting=bool(lam < 0 and sr["t"][1] < -1.6))


def build_system(long, sectors=CORE):
    """각 공급사 섹터의 다변량 ECM 방정식 추정 → 시스템."""
    logrev = {}
    for s in sectors:
        sig, mem = E.section_level(long, s, "revenue", log=True)
        if sig is not None:
            logrev[s] = sig
    eqs, exog = {}, []
    for s in sectors:
        if s not in logrev:
            continue
        custs = [c for c, ss in V.RELATIONSHIPS if ss == s and c in logrev and c != s]
        if not custs:
            exog.append(s); continue
        eq = estimate_ecm_multi(logrev[s], {c: logrev[c] for c in custs})
        if eq is None:
            exog.append(s)
        else:
            eqs[s] = eq
    return eqs, exog, logrev


# --------------------------------------------------------------------------- #
def _half_life(lam):
    return round(float(np.log(0.5) / np.log(1 + lam)), 2) if -2 < lam < 0 else None


def simulate(eqs, exog, shock_sector, shock_pct=10.0):
    """
    장기균형 전파(comparative statics): 외생 섹터 +shock_pct% 충격의 새 장기균형.
      Δlog(Y_s*) = Σ_c θ_{s,c}·Δlog(X_c*)  를 수렴할 때까지 반복(순환 대비).
    동적 IRF는 40분기 다변량에서 발산하므로, 안정적인 장기균형 + 조정 반감기(λ)로 대체.
    반환: 섹터별 {장기반응%, 조정 반감기(분기)}.
    """
    dshock = np.log1p(shock_pct / 100.0)
    dlog = {shock_sector: dshock}
    for e in exog:
        dlog.setdefault(e, 0.0)
    for _ in range(200):                            # 고정점 반복
        new = dict(dlog)
        for s, eq in eqs.items():
            new[s] = sum(eq["theta"][c] * dlog.get(c, 0.0) for c in eq["custs"])
        new[shock_sector] = dshock
        if max(abs(new.get(s, 0) - dlog.get(s, 0)) for s in new) < 1e-9:
            dlog = new; break
        dlog = new
    rows = []
    for s in list(eqs) + [x for x in exog]:
        resp = np.expm1(dlog.get(s, 0.0)) * 100.0
        hl = _half_life(eqs[s]["lam"]) if s in eqs else None
        rows.append(dict(sector=V.SECTIONS.get(s, s),
                         longrun_response_pct=round(resp, 2),
                         half_life_q=hl,
                         role="외생(충격)" if s == shock_sector else
                              ("외생" if s in exog else "방정식")))
    return pd.DataFrame(rows).sort_values("longrun_response_pct", ascending=False).reset_index(drop=True)


# --------------------------------------------------------------------------- #
def generate_md(eqs, exog, long, path, date="2026-07-08"):
    L = ["# VECM mini-GEM — 연립 ECM 시스템 (밸류체인 보편관계 기반)\n",
         f"**분석일:** {date} · **데이터:** `panel_long.csv` · **엔진:** `vecm.py`\n",
         "각 공급사 섹터 매출(log)이 고객 섹터 매출에 오차수정하는 다변량 ECM을 연립. "
         "충격을 외생 섹터에 주면 시스템 전체로 전파(연결적 해석).\n",
         f"\n- 방정식 섹터: {len(eqs)} · 외생(최상류) 섹터: {', '.join(V.SECTIONS.get(s,s) for s in exog)}\n"]
    L.append("\n## 방정식 (장기 탄력성 θ · 조정속도 λ)\n")
    L.append("| 공급사 (Y) | 고객 (X) | θ (장기탄력성) | λ (조정) | 오차수정 | 장기R² |")
    L.append("|---|---|---|---|---|---|")
    for s, eq in eqs.items():
        th = ", ".join(f"{V.SECTIONS.get(c,c)}={round(eq['theta'][c],2)}" for c in eq["custs"])
        L.append(f"| {V.SECTIONS.get(s,s)} | {', '.join(V.SECTIONS.get(c,c) for c in eq['custs'])} | "
                 f"{th} | {eq['lam']} (t={eq['lam_t']}) | {'✅' if eq['error_correcting'] else '·'} | {eq['lr_r2']} |")

    # 대표 시나리오: Hyperscaler +10% (장기균형 전파)
    if "hyperscalers" in exog:
        irf = simulate(eqs, exog, "hyperscalers", 10)
        L.append("\n## 시나리오: Hyperscaler 매출 영구 +10% → 장기 전파 (comparative statics)\n")
        L.append("| 섹터 | 장기 매출반응 % | 조정 반감기(분기) | 역할 |")
        L.append("|---|---|---|---|")
        for r in irf.itertuples(index=False):
            L.append(f"| {r.sector} | {r.longrun_response_pct} | "
                     f"{r.half_life_q if r.half_life_q else '—'} | {r.role} |")

    L += ["\n## 해석\n",
          "- θ = 고객 매출 1% → 공급사 매출 장기 θ%. λ<0·유의 = 오차수정(장기균형 복원).\n",
          "- 시나리오: 외생 충격이 밸류체인을 타고 하류로 전파되는 연결적 경로.\n",
          "\n## 한계\n",
          "- 표본 ~40분기 + AI붐 구조변화 → 공적분 검정력 낮음. θ·λ 부호로 신뢰도 판단.\n",
          "- Engle-Granger 다변량 근사(단일 공적분 가정). Johansen VECM은 향후 확장.\n",
          "- Foundry·ODM 데이터 부족으로 시스템 제외(데이터 쌓이면 CORE에 추가).\n"]
    Path(path).write_text("\n".join(L))
    return path


def _nid(s):
    return "n_" + str(s).replace(" ", "").replace("/", "")


def generate_html(eqs, exog, long, path, shock="hyperscalers", date="2026-07-08"):
    # mermaid 시스템 다이어그램: 고객→공급사, θ 라벨, 오차수정 굵게
    edges = []
    for s, eq in eqs.items():
        for c in eq["custs"]:
            th = round(eq["theta"][c], 2)
            arrow = "==>" if eq["error_correcting"] else "-->"
            edges.append(f'  {_nid(V.SECTIONS.get(c,c))}["{V.SECTIONS.get(c,c)}"] {arrow}'
                         f'|"θ={th}"| {_nid(V.SECTIONS.get(s,s))}["{V.SECTIONS.get(s,s)}"]')
    mer = "flowchart LR\n" + "\n".join(edges)

    eqrows = []
    for s, eq in eqs.items():
        th = ", ".join(f"{V.SECTIONS.get(c,c)}={round(eq['theta'][c],2)}" for c in eq["custs"])
        cls = "sig" if eq["error_correcting"] else ""
        eqrows.append(f"<tr class='{cls}'><td>{V.SECTIONS.get(s,s)}</td><td class='var'>{th}</td>"
                      f"<td>{eq['lam']} (t={eq['lam_t']})</td><td>{'✅' if eq['error_correcting'] else '·'}</td>"
                      f"<td>{eq['lr_r2']}</td></tr>")
    eqtable = "\n".join(eqrows)

    irf = simulate(eqs, exog, shock, 10)
    irows = []
    for r in irf.itertuples(index=False):
        w = max(1.0, abs(float(irf["longrun_response_pct"].abs().max())))
        pct = r.longrun_response_pct
        bw = int(round(abs(pct) / w * 100))
        col = "#2ca02c" if pct >= 0 else "#d62728"
        irows.append(f"<tr><td>{r.sector}</td><td><div class='barwrap'>"
                     f"<div class='bar' style='width:{bw}%;background:{col}'></div>"
                     f"<span>{pct}%</span></div></td>"
                     f"<td>{r.half_life_q if r.half_life_q else '—'}</td><td>{r.role}</td></tr>")
    itable = "\n".join(irows)

    html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>VECM mini-GEM</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
 body{{font-family:-apple-system,'Malgun Gothic',sans-serif;margin:32px;color:#1a1a1a}}
 h1{{font-size:21px}} h2{{font-size:15px;margin-top:22px}} .sub{{color:#666;font-size:13px}}
 .mermaid{{background:#fafafa;border:1px solid #eee;border-radius:8px;padding:16px;margin:12px 0}}
 table{{border-collapse:collapse;width:100%;font-size:13px}}
 th,td{{border:1px solid #e6e6e6;padding:6px 8px;text-align:center}}
 th{{background:#f4f4f4}} tr.sig{{background:#eefbf0}}
 td.var{{font-family:ui-monospace,Menlo,monospace;font-size:11px}}
 .barwrap{{position:relative;background:#eef2f7;border-radius:4px;height:18px;min-width:80px}}
 .bar{{height:18px;border-radius:4px}} .barwrap span{{position:absolute;left:6px;top:0;line-height:18px;font-size:11px;color:#123}}
 .interp{{background:#fff8e1;border-left:4px solid #f0b400;padding:12px 16px;margin:14px 0;font-size:13px;line-height:1.75;border-radius:4px}}
 .interp b{{color:#8a6d00}}
</style></head><body>
<h1>VECM mini-GEM — 밸류체인 연립 ECM 시스템</h1>
<div class="sub">공급사 매출이 고객 매출에 오차수정 · 굵은 화살표=오차수정(λ&lt;0·유의) · θ=장기탄력성 · 분석일 {date}</div>
<div class="interp">
📖 <b>이 시스템 읽는 법 (mini-GEM)</b><br>
각 공급사 섹터의 매출이 고객 섹터 매출에 맞춰 조정되는 방정식들을 <b>하나의 연결된 시스템</b>으로 엮은 것입니다
(Oxford GEM의 국가 방정식과 같은 구조를 산업에 적용).<br>
• 다이어그램 <b>θ = 장기 탄력성</b>: 고객 매출 1%↑ → 공급사 매출 장기 θ%↑. 굵은 화살표 = <b>오차수정</b>(λ&lt;0·유의, 장기균형으로 복원).<br>
• 아래 <b>시나리오</b>: Hyperscaler 매출 <b>영구 +10% 충격이 밸류체인 하류로 전파</b>되는 장기 반응입니다
(예: AI Chip +3%, Server Networking +2.7%). <b>반감기</b> = 조정 속도(작을수록 빠름).<br>
👉 이것이 "한 곳의 충격이 공급망 전체로 어떻게 번지는가"를 보는 GEM의 핵심입니다.
(동적 IRF는 40분기 표본에서 발산하므로 안정적인 <b>장기균형 반응</b>으로 표시합니다.)
</div>
<div class="mermaid">
{mer}
</div>
<h2>방정식 (장기 탄력성 θ · 조정속도 λ)</h2>
<table>
<tr><th>공급사(Y)</th><th>θ (고객별 장기탄력성)</th><th>λ (조정)</th><th>오차수정</th><th>장기R²</th></tr>
{eqtable}
</table>
<h2>시나리오: {V.SECTIONS.get(shock,shock)} 매출 영구 +10% → 장기 전파</h2>
<table>
<tr><th>섹터</th><th>장기 매출반응</th><th>조정 반감기(분기)</th><th>역할</th></tr>
{itable}
</table>
<script>mermaid.initialize({{startOnLoad:true,flowchart:{{curve:'basis'}}}});</script>
</body></html>"""
    Path(path).write_text(html)
    return path
