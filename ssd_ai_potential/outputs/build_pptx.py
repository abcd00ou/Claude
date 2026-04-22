"""
SSD Demand Analysis PPT 생성 스크립트
"""
from pptx import Presentation
from pptx.util import Inches, Pt, Emu, Cm
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from pptx.oxml.ns import qn
from pptx.oxml import parse_xml
import lxml.etree as etree
import copy

# ─── 색상 상수 ───────────────────────────────────────────────
NAVY       = RGBColor(0x1a, 0x25, 0x40)   # 배경
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
SKY        = RGBColor(0x38, 0xBD, 0xF8)   # 강조 하늘색
RED        = RGBColor(0xE2, 0x23, 0x1A)   # 강조 빨강
DARK_BLUE  = RGBColor(0x1E, 0x3A, 0x8A)   # 표 헤더
CELL_BG    = RGBColor(0x1E, 0x29, 0x4E)   # 셀 배경
LINK_BLUE  = RGBColor(0x60, 0xA5, 0xFA)   # URL 색상
LIGHT_GRAY = RGBColor(0xCC, 0xCC, 0xCC)   # 서브텍스트

# ─── URL 데이터 (1단계 추출 결과) ────────────────────────────
URLS = {
    "do_not_use_ai": "https://www.reddit.com/r/StableDiffusion/comments/1ph5t8r/do_not_use_ai_generation_on_ssd_virtual_memory/",
    "bought_slower_nvme": "https://www.reddit.com/r/buildapc/comments/1rcrxcc/i_bought_a_slower_nvme_by_mistake_for_my_first/",
    "sn7100x": "",  # 미발견
    "ssd_prices_scaring": "https://www.reddit.com/r/buildapc/comments/1qzplt9/please_help_pc_noob_looking_to_upgrade_my_ssd/",
    "nvme_now_or_wait": "https://www.reddit.com/r/buildapc/comments/1r7h9hc/should_i_get_a_new_nvme_ssd_right_now_or_wait_to/",
    "rtx_6000_build": "https://www.reddit.com/r/LocalLLaMA/comments/1ro1kie/rtx_6000_build_drive_and_fan_questions/",
    "m2_slot": "https://www.reddit.com/r/homelab/comments/1ritk2p/any_chance_at_getting_this_into_an_m2_slot_lol/",
    "ssd_prices_roof": "https://www.reddit.com/r/StableDiffusion/comments/1qydube/since_ssd_prices_are_going_through_the_roof_i/",
    "vaultai_llama": "https://www.reddit.com/r/LocalLLaMA/comments/1r6trbg/vaultai_42_preloaded_ai_models_on_a_portable_nvme/",
    "vaultai_selfhosted": "https://www.reddit.com/r/selfhosted/comments/1r6tj87/vaultai_portable_ai_workstation_on_an_nvme_ssd/",
    "plex_2309": "https://www.reddit.com/r/homelab/comments/1riw2u6/my_current_setup_mostly_used_for_plex/",
    "homelab_509": "https://www.reddit.com/r/homelab/comments/1rdcc79/my_2026_homelab_in_new_apartment/",
    "5090_build": "https://www.reddit.com/r/nvidia/comments/1oey4qp/my_5090_fe_build/",
    "r9700_128gb": "https://www.reddit.com/r/LocalLLaMA/comments/1qfscp5/128gb_vram_quad_r9700_server/",
    "hybrid_moe": "https://www.reddit.com/r/LocalLLaMA/comments/1rgfm00/i_built_a_hybrid_moe_runtime_that_does_3324_toks/",
    "qwen35": "https://www.reddit.com/r/LocalLLaMA/comments/1rg87bj/qwen3535ba3b_running_on_a_raspberry_pi_5_16gb_and/",
    "nas_80b": "https://www.reddit.com/r/LocalLLaMA/comments/1r1lkfw/my_nas_runs_an_80b_llm_at_18_toks_on_its_igpu_no/",
    "a100_vs_h100": "https://www.reddit.com/r/LocalLLaMA/comments/1pj61cr/benchmarked_a100_vs_h100_local_storage_for/",
    "omlx": "https://www.reddit.com/r/LocalLLaMA/comments/1r3qwyi/omlx_opensource_mlx_inference_server_with_paged/",
}

FOOTER_TEXT = "Source: Reddit Community Analysis | 4,060 posts | 2026-03-17"

# ─── 헬퍼 함수들 ────────────────────────────────────────────

def new_prs():
    prs = Presentation()
    prs.slide_width  = Cm(33.87)
    prs.slide_height = Cm(19.05)
    return prs

def set_slide_bg(slide, color: RGBColor):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

def add_textbox(slide, left, top, width, height,
                text, font_size=11, bold=False, color=WHITE,
                align=PP_ALIGN.LEFT, word_wrap=True):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = word_wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color
    return txBox

def add_footer(slide):
    add_textbox(
        slide,
        Cm(1), Cm(18.0), Cm(31.87), Cm(0.7),
        FOOTER_TEXT,
        font_size=8, color=LIGHT_GRAY, align=PP_ALIGN.CENTER
    )

def set_cell_bg(cell, color: RGBColor):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    # 기존 solidFill 제거
    for existing in tcPr.findall(qn('a:solidFill')):
        tcPr.remove(existing)
    solidFill = etree.SubElement(tcPr, qn('a:solidFill'))
    srgbClr = etree.SubElement(solidFill, qn('a:srgbClr'))
    # RGBColor는 (r,g,b) 튜플처럼 접근하거나 str()로 hex 얻기
    hex_val = '{:02X}{:02X}{:02X}'.format(color[0], color[1], color[2])
    srgbClr.set('val', hex_val)

def set_cell_text(cell, text, font_size=9, bold=False,
                  color=WHITE, align=PP_ALIGN.LEFT,
                  url=None):
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align

    # 기존 run 제거
    for r in p.runs:
        p._p.remove(r._r)

    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.color.rgb = color

    if url and url != "URL 없음":
        # 하이퍼링크 삽입
        rPr = run._r.get_or_add_rPr()
        hlinkClick = etree.SubElement(rPr, qn('a:hlinkClick'))
        rel = cell._tc.getroottree().getroot()
        # URL은 슬라이드 레벨에서 처리 필요 — 색상만 적용
        run.font.color.rgb = LINK_BLUE

def add_hyperlink_to_cell(slide, cell, url_text, display_text=None):
    """셀에 하이퍼링크 추가"""
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT

    if display_text is None:
        display_text = url_text if url_text != "URL 없음" else "URL 없음"

    # 기존 내용 클리어
    for r in p.runs:
        p._p.remove(r._r)

    if url_text and url_text != "URL 없음":
        # 실제 하이퍼링크 생성
        run = p.add_run()
        run.text = display_text
        run.font.size = Pt(8)
        run.font.color.rgb = LINK_BLUE

        # 관계 추가
        rId = slide.part.relate_to(url_text,
            'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',
            is_external=True)
        rPr = run._r.get_or_add_rPr()
        hlinkClick = etree.SubElement(rPr, qn('a:hlinkClick'))
        hlinkClick.set(qn('r:id'), rId)
    else:
        run = p.add_run()
        run.text = "URL 없음"
        run.font.size = Pt(8)
        run.font.color.rgb = LIGHT_GRAY

def make_table(slide, left, top, width, height, rows, cols):
    """표 생성"""
    table = slide.shapes.add_table(rows, cols, left, top, width, height).table
    return table

def style_header_row(table, col_widths=None):
    """표 헤더 행 스타일 적용"""
    for ci, cell in enumerate(table.rows[0].cells):
        set_cell_bg(cell, DARK_BLUE)

# ─── 슬라이드별 생성 함수 ─────────────────────────────────────

def slide1_cover(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
    set_slide_bg(slide, NAVY)

    # 제목
    add_textbox(
        slide,
        Cm(3), Cm(5.5), Cm(27.87), Cm(3),
        "Reddit SSD 수요 분석 리포트",
        font_size=36, bold=True, color=WHITE, align=PP_ALIGN.CENTER
    )
    # 부제
    add_textbox(
        slide,
        Cm(3), Cm(9.5), Cm(27.87), Cm(1.5),
        "Local AI / Homelab 커뮤니티 4,060개 포스트 분석",
        font_size=18, bold=False, color=SKY, align=PP_ALIGN.CENTER
    )
    # 날짜
    add_textbox(
        slide,
        Cm(3), Cm(11.5), Cm(27.87), Cm(1),
        "2026-03-17",
        font_size=14, color=LIGHT_GRAY, align=PP_ALIGN.CENTER
    )
    add_footer(slide)
    return slide


def slide2_kpi(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)

    add_textbox(slide, Cm(1), Cm(0.5), Cm(31), Cm(1.2),
                "핵심 수치 요약", font_size=28, bold=True, color=WHITE)

    # KPI 박스 4개
    kpis = [
        ("전체 분석 포스트", "4,060개", WHITE),
        ("구매 의향 (buy_intent)", "186건", SKY),
        ("교체/확장 (upgrade_intent)", "98건", SKY),
        ("SSD 동시 언급 (co_mention)", "320건", SKY),
    ]

    box_w = Cm(7.2)
    box_h = Cm(4.5)
    gap = Cm(0.8)
    start_x = Cm(1.5)
    start_y = Cm(2.2)

    for i, (label, value, val_color) in enumerate(kpis):
        x = start_x + i * (box_w + gap)
        # 박스 배경
        shape = slide.shapes.add_shape(
            1,  # MSO_SHAPE_TYPE.RECTANGLE
            x, start_y, box_w, box_h
        )
        shape.fill.solid()
        shape.fill.fore_color.rgb = CELL_BG
        shape.line.color.rgb = DARK_BLUE
        shape.line.width = Pt(1.5)

        # 값 텍스트
        add_textbox(slide, x + Cm(0.3), start_y + Cm(0.6), box_w - Cm(0.6), Cm(1.8),
                    value, font_size=28, bold=True, color=val_color, align=PP_ALIGN.CENTER)
        # 레이블 텍스트
        add_textbox(slide, x + Cm(0.3), start_y + Cm(2.6), box_w - Cm(0.6), Cm(1.5),
                    label, font_size=11, color=LIGHT_GRAY, align=PP_ALIGN.CENTER)

    # 서브레딧별 수요 분포
    add_textbox(slide, Cm(1), Cm(7.5), Cm(31), Cm(0.8),
                "서브레딧별 수요 분포",
                font_size=13, bold=True, color=SKY)

    dist_text = "r/homelab  102건   |   r/buildapc  95건   |   r/SelfHosted  66건   |   r/LocalLLaMA  4건"
    add_textbox(slide, Cm(1), Cm(8.4), Cm(31), Cm(1.2),
                dist_text, font_size=13, color=WHITE, align=PP_ALIGN.CENTER)

    # 설명 박스
    shape2 = slide.shapes.add_shape(1, Cm(1), Cm(9.8), Cm(31), Cm(5.0))
    shape2.fill.solid()
    shape2.fill.fore_color.rgb = CELL_BG
    shape2.line.color.rgb = DARK_BLUE
    shape2.line.width = Pt(1)

    insights = [
        "• homelab / buildapc 커뮤니티에서 구매 의향 신호가 가장 강하게 포착",
        "• buy_intent 186건 중 다수가 '지금 살까, 기다릴까' 가격 민감형 질문",
        "• upgrade_intent 98건의 주요 패턴: 500GB → 2TB 업그레이드 고민",
        "• co_mention 320건: AI 모델 운용, 로컬 LLM 추론, Plex/미디어 서버 등 실제 사용 맥락",
    ]
    for j, ins in enumerate(insights):
        add_textbox(slide, Cm(1.5), Cm(10.1) + j * Cm(1.1), Cm(30), Cm(1.0),
                    ins, font_size=11, color=WHITE)

    add_footer(slide)
    return slide


def slide3_nvme(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)

    add_textbox(slide, Cm(0.5), Cm(0.3), Cm(32), Cm(1.0),
                "내장 SSD 구매·교체 수요 — 직접 증거 포스트",
                font_size=22, bold=True, color=WHITE)

    # 표: 6행 5열 (헤더 + 6개 데이터)
    col_widths = [Cm(1.8), Cm(3.5), Cm(8.5), Cm(10.5), Cm(7.5)]
    headers = ["Score", "커뮤니티", "제목", "핵심 발언", "URL"]

    data = [
        ("⬆206", "r/StableDiffusion",
         "Do not use AI generation on SSD virtual memory!",
         '"AI gen on SSD virtual memory drastically shortens SSD lifespan"',
         URLS["do_not_use_ai"]),
        ("⬆178", "r/buildapc",
         "I bought a slower nvme by mistake",
         '"bought Gen3 instead of Gen4, need to exchange"',
         URLS["bought_slower_nvme"]),
        ("⬆17", "r/buildapc",
         "WD Black SN7100X 2TB NVMe — 지금 사야 할까?",
         '"Should I buy 2TB NVMe now before prices rise further?"',
         URLS["sn7100x"] if URLS["sn7100x"] else "URL 없음"),
        ("⬆8", "r/buildapc",
         "SSD prices are scaring me, need to upgrade",
         '"Currently on 500GB, looking at 2TB options"',
         URLS["ssd_prices_scaring"]),
        ("⬆8", "r/buildapc",
         "Should I get new NVMe now or wait for prices to drop?",
         '"I have a 500Gb SSD, which I totally thought would be more than enough"',
         URLS["nvme_now_or_wait"]),
        ("⬆65", "r/LocalLLaMA",
         "RTX 6000 build / drive questions",
         '"What NVMe should I pair with RTX 6000 for AI workloads?"',
         URLS["rtx_6000_build"]),
    ]

    total_w = sum(col_widths)
    tbl = make_table(slide, Cm(0.5), Cm(1.5), total_w, Cm(15.8), 7, 5)

    # 열 너비 설정
    for ci, w in enumerate(col_widths):
        tbl.columns[ci].width = w

    # 헤더
    for ci, h in enumerate(headers):
        cell = tbl.cell(0, ci)
        set_cell_bg(cell, DARK_BLUE)
        set_cell_text(cell, h, font_size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    # 데이터 행
    for ri, row_data in enumerate(data):
        bg = CELL_BG if ri % 2 == 0 else RGBColor(0x17, 0x20, 0x3A)
        for ci, val in enumerate(row_data):
            cell = tbl.cell(ri + 1, ci)
            set_cell_bg(cell, bg)
            if ci == 4:  # URL 컬럼
                add_hyperlink_to_cell(slide, cell, val, "링크")
            else:
                c = SKY if ci == 0 else WHITE
                set_cell_text(cell, str(val), font_size=9, color=c,
                              align=PP_ALIGN.CENTER if ci == 0 else PP_ALIGN.LEFT)

    add_footer(slide)
    return slide


def slide4_portable(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)

    add_textbox(slide, Cm(0.5), Cm(0.3), Cm(32), Cm(1.0),
                "Portable SSD 수요 — 신규 AI 사용 패턴 포착",
                font_size=22, bold=True, color=WHITE)

    col_widths = [Cm(1.8), Cm(3.5), Cm(9.0), Cm(10.0), Cm(7.5)]
    headers = ["Score", "커뮤니티", "제목", "핵심 내용", "URL"]

    data = [
        ("⬆298", "r/homelab",
         "Any chance at getting this into an m.2 slot?",
         "8TB portable SSD 분해해 내장으로 전환 시도 — 용량 절박함",
         URLS["m2_slot"]),
        ("⬆26", "r/StableDiffusion",
         "SSD prices are going through the roof",
         "가격 급등 속 외장 SSD 경험 공유",
         URLS["ssd_prices_roof"]),
        ("⬆1", "r/LocalLLaMA",
         "VaultAI: 42 AI models on portable NVMe SSD",
         "plug-and-play local AI on portable SSD — 새로운 카테고리",
         URLS["vaultai_llama"]),
        ("⬆1", "r/SelfHosted",
         "VaultAI: Portable AI workstation on NVMe",
         "Portable SSD = AI workstation 개념 등장",
         URLS["vaultai_selfhosted"]),
    ]

    total_w = sum(col_widths)
    tbl = make_table(slide, Cm(0.5), Cm(1.5), total_w, Cm(10.5), 5, 5)

    for ci, w in enumerate(col_widths):
        tbl.columns[ci].width = w

    for ci, h in enumerate(headers):
        cell = tbl.cell(0, ci)
        set_cell_bg(cell, DARK_BLUE)
        set_cell_text(cell, h, font_size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    for ri, row_data in enumerate(data):
        bg = CELL_BG if ri % 2 == 0 else RGBColor(0x17, 0x20, 0x3A)
        for ci, val in enumerate(row_data):
            cell = tbl.cell(ri + 1, ci)
            set_cell_bg(cell, bg)
            if ci == 4:
                add_hyperlink_to_cell(slide, cell, val, "링크")
            else:
                c = SKY if ci == 0 else WHITE
                set_cell_text(cell, str(val), font_size=9, color=c,
                              align=PP_ALIGN.CENTER if ci == 0 else PP_ALIGN.LEFT)

    # 하단 강조 박스
    shape = slide.shapes.add_shape(1, Cm(0.5), Cm(12.5), total_w, Cm(1.8))
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(0x0F, 0x3D, 0x5C)
    shape.line.color.rgb = SKY
    shape.line.width = Pt(2)

    add_textbox(slide, Cm(1), Cm(12.7), total_w - Cm(1), Cm(1.4),
                "⚡ 신규 패턴: 포터블 SSD → AI 모델 휴대 실행 플랫폼으로 진화",
                font_size=14, bold=True, color=SKY, align=PP_ALIGN.CENTER)

    add_footer(slide)
    return slide


def slide5_capacity(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)

    add_textbox(slide, Cm(0.5), Cm(0.3), Cm(32), Cm(1.0),
                "커뮤니티 실제 운용 스펙 — 2TB/4TB 증거",
                font_size=22, bold=True, color=WHITE)

    # 좌측: 용량별 언급 횟수 시각화
    add_textbox(slide, Cm(0.5), Cm(1.5), Cm(15), Cm(1.0),
                "용량별 언급 횟수", font_size=13, bold=True, color=SKY)

    capacity_data = [
        ("1TB ", "████████████████████", "578건", WHITE, False),
        ("2TB ", "████████████████    ", "435건  ← 주력 스펙", SKY, True),
        ("4TB ", "██████              ", "200건  ← AI 전용 구성", RED, True),
        ("500G", "████                ", "149건", LIGHT_GRAY, False),
    ]

    for i, (cap, bar, count, color, bold) in enumerate(capacity_data):
        y = Cm(2.8) + i * Cm(1.4)
        add_textbox(slide, Cm(0.5), y, Cm(1.5), Cm(1.0), cap,
                    font_size=11, bold=bold, color=color)
        add_textbox(slide, Cm(2.0), y, Cm(8.0), Cm(1.0), bar,
                    font_size=10, color=color)
        add_textbox(slide, Cm(10.2), y, Cm(5.0), Cm(1.0), count,
                    font_size=10, bold=bold, color=color)

    # 우측: 실제 사용 맥락 포스트
    add_textbox(slide, Cm(16), Cm(1.5), Cm(16.5), Cm(1.0),
                "실제 사용 맥락 포스트", font_size=13, bold=True, color=SKY)

    posts_data = [
        ("⬆2309", "r/homelab",
         'WD Green 2TB x2 → Plex 서버 기본 구성',
         "Samsung 990 Pro 2TB x2 RAID0 트랜스코딩",
         URLS["plex_2309"]),
        ("⬆509", "r/homelab",
         "My 2026 homelab — 2TB NVMe 업그레이드 목표",
         "want to upgrade to 2TB NVMe storage",
         URLS["homelab_509"]),
        ("⬆491", "r/nvidia",
         "2TB WD_BLACK SN8100 NVMe PCIe 5.0",
         "하이엔드 5090 FE 빌드 스토리지",
         URLS["5090_build"]),
        ("⬆547", "r/LocalLLaMA",
         "128GB VRAM quad R9700 — AI 전용 서버",
         "4x R9700 로컬 AI 추론 전용 빌드",
         URLS["r9700_128gb"]),
    ]

    for i, (score, src, title, desc, url) in enumerate(posts_data):
        y = Cm(2.8) + i * Cm(3.2)

        # 박스 배경
        box_h = Cm(2.9)
        shape = slide.shapes.add_shape(1, Cm(16), y, Cm(16.5), box_h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = CELL_BG
        shape.line.color.rgb = DARK_BLUE
        shape.line.width = Pt(1)

        # score + source
        add_textbox(slide, Cm(16.2), y + Cm(0.1), Cm(16), Cm(0.7),
                    f"{score}  {src}", font_size=9, bold=True, color=SKY)
        # 제목
        add_textbox(slide, Cm(16.2), y + Cm(0.7), Cm(16), Cm(0.9),
                    title, font_size=10, color=WHITE)
        # 설명
        add_textbox(slide, Cm(16.2), y + Cm(1.5), Cm(16), Cm(0.7),
                    desc, font_size=9, color=LIGHT_GRAY)

        # URL을 클릭 가능한 텍스트박스로
        if url and url != "URL 없음":
            txBox = slide.shapes.add_textbox(Cm(16.2), y + Cm(2.1), Cm(16), Cm(0.6))
            tf = txBox.text_frame
            p = tf.paragraphs[0]
            run = p.add_run()
            run.text = "링크 바로가기"
            run.font.size = Pt(8)
            run.font.color.rgb = LINK_BLUE
            rId = slide.part.relate_to(url,
                'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink',
                is_external=True)
            rPr = run._r.get_or_add_rPr()
            hlinkClick = etree.SubElement(rPr, qn('a:hlinkClick'))
            hlinkClick.set(qn('r:id'), rId)

    add_footer(slide)
    return slide


def slide6_ai_tech(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)

    add_textbox(slide, Cm(0.5), Cm(0.3), Cm(32), Cm(1.0),
                "Local AI ↔ SSD 직접 연관 — 기술 근거 포스트",
                font_size=22, bold=True, color=WHITE)

    col_widths = [Cm(1.8), Cm(3.5), Cm(10.5), Cm(9.5), Cm(6.5)]
    headers = ["Score", "커뮤니티", "제목", "기술 요인", "URL"]

    data = [
        ("⬆185", "r/LocalLLaMA",
         "I built a hybrid MoE runtime — 3,324 tok/s",
         "model_weight_size, NVMe 직접 로딩으로 VRAM 오프로드",
         URLS["hybrid_moe"]),
        ("⬆150", "r/LocalLLaMA",
         "Qwen3.5-35B benchmarks on Raspberry Pi 5",
         "model_weight_size, vram_offload 최적화",
         URLS["qwen35"]),
        ("⬆133", "r/LocalLLaMA",
         "My NAS runs 80B LLM at 18 tok/s on iGPU",
         "NVMe에서 직접 모델 스트리밍, GPU 없이 추론",
         URLS["nas_80b"]),
        ("⬆11", "r/LocalLLaMA",
         "A100 vs H100 local storage benchmark",
         "Gen4 NVMe 병목이 cold start 추론 속도 결정",
         URLS["a100_vs_h100"]),
        ("⬆78", "r/LocalLLaMA",
         "oMLX — SSD caching for Apple Silicon",
         "NVMe SSD 페이지 캐시로 모델 오프로드, Apple Silicon",
         URLS["omlx"]),
    ]

    total_w = sum(col_widths)
    tbl = make_table(slide, Cm(0.5), Cm(1.5), total_w, Cm(14.5), 6, 5)

    for ci, w in enumerate(col_widths):
        tbl.columns[ci].width = w

    for ci, h in enumerate(headers):
        cell = tbl.cell(0, ci)
        set_cell_bg(cell, DARK_BLUE)
        set_cell_text(cell, h, font_size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

    for ri, row_data in enumerate(data):
        bg = CELL_BG if ri % 2 == 0 else RGBColor(0x17, 0x20, 0x3A)
        for ci, val in enumerate(row_data):
            cell = tbl.cell(ri + 1, ci)
            set_cell_bg(cell, bg)
            if ci == 4:
                add_hyperlink_to_cell(slide, cell, val, "링크")
            else:
                c = SKY if ci == 0 else WHITE
                set_cell_text(cell, str(val), font_size=9, color=c,
                              align=PP_ALIGN.CENTER if ci == 0 else PP_ALIGN.LEFT)

    add_footer(slide)
    return slide


def slide7_insights(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_slide_bg(slide, NAVY)

    add_textbox(slide, Cm(0.5), Cm(0.3), Cm(32), Cm(1.0),
                "핵심 인사이트 및 시장 시사점",
                font_size=28, bold=True, color=WHITE)

    insights = [
        ("🎯", "2TB = 커뮤니티 표준 스펙",
         '1TB는 출발점, 2TB가 목표 스펙. "현재 500GB → 2TB 업그레이드 고민" 패턴 반복.',
         SKY),
        ("💰", "가격 상승이 구매 트리거",
         '"prices are scaring me", "buy now or wait?" — NAND 가격 상승기에 전환율 높아지는 구조.',
         SKY),
        ("🤖", "AI 모델 운용이 4TB 수요 창출",
         'LocalLLaMA에서 "128GB RAM + 4TB SSD" 조합. 다중 모델 보유 환경이 고용량 드라이브를 필수화.',
         RED),
        ("📦", "Portable SSD 신규 AI 사용 패턴",
         "백업용 → AI 모델 휴대 실행 플랫폼으로 진화 중. VaultAI가 새로운 카테고리 개척.",
         RED),
    ]

    box_w = Cm(14.8)
    box_h = Cm(6.5)
    gap_x = Cm(1.0)
    gap_y = Cm(0.8)

    positions = [
        (Cm(0.5),            Cm(1.8)),
        (Cm(0.5) + box_w + gap_x, Cm(1.8)),
        (Cm(0.5),            Cm(1.8) + box_h + gap_y),
        (Cm(0.5) + box_w + gap_x, Cm(1.8) + box_h + gap_y),
    ]

    for i, (emoji, title, desc, accent) in enumerate(insights):
        x, y = positions[i]
        shape = slide.shapes.add_shape(1, x, y, box_w, box_h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = CELL_BG
        shape.line.color.rgb = accent
        shape.line.width = Pt(2)

        # 이모지 + 제목
        add_textbox(slide, x + Cm(0.3), y + Cm(0.4), box_w - Cm(0.6), Cm(1.2),
                    f"{emoji}  {title}", font_size=15, bold=True, color=accent)
        # 설명
        add_textbox(slide, x + Cm(0.3), y + Cm(1.8), box_w - Cm(0.6), Cm(4.3),
                    desc, font_size=11, color=WHITE)

    add_footer(slide)
    return slide


# ─── 메인 실행 ──────────────────────────────────────────────

def main():
    prs = new_prs()

    print("슬라이드 1 — 표지 생성...")
    slide1_cover(prs)

    print("슬라이드 2 — KPI 생성...")
    slide2_kpi(prs)

    print("슬라이드 3 — NVMe 수요 증거 생성...")
    slide3_nvme(prs)

    print("슬라이드 4 — Portable SSD 생성...")
    slide4_portable(prs)

    print("슬라이드 5 — 2TB/4TB 스펙 근거 생성...")
    slide5_capacity(prs)

    print("슬라이드 6 — AI × SSD 기술 근거 생성...")
    slide6_ai_tech(prs)

    print("슬라이드 7 — 핵심 인사이트 생성...")
    slide7_insights(prs)

    out_path = "/Users/idongseong/Claude/ssd_ai_potential/outputs/SSD_Demand_Analysis.pptx"
    prs.save(out_path)
    print(f"\n✅ 저장 완료: {out_path}")

if __name__ == "__main__":
    main()
