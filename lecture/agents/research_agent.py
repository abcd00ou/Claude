"""
lecture/agents/research_agent.py
AI 진화 & 워크플로우 변화 자료 수집 에이전트

- Claude API를 사용해 각 챕터별 심층 리서치 수행
- 결과를 data/research_cache.json에 저장
- 슬라이드 빌더가 이 데이터를 참조해 PPT 내용 생성
"""

import json
import sys
import time
import pathlib
from datetime import datetime

import anthropic

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from config import CHAPTERS, AI_TIMELINE, WORKFLOW_CHANGES, DATA_DIR

client = anthropic.Anthropic()

# ──────────────────────────────────────────────
# 리서치 프롬프트 템플릿
# ──────────────────────────────────────────────
RESEARCH_PROMPTS = {
    "ai_evolution": """
당신은 AI 산업 분석 전문가입니다.
다음 AI 진화 타임라인을 바탕으로, B2C 영업·마케팅·상품기획 담당자들에게
임팩트 있게 설명할 수 있는 핵심 인사이트를 제공해주세요.

타임라인:
{timeline}

다음 형식으로 JSON 응답해주세요:
{{
  "key_insights": ["인사이트1", "인사이트2", "인사이트3"],
  "shocking_stats": ["통계1 (숫자 포함)", "통계2", "통계3"],
  "before_after_examples": [
    {{"before": "이전 방식", "after": "AI 이후 방식", "job": "직무"}}
  ],
  "analogy": "비전문가도 이해할 수 있는 비유 1개",
  "hook_sentence": "청중의 관심을 끄는 오프닝 문장 1개"
}}
""",
    "workflow_sales": """
당신은 B2C 영업 전문가이자 AI 활용 트레이너입니다.
AI가 B2C 영업 담당자의 일상 업무를 어떻게 바꾸고 있는지
구체적이고 실용적인 사례를 제공해주세요.

다음 형식으로 JSON 응답해주세요:
{{
  "top_use_cases": [
    {{
      "task": "업무명",
      "time_before": "이전 소요 시간",
      "time_after": "AI 사용 후 소요 시간",
      "tool": "사용 AI 도구",
      "example_prompt": "실제 프롬프트 예시"
    }}
  ],
  "roi_examples": ["ROI 사례1 (구체적 숫자 포함)", "ROI 사례2"],
  "common_mistakes": ["자주 하는 실수1", "자주 하는 실수2"],
  "quick_wins": ["바로 써먹을 수 있는 방법1", "방법2", "방법3"]
}}
""",
    "workflow_marketing": """
당신은 디지털 마케팅 전문가이자 AI 콘텐츠 전략가입니다.
AI가 B2C 마케팅 담당자의 콘텐츠 제작과 캠페인 운영을
어떻게 혁신하고 있는지 사례를 제공해주세요.

다음 형식으로 JSON 응답해주세요:
{{
  "content_automation": [
    {{
      "content_type": "콘텐츠 유형",
      "old_process": "기존 프로세스",
      "new_process": "AI 활용 프로세스",
      "productivity_gain": "생산성 향상 수치"
    }}
  ],
  "campaign_examples": [
    {{
      "brand": "브랜드명(실제 사례)",
      "ai_usage": "AI 활용 방식",
      "result": "성과"
    }}
  ],
  "image_gen_tips": ["이미지 생성 프롬프트 팁1", "팁2", "팁3"],
  "tools_matrix": [
    {{"tool": "도구명", "best_for": "최적 용도", "difficulty": "쉬움/보통/어려움"}}
  ]
}}
""",
    "workflow_product": """
당신은 소비재 상품기획 전문가이자 AI 데이터 분석가입니다.
AI가 B2C 상품기획 담당자의 리서치, 분석, 기획 업무를
어떻게 변화시키고 있는지 사례를 제공해주세요.

다음 형식으로 JSON 응답해주세요:
{{
  "research_automation": [
    {{
      "task": "리서치 업무",
      "manual_hours": "기존 소요 시간",
      "ai_hours": "AI 사용 후 시간",
      "method": "AI 활용 방법"
    }}
  ],
  "trend_analysis_examples": ["트렌드 분석 사례1", "사례2"],
  "competitor_analysis": {{
    "tools": ["도구1", "도구2"],
    "workflow": "경쟁사 분석 AI 워크플로우 단계별 설명"
  }},
  "planning_templates": [
    {{"template": "기획서 섹션명", "ai_prompt": "해당 섹션 AI 프롬프트"}}
  ]
}}
""",
    "agent_examples": """
당신은 AI 에이전트 아키텍처 전문가입니다.
B2C 영업·마케팅·상품기획 담당자들이 실제로 구축하거나 활용할 수 있는
실용적인 AI 에이전트 예시를 제공해주세요.

다음 형식으로 JSON 응답해주세요:
{{
  "agent_examples": [
    {{
      "name": "에이전트 이름",
      "job_role": "대상 직무",
      "description": "에이전트 기능 설명",
      "tools_used": ["도구1", "도구2"],
      "trigger": "실행 트리거 (매일 오전 9시 등)",
      "output": "산출물 예시",
      "difficulty": "초급/중급/고급"
    }}
  ],
  "no_code_agents": [
    {{
      "platform": "플랫폼명",
      "use_case": "사용 사례",
      "setup_time": "설정 시간"
    }}
  ],
  "future_outlook": "2026~2027년 에이전트 발전 방향 (3문장)"
}}
""",
}


def _call_claude(prompt: str, max_tokens: int = 2000) -> dict:
    """Claude API 호출 후 JSON 파싱."""
    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )
        text = response.content[0].text.strip()
        # JSON 블록 추출
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"  [경고] JSON 파싱 실패: {e}")
        return {"raw": text, "error": str(e)}
    except Exception as e:
        print(f"  [오류] Claude API 호출 실패: {e}")
        return {"error": str(e)}


def run_research(force_refresh: bool = False) -> dict:
    """
    모든 리서치 수행 후 data/research_cache.json에 저장.
    force_refresh=False이면 기존 캐시 재사용.
    """
    cache_path = DATA_DIR / "research_cache.json"

    if not force_refresh and cache_path.exists():
        print("✅ 캐시 데이터 로드:", cache_path)
        with open(cache_path, encoding="utf-8") as f:
            return json.load(f)

    print("🔍 AI 리서치 에이전트 시작...")
    results = {
        "generated_at": datetime.now().isoformat(),
        "sections": {},
    }

    # 1. AI 진화 타임라인
    print("  [1/5] AI 진화 타임라인 분석 중...")
    timeline_str = "\n".join(
        f"- {e['year']}.{e['month']} | {e['event']} | 임팩트: {e['impact']}"
        for e in AI_TIMELINE
    )
    prompt = RESEARCH_PROMPTS["ai_evolution"].format(timeline=timeline_str)
    results["sections"]["ai_evolution"] = _call_claude(prompt)
    time.sleep(1)

    # 2. 영업 워크플로우
    print("  [2/5] 영업 워크플로우 변화 분석 중...")
    results["sections"]["workflow_sales"] = _call_claude(RESEARCH_PROMPTS["workflow_sales"])
    time.sleep(1)

    # 3. 마케팅 워크플로우
    print("  [3/5] 마케팅 워크플로우 변화 분석 중...")
    results["sections"]["workflow_marketing"] = _call_claude(
        RESEARCH_PROMPTS["workflow_marketing"]
    )
    time.sleep(1)

    # 4. 상품기획 워크플로우
    print("  [4/5] 상품기획 워크플로우 변화 분석 중...")
    results["sections"]["workflow_product"] = _call_claude(RESEARCH_PROMPTS["workflow_product"])
    time.sleep(1)

    # 5. 에이전트 예시
    print("  [5/5] AI 에이전트 사례 수집 중...")
    results["sections"]["agent_examples"] = _call_claude(RESEARCH_PROMPTS["agent_examples"])

    # 캐시 저장
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 리서치 완료 → {cache_path}")
    return results


def print_research_summary(data: dict) -> None:
    """리서치 결과 요약 출력."""
    print("\n" + "=" * 60)
    print("📊 리서치 결과 요약")
    print("=" * 60)

    ev = data["sections"].get("ai_evolution", {})
    if "key_insights" in ev:
        print("\n[AI 진화 핵심 인사이트]")
        for i in ev["key_insights"]:
            print(f"  • {i}")
    if "hook_sentence" in ev:
        print(f"\n[오프닝 문장] {ev['hook_sentence']}")

    agent = data["sections"].get("agent_examples", {})
    if "agent_examples" in agent:
        print("\n[에이전트 예시]")
        for a in agent["agent_examples"][:3]:
            print(f"  • [{a.get('job_role', '')}] {a.get('name', '')} — {a.get('description', '')[:50]}...")

    print("=" * 60)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="AI 강의 리서치 에이전트")
    parser.add_argument("--refresh", action="store_true", help="캐시 무시하고 새로 수집")
    args = parser.parse_args()

    data = run_research(force_refresh=args.refresh)
    print_research_summary(data)
