"""
DB Agent — PostgreSQL ai_scm 데이터베이스 연동
psycopg2 없거나 DB 연결 실패 시 조용히 fallback
"""
import os, sys, json
from datetime import date

try:
    import psycopg2
    import psycopg2.extras
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False

DB_URL = os.environ.get("AI_SCM_DB", "postgresql://localhost:5432/ai_scm")

DDL = """
CREATE TABLE IF NOT EXISTS companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    layer VARCHAR(50),
    tier INTEGER,
    market_cap_billion FLOAT,
    description_ko TEXT,
    source_url TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS supply_chain_edges (
    id SERIAL PRIMARY KEY,
    from_company VARCHAR(100),
    to_company VARCHAR(100),
    relationship_type VARCHAR(50),
    description_ko TEXT,
    value_str VARCHAR(100),
    source_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS market_events (
    id SERIAL PRIMARY KEY,
    event_type VARCHAR(50),
    company VARCHAR(100),
    value_usd FLOAT,
    year INTEGER,
    description_ko TEXT,
    source_url TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE TABLE IF NOT EXISTS bottleneck_scores (
    id SERIAL PRIMARY KEY,
    layer VARCHAR(50),
    utilization_pct FLOAT,
    severity VARCHAR(20),
    description_ko TEXT,
    resolution_months INTEGER,
    run_date DATE DEFAULT CURRENT_DATE
);
CREATE TABLE IF NOT EXISTS investment_signals (
    id SERIAL PRIMARY KEY,
    company VARCHAR(100),
    layer VARCHAR(50),
    signal VARCHAR(30),
    thesis_ko TEXT,
    catalyst_ko TEXT,
    risk_ko TEXT,
    timeframe VARCHAR(50),
    source_url TEXT,
    run_date DATE DEFAULT CURRENT_DATE
);
CREATE TABLE IF NOT EXISTS model_results (
    id SERIAL PRIMARY KEY,
    scenario VARCHAR(20),
    year INTEGER,
    metric VARCHAR(50),
    value FLOAT,
    unit VARCHAR(20),
    run_date DATE DEFAULT CURRENT_DATE
);
CREATE TABLE IF NOT EXISTS hyperscaler_capex (
    id SERIAL PRIMARY KEY,
    company VARCHAR(100),
    year INTEGER,
    value_billion FLOAT,
    data_type VARCHAR(20),
    source_url TEXT,
    UNIQUE(company, year)
);
CREATE TABLE IF NOT EXISTS network_nodes (
    id SERIAL PRIMARY KEY,
    company VARCHAR(100),
    layer VARCHAR(50),
    market_cap_billion FLOAT,
    tier INTEGER,
    run_date DATE DEFAULT CURRENT_DATE
);
CREATE TABLE IF NOT EXISTS network_edges (
    id SERIAL PRIMARY KEY,
    from_company VARCHAR(100),
    to_company VARCHAR(100),
    relationship_type VARCHAR(50),
    description_ko TEXT,
    value_str VARCHAR(100),
    source_url TEXT,
    run_date DATE DEFAULT CURRENT_DATE
);
"""

def _connect():
    if not DB_AVAILABLE:
        return None
    try:
        conn = psycopg2.connect(DB_URL)
        return conn
    except Exception:
        return None

def init_db():
    conn = _connect()
    if not conn:
        print("  [DB] PostgreSQL 연결 불가 — 파일 기반으로 fallback")
        return False
    try:
        with conn.cursor() as cur:
            cur.execute(DDL)
        conn.commit()
        conn.close()
        print("  [DB] ai_scm DB 초기화 완료")
        return True
    except Exception as e:
        print(f"  [DB] 초기화 실패: {e}")
        conn.close()
        return False

def save_all(mapping_result=None, modeling_result=None,
             bottleneck_result=None, strategy_result=None):
    conn = _connect()
    if not conn:
        return False
    today = date.today()
    try:
        with conn.cursor() as cur:
            # 회사 정보 upsert
            if mapping_result and "company_map" in mapping_result:
                for name, info in mapping_result["company_map"].items():
                    cur.execute("""
                        INSERT INTO companies (name, layer, tier, updated_at)
                        VALUES (%s,%s,%s,NOW())
                        ON CONFLICT (name) DO UPDATE SET layer=EXCLUDED.layer, updated_at=NOW()
                    """, (name, info.get("layer",""), info.get("tier",0)))

            # 네트워크 노드/엣지
            if mapping_result and "network_graph" in mapping_result:
                ng = mapping_result["network_graph"]
                for node in ng.get("nodes", []):
                    cur.execute("""
                        INSERT INTO network_nodes (company, layer, market_cap_billion, tier, run_date)
                        VALUES (%s,%s,%s,%s,%s)
                    """, (node["id"], node.get("layer",""), node.get("market_cap_b",0), 0, today))
                for edge in ng.get("edges", []):
                    cur.execute("""
                        INSERT INTO network_edges
                        (from_company, to_company, relationship_type, description_ko, value_str, source_url, run_date)
                        VALUES (%s,%s,%s,%s,%s,%s,%s)
                    """, (edge["source"], edge["target"], edge["type"],
                          edge.get("description",""), edge.get("value",""),
                          edge.get("source_url",""), today))

            # 병목 스코어
            if bottleneck_result:
                for layer, info in bottleneck_result.get("layer_scores", {}).items():
                    cur.execute("""
                        INSERT INTO bottleneck_scores
                        (layer, utilization_pct, severity, description_ko, resolution_months, run_date)
                        VALUES (%s,%s,%s,%s,%s,%s)
                    """, (layer, info.get("utilization",0)*100,
                          info.get("severity",""), info.get("description",""),
                          info.get("resolution_months", 0), today))

            # 투자 시그널
            if strategy_result:
                for sig in strategy_result.get("investment_signals", []):
                    cur.execute("""
                        INSERT INTO investment_signals
                        (company, layer, signal, thesis_ko, catalyst_ko, risk_ko, timeframe, run_date)
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (sig.get("company",""), sig.get("layer",""),
                          sig.get("signal",""), sig.get("thesis",""),
                          sig.get("catalyst",""), sig.get("risk",""),
                          sig.get("timeframe",""), today))

            # CapEx 데이터
            sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            import config
            for company, years in config.HYPERSCALER_CAPEX.items():
                for yr, val in years.items():
                    year_int = int(yr.replace("_est",""))
                    dtype = "estimate" if "est" in yr else "actual"
                    url = config.REFERENCE_URLS.get(f"{company}_CapEx", "")
                    cur.execute("""
                        INSERT INTO hyperscaler_capex (company, year, value_billion, data_type, source_url)
                        VALUES (%s,%s,%s,%s,%s)
                        ON CONFLICT (company, year) DO UPDATE SET value_billion=EXCLUDED.value_billion
                    """, (company, year_int, val, dtype, url))

            # 모델 결과
            if modeling_result:
                for scenario, years_data in modeling_result.get("scenarios", {}).items():
                    for year, metrics in years_data.items():
                        if not isinstance(metrics, dict):
                            continue
                        for metric, value in metrics.items():
                            if isinstance(value, (int, float)):
                                cur.execute("""
                                    INSERT INTO model_results (scenario, year, metric, value, unit, run_date)
                                    VALUES (%s,%s,%s,%s,%s,%s)
                                """, (scenario, int(year), metric, float(value), "", today))

        conn.commit()
        conn.close()
        print("  [DB] 모든 데이터 저장 완료")
        return True
    except Exception as e:
        print(f"  [DB] 저장 실패: {e}")
        try:
            conn.rollback()
            conn.close()
        except Exception:
            pass
        return False

def run():
    """DB 초기화 및 상태 반환"""
    ok = init_db()
    return {"db_available": ok, "db_url": DB_URL if ok else "unavailable"}
