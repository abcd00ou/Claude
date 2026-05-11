"""
Company Intelligence Platform — Pipeline Runner

Usage:
    python run.py                    # update all companies
    python run.py --company sk_hynix # update one company
    python run.py --build-only       # rebuild dashboard without fetching
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

from config import TARGET_COMPANIES, DATA_DIR, AGENT_ON_FAILURE
from agents import news_agent, ir_agent, product_agent


AGENTS = [
    ("news_agent",    news_agent),
    ("ir_agent",      ir_agent),
    ("product_agent", product_agent),
]


def run_company(company: dict) -> bool:
    profile_path = DATA_DIR / f"{company['id']}.json"
    if not profile_path.exists():
        print(f"[run] profile not found: {profile_path} — skipping")
        return False

    print(f"\n{'='*60}")
    print(f"[run] {company['name']} ({company['id']})")
    print(f"{'='*60}")

    all_ok = True
    for agent_name, agent_module in AGENTS:
        print(f"\n[run] running {agent_name}...")
        try:
            ok = agent_module.run(company, profile_path)
        except Exception as e:
            print(f"  [{agent_name}] EXCEPTION: {e}", file=sys.stderr)
            ok = False

        if not ok:
            print(f"  [{agent_name}] FAILED", file=sys.stderr)
            all_ok = False
            if AGENT_ON_FAILURE == "abort":
                print("[run] aborting pipeline (AGENT_ON_FAILURE=abort)")
                return False
            else:
                print(f"  [{agent_name}] continuing despite failure")

    return all_ok


def main():
    parser = argparse.ArgumentParser(description="Company Intel pipeline")
    parser.add_argument("--company", help="Run for one company ID only")
    parser.add_argument("--build-only", action="store_true", help="Skip agents, rebuild dashboard only")
    args = parser.parse_args()

    if not args.build_only:
        targets = TARGET_COMPANIES
        if args.company:
            targets = [c for c in TARGET_COMPANIES if c["id"] == args.company]
            if not targets:
                print(f"[run] unknown company: {args.company}")
                print(f"[run] available: {[c['id'] for c in TARGET_COMPANIES]}")
                sys.exit(1)

        results = {}
        for company in targets:
            results[company["id"]] = run_company(company)

        print(f"\n{'='*60}")
        print("[run] SUMMARY")
        for cid, ok in results.items():
            status = "OK" if ok else "PARTIAL/FAILED"
            print(f"  {cid}: {status}")

    print("\n[run] building dashboard...")
    try:
        subprocess.run(
            [sys.executable, "build_dashboard.py"],
            cwd=Path(__file__).parent,
            check=True,
        )
        print("[run] dashboard built → dashboard/index.html")
    except subprocess.CalledProcessError:
        print("[run] dashboard build failed", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
