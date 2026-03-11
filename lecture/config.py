"""
lecture/config.py — AI 워크플로우 변화 강의 설정
대상: B2C 영업, 마케팅, 상품기획 담당자
"""

LECTURE_TITLE = "AI가 바꾸는 우리의 일하는 방식"
LECTURE_SUBTITLE = "B2C 실무자를 위한 AI 워크플로우 혁신 가이드"
LECTURE_AUTHOR = "AI Strategy Team"
LECTURE_DATE = "2026"

TARGET_AUDIENCE = ["B2C 영업", "마케팅", "상품기획"]

# ──────────────────────────────────────────────
# 강의 챕터 구성
# ──────────────────────────────────────────────
CHAPTERS = [
    {
        "id": 1,
        "title": "AI의 진화: 어떻게 여기까지 왔나",
        "subtitle": "질문-답변에서 CLI 에이전트까지",
        "slides": [
            "AI 등장 배경 — 2022~2026 타임라인",
            "1단계: 텍스트 Q&A (ChatGPT 3.5, 2022)",
            "2단계: 이미지·영상 생성 (DALL-E, Midjourney, Sora, 2023)",
            "3단계: 에이전트·스킬 (GPT Plugins, Claude Tools, 2024)",
            "4단계: CLI·코드 에이전트 (Claude Code, Cursor, 2025~)",
            "진화 요약: 사용성 & 자율성 확장 곡선",
        ],
        "color": "#1565C0",
    },
    {
        "id": 2,
        "title": "우리 업무는 어떻게 달라졌나",
        "subtitle": "영업·마케팅·상품기획 실무 변화",
        "slides": [
            "B2C 영업: 고객 분석 / 제안서 초안 / 반론 대응 스크립트",
            "마케팅: 콘텐츠 대량 생산 / A/B 카피 / SNS 이미지 생성",
            "상품기획: 트렌드 리포트 수집 / 경쟁사 분석 / 기획서 초안",
            "공통 패턴: 반복 업무 자동화 → 고부가 업무 집중",
            "Before / After 워크플로우 비교",
        ],
        "color": "#2E7D32",
    },
    {
        "id": 3,
        "title": "실전 데모: AI로 만드는 콘텐츠",
        "subtitle": "직접 보고, 직접 해보는 AI 활용",
        "slides": [
            "데모 1: 제품 소개 HTML 랜딩 페이지 30초 만들기",
            "데모 2: 마케팅 이미지 프롬프트 → 생성 결과 비교",
            "데모 3: 상품 기획서 초안 → AI 리뷰 → 완성본",
            "데모 4: 에이전트로 경쟁사 가격 자동 수집",
            "데모 5: 이 강의 자료도 AI가 만들었다",
        ],
        "color": "#6A1B9A",
    },
    {
        "id": 4,
        "title": "AI 에이전트: 자동화의 미래",
        "subtitle": "당신의 AI 팀원을 설계하는 법",
        "slides": [
            "에이전트란? — Tool + Memory + Orchestration",
            "실무 에이전트 예시: 주간 경쟁사 리포트 자동화",
            "실무 에이전트 예시: 신제품 캠페인 콘텐츠 파이프라인",
            "CLI 에이전트 시연: Claude Code로 코드 없이 자동화",
            "직접 만드는 첫 번째 에이전트 — 실습 가이드",
        ],
        "color": "#BF360C",
    },
    {
        "id": 5,
        "title": "지금 당장 시작하는 AI 워크플로우",
        "subtitle": "내일부터 써먹는 실전 로드맵",
        "slides": [
            "AI 도구 선택 기준: 역할별 추천 도구 매트릭스",
            "30일 실전 플랜: 영업 / 마케팅 / 상품기획",
            "프롬프트 잘 쓰는 법: TRIE 공식 (Task-Role-Input-Expectation)",
            "조직 도입 시 주의사항: 보안·저작권·환각",
            "마무리: AI는 대체가 아닌 증폭 — Q&A",
        ],
        "color": "#004D40",
    },
]

# ──────────────────────────────────────────────
# 슬라이드 디자인 설정
# ──────────────────────────────────────────────
SLIDE_DESIGN = {
    "title_font": "Pretendard",
    "body_font": "Pretendard",
    "fallback_font": "Apple SD Gothic Neo",
    "primary_color": "#1565C0",
    "accent_color": "#FF6F00",
    "bg_color": "#FFFFFF",
    "dark_bg": "#0D1B2A",
    "slide_width_emu": 12192000,   # 16:9 (33.87cm)
    "slide_height_emu": 6858000,   # 16:9 (19.05cm)
}

# ──────────────────────────────────────────────
# AI 진화 타임라인 데이터 (슬라이드에 직접 사용)
# ──────────────────────────────────────────────
AI_TIMELINE = [
    {
        "year": "2022",
        "month": "11월",
        "event": "ChatGPT 3.5 공개",
        "category": "텍스트 Q&A",
        "impact": "검색을 대화로 — 1억 명 2개월 돌파",
        "emoji": "💬",
    },
    {
        "year": "2023",
        "month": "3월",
        "event": "GPT-4 + 이미지 입력",
        "category": "멀티모달",
        "impact": "텍스트 + 이미지 동시 이해, 업무 분석 급증",
        "emoji": "🖼️",
    },
    {
        "year": "2023",
        "month": "7월",
        "event": "Midjourney V5 / DALL-E 3",
        "category": "이미지 생성",
        "impact": "디자이너 없이 마케팅 비주얼 제작 시대 개막",
        "emoji": "🎨",
    },
    {
        "year": "2023",
        "month": "11월",
        "event": "GPT-4 Turbo + Plugins / Assistants API",
        "category": "에이전트 v1",
        "impact": "외부 도구 연결 — 인터넷 검색, 코드 실행",
        "emoji": "🔌",
    },
    {
        "year": "2024",
        "month": "1월",
        "event": "Sora (텍스트→영상) 공개",
        "category": "영상 생성",
        "impact": "광고·제품 시연 영상을 프롬프트로 제작",
        "emoji": "🎬",
    },
    {
        "year": "2024",
        "month": "6월",
        "event": "Claude 3.5 Sonnet — Computer Use",
        "category": "에이전트 v2",
        "impact": "AI가 화면을 보고 앱을 직접 조작",
        "emoji": "🖱️",
    },
    {
        "year": "2025",
        "month": "2월",
        "event": "Claude Code (CLI 에이전트) 공개",
        "category": "CLI 에이전트",
        "impact": "터미널에서 코드·파일·시스템 전체 자동화",
        "emoji": "⚡",
    },
    {
        "year": "2025",
        "month": "하반기",
        "event": "Multi-Agent 협업 표준화 (MCP)",
        "category": "오케스트레이션",
        "impact": "전문 에이전트들이 팀처럼 협업하는 파이프라인",
        "emoji": "🤝",
    },
]

# ──────────────────────────────────────────────
# 직무별 워크플로우 Before/After
# ──────────────────────────────────────────────
WORKFLOW_CHANGES = {
    "영업": {
        "before": [
            "고객사 조사: 3~4시간 웹 서핑",
            "제안서 초안: 2~3일 작업",
            "반론 예상 답변: 경험과 기억에 의존",
            "콜드메일: 1건 작성 30분",
        ],
        "after": [
            "고객사 AI 분석 리포트: 15분",
            "제안서 초안 AI 생성 → 검수: 2~3시간",
            "반론 대응 시나리오 10개 자동 생성",
            "콜드메일 맞춤형 10개 버전: 5분",
        ],
        "tool_examples": ["Claude", "ChatGPT", "Perplexity", "Notion AI"],
    },
    "마케팅": {
        "before": [
            "SNS 콘텐츠 1건: 기획~발행 1~2일",
            "이미지 제작: 디자이너 의뢰 2~3일 대기",
            "카피라이팅 A/B 테스트: 수동 제작 제약",
            "트렌드 리포트: 주 1회 수동 정리",
        ],
        "after": [
            "SNS 콘텐츠 7일치 일괄 생성: 30분",
            "마케팅 이미지 즉시 생성·수정",
            "A/B 카피 50개 버전 자동 생성",
            "일간 트렌드 자동 수집·요약 에이전트",
        ],
        "tool_examples": ["Midjourney", "DALL-E 3", "Claude", "Jasper"],
    },
    "상품기획": {
        "before": [
            "경쟁사 분석: 주 8~10시간 리서치",
            "기획서 작성: 1~2주 소요",
            "소비자 리뷰 분석: 수백 건 수동 읽기",
            "트렌드 예측: 리포트 구매 비용 발생",
        ],
        "after": [
            "경쟁사 가격·스펙 자동 크롤링 & 비교",
            "기획서 초안 AI 생성 → 3일로 단축",
            "리뷰 수천 건 AI 감성 분석 & 인사이트",
            "SNS·커뮤니티 트렌드 자동 모니터링",
        ],
        "tool_examples": ["Claude Code", "Perplexity", "ChatGPT", "Pandas AI"],
    },
}

# ──────────────────────────────────────────────
# AI 산업 통계 데이터
# ──────────────────────────────────────────────
INDUSTRY_STATS = {
    "chatgpt_adoption": {
        "value": "1억 명",
        "timeframe": "2개월 만에",
        "label": "ChatGPT 사용자 달성",
        "context": "역사상 가장 빠른 제품 성장\nNetflix 3.5년 · Instagram 2.5년 · TikTok 9개월 대비",
        "bullets": [
            "ChatGPT 출시 5일 만에 100만 사용자",
            "2개월 만에 1억 명 → 역사상 최단 기록",
            "현재 전 세계 월간 사용자 2억 명 이상",
        ],
        "source": "UBS 2023 / OpenAI",
        "color": "#10A37F",
    },
    "mckinsey_value": {
        "value": "$4.4조",
        "timeframe": "연간 창출 가치",
        "label": "AI가 만들어내는 경제 가치",
        "context": "McKinsey Global Institute 추산\n글로벌 GDP의 약 3~5% 수준",
        "bullets": [
            "McKinsey: Generative AI $2.6~4.4T 연간 경제 기여",
            "마케팅·영업 분야 최대 $2.6T 영향",
            "고객 서비스 분야 생산성 30~45% 향상",
        ],
        "source": "McKinsey Global Institute 2023",
        "color": "#1565C0",
    },
    "microsoft_time_saved": {
        "value": "2.5시간",
        "timeframe": "매일 절약",
        "label": "AI 보조 업무자의 절감 시간",
        "context": "Microsoft Work Trend Index 2024\nCopilot 사용 직원 평균 절감량",
        "bullets": [
            "Microsoft: AI 도구 사용 직원 73% '업무 속도 향상'",
            "일주일 기준 평균 12.5시간 → 월 50시간 이상",
            "한국 직장인 평균 연 600시간 절약 가능",
        ],
        "source": "Microsoft Work Trend Index 2024",
        "color": "#0078D4",
    },
    "global_ai_workers": {
        "value": "75%",
        "timeframe": "2025년 기준",
        "label": "지식 근로자의 AI 사용 비율",
        "context": "LinkedIn 직업 기술 보고서\n3년 내 AI 리터러시가 필수 직무 역량",
        "bullets": [
            "LinkedIn: AI 활용 역량 채용 공고 21배 증가",
            "AI 사용 근로자 급여 평균 17% 더 높음",
            "국내 기업 60% 이상 AI 도입 계획 (2024 기준)",
        ],
        "source": "LinkedIn Future of Work Report 2024",
        "color": "#0A66C2",
    },
}

# ──────────────────────────────────────────────
# 직무별 통계 및 에이전트 데이터
# ──────────────────────────────────────────────
JOB_STATS = {
    "영업": {
        "headline_stat": "51%",
        "headline_label": "더 많은 거래 성사",
        "headline_source": "HubSpot State of AI 2024",
        "stats": [
            {"metric": "행정 업무 시간 감소", "value": "28%↓", "source": "HubSpot 2024"},
            {"metric": "거래 성사율 증가", "value": "51%↑", "source": "HubSpot 2024"},
            {"metric": "제안서 초안 제작 시간", "value": "3일→2시간", "source": "Salesforce 2024"},
            {"metric": "아웃리치 응답률", "value": "2배 향상", "source": "Outreach.io 2024"},
        ],
        "agent_workflow_steps": [
            "고객사 도메인 URL 입력",
            "Claude가 웹 검색으로 회사 개요·뉴스·담당자 수집",
            "제안서 템플릿 + 고객 맞춤 인사이트 병합",
            "예상 반론 10개 + 대응 스크립트 자동 생성",
            "CRM(Salesforce)에 미팅 노트 자동 저장",
            "미팅 전날 리마인더 이메일 자동 발송",
        ],
        "agent_examples": [
            {
                "name": "영업 준비 자동화 에이전트",
                "job_role": "영업",
                "description": "미팅 일정 등록 시 고객사 분석 리포트 + 반론 시나리오 자동 생성",
                "tools_used": ["Claude API", "Perplexity Search", "Salesforce API", "Gmail"],
                "output": "미팅 브리핑 PDF + 반론 10개 스크립트",
                "difficulty": "초급",
            },
            {
                "name": "콜드 아웃리치 맞춤화 에이전트",
                "job_role": "영업",
                "description": "고객 리스트 CSV 업로드 → 각 고객별 맞춤 이메일 50개 자동 생성",
                "tools_used": ["Claude API", "HubSpot API", "LinkedIn Data"],
                "output": "개인화 이메일 50개 초안",
                "difficulty": "초급",
            },
            {
                "name": "영업 성과 분석 에이전트",
                "job_role": "영업",
                "description": "CRM 데이터 주간 분석 → 성과 패턴 인사이트 + 액션 아이템 리포트",
                "tools_used": ["Claude API", "Salesforce API", "pandas"],
                "output": "주간 영업 인사이트 리포트",
                "difficulty": "중급",
            },
        ],
    },
    "마케팅": {
        "headline_stat": "10배",
        "headline_label": "콘텐츠 제작 속도 향상",
        "headline_source": "Jasper AI Internal Study 2024",
        "stats": [
            {"metric": "콘텐츠 제작 속도", "value": "10배↑", "source": "Jasper 2024"},
            {"metric": "A/B 카피 생성 시간", "value": "3일→30분", "source": "내부 벤치마크"},
            {"metric": "광고 클릭률(CTR) 개선", "value": "+18%", "source": "Persado 2024"},
            {"metric": "마케터 생산성", "value": "+40%", "source": "HubSpot 2024"},
        ],
        "agent_workflow_steps": [
            "제품명 / 타깃 / 시즌 키워드 입력",
            "Claude가 SNS별 최적 형식 분석 (인스타/X/링크드인)",
            "플랫폼별 7일치 카피 일괄 생성 (총 21개)",
            "DALL-E 3 연동으로 이미지 프롬프트 자동 생성",
            "Buffer/Hootsuite API로 예약 발행 스케줄 등록",
            "성과 데이터 기반 다음 주 방향 자동 피드백",
        ],
        "agent_examples": [
            {
                "name": "SNS 콘텐츠 파이프라인 에이전트",
                "job_role": "마케팅",
                "description": "매주 금요일 7일치 SNS 카피 21개 + 이미지 프롬프트 자동 생성",
                "tools_used": ["Claude API", "DALL-E 3", "Buffer API", "GA4 API"],
                "output": "주간 콘텐츠 캘린더 + 이미지 프롬프트 21개",
                "difficulty": "초급",
            },
            {
                "name": "A/B 테스트 자동화 에이전트",
                "job_role": "마케팅",
                "description": "제품 USP 입력 → 50개 광고 카피 변형 생성 → Meta API 자동 업로드",
                "tools_used": ["Claude API", "Meta Ads API", "Google Ads API"],
                "output": "50개 카피 변형 + 자동 게재",
                "difficulty": "중급",
            },
            {
                "name": "트렌드 모니터링 에이전트",
                "job_role": "마케팅",
                "description": "매일 오전 SNS·커뮤니티·뉴스 스캔 → 트렌드 키워드 + 콘텐츠 기회 알림",
                "tools_used": ["Claude API", "Perplexity", "Slack API"],
                "output": "일간 트렌드 알림 + 콘텐츠 아이디어 3개",
                "difficulty": "초급",
            },
        ],
    },
    "상품기획": {
        "headline_stat": "1,000배",
        "headline_label": "더 많은 데이터 처리 가능",
        "headline_source": "McKinsey Product Analytics Report 2024",
        "stats": [
            {"metric": "처리 가능 데이터 규모", "value": "1,000배↑", "source": "McKinsey 2024"},
            {"metric": "트렌드 조기 감지", "value": "3~6개월↑", "source": "Gartner 2024"},
            {"metric": "경쟁사 분석 시간", "value": "10시간→1시간", "source": "내부 사례"},
            {"metric": "기획서 작성 기간", "value": "2주→3일", "source": "내부 사례"},
        ],
        "agent_workflow_steps": [
            "분석 카테고리 + 경쟁사 URL 리스트 설정",
            "Playwright로 가격·스펙·리뷰 점수 자동 크롤링",
            "수천 건 리뷰 → Claude로 감성 분류 + 핵심 불만 추출",
            "SNS 키워드 모니터링 → 급상승 트렌드 신호 감지",
            "기획서 섹션별 AI 초안 생성 (시장→포지셔닝→로드맵)",
            "매주 경쟁사 변화 요약 리포트 자동 발송",
        ],
        "agent_examples": [
            {
                "name": "경쟁사 인텔리전스 에이전트",
                "job_role": "상품기획",
                "description": "매일 오전 경쟁사 가격·스펙 자동 수집 → 변동 감지 시 즉시 Slack 알림",
                "tools_used": ["Playwright", "Claude API", "pandas", "Slack API"],
                "output": "일간 경쟁사 변동 알림 + 주간 심층 분석",
                "difficulty": "중급",
            },
            {
                "name": "리뷰 인사이트 추출 에이전트",
                "job_role": "상품기획",
                "description": "Amazon/Coupang 리뷰 1,000건 수집 → 불만 유형 분류 + 개선 제안",
                "tools_used": ["Playwright", "Claude API", "pandas"],
                "output": "리뷰 감성 분석 리포트 + TOP10 불만 항목",
                "difficulty": "중급",
            },
            {
                "name": "기획서 초안 생성 에이전트",
                "job_role": "상품기획",
                "description": "카테고리 + 타깃 고객 입력 → 시장 분석·포지셔닝·로드맵 초안 자동 작성",
                "tools_used": ["Claude API", "Perplexity", "python-pptx"],
                "output": "기획서 초안 PPT (10~15슬라이드)",
                "difficulty": "초급",
            },
        ],
    },
}

# ──────────────────────────────────────────────
# TRIE 프롬프트 공식
# ──────────────────────────────────────────────
TRIE_FORMULA = {
    "name": "TRIE 프롬프트 공식",
    "subtitle": "4가지 요소만 기억하면 AI 프롬프트 마스터",
    "elements": [
        {
            "letter": "T", "word": "Task", "korean": "과제",
            "description": "AI에게 무엇을 시킬지 명확히",
            "example": '"고객사 제안서 초안을 작성해줘"',
            "bad_example": '"좋은 글 써줘"',
            "color": "#1565C0",
        },
        {
            "letter": "R", "word": "Role", "korean": "역할",
            "description": "어떤 전문가처럼 행동할지 지정",
            "example": '"당신은 10년 경력 B2B 영업 전문가입니다"',
            "bad_example": '"전문가처럼"',
            "color": "#2E7D32",
        },
        {
            "letter": "I", "word": "Input", "korean": "입력",
            "description": "필요한 배경 정보와 제약 조건",
            "example": '"고객사: 삼성전자, 예산: 5억, 납기: 3개월"',
            "bad_example": '"관련 정보 참고해서"',
            "color": "#6A1B9A",
        },
        {
            "letter": "E", "word": "Expectation", "korean": "기대 결과",
            "description": "원하는 출력 형식과 기준 명시",
            "example": '"PPT 5장, 각 장 핵심 3포인트, 한국어"',
            "bad_example": '"잘 정리해서"',
            "color": "#BF360C",
        },
    ],
}

# ──────────────────────────────────────────────
# 직무별 추천 도구 매트릭스
# ──────────────────────────────────────────────
TOOL_MATRIX = {
    "영업": [
        {"tool": "Claude.ai", "use_case": "제안서 초안, 이메일 맞춤화", "cost": "무료/월$20", "difficulty": "쉬움"},
        {"tool": "Perplexity AI", "use_case": "고객사 실시간 리서치", "cost": "무료/월$20", "difficulty": "쉬움"},
        {"tool": "Notion AI", "use_case": "미팅 노트 요약, CRM 메모", "cost": "월$16~", "difficulty": "쉬움"},
        {"tool": "Gong.io", "use_case": "영업 콜 AI 분석 + 코칭", "cost": "Enterprise", "difficulty": "보통"},
    ],
    "마케팅": [
        {"tool": "Claude.ai", "use_case": "카피라이팅, A/B 테스트 문구", "cost": "무료/월$20", "difficulty": "쉬움"},
        {"tool": "DALL-E 3 / Midjourney", "use_case": "마케팅 이미지 생성", "cost": "무료~월$60", "difficulty": "쉬움"},
        {"tool": "Canva AI", "use_case": "SNS 비주얼 빠른 제작", "cost": "무료/월$17", "difficulty": "쉬움"},
        {"tool": "Jasper AI", "use_case": "대량 콘텐츠 자동 생성", "cost": "월$49~", "difficulty": "보통"},
    ],
    "상품기획": [
        {"tool": "Claude.ai", "use_case": "기획서 초안, 리뷰 분석", "cost": "무료/월$20", "difficulty": "쉬움"},
        {"tool": "Perplexity AI", "use_case": "트렌드 리서치, 경쟁사 조사", "cost": "무료/월$20", "difficulty": "쉬움"},
        {"tool": "ChatGPT + Code Interpreter", "use_case": "데이터 분석, 차트 생성", "cost": "월$20", "difficulty": "보통"},
        {"tool": "Claude Code", "use_case": "크롤링 에이전트 구축", "cost": "월$20~", "difficulty": "보통"},
    ],
}

# ──────────────────────────────────────────────
# 30일 실전 플랜
# ──────────────────────────────────────────────
THIRTY_DAY_PLAN = {
    "week1": {
        "theme": "기초 다지기",
        "color": "#1565C0",
        "emoji": "🌱",
        "tasks": [
            "Claude.ai 가입 + TRIE 공식으로 첫 프롬프트 작성",
            "기존 반복 업무 1개를 AI로 대체 실험",
            "AI 산출물 검토·수정 습관 형성",
        ],
    },
    "week2": {
        "theme": "업무 적용",
        "color": "#2E7D32",
        "emoji": "🚀",
        "tasks": [
            "직무 핵심 업무 2개 AI 워크플로우로 전환",
            "프롬프트 개인 라이브러리 10개 이상 구축",
            "팀원에게 유용한 프롬프트 1개 공유",
        ],
    },
    "week3": {
        "theme": "자동화 첫 발",
        "color": "#6A1B9A",
        "emoji": "⚙️",
        "tasks": [
            "Zapier 또는 Make로 노코드 자동화 1개 설정",
            "반복 보고서 자동 생성 파이프라인 구축",
            "AI 품질 검수 체크리스트 완성",
        ],
    },
    "week4": {
        "theme": "에이전트 진입",
        "color": "#BF360C",
        "emoji": "🤖",
        "tasks": [
            "직무 맞춤 에이전트 설계서 직접 작성",
            "Claude Code로 첫 번째 자동화 스크립트 실행",
            "AI 도입 효과 측정 후 팀 발표",
        ],
    },
}

# ──────────────────────────────────────────────
# 주의사항 및 윤리
# ──────────────────────────────────────────────
CAUTION_ITEMS = [
    {
        "icon": "🔒",
        "title": "보안 & 개인정보",
        "risk": "고객 개인정보·내부 기밀을 공개 AI 서비스에 직접 입력 금지",
        "action": "데이터 익명화 처리 후 입력 / 사내 전용 AI 환경 구축",
        "color": "#C62828",
    },
    {
        "icon": "©️",
        "title": "저작권 & 상업 사용",
        "risk": "AI 생성 이미지·텍스트의 상업적 사용 시 라이선스 확인 필수",
        "action": "Adobe Firefly(상업용 안전 설계) 우선 사용 / 출처 기록 관리",
        "color": "#E65100",
    },
    {
        "icon": "🧠",
        "title": "환각(Hallucination)",
        "risk": "AI가 사실처럼 들리는 잘못된 수치·정보를 만들어낼 수 있음",
        "action": "수치·출처 포함 내용은 반드시 팩트체크 후 사용",
        "color": "#1565C0",
    },
    {
        "icon": "⚖️",
        "title": "편향성 & 공정성",
        "risk": "AI 학습 데이터의 편향으로 특정 집단에 불공정 결과 가능",
        "action": "다양한 관점 검토 / 최종 판단은 반드시 사람이 내릴 것",
        "color": "#4A148C",
    },
]

# ──────────────────────────────────────────────
# 컨텍스트 윈도우 진화 타임라인
# ──────────────────────────────────────────────
CONTEXT_EVOLUTION = [
    {"model": "GPT-2",      "year": 2019, "tokens": 1_024,      "color": "#94A3B8"},
    {"model": "GPT-3",      "year": 2020, "tokens": 2_048,      "color": "#64748B"},
    {"model": "GPT-3.5",    "year": 2022, "tokens": 4_096,      "color": "#1D4ED8"},
    {"model": "GPT-4",      "year": 2023, "tokens": 32_768,     "color": "#2563EB"},
    {"model": "Claude 2",   "year": 2023, "tokens": 100_000,    "color": "#0D6B4F"},
    {"model": "Gemini 1.5", "year": 2024, "tokens": 1_000_000,  "color": "#B91C1C"},
    {"model": "Claude 3.7", "year": 2025, "tokens": 200_000,    "color": "#0E7490"},
    {"model": "Gemini 2.0", "year": 2025, "tokens": 2_000_000,  "color": "#6D28D9"},
]

# ──────────────────────────────────────────────
# 토큰 · 컨텍스트 · 메모리 기술 데이터
# ──────────────────────────────────────────────
TOKEN_MEMORY = {
    "what_is_token": {
        "definition": "AI가 텍스트를 이해하는 최소 단위 — 단어 혹은 단어 조각",
        "analogy": "레고 블록처럼 언어를 작은 조각으로 분해한 것",
        "conversion": "1,000 토큰 ≈ 750 단어 ≈ A4 용지 1.5장",
        "examples": [
            "영어: 'Hello' = 1 토큰",
            "한국어: '안녕하세요' = 3~5 토큰",
            "GPT-4o 기준: 이미지 1장 = 약 170~300 토큰",
        ],
        "why_matters": "컨텍스트 윈도우 크기(처리 가능 정보량)와 API 비용을 결정",
    },
    "memory_types": [
        {
            "name": "컨텍스트 메모리",
            "icon": "💬",
            "color": "#1D4ED8",
            "description": "현재 대화창에 올라와 있는 텍스트 전체",
            "limit": "수천~수백만 토큰 (모델마다 다름)",
            "analogy": "책상 위에 펼쳐진 문서들",
            "use_case": "긴 계약서 요약, 멀티턴 대화, 코드 분석",
        },
        {
            "name": "외부 메모리 (RAG)",
            "icon": "🗄️",
            "color": "#0D6B4F",
            "description": "Vector DB에 저장, 필요할 때 검색·주입",
            "limit": "이론상 무한 (외부 저장소 크기에 의존)",
            "analogy": "도서관 — 필요한 책을 꺼내 책상에 올려놓음",
            "use_case": "사내 문서 QA, 제품 카탈로그 검색, 고객 히스토리",
        },
        {
            "name": "파인튜닝 메모리",
            "icon": "🧠",
            "color": "#6D28D9",
            "description": "모델 가중치 자체에 학습된 지식",
            "limit": "학습 시점 고정, 업데이트 비용 높음",
            "analogy": "오랜 경험으로 쌓인 전문 지식",
            "use_case": "특정 도메인 전문화, 말투·스타일 고정",
        },
        {
            "name": "에이전트 메모리",
            "icon": "📋",
            "color": "#B91C1C",
            "description": "작업 간 저장·전달되는 상태 정보",
            "limit": "설계에 따라 다름 (파일, DB, 변수)",
            "analogy": "To-Do 리스트 + 작업 일지",
            "use_case": "멀티스텝 자동화, 장기 프로젝트 관리",
        },
    ],
    "cost_trend": [
        {"period": "GPT-4\n(2023.03)", "model": "GPT-4",        "cost_per_1m_input": 30.0,  "relative": 100},
        {"period": "GPT-4o\n(2024.05)", "model": "GPT-4o",       "cost_per_1m_input": 5.0,   "relative": 17},
        {"period": "Claude 3.5\n(2024.10)", "model": "Claude 3.5 H", "cost_per_1m_input": 3.0, "relative": 10},
        {"period": "Claude 3.7\n(2025.02)", "model": "Claude 3.7 S", "cost_per_1m_input": 0.6, "relative": 2},
    ],
    "context_engineering": {
        "definition": "컨텍스트 윈도우를 전략적으로 채워 AI 성능을 극대화하는 기술",
        "why_matters": "모델 크기보다 무엇을 컨텍스트에 넣느냐가 결과 품질을 결정",
        "techniques": [
            {
                "name": "RAG (검색 증강 생성)",
                "desc": "외부 DB에서 관련 정보를 검색해 컨텍스트에 주입",
                "icon": "🔍",
            },
            {
                "name": "프롬프트 압축",
                "desc": "긴 컨텍스트를 LLMLingua 등으로 4x 압축해 비용 절감",
                "icon": "📦",
            },
            {
                "name": "대화 요약",
                "desc": "과거 대화를 요약본으로 교체해 윈도우 효율 유지",
                "icon": "📝",
            },
            {
                "name": "청킹 전략",
                "desc": "문서를 의미 단위로 분할해 검색 정확도 향상",
                "icon": "✂️",
            },
        ],
    },
    "new_architectures": [
        {
            "name": "KV 캐시 (Key-Value Cache)",
            "icon": "⚡",
            "color": "#1D4ED8",
            "desc": "이미 계산한 어텐션 결과를 재사용 → 반복 요청 속도 10x",
            "impact": "API 응답 속도 대폭 향상, 비용 절감",
            "status": "현재 모든 LLM 서비스에 적용",
        },
        {
            "name": "Mamba / SSM",
            "icon": "🌊",
            "color": "#0D6B4F",
            "desc": "Transformer 대신 선형 확장 State Space Model — 긴 시퀀스를 O(n)으로 처리",
            "impact": "100만 토큰 이상 초장문 처리 가능",
            "status": "연구 단계, Jamba(AI21) 등 상용화 중",
        },
        {
            "name": "Flash Attention",
            "icon": "🔥",
            "color": "#B91C1C",
            "desc": "GPU 메모리 I/O 최적화 — 어텐션 계산을 타일 단위로 처리",
            "impact": "학습 3x 빠름, VRAM 사용량 4x 절감",
            "status": "GPT-4, Claude, Gemini 모두 적용",
        },
        {
            "name": "Sparse MoE (Mixture of Experts)",
            "icon": "🎯",
            "color": "#6D28D9",
            "desc": "입력에 따라 필요한 전문가(expert) 모듈만 활성화",
            "impact": "파라미터 8x 확장해도 계산량은 동일",
            "status": "GPT-4, Gemini 1.5에 적용 (추정)",
        },
    ],
}

# ──────────────────────────────────────────────
# GPU / 하드웨어 데이터
# ──────────────────────────────────────────────
GPU_DATA = {
    "cpu_vs_gpu": {
        "cpu": {
            "cores": "8~32개",
            "type": "직렬(순차) 처리",
            "analogy": "천재 수학자 1명",
            "strength": "복잡한 로직, 조건 분기",
            "role": "OS, 앱, DB — 순서가 중요한 모든 것",
        },
        "gpu": {
            "cores": "수천~수만 개",
            "type": "병렬(동시) 처리",
            "analogy": "단순 계산 직원 수만 명",
            "strength": "행렬 곱셈, 벡터 연산 동시 처리",
            "role": "AI 학습·추론 — 수십억 번의 곱셈을 동시에",
        },
        "why_ai": "AI 학습 = 수십억 번의 행렬 곱셈 반복 → GPU가 CPU 대비 100~1,000배 빠름",
        "analogy_full": "ChatGPT 답변 1번 = A4 수만 장 분량의 행렬 곱셈. GPU 없이는 수년 걸릴 계산을 수초 만에.",
    },
    "gpu_evolution": [
        {"year": 2012, "model": "GTX 580", "tflops": 1.6,   "vram_gb": 1.5,  "event": "AlexNet — AI GPU 시대 개막"},
        {"year": 2016, "model": "P100",    "tflops": 21.2,  "vram_gb": 16,   "event": "딥러닝 전성시대"},
        {"year": 2020, "model": "A100",    "tflops": 312,   "vram_gb": 80,   "event": "GPT-3 학습"},
        {"year": 2022, "model": "H100",    "tflops": 1979,  "vram_gb": 80,   "event": "ChatGPT·GPT-4 학습"},
        {"year": 2024, "model": "H200",    "tflops": 4916,  "vram_gb": 141,  "event": "Claude 3.5·GPT-4o 추론"},
        {"year": 2025, "model": "B200",    "tflops": 9000,  "vram_gb": 192,  "event": "차세대 AGI 연구"},
    ],
    "nvidia_market": {
        "share": "70~80%",
        "moat": "CUDA 에코시스템 — 10년 이상 AI 연구자가 쌓아온 코드·라이브러리",
        "h100_price": "$25,000~40,000/개",
        "cloud_cost": "H100 클라우드 임대 $2~3/시간",
        "competitors": ["AMD MI300X", "Google TPU v5", "AWS Trainium 2", "Intel Gaudi 3"],
    },
    "training_compute": {
        "gpt3":       {"cost": "$4.6M",  "note": "A100 355 GPU-year 추정"},
        "gpt4":       {"cost": "$~100M", "note": "수만 H100, 수개월"},
        "llama3_70b": {"cost": "$2~5M",  "note": "Meta 공개 기준"},
        "key_insight": "학습 비용은 천문학적 — 그러나 추론(사용) 비용은 토큰당 $0.0001 수준",
    },
}

# ──────────────────────────────────────────────
# Transformer 아키텍처 데이터
# ──────────────────────────────────────────────
TRANSFORMER_DATA = {
    "overview": "2017년 Google 'Attention Is All You Need' 논문. 현재 GPT·Claude·Gemini 모두의 기반.",
    "key_idea": "단어(토큰) 간 '관계의 중요도'를 계산하는 Self-Attention 메커니즘",
    "analogy": "독서 토론처럼: 문장의 각 단어가 다른 단어와 얼마나 관련 있는지 서로 '투표'",
    "components": [
        {
            "name": "임베딩 (Embedding)",
            "desc": "'고양이'→[0.23, -0.71, ...] 3,000차원 숫자 배열로 변환. 의미가 비슷한 단어는 가까운 벡터.",
            "icon": "🔢",
            "color": "#1D4ED8",
        },
        {
            "name": "Self-Attention",
            "desc": "각 토큰이 다른 모든 토큰과의 '관련도 점수' 계산. '그것'이 '고양이'를 가리키는지 파악하는 핵심.",
            "icon": "🎯",
            "color": "#0D6B4F",
        },
        {
            "name": "피드포워드 (FFN)",
            "desc": "Attention 결과를 변환·압축. 모델의 '지식'이 주로 여기 저장됨. 레이어당 두 개의 선형 변환.",
            "icon": "⚙️",
            "color": "#B91C1C",
        },
        {
            "name": "레이어 스택",
            "desc": "Attention+FFN 과정을 32~128번 반복. 깊이가 깊을수록 추상적 개념 이해 → '의도' 파악 가능.",
            "icon": "📚",
            "color": "#6D28D9",
        },
    ],
    "scale_table": [
        {"model": "GPT-2",    "params": "1.5B",         "layers": 48,       "year": 2019},
        {"model": "GPT-3",    "params": "175B",         "layers": 96,       "year": 2020},
        {"model": "GPT-4",    "params": "~1.76T (MoE)", "layers": "비공개", "year": 2023},
        {"model": "Claude 3", "params": "비공개",       "layers": "비공개", "year": 2024},
        {"model": "Llama 3",  "params": "8B/70B/405B",  "layers": "다양",   "year": 2024},
    ],
    "token_generation": "출력 = 한 번에 한 토큰. 이전 토큰 전체를 참고해 다음 토큰을 확률적으로 선택 (Autoregressive Decoding)",
}

# ──────────────────────────────────────────────
# 학습(Training) vs 추론(Inference)
# ──────────────────────────────────────────────
TRAINING_INFERENCE_DATA = {
    "training": {
        "what": "수조 개의 문서로 수십억 개의 가중치(파라미터)를 반복 조정",
        "cost": "수억~수십억 달러, 수개월",
        "hardware": "수천 개 H100 GPU 클러스터 + 고속 네트워크 (InfiniBand)",
        "output": "수백 GB의 모델 가중치 파일",
        "energy": "GPT-3 학습 ≈ 500가구 연간 전력 소비",
        "analogy": "대학 4년 공부 → 뇌의 신경망(시냅스) 형성",
        "phases": ["사전학습 Pre-training", "지시 튜닝 SFT", "강화학습 RLHF", "안전 정렬 Constitutional AI"],
    },
    "inference": {
        "what": "학습된 모델 가중치를 로드해 사용자 입력에 응답 생성",
        "cost": "토큰당 $0.0001~0.003 (API 기준)",
        "hardware": "GPU 1~8개 (클라우드 임대 가능)",
        "speed": "초당 50~200 토큰 생성 (Claude Sonnet 기준)",
        "analogy": "졸업 후 실제 업무 수행 — 공부는 끝, 실력만 발휘",
        "latency": "첫 토큰 도달 0.3~2초, 이후 스트리밍 출력",
    },
    "fine_tuning": {
        "what": "사전학습 모델에 특정 도메인 데이터로 추가 학습",
        "cost": "$1K~100K (사전학습 대비 1/1,000)",
        "use_case": "사내 규정 특화, 특정 말투·스타일, 의료·법률 전문화",
        "analogy": "입사 후 사내 교육 3개월 — 기본기는 이미 있음",
    },
    "rag_vs_fine": {
        "rag": {"desc": "매번 외부 DB 검색 → 항상 최신 정보", "cost": "API 비용↑", "update": "실시간 가능"},
        "fine": {"desc": "모델에 지식 내재화 → 빠른 응답", "cost": "초기 학습 비용", "update": "재학습 필요"},
        "when_rag": "자주 바뀌는 정보, 사내 문서, 제품 카탈로그",
        "when_fine": "스타일 고정, 응답 형식 통일, 비공개 학습 데이터",
    },
}

# ──────────────────────────────────────────────
# 스케일링 법칙 (Scaling Laws)
# ──────────────────────────────────────────────
SCALING_LAWS_DATA = {
    "chinchilla": {
        "law": "최적 학습을 위해 파라미터 수 × 20배의 토큰이 필요",
        "example": "70B 파라미터 모델 → 1.4조 토큰으로 학습해야 최적",
        "insight": "크기만 키운다고 좋은 게 아님 — 데이터·컴퓨트 균형이 핵심",
        "source": "DeepMind Chinchilla 논문 (2022)",
    },
    "capability_levels": [
        {"params": "1B 이하",  "level": "기초", "desc": "기본 문장 완성, 번역, 간단한 Q&A",         "color": "#94A3B8"},
        {"params": "7B~13B",   "level": "실용", "desc": "추론, 코딩, 요약 가능 — 노트북에서 실행",  "color": "#1D4ED8"},
        {"params": "70B",      "level": "전문", "desc": "전문가 수준 분석, 복잡한 지시 이해",        "color": "#0D6B4F"},
        {"params": "200B+",    "level": "최고", "desc": "창의성, 멀티스텝 계획, 전문 분야 통달",     "color": "#B91C1C"},
    ],
    "efficiency_revolution": [
        {"year": "2020", "model": "GPT-3",   "params": "175B",  "note": "서버 클러스터 필요"},
        {"year": "2023", "model": "Llama 2", "params": "13B",   "note": "GPT-3급 성능, M1 Mac 실행"},
        {"year": "2024", "model": "Phi-3",   "params": "3.8B",  "note": "GPT-3.5급 성능, 스마트폰"},
        {"year": "2025", "model": "Phi-4",   "params": "14B",   "note": "GPT-4급 성능, 비용 1/10"},
    ],
    "trend": "같은 성능을 내는 데 필요한 파라미터 수가 매년 절반으로 — 효율 혁명 진행 중",
    "emergent": "특정 규모를 넘으면 갑자기 새 능력 등장 (Emergent Ability) — 예: GPT-3.5에서 갑작스런 코딩 능력",
}

# ──────────────────────────────────────────────
# VRAM 및 KV 캐시
# ──────────────────────────────────────────────
VRAM_KVCACHE_DATA = {
    "vram_overview": {
        "what": "GPU의 고속 메모리 — AI 모델 가중치 + 계산 버퍼 저장",
        "analogy": "요리사의 작업대 — 넓을수록 더 많은 재료(토큰)를 동시에 처리",
        "bottleneck": "VRAM 부족 = 느린 추론, 짧은 컨텍스트 제한",
    },
    "vram_requirements": [
        {"model": "Llama 3 8B",   "vram": "16GB",  "device": "RTX 4090 1개"},
        {"model": "Llama 3 70B",  "vram": "140GB", "device": "H100 2개"},
        {"model": "GPT-4 (추정)","vram": "~800GB","device": "H100 10개+"},
        {"model": "Claude 3.5",   "vram": "비공개","device": "클라우드 전용"},
    ],
    "kv_cache": {
        "what": "이미 계산한 Key-Value 어텐션 결과를 메모리에 저장·재사용",
        "problem": "Transformer는 매 토큰 생성 시 전체 이전 컨텍스트 재계산 필요",
        "solution": "이전 계산 결과를 VRAM에 캐시 → 새 토큰만 계산",
        "benefit": "반복 요청 속도 5~10x 향상, API 비용 절감",
        "analogy": "책을 처음부터 다시 읽지 않고 북마크에서 이어 읽기",
        "tradeoff": "컨텍스트가 길수록 KV 캐시 VRAM 증가 (컨텍스트 × 레이어 수 × 헤드 수)",
    },
    "memory_bandwidth": {
        "what": "GPU VRAM ↔ 연산 코어 간 데이터 전송 속도",
        "h100": "3.35 TB/s (H100 SXM5)",
        "bottleneck": "추론 시 가장 큰 병목 — 계산 속도보다 메모리 전송이 느림",
        "solution": "Flash Attention, Grouped Query Attention, 양자화(Quantization)",
    },
}

# ──────────────────────────────────────────────
# 멀티모달 AI
# ──────────────────────────────────────────────
MULTIMODAL_DATA = {
    "vision_pipeline": [
        "이미지 입력",
        "패치 분할 (16×16 픽셀 조각)",
        "각 패치를 토큰 임베딩으로 변환",
        "텍스트 토큰과 동일한 Transformer에 입력",
        "이미지+텍스트 통합 이해",
    ],
    "modalities": [
        {
            "name": "텍스트",
            "token_method": "BPE / SentencePiece",
            "token_count": "수십K 어휘",
            "examples": "GPT-4, Claude, Gemini",
            "icon": "📝",
            "color": "#1D4ED8",
        },
        {
            "name": "이미지",
            "token_method": "ViT 패치 (16×16px)",
            "token_count": "196~1,024 토큰/이미지",
            "examples": "GPT-4V, Claude 3, Gemini",
            "icon": "🖼️",
            "color": "#0D6B4F",
        },
        {
            "name": "음성",
            "token_method": "Mel-스펙트로그램 패치",
            "token_count": "~1,500 토큰/분",
            "examples": "Whisper, GPT-4o Audio",
            "icon": "🎙️",
            "color": "#B91C1C",
        },
        {
            "name": "동영상",
            "token_method": "프레임 샘플링 + 이미지 패치",
            "token_count": "수천~수만 토큰",
            "examples": "Gemini 1.5/2.0, GPT-4o",
            "icon": "🎬",
            "color": "#6D28D9",
        },
    ],
    "unified_space": "텍스트·이미지·음성을 같은 벡터 공간에 표현 → 서로 다른 모달이 '이해'",
    "business_value": [
        "계약서 이미지 → OCR 없이 직접 분석·요약",
        "제품 사진 → 설명문·마케팅 카피 즉시 생성",
        "회의 녹음 → 실시간 요약 + 액션 아이템 추출",
        "광고 영상 → 자동 자막 + 다국어 번역 + 하이라이트 편집",
    ],
}

# ──────────────────────────────────────────────
# AI 2026 최전선
# ──────────────────────────────────────────────
AI_FRONTIER_2026 = {
    "headline": "지금 가장 빠르게 바뀌고 있는 것들",
    "trends": [
        {
            "title": "추론 모델 (Reasoning)",
            "desc": "o1·o3·Claude 3.7 Extended Thinking — 답 전에 수십 초 '생각'. 수학·코딩·과학에서 인간 전문가 초월.",
            "icon": "🧠",
            "color": "#1D4ED8",
            "impact": "전략 보고서·투자 분석·R&D에 즉시 활용 가능",
        },
        {
            "title": "멀티에이전트 시스템",
            "desc": "여러 AI가 역할 분담하고 서로 검증. Claude가 코드 작성 → 다른 Claude가 테스트 → 또 다른 Claude가 배포.",
            "icon": "🤖",
            "color": "#0D6B4F",
            "impact": "24시간 자율 운영 가능한 AI 팀",
        },
        {
            "title": "컴퓨터 사용 (Computer Use)",
            "desc": "Claude·GPT-4o가 화면을 보고 마우스·키보드 직접 조작. RPA를 자연어로 대체.",
            "icon": "🖥️",
            "color": "#B91C1C",
            "impact": "ERP·CRM 수동 입력 자동화, 레거시 시스템 연동",
        },
        {
            "title": "실시간 멀티모달",
            "desc": "GPT-4o·Gemini Live — 영상·음성·화면을 동시에 보고 실시간 대화. 화상 회의 AI 코치.",
            "icon": "⚡",
            "color": "#6D28D9",
            "impact": "영업 실시간 코칭, 고객 응대 AI 어시스턴트",
        },
        {
            "title": "온디바이스 AI",
            "desc": "Phi-4·Gemma·Llama 3.2 — 서버 없이 스마트폰·노트북에서 실행. 데이터 외부 유출 없음.",
            "icon": "📱",
            "color": "#0E7490",
            "impact": "보안 데이터 로컬 처리, 인터넷 없는 환경 활용",
        },
        {
            "title": "비용 1/100 시대",
            "desc": "2023년 대비 API 비용 98% 감소. 2026년 Haiku급 성능을 하루 수천 번 써도 월 3천원.",
            "icon": "💰",
            "color": "#92400E",
            "impact": "AI 사용 '예산' 고민 끝 → 전략·프로세스 설계가 핵심",
        },
    ],
    "key_message": "기술보다 '어떻게 쓸 것인가'가 경쟁력 — 도구를 아는 사람이 아닌 프로세스를 설계하는 사람이 앞선다",
}

# ──────────────────────────────────────────────
# 경로 설정
# ────────────────────────────────────────��─────
import pathlib

BASE_DIR = pathlib.Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = BASE_DIR / "data"
WEBSITE_DIR = BASE_DIR / "website"

OUTPUT_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
