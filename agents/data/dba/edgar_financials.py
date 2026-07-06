"""
SEC EDGAR XBRL financials puller — deep history (back to 2016+) for US-SEC filers.

Uses the official companyfacts API (free, Tier A — sourced from 10-K/10-Q/20-F):
  https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json

Returns annual + quarterly financial rows mapping XBRL us-gaap concepts to the
financials.db schema columns. Foreign companies that don't file with the SEC
(most .KS/.T/.TW/.DE tickers) won't resolve to a CIK — those stay on yfinance.

Public API:
  cik_map()                  -> {TICKER: cik10}   (cached)
  pull(ticker, since=2016)   -> (annual_rows, quarterly_rows)

Each row is a dict keyed to financials.db columns. Tier A.
"""
import json
import time
import urllib.request
from datetime import date

UA = {"User-Agent": "AI-SCM-Research research@example.com"}
_CIK_CACHE = None

# XBRL us-gaap concept candidates per metric (first non-null wins)
CONCEPTS = {
    "revenue": ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues",
                "RevenueFromContractWithCustomerIncludingAssessedTax", "SalesRevenueNet"],
    "gross_profit": ["GrossProfit"],
    "operating_income": ["OperatingIncomeLoss"],
    "net_income": ["NetIncomeLoss", "ProfitLoss"],
    "eps_diluted": ["EarningsPerShareDiluted"],
    "capex": ["PaymentsToAcquirePropertyPlantAndEquipment",
              "PaymentsToAcquireProductiveAssets"],
    "ocf": ["NetCashProvidedByUsedInOperatingActivities",
            "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"],
    "cash": ["CashAndCashEquivalentsAtCarryingValue"],
    "inventory": ["InventoryNet"],
    "receivables": ["AccountsReceivableNetCurrent", "ReceivablesNetCurrent"],
    "payables": ["AccountsPayableCurrent", "AccountsPayableTradeCurrent",
                 "AccountsPayableAndAccruedLiabilitiesCurrent"],
    "total_assets": ["Assets"],
    "equity": ["StockholdersEquity",
               "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest"],
    "lt_debt": ["LongTermDebtNoncurrent", "LongTermDebt"],
    "st_debt": ["LongTermDebtCurrent", "DebtCurrent"],
}
INSTANT = {"cash", "inventory", "receivables", "payables",
           "total_assets", "equity", "lt_debt", "st_debt"}


def _get(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=25) as r:
                return json.loads(r.read())
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(1.0)


def cik_map():
    global _CIK_CACHE
    if _CIK_CACHE is None:
        data = _get("https://www.sec.gov/files/company_tickers.json")
        _CIK_CACHE = {v["ticker"].upper(): str(v["cik_str"]).zfill(10) for v in data.values()}
    return _CIK_CACHE


def _units(facts, names):
    """Merge the unit entries across ALL candidate concepts (companies switch
    XBRL tags across years, e.g. Revenues → RevenueFromContract...)."""
    gaap = facts.get("facts", {}).get("us-gaap", {})
    out = []
    for n in names:
        if n in gaap:
            units = gaap[n]["units"]
            for u in ("USD", "USD/shares", "shares"):
                if u in units:
                    out.extend(units[u])
    return out


def _days(a, b):
    from datetime import datetime
    d0 = datetime.fromisoformat(a); d1 = datetime.fromisoformat(b)
    return (d1 - d0).days


def pull(ticker, since=2016):
    """Return (annual_rows, quarterly_rows) from EDGAR for a US-SEC filer, or ([],[])."""
    cik = cik_map().get(ticker.upper())
    if not cik:
        return [], []
    try:
        facts = _get(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json")
    except Exception:
        return [], []

    annual = {}     # fy -> {metric: val, period_end}
    quarterly = {}  # (fy, q) -> {metric: val, period_end}

    for metric, names in CONCEPTS.items():
        for e in _units(facts, names):
            fy = e.get("fy"); fp = e.get("fp"); end = e.get("end"); val = e.get("val")
            form = e.get("form", "")
            if fy is None or fy < since or val is None or not end:
                continue
            if metric in INSTANT:
                # balance-sheet (point in time): annual at FY end, quarterly at Q end
                if fp == "FY" and form.startswith("10-K"):
                    annual.setdefault(fy, {}).setdefault(metric, (val, end))
                elif fp in ("Q1", "Q2", "Q3", "Q4"):
                    quarterly.setdefault((fy, fp), {}).setdefault(metric, (val, end))
            else:
                start = e.get("start")
                if not start:
                    continue
                dur = _days(start, end)
                if fp == "FY" and 330 <= dur <= 400 and form.startswith("10-K"):
                    annual.setdefault(fy, {}).setdefault(metric, (val, end))
                elif fp in ("Q1", "Q2", "Q3", "Q4") and 80 <= dur <= 100:
                    # discrete ~3-month quarter only (skip YTD cumulative facts)
                    quarterly.setdefault((fy, fp), {}).setdefault(metric, (val, end))

    def to_row(d):
        g = lambda k: d[k][0] if k in d else None
        rev, gp = g("revenue"), g("gross_profit")
        ltd, std = g("lt_debt"), g("st_debt")
        debt = None
        if ltd is not None or std is not None:
            debt = (ltd or 0) + (std or 0)
        ocf, capex = g("ocf"), g("capex")
        fcf = (ocf - capex) if (ocf is not None and capex is not None) else None
        end = None
        for k in ("net_income", "revenue", "total_assets"):
            if k in d:
                end = d[k][1]; break
        return dict(
            revenue=_M(rev), gross_profit=_M(gp),
            gm=round(gp / rev * 100, 1) if (gp and rev) else None,
            op=_M(g("operating_income")), ni=_M(g("net_income")), eps=g("eps_diluted"),
            capex=_M(abs(capex)) if capex is not None else None,
            fcf=_M(fcf), ocf=_M(ocf), cash=_M(g("cash")), inv=_M(g("inventory")),
            recv=_M(g("receivables")), payables=_M(g("payables")), ta=_M(g("total_assets")),
            debt=_M(debt), eq=_M(g("equity")), period_end=end,
        )

    annual_rows = []
    for fy, d in sorted(annual.items()):
        r = to_row(d)
        if r["revenue"] is None and r["ni"] is None:
            continue
        r["fiscal_year"] = fy
        annual_rows.append(r)

    q_order = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
    quarterly_rows = []
    for (fy, fp), d in sorted(quarterly.items(), key=lambda x: (x[0][0], q_order.get(x[0][1], 9))):
        r = to_row(d)
        if r["revenue"] is None and r["ni"] is None:
            continue
        r["fiscal_year"] = fy; r["fiscal_quarter"] = q_order[fp]
        quarterly_rows.append(r)

    return annual_rows, quarterly_rows


def _M(v):
    return v / 1e6 if v is not None else None


if __name__ == "__main__":
    import sys
    t = sys.argv[1] if len(sys.argv) > 1 else "NVDA"
    a, q = pull(t)
    print(f"{t}: {len(a)} annual rows, {len(q)} quarterly rows")
    for r in a:
        print(f"  FY{r['fiscal_year']}: rev={r['revenue']:.0f}M  ni={r['ni']}  "
              f"assets={r['ta']}  inv={r['inv']}" if r['revenue'] else f"  FY{r['fiscal_year']}")
