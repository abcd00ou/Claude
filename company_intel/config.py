"""
Company Intelligence Platform — Configuration
Target: HBM/semiconductor manufacturers' marketing teams

AI Supply Chain Layers:
  Hyperscalers (demand) → NVIDIA (GPU) → TSMC (packaging) → HBM Suppliers (memory)
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data" / "companies"
DASHBOARD_DIR = BASE_DIR / "dashboard"
AI_SCM_SEED = BASE_DIR.parent / "AI_SCM" / "data" / "seed_data.json"

TARGET_COMPANIES = [
    # ── HBM Memory Suppliers ────────────────────────────────────────────────
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
    # ── GPU & Packaging ──────────────────────────────────────────────────────
    {
        "id": "nvidia",
        "name": "NVIDIA",
        "ticker": "NVDA",
        "layer": "GPU",
        "ir_url": "https://investor.nvidia.com/",
        "news_query": "NVIDIA Blackwell HBM GPU datacenter",
    },
    {
        "id": "tsmc",
        "name": "TSMC",
        "ticker": "TSM",
        "layer": "Foundry",
        "ir_url": "https://ir.tsmc.com/",
        "news_query": "TSMC CoWoS AI packaging advanced node",
    },
    # ── Hyperscalers (demand side) ───────────────────────────────────────────
    {
        "id": "microsoft",
        "name": "Microsoft",
        "ticker": "MSFT",
        "layer": "Hyperscaler",
        "ir_url": "https://www.microsoft.com/en-us/investor",
        "news_query": "Microsoft Azure AI datacenter CapEx GPU",
    },
    {
        "id": "google",
        "name": "Google (Alphabet)",
        "ticker": "GOOGL",
        "layer": "Hyperscaler",
        "ir_url": "https://abc.xyz/investor/",
        "news_query": "Google TPU datacenter AI CapEx HBM",
    },
    {
        "id": "amazon",
        "name": "Amazon (AWS)",
        "ticker": "AMZN",
        "layer": "Hyperscaler",
        "ir_url": "https://ir.aboutamazon.com/",
        "news_query": "Amazon AWS Trainium Inferentia AI CapEx",
    },
    {
        "id": "meta",
        "name": "Meta Platforms",
        "ticker": "META",
        "layer": "Hyperscaler",
        "ir_url": "https://investor.fb.com/",
        "news_query": "Meta AI datacenter GPU CapEx Llama",
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
