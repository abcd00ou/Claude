import type { TeamId } from "./types";

export interface TeamConfig {
  id: TeamId;
  label: string;
  subjectPrefix: string;
  focus: string;
  /** 업무 카테고리 — 각 일일 업데이트는 이 중 하나로 분류된다. 탭 패널을 구성. */
  categories: string[];
}

export const TEAMS: Record<TeamId, TeamConfig> = {
  sales: {
    id: "sales",
    label: "영업",
    subjectPrefix: "영업 — 고객 및 수요",
    focus:
      "고객 수요, 제품 할당, 주요 고객/CRM 신호, 그리고 그것이 장기 계약(LTA) 확보와 HBM 점유율 방어에 갖는 의미",
    categories: ["고객 수요", "제품 할당", "CRM 이슈", "AI 서버 수요", "고객 동향"],
  },
  marketing: {
    id: "marketing",
    label: "마케팅",
    subjectPrefix: "마케팅 — 시장 및 가격",
    focus: "메모리 시장 트렌드, DRAM/HBM/LPDDR 가격, 경쟁사 동향, 그리고 수급 균형",
    categories: ["가격", "시장 트렌드", "경쟁사 동향", "공급/생산능력", "시장 뉴스"],
  },
  product_planning: {
    id: "product_planning",
    label: "제품기획",
    subjectPrefix: "제품기획 — 로드맵 및 AI 서버",
    focus:
      "기술 로드맵(HBM4/HBM4E, LPDDR6, DDR5), AI 서버 로드맵, 고객 기술 수요, 생산/인증 신호",
    categories: ["AI 서버 로드맵", "기술 사양", "고객 기술 수요", "생산/인증", "표준 및 경쟁사 로드맵"],
  },
};

export const TEAM_IDS = Object.keys(TEAMS) as TeamId[];
