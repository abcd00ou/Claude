-- Price Intelligence DB Schema
-- PostgreSQL

-- SKU 마스터
CREATE TABLE IF NOT EXISTS skus (
    sku_id   TEXT PRIMARY KEY,
    brand    TEXT NOT NULL,      -- samsung | sandisk | lexar
    category TEXT NOT NULL,      -- portable_ssd | internal_ssd | microsd
    model    TEXT NOT NULL,
    capacity TEXT,
    notes    TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- URL 카탈로그 (SKU × 국가 × 소스)
CREATE TABLE IF NOT EXISTS sku_urls (
    id           SERIAL PRIMARY KEY,
    sku_id       TEXT REFERENCES skus(sku_id) ON DELETE CASCADE,
    country      TEXT NOT NULL,   -- US | KR | JP | DE
    source       TEXT NOT NULL,   -- amazon | manufacturer
    url          TEXT NOT NULL,
    is_active    BOOLEAN DEFAULT TRUE,
    last_verified_at TIMESTAMPTZ,
    UNIQUE(sku_id, country, source)
);

-- 가격 히스토리 (append-only)
CREATE TABLE IF NOT EXISTS price_observations (
    id               BIGSERIAL PRIMARY KEY,
    run_id           TEXT NOT NULL,
    sku_id           TEXT NOT NULL,
    country          TEXT NOT NULL,
    source           TEXT NOT NULL,
    observed_at      TIMESTAMPTZ NOT NULL,
    price            NUMERIC(12,2),
    currency         CHAR(3),
    original_price   NUMERIC(12,2),
    shipping_price   NUMERIC(12,2),
    availability     TEXT,        -- in_stock | out_of_stock | limited | unknown
    seller_name      TEXT,
    fulfillment      TEXT,        -- FBA | FBM | 3P | official
    offer_scope      TEXT,        -- buybox | top_offers | unknown
    content_hash     TEXT,
    raw_path         TEXT,
    parse_confidence REAL,
    parse_notes      TEXT,
    is_accepted      BOOLEAN DEFAULT TRUE,
    created_at       TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(run_id, sku_id, country, source, content_hash)
);

-- 인덱스 (조회 성능)
CREATE INDEX IF NOT EXISTS idx_price_obs_sku_country ON price_observations(sku_id, country);
CREATE INDEX IF NOT EXISTS idx_price_obs_observed_at ON price_observations(observed_at DESC);
CREATE INDEX IF NOT EXISTS idx_price_obs_run_id ON price_observations(run_id);

-- HITL 큐
CREATE TABLE IF NOT EXISTS hitl_queue (
    id             SERIAL PRIMARY KEY,
    run_id         TEXT,
    sku_id         TEXT,
    country        TEXT,
    source         TEXT,
    priority       TEXT,          -- P0 | P1
    reason         TEXT,
    evidence       JSONB,
    status         TEXT DEFAULT 'pending', -- pending | approved | fixed | ignored
    human_note     TEXT,
    decided_at     TIMESTAMPTZ,
    created_at     TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_hitl_status ON hitl_queue(status, priority);

-- 실행 로그
CREATE TABLE IF NOT EXISTS run_log (
    run_id           TEXT PRIMARY KEY,
    started_at       TIMESTAMPTZ,
    completed_at     TIMESTAMPTZ,
    total_targets    INT DEFAULT 0,
    success_count    INT DEFAULT 0,
    quarantine_count INT DEFAULT 0,
    hitl_count       INT DEFAULT 0,
    status           TEXT          -- completed | failed | partial
);
