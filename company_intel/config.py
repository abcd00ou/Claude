"""
Company Intelligence Platform — Configuration
Target: HBM/semiconductor manufacturers' marketing teams
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "companies"
DASHBOARD_DIR = BASE_DIR / "dashboard"
AI_SCM_SEED = BASE_DIR.parent / "AI_SCM" / "data" / "seed_data.json"

# Phase 1: SK Hynix only. Phase 2: add Samsung, Micron.
TARGET_COMPANIES = [
    {
        "id": "sk_hynix",
        "name": "SK Hynix",
        "ticker": "000660.KS",
        "layer": "HBM",
        "ir_url": "https://www.skhynix.com/ir/",
        "news_query": "SK Hynix HBM memory",
    },
    {
        "id": "samsung_semiconductor",
        "name": "Samsung Semiconductor",
        "ticker": "005930.KS",
        "layer": "HBM",
        "ir_url": "https://semiconductor.samsung.com/",
        "news_query": "Samsung HBM memory semiconductor",
    },
    {
        "id": "micron",
        "name": "Micron Technology",
        "ticker": "MU",
        "layer": "HBM",
        "ir_url": "https://investors.micron.com/",
        "news_query": "Micron HBM memory AI",
    },
]

# News collection (Phase 1-2: Google News RSS, free)
NEWS_MAX_ITEMS = 10
NEWS_LOOKBACK_DAYS = 30

# Agent failure behavior: partial save + continue (never abort full pipeline)
AGENT_TIMEOUT_SECONDS = 30
AGENT_ON_FAILURE = "continue"  # options: "continue" | "abort"

# API keys — loaded from .env, never hardcoded here
NEWSAPI_KEY = os.environ.get("NEWSAPI_KEY", "")  # optional, Phase 3+
