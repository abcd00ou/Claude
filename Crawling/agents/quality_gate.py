"""
Quality Gate Agent
price_observations → accepted / quarantined 분리.

규칙:
  - parse_confidence < 0.7  → quarantine
  - price is None or <= 0   → quarantine
  - currency is None        → quarantine
  - |price_change| >= 30%   → flag (통과, anomaly 기록)
"""
from config import QUALITY_RULES


def _last_price(sku_id: str, country: str, source: str, last_obs: dict) -> float | None:
    """last_obs: { (sku_id, country, source): price }"""
    return last_obs.get((sku_id, country, source))


def gate(
    observations: list[dict],
    last_obs: dict,
) -> dict:
    """
    Returns:
      {
        "accepted":    [...],
        "quarantined": [...],   # each with "quarantine_reason"
        "anomalies":   [...],   # price spike/drop flags
        "summary":     {...}
      }
    """
    min_conf    = QUALITY_RULES["min_confidence"]
    change_pct  = QUALITY_RULES["price_change_flag_pct"]

    accepted    = []
    quarantined = []
    anomalies   = []

    for obs in observations:
        reasons = []

        if (obs.get("parse_confidence") or 0) < min_conf:
            reasons.append(f"low_confidence:{obs.get('parse_confidence'):.2f}")

        if obs.get("price") is None or obs.get("price", 0) <= 0:
            reasons.append("price_invalid")

        if obs.get("currency") is None:
            reasons.append("currency_null")

        if reasons:
            obs["quarantine_reason"] = "; ".join(reasons)
            quarantined.append(obs)
            continue

        # Anomaly check (±30%)
        prev = _last_price(obs["sku_id"], obs["country"], obs["source"], last_obs)
        if prev and prev > 0:
            delta_pct = abs(obs["price"] - prev) / prev * 100
            if delta_pct >= change_pct:
                direction = "up" if obs["price"] > prev else "down"
                anomalies.append({
                    **obs,
                    "anomaly_type":      "price_spike",
                    "prev_price":        prev,
                    "delta_pct":         round(delta_pct, 1),
                    "direction":         direction,
                })

        accepted.append(obs)

    return {
        "accepted":    accepted,
        "quarantined": quarantined,
        "anomalies":   anomalies,
        "summary": {
            "total":       len(observations),
            "accepted":    len(accepted),
            "quarantined": len(quarantined),
            "anomalies":   len(anomalies),
        },
    }
