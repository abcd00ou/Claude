"""
Bottleneck Detection Agent
- Calculate demand/capacity ratio per layer
- Score current bottleneck severity
- Predict bottleneck cascade (current -> next -> after)
- Estimate resolution timelines
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config


# Resolution timeline estimates (months to add meaningful capacity)
RESOLUTION_TIMELINES = {
    "HBM": {"months": 18, "reason": "New HBM fab capacity requires 18-24 months"},
    "CoWoS": {"months": 12, "reason": "TSMC CoWoS expansion underway, 12-18 months"},
    "GPU": {"months": 9, "reason": "Blackwell ramp + AMD MI300X providing relief"},
    "Power_DC": {"months": 24, "reason": "Transformer shortage + grid permitting 2-3 years"},
    "Networking": {"months": 6, "reason": "400G/800G capacity expanding"},
    "DRAM": {"months": 6, "reason": "DRAM cycle normalizing, oversupply possible"},
    "SSD": {"months": 3, "reason": "NAND oversupply, capacity available"},
    "CPU": {"months": 6, "reason": "Balanced supply/demand"},
    "Foundry_Advanced": {"months": 18, "reason": "TSMC 3nm/2nm expansion ongoing"},
    "ASIC": {"months": 12, "reason": "Custom silicon design cycles 18-24mo, then scale"},
    "Edge_AI": {"months": 6, "reason": "Early stage, ample capacity"},
}

# Bottleneck cascade order: as one is relieved, pressure moves to next
BOTTLENECK_CASCADE = [
    ("HBM", "Current primary bottleneck - packaging limited"),
    ("CoWoS", "Enables HBM - co-bottleneck"),
    ("Power_DC", "Emerging as DC power becomes scarce"),
    ("GPU", "Supply improving with Blackwell ramp"),
    ("Networking", "400G/800G upgrade cycle pressure"),
    ("Foundry_Advanced", "Advanced node capacity tight"),
]

# Investment windows per bottleneck phase
INVESTMENT_WINDOWS = {
    # 기준일 2026-03-24 기준으로 업데이트
    "HBM":               "2024~2025 (이미 진입) → 2026 H1 핵심 구간",
    "CoWoS":             "2024~2025 (이미 진입) → 2026 H1 핵심 구간",
    "Power_DC":          "2026 H1 ~ 2027 H1 ★현재 진입 중 (2차 병목)",
    "GPU":               "2023~ 지속 / B200 전환 수혜 2026",
    "Networking":        "2026 H1 ~ 2027 H1 ★현재 진입 중 (3차 병목)",
    "Foundry_Advanced":  "2025 ~ 2027 (N3 CoWoS 캐파 타이트)",
    "ASIC":              "2026 ~ 2027 (TPU v5, Trainium2, Maia 본격화)",
}


def score_bottleneck(component, utilization):
    """Score a component's bottleneck severity."""
    if utilization >= config.BOTTLENECK_THRESHOLDS["critical"]:
        return "critical"
    elif utilization >= config.BOTTLENECK_THRESHOLDS["high"]:
        return "high"
    elif utilization >= config.BOTTLENECK_THRESHOLDS["medium"]:
        return "medium"
    else:
        return "low"


def compute_bottleneck_scores(utilization_data=None):
    """Compute bottleneck scores for all components."""
    if utilization_data is None:
        utilization_data = config.CURRENT_CAPACITY_UTILIZATION

    scores = {}
    for component, util in utilization_data.items():
        severity = score_bottleneck(component, util)
        scores[component] = {
            "utilization": util,
            "severity": severity,
            "utilization_pct": f"{util:.0%}",
            "headroom": f"{(1-util):.0%}",
            "resolution_months": RESOLUTION_TIMELINES.get(component, {}).get("months", "unknown"),
            "resolution_reason": RESOLUTION_TIMELINES.get(component, {}).get("reason", ""),
            "investment_window": INVESTMENT_WINDOWS.get(component, "N/A"),
        }

    return scores


def find_primary_bottleneck(scores):
    """Find the current primary bottleneck (highest utilization)."""
    sorted_components = sorted(
        scores.items(),
        key=lambda x: x[1]["utilization"],
        reverse=True
    )
    return sorted_components[0] if sorted_components else (None, {})


def predict_cascade(scores):
    """Predict bottleneck cascade sequence."""
    # Sort by current utilization
    sorted_components = sorted(
        [(c, d) for c, d in scores.items()],
        key=lambda x: x[1]["utilization"],
        reverse=True
    )

    cascade = []
    for component, data in sorted_components[:5]:
        cascade.append({
            "component": component,
            "current_util": data["utilization"],
            "severity": data["severity"],
            "will_ease_in_months": data["resolution_months"],
        })

    return cascade


def compute_supply_demand_gap(modeling_results=None):
    """Compute supply-demand gaps for key components."""
    gaps = {}

    # HBM Supply vs Demand
    # Total HBM capacity: ~110K wpm * 12 months * yield * GB per wafer
    # Rough: 110K wpm * 12 * 0.75 * 50GB/wafer = 49.5B GB = ~50EB
    hbm_supply_gb_year = 110000 * 12 * 0.75 * 50  # GB
    hbm_supply_gb_year *= 1e0  # scale

    # From modeling: 2025 base HBM demand
    # Use hardcoded estimate if modeling_results not available
    if modeling_results:
        hbm_demand = modeling_results.get("current_snapshot_2025", {}).get("hbm_demand_gb", 0)
    else:
        hbm_demand = 3e9  # ~3EB estimate for 2025

    gaps["HBM"] = {
        "supply_est": hbm_supply_gb_year,
        "demand_est": hbm_demand,
        "gap_ratio": min(hbm_demand / max(hbm_supply_gb_year, 1), 2.0),
        "note": "Supply in GB/year, demand in GB total installed",
    }

    # CoWoS Supply vs Demand
    cowos_supply_wpm = 50000  # 2024
    cowos_demand_wpm = 55000  # estimated demand
    gaps["CoWoS"] = {
        "supply_wpm": cowos_supply_wpm,
        "demand_wpm": cowos_demand_wpm,
        "gap_ratio": cowos_demand_wpm / cowos_supply_wpm,
        "note": "Wafers per month",
    }

    # Power Supply vs Demand (GW)
    power_supply_gw = 50   # existing DC capacity
    power_demand_gw = 70   # 2025 projected
    gaps["Power_DC"] = {
        "supply_gw": power_supply_gw,
        "demand_gw": power_demand_gw,
        "gap_ratio": power_demand_gw / power_supply_gw,
        "note": "Global data center power GW",
    }

    return gaps


def analyze_cascade_risk(scores):
    """Analyze cascade risk chains."""
    risks = []

    # HBM -> CoWoS chain
    hbm_util = scores.get("HBM", {}).get("utilization", 0)
    cowos_util = scores.get("CoWoS", {}).get("utilization", 0)
    if hbm_util > 0.85 and cowos_util > 0.85:
        risks.append({
            "chain": "CoWoS -> HBM -> GPU",
            "description": "Packaging bottleneck constrains HBM supply, limiting GPU shipments",
            "severity": "critical",
            "affected_companies": ["SK Hynix", "Samsung", "Micron", "NVIDIA"],
        })

    # Power -> DC chain
    power_util = scores.get("Power_DC", {}).get("utilization", 0)
    if power_util > 0.70:
        risks.append({
            "chain": "Power Grid -> Data Center -> GPU Utilization",
            "description": "Grid capacity limits new DC deployments, slowing GPU absorption",
            "severity": "high",
            "affected_companies": ["Microsoft Azure", "AWS", "Google Cloud", "Meta"],
        })

    # GPU -> HBM demand acceleration
    gpu_util = scores.get("GPU", {}).get("utilization", 0)
    if gpu_util > 0.85:
        risks.append({
            "chain": "GPU Demand -> HBM Acceleration",
            "description": "Each new GPU generation requires more HBM, amplifying memory shortage",
            "severity": "high",
            "affected_companies": ["SK Hynix", "Micron", "TSMC CoWoS"],
        })

    return risks


def run(market_state=None, modeling_results=None):
    """Run the bottleneck detection agent."""
    print("[BottleneckAgent] Analyzing supply chain bottlenecks...")

    # Get utilization data
    if market_state and "capacity_utilization" in market_state:
        utilization_data = market_state["capacity_utilization"]
    else:
        utilization_data = config.CURRENT_CAPACITY_UTILIZATION

    # Score all components
    scores = compute_bottleneck_scores(utilization_data)

    # Find primary bottleneck
    primary_name, primary_data = find_primary_bottleneck(scores)

    # Predict cascade
    cascade = predict_cascade(scores)

    # Supply-demand gaps
    gaps = compute_supply_demand_gap(modeling_results)

    # Cascade risk analysis
    cascade_risks = analyze_cascade_risk(scores)

    # Determine next bottleneck (second highest utilization, excluding co-bottlenecks)
    sorted_scores = sorted(scores.items(), key=lambda x: x[1]["utilization"], reverse=True)
    next_bottleneck = sorted_scores[1][0] if len(sorted_scores) > 1 else "Unknown"
    after_bottleneck = sorted_scores[2][0] if len(sorted_scores) > 2 else "Unknown"

    # Summary
    result = {
        "current_bottleneck": primary_name,
        "current_utilization": primary_data.get("utilization", 0),
        "current_severity": primary_data.get("severity", "unknown"),
        "next_bottleneck": next_bottleneck,
        "after_bottleneck": after_bottleneck,
        "resolution_timeline_months": primary_data.get("resolution_months", "unknown"),
        "investment_window": INVESTMENT_WINDOWS.get(primary_name, "N/A"),

        "all_scores": scores,
        "cascade_sequence": cascade,
        "cascade_risks": cascade_risks,
        "supply_demand_gaps": gaps,

        "critical_components": [
            c for c, d in scores.items() if d["severity"] == "critical"
        ],
        "high_risk_components": [
            c for c, d in scores.items() if d["severity"] == "high"
        ],

        "bottleneck_narrative": (
            f"Primary bottleneck: {primary_name} at {primary_data.get('utilization_pct','?')} utilization. "
            f"Next constraint: {next_bottleneck}. "
            f"Resolution estimated in {primary_data.get('resolution_months','?')} months."
        ),
    }

    print(f"  [BottleneckAgent] Primary bottleneck: {primary_name} ({primary_data.get('utilization_pct','?')})")
    print(f"  [BottleneckAgent] Critical: {result['critical_components']}")
    print(f"  [BottleneckAgent] High risk: {result['high_risk_components']}")

    return result


if __name__ == "__main__":
    result = run()
    print(f"\nCurrent: {result['current_bottleneck']} ({result['current_utilization']:.0%})")
    print(f"Next: {result['next_bottleneck']}")
    print(f"Resolution: {result['resolution_timeline_months']} months")
    print(f"\nCritical components: {result['critical_components']}")
    print(f"High risk: {result['high_risk_components']}")
