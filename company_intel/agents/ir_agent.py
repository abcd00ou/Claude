"""
IR Agent — pulls latest quarterly snapshot from AI_SCM seed_data.json.
Enriches the company profile with up-to-date financials from the existing data store.
"""

import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from config import AI_SCM_SEED


_COMPANY_MAP = {
    # HBM suppliers — pull HBM market share + quarterly revenue from seed_data
    "sk_hynix": {
        "seed_key": "SK_Hynix",
        "quarterly_field": "memory_maker_revenue_quarterly_krw_t",
        "hbm_share_field": "market_share_annual",
        "capex_key": None,
    },
    "samsung_semiconductor": {
        "seed_key": "Samsung",
        "quarterly_field": None,
        "hbm_share_field": "market_share_annual",
        "capex_key": None,
    },
    "micron": {
        "seed_key": "Micron",
        "quarterly_field": None,
        "hbm_share_field": "market_share_annual",
        "capex_key": None,
    },
    # Hyperscalers — pull quarterly CapEx from seed_data
    "microsoft": {
        "seed_key": "MSFT",
        "quarterly_field": None,
        "hbm_share_field": None,
        "capex_key": "hyperscaler_capex_quarterly_usd_bn",
    },
    "google": {
        "seed_key": "GOOGL",
        "quarterly_field": None,
        "hbm_share_field": None,
        "capex_key": "hyperscaler_capex_quarterly_usd_bn",
    },
    "amazon": {
        "seed_key": "AMZN",
        "quarterly_field": None,
        "hbm_share_field": None,
        "capex_key": "hyperscaler_capex_quarterly_usd_bn",
    },
    "meta": {
        "seed_key": "META",
        "quarterly_field": None,
        "hbm_share_field": None,
        "capex_key": "hyperscaler_capex_quarterly_usd_bn",
    },
    # GPU / Foundry — no seed_data mapping; profiles maintained manually
    "nvidia": {"seed_key": None, "quarterly_field": None, "hbm_share_field": None, "capex_key": None},
    "tsmc": {"seed_key": None, "quarterly_field": None, "hbm_share_field": None, "capex_key": None},
}


def _load_seed() -> dict:
    if not AI_SCM_SEED.exists():
        print(f"  [ir_agent] seed_data.json not found at {AI_SCM_SEED}", file=sys.stderr)
        return {}
    return json.loads(AI_SCM_SEED.read_text())


def _latest_quarter(quarterly_data: dict) -> tuple[str, float] | tuple[None, None]:
    """Return the most recent non-metadata quarter key and value."""
    quarters = {
        k: v
        for k, v in quarterly_data.items()
        if not k.startswith("_") and isinstance(v, (int, float))
    }
    if not quarters:
        return None, None
    latest_key = max(quarters.keys())
    return latest_key, quarters[latest_key]


def run(company_config: dict, profile_path: Path) -> bool:
    company_id = company_config["id"]
    mapping = _COMPANY_MAP.get(company_id)
    if not mapping:
        print(f"  [ir_agent] no mapping for {company_id}, skipping", file=sys.stderr)
        return True

    seed = _load_seed()
    if not seed:
        return False

    try:
        profile = json.loads(profile_path.read_text())
    except Exception as e:
        print(f"  [ir_agent] could not read profile: {e}", file=sys.stderr)
        return False

    updated = False
    seed_key = mapping.get("seed_key")

    # HBM market share (memory suppliers only)
    if mapping.get("hbm_share_field") and seed_key:
        hbm_data = seed.get("hbm_market", {}).get("market_share_annual", {})
        latest_year = max(
            (k for k in hbm_data if not k.startswith("_")), default=None
        )
        if latest_year and seed_key in hbm_data.get(latest_year, {}):
            share = hbm_data[latest_year][seed_key]
            profile.setdefault("snapshot", {})["hbm_market_share_pct"] = round(share * 100, 1)
            updated = True
            print(f"  [ir_agent] HBM share ({latest_year}): {share*100:.0f}%")

    # Quarterly revenue from memory_maker section (SK Hynix)
    if mapping.get("quarterly_field") == "memory_maker_revenue_quarterly_krw_t" and seed_key:
        qdata = seed.get("memory_maker_revenue_quarterly_krw_t", {}).get(seed_key, {})
        qkey, qval = _latest_quarter(qdata)
        if qkey and qval:
            profile.setdefault("financials_history", {})[f"{qkey}_revenue_krw_t"] = qval
            profile.setdefault("snapshot", {})["revenue_qtr"] = f"KRW {qval}T ({qkey})"
            updated = True
            print(f"  [ir_agent] revenue ({qkey}): KRW {qval}T")

    # Quarterly CapEx from hyperscaler_capex_quarterly (hyperscalers)
    if mapping.get("capex_key") == "hyperscaler_capex_quarterly_usd_bn" and seed_key:
        qdata = seed.get("hyperscaler_capex_quarterly_usd_bn", {}).get(seed_key, {})
        qkey, qval = _latest_quarter(qdata)
        if qkey and qval:
            profile.setdefault("snapshot", {})["capex_qtr_usd"] = f"${qval}B"
            profile.setdefault("financials_history", {})[f"{qkey}_capex_usd_bn"] = qval
            updated = True
            print(f"  [ir_agent] CapEx ({qkey}): ${qval}B")

    if updated:
        profile["last_updated"] = datetime.utcnow().strftime("%Y-%m-%d")
        profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2))

    return True
