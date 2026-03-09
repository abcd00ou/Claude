"""
Email Reporter — SanDisk B2C Marketing Daily Simulation Report
Gmail SMTP로 HTML 리포트 + PPT 첨부 전송

필요 환경변수:
  GMAIL_APP_PASSWORD  — Gmail 앱 비밀번호 (16자리)
  GMAIL_SENDER        — 발신 계정 (기본: abcd00ou@gmail.com)

Gmail 앱 비밀번호 설정:
  1. myaccount.google.com → 보안 → 2단계 인증 활성화
  2. 앱 비밀번호 생성 (앱: 메일, 기기: Mac)
  3. export GMAIL_APP_PASSWORD="xxxx xxxx xxxx xxxx"
"""
import os
import smtplib
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

RECIPIENT = "abcd00ou@gmail.com"
SENDER = os.getenv("GMAIL_SENDER", "abcd00ou@gmail.com")
BASE_DIR = Path(__file__).parent
PPTX_DIR = BASE_DIR / "outputs" / "pptx"


def _build_html(sim_data: dict, agent_results: dict) -> str:
    """시뮬레이션 결과를 HTML 이메일로 변환."""
    sim_date = sim_data.get("sim_date", "N/A")
    total_rev = sim_data.get("total_rev_m", 0)
    blended_gm = sim_data.get("blended_gm_pct", 0)
    rev = sim_data.get("revenue_m", {})
    gm = sim_data.get("gross_margin_pct", {})
    mshare = sim_data.get("market_share_pct", {})
    nand = sim_data.get("nand_cost_per_gb", {})
    event = sim_data.get("event", {})
    promo = sim_data.get("promo")

    # 에이전트 실행 결과
    success_count = sum(1 for v in agent_results.values() if v)
    total_count = len(agent_results)

    # 이벤트 색상
    EVENT_COLORS = {
        "competitor_price_cut": "#d32f2f",
        "nand_cost_spike":      "#f57c00",
        "market_share_gain":    "#388e3c",
        "promo_opportunity":    "#1976d2",
        "supply_constraint":    "#7b1fa2",
        "none":                 "#757575",
    }
    event_color = EVENT_COLORS.get(event.get("type", "none"), "#757575")
    event_desc = event.get("description", "이벤트 없음")

    # 카테고리 테이블 행
    cat_rows = ""
    cat_labels = {
        "external_ssd": "External SSD",
        "internal_ssd": "Internal SSD",
        "microsd":      "microSD",
    }
    for cat, label in cat_labels.items():
        r = rev.get(cat, 0)
        g = gm.get(cat, 0)
        ms = mshare.get(cat, 0)
        cat_rows += f"""
        <tr>
          <td style="padding:8px 12px;border-bottom:1px solid #eee;font-weight:600">{label}</td>
          <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:right">${r:.1f}M</td>
          <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:right">{g:.1f}%</td>
          <td style="padding:8px 12px;border-bottom:1px solid #eee;text-align:right">{ms:.1f}%</td>
        </tr>"""

    # NAND 원가 행
    nand_rows = ""
    for gen, cost in nand.items():
        nand_rows += f"""
        <tr>
          <td style="padding:6px 12px;border-bottom:1px solid #eee">{gen}</td>
          <td style="padding:6px 12px;border-bottom:1px solid #eee;text-align:right">${cost:.4f}/GB</td>
        </tr>"""

    # 에이전트 결과 행
    agent_rows = ""
    agent_labels = {
        "production": "생산 에이전트",
        "supply":     "공급 에이전트",
        "demand_excel": "수요예측 (Excel)",
        "demand_pptx_vp": "수요예측 (PPT)",
        "strategy_excel": "마케팅 전략 (Excel)",
        "strategy_pptx_vp": "마케팅 전략 (PPT)",
        "marcom_pptx_vp": "MarCom (PPT)",
        "product_mix_pptx_vp": "Product Mix (PPT)",
    }
    for key, label in agent_labels.items():
        status = agent_results.get(key)
        badge = "✅" if status else "❌"
        agent_rows += f"""
        <tr>
          <td style="padding:6px 12px;border-bottom:1px solid #eee">{label}</td>
          <td style="padding:6px 12px;border-bottom:1px solid #eee;text-align:center">{badge}</td>
        </tr>"""

    # 프로모 섹션
    promo_section = ""
    if promo:
        promo_type = "Holiday" if promo["type"] == "holiday" else "BTS"
        promo_section = f"""
        <div style="background:#e8f5e9;border-left:4px solid #4caf50;padding:12px 16px;margin:16px 0;border-radius:4px">
          <strong>🎯 프로모션 기회: {promo_type}</strong><br>
          투자: ${promo['invest_m']:.1f}M &nbsp;|&nbsp;
          예상 추가 매출: ${promo['incremental_rev_m']:.1f}M &nbsp;|&nbsp;
          ROI: {promo['roi']:.2f}×
        </div>"""

    now_str = datetime.now().strftime("%Y-%m-%d %H:%M KST")

    html = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8">
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; margin:0; background:#f5f7fa; }}
  .container {{ max-width:680px; margin:20px auto; background:#fff; border-radius:8px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,.1); }}
  .header {{ background:linear-gradient(135deg,#1428A0,#0a1670); color:#fff; padding:28px 32px; }}
  .header h1 {{ margin:0 0 6px; font-size:22px; font-weight:700; }}
  .header p {{ margin:0; opacity:.8; font-size:13px; }}
  .body {{ padding:28px 32px; }}
  .kpi-grid {{ display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:24px; }}
  .kpi {{ background:#f8f9ff; border:1px solid #e0e4ff; border-radius:6px; padding:14px 16px; text-align:center; }}
  .kpi-value {{ font-size:24px; font-weight:700; color:#1428A0; }}
  .kpi-label {{ font-size:11px; color:#666; margin-top:4px; }}
  table {{ width:100%; border-collapse:collapse; margin-bottom:16px; }}
  th {{ background:#f0f2ff; padding:8px 12px; text-align:left; font-size:12px; color:#444; font-weight:600; }}
  th:not(:first-child) {{ text-align:right; }}
  .section-title {{ font-size:14px; font-weight:700; color:#1428A0; margin:20px 0 8px; text-transform:uppercase; letter-spacing:.5px; }}
  .event-badge {{ display:inline-block; background:{event_color}; color:#fff; border-radius:4px; padding:4px 10px; font-size:12px; font-weight:600; }}
  .footer {{ background:#f0f2ff; padding:16px 32px; font-size:11px; color:#888; }}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <h1>SanDisk B2C Marketing Intelligence</h1>
    <p>시뮬레이션 월: <strong>{sim_date}</strong> &nbsp;|&nbsp; 실행 시각: {now_str}</p>
    <p style="margin-top:6px">에이전트 실행: {success_count}/{total_count} 성공</p>
  </div>

  <div class="body">

    <!-- KPI -->
    <div class="kpi-grid">
      <div class="kpi">
        <div class="kpi-value">${total_rev:.1f}M</div>
        <div class="kpi-label">월 총 매출</div>
      </div>
      <div class="kpi">
        <div class="kpi-value">{blended_gm:.1f}%</div>
        <div class="kpi-label">블렌딩 GM%</div>
      </div>
      <div class="kpi">
        <div class="kpi-value">{mshare.get('external_ssd', 0):.1f}%</div>
        <div class="kpi-label">External SSD 점유율</div>
      </div>
    </div>

    <!-- 이벤트 -->
    <div class="section-title">이번 달 주요 이벤트</div>
    <div style="margin-bottom:16px">
      <span class="event-badge">{event.get('type','none').replace('_',' ').upper()}</span>
      <span style="margin-left:10px;color:#333;font-size:14px">{event_desc if event_desc else '특이사항 없음'}</span>
    </div>

    {promo_section}

    <!-- 카테고리 실적 -->
    <div class="section-title">카테고리별 실적</div>
    <table>
      <tr>
        <th>카테고리</th>
        <th>월 매출</th>
        <th>GM%</th>
        <th>시장점유율</th>
      </tr>
      {cat_rows}
    </table>

    <!-- NAND 원가 -->
    <div class="section-title">NAND 원가 현황</div>
    <table>
      <tr><th>NAND 세대</th><th>$/GB</th></tr>
      {nand_rows}
    </table>

    <!-- 에이전트 실행 결과 -->
    <div class="section-title">에이전트 실행 결과</div>
    <table>
      <tr><th>에이전트</th><th style="text-align:center">상태</th></tr>
      {agent_rows}
    </table>

    <!-- 첨부 안내 -->
    <div style="background:#fff8e1;border:1px solid #ffe082;border-radius:6px;padding:12px 16px;margin-top:16px;font-size:13px">
      📎 <strong>VP-급 PPT 4종 첨부</strong>: 수요예측 · 마케팅전략 · MarCom · Product Mix<br>
      각 파일을 열어 슬라이드별 전략 세부 내용을 확인하세요.
    </div>

  </div>

  <div class="footer">
    이 리포트는 SanDisk B2C Marketing AI Agent System이 자동 생성한 시뮬레이션 자료입니다.<br>
    1시간 = 1개월 시뮬레이션 | 실제 데이터와 다를 수 있음 | {now_str}
  </div>
</div>
</body>
</html>"""
    return html


def send_report(sim_data: dict, agent_results: dict) -> bool:
    """
    시뮬레이션 리포트 이메일 전송.

    필요:
      GMAIL_APP_PASSWORD 환경변수 설정
      (export GMAIL_APP_PASSWORD="abcd efgh ijkl mnop")
    """
    app_password = os.getenv("GMAIL_APP_PASSWORD", "")
    if not app_password:
        print("  [Email] ⚠️  GMAIL_APP_PASSWORD 환경변수 미설정 — 이메일 전송 건너뜀")
        print("  [Email]    설정 방법: export GMAIL_APP_PASSWORD='xxxx xxxx xxxx xxxx'")
        return False

    sim_date = sim_data.get("sim_date", "N/A")
    subject = f"[SanDisk Marketing AI] {sim_date} 월간 리포트 — Rev ${sim_data.get('total_rev_m', 0):.1f}M"

    msg = MIMEMultipart("mixed")
    msg["From"]    = SENDER
    msg["To"]      = RECIPIENT
    msg["Subject"] = subject

    # HTML 본문
    html_content = _build_html(sim_data, agent_results)
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    # PPT 첨부
    attached_count = 0
    pptx_files = list(PPTX_DIR.glob("*.pptx")) if PPTX_DIR.exists() else []
    for pptx in sorted(pptx_files):
        try:
            with open(pptx, "rb") as f:
                part = MIMEBase("application", "vnd.openxmlformats-officedocument.presentationml.presentation")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment",
                            filename=f"{sim_date}_{pptx.name}")
            msg.attach(part)
            attached_count += 1
        except Exception as e:
            print(f"  [Email] PPT 첨부 실패 {pptx.name}: {e}")

    # 전송
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(SENDER, app_password.replace(" ", ""))
            server.sendmail(SENDER, RECIPIENT, msg.as_string())
        print(f"  [Email] ✅ 전송 완료 → {RECIPIENT} | PPT {attached_count}개 첨부")
        return True
    except smtplib.SMTPAuthenticationError:
        print("  [Email] ❌ 인증 실패 — Gmail 앱 비밀번호를 확인하세요")
        print("  [Email]    https://myaccount.google.com/apppasswords")
        return False
    except Exception as e:
        print(f"  [Email] ❌ 전송 실패: {e}")
        return False


if __name__ == "__main__":
    # 테스트용
    dummy_sim = {
        "sim_date": "2025-03",
        "total_rev_m": 285.4,
        "blended_gm_pct": 48.2,
        "revenue_m": {"external_ssd": 82, "internal_ssd": 65, "microsd": 138},
        "gross_margin_pct": {"external_ssd": 45.1, "internal_ssd": 39.2, "microsd": 57.8},
        "market_share_pct": {"external_ssd": 22.3, "internal_ssd": 17.5, "microsd": 32.1},
        "nand_cost_per_gb": {"BiCS5": 0.053, "BiCS6": 0.040, "BiCS8": 0.037},
        "event": {"type": "promo_opportunity", "description": "프로모션 기회 (예상 ROI 2.8×)"},
        "promo": None,
    }
    dummy_agents = {k: True for k in ["production", "supply", "demand_excel", "demand_pptx_vp",
                                       "strategy_excel", "strategy_pptx_vp", "marcom_pptx_vp",
                                       "product_mix_pptx_vp"]}
    send_report(dummy_sim, dummy_agents)
