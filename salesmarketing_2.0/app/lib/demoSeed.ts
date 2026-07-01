import type { EmailBlock, ReportContent, TaskUpdate, TeamId } from "./types";

// 데모 전용 구조화 콘텐츠 (실제 2026 신호 + 시뮬레이션 내부 데이터). DEMO_SEED=1 일 때만 활성화.
// emailBlocks 는 CEO에게 보내는 자연스러운 아침 보고처럼 작성됨.

// 데모 모드 재생성: Anthropic 크레딧이 없을 때 "다시 생성"이 실제로 데이터를 갱신하고
// 보고서를 재작성하도록 한다. 원칙: 출처가 표기된 REAL(공개) 수치는 그대로 둔다(사실 왜곡
// 방지). 변하는 것은 SIM(내부 추정) 수치 — 새 크롤링/추정처럼 매번 소폭 갱신되고, 데이터
// 갱신 시각이 다시 찍히며, 도입부는 리더 코멘트를 반영해 다시 쓰인다.
// 크레딧이 있으면 실제 경로(lib/anthropic.ts)가 코멘트를 프롬프트에 넣어 진짜로 재작성한다.

function nowKstStamp(): string {
  // KST = UTC+9
  const d = new Date(Date.now() + 9 * 3600 * 1000);
  const p = (n: number) => String(n).padStart(2, "0");
  return `${d.getUTCFullYear()}-${p(d.getUTCMonth() + 1)}-${p(d.getUTCDate())} ${p(d.getUTCHours())}:${p(d.getUTCMinutes())} KST`;
}

// 호출 시각 기반 결정적(deterministic) 흔들림 — REAL이 아닌 SIM 수치에만 적용.
function jitter(value: number, seed: number): number {
  const wave = Math.sin(seed * 0.7 + value) * 0.06; // ±6%
  const out = value * (1 + wave);
  // 정수였던 값은 정수로, 소수였던 값은 소수 한 자리로 유지
  return Number.isInteger(value) ? Math.round(out) : Math.round(out * 10) / 10;
}

function jitterNumericString(s: string, seed: number): string {
  // "180", "1,500" 같은 순수 숫자 셀만 흔든다. 범위/기호가 섞인 셀(예 "+58~63%")은 그대로.
  const cleaned = s.replace(/,/g, "");
  if (!/^\d+$/.test(cleaned)) return s;
  const n = jitter(Number(cleaned), seed);
  return n.toLocaleString("en-US");
}

const TABLE_IS_SIM = (title?: string) => !!title && /추정|내부/.test(title);

const isNumericCell = (s: string) => /^\d+$/.test(s.replace(/,/g, ""));

// 회사명 별칭(오타/약어/한글 포함) → 표의 첫 열과 매칭하기 위한 정규화 키워드.
const COMPANY_ALIASES: Record<string, string[]> = {
  nvidia: ["nvidia", "nvdia", "nvida", "nvda", "엔비디아"],
  amd: ["amd", "에이엠디"],
  microsoft: ["microsoft", "msft", " ms ", "마이크로소프트"],
  dell: ["dell", "델"],
  samsung: ["samsung", "삼성"],
  micron: ["micron", "마이크론"],
};

// 리더 코멘트에서 "<회사> ... <숫자>[k]" 형태의 데이터 수정 지시를 추출한다.
// 예: "nvidia request changed 200k" → { company: "nvidia", value: 200 }
interface Directive { company: string; value: number; }
function parseDirectives(feedback: string): Directive[] {
  const lc = ` ${feedback.toLowerCase()} `;
  const out: Directive[] = [];
  for (const [canon, names] of Object.entries(COMPANY_ALIASES)) {
    const hit = names.find((n) => lc.includes(n));
    if (!hit) continue;
    const idx = lc.indexOf(hit);
    // 회사명 뒤에서 가장 가까운 숫자(+선택적 k)를 찾는다.
    const after = feedback.slice(Math.max(0, idx - 1));
    const m = after.match(/(\d[\d,]*)\s*([kK])?/);
    if (m) out.push({ company: canon, value: Number(m[1].replace(/,/g, "")) });
  }
  return out;
}

// 표의 한 행이 특정 회사 행인지(첫 열 기준).
function rowMatchesCompany(row: string[], canon: string): boolean {
  const first = (row[0] || "").toLowerCase();
  return (COMPANY_ALIASES[canon] || [canon]).some((n) => first.includes(n.trim())) || first.includes(canon);
}

export function regenerateDemo(
  base: ReportContent,
  opts: { feedback?: string; requestDataUpdate?: boolean },
): ReportContent {
  const seed = Math.floor(Date.now() / 1000) % 997;
  const stamp = nowKstStamp();
  const directives = opts.feedback ? parseDirectives(opts.feedback) : [];
  const applied: string[] = [];

  // 1) 데이터 갱신.
  //    - 지시(directive)가 있으면: 해당 회사 행의 수량 셀을 정확히 그 값으로 바꾸고, 다른 셀은
  //      흔들지 않는다(리더가 요청한 변화만 보이도록).
  //    - 지시가 없으면: SIM(내부 추정) 수치를 새 크롤링처럼 소폭 재산출.
  const emailBlocks: EmailBlock[] = base.emailBlocks.map((b) => {
    if (b.type === "chart") {
      if (directives.length > 0) return b;
      return {
        ...b,
        bars: b.bars.map((bar) => (bar.tag === "SIM" ? { ...bar, value: jitter(bar.value, seed) } : bar)),
      };
    }
    if (b.type === "table" && TABLE_IS_SIM(b.title)) {
      if (directives.length > 0) {
        const rows = b.rows.map((r) => {
          const d = directives.find((dir) => rowMatchesCompany(r, dir.company));
          if (!d) return r;
          const cellIdx = r.findIndex(isNumericCell);
          if (cellIdx === -1) return r;
          const next = [...r];
          next[cellIdx] = d.value.toLocaleString("en-US");
          applied.push(`${r[0]} ${d.value.toLocaleString("en-US")}`);
          return next;
        });
        return { ...b, rows };
      }
      return { ...b, rows: b.rows.map((r) => r.map((cell) => jitterNumericString(cell, seed))) };
    }
    return b;
  });

  // 2) 도입부 재작성 — 리더 코멘트/데이터 갱신 요청을 리더의 목소리로 반영(배너 X).
  const openings: string[] = [];
  if (applied.length > 0) {
    openings.push(`안녕하세요. 말씀 주신 대로 할당 수치를 수정했습니다 (${applied.join(", ")}).`);
  } else if (opts.feedback) {
    openings.push(`안녕하세요. 말씀 주신 “${opts.feedback}” 의견을 반영해 다시 정리했습니다.`);
  } else if (opts.requestDataUpdate) {
    openings.push(`안녕하세요. 최신 데이터로 다시 크롤링해 수치를 갱신했습니다.`);
  } else {
    openings.push(`안녕하세요. 데이터를 다시 갱신했습니다.`);
  }
  openings.push(`(데이터 갱신: ${stamp}${applied.length > 0 ? "" : " · 내부 추정치는 이번 갱신 기준으로 재산출"})`);
  // 첫 블록이 인사 텍스트면 교체, 아니면 앞에 삽입.
  if (emailBlocks[0]?.type === "text") {
    emailBlocks[0] = { type: "text", text: openings.join(" ") };
  } else {
    emailBlocks.unshift({ type: "text", text: openings.join(" ") });
  }

  // 3) 스캔 패널 상단에 갱신 로그 한 줄.
  const refreshUpdate: TaskUpdate = {
    category: "데이터 갱신",
    tag: "SIM",
    headline: applied.length > 0 ? "리더 지시로 할당 수치 수정" : opts.feedback ? "리더 코멘트 반영해 재생성" : "데이터 갱신 후 재생성",
    detail: applied.length > 0
      ? `수정: ${applied.join(", ")} · 갱신 ${stamp}`
      : `${opts.feedback ? `요청: ${opts.feedback} · ` : ""}내부 추정치 재산출, 갱신 ${stamp}`,
    source: "",
  };

  return { taskUpdates: [refreshUpdate, ...base.taskUpdates], emailBlocks };
}

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
