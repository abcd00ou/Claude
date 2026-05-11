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
    # ── Custom ASIC Designers ────────────────────────────────────────────────
    {
        "id": "broadcom",
        "name": "Broadcom",
        "ticker": "AVGO",
        "layer": "ASIC",
        "ir_url": "https://investors.broadcom.com/",
        "news_query": "Broadcom ASIC TPU AI custom silicon HBM",
    },
    {
        "id": "marvell",
        "name": "Marvell Technology",
        "ticker": "MRVL",
        "layer": "ASIC",
        "ir_url": "https://investor.marvell.com/",
        "news_query": "Marvell AI ASIC Trainium custom silicon",
    },
    {
        "id": "amd",
        "name": "AMD",
        "ticker": "AMD",
        "layer": "ASIC",
        "ir_url": "https://ir.amd.com/",
        "news_query": "AMD Instinct MI300 MI325 HBM datacenter GPU",
    },
    # ── Power & Infrastructure ───────────────────────────────────────────────
    {
        "id": "vertiv",
        "name": "Vertiv",
        "ticker": "VRT",
        "layer": "Power",
        "ir_url": "https://ir.vertiv.com/",
        "news_query": "Vertiv AI data center power cooling liquid",
    },
    {
        "id": "ge_vernova",
        "name": "GE Vernova",
        "ticker": "GEV",
        "layer": "Power",
        "ir_url": "https://www.gevernova.com/investors",
        "news_query": "GE Vernova data center power grid AI electricity",
    },
    {
        "id": "constellation_energy",
        "name": "Constellation Energy",
        "ticker": "CEG",
        "layer": "Power",
        "ir_url": "https://ir.constellationenergy.com/",
        "news_query": "Constellation Energy nuclear AI data center power PPA",
    },
    # ── China AI Supply Chain ────────────────────────────────────────────────
    {
        "id": "huawei",
        "name": "Huawei (AI/Cloud)",
        "ticker": "Unlisted",
        "layer": "China",
        "ir_url": "https://www.huawei.com/en/investor-relations",
        "news_query": "Huawei Ascend AI chip HBM cloud datacenter",
    },
    {
        "id": "cxmt",
        "name": "CXMT (ChangXin Memory)",
        "ticker": "Unlisted",
        "layer": "China",
        "ir_url": "",
        "news_query": "CXMT ChangXin Memory HBM China DRAM",
    },
    {
        "id": "smic",
        "name": "SMIC",
        "ticker": "0981.HK",
        "layer": "China",
        "ir_url": "https://www.smics.com/en/site/company_investor",
        "news_query": "SMIC China foundry advanced node AI chip",
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
