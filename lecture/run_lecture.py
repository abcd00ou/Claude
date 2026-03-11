"""
lecture/run_lecture.py — 강의 자료 생성 오케스트레이터

실행 방법:
  python3 run_lecture.py              # 전체 파이프라인 (캐시 재사용)
  python3 run_lecture.py --refresh    # 리서치 데이터 새로 수집
  python3 run_lecture.py --ppt-only   # PPT만 생성 (데모 스킵)
  python3 run_lecture.py --demo-only  # 데모 HTML만 생성
  python3 run_lecture.py --no-ai      # Claude API 없이 기본 데이터로 PPT 생성
"""

import argparse
import subprocess
import sys
import pathlib
from datetime import datetime

BASE_DIR = pathlib.Path(__file__).parent
sys.path.insert(0, str(BASE_DIR))


def check_dependencies() -> bool:
    """필수 패키지 확인."""
    required = ["pptx", "anthropic"]
    missing = []
    for pkg in required:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"⚠️  누락된 패키지: {', '.join(missing)}")
        print("   실행: pip3 install -r requirements.txt")
        return False
    return True


def run_research(force_refresh: bool) -> dict | None:
    """리서치 에이전트 실행."""
    print("\n" + "=" * 60)
    print("📡 STEP 1/3 — AI 리서치 에이전트")
    print("=" * 60)
    try:
        from agents.research_agent import run_research as _run, print_research_summary
        data = _run(force_refresh=force_refresh)
        print_research_summary(data)
        return data
    except ImportError as e:
        print(f"  [오류] anthropic 패키지 필요: {e}")
        return None
    except Exception as e:
        print(f"  [오류] 리서치 실패: {e}")
        return None


def build_ppt(research_data: dict | None) -> str | None:
    """PPT 빌더 실행."""
    print("\n" + "=" * 60)
    print("📊 STEP 2/3 — PowerPoint 생성")
    print("=" * 60)
    try:
        from agents.slide_builder import build_presentation
        path = build_presentation(research_data)
        return path
    except Exception as e:
        print(f"  [오류] PPT 생성 실패: {e}")
        import traceback
        traceback.print_exc()
        return None


def build_demos() -> list[str]:
    """데모 HTML 빌더 실행."""
    print("\n" + "=" * 60)
    print("🎨 STEP 3/3 — 데모 HTML 생성")
    print("=" * 60)
    try:
        from agents.demo_builder import build_all_demos
        return build_all_demos()
    except Exception as e:
        print(f"  [오류] 데모 생성 실패: {e}")
        return []


def run_daily(force_refresh: bool = False) -> dict:
    """일일 뉴스 수집 + Word 브리핑 생성."""
    print("\n" + "=" * 60)
    print("📡 DAILY — AI 뉴스 수집 + 브리핑 생성")
    print("=" * 60)
    try:
        from agents.news_agent import run_news_agent, print_news_summary
        result = run_news_agent(force_refresh=force_refresh)
        print_news_summary(result)
        return result
    except ImportError as e:
        print(f"  [오류] feedparser/anthropic 패키지 필요: {e}")
        return {}
    except Exception as e:
        print(f"  [오류] 뉴스 수집 실패: {e}")
        import traceback; traceback.print_exc()
        return {}


def build_briefing_doc(news_data: dict) -> str:
    """뉴스 데이터로 Word 브리핑 문서 생성."""
    print("\n" + "=" * 60)
    print("📝 DAILY — Word 브리핑 문서 생성")
    print("=" * 60)
    try:
        from agents.word_builder import build_daily_briefing_doc
        return build_daily_briefing_doc(news_data)
    except ImportError as e:
        print(f"  [오류] python-docx 패키지 필요: {e}")
        print("   실행: pip3 install python-docx")
        return ""
    except Exception as e:
        print(f"  [오류] Word 생성 실패: {e}")
        import traceback; traceback.print_exc()
        return ""


def open_file(path: str) -> None:
    """macOS에서 파일 열기."""
    try:
        subprocess.run(["open", path], check=True)
    except Exception:
        pass


def print_summary(ppt_path: str | None, demo_paths: list[str], start_time: datetime) -> None:
    """최종 결과 요약 출력."""
    elapsed = (datetime.now() - start_time).total_seconds()

    print("\n" + "=" * 60)
    print("🎉 강의 자료 생성 완료!")
    print("=" * 60)
    print(f"⏱️  소요 시간: {elapsed:.1f}초")
    print()

    if ppt_path:
        print(f"📊 PPT 파일:")
        print(f"   {ppt_path}")

    if demo_paths:
        print(f"\n🌐 데모 HTML ({len(demo_paths)}개):")
        for p in demo_paths:
            print(f"   {p}")

    website_path = BASE_DIR / "website" / "index.html"
    print(f"\n🖥️  강의 웹사이트:")
    print(f"   {website_path}")

    print()
    print("📁 전체 출력 폴더:", BASE_DIR / "output")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="AI 워크플로우 강의 자료 생성 에이전트",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--refresh", action="store_true", help="리서치 캐시 무시하고 새로 수집")
    parser.add_argument("--ppt-only", action="store_true", help="PPT만 생성")
    parser.add_argument("--demo-only", action="store_true", help="데모 HTML만 생성")
    parser.add_argument("--no-ai", action="store_true", help="Claude API 없이 기본 데이터로 실행")
    parser.add_argument("--open", action="store_true", help="완료 후 파일 자동 열기")
    parser.add_argument("--daily", action="store_true", help="일일 뉴스 수집 + Word 브리핑 생성 (+ 업데이트 많으면 PPT 재생성)")
    args = parser.parse_args()

    start_time = datetime.now()

    print()
    print("┌─────────────────────────────────────────────────────┐")
    print("│  AI 워크플로우 강의 자료 생성 에이전트               │")
    print("│  B2C 영업·마케팅·상품기획 실무자를 위한 강의        │")
    print("└─────────────────────────────────────────────────────┘")
    print(f"  실행 시각: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 의존성 확인
    if not args.no_ai and not args.demo_only:
        if not check_dependencies():
            if not args.ppt_only:
                print("\n⚠️  --no-ai 플래그로 Claude API 없이 실행합니다...")
                args.no_ai = True

    ppt_path = None
    demo_paths = []
    research_data = None
    doc_path = None

    # 일일 뉴스 브리핑 모드
    if args.daily:
        news_data = run_daily(force_refresh=args.refresh)
        doc_path = build_briefing_doc(news_data) if news_data else ""
        # 유의미한 업데이트가 있으면 PPT도 재생성
        if news_data.get("has_significant_updates"):
            print("\n  ℹ️  유의미한 뉴스 업데이트 감지 — PPT 재생성")
            ppt_path = build_ppt(None)
        elapsed = (datetime.now() - start_time).total_seconds()
        print("\n" + "=" * 60)
        print("🎉 일일 브리핑 완료!")
        print("=" * 60)
        print(f"⏱️  소요 시간: {elapsed:.1f}초")
        if doc_path:
            print(f"📝 Word 브리핑: {doc_path}")
        if ppt_path:
            print(f"📊 PPT (재생성): {ppt_path}")
        print("\n💡 cron 자동화:\n   0 9 * * * cd {path} && python3 run_lecture.py --daily".format(
            path=BASE_DIR))
        if args.open:
            if doc_path: open_file(doc_path)
            if ppt_path: open_file(ppt_path)
        return

    # 데모만 생성
    if args.demo_only:
        demo_paths = build_demos()
        print_summary(None, demo_paths, start_time)
        if args.open and demo_paths:
            open_file(demo_paths[0])
        return

    # PPT만 생성
    if args.ppt_only:
        if not args.no_ai:
            research_data = run_research(force_refresh=args.refresh)
        ppt_path = build_ppt(research_data)
        print_summary(ppt_path, [], start_time)
        if args.open and ppt_path:
            open_file(ppt_path)
        return

    # 전체 파이프라인
    # 1. 리서치
    if not args.no_ai:
        research_data = run_research(force_refresh=args.refresh)
    else:
        print("\n[--no-ai] Claude API 리서치 스킵, 기본 데이터 사용")

    # 2. PPT
    ppt_path = build_ppt(research_data)

    # 3. 데모
    demo_paths = build_demos()

    # 결과 요약
    print_summary(ppt_path, demo_paths, start_time)

    if args.open:
        if ppt_path:
            open_file(ppt_path)
        website = str(BASE_DIR / "website" / "index.html")
        open_file(website)


if __name__ == "__main__":
    main()
