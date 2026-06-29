import type { ReportContent, TeamId } from "./types";

// 데모 전용 구조화 콘텐츠 (실제 2026 신호 + 시뮬레이션 내부 데이터). DEMO_SEED=1 일 때만 활성화.
// emailBlocks 는 CEO에게 보내는 자연스러운 아침 보고처럼 작성됨.

export const DEMO_CONTENT: Record<TeamId, ReportContent> = {
  sales: {
    taskUpdates: [
      { category: "고객 수요", tag: "REAL", headline: "NVIDIA Vera Rubin 양산 돌입", detail: "GTC Taipei; 대규모 HBM 수요 견인.", source: "Bloomberg, Jun" },
      { category: "고객 수요", tag: "REAL", headline: "젠슨 황, SK하이닉스에 HBM 증산 요청", detail: "직접적인 수요 압박 신호.", source: "Bloomberg, Jun" },
      { category: "AI 서버 수요", tag: "REAL", headline: "AI 서버 캐비닛 2026년 28k → 60k+", detail: "GB300 출하 전년比 +129%.", source: "Morgan Stanley" },
      { category: "제품 할당", tag: "SIM", headline: "P1 HBM3E 수요가 공급능력 초과", detail: "NVIDIA 180k + AMD 120k + Microsoft 140k vs 제한된 공급.", source: "" },
      { category: "CRM 이슈", tag: "SIM", headline: "Microsoft, 부분 공급에 에스컬레이션", detail: "HBM3E 부분 할당 관련 관계 리스크.", source: "" },
      { category: "고객 동향", tag: "REAL", headline: "장기계약(LTA)으로 물량 선확보", detail: "모바일 DRAM LTA 최고 $21/GB 보도.", source: "Wccftech" },
    ],
    emailBlocks: [
      { type: "text", text: "안녕하세요. 핵심만 말씀드리면, 이번 분기 공급 가능량보다 수요가 훨씬 앞서 있고 NVIDIA가 직접 압박을 가하고 있습니다. 현재 영업 현황입니다." },
      { type: "text", text: "NVIDIA의 Vera Rubin 플랫폼이 GTC Taipei에서 양산에 돌입했고(Bloomberg, Jun), 젠슨 황이 공개적으로 HBM 증산을 요청했습니다(Bloomberg, Jun) — 공급을 얼마나 타이트하게 보는지 보여주는 드문 직접 신호입니다. 분석가들은 우리를 Rubin HBM4 물량의 약 60~70%로 보고 있어, 관계 주도권은 우리에게 있습니다." },
      { type: "table", title: "P1 신규 할당 — 주요 고객 (내부 추정)", columns: ["고객", "제품", "요청량(k)", "상태"], rows: [["NVIDIA", "HBM3E-12hi", "180", "확정"], ["AMD", "HBM3E-12hi", "120", "부분"], ["Microsoft", "HBM3E-12hi", "140", "부분"], ["Dell", "DDR5-6400", "1,500", "검토중"]] },
      { type: "text", text: "관건은 할당입니다. 이번 분기 HBM3E의 P1 요청량이 이미 가용 공급능력을 초과했고(내부 추정), Microsoft가 부분 공급에 대해 에스컬레이션했습니다. 단순 공급 문제가 아니라 관계 리스크로 다루고 있습니다." },
      { type: "chart", title: "AI 서버 캐비닛 수요, NVIDIA 플랫폼", unit: "천 대", bars: [{ label: "2025", value: 28, tag: "REAL" }, { label: "2026 (추정)", value: 60, tag: "REAL" }] },
      { type: "text", text: "주시 사항: 삼성·마이크론의 Rubin HBM4 인증 진척이 점유율을 잠식하는지 여부. 의사결정 요청: Microsoft 건 — P1 약정을 고수할지, 관계 보호를 위해 일부 물량을 풀지 방향을 주시기 바랍니다." },
    ],
  },
  marketing: {
    taskUpdates: [
      { category: "가격", tag: "REAL", headline: "2Q26 DRAM 전분기比 +58~63%", detail: "PC DDR5 +43~48%.", source: "TrendForce, Mar" },
      { category: "가격", tag: "REAL", headline: "HBM3E 2026년 약 +20% 인상", detail: "HBM 출하의 약 2/3.", source: "Digitimes, Dec" },
      { category: "시장 트렌드", tag: "REAL", headline: "DDR5 수익성, HBM3E 상회 전망", detail: "서버 DRAM이 수익 엔진.", source: "TrendForce" },
      { category: "경쟁사 동향", tag: "REAL", headline: "삼성 HBM4E 샘플(3.6 TB/s)", detail: "약 6개월 앞섰다고 주장.", source: "TechTimes, May" },
      { category: "경쟁사 동향", tag: "REAL", headline: "마이크론, Rubin HBM4 인증 통과", detail: "3사 경쟁 본격화.", source: "Bloomberg, Jun" },
      { category: "공급/생산능력", tag: "SIM", headline: "자사 HBM3E 라인 가동률 ~98%", detail: "여유 거의 없음.", source: "" },
    ],
    emailBlocks: [
      { type: "text", text: "안녕하세요. 가격 모멘텀이 계속 강해지고 있으며, 이제 HBM에 국한되지 않고 전반으로 확산되고 있습니다. 간단히 보고드립니다." },
      { type: "text", text: "범용 DRAM 계약가격이 2Q26에 전분기 대비 58~63% 상승할 전망이며, PC DDR5는 43~48% 상승합니다(TrendForce, Mar). 모바일이 두드러져 장기계약이 최고 $21/GB까지 체결되는 것으로 보도됐습니다. 전략적 포인트는, TrendForce가 올해 DDR5 수익성이 HBM3E를 상회할 것으로 보면서 마진 방어 지점이 달라진다는 점입니다." },
      { type: "table", title: "계약 가격, 2Q26", columns: ["부문", "전분기比", "비고"], rows: [["범용 DRAM", "+58~63%", "TrendForce, Mar"], ["PC DDR5", "+43~48%", "서버 주도 수요"], ["HBM3E", "+약 20%", "Digitimes, Dec"]] },
      { type: "chart", title: "계약가격 상승률, 2Q26", unit: "% (전분기比)", bars: [{ label: "DRAM (평균)", value: 60, tag: "REAL" }, { label: "DDR5", value: 45, tag: "REAL" }, { label: "HBM3E", value: 20, tag: "REAL" }] },
      { type: "text", text: "경쟁 측면에서 삼성이 업계 최초 HBM4E 샘플을 3.6 TB/s로 출하했고(TechTimes, May), 마이크론이 NVIDIA Rubin HBM4 인증을 통과했습니다(Bloomberg, Jun) — 이제 3사 경쟁이 현실입니다. 공급은 여전히 타이트해 의미 있는 증설은 2027년 하반기 이후로 예상되며, 자사 HBM3E 라인은 가동률 약 98%입니다(내부 추정)." },
      { type: "text", text: "주시 사항: 삼성의 HBM4E '최초' 내러티브가 우리 프리미엄을 압박하는지. 요청: 대외 메시지를 HBM에만 두지 말고 DDR5 수익성으로 확장하는 데 동의해 주시기 바랍니다." },
    ],
  },
  product_planning: {
    taskUpdates: [
      { category: "기술 사양", tag: "REAL", headline: "HBM4 2월부터 10 GT/s 양산", detail: "JEDEC 8 GT/s 대비 약 25%↑; 2048-bit.", source: "SK hynix IR / JEDEC" },
      { category: "생산/인증", tag: "REAL", headline: "3사 모두 Rubin HBM4 인증", detail: "당사가 가장 먼저 인증 착수.", source: "Bloomberg, Jun" },
      { category: "생산/인증", tag: "SIM", headline: "M15X HBM4 16단 수율 램프", detail: "1c 노드 성숙 중; 양산 목표 Q3.", source: "" },
      { category: "고객 기술 수요", tag: "SIM", headline: "NVIDIA, Q4까지 HBM4 48GB 요구", detail: "16단 일정 대비 타이트.", source: "" },
      { category: "AI 서버 로드맵", tag: "REAL", headline: "Blackwell, 하이엔드 GPU 출하의 70%+", detail: "Rubin은 2026 하반기 램프.", source: "TrendForce" },
      { category: "표준 및 경쟁사 로드맵", tag: "REAL", headline: "NVIDIA, HBM4 사양 완화 가능성", detail: "공급사 점유율 재편 소지.", source: "TrendForce, Feb" },
    ],
    emailBlocks: [
      { type: "text", text: "안녕하세요. HBM4는 이미 실재하고 출하 중이며, 이제 관건은 16단 실행과 NVIDIA의 사양 완화 여부입니다. 로드맵 현황입니다." },
      { type: "text", text: "당사는 2월부터 HBM4를 10 GT/s로 양산 중이며, 이는 JEDEC 8 GT/s 기준보다 약 25% 높습니다(SK hynix IR; JEDEC). 지난주 3사 모두 NVIDIA Rubin HBM4 인증을 통과했지만 당사가 가장 먼저 인증에 착수했고(Bloomberg, Jun), 이는 할당에 유리하게 작용할 것입니다." },
      { type: "table", title: "메모리 로드맵", columns: ["제품", "핵심 사양", "양산", "상태"], rows: [["HBM4 12단", "10 GT/s, 2048-bit", "2026년 2월", "출하 중"], ["HBM4 16단", "16단 적층", "2026 Q3(목표)", "램프(추정)"], ["LPDDR6 1c", "JESD209-6", "2026 하반기", "정상 진행"], ["HBM4E", "차세대", "2026 하반기(샘플)", "로드맵"]] },
      { type: "text", text: "내부적으로 주시할 항목은 M15X의 HBM4 16단 수율 램프입니다(내부 추정) — NVIDIA가 Q4까지 48GB HBM4를 원하는데 이 일정과 빠듯합니다. 별도로 TrendForce는(Feb) 업계 생산능력·수율 한계로 NVIDIA가 HBM4 사양을 완화할 수 있다고 지적했으며, 현실화 시 점유율이 재편될 수 있습니다." },
      { type: "chart", title: "세대별 HBM 스택 대역폭", unit: "TB/s", bars: [{ label: "HBM3E", value: 1.2, tag: "REAL" }, { label: "HBM4", value: 2.0, tag: "REAL" }, { label: "HBM4E (샘플)", value: 3.6, tag: "REAL" }] },
      { type: "text", text: "주시 사항: Rubin 램프 대비 16단 양산 시점. 요청: 16단 일정 보호와 10 GT/s 성능 리더십 유지를 우선해 주시기 바랍니다." },
    ],
  },
};
