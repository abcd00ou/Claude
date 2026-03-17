"""
report_agent.py — HTML 분석 리포트 생성
"""
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [REPORT] %(message)s")
log = logging.getLogger(__name__)

SIGNAL_LABELS = {
    "buy_intent":     "구매 의향",
    "upgrade_intent": "교체/확장 의향",
    "technical_need": "기술적 필요",
    "co_mention":     "동시 언급",
    "no_signal":      "무관",
}
SIGNAL_COLORS = {
    "buy_intent":     "#ef4444",
    "upgrade_intent": "#f97316",
    "technical_need": "#3b82f6",
    "co_mention":     "#a855f7",
    "no_signal":      "#d1d5db",
}
FACTOR_LABELS = {
    "model_weight_size": "모델 파일 용량",
    "vram_offload":      "VRAM 오프로드",
    "swap_speed":        "스왑/가상메모리 속도",
    "io_bottleneck":     "I/O 병목 (로딩 속도)",
    "portability":       "포터블 사용 (여러 PC)",
    "capacity":          "단순 용량 부족",
    "speed_matters":     "NVMe 속도 중요성",
}


def answer_research_questions(result: dict) -> dict:
    """3대 질문에 대한 직접 답변 생성"""
    total   = result["total_posts"]
    signals = result["demand_signals"]
    demand  = result["demand_total"]
    rate    = result["demand_rate_pct"]

    # Q1: 수요 존재 여부
    buy      = signals.get("buy_intent", 0)
    upgrade  = signals.get("upgrade_intent", 0)
    tech     = signals.get("technical_need", 0)
    q1_yes   = demand > 0
    q1_level = "강함" if rate > 10 else "중간" if rate > 3 else "약함"
    q1_answer = f"""{"✅ 존재함" if q1_yes else "❌ 미확인"} (수요 신호 포스트 {demand}개 / 전체 {total}개, {rate}%)
구매 의향: {buy}건 | 교체/확장 의향: {upgrade}건 | 기술적 필요: {tech}건
신호 강도: <strong>{q1_level}</strong>"""

    # Q2: 직접 연관성
    tech_rate = round(tech / total * 100, 1) if total else 0
    co        = signals.get("co_mention", 0)
    q2_answer = f"""{"✅ 직접 연관 확인됨" if tech > 20 else "⚠️ 부분 연관" if tech > 5 else "❌ 연관 약함"}
기술적 필요 명시 포스트: {tech}개 ({tech_rate}%)
SSD+LLM 동시 언급: {co}개 추가
→ Local LLM 실행이 SSD 필요성을 유발한다는 직접적 언급 {"다수 존재" if tech > 20 else "일부 존재" if tech > 5 else "소수"}"""

    # Q3: 기술 근거
    factors = result.get("technical_factors", {})
    top_factors = sorted(factors.items(), key=lambda x: -x[1])[:5]
    factor_lines = "\n".join([
        f"  {i+1}. {FACTOR_LABELS.get(f, f)}: {c}건"
        for i, (f, c) in enumerate(top_factors)
    ])
    q3_answer = f"""상위 기술 근거:\n{factor_lines if factor_lines else "  데이터 수집 중"}"""

    return {
        "q1": {"question": "SSD 교체·확장·구매 수요가 존재하는가?",     "answer": q1_answer},
        "q2": {"question": "Local LLM과 SSD가 직접 연관되어 언급되는가?", "answer": q2_answer},
        "q3": {"question": "어떤 기술적 근거로 SSD가 필요하다고 인식하는가?", "answer": q3_answer},
    }


def build_html(result: dict) -> str:
    signals = result["demand_signals"]
    factors = result.get("technical_factors", {})
    qa      = answer_research_questions(result)
    top_posts = result.get("top_demand_posts", [])[:20]
    by_source = result.get("by_source", {})
    portable  = result.get("portable_ssd_mentions", 0)
    portable_pct = result.get("portable_ssd_pct", 0)
    gen_time  = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    # 도넛 차트용 데이터
    chart_labels = [SIGNAL_LABELS.get(k, k) for k in signals]
    chart_values = list(signals.values())
    chart_colors = [SIGNAL_COLORS.get(k, "#999") for k in signals]

    # 기술 근거 바 차트
    factor_items = sorted(factors.items(), key=lambda x: -x[1])
    factor_labels_js = json.dumps([FACTOR_LABELS.get(k, k) for k, _ in factor_items])
    factor_values_js = json.dumps([v for _, v in factor_items])

    # 소스별 테이블
    source_rows = ""
    for src, counts in sorted(by_source.items(), key=lambda x: -x[1]["demand"])[:15]:
        demand_rate = round(counts["demand"] / counts["total"] * 100, 1) if counts["total"] else 0
        bar_w = min(demand_rate * 5, 100)
        source_rows += f"""
        <tr>
          <td><code>{src}</code></td>
          <td class="num">{counts['total']}</td>
          <td class="num">{counts['demand']}</td>
          <td>
            <div class="bar-bg"><div class="bar-fill" style="width:{bar_w}%"></div></div>
            <span class="num">{demand_rate}%</span>
          </td>
        </tr>"""

    # 상위 포스트 테이블
    signal_badge = {
        "buy_intent":     '<span class="badge badge-buy">구매의향</span>',
        "upgrade_intent": '<span class="badge badge-upgrade">교체의향</span>',
        "technical_need": '<span class="badge badge-tech">기술필요</span>',
    }
    post_rows = ""
    for p in top_posts:
        sig   = p.get("signal", "")
        badge = signal_badge.get(sig, "")
        title = p.get("title", "")[:80]
        quote = p.get("key_quote", "")
        factors_str = ", ".join(FACTOR_LABELS.get(f, f) for f in p.get("technical_factors", []))
        post_rows += f"""
        <tr>
          <td>{badge}</td>
          <td><a href="{p.get('url','#')}" target="_blank">{title}</a>
              {"<br><small class='quote'>\"" + quote + "\"</small>" if quote else ""}</td>
          <td><small>{p.get('source','')}</small></td>
          <td class="num">{p.get('score', 0)}</td>
          <td><small>{factors_str}</small></td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>SSD × Local AI 수요 분석 리포트</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
          background: #0f172a; color: #e2e8f0; line-height: 1.6; }}
  .header {{ background: linear-gradient(135deg, #1e3a5f, #0f172a);
             padding: 2rem; border-bottom: 1px solid #1e40af; }}
  .header h1 {{ font-size: 1.8rem; color: #60a5fa; margin-bottom: 0.3rem; }}
  .header .meta {{ color: #94a3b8; font-size: 0.85rem; }}
  .container {{ max-width: 1200px; margin: 0 auto; padding: 1.5rem; }}
  .grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-bottom: 1.5rem; }}
  .grid-2 {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-bottom: 1.5rem; }}
  .card {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.2rem; }}
  .card h2 {{ font-size: 1rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 1rem; }}
  .stat-num {{ font-size: 2.5rem; font-weight: 700; color: #60a5fa; }}
  .stat-label {{ font-size: 0.8rem; color: #64748b; margin-top: 0.2rem; }}
  .qa-block {{ background: #1e293b; border: 1px solid #334155; border-radius: 12px; padding: 1.2rem; margin-bottom: 1rem; }}
  .qa-block h3 {{ color: #60a5fa; font-size: 1rem; margin-bottom: 0.5rem; }}
  .qa-block pre {{ white-space: pre-wrap; font-family: inherit; color: #cbd5e1; font-size: 0.9rem; }}
  .chart-wrap {{ position: relative; height: 260px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
  th {{ background: #0f172a; color: #94a3b8; padding: 0.5rem 0.7rem; text-align: left; }}
  td {{ padding: 0.45rem 0.7rem; border-bottom: 1px solid #1e293b; vertical-align: top; }}
  tr:hover td {{ background: #162032; }}
  .num {{ text-align: right; font-variant-numeric: tabular-nums; }}
  code {{ background: #0f172a; padding: 0.1em 0.3em; border-radius: 3px; font-size: 0.8rem; color: #7dd3fc; }}
  a {{ color: #60a5fa; text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  .badge {{ padding: 0.15em 0.5em; border-radius: 4px; font-size: 0.7rem; font-weight: 600; white-space: nowrap; }}
  .badge-buy     {{ background: #7f1d1d; color: #fca5a5; }}
  .badge-upgrade {{ background: #7c2d12; color: #fdba74; }}
  .badge-tech    {{ background: #1e3a8a; color: #93c5fd; }}
  .bar-bg {{ display: inline-block; width: 80px; height: 6px; background: #334155; border-radius: 3px; vertical-align: middle; margin-right: 4px; }}
  .bar-fill {{ height: 100%; background: #3b82f6; border-radius: 3px; }}
  .quote {{ color: #64748b; font-style: italic; }}
  .highlight {{ background: #1e3a5f; border: 1px solid #1e40af; border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }}
  .highlight p {{ color: #93c5fd; font-size: 0.9rem; }}
  .section-title {{ color: #64748b; font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.1em; margin: 1.5rem 0 0.7rem; }}
  .portable-card {{ background: linear-gradient(135deg, #0c4a6e, #1e293b); border: 1px solid #0369a1; }}
</style>
</head>
<body>

<div class="header">
  <h1>SSD × Local AI 수요 분석 리포트</h1>
  <div class="meta">생성: {gen_time} &nbsp;|&nbsp; 분석 포스트: {result['total_posts']:,}개 &nbsp;|&nbsp; 커뮤니티: Reddit LocalLLaMA, LocalAI 외 15개 + HackerNews</div>
</div>

<div class="container">

  <!-- KPI 카드 -->
  <p class="section-title">핵심 지표</p>
  <div class="grid-3">
    <div class="card">
      <h2>수집 포스트</h2>
      <div class="stat-num">{result['total_posts']:,}</div>
      <div class="stat-label">누적 분석 포스트 수</div>
    </div>
    <div class="card">
      <h2>수요 신호 포스트</h2>
      <div class="stat-num" style="color:#ef4444">{result['demand_total']:,}</div>
      <div class="stat-label">전체의 {result['demand_rate_pct']}%</div>
    </div>
    <div class="card portable-card">
      <h2>포터블 SSD 언급</h2>
      <div class="stat-num" style="color:#38bdf8">{portable:,}</div>
      <div class="stat-label">전체의 {portable_pct}%</div>
    </div>
  </div>

  <!-- 3대 질문 답변 -->
  <p class="section-title">3대 핵심 질문 답변</p>
  <div class="qa-block">
    <h3>Q1. {qa['q1']['question']}</h3>
    <pre>{qa['q1']['answer']}</pre>
  </div>
  <div class="qa-block">
    <h3>Q2. {qa['q2']['question']}</h3>
    <pre>{qa['q2']['answer']}</pre>
  </div>
  <div class="qa-block">
    <h3>Q3. {qa['q3']['question']}</h3>
    <pre>{qa['q3']['answer']}</pre>
  </div>

  <!-- 차트 -->
  <p class="section-title">수요 신호 분포</p>
  <div class="grid-2">
    <div class="card">
      <h2>수요 신호 분류</h2>
      <div class="chart-wrap">
        <canvas id="signalChart"></canvas>
      </div>
    </div>
    <div class="card">
      <h2>기술 근거 TOP 요인</h2>
      <div class="chart-wrap">
        <canvas id="factorChart"></canvas>
      </div>
    </div>
  </div>

  <!-- 소스별 분석 -->
  <p class="section-title">커뮤니티별 수요 신호</p>
  <div class="card">
    <table>
      <thead><tr><th>커뮤니티</th><th class="num">수집</th><th class="num">수요신호</th><th>수요율</th></tr></thead>
      <tbody>{source_rows}</tbody>
    </table>
  </div>

  <!-- 상위 포스트 -->
  <p class="section-title">수요 신호 상위 포스트 (score 순)</p>
  <div class="card">
    <table>
      <thead><tr><th>분류</th><th>제목 / 인용</th><th>출처</th><th class="num">Score</th><th>기술근거</th></tr></thead>
      <tbody>{post_rows if post_rows else '<tr><td colspan="5" style="text-align:center;color:#64748b">수요 신호 포스트 없음 — 크롤링 데이터 확인 필요</td></tr>'}</tbody>
    </table>
  </div>

  <!-- 마케팅 시사점 -->
  <p class="section-title">마케팅 시사점 (WD/SanDisk)</p>
  <div class="highlight">
    <p>• <strong>내장 SSD (WD_BLACK SN850X/SN8100)</strong>: VRAM 오프로드·스왑 속도 민감 유저 → NVMe 고속 I/O 메시지</p>
    <p>• <strong>포터블 SSD (SanDisk Extreme)</strong>: 모델 파일을 여러 기기에서 이동 실행하는 유저 → "AI 모델 포터블 스토리지" 포지셔닝</p>
    <p>• <strong>용량 전략</strong>: 7B~70B 모델 복수 보유 트렌드 → 2TB/4TB 대용량 SKU 강조</p>
    <p>• <strong>타깃 채널</strong>: r/LocalLLaMA, r/OllamaAI, r/SelfHosted — 직접 커뮤니티 engagement 가능</p>
  </div>

</div>

<script>
// 수요 신호 도넛 차트
new Chart(document.getElementById('signalChart'), {{
  type: 'doughnut',
  data: {{
    labels: {json.dumps(chart_labels)},
    datasets: [{{ data: {json.dumps(chart_values)}, backgroundColor: {json.dumps(chart_colors)}, borderWidth: 0 }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ position: 'right', labels: {{ color: '#94a3b8', font: {{ size: 11 }} }} }} }}
  }}
}});

// 기술 근거 바 차트
new Chart(document.getElementById('factorChart'), {{
  type: 'bar',
  data: {{
    labels: {factor_labels_js},
    datasets: [{{ data: {factor_values_js}, backgroundColor: '#3b82f6', borderRadius: 4 }}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false, indexAxis: 'y',
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      x: {{ ticks: {{ color: '#94a3b8' }}, grid: {{ color: '#1e293b' }} }},
      y: {{ ticks: {{ color: '#94a3b8', font: {{ size: 10 }} }}, grid: {{ display: false }} }}
    }}
  }}
}});
</script>
</body>
</html>"""


class ReportAgent:
    def __init__(self):
        self.analysis_file = config.ANALYSIS_FILE
        self.output_dir    = config.OUTPUT_DIR

    def run(self) -> Optional[Path]:
        if not self.analysis_file.exists():
            log.error("analysis_results.json 없음 — 분석기 먼저 실행하세요")
            return None

        with open(self.analysis_file, encoding="utf-8") as f:
            history = json.load(f)

        if not history:
            log.error("분석 결과 없음")
            return None

        result = history[-1]  # 최신 분석 결과 사용
        html   = build_html(result)

        ts       = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M")
        out_path = self.output_dir / f"ssd_ai_demand_{ts}.html"
        out_path.write_text(html, encoding="utf-8")

        # 최신본 고정 링크
        latest = self.output_dir / "latest.html"
        latest.write_text(html, encoding="utf-8")

        log.info(f"리포트 생성: {out_path}")
        return out_path


if __name__ == "__main__":
    agent = ReportAgent()
    path  = agent.run()
    if path:
        import subprocess
        subprocess.Popen(["open", str(path)])
