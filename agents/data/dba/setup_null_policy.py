"""
setup_null_policy.py — null_policy 테이블 생성 및 초기 데이터 입력.

null_type 종류:
  structural_zero : 기업 비즈니스 모델상 해당 항목이 구조적으로 0인 경우.
                    (예: 소프트웨어 기업 inventory = 0, 유틸리티 receivables 미분류 등)
                    → build_panel_long.py가 NULL → 0으로 채워 DIO/DPO 계산 오류를 방지.
  data_gap        : 데이터를 수집하지 못한 것. NULL 그대로 유지.
  not_applicable  : 해당 지표 자체가 의미 없는 업종 (기록용).

Run: python3 setup_null_policy.py
"""
from __future__ import annotations
import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB = HERE / "financials.db"

# (ticker, item, null_type, reason)
# item은 panel_long item명 기준
POLICY: list[tuple[str, str, str, str]] = [
    # ── 소프트웨어·플랫폼: 재고(inventory) 구조적 제로 ──────────────────────
    # ai_platforms
    ("ADBE", "inventory", "structural_zero", "SaaS — 물리적 재고 없음"),
    ("NET",  "inventory", "structural_zero", "SaaS — 물리적 재고 없음"),
    ("DDOG", "inventory", "structural_zero", "SaaS — 물리적 재고 없음"),
    ("MDB",  "inventory", "structural_zero", "SaaS — 물리적 재고 없음"),
    ("PLTR", "inventory", "structural_zero", "SaaS — 물리적 재고 없음"),
    ("CRM",  "inventory", "structural_zero", "SaaS — 물리적 재고 없음"),
    ("NOW",  "inventory", "structural_zero", "SaaS — 물리적 재고 없음"),
    ("SNOW", "inventory", "structural_zero", "SaaS — 물리적 재고 없음"),
    # ai_software
    ("META", "inventory", "structural_zero", "광고 플랫폼 — 물리적 재고 없음"),
    # sw_equipment
    ("SNPS", "inventory", "structural_zero", "EDA 소프트웨어 — 물리적 재고 없음"),
    # hyperscalers (클라우드 서비스 수익이 주, 재고 미보고 분기 있음)
    ("GOOGL", "inventory", "structural_zero", "클라우드·광고 주력 — 재고 미중요"),
    ("MSFT", "inventory", "structural_zero", "SaaS·클라우드 주력 — 재고 미중요"),

    # ── 유틸리티·에너지: 전통 제조 재고 없음 ─────────────────────────────────
    ("CEG",  "inventory", "structural_zero", "원자력 유틸리티 — 연료 재고 별도 보고"),
    ("D",    "inventory", "structural_zero", "전력 유틸리티 — 물리적 재고 미분류"),
    ("NEE",  "inventory", "structural_zero", "신재생에너지 유틸리티 — 재고 미분류"),
    ("SO",   "inventory", "structural_zero", "전력 유틸리티 — 재고 미분류"),
    ("VST",  "inventory", "structural_zero", "전력 유틸리티 — 재고 미분류"),
    ("EQIX", "inventory", "structural_zero", "데이터센터 REIT — 재고 없음"),

    # ── neocloud: 하드웨어 GPU 구매하므로 data_gap (0 아님) ───────────────────
    ("CRWV", "inventory", "data_gap", "GPU 재고 있으나 미공개 분기 존재"),
    ("IREN", "inventory", "data_gap", "GPU 재고 있으나 미공개 분기 존재"),

    # ── 소프트웨어·플랫폼: AP(매입채무) 구조적 제로 ─────────────────────────
    # 물리적 공급업체 없으므로 AP가 0 또는 미공개인 경우
    ("PLTR", "accounts_payable", "structural_zero", "SaaS — 물리적 구매 AP 미중요"),
    ("SNOW", "accounts_payable", "structural_zero", "SaaS — 물리적 구매 AP 미중요"),
    ("MDB",  "accounts_payable", "structural_zero", "SaaS — 물리적 구매 AP 미중요"),
]


DDL = """
CREATE TABLE IF NOT EXISTS null_policy (
    ticker      TEXT NOT NULL,
    item        TEXT NOT NULL,
    null_type   TEXT NOT NULL CHECK(null_type IN ('structural_zero','data_gap','not_applicable')),
    reason      TEXT,
    updated_at  TEXT DEFAULT (date('now')),
    PRIMARY KEY (ticker, item)
)
"""


def setup():
    con = sqlite3.connect(DB)
    con.execute(DDL)
    con.execute("DELETE FROM null_policy")   # 전체 리셋 후 재입력 (멱등)
    con.executemany(
        "INSERT INTO null_policy(ticker, item, null_type, reason) VALUES (?,?,?,?)",
        POLICY,
    )
    con.commit()

    n = con.execute("SELECT COUNT(*) FROM null_policy").fetchone()[0]
    breakdown = con.execute(
        "SELECT null_type, COUNT(*) FROM null_policy GROUP BY null_type").fetchall()
    con.close()

    print(f"null_policy 설정 완료: {n}개 항목")
    for nt, c in breakdown:
        print(f"  {nt}: {c}개")


if __name__ == "__main__":
    setup()
