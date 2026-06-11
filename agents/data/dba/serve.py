"""
Live dashboard server — connects the dashboard directly to the SQLite databases.

Serves the dashboard and a /api/data endpoint that queries financials.db +
intelligence.db live on every request. Any DB update is reflected on page refresh
(no re-export needed).

Stdlib only — no external dependencies.

Run:  python3 serve.py            (default port 8765)
      python3 serve.py 9000       (custom port)

Then open:  http://localhost:8765/
"""
import sqlite3
import json
import sys
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from datetime import datetime

HERE      = Path(__file__).parent
FIN_DB    = HERE / "financials.db"
INTEL_DB  = HERE / "intelligence.db"
DASH_DIR  = HERE / "dashboard"
PORT      = int(sys.argv[1]) if len(sys.argv) > 1 else 8765

# Reuse the exact same join/mapping logic as the static exporter
sys.path.insert(0, str(HERE))
from export_dashboard_data import NAME_TO_SLUG, rows  # noqa: E402


def build_payload() -> dict:
    """Query both DBs live and return the dashboard JSON payload."""
    fin   = sqlite3.connect(FIN_DB)
    intel = sqlite3.connect(INTEL_DB)

    companies = rows(fin, "SELECT * FROM companies ORDER BY name")

    scm_by_slug = {}
    for r in rows(intel, "SELECT * FROM companies"):
        slug = NAME_TO_SLUG.get(r["company"].strip().lower())
        if not slug:
            continue
        scm_by_slug.setdefault(slug, []).append({
            "segment":  r.get("segment"),
            "role":     r.get("role"),
            "share":    f'{r.get("share_metric") or ""}: {r.get("share_value") or ""}'.strip(": ").strip(),
            "revenue":  r.get("latest_revenue"),
            "signal":   r.get("key_signal"),
            "sourced":  r.get("last_sourced"),
        })

    out = {"companies": [], "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"), "live": True}
    for c in companies:
        ticker = c["ticker"]
        qfin = rows(fin, """
            SELECT calendar_quarter, period_end_date, fiscal_year, fiscal_quarter,
                   revenue_usd_m, revenue_ai_dc_usd_m, revenue_yoy_pct, gross_margin_pct,
                   operating_income_usd_m, net_income_usd_m, capex_usd_m,
                   revenue_guidance_low_usd_m, revenue_guidance_high_usd_m,
                   source_doc, source_date, importance, notes
            FROM quarterly_financials WHERE ticker=? ORDER BY period_end_date""", (ticker,))
        afin = rows(fin, """
            SELECT fiscal_year, period_end_date, revenue_usd_m, gross_profit_usd_m,
                   gross_margin_pct, operating_income_usd_m, net_income_usd_m,
                   eps_diluted, source_doc
            FROM annual_financials WHERE ticker=? ORDER BY fiscal_year""", (ticker,))
        prices = rows(fin, """
            SELECT price_date, close_usd, volume, currency
            FROM stock_prices WHERE ticker=? ORDER BY price_date""", (ticker,))
        commentary = rows(fin, """
            SELECT earnings_date, calendar_quarter, quote, speaker, signal_type, segment, source_doc
            FROM earnings_commentary WHERE ticker=? ORDER BY earnings_date DESC""", (ticker,))
        out["companies"].append({
            "slug": c["slug"], "ticker": ticker, "name": c["name"], "exchange": c["exchange"],
            "segments": c["segments"].split(",") if c["segments"] else [],
            "hq_country": c["hq_country"], "fiscal_year_end": c["fiscal_year_end"],
            "currency": prices[-1]["currency"] if prices else "USD",
            "scm": scm_by_slug.get(c["slug"], []),
            "financials": qfin, "annual": afin, "prices": prices, "commentary": commentary,
        })
    fin.close(); intel.close()
    return out


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, body, ctype="application/json"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.wfile.write(body)

    def do_GET(self):
        path = self.path.split("?")[0]
        if path == "/api/data":
            try:
                payload = build_payload()
                self._send(200, json.dumps(payload, ensure_ascii=False))
            except Exception as e:
                self._send(500, json.dumps({"error": str(e)}))
            return
        # static file serving from dashboard dir
        rel = path.lstrip("/") or "index.html"
        fp = (DASH_DIR / rel).resolve()
        if not str(fp).startswith(str(DASH_DIR.resolve())) or not fp.is_file():
            self._send(404, "Not found", "text/plain")
            return
        ctype = {".html": "text/html", ".js": "application/javascript",
                 ".css": "text/css", ".json": "application/json"}.get(fp.suffix, "text/plain")
        self._send(200, fp.read_bytes(), ctype)

    def log_message(self, *a):  # quiet
        pass


if __name__ == "__main__":
    srv = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://localhost:{PORT}/"
    print(f"✅ Live dashboard — databases connected")
    print(f"   financials.db + intelligence.db queried live on each load")
    print(f"   {url}")
    print(f"   Ctrl+C to stop")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 stopped")
        srv.shutdown()
