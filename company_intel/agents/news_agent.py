"""
News Agent — Google News RSS collection (free, no API key required).
Fetches recent news for a company and updates the recent_news field in its JSON profile.
"""

import json
import sys
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import NEWS_MAX_ITEMS, NEWS_LOOKBACK_DAYS, AGENT_TIMEOUT_SECONDS


def fetch_google_news_rss(query: str, max_items: int = NEWS_MAX_ITEMS) -> list[dict]:
    encoded = urllib.parse.quote(query)
    url = f"https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=AGENT_TIMEOUT_SECONDS) as resp:
            content = resp.read()
    except Exception as e:
        print(f"  [news_agent] fetch failed: {e}", file=sys.stderr)
        return []

    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        print(f"  [news_agent] XML parse error: {e}", file=sys.stderr)
        return []

    cutoff = datetime.utcnow() - timedelta(days=NEWS_LOOKBACK_DAYS)
    items = []

    for item in root.findall(".//item"):
        title_el = item.find("title")
        link_el = item.find("link")
        pub_el = item.find("pubDate")
        source_el = item.find("source")

        title = title_el.text.strip() if title_el is not None and title_el.text else ""
        link = link_el.text.strip() if link_el is not None and link_el.text else ""
        pub_raw = pub_el.text.strip() if pub_el is not None and pub_el.text else ""
        source = source_el.text.strip() if source_el is not None and source_el.text else "Unknown"

        # Strip source suffix Google News appends: "Title - Source"
        if " - " in title and title.endswith(source):
            title = title[: title.rfind(" - " + source)].strip()

        try:
            pub_dt = datetime.strptime(pub_raw, "%a, %d %b %Y %H:%M:%S %Z")
        except ValueError:
            pub_dt = datetime.utcnow()

        if pub_dt < cutoff:
            continue

        items.append(
            {
                "date": pub_dt.strftime("%Y-%m-%d"),
                "title": title,
                "url": link,
                "source": source,
            }
        )

        if len(items) >= max_items:
            break

    return items


def run(company_config: dict, profile_path: Path) -> bool:
    query = company_config.get("news_query", company_config["name"])
    print(f"  [news_agent] fetching: '{query}'")

    news_items = fetch_google_news_rss(query)
    print(f"  [news_agent] {len(news_items)} articles collected")

    try:
        profile = json.loads(profile_path.read_text())
    except Exception as e:
        print(f"  [news_agent] could not read profile: {e}", file=sys.stderr)
        return False

    profile["recent_news"] = news_items
    profile["last_updated"] = datetime.utcnow().strftime("%Y-%m-%d")

    profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2))
    return True
