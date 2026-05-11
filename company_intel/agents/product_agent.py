"""
Product Agent — monitors product roadmap signals from news headlines.
Scans recent_news (already populated by news_agent) for roadmap keywords
and flags items worth reviewing in the sales_hooks field.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))


_ROADMAP_KEYWORDS = [
    "roadmap", "HBM4", "HBM4E", "HBM5", "sampling", "mass production",
    "ramp", "qualification", "certified", "next-gen", "launch", "announce",
    "partnership", "supply agreement", "contract",
]

_RISK_KEYWORDS = [
    "delay", "yield issue", "shortage", "recall", "defect", "penalty",
    "lawsuit", "export control", "ban", "restriction",
]


def _score_headline(title: str) -> tuple[str, int]:
    """Return (category, score). Higher score = more relevant."""
    t = title.lower()
    roadmap_hits = sum(1 for kw in _ROADMAP_KEYWORDS if kw.lower() in t)
    risk_hits = sum(1 for kw in _RISK_KEYWORDS if kw.lower() in t)

    if risk_hits > 0:
        return "risk", risk_hits * 2
    if roadmap_hits > 0:
        return "roadmap", roadmap_hits
    return "general", 0


def run(company_config: dict, profile_path: Path) -> bool:
    try:
        profile = json.loads(profile_path.read_text())
    except Exception as e:
        print(f"  [product_agent] could not read profile: {e}", file=sys.stderr)
        return False

    news = profile.get("recent_news", [])
    if not news:
        print("  [product_agent] no news to scan, skipping")
        return True

    flagged = []
    for item in news:
        category, score = _score_headline(item.get("title", ""))
        if score > 0:
            flagged.append(
                {
                    "title": item["title"],
                    "date": item["date"],
                    "url": item["url"],
                    "category": category,
                    "relevance_score": score,
                }
            )

    flagged.sort(key=lambda x: x["relevance_score"], reverse=True)

    if flagged:
        profile["flagged_news"] = flagged[:5]
        print(f"  [product_agent] {len(flagged)} relevant articles flagged")
    else:
        profile["flagged_news"] = []
        print("  [product_agent] no high-relevance articles found")

    profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2))
    return True
