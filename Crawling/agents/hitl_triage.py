"""
HITL Triage Agent
quarantined + anomalies → hitl_queue 항목 생성 (P0 / P1 우선순위).

P0: currency_null, fetch_failed, parse_confidence < 0.3
P1: price_spike/drop ≥ 30%, low_confidence (0.3~0.7)
"""
from datetime import datetime


def _priority(obs: dict) -> str:
    reason = obs.get("quarantine_reason", "") or ""
    conf   = obs.get("parse_confidence", 0) or 0

    if "currency_null" in reason:
        return "P0"
    if "fetch_failed" in reason or "blocked" in reason:
        return "P0"
    if conf < 0.3:
        return "P0"
    if obs.get("anomaly_type") == "price_spike":
        return "P1"
    return "P1"


def build_hitl_queue(
    run_id: str,
    quarantined: list[dict],
    anomalies: list[dict],
) -> list[dict]:
    items = []

    for obs in quarantined:
        items.append({
            "run_id":   run_id,
            "sku_id":   obs["sku_id"],
            "country":  obs["country"],
            "source":   obs["source"],
            "priority": _priority(obs),
            "reason":   obs.get("quarantine_reason", "quarantined"),
            "evidence": {
                "content_hash":     obs.get("content_hash"),
                "raw_path":         obs.get("raw_path"),
                "parse_confidence": obs.get("parse_confidence"),
                "parse_notes":      obs.get("parse_notes"),
                "price_raw":        None,
            },
            "status":      "pending",
            "created_at":  datetime.utcnow().isoformat() + "Z",
        })

    for obs in anomalies:
        items.append({
            "run_id":   run_id,
            "sku_id":   obs["sku_id"],
            "country":  obs["country"],
            "source":   obs["source"],
            "priority": "P1",
            "reason":   (
                f"price_{obs.get('direction','change')} "
                f"{obs.get('delta_pct')}%: "
                f"{obs.get('prev_price')} → {obs.get('price')} {obs.get('currency')}"
            ),
            "evidence": {
                "prev_price":   obs.get("prev_price"),
                "curr_price":   obs.get("price"),
                "currency":     obs.get("currency"),
                "delta_pct":    obs.get("delta_pct"),
                "direction":    obs.get("direction"),
                "content_hash": obs.get("content_hash"),
                "raw_path":     obs.get("raw_path"),
            },
            "status":     "pending",
            "created_at": datetime.utcnow().isoformat() + "Z",
        })

    # P0 먼저
    items.sort(key=lambda x: (0 if x["priority"] == "P0" else 1))
    return items


def priority_summary(items: list[dict]) -> dict:
    p0 = [i for i in items if i["priority"] == "P0"]
    p1 = [i for i in items if i["priority"] == "P1"]
    return {
        "total": len(items),
        "P0":    len(p0),
        "P1":    len(p1),
        "P0_skus": [f"{i['sku_id']}({i['country']})" for i in p0],
    }
