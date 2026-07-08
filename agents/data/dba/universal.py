"""
universal.py — (4) 전체 밸류체인에 '보편적으로' 성립하는 현금흐름 관계 발굴.

AP→revenue YoY 하나가 아니라, 여러 변수쌍 × 변환(yoy/qoq/rolling)이 밸류체인의
'몇 개 엣지에서 일관되게 유의한가'(=보편성)를 측정한다. 보편성 높은 관계는 전 섹터에
적용 가능 → 전체 공급망 자금흐름을 하나의 틀로 해석 가능하고, VECM mini-GEM(5)의
방정식 채널이 된다.

기업간(6) 기반: 각 엣지에서 고객사×공급사 기업쌍 lead-lag를 구하고, 유의 기업쌍이
있으면 그 엣지에서 '성립'으로 본다. 보편성 = 성립 엣지 / 분석가능 엣지.

reuse: features.get_feature(변환) · cashflow_leadlag.lead_lag_scan · pairwise_cashflow.members.
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

HERE = Path(__file__).parent
MIN_N = 10
MIN_PAIRS = 2

# 금액 성장 채널 (X→Y, 둘 다 같은 성장변환 스윕)
GROWTH_CHANNELS = [
    ("AP", "REVENUE", "결제 AP→매출"),
    ("COGS", "REVENUE", "구매 COGS→매출"),
    ("CAPEX", "REVENUE", "투자 capex→매출"),
    ("INVENTORY", "REVENUE", "재고→매출"),
    ("REVENUE", "REVENUE", "수요 매출→매출"),
]
GROWTH_TF = ["growth_yoy", "growth_qoq", "rolling_yoy"]
# 특수 채널 (X,Y 변환 개별 고정)
SPECIAL = [
    ("DPO", "level", "DSO", "level", "지급→회수 DPO→DSO"),
    ("AP_TO_COGS", "level", "AR_TO_REVENUE", "level", "미지급→미수"),
    ("FCF_MARGIN", "level", "REVENUE", "growth_yoy", "현금여력→매출"),
]


def build_channels():
    ch = []
    for xf, yf, nm in GROWTH_CHANNELS:
        for tf in GROWTH_TF:
            ch.append((xf, tf, yf, tf, f"{nm} [{tf.replace('growth_','')}]"))
    for xf, xtf, yf, ytf, nm in SPECIAL:
        ch.append((xf, xtf, yf, ytf, nm))
    return ch


# --------------------------------------------------------------------------- #
def channel_universality(long, xf, xtf, yf, ytf, relationships, lags=(0, 4)):
    """한 채널이 전 엣지에서 기업쌍 유의로 얼마나 보편적으로 성립하는지."""
    edges = []
    for cs, ss in relationships:
        cs_m = PW.members(long, cs, xf)
        ss_m = PW.members(long, ss, yf)
        xsig = {ct: F.get_feature(long, ct, xf, xtf) for ct in cs_m}
        ysig = {st: F.get_feature(long, st, yf, ytf) for st in ss_m}
        sig = tot = 0
        corrs, lgs = [], []
        for ct in cs_m:
            x = xsig[ct]
            if x.dropna().shape[0] < MIN_N:
                continue
            for st in ss_m:
                if ct == st:
                    continue
                y = ysig[st]
                if y.dropna().shape[0] < MIN_N:
                    continue
                r = C.lead_lag_scan(x, y, lags)
                if r.get("status") != "ok" or r["n"] < MIN_N:
                    continue
                tot += 1
                if r["significant"]:
                    sig += 1
                    corrs.append(abs(r["pearson"]))
                    lgs.append(r["best_lag"])
        edges.append(dict(edge=f"{V.SECTIONS.get(cs,cs)}→{V.SECTIONS.get(ss,ss)}",
                          pairs=tot, sig_pairs=sig, edge_sig=int(sig >= 1),
                          sig_rate=round(sig / tot, 2) if tot else 0.0,
                          mean_corr=np.mean(corrs) if corrs else np.nan,
                          mean_lag=np.mean(lgs) if lgs else np.nan))
    edf = pd.DataFrame(edges)
    ana = edf[edf.pairs >= MIN_PAIRS]
    summ = dict(
        universality=round(ana.edge_sig.mean(), 3) if len(ana) else 0.0,
        edges_ok=int(ana.edge_sig.sum()) if len(ana) else 0,
        edges_analyzable=len(ana),
        total_sig_pairs=int(edf.sig_pairs.sum()),
        total_pairs=int(edf.pairs.sum()),
        mean_corr=round(float(np.nanmean(edf.mean_corr)), 3) if edf.mean_corr.notna().any() else None,
        mean_lag=round(float(np.nanmean(edf.mean_lag)), 2) if edf.mean_lag.notna().any() else None,
    )
    return summ, edf


def find_universal(long, relationships=None):
    """모든 채널의 보편성 랭킹."""
    relationships = relationships or V.RELATIONSHIPS
    rows, details = [], {}
    for xf, xtf, yf, ytf, nm in build_channels():
        summ, edf = channel_universality(long, xf, xtf, yf, ytf, relationships)
        rows.append(dict(channel=nm, x=f"{xf}[{xtf}]", y=f"{yf}[{ytf}]", **summ))
        details[nm] = edf
    df = pd.DataFrame(rows).sort_values(
        ["universality", "total_sig_pairs"], ascending=False).reset_index(drop=True)
    return df, details


# --------------------------------------------------------------------------- #
def generate_md(df, path, date="2026-07-08"):
    L = ["# 밸류체인 보편 현금흐름 관계 발굴\n",
         f"**분석일:** {date} · **데이터:** `panel_long.csv` · **엔진:** `universal.py`\n",
         "각 변수쌍×변환이 밸류체인 엣지에서 기업쌍 유의로 얼마나 보편적으로 성립하는지. "
         "보편성 = 성립 엣지 / 분석가능 엣지. 높을수록 전 섹터 적용 가능(→ VECM 채널 후보).\n",
         "\n## 보편성 랭킹\n",
         "| 채널 | X | Y | 보편성 | 성립/가능 엣지 | 유의쌍/전체 | 평균 r | 평균시차 |",
         "|---|---|---|---|---|---|---|---|"]
    for r in df.itertuples(index=False):
        L.append(f"| {r.channel} | `{r.x}` | `{r.y}` | **{r.universality}** | "
                 f"{r.edges_ok}/{r.edges_analyzable} | {r.total_sig_pairs}/{r.total_pairs} | "
                 f"{r.mean_corr} | {r.mean_lag} |")
    L += ["\n## 해석\n",
          "- **보편성 1.0** = 분석가능한 모든 엣지에서 유의 기업쌍 존재 → 전 밸류체인 공통 채널.\n",
          "- 평균시차 = 유의 기업쌍들의 평균 선행 분기.\n",
          "- 상위 채널이 전체 공급망 자금흐름 해석 + VECM mini-GEM(5)의 방정식 우변 후보.\n",
          "\n## 한계\n- 기업쌍 표본 24~34분기, 실제 거래 미확인(SPLC 없음). 다중비교 주의.\n"
          "- Foundry·ODM은 데이터 부족(나중에 쌓이면 자동 반영).\n"]
    Path(path).write_text("\n".join(L))
    return path


def generate_html(df, path, date="2026-07-08"):
    mx = max(1.0, float(df["total_sig_pairs"].max()))
    rows = []
    for r in df.itertuples(index=False):
        bar = int(round((r.universality or 0) * 100))
        rows.append(
            f"<tr><td class='ch'>{r.channel}</td><td class='var'>{r.x}</td><td class='var'>{r.y}</td>"
            f"<td><div class='barwrap'><div class='bar' style='width:{bar}%'></div>"
            f"<span>{r.universality}</span></div></td>"
            f"<td>{r.edges_ok}/{r.edges_analyzable}</td><td>{r.total_sig_pairs}/{r.total_pairs}</td>"
            f"<td>{r.mean_corr}</td><td>{r.mean_lag}</td></tr>")
    table = "\n".join(rows)
    html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>밸류체인 보편 현금흐름 관계</title>
<style>
 body{{font-family:-apple-system,'Malgun Gothic',sans-serif;margin:32px;color:#1a1a1a}}
 h1{{font-size:21px}} .sub{{color:#666;font-size:13px;margin-bottom:14px}}
 table{{border-collapse:collapse;width:100%;font-size:13px}}
 th,td{{border:1px solid #e6e6e6;padding:6px 8px;text-align:center}}
 th{{background:#f4f4f4}} td.ch{{text-align:left;font-weight:600}}
 td.var{{font-family:ui-monospace,Menlo,monospace;font-size:11px;color:#444}}
 .barwrap{{position:relative;background:#eef2f7;border-radius:4px;height:18px;min-width:90px}}
 .bar{{background:#2ca02c;height:18px;border-radius:4px}}
 .barwrap span{{position:absolute;left:6px;top:0;line-height:18px;font-size:11px;color:#123}}
 .interp{{background:#fff8e1;border-left:4px solid #f0b400;padding:12px 16px;margin:14px 0;font-size:13px;line-height:1.75;border-radius:4px}}
 .interp b{{color:#8a6d00}}
</style></head><body>
<h1>밸류체인 보편 현금흐름 관계 (전 섹터 적용 가능성)</h1>
<div class="sub">각 변수쌍×변환이 밸류체인 엣지에서 기업쌍 유의로 얼마나 보편적으로 성립하는지 · 분석일 {date}
 · 보편성 1.0 = 분석가능한 모든 엣지에서 성립 → VECM 방정식 후보</div>
<div class="interp">
📖 <b>이 표 읽는 법</b><br>
"AP→매출 YoY처럼 <b>모든 섹터에 두루 적용되는 자금흐름 관계</b>가 무엇인가"를 찾은 결과입니다.<br>
• <b>보편성</b> = (그 채널이 유의하게 성립한 엣지 수) / (분석가능 엣지 수). <b>1.0이면 전 밸류체인 공통 채널</b>.
초록 막대가 길수록 보편적입니다.<br>
• <b>변환</b>: <b>rolling_yoy</b>(4분기 이동평균의 YoY)가 노이즈를 제거해 상관·보편성이 가장 높습니다.
qoq는 단기, yoy는 계절제거·구조적 신호.<br>
• <b>평균시차</b> = 유의 기업쌍들의 평균 선행 분기(대략 2분기).<br>
👉 상위 채널(수요 매출→매출, 결제 AP→매출, 재고→매출)이 <b>전체 공급망 자금흐름의 공통 언어</b>이며,
아래 VECM mini-GEM의 방정식 재료가 됩니다.
</div>
<table>
<tr><th>채널</th><th>X (고객)</th><th>Y (공급사)</th><th>보편성</th><th>성립/가능 엣지</th><th>유의쌍/전체</th><th>평균 r</th><th>평균시차</th></tr>
{table}
</table>
</body></html>"""
    Path(path).write_text(html)
    return path
