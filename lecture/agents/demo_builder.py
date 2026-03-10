"""
lecture/agents/demo_builder.py
강의 실전 데모 HTML 예시 파일 생성

데모 1: 제품 소개 랜딩 페이지 (AI가 만든 예시)
데모 2: 마케팅 이미지 프롬프트 가이드 페이지
데모 3: AI 제안서 초안 비교 (Before/After)
데모 4: 에이전트 워크플로우 다이어그램
데모 5: "이 강의도 AI가 만들었다" 메타 데모
"""

import sys
import pathlib
from datetime import datetime

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from config import OUTPUT_DIR

DEMO_DIR = OUTPUT_DIR / "demos"
DEMO_DIR.mkdir(exist_ok=True)


# ──────────────────────────────────────────────
# 공통 CSS
# ──────────────────────────────────────────────
BASE_CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: 'Pretendard', 'Apple SD Gothic Neo', -apple-system, sans-serif; }
.tag { display: inline-block; padding: 4px 12px; border-radius: 20px; font-size: 12px; font-weight: 700; }
.btn {
  display: inline-block; padding: 14px 32px; border-radius: 8px;
  font-size: 16px; font-weight: 700; text-decoration: none; cursor: pointer;
  border: none; transition: transform 0.2s, box-shadow 0.2s;
}
.btn:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.2); }
"""


# ──────────────────────────────────────────────
# 데모 1: 제품 소개 랜딩 페이지
# ──────────────────────────────────────────────
def build_demo1_landing() -> str:
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>데모 1 — AI가 30초 만에 만든 제품 랜딩 페이지</title>
<style>
{BASE_CSS}
:root {{
  --primary: #1565C0;
  --accent: #FF6F00;
  --dark: #0D1B2A;
}}
body {{ background: #f8f9fa; color: #212121; }}

/* 배너 */
.demo-banner {{
  background: linear-gradient(135deg, #FF6F00, #FF8F00);
  color: #fff; text-align: center; padding: 12px;
  font-size: 14px; font-weight: 600;
}}

/* 히어로 */
.hero {{
  background: linear-gradient(135deg, var(--dark) 0%, #1565C0 100%);
  color: #fff; padding: 100px 40px;
  text-align: center; position: relative; overflow: hidden;
}}
.hero::before {{
  content: ''; position: absolute; top: -50%; left: -50%;
  width: 200%; height: 200%;
  background: radial-gradient(circle, rgba(255,111,0,0.1) 0%, transparent 60%);
}}
.hero h1 {{ font-size: 52px; font-weight: 900; margin-bottom: 20px; line-height: 1.2; }}
.hero h1 span {{ color: #FF8F00; }}
.hero p {{ font-size: 20px; opacity: 0.85; max-width: 600px; margin: 0 auto 40px; }}
.hero-badge {{
  background: rgba(255,255,255,0.1); backdrop-filter: blur(10px);
  border: 1px solid rgba(255,255,255,0.2); border-radius: 50px;
  padding: 8px 20px; font-size: 13px; margin-bottom: 30px; display: inline-block;
}}
.btn-primary {{ background: #FF6F00; color: #fff; }}
.btn-outline {{ background: transparent; color: #fff; border: 2px solid #fff; margin-left: 12px; }}

/* 특징 섹션 */
.features {{ max-width: 1100px; margin: 80px auto; padding: 0 40px; }}
.features h2 {{ text-align: center; font-size: 36px; color: var(--dark); margin-bottom: 16px; }}
.features-sub {{ text-align: center; color: #757575; margin-bottom: 60px; font-size: 18px; }}
.features-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }}
.feature-card {{
  background: #fff; border-radius: 16px; padding: 36px 28px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.06); transition: transform 0.2s;
}}
.feature-card:hover {{ transform: translateY(-4px); }}
.feature-icon {{ font-size: 40px; margin-bottom: 16px; }}
.feature-card h3 {{ font-size: 18px; font-weight: 700; color: var(--dark); margin-bottom: 10px; }}
.feature-card p {{ color: #616161; font-size: 14px; line-height: 1.7; }}

/* 비교 섹션 */
.comparison {{ background: var(--dark); padding: 80px 40px; }}
.comparison h2 {{ text-align: center; color: #fff; font-size: 36px; margin-bottom: 12px; }}
.comparison-sub {{ text-align: center; color: #90A4AE; margin-bottom: 60px; }}
.compare-grid {{ max-width: 900px; margin: 0 auto; display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
.compare-card {{ background: #1A2744; border-radius: 16px; padding: 32px; }}
.compare-card.before {{ border-top: 4px solid #EF5350; }}
.compare-card.after {{ border-top: 4px solid #66BB6A; }}
.compare-card h3 {{ font-size: 22px; font-weight: 700; margin-bottom: 24px; }}
.compare-card.before h3 {{ color: #EF9A9A; }}
.compare-card.after h3 {{ color: #A5D6A7; }}
.compare-item {{ padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.06); }}
.compare-item:last-child {{ border-bottom: none; }}
.compare-item .label {{ font-size: 12px; color: #78909C; margin-bottom: 4px; }}
.compare-item .value {{ color: #ECEFF1; font-size: 14px; }}

/* 프롬프트 섹션 */
.prompt-section {{ max-width: 900px; margin: 80px auto; padding: 0 40px; }}
.prompt-section h2 {{ font-size: 32px; color: var(--dark); margin-bottom: 12px; }}
.prompt-section p {{ color: #757575; margin-bottom: 32px; }}
.prompt-box {{
  background: #0D1B2A; border-radius: 12px; padding: 28px 32px;
  border-left: 4px solid #FF6F00;
}}
.prompt-label {{ color: #FF8F00; font-size: 12px; font-weight: 700; margin-bottom: 12px; }}
.prompt-text {{ color: #ECEFF1; font-size: 14px; line-height: 1.8; font-family: monospace; }}

/* CTA */
.cta {{ background: linear-gradient(135deg, #FF6F00, #E65100); padding: 80px 40px; text-align: center; }}
.cta h2 {{ color: #fff; font-size: 36px; font-weight: 900; margin-bottom: 16px; }}
.cta p {{ color: rgba(255,255,255,0.85); font-size: 18px; margin-bottom: 40px; }}
.btn-white {{ background: #fff; color: #E65100; }}

/* 푸터 */
footer {{
  background: var(--dark); color: #546E7A; text-align: center;
  padding: 24px; font-size: 13px;
}}
</style>
</head>
<body>

<div class="demo-banner">
  🤖 이 페이지는 AI(Claude)가 약 30초 만에 생성한 데모입니다 — AI 워크플로우 변화 강의용 예시
</div>

<section class="hero">
  <div class="hero-badge">⚡ NEW — AI 시대의 스토리지 솔루션</div>
  <h1>데이터를 <span>더 빠르게</span><br>더 안전하게</h1>
  <p>차세대 NVMe SSD로 업무 생산성을 2배 높이세요.<br>AI 워크플로우에 최적화된 성능.</p>
  <a href="#" class="btn btn-primary">지금 시작하기</a>
  <a href="#" class="btn btn-outline">사양 보기</a>
</section>

<section class="features">
  <h2>왜 선택해야 할까요?</h2>
  <p class="features-sub">3가지 핵심 이유</p>
  <div class="features-grid">
    <div class="feature-card">
      <div class="feature-icon">⚡</div>
      <h3>초고속 전송</h3>
      <p>최대 7,450MB/s 읽기 속도로 대용량 파일도 눈 깜짝할 새에. AI 모델 로딩 시간 80% 단축.</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon">🛡️</div>
      <h3>데이터 보안</h3>
      <p>AES 256비트 암호화 및 충격 방지 설계로 소중한 데이터를 완벽하게 보호합니다.</p>
    </div>
    <div class="feature-card">
      <div class="feature-icon">🔋</div>
      <h3>저전력 설계</h3>
      <p>업계 최저 전력 소비로 노트북 배터리 수명을 15% 연장. 이동 중에도 효율적으로.</p>
    </div>
  </div>
</section>

<section class="comparison">
  <h2>Before / After</h2>
  <p class="comparison-sub">기존 SSD vs AI 시대 SSD</p>
  <div class="compare-grid">
    <div class="compare-card before">
      <h3>😓 기존 방식</h3>
      <div class="compare-item">
        <div class="label">읽기 속도</div>
        <div class="value">3,500 MB/s</div>
      </div>
      <div class="compare-item">
        <div class="label">AI 모델 로딩</div>
        <div class="value">약 45초</div>
      </div>
      <div class="compare-item">
        <div class="label">대용량 파일 전송</div>
        <div class="value">100GB = 약 29초</div>
      </div>
      <div class="compare-item">
        <div class="label">배터리 소비</div>
        <div class="value">높음 (4.5W)</div>
      </div>
    </div>
    <div class="compare-card after">
      <h3>🚀 신제품 적용</h3>
      <div class="compare-item">
        <div class="label">읽기 속도</div>
        <div class="value">7,450 MB/s ↑ 2.1배</div>
      </div>
      <div class="compare-item">
        <div class="label">AI 모델 로딩</div>
        <div class="value">약 9초 ↓ 80%</div>
      </div>
      <div class="compare-item">
        <div class="label">대용량 파일 전송</div>
        <div class="value">100GB = 약 14초 ↑</div>
      </div>
      <div class="compare-item">
        <div class="label">배터리 소비</div>
        <div class="value">낮음 (2.8W) ↓ 38%</div>
      </div>
    </div>
  </div>
</section>

<section class="prompt-section">
  <h2>이 페이지를 만든 프롬프트</h2>
  <p>아래 프롬프트 하나로 이 랜딩 페이지가 생성되었습니다.</p>
  <div class="prompt-box">
    <div class="prompt-label">USER PROMPT →</div>
    <div class="prompt-text">
"NVMe SSD 제품 소개 랜딩 페이지를 HTML로 만들어줘.<br>
히어로 섹션에 제품 핵심 가치 3가지, Before/After 성능 비교,<br>
구매 유도 CTA 포함. 다크 배경에 오렌지 액센트 컬러 사용.<br>
B2C 소비자 대상, 감성적이면서도 데이터 기반 설득력 있게."
    </div>
  </div>
</section>

<section class="cta">
  <h2>지금 AI로 시작하세요</h2>
  <p>이런 페이지, 이제는 30초면 만들 수 있습니다.</p>
  <a href="#" class="btn btn-white">무료로 시작하기</a>
</section>

<footer>
  <p>🤖 AI Workflow Lecture Demo — Generated by Claude in ~30 seconds | {datetime.now().strftime('%Y-%m-%d')}</p>
</footer>

</body>
</html>"""
    out = DEMO_DIR / "demo1_landing_page.html"
    out.write_text(html, encoding="utf-8")
    return str(out)


# ──────────────────────────────────────────────
# 데모 2: 마케팅 이미지 프롬프트 가이드
# ──────────────────────────────────────────────
def build_demo2_image_prompts() -> str:
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>데모 2 — AI 이미지 생성 프롬프트 가이드</title>
<style>
{BASE_CSS}
body {{ background: #0F0F23; color: #E0E0E0; font-family: 'Apple SD Gothic Neo', sans-serif; }}
.header {{ background: linear-gradient(135deg, #1a1a3e, #0F0F23); padding: 60px 40px; text-align: center; border-bottom: 1px solid rgba(255,255,255,0.1); }}
.header h1 {{ font-size: 40px; font-weight: 900; color: #fff; margin-bottom: 12px; }}
.header h1 span {{ background: linear-gradient(90deg, #FF6F00, #FF8F00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
.header p {{ color: #9E9E9E; font-size: 18px; }}
.container {{ max-width: 1100px; margin: 0 auto; padding: 60px 40px; }}

.section-title {{ font-size: 28px; font-weight: 700; color: #fff; margin: 60px 0 8px; }}
.section-sub {{ color: #757575; margin-bottom: 32px; }}

/* 프롬프트 카드 */
.prompt-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-bottom: 60px; }}
.prompt-card {{ background: #1A1A3E; border-radius: 12px; overflow: hidden; }}
.card-preview {{
  height: 180px; display: flex; align-items: center; justify-content: center;
  font-size: 60px; position: relative;
}}
.card-body {{ padding: 24px; }}
.card-tag {{ font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 20px; margin-bottom: 10px; display: inline-block; }}
.card-body h3 {{ font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 12px; }}
.prompt-text-sm {{
  background: #0F0F23; border-radius: 8px; padding: 12px 16px;
  font-size: 12px; color: #B0BEC5; font-family: monospace;
  line-height: 1.6; border-left: 3px solid #FF6F00;
}}
.tip {{ color: #81C784; font-size: 12px; margin-top: 10px; }}

/* TRIE 공식 */
.trie {{ background: linear-gradient(135deg, #1565C0, #0D47A1); border-radius: 16px; padding: 40px; margin-bottom: 60px; }}
.trie h2 {{ color: #fff; font-size: 28px; margin-bottom: 8px; }}
.trie p {{ color: rgba(255,255,255,0.7); margin-bottom: 32px; }}
.trie-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }}
.trie-item {{ background: rgba(255,255,255,0.08); border-radius: 12px; padding: 24px; text-align: center; }}
.trie-letter {{ font-size: 40px; font-weight: 900; color: #FF8F00; margin-bottom: 8px; }}
.trie-word {{ font-size: 14px; font-weight: 700; color: #fff; margin-bottom: 6px; }}
.trie-desc {{ font-size: 12px; color: #90CAF9; }}

/* 도구 비교 */
.tool-table {{ width: 100%; border-collapse: collapse; }}
.tool-table th {{ background: #1565C0; color: #fff; padding: 14px 16px; text-align: left; font-size: 13px; }}
.tool-table td {{ padding: 14px 16px; font-size: 13px; border-bottom: 1px solid rgba(255,255,255,0.06); }}
.tool-table tr:hover td {{ background: rgba(255,255,255,0.03); }}
.difficulty-easy {{ color: #81C784; font-weight: 700; }}
.difficulty-mid {{ color: #FFD54F; font-weight: 700; }}
.difficulty-hard {{ color: #EF9A9A; font-weight: 700; }}
</style>
</head>
<body>

<div class="header">
  <h1>AI <span>이미지 생성</span> 마스터 가이드</h1>
  <p>마케터를 위한 프롬프트 작성법 — 디자이너 없이 비주얼 콘텐츠 만들기</p>
</div>

<div class="container">

  <!-- TRIE 공식 -->
  <div class="trie">
    <h2>🎯 TRIE 프롬프트 공식</h2>
    <p>4가지 요소만 기억하면 AI 이미지 생성 마스터!</p>
    <div class="trie-grid">
      <div class="trie-item">
        <div class="trie-letter">T</div>
        <div class="trie-word">Task (과제)</div>
        <div class="trie-desc">무엇을 만들건지<br>"제품 광고 이미지"</div>
      </div>
      <div class="trie-item">
        <div class="trie-letter">R</div>
        <div class="trie-word">Role (역할)</div>
        <div class="trie-desc">어떤 스타일로<br>"미니멀 모던 광고"</div>
      </div>
      <div class="trie-item">
        <div class="trie-letter">I</div>
        <div class="trie-word">Input (입력)</div>
        <div class="trie-desc">세부 조건<br>"흰 배경, 오렌지 포인트"</div>
      </div>
      <div class="trie-item">
        <div class="trie-letter">E</div>
        <div class="trie-word">Expectation (기대)</div>
        <div class="trie-desc">원하는 결과<br>"SNS 피드용 1:1 비율"</div>
      </div>
    </div>
  </div>

  <!-- 프롬프트 예시 카드 -->
  <h2 class="section-title">실전 프롬프트 예시</h2>
  <p class="section-sub">직무별로 바로 복사해서 쓰는 프롬프트 모음</p>

  <div class="prompt-grid">
    <div class="prompt-card">
      <div class="card-preview" style="background: linear-gradient(135deg, #1565C0, #0D47A1);">
        💻
      </div>
      <div class="card-body">
        <span class="card-tag" style="background: #1565C0; color: #fff;">상품기획</span>
        <h3>제품 컨셉 이미지</h3>
        <div class="prompt-text-sm">
"Modern NVMe SSD product shot, floating on white background,
blue electric energy particles surrounding, ultra-detailed,
8K resolution, studio lighting, premium tech aesthetic,
Samsung-style minimalist design, cinematic"
        </div>
        <p class="tip">💡 팁: 브랜드명 + 제품 카테고리 + 무드 키워드</p>
      </div>
    </div>

    <div class="prompt-card">
      <div class="card-preview" style="background: linear-gradient(135deg, #2E7D32, #1B5E20);">
        📱
      </div>
      <div class="card-body">
        <span class="card-tag" style="background: #2E7D32; color: #fff;">SNS 마케팅</span>
        <h3>SNS 피드 광고 이미지</h3>
        <div class="prompt-text-sm">
"Korean young professional using laptop in modern cafe,
bright natural light, lifestyle photography, candid shot,
warm tones, --ar 1:1 --style raw --q 2"
        </div>
        <p class="tip">💡 팁: 타깃 인물 묘사 + 공간 설정 + 감성 톤</p>
      </div>
    </div>

    <div class="prompt-card">
      <div class="card-preview" style="background: linear-gradient(135deg, #6A1B9A, #4A148C);">
        📊
      </div>
      <div class="card-body">
        <span class="card-tag" style="background: #6A1B9A; color: #fff;">마케팅</span>
        <h3>인포그래픽 배경</h3>
        <div class="prompt-text-sm">
"Abstract data visualization background, flowing lines
representing data transfer, deep purple and electric blue,
corporate presentation style, no text, clean geometric"
        </div>
        <p class="tip">💡 팁: "no text" 명시로 텍스트 없는 배경 생성</p>
      </div>
    </div>

    <div class="prompt-card">
      <div class="card-preview" style="background: linear-gradient(135deg, #BF360C, #870000);">
        🎯
      </div>
      <div class="card-body">
        <span class="card-tag" style="background: #BF360C; color: #fff;">영업</span>
        <h3>제안서 헤더 이미지</h3>
        <div class="prompt-text-sm">
"Business partnership handshake, digital transformation
concept, blue holographic interface, professional b2b
aesthetic, wide banner 16:9, corporate photography"
        </div>
        <p class="tip">💡 팁: 비율 명시(16:9)로 제안서에 바로 활용</p>
      </div>
    </div>
  </div>

  <!-- 도구 비교 -->
  <h2 class="section-title">AI 이미지 도구 비교</h2>
  <p class="section-sub">목적에 맞는 도구 선택 가이드</p>

  <table class="tool-table">
    <tr>
      <th>도구</th>
      <th>최적 용도</th>
      <th>가격</th>
      <th>난이도</th>
      <th>한국어 지원</th>
    </tr>
    <tr>
      <td><strong>DALL-E 3</strong> (ChatGPT)</td>
      <td>빠른 초안, 텍스트 포함 이미지</td>
      <td>ChatGPT Plus ($20/월)</td>
      <td class="difficulty-easy">쉬움</td>
      <td>✅ 완벽 지원</td>
    </tr>
    <tr>
      <td><strong>Midjourney</strong></td>
      <td>고퀄리티 아트, 브랜드 비주얼</td>
      <td>$10~$60/월</td>
      <td class="difficulty-mid">보통</td>
      <td>⚠️ 영어 권장</td>
    </tr>
    <tr>
      <td><strong>Adobe Firefly</strong></td>
      <td>상업용 안전, 제품 편집</td>
      <td>Creative Cloud 포함</td>
      <td class="difficulty-mid">보통</td>
      <td>✅ 지원</td>
    </tr>
    <tr>
      <td><strong>Canva AI</strong></td>
      <td>SNS 템플릿, 빠른 제작</td>
      <td>무료 / $17/월</td>
      <td class="difficulty-easy">쉬움</td>
      <td>✅ 완벽 지원</td>
    </tr>
    <tr>
      <td><strong>Stable Diffusion</strong></td>
      <td>커스텀 스타일, 대량 생성</td>
      <td>무료 (로컬 실행)</td>
      <td class="difficulty-hard">어려움</td>
      <td>⚠️ 제한적</td>
    </tr>
  </table>

</div>

<footer style="background: #0A0A1A; color: #546E7A; text-align: center; padding: 24px; font-size: 13px; margin-top: 60px;">
  🤖 AI Workflow Lecture Demo 2 — Image Prompt Guide | {datetime.now().strftime('%Y-%m-%d')}
</footer>

</body>
</html>"""
    out = DEMO_DIR / "demo2_image_prompts.html"
    out.write_text(html, encoding="utf-8")
    return str(out)


# ──────────────────────────────────────────────
# 데모 3: 에이전트 워크플로우 다이어그램
# ──────────────────────────────────────────────
def build_demo3_agent_workflow() -> str:
    html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>데모 3 — AI 에이전트 워크플로우</title>
<style>
{BASE_CSS}
body {{ background: #0D1B2A; color: #E0E0E0; }}
.header {{ padding: 60px 40px; text-align: center; }}
.header h1 {{ font-size: 40px; font-weight: 900; color: #fff; margin-bottom: 12px; }}
.header h1 span {{ color: #FF8F00; }}
.header p {{ color: #90A4AE; font-size: 18px; }}

.container {{ max-width: 1100px; margin: 0 auto; padding: 0 40px 80px; }}

/* 워크플로우 다이어그램 */
.workflow {{ position: relative; }}
.workflow-row {{ display: flex; align-items: center; margin-bottom: 12px; }}
.step {{
  background: #1A2744; border-radius: 12px; padding: 20px 24px;
  flex: 1; position: relative;
}}
.step-num {{
  font-size: 11px; font-weight: 700; color: #FF8F00;
  margin-bottom: 6px;
}}
.step-title {{ font-size: 16px; font-weight: 700; color: #fff; margin-bottom: 6px; }}
.step-desc {{ font-size: 12px; color: #90A4AE; line-height: 1.6; }}
.step-tool {{
  display: inline-block; margin-top: 10px;
  background: rgba(255,111,0,0.15); color: #FF8F00;
  padding: 3px 10px; border-radius: 20px; font-size: 11px; font-weight: 700;
}}
.arrow {{
  font-size: 28px; color: #FF8F00; padding: 0 16px; flex-shrink: 0;
}}
.output-box {{
  background: linear-gradient(135deg, #1B5E20, #2E7D32);
  border-radius: 12px; padding: 24px 28px; margin-top: 24px;
  border: 1px solid rgba(102,187,106,0.3);
}}
.output-box h3 {{ color: #A5D6A7; font-size: 16px; margin-bottom: 12px; }}
.output-item {{ color: #C8E6C9; font-size: 13px; margin-bottom: 8px; }}

/* 예시 카드 */
.example-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-top: 60px; }}
.example-card {{ background: #1A2744; border-radius: 12px; padding: 28px; }}
.example-card .icon {{ font-size: 32px; margin-bottom: 12px; }}
.example-card h3 {{ color: #fff; font-size: 15px; font-weight: 700; margin-bottom: 8px; }}
.example-card p {{ color: #90A4AE; font-size: 12px; line-height: 1.7; }}
.example-card .metrics {{ margin-top: 16px; }}
.metric {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.06); }}
.metric-label {{ color: #78909C; font-size: 11px; }}
.metric-value {{ color: #81C784; font-size: 11px; font-weight: 700; }}
</style>
</head>
<body>

<div class="header">
  <h1>AI <span>에이전트</span> 워크플로우</h1>
  <p>실무 자동화 파이프라인 — 설정 한 번, 매일 자동 실행</p>
</div>

<div class="container">

  <h2 style="font-size: 24px; color: #fff; margin-bottom: 8px;">📊 주간 경쟁사 가격 모니터링 에이전트</h2>
  <p style="color: #607D8B; margin-bottom: 40px;">매주 월요일 오전 9시 자동 실행 → 보고서 이메일 발송</p>

  <div class="workflow">
    <div class="workflow-row">
      <div class="step">
        <div class="step-num">STEP 01</div>
        <div class="step-title">트리거 & 초기화</div>
        <div class="step-desc">매주 월요일 9:00 cron 실행<br>대상 SKU 목록 및 경쟁사 URL 로드</div>
        <span class="step-tool">⏰ Cron + Config</span>
      </div>
      <div class="arrow">→</div>
      <div class="step">
        <div class="step-num">STEP 02</div>
        <div class="step-title">웹 크롤링</div>
        <div class="step-desc">Amazon / 공식몰 가격 자동 수집<br>스크린샷 증거 보존, 비정상 감지</div>
        <span class="step-tool">🕷️ Playwright</span>
      </div>
      <div class="arrow">→</div>
      <div class="step">
        <div class="step-num">STEP 03</div>
        <div class="step-title">데이터 파싱 & 정규화</div>
        <div class="step-desc">가격 추출, 통화 변환, 이상값 필터링<br>DB 저장 (품질 게이트 통과 후)</div>
        <span class="step-tool">🔍 Claude API + DB</span>
      </div>
    </div>

    <div class="workflow-row">
      <div class="step">
        <div class="step-num">STEP 04</div>
        <div class="step-title">AI 분석 & 인사이트</div>
        <div class="step-desc">전주 대비 가격 변동 분석<br>이상 징후, 판촉 패턴 AI 해석</div>
        <span class="step-tool">🤖 Claude Sonnet</span>
      </div>
      <div class="arrow">→</div>
      <div class="step">
        <div class="step-num">STEP 05</div>
        <div class="step-title">리포트 생성</div>
        <div class="step-desc">HTML/PDF 보고서 자동 작성<br>차트, 요약 테이블, 액션 아이템 포함</div>
        <span class="step-tool">📊 Jinja2 + Charts</span>
      </div>
      <div class="arrow">→</div>
      <div class="step">
        <div class="step-num">STEP 06</div>
        <div class="step-title">이메일 발송</div>
        <div class="step-desc">담당자에게 자동 발송<br>긴급 사항은 Slack 알림 추가</div>
        <span class="step-tool">📧 Gmail SMTP + Slack</span>
      </div>
    </div>

    <div class="output-box">
      <h3>📤 자동 생성 산출물</h3>
      <div class="output-item">✅ 주간 경쟁사 가격 변동 요약 리포트 (PDF)</div>
      <div class="output-item">✅ 이상 징후 알림 (±10% 이상 변동 시 즉시 Slack)</div>
      <div class="output-item">✅ 대시보드 업데이트 (Streamlit 자동 반영)</div>
      <div class="output-item">✅ 이번 주 액션 아이템 3개 자동 도출</div>
    </div>
  </div>

  <!-- 3가지 에이전트 예시 -->
  <h2 style="font-size: 24px; color: #fff; margin: 60px 0 12px;">직무별 에이전트 예시</h2>
  <p style="color: #607D8B; margin-bottom: 32px;">지금 당장 구축 가능한 실용 에이전트</p>

  <div class="example-grid">
    <div class="example-card">
      <div class="icon">💼</div>
      <h3>영업 제안서 자동화 에이전트</h3>
      <p>고객사명 + 미팅 목적 입력 → 맞춤형 제안서 PPT + 반론 시나리오 5개 자동 생성</p>
      <div class="metrics">
        <div class="metric">
          <span class="metric-label">기존 소요 시간</span>
          <span class="metric-value">2~3일</span>
        </div>
        <div class="metric">
          <span class="metric-label">AI 적용 후</span>
          <span class="metric-value">2~3시간 ↓ 90%</span>
        </div>
        <div class="metric">
          <span class="metric-label">난이도</span>
          <span class="metric-value">초급</span>
        </div>
      </div>
    </div>

    <div class="example-card">
      <div class="icon">📱</div>
      <h3>SNS 콘텐츠 파이프라인</h3>
      <p>제품 URL 입력 → 7일치 인스타/페이스북/X 카피 + 이미지 프롬프트 일괄 생성</p>
      <div class="metrics">
        <div class="metric">
          <span class="metric-label">기존 소요 시간</span>
          <span class="metric-value">7~14시간/주</span>
        </div>
        <div class="metric">
          <span class="metric-label">AI 적용 후</span>
          <span class="metric-value">30분/주 ↓ 96%</span>
        </div>
        <div class="metric">
          <span class="metric-label">난이도</span>
          <span class="metric-value">초급</span>
        </div>
      </div>
    </div>

    <div class="example-card">
      <div class="icon">📦</div>
      <h3>신제품 트렌드 분석 에이전트</h3>
      <p>키워드 설정 → 매일 SNS·리뷰·뉴스 스캔 → 트렌드 인사이트 + 기획 힌트 메일</p>
      <div class="metrics">
        <div class="metric">
          <span class="metric-label">기존 소요 시간</span>
          <span class="metric-value">주 8~10시간</span>
        </div>
        <div class="metric">
          <span class="metric-label">AI 적용 후</span>
          <span class="metric-value">일일 15분 리뷰</span>
        </div>
        <div class="metric">
          <span class="metric-label">난이도</span>
          <span class="metric-value">중급</span>
        </div>
      </div>
    </div>
  </div>

</div>

<footer style="background: #0A111E; color: #546E7A; text-align: center; padding: 24px; font-size: 13px;">
  🤖 AI Workflow Lecture Demo 3 — Agent Workflow | {datetime.now().strftime('%Y-%m-%d')}
</footer>

</body>
</html>"""
    out = DEMO_DIR / "demo3_agent_workflow.html"
    out.write_text(html, encoding="utf-8")
    return str(out)


# ──────────────────────────────────────────────
# 메인
# ──────────────────────────────────────────────
def build_all_demos() -> list[str]:
    """모든 데모 HTML 생성."""
    print("🎨 데모 HTML 생성 중...")
    paths = []

    print("  [1/3] 제품 랜딩 페이지 데모...")
    paths.append(build_demo1_landing())

    print("  [2/3] 이미지 프롬프트 가이드...")
    paths.append(build_demo2_image_prompts())

    print("  [3/3] 에이전트 워크플로우...")
    paths.append(build_demo3_agent_workflow())

    print(f"\n✅ 데모 생성 완료 → {DEMO_DIR}")
    for p in paths:
        print(f"  · {pathlib.Path(p).name}")

    return paths


if __name__ == "__main__":
    build_all_demos()
