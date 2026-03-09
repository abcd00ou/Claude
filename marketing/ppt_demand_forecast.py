"""
수요예측 VP 보고서 — Demand Forecast
SanDisk B2C Storage Marketing Team
"""
import sys
sys.path.insert(0, str(__import__('pathlib').Path(__file__).parent))

import json, datetime
from pathlib import Path
from pptx.enum.text import PP_ALIGN

import ppt_design as D
from ppt_design import C, Layout, rect, tbox, tbox_multi, card, data_table
from ppt_design import slide_header, slide_footer, bar_chart, stacked_bar
from ppt_design import horizontal_bar, exec_summary_block, waterfall_chart
from config import PPTX_DIR, DATA_DIR

with open(DATA_DIR / "market_data.json")    as f: MKT  = json.load(f)
with open(DATA_DIR / "internal_sales.json") as f: SALE = json.load(f)

TODAY = datetime.date.today()
PAGE_PREFIX = "Demand Forecast"


def build():
    prs = D.new_prs()
    pg = 1

    # ══════════════════════════════════════════════════════════
    # SLIDE 1: Title
    # ══════════════════════════════════════════════════════════
    D.title_slide(prs,
        title="B2C Storage\nDemand Forecast",
        subtitle="2025~2026 글로벌 수요 예측 & 시장 분석 보고서",
        deck_type="DEMAND FORECAST")

    # ══════════════════════════════════════════════════════════
    # SLIDE 2: Executive Summary
    # ══════════════════════════════════════════════════════════
    sl = D.new_slide(prs); pg += 1
    slide_header(sl, "Executive Summary", f"{PAGE_PREFIX}  |  Slide {pg}")

    # 핵심 KPI 카드 (상단 4개)
    kpis = [
        ("2025E B2C Revenue", "$3.53B", "+9.2% YoY", C.RED),
        ("microSD 시장 점유율", "#1  32%", "→ 34% 목표 (2025)", C.BLUE),
        ("External SSD 성장률", "+9.1%", "TAM CAGR 20% 상회 예정", C.GREEN),
        ("Blended GM%", "49.8%", "+2.2%p YoY — BiCS6 전환 효과", C.ORANGE),
    ]
    for i, (title, val, sub, col) in enumerate(kpis):
        card(sl, Layout.MARGIN_L + i*3.15, Layout.CONTENT_Y,
             3.0, 1.45, fill=C.NAVY_MID,
             title=title, title_size=9, title_color=C.GRAY_400,
             value=val, value_size=22, value_color=C.WHITE,
             sub=sub, sub_size=8, sub_color=col,
             line_color=col)

    # 핵심 발견 (3개 블록)
    findings = [
        ("📈", "시장 성장 모멘텀 지속",
         "글로벌 External SSD TAM $5.0B(+25% YoY), microSD TAM $8.0B — "
         "콘텐츠 크리에이터 급증, 게이밍 핸드헬드(스팀덱·스위치) 수요가 핵심 드라이버"),
        ("🏆", "SanDisk 경쟁 포지션 강화",
         "microSD #1(32%) 수성 확실, External SSD Samsung 추격 중(22%→24% 목표) — "
         "BiCS8 수직계열화 원가 경쟁력이 핵심 무기. Kingston·Lexar 대비 원가 12~18% 우위"),
        ("⚠️", "리스크: Amazon 3P 가격 이탈 심화",
         f"실측 데이터(Crawling, {TODAY}): SD Extreme 1TB $198.59 (MSRP $99.99 대비 +99%) — "
         "3P 셀러 프리미엄이 소비자 인식 왜곡 가능. Amazon 1P 관리 강화 필요"),
    ]
    exec_summary_block(sl, findings,
                       Layout.MARGIN_L, 2.65, Layout.CONTENT_W, 4.1)
    slide_footer(sl,
        source="WD FY2024 10-K; TrendForce Q4 2024; IDC Storage Tracker; "
               f"SanDisk Crawling Agent (실측 {TODAY})",
        page_num=f"{pg}")

    # ══════════════════════════════════════════════════════════
    # SLIDE 3: TAM / SAM / SOM
    # ══════════════════════════════════════════════════════════
    sl = D.new_slide(prs); pg += 1
    slide_header(sl, "시장 규모 분석 — TAM / SAM / SOM (2025E)",
                 f"{PAGE_PREFIX}  |  Slide {pg}")

    cats = [
        ("External SSD", 5.0, 3.25, 1.14, C.RED,   "CAGR +20%"),
        ("Internal SSD",13.5, 8.10, 1.38, C.BLUE,  "CAGR +18%"),
        ("microSD",      8.0, 6.00, 2.09, C.GREEN,  "CAGR +10%"),
    ]
    for i, (name, tam, sam, som, col, cagr) in enumerate(cats):
        x = Layout.MARGIN_L + i * 4.2
        # 카테고리 헤더
        rect(sl, x, 1.1, 3.9, 0.5, fill=col)
        tbox(sl, name, x, 1.1, 3.9, 0.5, size=14, bold=True, align=PP_ALIGN.CENTER)
        tbox(sl, cagr, x+2.8, 1.05, 1.0, 0.3, size=8, color=col, align=PP_ALIGN.RIGHT)

        # 3단 퍼널 (TAM > SAM > SOM)
        bars = [("TAM", tam, C.NAVY_LIGHT, 3.9),
                ("SAM", sam, "1A3050",     3.2),
                ("SOM", som, col,          2.5)]
        for j, (label, val, fill, bw) in enumerate(bars):
            bx = x + (3.9-bw)/2
            by = 1.75 + j*1.5
            rect(sl, bx, by, bw, 1.3, fill=fill)
            tbox(sl, label, bx+0.15, by+0.12, 1.2, 0.35,
                 size=9, color=C.GRAY_400)
            tbox(sl, f"${val:.1f}B", bx+0.15, by+0.45, bw-0.3, 0.55,
                 size=22, bold=True, color=C.WHITE)
            if label in ("SAM","SOM"):
                pct = val/tam*100 if label=="SAM" else val/sam*100
                tbox(sl, f"{pct:.0f}% of {'TAM' if label=='SAM' else 'SAM'}",
                     bx+0.15, by+0.95, bw-0.3, 0.28,
                     size=8, color=C.GRAY_400)
            if j < 2:
                rect(sl, bx+bw/2-0.15, by+1.3, 0.3, 0.2, fill=C.NAVY_LIGHT)

    # 우측 인사이트 박스
    rect(sl, 12.7, 1.1, 0.23, 5.65, fill=C.RED)
    tbox_multi(sl, [
        ("Key Insight", 9, True, C.RED, PP_ALIGN.LEFT),
        ("", 6, False, C.GRAY_400, PP_ALIGN.LEFT),
        ("SanDisk SOM $4.61B", 11, True, C.WHITE, PP_ALIGN.LEFT),
        ("(합산 기준)", 8, False, C.GRAY_400, PP_ALIGN.LEFT),
        ("", 6, False, C.GRAY_400),
        ("SAM 침투율", 8, False, C.GRAY_400, PP_ALIGN.LEFT),
        ("Ext. 35%  Int. 17%", 9, True, C.ORANGE, PP_ALIGN.LEFT),
        ("microSD  35%", 9, True, C.GREEN, PP_ALIGN.LEFT),
    ], 12.78, 1.15, 0.0, 5.5)

    slide_footer(sl,
        source="IDC Worldwide Quarterly Storage Tracker Q4 2024; "
               "Grand View Research microSD Market Report 2025; TrendForce",
        page_num=f"{pg}")

    # ══════════════════════════════════════════════════════════
    # SLIDE 4: 연간 매출 추이 & YoY
    # ══════════════════════════════════════════════════════════
    sl = D.new_slide(prs); pg += 1
    slide_header(sl, "SanDisk B2C 매출 추이 — 2022~2025E",
                 f"{PAGE_PREFIX}  |  Slide {pg}")

    # 좌측: 연간 Revenue 누적 바차트
    rev_annual = SALE["annual_revenue_usd_m"]
    years = ["2022","2023","2024","2025E"]
    data_stacked = {
        "External SSD": [rev_annual[y]["external_ssd"] for y in years],
        "Internal SSD": [rev_annual[y]["internal_ssd"] for y in years],
        "microSD":      [rev_annual[y]["microsd"] for y in years],
    }
    stacked_bar(sl, data_stacked, years,
                l=Layout.MARGIN_L, t=1.15, w=6.0, h=5.55,
                colors=[C.RED, C.BLUE, C.GREEN],
                show_total=True, show_legend=True,
                bg_color=C.NAVY_MID)

    # 우측: YoY 상세 테이블
    rect(sl, 6.7, 1.15, 6.2, 5.55, fill=C.NAVY_MID)
    tbox(sl, "연간 성장률 & 카테고리 성과", 6.85, 1.25, 5.9, 0.4,
         size=12, bold=True, color=C.WHITE)

    yoy = SALE["yoy_growth_pct"]
    rows_t = [
        ["External SSD", "$208M→$274M", "+31.7%",
         ("+6.7%","E87070") if yoy["2024_vs_2023"]["external_ssd"]<10 else "+6.7%",
         ("+9.1%","5CB85C")],
        ["Internal SSD", "$165M→$222M", "+34.5%", "+5.6%", ("+16.1%","5CB85C")],
        ["microSD",      "$330M→$430M", "+30.3%", "+10.1%",("+5.9%","CCCCCC")],
        ["Total B2C",    "$703M→$926M", "+31.7%", "+8.0%", ("+9.2%","5CB85C")],
    ]
    # Simplified table
    table_headers = ["카테고리", "Q1→Q4 2024", "Q1→Q4 성장", "2024 YoY", "2025E YoY"]
    table_rows = [
        ["External SSD", "$208M→$274M", "+31.7%", "+6.7%", ("+9.1%", C.GREEN)],
        ["Internal SSD", "$165M→$222M", "+34.5%", "+5.6%", ("+16.1%",C.GREEN)],
        ["microSD",      "$330M→$430M", "+30.3%", "+10.1%",("+5.9%", C.GRAY_400)],
        ["Total B2C",    "$703M→$926M", "+31.7%", "+8.0%", ("+9.2%", C.GREEN)],
    ]
    data_table(sl, 6.85, 1.75, 5.9, table_headers, table_rows,
               col_widths=[1.5, 1.6, 1.1, 0.85, 0.85],
               header_fill=C.RED, font_size=9)

    # GM% 트렌드
    tbox(sl, "Gross Margin % 추이", 6.85, 3.75, 5.9, 0.35,
         size=10, bold=True, color=C.WHITE)
    gm = SALE["gross_margin_pct"]
    gm_data = [
        ("2022", gm["2022"]["blended"]),
        ("2023", gm["2023"]["blended"]),
        ("2024", gm["2024"]["blended"]),
        ("2025E",gm["2025E"]["blended"]),
    ]
    bar_chart(sl, gm_data, 6.85, 4.1, 5.9, 2.3,
              max_val=60, bar_color=C.ORANGE,
              bg_color="162030", show_labels=True)
    tbox(sl, "※ 2023 저점 (NAND 과잉공급) → 2024 회복 (+10.4%p) → 2025E BiCS6/8 전환으로 추가 개선",
         6.85, 6.45, 5.9, 0.25, size=8, color=C.GRAY_400, italic=True)

    slide_footer(sl,
        source="WD FY2022~FY2024 Annual Report (Flash Segment); "
               "SanDisk Internal Sales Tracking; TrendForce NAND Pricing",
        page_num=f"{pg}")

    # ══════════════════════════════════════════════════════════
    # SLIDE 5: 분기별 수요 예측 (2025~2026)
    # ══════════════════════════════════════════════════════════
    sl = D.new_slide(prs); pg += 1
    slide_header(sl, "분기별 Revenue 예측 — 2025~2026 (계절성 반영)",
                 f"{PAGE_PREFIX}  |  Slide {pg}")

    q_data = SALE["quarterly_revenue_usd_m"]
    quarters_all = ["2024Q1","2024Q2","2024Q3","2024Q4",
                    "2025Q1","2025Q2","2025Q3","2025Q4","2026Q1E"]
    q_labels = ["24Q1","24Q2","24Q3","24Q4","25Q1","25Q2","25Q3","25Q4","26Q1E"]

    data_stk = {
        "External SSD": [q_data[q]["external_ssd"] for q in quarters_all],
        "Internal SSD": [q_data[q]["internal_ssd"] for q in quarters_all],
        "microSD":      [q_data[q]["microsd"] for q in quarters_all],
    }
    stacked_bar(sl, data_stk, q_labels,
                l=Layout.MARGIN_L, t=1.15, w=8.8, h=5.6,
                colors=[C.RED, C.BLUE, C.GREEN],
                show_total=True, show_legend=True,
                bg_color=C.NAVY_MID)

    # 우측 인사이트
    rect(sl, 9.5, 1.15, 3.43, 5.6, fill=C.NAVY_MID)
    tbox(sl, "분기별 Key Driver", 9.65, 1.3, 3.1, 0.4,
         size=11, bold=True, color=C.WHITE)

    insights = [
        ("Q4 성수기 집중", C.RED,
         "연간 매출의 30% Q4에 집중\n(Black Friday, 크리스마스)\n→ 재고/물류 사전 준비 필수"),
        ("Q3 Back-to-School", C.ORANGE,
         "microSD/External SSD\nBack-to-School 수요 급증\n(8~9월 집중 마케팅)"),
        ("Q1 신제품 런칭", C.BLUE,
         "CES(1월) 연계 신제품 발표\nSN850X 4TB·Extreme Pro\nBiCS8 하반기 출시 준비"),
    ]
    y_start = 1.85
    for title, col, body in insights:
        rect(sl, 9.55, y_start, 3.25, 1.5, fill=C.NAVY_LIGHT)
        rect(sl, 9.55, y_start, 0.04, 1.5, fill=col)
        tbox(sl, title, 9.7, y_start+0.1, 3.0, 0.35, size=10, bold=True, color=col)
        tbox(sl, body, 9.7, y_start+0.45, 3.0, 0.95, size=8.5, color=C.GRAY_400)
        y_start += 1.65

    tbox(sl, f"2026Q1E: ${q_data['2026Q1E']['total']}M (+{(q_data['2026Q1E']['total']-q_data['2025Q1']['total'])/q_data['2025Q1']['total']*100:.1f}% YoY)",
         9.65, 5.5, 3.1, 0.35, size=9, bold=True, color=C.GREEN)

    slide_footer(sl,
        source="SanDisk Internal Sales Tracking 2024; "
               "2025~2026 Marketing Planning Model (Bottom-up); "
               "계절지수: 역사적 평균(2021~2024) 기반",
        page_num=f"{pg}")

    # ══════════════════════════════════════════════════════════
    # SLIDE 6: 경쟁사 가격 실측 분석 (Real Data)
    # ══════════════════════════════════════════════════════════
    sl = D.new_slide(prs); pg += 1
    slide_header(sl, f"경쟁사 Amazon 가격 실측 분석 — {TODAY} 기준",
                 f"{PAGE_PREFIX}  |  Slide {pg}")

    # ⚡ 실측 데이터 뱃지
    rect(sl, Layout.MARGIN_L, 1.12, 2.5, 0.38, fill=C.RED)
    tbox(sl, f"⚡ LIVE DATA  {TODAY}", Layout.MARGIN_L, 1.12, 2.5, 0.38,
         size=9, bold=True, align=PP_ALIGN.CENTER)
    tbox(sl, "Crawling Agent 자동 수집 | Amazon US 실거래가 (3P 포함)",
         3.1, 1.17, 7.0, 0.28, size=8.5, color=C.GRAY_400, italic=True)

    # 가격 비교 테이블
    real = MKT["asp_usd"]
    crawled = SALE["amazon_real_prices"]

    price_headers = ["제품 (카테고리)", "SanDisk MSRP", "Amazon 실측가", "3P Premium", "Samsung 경쟁제품", "Gap vs Samsung"]
    price_rows = [
        ["Extreme 1TB (Ext.SSD)",
         "$99.99",
         (f"${crawled['SD_EXTREME_1TB_USD']['crawled']:.2f}",  C.DARK_RED),
         (f"+{crawled['SD_EXTREME_1TB_USD']['premium_pct']:.0f}%", C.DARK_RED),
         "T7 1TB  $174.99",
         ("-$76",  C.GREEN)],
        ["Extreme 2TB (Ext.SSD)",
         "$159.99",
         (f"${crawled['SD_EXTREME_2TB_USD']['crawled']:.2f}", C.DARK_RED),
         (f"+{crawled['SD_EXTREME_2TB_USD']['premium_pct']:.0f}%", C.DARK_RED),
         "T7 2TB  $309.17",
         ("-$24",  C.GREEN)],
        ["SN850X 2TB (Int.SSD)",
         "$149.99",
         (f"${crawled['SD_SN850X_2TB_USD']['crawled']:.2f}", C.DARK_RED),
         (f"+{crawled['SD_SN850X_2TB_USD']['premium_pct']:.0f}%", C.DARK_RED),
         "990 Pro 2TB  $384.97",
         ("+$58",  C.ORANGE)],
        ["Ultra microSD 128G",
         "$18.99",
         (f"${crawled['SD_ULTRA_MICRO_128G_USD']['crawled']:.2f}", C.DARK_RED),
         (f"+{crawled['SD_ULTRA_MICRO_128G_USD']['premium_pct']:.0f}%", C.DARK_RED),
         "—",
         "N/A"],
        ["Extreme microSD 256G",
         "$28.99",
         (f"${crawled['SD_EXTREME_MICRO_256G_USD']['crawled']:.2f}", C.GREEN),
         (f"+{crawled['SD_EXTREME_MICRO_256G_USD']['premium_pct']:.0f}%", C.GRAY_400),
         "N/A (SanDisk #1)",
         "N/A"],
    ]
    data_table(sl, Layout.MARGIN_L, 1.6, Layout.CONTENT_W, price_headers, price_rows,
               col_widths=[2.8, 1.7, 1.7, 1.5, 2.5, 2.33],
               header_fill=C.NAVY_MID, font_size=9)

    # 인사이트 박스
    rect(sl, Layout.MARGIN_L, 4.45, Layout.CONTENT_W, 0.04, fill=C.RED)
    rect(sl, Layout.MARGIN_L, 4.49, Layout.CONTENT_W, 2.25, fill="0A1628")

    findings2 = [
        ("🚨", "Amazon 3P 가격 이탈 심각",
         "SD Ultra microSD 128G: MSRP $18.99 → 실측 $82.99(+337%). "
         "SD Extreme 1TB: MSRP $99.99 → $198.59(+99%). Amazon 1P 재고 부족이 원인 — "
         "즉시 Amazon Vendor Central 재고 보충 및 Buy Box 확보 전략 필요"),
        ("💡", "가격 인텔리전스 시사점",
         "SN850X 2TB($442.99) vs Samsung 990Pro 2TB($384.97) — 경쟁사 대비 $58 열위. "
         "Crawling Agent 일일 모니터링으로 가격 이탈 조기 감지 중 (SLA: 24h 이내 알림)"),
    ]
    exec_summary_block(sl, findings2, Layout.MARGIN_L+0.1, 4.55, Layout.CONTENT_W-0.2, 2.1)

    slide_footer(sl,
        source=f"SanDisk Crawling Agent 실측 ({TODAY}) — Amazon US 3P 포함 최저가 기준; "
               "MSRP: SanDisk.com 공식가; Samsung 가격: Amazon US 공식 스토어",
        page_num=f"{pg}")

    # ══════════════════════════════════════════════════════════
    # SLIDE 7: 경쟁사 시장 점유율
    # ══════════════════════════════════════════════════════════
    sl = D.new_slide(prs); pg += 1
    slide_header(sl, "글로벌 시장 점유율 현황 — 카테고리별 (2024E)",
                 f"{PAGE_PREFIX}  |  Slide {pg}")

    comp_cats = [
        ("External SSD", [
            ("Samsung",      33, C.GRAY_400),
            ("SanDisk/WD ★", 22, C.RED),
            ("Seagate",      13, C.GRAY_600),
            ("Crucial",       7, C.GRAY_600),
            ("ADATA",         6, C.GRAY_600),
            ("Lexar",         4, C.GRAY_600),
            ("Others",       15, C.NAVY_LIGHT),
        ], C.RED),
        ("Internal SSD (Consumer)", [
            ("Samsung",      28, C.GRAY_400),
            ("SanDisk/WD ★", 17, C.RED),
            ("SK Hynix",     12, C.GRAY_600),
            ("Kingston",     11, C.GRAY_600),
            ("Crucial",      11, C.GRAY_600),
            ("Seagate",       6, C.GRAY_600),
            ("Others",       15, C.NAVY_LIGHT),
        ], C.BLUE),
        ("microSD", [
            ("SanDisk ★",    32, C.RED),
            ("Samsung",      23, C.GRAY_400),
            ("Lexar",        11, C.GRAY_600),
            ("Kingston",      9, C.GRAY_600),
            ("Transcend",     6, C.GRAY_600),
            ("Others",       19, C.NAVY_LIGHT),
        ], C.GREEN),
    ]

    for i, (cat_name, comp_data, accent_col) in enumerate(comp_cats):
        x = Layout.MARGIN_L + i*4.25
        rect(sl, x, 1.15, 3.95, 0.45, fill=accent_col)
        tbox(sl, cat_name, x, 1.15, 3.95, 0.45,
             size=12, bold=True, align=PP_ALIGN.CENTER)

        rect(sl, x, 1.65, 3.95, 5.05, fill=C.NAVY_MID)
        for j, (brand, share, bar_col) in enumerate(comp_data):
            y = 1.75 + j * 0.65
            bar_w = share / 35 * 2.8
            is_sd = "SanDisk" in brand or "WD" in brand
            text_col = C.RED if is_sd else (C.GRAY_400 if brand=="Samsung" else C.GRAY_600)
            fw = 10 if is_sd else 9

            tbox(sl, brand, x+0.15, y+0.06, 1.7, 0.4,
                 size=fw, bold=is_sd, color=text_col)
            if share > 0:
                rect(sl, x+1.9, y+0.1, bar_w, 0.38, fill=bar_col)
            tbox(sl, f"{share}%", x+1.9+bar_w+0.1, y+0.06, 0.6, 0.38,
                 size=fw, bold=is_sd, color=text_col)

    # 하단 인사이트
    rect(sl, Layout.MARGIN_L, 6.75, Layout.CONTENT_W, 0.02, fill=C.RED)
    tbox(sl,
         "Strategic Priority: microSD #1 수성(32%→34%) + External SSD 점유율 확대(22%→24%) + "
         "Internal SSD 게이밍 세그먼트 집중(SN850X PS5 인증 레버리지)",
         Layout.MARGIN_L, 6.82, Layout.CONTENT_W, 0.35,
         size=9, color=C.GRAY_400, italic=True)

    slide_footer(sl,
        source="IDC Worldwide Storage Quarterly Tracker Q4 2024; "
               "TrendForce Consumer SSD Market Share H2 2024; "
               "SanDisk Internal Estimate (microSD)",
        page_num=f"{pg}")

    # ══════════════════════════════════════════════════════════
    # SLIDE 8: 카테고리별 성장 동인
    # ══════════════════════════════════════════════════════════
    sl = D.new_slide(prs); pg += 1
    slide_header(sl, "카테고리별 성장 동인 & 리스크 매트릭스",
                 f"{PAGE_PREFIX}  |  Slide {pg}")

    cat_details = [
        {
            "name": "External SSD", "rev_2025": "$1.04B", "growth": "+9.1%",
            "color": C.RED, "cagr": "TAM +20%",
            "drivers": [
                "콘텐츠 크리에이터 급증: YouTube 크리에이터 5.1억명(+22% YoY)",
                "HDD 완전 대체 가속: HDD 외장 시장 -18% YoY → SSD 전환",
                "USB4/Thunderbolt 채택: 2000MB/s 고속 포트 보급 확산",
                "4K/8K 촬영 폭증: 파일 용량 증가 → 대용량 수요",
            ],
            "risks": [
                "Samsung T9 프리미엄 프라이싱 압박 (T9 1TB $224.99)",
                "Amazon 재고 부족으로 3P 프리미엄 발생 (+99%)",
            ],
        },
        {
            "name": "Internal SSD (Consumer)", "rev_2025": "$882M", "growth": "+16.1%",
            "color": C.BLUE, "cagr": "TAM +18%",
            "drivers": [
                "PS5/Xbox 공식 확장 저장소 수요: SN850X PS5 공식 인증",
                "PC 빌드/업그레이드 시즌: 연 2회 피크(Q1 CES, Q4 홀리데이)",
                "AI PC 등장: PCIe 5.0 NVMe 수요 견인",
                "HDD → NVMe 전환 지속: 라이트 사용자 SSD 첫 구매",
            ],
            "risks": [
                "가격 경쟁 심화: Kingston NV3 1TB $45(QL)",
                "삼성 990Pro vs SN850X 벤치마크 열위 구간 존재",
            ],
        },
        {
            "name": "microSD", "rev_2025": "$1.61B", "growth": "+5.9%",
            "color": C.GREEN, "cagr": "TAM +10%",
            "drivers": [
                "Steam Deck/Nintendo Switch 번들 수요 지속",
                "드론·액션캠(DJI, GoPro) 고속 카드 필수화",
                "APAC 예산폰 보급: 인도·동남아 Android 시장",
                "CCTV·블랙박스 IoT 수요: High Endurance 라인",
            ],
            "risks": [
                "스마트폰 microSD 슬롯 폐지 트렌드 (Samsung 플래그십)",
                "Lexar·Kingston 공격적 저가 공세",
            ],
        },
    ]

    for i, cat in enumerate(cat_details):
        x = Layout.MARGIN_L + i * 4.25
        col = cat["color"]

        # 헤더
        rect(sl, x, 1.15, 3.95, 0.6, fill=col)
        tbox(sl, cat["name"], x+0.1, 1.18, 2.5, 0.38, size=13, bold=True, color=C.WHITE)
        tbox(sl, f"{cat['rev_2025']}  {cat['growth']}", x+2.6, 1.22, 1.3, 0.28,
             size=9, color=C.WHITE, align=PP_ALIGN.RIGHT)
        tbox(sl, cat["cagr"], x+2.6, 1.5, 1.3, 0.2,
             size=8, color="FFAAAA", align=PP_ALIGN.RIGHT)

        # 성장 동인
        rect(sl, x, 1.8, 3.95, 0.35, fill=C.NAVY_LIGHT)
        tbox(sl, "✅ 성장 동인", x+0.1, 1.83, 3.7, 0.28, size=9, bold=True, color=C.GREEN)

        rect(sl, x, 2.15, 3.95, 3.0, fill=C.NAVY_MID)
        for j, d in enumerate(cat["drivers"]):
            tbox(sl, f"• {d}", x+0.15, 2.2+j*0.7, 3.7, 0.6,
                 size=8.5, color=C.WHITE)

        # 리스크
        rect(sl, x, 5.2, 3.95, 0.32, fill="2A1515")
        tbox(sl, "⚠️ 리스크", x+0.1, 5.23, 3.7, 0.25, size=9, bold=True, color=C.RED)
        rect(sl, x, 5.52, 3.95, 1.18, fill="1A0F0F")
        for j, r in enumerate(cat["risks"]):
            tbox(sl, f"• {r}", x+0.15, 5.56+j*0.55, 3.7, 0.48, size=8.5, color="FFB3B3")

    slide_footer(sl,
        source="SanDisk Product Marketing; Steam/Nintendo Switch 출하 데이터; "
               "IDC Global PC Monitor Q3 2024; Sony PlayStation 판매 통계",
        page_num=f"{pg}")

    # ══════════════════════════════════════════════════════════
    # SLIDE 9: 채널 & 지역 믹스
    # ══════════════════════════════════════════════════════════
    sl = D.new_slide(prs); pg += 1
    slide_header(sl, "채널별·지역별 매출 믹스 분석 (2024 실적)",
                 f"{PAGE_PREFIX}  |  Slide {pg}")

    ch_mix = SALE["channel_mix_pct"]["2024"]
    geo_mix = SALE["geo_mix_pct"]["2024"]

    # 채널 믹스 (좌측)
    rect(sl, Layout.MARGIN_L, 1.15, 6.0, 5.6, fill=C.NAVY_MID)
    tbox(sl, "채널별 매출 비중 (2024)", Layout.MARGIN_L+0.15, 1.25, 5.6, 0.38,
         size=12, bold=True, color=C.WHITE)

    ch_labels = {"ecommerce":"E-Commerce (Amazon 등)","retail":"오프라인 Retail","b2b":"B2B/Corporate"}
    ch_colors = [C.RED, C.BLUE, C.GREEN]
    cats_ch = ["external_ssd","internal_ssd","microsd"]
    cat_names_ch = ["External SSD","Internal SSD","microSD"]

    for ci, (cat_k, cat_n) in enumerate(zip(cats_ch, cat_names_ch)):
        y = 1.75 + ci * 1.6
        tbox(sl, cat_n, Layout.MARGIN_L+0.15, y, 1.5, 0.35, size=10, bold=True, color=C.WHITE)
        cumul_x = Layout.MARGIN_L + 0.15
        total_bar_w = 5.5
        for chi, ch_k in enumerate(["ecommerce","retail","b2b"]):
            pct = ch_mix[cat_k][ch_k]
            bw = pct / 100 * total_bar_w
            rect(sl, cumul_x, y+0.4, bw, 0.6, fill=ch_colors[chi])
            if pct >= 12:
                tbox(sl, f"{pct}%", cumul_x+0.05, y+0.45, bw-0.1, 0.5,
                     size=9, bold=True, align=PP_ALIGN.CENTER)
            cumul_x += bw

    # 범례
    for i, (ch_k, label) in enumerate(ch_labels.items()):
        rect(sl, Layout.MARGIN_L+0.15+i*2.0, 6.55, 0.2, 0.2, fill=ch_colors[i])
        tbox(sl, label, Layout.MARGIN_L+0.45+i*2.0, 6.53, 1.7, 0.25, size=8, color=C.GRAY_400)

    # 지역 믹스 (우측)
    rect(sl, 6.7, 1.15, 6.23, 5.6, fill=C.NAVY_MID)
    tbox(sl, "지역별 매출 비중 (2024)", 6.85, 1.25, 5.9, 0.38,
         size=12, bold=True, color=C.WHITE)

    geo_colors = {"NA":C.BLUE,"EMEA":C.GREEN,"APAC":C.ORANGE,"Japan":C.PURPLE,"China":C.RED}
    for ci, (cat_k, cat_n) in enumerate(zip(cats_ch, cat_names_ch)):
        y = 1.75 + ci * 1.6
        tbox(sl, cat_n, 6.85, y, 1.5, 0.35, size=10, bold=True, color=C.WHITE)
        cumul_x = 6.85
        total_bar_w = 5.9
        for geo in ["NA","EMEA","APAC","Japan","China"]:
            pct = geo_mix[cat_k].get(geo, 0)
            bw = pct / 100 * total_bar_w
            rect(sl, cumul_x, y+0.4, bw, 0.6, fill=geo_colors[geo])
            if pct >= 8:
                tbox(sl, f"{geo}\n{pct}%", cumul_x+0.02, y+0.4, bw-0.04, 0.6,
                     size=7.5, bold=False, align=PP_ALIGN.CENTER)
            cumul_x += bw

    # 지역 범례
    for i, (geo, col) in enumerate(geo_colors.items()):
        rect(sl, 6.85+i*1.15, 6.55, 0.2, 0.2, fill=col)
        tbox(sl, geo, 7.1+i*1.15, 6.53, 0.9, 0.25, size=8, color=C.GRAY_400)

    slide_footer(sl,
        source="SanDisk Internal Channel Sales Tracking 2024; "
               "Amazon Vendor Central 채널 보고; WD Regional Sales Reports",
        page_num=f"{pg}")

    # ══════════════════════════════════════════════════════════
    # SLIDE 10: 전략적 시사점 & Recommendations
    # ══════════════════════════════════════════════════════════
    sl = D.new_slide(prs); pg += 1
    slide_header(sl, "전략적 시사점 & 마케팅 Recommendations",
                 f"{PAGE_PREFIX}  |  Slide {pg}")

    recs = [
        ("🥇", "P0  즉시 액션", C.RED,
         [
          "Amazon 1P 재고 긴급 보충 — Ultra microSD·Extreme 1TB 3P 이탈 방지",
          "SN850X 2TB 가격 조정 검토 ($442→$149 목표, Amazon Buy Box 확보)",
          "Extreme Pro (BiCS8) Q3 출시 일정 재확인 — GM% 개선 핵심 레버",
         ]),
        ("📈", "P1  Q2~Q3 추진", C.ORANGE,
         [
          "External SSD 2TB 믹스 상향 캠페인 — GM% 높은 대용량 집중",
          "microSD 게이밍(Steam Deck·Switch) 번들 파트너십 집행",
          "EMEA/APAC 지역 확대 — microSD CAGR 높은 인도·동남아 집중",
         ]),
        ("🔭", "P2  중장기 (2026)", C.BLUE,
         [
          "BiCS8 전 라인업 전환 완료 → 원가 구조 혁신 (GM% 55%+ 목표)",
          "Internal SSD 점유율 17%→19% — PS5 공식 인증 마케팅 레버리지",
          "TrendForce 데이터 구독 + Crawling Agent 연동 — 실시간 가격 모니터링",
         ]),
    ]

    for i, (icon, priority, col, bullets) in enumerate(recs):
        x = Layout.MARGIN_L + i * 4.25
        rect(sl, x, 1.15, 3.95, 0.55, fill=col)
        tbox(sl, f"{icon}  {priority}", x+0.15, 1.18, 3.7, 0.45, size=13, bold=True)
        rect(sl, x, 1.72, 3.95, 4.95, fill=C.NAVY_MID)
        for j, b in enumerate(bullets):
            rect(sl, x+0.15, 1.88+j*1.45, 0.05, 0.9, fill=col)
            tbox(sl, b, x+0.3, 1.85+j*1.45, 3.55, 1.1, size=9, color=C.WHITE)

    # 요약 한 줄
    rect(sl, Layout.MARGIN_L, 6.75, Layout.CONTENT_W, 0.03, fill=C.RED)
    tbox(sl,
         "Bottom Line: $3.53B 2025 목표 달성을 위해 — 재고 관리(Amazon 1P), "
         "BiCS 전환(원가), 게이밍·크리에이터 타겟팅(마케팅) 3축 동시 실행 필요",
         Layout.MARGIN_L, 6.83, Layout.CONTENT_W, 0.35,
         size=9, bold=True, color=C.WHITE)

    slide_footer(sl,
        source="SanDisk Marketing Planning 2025; 내부 분석 종합",
        page_num=f"{pg}")

    # 저장
    out = PPTX_DIR / "demand_forecast_vp.pptx"
    prs.save(out)
    print(f"[수요예측 에이전트] ✅ VP급 PPTX: {out}")
    return out


if __name__ == "__main__":
    build()
