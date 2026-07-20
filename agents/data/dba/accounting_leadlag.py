"""
accounting_leadlag.py — (산출물 a) 회계지표 기업간/기업내 lead-lag 도출·수식·도식.

reports/accounting_flow_theory.md 의 회계 항등식에서 연역한 가설 P1–P7을 데이터로
검증한다. 기업간(cross)은 고객사×공급사 기업쌍, 기업내(internal)는 동일기업 X_t→Y_{t+k}.
예측 시차/부호(회계 근거)와 실측을 대조해 논문 실증 테이블 + mermaid 회계흐름 도식을 만든다.

reuse: features.get_feature(변환) · cashflow_leadlag.lead_lag_scan · universal.channel_universality
       · pairwise_cashflow.members · valuechain.RELATIONSHIPS
"""
from __future__ import annotations
from pathlib import Path

import numpy as np
import pandas as pd

import panel as P
import features as F
import valuechain as V
import cashflow_leadlag as C
import pairwise_cashflow as PW
import universal as U

HERE = Path(__file__).parent
INT_TICKERS = ["NVDA", "AMD", "AVGO", "MRVL", "MU", "INTC", "AMAT", "LRCX",
               "AMKR", "DELL", "SMCI", "STX", "WDC", "ANET", "CSCO"]

# 이론(theory.md §4)에서 연역한 가설. kind: cross(기업간)/internal(기업내)
HYPOTHESES = [
    dict(id="P1", kind="cross", x="COGS", xtf="rolling_yoy", y="REVENUE", ytf="rolling_yoy",
         exp_lag="0–1", sign="+", basis="거래 항등식 Rev_S=Σω·Purch_C (정의1)",
         label="고객 매입(COGS) → 공급사 매출"),
    dict(id="P2", kind="internal", x="REVENUE", xtf="rolling_yoy", y="AR", ytf="rolling_yoy",
         exp_lag="0", sign="+", basis="AR 동학 (정의4)", label="매출 → 매출채권"),
    dict(id="P3", kind="internal", x="REVENUE", xtf="growth_yoy", y="OCF", ytf="growth_yoy",
         exp_lag="+DSO", sign="+", basis="OCF=NI+D&A−ΔNWC (정의5)", label="매출 → 영업현금흐름"),
    dict(id="P4", kind="cross", x="REVENUE", xtf="rolling_yoy", y="REVENUE", ytf="rolling_yoy",
         exp_lag="0–2", sign="+", basis="수요→매입→매출 전파", label="고객 매출 → 공급사 매출"),
    dict(id="P5", kind="cross", x="AP", xtf="rolling_yoy", y="AR", ytf="rolling_yoy",
         exp_lag="0–1", sign="+", basis="거울 항등식 AP_C=AR_S (정의2)", label="고객 매입채무 → 공급사 매출채권"),
    dict(id="P6", kind="cross", x="DPO", xtf="level", y="DSO", ytf="level",
         exp_lag="0–2", sign="+", basis="현금전이 DPO_C→DSO_S (§3)", label="고객 지급기간 → 공급사 회수기간"),
    dict(id="P7", kind="internal", x="CCC", xtf="level", y="FCF_MARGIN", ytf="level",
         exp_lag="0–1", sign="-", basis="CCC·현금전환 (정의3,5)", label="현금전환주기 → FCF마진"),
]


# --------------------------------------------------------------------------- #
def test_internal(long, x, xtf, y, ytf, sign, tickers=INT_TICKERS, lags=(0, 4), min_n=10):
    """동일기업 X_t → Y_{t+k}: 부호일치·유의 비율, 평균시차·상관."""
    tot = sig = 0
    corrs, lgs = [], []
    for tk in tickers:
        xs, ys = F.get_feature(long, tk, x, xtf), F.get_feature(long, tk, y, ytf)
        if xs.dropna().shape[0] < min_n or ys.dropna().shape[0] < min_n:
            continue
        r = C.lead_lag_scan(xs, ys, lags, expected=sign)
        if r.get("status") != "ok" or r["n"] < min_n:
            continue
        tot += 1
        if r["significant"] and r["sign_match"]:
            sig += 1
            corrs.append(abs(r["pearson"]))
            lgs.append(r["best_lag"])
    return dict(support_rate=round(sig / tot, 2) if tot else 0.0, n_sig=sig, n_tested=tot,
                mean_corr=round(float(np.mean(corrs)), 3) if corrs else None,
                mean_lag=round(float(np.mean(lgs)), 2) if lgs else None)


def test_cross(long, x, xtf, y, ytf, sign, lags=(0, 4)):
    """기업간(고객사×공급사) 보편성: universal 엔진 재사용 + 부호."""
    summ, edf = U.channel_universality(long, x, xtf, y, ytf, V.RELATIONSHIPS, lags)
    return dict(support_rate=summ["universality"], n_sig=summ["total_sig_pairs"],
                n_tested=summ["total_pairs"], mean_corr=summ["mean_corr"],
                mean_lag=summ["mean_lag"], edges_ok=summ["edges_ok"],
                edges=summ["edges_analyzable"])


def run_hypotheses(long):
    rows = []
    for h in HYPOTHESES:
        if h["kind"] == "cross":
            res = test_cross(long, h["x"], h["xtf"], h["y"], h["ytf"], h["sign"])
        else:
            res = test_internal(long, h["x"], h["xtf"], h["y"], h["ytf"], h["sign"])
        rows.append({**{k: h[k] for k in ("id", "kind", "label", "x", "xtf", "y", "ytf",
                                          "exp_lag", "sign", "basis")}, **res})
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- #
# 기업(쌍)별 상세 통계 검증 — 논문 부록
# --------------------------------------------------------------------------- #
def _detail_internal(long, h, tickers=INT_TICKERS, lags=(0, 4), min_n=10):
    rows = []
    for tk in tickers:
        xs = F.get_feature(long, tk, h["x"], h["xtf"])
        ys = F.get_feature(long, tk, h["y"], h["ytf"])
        if xs.dropna().shape[0] < min_n or ys.dropna().shape[0] < min_n:
            continue
        r = C.lead_lag_scan(xs, ys, lags, expected=h["sign"])
        if r.get("status") != "ok" or r["n"] < min_n:
            continue
        rows.append(dict(hypothesis=h["id"], kind="기업내", label=h["label"],
                         entity=P.company_name(long, tk), sector=P.section_of(long, tk),
                         counterparty="—", lag_q=r["best_lag"], pearson=r["pearson"],
                         spearman=r["spearman"], p_value=r["p_value"], n=r["n"],
                         sign_expected=h["sign"], significant=bool(r["significant"] and r["sign_match"])))
    return rows


def _detail_cross(long, h, lags=(0, 4), min_n=10):
    rows = []
    for cs, ss in V.RELATIONSHIPS:
        cs_m = PW.members(long, cs, h["x"])
        ss_m = PW.members(long, ss, h["y"])
        for ct in cs_m:
            xs = F.get_feature(long, ct, h["x"], h["xtf"])
            if xs.dropna().shape[0] < min_n:
                continue
            for st in ss_m:
                if ct == st:
                    continue
                ys = F.get_feature(long, st, h["y"], h["ytf"])
                if ys.dropna().shape[0] < min_n:
                    continue
                r = C.lead_lag_scan(xs, ys, lags, expected=h["sign"])
                if r.get("status") != "ok" or r["n"] < min_n:
                    continue
                rows.append(dict(hypothesis=h["id"], kind="기업간", label=h["label"],
                                 entity=P.company_name(long, ct), sector=V.SECTIONS.get(cs, cs),
                                 counterparty=P.company_name(long, st),
                                 counterparty_sector=V.SECTIONS.get(ss, ss),
                                 lag_q=r["best_lag"], pearson=r["pearson"], spearman=r["spearman"],
                                 p_value=r["p_value"], n=r["n"], sign_expected=h["sign"],
                                 significant=bool(r["significant"] and r["sign_match"])))
    return rows


def run_detail(long):
    """모든 가설의 기업(쌍)별 통계 검증 상세 (long DataFrame)."""
    rows = []
    for h in HYPOTHESES:
        rows += (_detail_cross(long, h) if h["kind"] == "cross" else _detail_internal(long, h))
    cols = ["hypothesis", "kind", "label", "entity", "sector", "counterparty",
            "counterparty_sector", "lag_q", "pearson", "spearman", "p_value", "n",
            "sign_expected", "significant"]
    df = pd.DataFrame(rows)
    return df[[c for c in cols if c in df.columns]] if len(df) else df


def generate_detail_html(det, path, date="2026-07-20"):
    """기업(쌍)별 상세 통계 — JS 필터/정렬 테이블 (논문 부록)."""
    import json
    recs = det.to_dict(orient="records")
    hyps = sorted(det["hypothesis"].unique())
    payload = json.dumps(recs, ensure_ascii=False, default=str)
    hopts = "".join(f'<option value="{h}">{h}</option>' for h in hyps)
    html = """<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>기업별 Lead-Lag 통계 검증 (부록)</title>
<style>
 body{font-family:-apple-system,'Malgun Gothic',sans-serif;margin:24px;color:#1a1a1a}
 h1{font-size:20px} .sub{color:#666;font-size:13px;margin-bottom:10px}
 .interp{background:#fff8e1;border-left:4px solid #f0b400;padding:11px 15px;margin:10px 0;font-size:13px;line-height:1.7;border-radius:4px}
 .ctl{display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin:10px 0;font-size:13px}
 table{border-collapse:collapse;width:100%;font-size:12px} th,td{border:1px solid #e6e6e6;padding:4px 7px;text-align:center}
 th{background:#f4f4f4;cursor:pointer;position:sticky;top:0} tr.sig{background:#eefbf0}
 td.l{text-align:left} .p0{color:#0a0;font-weight:600} .neg{color:#c00}
 #n{color:#666}
</style></head><body>
<h1>기업(쌍)별 Lead-Lag 통계 검증 — 부록</h1>
<div class="sub">각 가설 P1–P7을 개별 기업/기업쌍 단위로 검정 · 분석일 __DATE__</div>
<div class="interp">
📖 각 행은 <b>한 기업(기업내) 또는 한 기업쌍(기업간)</b>의 lead-lag 검정 결과입니다.
<b>lag</b>=선행 분기, <b>r</b>=Pearson, <b>ρ</b>=Spearman(비선형/순위), <b>p</b>=유의확률,
<b>n</b>=표본 분기수. 초록 배경 = 예측부호 일치 & p&lt;0.05 유의. 헤더 클릭 시 정렬.
</div>
<div class="ctl">
 <span>가설 <select id="fh"><option value="">전체</option>__HOPTS__</select></span>
 <span><label><input type="checkbox" id="fs"> 유의(p&lt;0.05)만</label></span>
 <span>기업 검색 <input id="fq" placeholder="예: NVIDIA"></span>
 <span id="n"></span>
</div>
<table id="t"><thead><tr>
 <th data-k="hypothesis">가설</th><th data-k="kind">유형</th><th data-k="label" class="l">관계</th>
 <th data-k="entity" class="l">기업(X)</th><th data-k="counterparty" class="l">상대(Y)</th>
 <th data-k="lag_q">lag</th><th data-k="pearson">r</th><th data-k="spearman">ρ</th>
 <th data-k="p_value">p</th><th data-k="n">n</th><th data-k="significant">유의</th>
</tr></thead><tbody id="b"></tbody></table>
<script>
const D=__PAYLOAD__; let sortK='pearson', sortA=false;
const fh=document.getElementById('fh'),fs=document.getElementById('fs'),fq=document.getElementById('fq');
function view(){
 let r=D.filter(d=>(!fh.value||d.hypothesis===fh.value)&&(!fs.checked||d.significant)&&
   (!fq.value||((d.entity||'')+ (d.counterparty||'')).toLowerCase().includes(fq.value.toLowerCase())));
 r.sort((a,b)=>{let x=a[sortK],y=b[sortK]; if(typeof x==='string'){return sortA?(''+x).localeCompare(y):(''+y).localeCompare(x);} return sortA?x-y:y-x;});
 document.getElementById('n').textContent=r.length+' 행';
 document.getElementById('b').innerHTML=r.map(d=>`<tr class="${d.significant?'sig':''}">
   <td>${d.hypothesis}</td><td>${d.kind}</td><td class="l">${d.label}</td>
   <td class="l">${d.entity}</td><td class="l">${d.counterparty||'—'}</td>
   <td>${d.lag_q}</td><td class="${d.pearson<0?'neg':''}">${(+d.pearson).toFixed(3)}</td>
   <td>${d.spearman==null?'':(+d.spearman).toFixed(3)}</td>
   <td class="${d.p_value<0.05?'p0':''}">${d.p_value==null?'':(+d.p_value).toFixed(4)}</td>
   <td>${d.n}</td><td>${d.significant?'✅':''}</td></tr>`).join('');
}
document.querySelectorAll('th').forEach(th=>th.onclick=()=>{const k=th.dataset.k; if(k===sortK)sortA=!sortA; else{sortK=k;sortA=false;} view();});
[fh,fq].forEach(e=>e.oninput=view); fs.onchange=view; view();
</script></body></html>"""
    html = (html.replace("__PAYLOAD__", payload).replace("__HOPTS__", hopts)
                .replace("__DATE__", date))
    Path(path).write_text(html)
    return path


# --------------------------------------------------------------------------- #
def _mermaid_chain():
    """회계 흐름 도식 (mermaid): P1–P7 체인."""
    return """flowchart LR
  RevC["고객 매출<br/>Rev_C"] -->|"P4 (0–2q)"| PurC["고객 매입<br/>Purch_C≈COGS"]
  PurC -->|"P1 (0–1q)<br/>거래항등식"| RevS["공급사 매출<br/>Rev_S"]
  RevS -->|"P2 (0q)"| ARS["공급사 매출채권<br/>AR_S"]
  ARS -->|"P3 (+DSO)"| OCFS["공급사 영업현금<br/>OCF_S"]
  OCFS -->|"− Capex"| FCFS["공급사 잉여현금<br/>FCF_S"]
  APC["고객 매입채무<br/>AP_C"] -.->|"P5 거울항등식"| ARS
  DPOC["고객 지급기간<br/>DPO_C"] -.->|"P6 (0–2q)"| DSOS["공급사 회수기간<br/>DSO_S"]
  CCCS["공급사 CCC"] -->|"P7 (−)"| FCFS"""


def generate_md(df, long, path, date="2026-07-20"):
    L = ["# 회계지표 기업간 Lead-Lag — 도출·수식·도식 (산출물 a)\n",
         f"**분석일:** {date} · **데이터:** `panel_long.csv` · **이론:** `accounting_flow_theory.md`\n",
         "복식부기 항등식에서 연역한 가설 P1–P7을 데이터로 검증. 예측 시차/부호(회계 근거)와 "
         "실측(support_rate=부호일치·유의 비율)을 대조.\n"]
    L.append("\n## 1. 회계 흐름 도식\n```mermaid\n" + _mermaid_chain() + "\n```\n")
    L.append("\n## 2. 가설 검증 결과\n")
    L.append("| # | 유형 | 관계 | 회계 근거 | 예측시차 | 예측부호 | 실측 지지율 | 유의/검정 | 실측 평균시차 | 평균 r |")
    L.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in df.itertuples(index=False):
        kind = "기업간" if r.kind == "cross" else "기업내"
        sr = "— (데이터부족)" if r.n_tested == 0 else f"**{r.support_rate}**"
        L.append(f"| **{r.id}** | {kind} | {r.label} | {r.basis} | {r.exp_lag} | {r.sign} | "
                 f"{sr} | {r.n_sig}/{r.n_tested} | {r.mean_lag} | {r.mean_corr} |")
    L.append("\n## 3. 핵심 수식 (이론 문서 §요약)\n")
    L += [
        "**거래 항등식 (P1):**  $\\text{Rev}_{S,t}=\\sum_{C\\to S}\\omega_{C\\to S}\\,\\text{Purch}_{C,t}$, "
        "$\\ \\text{Purch}_C=\\text{COGS}_C+\\Delta\\text{Inv}_C$\n",
        "**거울 항등식 (P5):**  $\\text{AP}^{(C\\to S)}_{C,t}=\\text{AR}^{(C\\to S)}_{S,t}$\n",
        "**운전자본 사이클:**  $\\text{CCC}=\\text{DIO}+\\text{DSO}-\\text{DPO}$\n",
        "**현금흐름 항등식 (P3,P7):**  $\\text{OCF}=\\text{NI}+\\text{D\\&A}-\\Delta\\text{NWC}$, "
        "$\\ \\Delta\\text{NWC}=\\Delta\\text{Inv}+\\Delta\\text{AR}-\\Delta\\text{AP}$, "
        "$\\ \\text{FCF}=\\text{OCF}-\\text{Capex}$\n",
        "**공적분 제약 (→ VECM):**  $\\log\\text{Rev}_{S,t}=c_S+\\sum_C\\theta_{S,C}\\log\\text{Rev}_{C,t}+u_{S,t}$, "
        "$\\ \\Delta\\log\\text{Rev}_{S,t}=\\alpha_S u_{S,t-1}+\\sum_C\\beta_{S,C}\\Delta\\log\\text{Rev}_{C,t}+\\eta$\n",
    ]
    L.append("\n## 4. 해석\n- support_rate = 예측 부호와 일치하며 유의한 관계 비율. 1.0에 가까울수록 "
             "회계 이론이 데이터로 뒷받침됨.\n- 기업간(P1,P4,P5)은 기업쌍, 기업내(P2,P3,P7)는 동일기업 검정.\n"
             "- 상세 기업쌍/변환은 `universal_channels.csv`, `cashflow_channels_data.csv` 참조.\n")
    L.append("\n## 5. 한계\n- 거래처별 분해(ω) 부재 → 집계 근사. 표본 ~40분기. 상관≠거래(10-K 교차확인).\n")
    Path(path).write_text("\n".join(L))
    return path


def generate_html(df, path, date="2026-07-20"):
    rows = []
    for r in df.itertuples(index=False):
        kind = "기업간" if r.kind == "cross" else "기업내"
        if r.n_tested == 0:
            cell = "<td colspan=1 style='color:#b58900'>데이터부족</td>"
        else:
            bar = int(round((r.support_rate or 0) * 100))
            cell = (f"<td><div class='barwrap'><div class='bar' style='width:{bar}%'></div>"
                    f"<span>{r.support_rate}</span></div></td>")
        rows.append(
            f"<tr><td><b>{r.id}</b></td><td>{kind}</td><td class='lb'>{r.label}</td>"
            f"<td class='bs'>{r.basis}</td><td>{r.exp_lag}</td><td>{r.sign}</td>"
            f"{cell}<td>{r.n_sig}/{r.n_tested}</td><td>{r.mean_lag}</td><td>{r.mean_corr}</td></tr>")
    table = "\n".join(rows)
    html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>회계지표 기업간 Lead-Lag</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
 body{{font-family:-apple-system,'Malgun Gothic',sans-serif;margin:32px;color:#1a1a1a}}
 h1{{font-size:21px}} h2{{font-size:15px;margin-top:22px}} .sub{{color:#666;font-size:13px}}
 .interp{{background:#fff8e1;border-left:4px solid #f0b400;padding:12px 16px;margin:14px 0;font-size:13px;line-height:1.75;border-radius:4px}}
 .interp b{{color:#8a6d00}}
 .mermaid{{background:#fafafa;border:1px solid #eee;border-radius:8px;padding:16px;margin:12px 0}}
 table{{border-collapse:collapse;width:100%;font-size:12.5px}}
 th,td{{border:1px solid #e6e6e6;padding:5px 7px;text-align:center}} th{{background:#f4f4f4}}
 td.lb{{text-align:left;font-weight:600}} td.bs{{text-align:left;color:#555;font-size:11px}}
 .barwrap{{position:relative;background:#eef2f7;border-radius:4px;height:18px;min-width:80px}}
 .bar{{background:#2ca02c;height:18px;border-radius:4px}}
 .barwrap span{{position:absolute;left:6px;top:0;line-height:18px;font-size:11px;color:#123}}
</style></head><body>
<h1>회계지표 기업간 Lead-Lag — 돈의 흐름 (산출물 a)</h1>
<div class="sub">복식부기 항등식에서 연역한 가설 P1–P7의 데이터 검증 · 분석일 {date}</div>
<div class="interp">
📖 <b>이 페이지 읽는 법</b><br>
공급사 매출은 고객의 매입(회계상 <b>거래 항등식</b> Rev_S=Σω·Purch_C)이며, 이는 다시 매출채권→영업현금
→잉여현금으로 이어집니다. 아래 도식이 <b>돈의 회계적 흐름</b>이고, 표의 각 가설 P1–P7이 그 화살표입니다.<br>
• <b>지지율(support_rate)</b> = 예측한 부호·방향과 일치하며 통계적으로 유의한 관계 비율(초록 막대). 1.0=이론 완전 지지.<br>
• <b>예측시차</b>는 회계 근거에서 나온 값, <b>실측 평균시차</b>는 데이터에서 나온 값 — 둘을 대조합니다.<br>
👉 회계 항등식이 데이터로도 성립하는지를 보는, 논문의 핵심 실증 표입니다.
</div>
<h2>회계 흐름 도식</h2>
<div class="mermaid">
{_mermaid_chain()}
</div>
<h2>가설 검증 (P1–P7)</h2>
<table>
<tr><th>#</th><th>유형</th><th>관계</th><th>회계 근거</th><th>예측시차</th><th>부호</th><th>지지율</th><th>유의/검정</th><th>실측시차</th><th>평균 r</th></tr>
{table}
</table>
<script>mermaid.initialize({{startOnLoad:true,flowchart:{{curve:'basis'}}}});</script>
</body></html>"""
    Path(path).write_text(html)
    return path
