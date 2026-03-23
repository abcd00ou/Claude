"""
Word Agent — 한국어 학습용 Word 보고서 생성
주제별 7장 구성, 참고 URL 포함
출력: outputs/reports/ai_scm_study_YYYYMMDD.docx
"""
import os, sys, json
from datetime import datetime, date
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, RGBColor, Cm, Inches
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

OUTPUT_DIR = Path(__file__).parent.parent / "outputs" / "reports"
DATA_DIR   = Path(__file__).parent.parent / "data"

def _load_state():
    p = DATA_DIR / "market_state.json"
    if p.exists():
        with open(p) as f:
            return json.load(f)
    return {}

def _add_heading(doc, text, level=1, color=None):
    h = doc.add_heading(text, level=level)
    if color:
        for run in h.runs:
            run.font.color.rgb = RGBColor(*color)
    return h

def _add_table(doc, headers, rows, col_widths=None):
    table = doc.add_table(rows=1+len(rows), cols=len(headers))
    table.style = "Table Grid"
    # 헤더
    hrow = table.rows[0]
    for i, h in enumerate(headers):
        cell = hrow.cells[i]
        cell.text = h
        for run in cell.paragraphs[0].runs:
            run.bold = True
            run.font.size = Pt(10)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        shading = OxmlElement("w:shd")
        shading.set(qn("w:fill"), "1F4E79")
        shading.set(qn("w:color"), "FFFFFF")
        cell._tc.get_or_add_tcPr().append(shading)
        for run in cell.paragraphs[0].runs:
            run.font.color.rgb = RGBColor(255,255,255)
    # 데이터 행
    for ri, row in enumerate(rows):
        trow = table.rows[ri+1]
        for ci, val in enumerate(row):
            trow.cells[ci].text = str(val)
            if trow.cells[ci].paragraphs[0].runs:
                trow.cells[ci].paragraphs[0].runs[0].font.size = Pt(9)
    return table

def _add_ref_table(doc, refs):
    """참고자료 표 추가"""
    if not refs:
        return
    doc.add_paragraph("참고 자료", style="Heading 3")
    table = doc.add_table(rows=1+len(refs), cols=3)
    table.style = "Table Grid"
    for i, h in enumerate(["출처", "URL", "설명"]):
        cell = table.rows[0].cells[i]
        cell.text = h
        for run in cell.paragraphs[0].runs:
            run.bold = True
    for ri, (name, url, desc) in enumerate(refs):
        row = table.rows[ri+1]
        row.cells[0].text = name
        p = row.cells[1].paragraphs[0]
        run = p.add_run(url)
        run.font.color.rgb = RGBColor(0, 70, 180)
        run.font.size = Pt(8)
        row.cells[2].text = desc
    doc.add_paragraph()

def build(state=None, bottleneck=None, strategy=None, modeling=None, mapping=None):
    if not DOCX_AVAILABLE:
        print("  [Word] python-docx 미설치 — 건너뜀")
        return None

    if state is None:
        state = _load_state()

    doc = Document()

    # 페이지 여백
    for section in doc.sections:
        section.top_margin    = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin   = Cm(3.0)
        section.right_margin  = Cm(2.5)

    # ══════════════════════════════════════════
    # 표지
    # ══════════════════════════════════════════
    doc.add_paragraph()
    title = doc.add_heading("AI 공급망 인텔리전스 리포트", 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sub = doc.add_paragraph("AI Supply Chain Intelligence — 심층 학습 자료")
    sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    dt = doc.add_paragraph(f"작성일: {date.today().strftime('%Y년 %m월 %d일')}")
    dt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    doc.add_page_break()

    # ══════════════════════════════════════════
    # 1장. AI 공급망 개요
    # ══════════════════════════════════════════
    _add_heading(doc, "1장. AI 공급망 개요", 1)
    doc.add_paragraph(
        "AI 공급망은 최종 사용자의 토큰 수요로부터 시작하여 GPU, HBM 메모리, "
        "패키징(CoWoS), 파운드리(TSMC), 전력 인프라까지 연결된 복잡한 생태계입니다. "
        "각 레이어는 상호의존적이며, 특정 레이어의 병목이 전체 공급망에 영향을 미칩니다."
    )

    _add_heading(doc, "1.1 밸류 체인 레이어 (14개)", 2)
    vc_rows = []
    for layer, info in config.VALUE_CHAIN.items():
        companies = ", ".join(info.get("companies", [])[:3])
        risk = info.get("bottleneck_risk", "-")
        layer_ko = {
            "end_customer":"최종 사용자", "ai_service":"AI 서비스", "cloud_dc":"클라우드/DC",
            "gpu_server":"GPU 서버", "hbm":"HBM 메모리", "dram":"DRAM",
            "ssd_storage":"SSD 스토리지", "cpu":"CPU", "networking":"네트워킹",
            "packaging":"패키징(CoWoS)", "power":"전력 인프라", "foundry":"파운드리",
            "asic":"ASIC", "edge_ai":"엣지 AI", "sovereign_ai":"Sovereign AI",
        }.get(layer, layer)
        risk_ko = {"critical":"위험", "high":"높음", "medium":"보통", "low":"낮음"}.get(risk, risk)
        vc_rows.append([layer_ko, companies, risk_ko])
    _add_table(doc, ["레이어", "주요 기업", "병목 위험도"], vc_rows)
    doc.add_paragraph()

    _add_heading(doc, "1.2 공급망 흐름 다이어그램", 2)
    doc.add_paragraph(
        "토큰 수요 → AI 서비스 → 클라우드 DC → GPU 서버 → HBM/DRAM → 패키징(CoWoS) → 파운드리(TSMC)\n"
        "                                    ↓\n"
        "                         전력 인프라 / 네트워킹\n\n"
        "* 핵심 병목: HBM(95%) → CoWoS(92%) → 전력(78%) 순"
    )

    _add_ref_table(doc, [
        ("Bloomberg AI 투자 차트", config.REFERENCE_URLS.get("Bloomberg_AI_Chart",""), "AI 공급망 투자 관계 시각화"),
        ("Sequoia AI 인프라 분석", config.REFERENCE_URLS.get("Sequoia_AI_Infra",""), "AI $600B 인프라 투자 분석"),
        ("IEA 전력 보고서", config.REFERENCE_URLS.get("DC_Power_IEA",""), "데이터센터 전력 수요 전망"),
    ])
    doc.add_page_break()

    # ══════════════════════════════════════════
    # 2장. 토큰 수요 → 하드웨어 수요 변환 모델
    # ══════════════════════════════════════════
    _add_heading(doc, "2장. 토큰 수요 → 하드웨어 수요 변환 모델", 1)
    doc.add_paragraph(
        "AI 서비스의 핵심 수요 단위는 '토큰'입니다. 토큰 처리량이 증가할수록 "
        "GPU, HBM 메모리, 전력 수요가 연쇄적으로 증가합니다."
    )

    _add_heading(doc, "2.1 핵심 수식", 2)
    formulas = [
        ("Token → GPU",  "GPU 수량 = 일간 토큰 수 ÷ (GPU 초당 토큰 × 가동률)"),
        ("GPU → HBM",    "HBM 수요(GB) = GPU 수량 × GPU당 HBM 용량"),
        ("KV 캐시 메모리", "KV Cache(GB) = 컨텍스트 길이 × 동시 사용자 × 2바이트 × 2 ÷ 10⁹"),
        ("SSD 수요",     "SSD(GB) = 일간 RAG 토큰 × 문서당 토큰 ÷ 10⁹ × 바이트/토큰"),
        ("전력 수요",    "전력(MW) = GPU 수량 × TDP × 서버 오버헤드(1.3) × PUE(1.4) ÷ 10⁶"),
    ]
    _add_table(doc, ["수식명", "공식"], formulas)
    doc.add_paragraph()

    _add_heading(doc, "2.2 2025년 기준 수치 (Base 시나리오)", 2)
    base_rows = [
        ["토큰 수요",      "88.5T tokens/day",  "ChatGPT·Claude·Gemini·오픈소스 합산"],
        ["필요 GPU",       "60만 개 (H100 기준)", "가동률 85% 가정"],
        ["HBM 수요",       "48.2 PB",            "H100 80GB 기준"],
        ["전력 수요",      "768 MW",             "PUE 1.4 적용"],
        ["SSD 수요 (RAG)", "연간 ~50 EB 누적",   "RAG 비율 30% 가정"],
    ]
    _add_table(doc, ["지표", "수치", "비고"], base_rows)
    doc.add_paragraph()

    _add_heading(doc, "2.3 시나리오별 예측 (2024-2027)", 2)
    scenario_rows = [
        ["Base", "2024", "29.4T/day",   "38만 GPU",  "7.1GW"],
        ["Base", "2025", "88.5T/day",   "60만 GPU",  "7.7GW"],
        ["Base", "2026", "177T/day",    "120만 GPU", "15.4GW"],
        ["Bull", "2025", "132.7T/day",  "90만 GPU",  "11.5GW"],
        ["Bull", "2026", "398T/day",    "270만 GPU", "34.7GW"],
        ["Bear", "2025", "61.9T/day",   "42만 GPU",  "5.4GW"],
        ["Bear", "2026", "105.3T/day",  "71만 GPU",  "9.2GW"],
    ]
    _add_table(doc, ["시나리오", "연도", "토큰/일", "GPU 수요", "전력(MW)"], scenario_rows)

    _add_ref_table(doc, [
        ("NVIDIA 분기 실적", config.REFERENCE_URLS.get("NVIDIA_DataCenter",""), "GPU 출하량 및 데이터센터 매출"),
        ("Goldman Sachs 전력 분석", config.REFERENCE_URLS.get("Goldman_DC_Power",""), "AI 전력 수요 160% 증가 예측"),
        ("IDC GPU 시장", config.REFERENCE_URLS.get("IDC_GPU_Market",""), "GPU 시장 출하량 데이터"),
    ])
    doc.add_page_break()

    # ══════════════════════════════════════════
    # 3장. 병목 분석
    # ══════════════════════════════════════════
    _add_heading(doc, "3장. 병목 분석", 1)
    doc.add_paragraph(
        "공급망 병목은 수요 증가 속도가 공급 증설 속도를 초과할 때 발생합니다. "
        "2025년 현재 HBM이 1차 병목이며, Power/Grid가 2026년 주요 병목으로 전환될 전망입니다."
    )

    _add_heading(doc, "3.1 레이어별 가동률 현황 (2025 기준)", 2)
    bn_rows = []
    for layer, util in config.CURRENT_CAPACITY_UTILIZATION.items():
        sev = "위험" if util >= 0.85 else ("높음" if util >= 0.70 else ("보통" if util >= 0.50 else "낮음"))
        layer_ko = {"HBM":"HBM 메모리","CoWoS":"CoWoS 패키징","GPU":"GPU 서버",
                    "Power_DC":"전력/DC","Networking":"네트워킹","DRAM":"DRAM","SSD":"SSD"}.get(layer, layer)
        bn_rows.append([layer_ko, f"{util*100:.0f}%", sev])
    _add_table(doc, ["레이어", "가동률", "심각도"], bn_rows)
    doc.add_paragraph()

    _add_heading(doc, "3.2 병목 전이 예측", 2)
    cascade = [
        ["현재 (2025 H1)", "HBM",        "95%", "SK Hynix CoWoS 물량 부족, B200 수요 폭증"],
        ["단기 (2025 H2)", "CoWoS",      "92%", "TSMC CoWoS 캐파 80K wpm로 확대 예정"],
        ["중기 (2026)",    "Power/Grid", "78%→90%+", "데이터센터 전력 수요 2배 증가"],
        ["장기 (2027)",    "Networking", "65%→85%", "GB200 클러스터 확산으로 IB 수요 급증"],
    ]
    _add_table(doc, ["시기", "병목 레이어", "예상 가동률", "원인"], cascade)

    _add_ref_table(doc, [
        ("SK Hynix HBM", config.REFERENCE_URLS.get("SKHynix_HBM",""), "HBM3e 생산 현황 및 공급 계획"),
        ("TSMC CoWoS", config.REFERENCE_URLS.get("TSMC_CoWoS",""), "CoWoS 패키징 캐파 확대 계획"),
        ("HBM 시장 규모", config.REFERENCE_URLS.get("HBM_Market_Size",""), "HBM 시장 $35B(2025E) → $55B(2026E)"),
    ])
    doc.add_page_break()

    # ══════════════════════════════════════════
    # 4장. 하이퍼스케일러 CapEx 동향
    # ══════════════════════════════════════════
    _add_heading(doc, "4장. 하이퍼스케일러 CapEx 동향", 1)
    doc.add_paragraph(
        "Big 4(Microsoft, Google, Amazon, Meta) + xAI의 AI 인프라 투자는 "
        "2024년 $219B에서 2025년 $340B으로 55% 급증했습니다. "
        "이 투자의 약 40-60%가 GPU 구매에 해당하며, NVIDIA 수혜가 가장 큽니다."
    )

    _add_heading(doc, "4.1 연도별 CapEx 테이블 (USD 십억)", 2)
    capex_rows = []
    for company, years in config.HYPERSCALER_CAPEX.items():
        row = [company]
        for yr in ["2022","2023","2024","2025","2026_est"]:
            row.append(f"${years.get(yr, '-')}B" if years.get(yr) else "-")
        capex_rows.append(row)
    _add_table(doc, ["회사", "2022", "2023", "2024", "2025", "2026E"], capex_rows)
    doc.add_paragraph()

    _add_heading(doc, "4.2 AI 투자 시사점", 2)
    doc.add_paragraph(
        "- Microsoft: OpenAI 독점 파트너십 + Azure AI 서비스 확장. $80B CapEx 중 50%+ AI 인프라.\n"
        "- Google: TPU v5 + NVIDIA GPU 병행. Anthropic 투자로 모델 다양화.\n"
        "- Amazon: AWS 트레이닝 인프라 + Anthropic $40억 투자. Trainium2 자체 칩 개발.\n"
        "- Meta: 오픈소스 LLaMA 전략. 자체 MTIA ASIC 칩 개발 중.\n"
        "- xAI: Grok 모델. 멤피스 Colossus 클러스터 (10만 H100 → 20만 목표)."
    )

    _add_ref_table(doc, [
        ("Microsoft 실적발표", config.REFERENCE_URLS.get("Microsoft_CapEx",""), "분기 CapEx 공시"),
        ("Google 실적발표",    config.REFERENCE_URLS.get("Google_CapEx",""),    "알파벳 IR 자료"),
        ("Amazon 실적발표",    config.REFERENCE_URLS.get("Amazon_CapEx",""),    "AWS CapEx 공시"),
        ("Meta 실적발표",      config.REFERENCE_URLS.get("Meta_CapEx",""),      "Meta AI 투자 공시"),
    ])
    doc.add_page_break()

    # ══════════════════════════════════════════
    # 5장. 투자 네트워크 분석
    # ══════════════════════════════════════════
    _add_heading(doc, "5장. 투자 네트워크 분석", 1)
    doc.add_paragraph(
        "AI 공급망의 자금 흐름을 투자 관계(Investment), 하드웨어 공급(Hardware Supply), "
        "서비스 계약(Service), VC 투자(VC) 4가지 유형으로 분류합니다."
    )

    _add_heading(doc, "5.1 주요 투자 관계 요약", 2)
    inv_rows = []
    for rel in config.COMPANY_RELATIONSHIPS:
        if rel[2] in ("investment", "vc"):
            inv_rows.append([rel[0], rel[1], rel[2], rel[3] if len(rel)>3 else "", rel[4] if len(rel)>4 else ""])
    inv_rows = inv_rows[:15]
    _add_table(doc, ["투자자", "피투자사", "유형", "설명", "규모"], inv_rows)
    doc.add_paragraph()

    _add_heading(doc, "5.2 하드웨어 공급 구조 (독점/경쟁 분석)", 2)
    hw_rows = []
    for rel in config.COMPANY_RELATIONSHIPS:
        if rel[2] == "hardware_supply" and "독점" in (rel[4] if len(rel)>4 else ""):
            hw_rows.append([rel[0], rel[1], rel[3] if len(rel)>3 else "", "독점"])
    for rel in config.COMPANY_RELATIONSHIPS:
        if rel[2] == "hardware_supply" and "독점" not in (rel[4] if len(rel)>4 else "") and len(hw_rows) < 12:
            hw_rows.append([rel[0], rel[1], rel[3] if len(rel)>3 else "", "경쟁"])
    _add_table(doc, ["공급사", "수요사", "공급 내용", "구조"], hw_rows[:12])

    _add_ref_table(doc, [
        ("NVIDIA-OpenAI 투자", config.REFERENCE_URLS.get("NVIDIA_OpenAI_Investment",""), "NVIDIA $1,000억 투자 합의"),
        ("Microsoft-OpenAI",   config.REFERENCE_URLS.get("Microsoft_OpenAI",""),         "$130억+ 누적 투자"),
        ("Google-Anthropic",   config.REFERENCE_URLS.get("Google_Anthropic",""),         "$20억 투자"),
        ("Amazon-Anthropic",   config.REFERENCE_URLS.get("Amazon_Anthropic",""),         "$40억 투자"),
    ])
    doc.add_page_break()

    # ══════════════════════════════════════════
    # 6장. 투자 시그널 & 포지셔닝
    # ══════════════════════════════════════════
    _add_heading(doc, "6장. 투자 시그널 & 포지셔닝", 1)
    doc.add_paragraph(
        "현재 AI 공급망 투자 사이클은 Phase 2 (HBM & 패키징) 단계입니다. "
        "Phase 1 GPU 사이클이 무르익은 가운데, HBM 병목이 심화되며 메모리 업사이클이 진행 중입니다."
    )

    _add_heading(doc, "6.1 투자 단계별 로드맵", 2)
    phase_rows = [
        ["Phase 1", "GPU",           "진행 중", "NVIDIA, AMD",              "GPU 수요 폭증기, 이미 주가 반영"],
        ["Phase 2", "HBM & 패키징",  "현재",   "SK Hynix, TSMC CoWoS",    "병목 심화, 메모리 업사이클"],
        ["Phase 3", "전력 인프라",   "2026~",  "Vertiv, Eaton, GE Vernova","DC 전력 수요 2배 증가"],
        ["Phase 4", "엣지/Physical", "2027~",  "퀄컴, 브로드컴, 로봇 기업", "AI 단말 확산"],
    ]
    _add_table(doc, ["단계", "테마", "현황", "수혜 기업", "투자 포인트"], phase_rows)
    doc.add_paragraph()

    _add_heading(doc, "6.2 핵심 투자 시그널", 2)
    signal_rows = [
        ["SK Hynix",    "Strong Buy", "HBM3e 50% 점유율, GB200 전용 공급, 95% 가동률",   "6-18개월"],
        ["TSMC",        "Buy",        "CoWoS 독점, 캐파 확대 진행 중",                   "6-24개월"],
        ["Vertiv",      "Buy",        "DC 전력/냉각 인프라 수요 2배 증가",               "12-24개월"],
        ["Broadcom",    "Buy",        "네트워킹 칩 + ASIC 공동 개발 (Google/Meta)",       "12-18개월"],
        ["NVIDIA",      "Hold",       "주가 선반영, GPU 독점 지속",                      "장기 보유"],
        ["Samsung",     "Watch",      "HBM3e 인증 통과 시 점유율 확대 가능",             "인증 결과 대기"],
        ["AMD",         "Watch",      "MI300X 점유율 확대 중, NVIDIA 격차 축소 모니터링", "경쟁 추이 관찰"],
    ]
    _add_table(doc, ["기업", "시그널", "근거", "투자 기간"], signal_rows)

    _add_ref_table(doc, [
        ("SK Hynix HBM",       config.REFERENCE_URLS.get("SKHynix_HBM",""),      "HBM 생산 및 점유율"),
        ("TSMC CoWoS",         config.REFERENCE_URLS.get("TSMC_Capacity",""),     "패키징 캐파 확대"),
        ("Goldman 전력 분석",   config.REFERENCE_URLS.get("Goldman_DC_Power",""),  "전력 인프라 투자 기회"),
    ])
    doc.add_page_break()

    # ══════════════════════════════════════════
    # 7장. 2025-2027 수요 예측 시나리오
    # ══════════════════════════════════════════
    _add_heading(doc, "7장. 2025-2027 수요 예측 시나리오", 1)
    _add_heading(doc, "7.1 시나리오 가정", 2)
    scenario_def = [
        ["Base", "현 성장세 유지", "연 3배 성장", "가동률 85%",  "NAND/HBM 가격 안정"],
        ["Bull", "AI 확산 가속화", "연 4.5배 성장", "가동률 90%", "공급 부족 심화"],
        ["Bear", "성장 둔화",      "연 2배 성장",  "가동률 75%",  "수요 증가 둔화"],
    ]
    _add_table(doc, ["시나리오", "가정", "토큰 성장률", "GPU 가동률", "공급 환경"], scenario_def)
    doc.add_paragraph()

    _add_heading(doc, "7.2 핵심 지표 예측 (2024-2027)", 2)
    pred_rows = [
        ["2024", "Base", "29.4T/day", "28만", "22.3PB",  "320MW"],
        ["2025", "Base", "88.5T/day", "60만", "48.2PB",  "768MW"],
        ["2025", "Bull", "132.7T/day","90만", "72.4PB", "1,152MW"],
        ["2025", "Bear", "61.9T/day", "42만", "33.7PB",  "538MW"],
        ["2026", "Base", "177T/day", "120만", "96.4PB", "1,536MW"],
        ["2026", "Bull", "398T/day", "270만","216.8PB", "3,456MW"],
        ["2027", "Base", "354T/day", "240만","192.8PB", "3,072MW"],
    ]
    _add_table(doc, ["연도","시나리오","토큰/일","GPU 수요","HBM 수요","전력(MW)"], pred_rows)
    doc.add_paragraph()

    _add_heading(doc, "7.3 시나리오별 수혜/피해 기업", 2)
    impact_rows = [
        ["Bull", "수혜", "SK Hynix, TSMC, Vertiv, NVIDIA", "HBM·패키징·전력 모두 초과 수요"],
        ["Bull", "피해", "공급 확보 실패 AI 서비스 기업",   "인프라 병목으로 서비스 제한"],
        ["Base", "수혜", "SK Hynix, TSMC CoWoS",           "지속적 병목 프리미엄"],
        ["Bear", "수혜", "AMD, Intel Gaudi",               "대체 GPU 수요 증가"],
        ["Bear", "피해", "NVIDIA (고점 대비), HBM 증설 기업","공급 과잉 위험"],
    ]
    _add_table(doc, ["시나리오","구분","기업","근거"], impact_rows)

    _add_ref_table(doc, [
        ("Sequoia AI 인프라", config.REFERENCE_URLS.get("Sequoia_AI_Infra",""),  "AI $600B 인프라 투자 분석"),
        ("IEA 전력 전망",     config.REFERENCE_URLS.get("DC_Power_IEA",""),       "2024-2026 DC 전력 수요"),
        ("IDC GPU 시장",      config.REFERENCE_URLS.get("IDC_GPU_Market",""),     "GPU 시장 출하량 예측"),
    ])

    # ══════════════════════════════════════════
    # 저장
    # ══════════════════════════════════════════
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    today_str = date.today().strftime("%Y%m%d")
    out_path = OUTPUT_DIR / f"ai_scm_study_{today_str}.docx"
    doc.save(str(out_path))
    print(f"  [Word] 학습 문서 생성: {out_path}")
    return str(out_path)

def run(state=None, bottleneck=None, strategy=None, modeling=None, mapping=None):
    return {"word_path": build(state, bottleneck, strategy, modeling, mapping)}
