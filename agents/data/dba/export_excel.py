"""
export_excel.py — 모든 분석의 시작점인 panel_long 데이터프레임을 엑셀로 내보낸다.

지금의 모든 lead-lag / 밸류체인 / 현금흐름 / ECM 분석은 예외 없이
`panel.load_long()` 으로 panel_long 을 불러오는 데서 시작한다. 이 스크립트는
그 원본 데이터프레임(+검토 편의용 요약/피벗)을 하나의 .xlsx 로 저장한다.

시트 구성:
  README        이 파일과 각 시트 설명
  panel_long    원본 롱포맷 (분석의 진짜 시작점) — ticker·companyname·date·item·value·section
  item_catalog  item 목록·의미·행수
  coverage      기업 × item 커버리지(분기 수)
  revenue_wide  검토용 피벗 예시 (기업 × 분기, revenue)

Run:  python3 export_excel.py [YYYY-MM-DD]
"""
from __future__ import annotations
import sys
from pathlib import Path

import pandas as pd

import panel as P
import features as F

HERE = Path(__file__).parent
DATE = sys.argv[1] if len(sys.argv) > 1 else "2026-07-07"

# 원천 item 설명 (파생은 features.FEATURE_REGISTRY 에서 자동)
SOURCE_DESC = {
    "revenue": "매출 (원천)", "revenue_ai_dc": "AI/DC 매출 (원천, 일부)",
    "revenue_yoy": "매출 YoY% (원천, 일부)", "gross_profit": "매출총이익 (원천)",
    "gross_margin": "매출총이익률% (원천)", "operating_income": "영업이익 (원천)",
    "net_income": "순이익 (원천)", "eps": "희석 EPS (원천)", "cash": "현금성자산 (원천)",
    "capex": "설비투자 (원천)", "fcf": "잉여현금흐름 (원천)",
    "operating_cash_flow": "영업활동현금흐름 (원천)", "inventory": "재고 (원천)",
    "receivables": "매출채권 (원천)", "accounts_payable": "매입채무 (원천, EDGAR 백필)",
    "total_assets": "총자산 (원천)", "total_debt": "총부채 (원천)",
    "stockholders_equity": "자기자본 (원천)", "stock_price": "분기말 주가 (원천, as-of)",
}
# 원천 + 파생(가이드 문서 변수) 전체 설명
ITEM_DESC = {**SOURCE_DESC,
             **{k: f"{v['desc']} (파생)" for k, v in F.FEATURE_REGISTRY.items()
                if k in P.FEATURE_ITEMS}}


def qkey(s):
    y, q = s.split("-Q"); return int(y) * 4 + int(q)


def main():
    long = P.load_long(P.DB_DEFAULT)
    long = long.sort_values(["section", "ticker", "item", "date"]).reset_index(drop=True)
    out = HERE / f"panel_long_dataset_{DATE}.xlsx"

    # README
    readme = pd.DataFrame({
        "항목": ["파일 목적", "분석 시작점", "생성일", "행 수", "기업 수", "item 수", "기간",
               "", "시트: panel_long", "시트: item_catalog", "시트: coverage", "시트: revenue_wide"],
        "설명": [
            "지금의 모든 분석(lead-lag/밸류체인/현금흐름/ECM)이 사용하는 원본 데이터",
            "panel.load_long() → 이 panel_long 데이터프레임에서 모든 분석이 시작됨",
            DATE, f"{len(long):,}", f"{long.ticker.nunique()}", f"{long.item.nunique()}",
            f"{long.date.min()} ~ {long.date.max()}",
            "",
            "원본 롱포맷 (ticker·companyname·date·item·value·section)",
            "item 목록·의미·행수",
            "기업 × item 커버리지(분기 수) — 데이터 충분성 확인용",
            "검토용 피벗 예시 (기업 × 분기, revenue). 다른 item은 필요시 panel.to_wide()",
        ]})

    # item catalog
    cnt = long.groupby("item")["value"].size()
    catalog = pd.DataFrame({
        "item": list(ITEM_DESC),
        "설명": [ITEM_DESC[i] for i in ITEM_DESC],
        "행수": [int(cnt.get(i, 0)) for i in ITEM_DESC],
    }).sort_values("행수", ascending=False)

    # coverage: 기업 × item 분기 수
    cov = (long.pivot_table(index=["section", "ticker", "companyname"],
                            columns="item", values="date", aggfunc="nunique")
               .fillna(0).astype(int).reset_index())

    # wide 예시 (기업 × 분기): 원천 revenue + 파생 CCC
    def _wide(item):
        d = P.to_wide(item)
        return d.loc[sorted(d.index, key=qkey)].round(2).reset_index().rename(columns={"index": "quarter"})
    rev, ccc = _wide("revenue"), _wide("CCC")

    with pd.ExcelWriter(out, engine="openpyxl") as w:
        readme.to_excel(w, sheet_name="README", index=False)
        long.to_excel(w, sheet_name="panel_long", index=False)
        catalog.to_excel(w, sheet_name="item_catalog", index=False)
        cov.to_excel(w, sheet_name="coverage", index=False)
        rev.to_excel(w, sheet_name="revenue_wide", index=False)
        ccc.to_excel(w, sheet_name="CCC_wide", index=False)
        # 열 너비 살짝 정리
        for sh, widths in {"README": [16, 70], "panel_long": [10, 26, 12, 20, 16, 16],
                           "item_catalog": [22, 30, 8]}.items():
            ws = w.sheets[sh]
            for i, wd in enumerate(widths, 1):
                ws.column_dimensions[chr(64 + i)].width = wd

    print(f"[written] {out.name}  ({len(long):,} rows, {long.ticker.nunique()} companies, "
          f"{long.item.nunique()} items)")
    return out


if __name__ == "__main__":
    main()
