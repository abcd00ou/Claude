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


def generate_simulator_html(eqs, exog, long, path, date="2026-07-20"):
    """(산출물 c) 인터랙티브 시뮬레이터: 충격 섹터·크기 → 전 섹터 장기추세 곡선."""
    import json
    sectors = list(eqs) + list(exog)
    labels = {s: V.SECTIONS.get(s, s) for s in sectors}
    # 각 섹터 대표기업(매출 1위) — '특정 기업' 라벨용
    reps = {}
    for s in sectors:
        try:
            import pairwise_cashflow as PW
            r = PW.top_company(long, s)
            reps[s] = P.company_name(long, r) if r else "—"
        except Exception:
            reps[s] = "—"
    model = {
        "sectors": sectors, "exog": list(exog), "labels": labels, "reps": reps,
        "eqs": {s: {"custs": eq["custs"], "theta": eq["theta"], "lam": eq["lam"]}
                for s, eq in eqs.items()},
    }
    # 지표→매출 등가 전환계수 (회계 근거): revenue 직접, COGS=거래항등식,
    # AP=P5 실측 corr, capex/inventory=부분 전이. accounting_flow_theory §4 참조.
    model["indicators"] = {
        "revenue": {"label": "매출 (Revenue)", "elas": 1.00, "basis": "직접 매출"},
        "cogs": {"label": "매출원가/매입 (COGS)", "elas": 1.00, "basis": "거래항등식 Purch_C≈Rev_S"},
        "accounts_payable": {"label": "매입채무 (AP)", "elas": 0.70, "basis": "P5 거울항등식 AP_C↔AR_S (실측 r≈0.65)"},
        "inventory": {"label": "재고 (Inventory)", "elas": 0.60, "basis": "재고→주문 전이"},
        "capex": {"label": "설비투자 (Capex)", "elas": 0.45, "basis": "투자→매출 부분 전이"},
    }
    mj = json.dumps(model, ensure_ascii=False)
    opts = "\n".join(f'<option value="{s}">{labels[s]} (대표: {reps[s]})</option>' for s in sectors)
    iopts = "\n".join(f'<option value="{k}">{v["label"]}</option>'
                      for k, v in model["indicators"].items())

    html = """<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>VECM mini-GEM 시뮬레이터</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4"></script>
<style>
 body{font-family:-apple-system,'Malgun Gothic',sans-serif;margin:28px;color:#1a1a1a}
 h1{font-size:20px} .sub{color:#666;font-size:13px;margin-bottom:12px}
 .interp{background:#fff8e1;border-left:4px solid #f0b400;padding:12px 16px;margin:12px 0;font-size:13px;line-height:1.7;border-radius:4px}
 .interp b{color:#8a6d00}
 .ctl{display:flex;gap:18px;align-items:center;flex-wrap:wrap;background:#f7f8fa;border:1px solid #e6e6e6;border-radius:8px;padding:14px 16px;margin:12px 0}
 .ctl label{font-size:13px;font-weight:600} select,input{font-size:13px}
 #val{font-weight:700;color:#1f6feb;min-width:52px;display:inline-block}
 #ebox{font-size:12px;color:#666;margin:4px 0 10px}
 canvas{max-height:440px} table{border-collapse:collapse;font-size:12.5px;margin-top:14px;width:100%}
 th,td{border:1px solid #e6e6e6;padding:5px 8px;text-align:center} th{background:#f4f4f4}
</style></head><body>
<h1>VECM mini-GEM 시뮬레이터 — 회계지표 충격 → 장기추세</h1>
<div class="sub">특정 섹터(대표기업)의 <b>회계지표</b>(매출·AP·COGS·재고·capex)에 영구 충격을 주면, 밸류체인 전체 매출이 장기적으로 어떻게 반응하는지 시뮬레이션 · __DATE__</div>
<div class="interp">
📖 <b>사용법</b> — ① <b>충격 대상 섹터</b>, ② <b>충격 지표</b>(매출/AP/COGS/재고/capex), ③ <b>크기(%)</b>를 고르세요.
회계지표 충격은 <b>거래 항등식</b>으로 "그 섹터 활동의 매출 등가"로 환산(전환계수)된 뒤, VECM 공적분+오차수정(λ)으로
밸류체인에 전파됩니다.<br>
• <b>전환계수</b>: 매출·COGS=1.0(거래항등식), AP=0.70(거울항등식 P5), 재고=0.60, capex=0.45.<br>
👉 예: <b>AI Chip의 AP +10%</b> → 매입채무 증가가 공급사(DRAM 등) 매출로 전이되는 장기추세.
(장기균형 comparative statics — 안정 시뮬레이션)
</div>
<div class="ctl">
 <div><label>① 충격 대상 섹터</label><br><select id="shock">__OPTS__</select></div>
 <div><label>② 충격 지표</label><br><select id="ind">__IOPTS__</select></div>
 <div><label>③ 충격 크기</label><br><input id="pct" type="range" min="-20" max="30" value="10" step="1">
   <span id="val">+10%</span></div>
 <div><label>④ 기간(분기)</label><br><input id="hz" type="range" min="4" max="24" value="12" step="1">
   <span id="hzv">12</span></div>
</div>
<div id="ebox"></div>
<canvas id="chart"></canvas>
<table id="tbl"></table>
<script>
const M = __MODEL__;
const PAL = ['#1f77b4','#d62728','#2ca02c','#9467bd','#ff7f0e','#17becf','#8c564b','#e377c2','#7f7f7f'];

// shock: 어느 섹터든(외생·내생). indicator: 지표(전환계수 적용). 충격섹터는 고정, 나머지 내생은 θ 전파.
function simulate(shock, indicator, pct, H){
  const elas = M.indicators[indicator].elas;
  const ds = Math.log(1 + (pct*elas)/100);       // 지표→매출 등가 충격
  let dl={}; M.sectors.forEach(s=>dl[s]=0); dl[shock]=ds;
  for(let it=0; it<300; it++){
    let nw=Object.assign({},dl);
    for(const s in M.eqs){ if(s===shock) continue;
      nw[s]=M.eqs[s].custs.reduce((a,c)=>a+(M.eqs[s].theta[c]||0)*(dl[c]||0),0); }
    nw[shock]=ds; dl=nw;
  }
  let y={}; M.sectors.forEach(s=>y[s]=0); y[shock]=ds;
  let paths={}; M.sectors.forEach(s=>paths[s]=[0]);
  for(let t=1;t<=H;t++){
    let nw=Object.assign({},y);
    for(const s in M.eqs){ if(s===shock) continue;
      const tgt=dl[s]||0, lam=M.eqs[s].lam;
      nw[s]= y[s] + (lam<0? lam : -0.15)*(y[s]-tgt); }
    nw[shock]=ds; y=nw;
    M.sectors.forEach(s=>paths[s].push((Math.exp(y[s])-1)*100));
  }
  return {paths, longrun:dl};
}

let chart;
function render(){
  const shock=document.getElementById('shock').value;
  const ind=document.getElementById('ind').value;
  const pct=+document.getElementById('pct').value;
  const H=+document.getElementById('hz').value;
  document.getElementById('val').textContent=(pct>=0?'+':'')+pct+'%';
  document.getElementById('hzv').textContent=H;
  const inf=M.indicators[ind];
  document.getElementById('ebox').innerHTML='전환계수 β='+inf.elas+' ('+inf.basis+') → 매출 등가 충격 '+
     ((pct>=0?'+':'')+(pct*inf.elas).toFixed(1))+'%';
  const {paths,longrun}=simulate(shock,ind,pct,H);
  const labels=[...Array(H+1).keys()];
  const order=M.sectors.slice().sort((a,b)=>Math.abs((longrun[b]||0))-Math.abs((longrun[a]||0)));
  const ds=order.map((s,i)=>({label:M.labels[s]+(s===shock?' (충격)':''),
     data:paths[s], borderColor:PAL[i%PAL.length], borderWidth:s===shock?3:2,
     borderDash:s===shock?[6,3]:[], pointRadius:0, tension:.25}));
  if(chart) chart.destroy();
  chart=new Chart(document.getElementById('chart'),{type:'line',
    data:{labels,datasets:ds},
    options:{responsive:true,interaction:{mode:'index',intersect:false},
      plugins:{title:{display:true,text:M.labels[shock]+' '+inf.label+' '+(pct>=0?'+':'')+pct+'% 충격 → 섹터별 매출 % 반응'},
        legend:{position:'right',labels:{font:{size:11}}}},
      scales:{x:{title:{display:true,text:'분기 후'}},y:{title:{display:true,text:'매출 반응 %'}}}}});
  let h='<tr><th>섹터</th><th>대표기업</th><th>장기 매출반응 %</th></tr>';
  order.forEach(s=>{h+='<tr><td>'+M.labels[s]+'</td><td>'+M.reps[s]+'</td><td>'+
     ((Math.exp(longrun[s]||0)-1)*100).toFixed(2)+'</td></tr>';});
  document.getElementById('tbl').innerHTML=h;
}
['shock','ind','pct','hz'].forEach(id=>document.getElementById(id).addEventListener('input',render));
render();
</script></body></html>"""
    html = (html.replace("__MODEL__", mj).replace("__OPTS__", opts)
                .replace("__IOPTS__", iopts).replace("__DATE__", date))
    Path(path).write_text(html)
    return path


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
