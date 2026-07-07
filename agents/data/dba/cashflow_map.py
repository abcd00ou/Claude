"""
cashflow_map.py — 섹터간 현금흐름 lead-lag + 시차 반영 밸류체인 맵.

사용자 정의 고객→공급사 관계(valuechain.RELATIONSHIPS)를 따라, 각 엣지에서 "돈이
고객으로부터 공급사로 흐르는" 시차를 밝힌다. 매출→매출 하나가 아니라 여러 현금흐름
채널을 후보로 두고, 데이터가 가장 유의한 채널을 스스로 고르게 한다:

  구매흐름  고객 COGS_GROWTH_QOQ   → 공급사 REVENUE_GROWTH_QOQ  (고객이 사들이는 돈)
  투자흐름  고객 CAPEX_GROWTH_QOQ  → 공급사 REVENUE_GROWTH_QOQ  (고객 설비투자)
  수요흐름  고객 REVENUE_GROWTH_QOQ→ 공급사 REVENUE_GROWTH_QOQ  (고객 최종수요)

각 엣지의 최적 시차(고객 선행 분기)를 뽑아 mermaid 밸류체인 맵과 MD로 그린다.
제약(섹터 전체 반영 어려움)은 섹터 집계에 커버리지 좋은 기업만 넣는 방식으로 흡수.

reuse: cashflow_leadlag.analyze_cross(섹터 집계 lead-lag) · valuechain(관계·라벨).
"""
from __future__ import annotations
from pathlib import Path

import numpy as np
import pandas as pd

import panel as P
import valuechain as V
import cashflow_leadlag as C

HERE = Path(__file__).parent

# 현금흐름 채널 후보: (X_feat, X_transform, Y_feat, Y_transform, 채널명, 약칭)
# transform 'auto' = 저장된 형태 그대로. 결제/구매/투자/재고/현금여력 × QoQ·YoY.
CASH_DRIVERS = [
    # 결제/지급 흐름 — 고객이 아직 안 낸 돈(AP)이 공급사 매출/미수로
    ("AP_GROWTH_QOQ", "auto", "REVENUE_GROWTH_QOQ", "auto", "결제(QoQ)", "고객AP→공급사매출"),
    ("AP_GROWTH_YOY", "auto", "REVENUE_GROWTH_YOY", "auto", "결제(YoY)", "고객AP→공급사매출"),
    ("DPO", "auto", "DSO", "auto", "지급→회수", "고객DPO→공급사DSO"),
    ("AP_TO_COGS", "auto", "AR_TO_REVENUE", "auto", "미지급→미수", "고객AP/COGS→공급사AR/매출"),
    # 구매 흐름 — 고객 매출원가(구매)
    ("COGS_GROWTH_QOQ", "auto", "REVENUE_GROWTH_QOQ", "auto", "구매(QoQ)", "고객COGS→공급사매출"),
    ("COGS_GROWTH_YOY", "auto", "REVENUE_GROWTH_YOY", "auto", "구매(YoY)", "고객COGS→공급사매출"),
    # 투자 흐름 — 고객 capex
    ("CAPEX_GROWTH_QOQ", "auto", "REVENUE_GROWTH_QOQ", "auto", "투자(QoQ)", "고객capex→공급사매출"),
    ("CAPEX", "growth_yoy", "REVENUE", "growth_yoy", "투자(YoY)", "고객capex→공급사매출"),
    # 재고 흐름 — 고객 재고축적/소진
    ("INVENTORY_GROWTH_QOQ", "auto", "REVENUE_GROWTH_QOQ", "auto", "재고(QoQ)", "고객재고→공급사매출"),
    ("INVENTORY_GROWTH_YOY", "auto", "REVENUE_GROWTH_YOY", "auto", "재고(YoY)", "고객재고→공급사매출"),
    # 현금여력 흐름 — 고객 FCF마진
    ("FCF_MARGIN", "auto", "REVENUE_GROWTH_QOQ", "auto", "현금여력", "고객FCF마진→공급사매출"),
    # 수요 흐름 — 고객 최종 매출
    ("REVENUE_GROWTH_QOQ", "auto", "REVENUE_GROWTH_QOQ", "auto", "수요(QoQ)", "고객매출→공급사매출"),
    ("REVENUE_GROWTH_YOY", "auto", "REVENUE_GROWTH_YOY", "auto", "수요(YoY)", "고객매출→공급사매출"),
]
# 시각화/경로 해석용 주요 현금전파 경로
KEY_PATHS = [
    ["hyperscalers", "ai_chip", "dram"],
    ["hyperscalers", "ai_chip", "nand"],
    ["hyperscalers", "ai_chip", "osat_packaging"],
    ["server_oem", "ai_chip", "dram"],
    ["ai_chip", "dram", "hw_equipment"],
]


# --------------------------------------------------------------------------- #
def _vd(feat, tf):
    return feat if tf == "auto" else f"{feat}[{tf}]"


def _channel(long, cust, supp, xf, xtf, yf, ytf, lags):
    """한 채널의 lead-lag. None if 신호 부족."""
    sx, _ = C.section_feature(long, cust, xf, xtf)
    sy, _ = C.section_feature(long, supp, yf, ytf)
    if sx is None or sy is None:
        return None
    r = C.lead_lag_scan(sx, sy, lags, expected="+")
    return r if r.get("status") == "ok" else None


def edge_cashflow(long, cust, supp, drivers=CASH_DRIVERS, lags=(0, 4)):
    """엣지 하나: 주어진 채널 중 가장 유의한 것을 골라 시차·분석변수를 확정."""
    base = dict(customer=cust, supplier=supp,
                customer_label=V.SECTIONS.get(cust, cust),
                supplier_label=V.SECTIONS.get(supp, supp))
    cand = []
    for xf, xtf, yf, ytf, ch_ko, ch_short in drivers:
        r = _channel(long, cust, supp, xf, xtf, yf, ytf, lags)
        if r:
            r.update(channel=ch_ko, channel_short=ch_short,
                     x_var=_vd(xf, xtf), y_var=_vd(yf, ytf))
            cand.append(r)
    if not cand:
        return {**base, "status": "insufficient data", "note": "데이터 부족"}
    strong = [r for r in cand if r["significant"] and r["sign_match"]]
    pool = strong or cand
    best = max(pool, key=lambda r: abs(r["pearson"]))
    return {**base, "status": "ok", "channel": best["channel"],
            "channel_short": best["channel_short"],
            "x_var": best["x_var"], "y_var": best["y_var"],
            "lag_q": best["best_lag"], "pearson": best["pearson"],
            "p_value": best["p_value"], "granger_p": None, "n": best["n"],
            "significant": bool(best["significant"] and best["sign_match"])}


def run_map(long, relationships=None, channel=None):
    """
    channel=None → 각 엣지 최유의 채널 자동선택.
    channel=(X_feat, Y_feat) → 그 채널만 고정 (예: ('AP_GROWTH_QOQ','REVENUE_GROWTH_QOQ')).
    """
    relationships = relationships or V.RELATIONSHIPS
    drivers = CASH_DRIVERS
    if channel is not None:
        drivers = [d for d in CASH_DRIVERS if (d[0], d[2]) == tuple(channel)]
        if not drivers:                              # 목록에 없는 조합도 허용
            drivers = [(channel[0], "auto", channel[1], "auto", "지정채널",
                        f"{channel[0]}→{channel[1]}")]
    rows = [edge_cashflow(long, c, s, drivers=drivers) for c, s in relationships]
    cols = ["customer_label", "supplier_label", "status", "channel", "channel_short",
            "x_var", "y_var", "lag_q", "pearson", "p_value", "granger_p", "n", "significant"]
    df = pd.DataFrame(rows)
    df["customer"] = [r["customer"] for r in rows]
    df["supplier"] = [r["supplier"] for r in rows]
    return df[[c for c in cols if c in df.columns] + ["customer", "supplier"]]


def scan_all_channels(long, relationships=None, lags=(0, 4)):
    """
    여러 방면 탐색: 모든 엣지 × 모든 채널의 lead-lag를 long 형태로. 사용자가 채널·
    변환·시차를 자유롭게 필터/검토. (자동선택 편향 없이 전 채널을 그대로 보여줌)
    """
    relationships = relationships or V.RELATIONSHIPS
    rows = []
    for c, s in relationships:
        for xf, xtf, yf, ytf, ch_ko, ch_short in CASH_DRIVERS:
            r = _channel(long, c, s, xf, xtf, yf, ytf, lags)
            base = dict(customer=V.SECTIONS.get(c, c), supplier=V.SECTIONS.get(s, s),
                        channel=ch_ko, x_var=_vd(xf, xtf), y_var=_vd(yf, ytf))
            if r is None:
                rows.append({**base, "status": "insufficient data"})
            else:
                rows.append({**base, "status": "ok", "lag_q": r["best_lag"],
                             "pearson": r["pearson"], "spearman": r["spearman"],
                             "p_value": r["p_value"], "n": r["n"],
                             "significant": bool(r["significant"] and r["sign_match"])})
    cols = ["customer", "supplier", "channel", "x_var", "y_var", "status",
            "lag_q", "pearson", "spearman", "p_value", "n", "significant"]
    df = pd.DataFrame(rows)
    return df[[c for c in cols if c in df.columns]]


# --------------------------------------------------------------------------- #
def path_lag(df, path):
    """경로(섹터 리스트)의 누적 시차 = 각 홉 시차 합 (유의 엣지만; 불가시 None)."""
    total, legs = 0, []
    for a, b in zip(path[:-1], path[1:]):
        row = df[(df.customer == a) & (df.supplier == b)]
        if row.empty or row.iloc[0].status != "ok":
            return None, []
        r = row.iloc[0]
        total += int(r.lag_q)
        legs.append(f"{r.customer_label}→{r.supplier_label} {int(r.lag_q):+d}q")
    return total, legs


# --------------------------------------------------------------------------- #
def generate_html(df, path, date="2026-07-07"):
    edges = []
    for i, r in enumerate(df.itertuples(index=False)):
        c, s = _nid(r.customer_label), _nid(r.supplier_label)
        if r.status != "ok":
            edges.append(f'  {c}["{r.customer_label}"] -.->|"데이터부족"| {s}["{r.supplier_label}"]')
            continue
        lbl = f"{r.channel_short} · {int(r.lag_q):+d}q · r={r.pearson}"
        arrow = "==>" if r.significant else "-->"
        edges.append(f'  {c}["{r.customer_label}"] {arrow}|"{lbl}"| {s}["{r.supplier_label}"]')
    mer = "flowchart LR\n" + "\n".join(edges)

    # 시차별 링크 색 (유의 엣지: 0q 빨강 즉각 → 4q 파랑 지연)
    ok = df[df.status == "ok"].reset_index(drop=True)
    lag_color = {0: "#d62728", 1: "#ff7f0e", 2: "#2ca02c", 3: "#1f77b4", 4: "#6a3d9a"}
    styles = []
    for i, r in enumerate(df.itertuples(index=False)):
        if r.status == "ok" and r.significant:
            col = lag_color.get(int(r.lag_q), "#888")
            styles.append(f"linkStyle {i} stroke:{col},stroke-width:3px;")
    style_block = "\n".join(styles)

    rows = []
    for r in df.itertuples(index=False):
        if r.status != "ok":
            rows.append(f"<tr><td>{r.customer_label}</td><td>{r.supplier_label}</td>"
                        f"<td colspan=6 class='na'>데이터 부족</td></tr>")
        else:
            cls = "sig" if r.significant else ""
            rows.append(f"<tr class='{cls}'><td>{r.customer_label}</td><td>{r.supplier_label}</td>"
                        f"<td>{r.channel}</td><td class='var'>{r.x_var} → {r.y_var}</td>"
                        f"<td>{int(r.lag_q):+d}q</td><td>{r.pearson}</td>"
                        f"<td>{r.p_value}</td><td>{'유의' if r.significant else '·'}</td></tr>")
    table = "\n".join(rows)

    # 주요 경로 누적 시차
    paths_html = []
    for pth in KEY_PATHS:
        tot, legs = path_lag(df, pth)
        if tot is not None:
            chain = " → ".join(V.SECTIONS.get(x, x) for x in pth)
            paths_html.append(f"<li><b>{chain}</b> : 누적 <b>{tot}분기</b> "
                              f"<span class='legs'>({' , '.join(legs)})</span></li>")
    paths_html = "\n".join(paths_html) or "<li>유의 경로 없음</li>"

    html = f"""<!doctype html><html lang="ko"><head><meta charset="utf-8">
<title>AI 공급망 현금흐름 시차 맵</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
<style>
 body{{font-family:-apple-system,Segoe UI,'Malgun Gothic',sans-serif;margin:32px;color:#1a1a1a}}
 h1{{font-size:22px}} .sub{{color:#666;margin-bottom:12px}}
 .legend span{{margin-right:14px;font-size:12px}}
 .mermaid{{background:#fafafa;border:1px solid #eee;border-radius:8px;padding:16px;margin:14px 0}}
 table{{border-collapse:collapse;width:100%;font-size:13px;margin-top:12px}}
 th,td{{border:1px solid #e5e5e5;padding:6px 8px;text-align:center}}
 th{{background:#f4f4f4}} tr.sig{{background:#eefbf0}} td.na{{color:#b58900}}
 td.var{{font-family:ui-monospace,Menlo,monospace;font-size:11px;color:#333}}
 ul{{font-size:13px;line-height:1.7}} .legs{{color:#888}}
 h2{{font-size:16px;margin-top:22px}}
</style></head><body>
<h1>AI 공급망 현금흐름 Lead-Lag 시차 맵</h1>
<div class="sub">고객→공급사 현금 전이. 굵은 화살표=유의. 채널은 데이터가 선택(구매/투자/수요흐름). 분석일 {date}</div>
<div class="legend">
 <span>🔴 0q 즉시</span><span>🟠 1q</span><span>🟢 2q</span><span>🔵 3q</span><span>🟣 4q 지연</span>
 <span>⋯ 데이터부족</span>
</div>
<div class="mermaid">
{mer}
{style_block}
</div>
<h2>주요 현금전파 경로 (누적 시차)</h2>
<ul>
{paths_html}
</ul>
<h2>엣지별 현금흐름 시차 (분석 변수 명시)</h2>
<table>
<tr><th>고객</th><th>공급사</th><th>채널</th><th>분석변수 (X→Y)</th><th>시차</th><th>r</th><th>p</th><th>유의</th></tr>
{table}
</table>
<script>mermaid.initialize({{startOnLoad:true,flowchart:{{curve:'basis'}}}});</script>
</body></html>"""
    Path(path).write_text(html)
    return path


def generate_md(df, path, date="2026-07-07"):
    L = ["# AI 공급망 현금흐름 Lead-Lag 시차 분석\n",
         f"**분석일:** {date} · **데이터:** `panel_long` · **엔진:** `cashflow_map.py`\n",
         "고객→공급사 현금 전이 시차. 각 엣지는 구매(COGS→매출)·투자(capex→매출)·"
         "수요(매출→매출) 채널 중 데이터가 가장 유의한 것으로 시차를 확정.\n"]
    ok = df[df.status == "ok"]
    L.append(f"\n- 엣지 {len(df)} · 분석가능 {len(ok)} · **유의 {int(ok.significant.sum())}**\n")
    L.append("\n## 엣지별 현금흐름 시차 (분석 변수 명시)\n")
    L.append("| 고객 | 공급사 | 채널 | 분석변수 (X→Y) | 시차(분기) | r | p | 유의 |")
    L.append("|---|---|---|---|---|---|---|---|")
    for r in df.itertuples(index=False):
        if r.status != "ok":
            L.append(f"| {r.customer_label} | {r.supplier_label} | — | — | — | — | — | 데이터부족 |")
        else:
            star = "**" if r.significant else ""
            L.append(f"| {r.customer_label} | {r.supplier_label} | {r.channel} | "
                     f"`{r.x_var}→{r.y_var}` | {star}{int(r.lag_q):+d}{star} | {r.pearson} | "
                     f"{r.p_value} | {'✅' if r.significant else '·'} |")
    L.append("\n## 주요 현금전파 경로 (누적 시차)\n")
    for pth in KEY_PATHS:
        tot, legs = path_lag(df, pth)
        chain = " → ".join(V.SECTIONS.get(x, x) for x in pth)
        L.append(f"- **{chain}**: " + (f"누적 **{tot}분기** ({', '.join(legs)})" if tot is not None
                                       else "경로 일부 데이터 부족"))
    L.append("\n## 해석·한계\n")
    L.append("- 시차 = 고객 활동이 공급사 매출을 선행하는 분기 수 (양수=고객 선행).\n")
    L.append("- 채널은 데이터가 선택: 구매(COGS)·투자(capex)·수요(매출) 중 최유의.\n")
    L.append("- 섹터 집계는 커버리지 좋은 기업만 포함(전체 반영 대신 강한 관계 중심).\n")
    L.append("- Foundry·Server ODM은 데이터 부족으로 다수 엣지 분석 불가.\n")
    Path(path).write_text("\n".join(L))
    return path


def _nid(label):
    return "n_" + label.replace(" ", "").replace("/", "").replace("-", "")


def generate_channels_report(long, path, date="2026-07-08"):
    """여러 방면 스캔 리포트: 채널×엣지 전체, 채널별 요약, 시차>0 선행 관계."""
    df = scan_all_channels(long)
    df.to_csv(str(Path(path).with_suffix("")) + "_data.csv", index=False)
    ok = df[df.status == "ok"]
    sig = ok[ok.significant]
    L = ["# 현금흐름 Lead-Lag — 채널 전체 스캔 (여러 방면)\n",
         f"**분석일:** {date} · **데이터:** `panel_long` · **엔진:** `cashflow_map.py`\n",
         f"고객→공급사 {df[['customer','supplier']].drop_duplicates().shape[0]}개 엣지 × "
         f"{df.channel.nunique()}개 현금흐름 채널(결제/구매/투자/재고/현금여력/수요, QoQ·YoY) "
         f"= {len(df)} 조합. 분석가능 {len(ok)} · **유의 {len(sig)}**.\n",
         "\n> ⚠️ 다중비교: 채널을 많이 시도하면 우연 유의가 늘어난다. 경제적 방향과 "
         "시차 안정성, YoY/QoQ 교차확인을 함께 볼 것.\n"]

    L.append("\n## 1. 채널별 요약 (유의 엣지 수 · 평균시차 · 평균 r)\n")
    L.append("| 채널 | 유의 엣지 | 평균 시차(분기) | 평균 r |")
    L.append("|---|---|---|---|")
    g = (sig.groupby("channel")
            .agg(n=("significant", "size"), lag=("lag_q", "mean"), r=("pearson", "mean"))
            .round(2).sort_values("n", ascending=False))
    for ch, row in g.iterrows():
        L.append(f"| {ch} | {int(row.n)} | {row.lag} | {row.r} |")

    L.append("\n## 2. 시차>0 (고객이 실제로 선행하는) 유의 관계\n")
    L.append("| 고객 | 공급사 | 채널 | 분석변수 (X→Y) | 시차 | r | p |")
    L.append("|---|---|---|---|---|---|---|")
    lead = sig[sig.lag_q > 0].sort_values("lag_q", ascending=False)
    for r in lead.itertuples(index=False):
        L.append(f"| {r.customer} | {r.supplier} | {r.channel} | `{r.x_var}→{r.y_var}` | "
                 f"{int(r.lag_q)}q | {r.pearson} | {r.p_value} |")

    L.append("\n## 3. 채널 정의\n")
    L.append("| 채널 | X (고객) | Y (공급사) | 의미 |")
    L.append("|---|---|---|---|")
    meaning = {"결제": "고객이 아직 안 낸 돈(AP)이 공급사 매출/미수로",
               "지급→회수": "고객 지급기간이 공급사 회수기간으로 전이",
               "미지급→미수": "고객 미지급 부담이 공급사 미수 부담으로",
               "구매": "고객 매출원가(구매)가 공급사 매출로",
               "투자": "고객 capex가 공급사 매출로",
               "재고": "고객 재고 축적/소진이 공급사 주문으로",
               "현금여력": "고객 FCF마진(현금여력)이 공급사 매출로",
               "수요": "고객 최종 매출이 공급사 매출로"}
    seen = set()
    for xf, xtf, yf, ytf, ch, sh in CASH_DRIVERS:
        key = ch.split("(")[0]
        note = meaning.get(key, "")
        L.append(f"| {ch} | `{_vd(xf,xtf)}` | `{_vd(yf,ytf)}` | {note} |")

    L.append("\n## 4. 해석 메모 (직접 작성)\n> \n- \n")
    L.append("\n## 5. 한계\n- QoQ는 단기·즉시전이, YoY는 계절제거·구조시차 포착(문서 §6).\n"
             "- 전체 조합 데이터는 동봉 CSV 참조. Foundry·ODM은 데이터 부족.\n")
    Path(path).write_text("\n".join(L))
    return path
