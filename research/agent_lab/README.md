# 에이전트 만들기 랩: 설계 문서

#ai-work-lab #agent #codex #date:2026-11-24

- **작성:** 2026-11-24
- **위치:** AI WORK LAB 사이트 사이드바 → 🤖 에이전트 만들기 랩 (https://ai-work-lab-khaki.vercel.app)
- **대체한 것:** 팀 과제 랩 v2(B2B 영업·마케팅·상품기획 암묵지 과제, `research/kkachilhan_ai/fde_team_track.md`). 2026-11-24 요청으로 "일반적인 에이전트 개발·자동화, 가장 많이 쓰는 사용 사례"로 교체.
- **사이트 코드:** `research/ai-work-lab/src/AgentLab.jsx`, `src/agentData.js` (git 미추적, 저장소 코드 금지 규칙)
- **시험 자료 원본:** `research/agent_lab/data/` (이 폴더)

## 구조

자습형. 공통 준비 3단계 → 프로젝트 7개(각 4~6단계) = 총 37단계. 모든 프로젝트가 같은 뼈대를 씁니다.

| 부품 | 맡는 것 |
|---|---|
| 트리거 | macOS launchd (정한 시각 · 간격 · 폴더 감시) |
| 수집 | 파이썬 표준 라이브러리 스크립트 (RSS, IMAP, OpenDART, 웹페이지) |
| 판단 | `~/agents/.agents/skills/<이름>/SKILL.md` 스킬을 `codex exec --sandbox workspace-write '$스킬'`로 실행 |
| 전달 | `~/agents/common/notify.py` (Gmail SMTP 앱 비밀번호, 텔레그램 봇) |
| 기억 | `state/` (처리한 항목), `logs/` (실행 기록), `profile.md` (내 기준) |
| 안전장치 | `--dry-run` 기본, 사람 승인, 하루 한도, 실패 시 텔레그램 알림 |

작업실은 `~/agents` 하나 (git 저장소 → AGENTS.md 상위·하위 적용). 비밀은 `~/agents/.env`에만.

단계 화면 구성: 만드는 것 → 왜 이렇게 하나 → 사람이 먼저 할 일 → 시험 자료 → Codex 프롬프트(목표·입력·처리·제약·검증) → 터미널 명령 → 채점 → 완료 기준 → 막히면 → 정답과 해설.

## 프로젝트와 단계

| 프로젝트 | 단계 | 시험 자료 |
|---|---|---|
| 🧰 공통 준비 | 작업실(AGENTS.md·.gitignore·.env) / 알림 통로(notify.py) / codex exec | - |
| 🌅 모닝 테크 브리핑 | 관심사 인터뷰 / fetch.py(시간대) / 묶기·고르기 / 브리핑 쓰기 / 발송·기억(run.sh) / 매일 07:00 launchd | news_sample.json |
| 📺 유튜브 요약 | transcript.py(yt-dlp 자막) / $yt-note / 볼 가치 판정 / 채널 RSS 감시 / 21:00 다이제스트 | - |
| 𝕏 X 테마 계정 + 수익화 | 테마·목소리 / 소재·관점 질문 / $x-writer(가중치 길이) / $x-checker / 승인·게시(웹 예약 또는 API) / 주간 분석·수익화 진척 | x_drafts.md |
| 📥 메일 비서 | triage.md / $mail-triage 채점 / IMAP 읽기(BODY.PEEK) / Gmail 임시보관함 초안(APPEND) / 평일 08:30·13:30 | inbox_sample.json |
| 📈 공시 알리미 | 인증키·corp_code / check_new.py(rcept_no) / $disclosure 유형별 숫자 / 평일 장중 30분 알림·18:00 요약 | - |
| 🔔 웹 변화 감시 | watch.json(조건·무시) / snapshot.py / $change-judge 채점 / 1시간 간격·중복 알림 방지 | page_changes.json |
| 📝 회의록 비서 | $minutes(미정 규칙·날짜 변환) / 시험 녹취 채점 / inbox WatchPaths / 마감 알림 | meeting_sample.md |

## 시험 자료와 정답 (모두 가상)

### news_sample.json (기사 15건)
- 창 2026-11-23 19:00 ~ 2026-11-24 07:00 KST 안: **13건** (A01~A13). 창 밖: A14(23일 18:30 KST), A15(22일).
- 시간대를 버리면 5건 (A03, A05, A09, A11, A12). 2026-11-24 파이썬으로 계산 확인.
- 묶음 **9개**: Atlas-3(A01·A02·A03) / 쿼크라인 투자(A04·A05) / 추론칩 분석(A06, 별도) / OpenMed-7B(A07) / Postgres TUI(A08) / 펠리컨 폰 9(A09) / 반토르 과징금(A10·A11) / 반토르 장애(A12, 별도) / EV 전해질(A13).

### x_drafts.md (초안 10개, 규칙 R1~R7)
- 게시: D1, D10
- 고쳐서 게시: D2(R1·R7), D5(R5), D6(R7), D9(R7: 가중치 315 > 280, 글자 수 186)
- 폐기: D3(R3 중복), D4(R4 자동 답글), D7(R6 투자 권유), D8(R2 복사)
- 가중치는 twitter-text 방식(한글 2, 영문·숫자·공백 1, URL 23)으로 계산: D1 169, D6 155, D9 315, D10 각 97·80·135·57.

### inbox_sample.json (메일 12통)
- 답장 필요: E01, E02, E08, E11
- 읽기만: E03, E06, E10(전체 공지), E12(결제 영수증)
- 뉴스레터·광고: E04, E09
- 위험·의심: E05(피싱), E07(메일 속 AI 지시문 = 프롬프트 인젝션)

### page_changes.json (변화 7건)
- 알림: C1(37,900 ≤ 38,000), C3(마케팅 공고 추가), C5(마감 12/05→12/12), C7(재입고)
- 무시: C2(리뷰 수), C4(D-day만), C6(배너·연도만)

### meeting_sample.md (회의일 2026-11-24 화)
- 결정 3: 출시일 12/15 / 인플루언서 1,200만→800만 원, 400만 원 검색광고 / 체험단 안 함
- 할 일 5: 오민수 11-25 · 한지민 11-27 · 정하늘 12-02(다음 주 수요일) · 담당 미정 12-01(법무 검토, 출시 2주 전) · 이도윤 11-26
- 할 일 아님: A/B 테스트(철회), 번들 할인(다음 회의 안건). 미결: 경쟁사 B 출시설.

## 확인한 사실 (2026-11-24)

- **codex exec**: 기본 읽기 전용 샌드박스, `--sandbox workspace-write`, `-o/--output-last-message`, `--skip-git-repo-check`, `--trust`, `--ephemeral`, stdin 파이프 지원. `--full-auto`는 더 이상 지원 안 함. CI에서는 `CODEX_API_KEY` 권장, ChatGPT 관리형 인증은 신뢰된 러너 전용 고급 옵션.
  **Source:** Non-interactive mode, OpenAI (learn.chatgpt.com/docs/non-interactive-mode), 2026-11-24 확인
- **예약 작업(Scheduled tasks)**: ChatGPT 데스크톱 앱에서 로컬 프로젝트 대상 예약 가능, 앱이 켜져 있어야 함. 결과는 Scheduled 목록. 기본 샌드박스로 실행되어 workspace-write는 네트워크 실패, 규칙으로 명령 허용 가능. 웹은 Gmail·Slack·GitHub 이벤트 트리거(요금제별). CLI·IDE에는 예약 관리 화면 없음.
  **Source:** Automations / Scheduled tasks, OpenAI (learn.chatgpt.com/docs/automations), 2026-11-24 확인
- **규칙 파일**: `~/.codex/rules/default.rules`, `prefix_rule(pattern=[...], decision="allow"|"prompt"|"forbidden")`, `codex execpolicy check`로 확인, 변경 후 재시작.
  **Source:** Rules, OpenAI (learn.chatgpt.com/docs/agent-configuration/rules), 2026-11-24 확인
- **설정 키**: `sandbox_workspace_write.network_access`(불리언), `web_search = disabled|cached|indexed|live`(기본 cached).
  **Source:** Configuration reference, OpenAI (learn.chatgpt.com/docs/config-file/config-reference), 2026-11-24 확인
- **GitHub Action**: `openai/codex-action@v1`, 입력 `prompt`/`prompt-file`, `openai-api-key`, `sandbox`.
  **Source:** GitHub Action, OpenAI (learn.chatgpt.com/docs/github-action), 2026-11-24 확인
- **X API 요금**: 종량제·선불 크레딧. 포스트 생성 $0.015, URL 포함 $0.200, 포스트 읽기 $0.005, 내 데이터 읽기 $0.001. 월 300만 포스트 읽기 상한.
  **Source:** Pricing, X Developer Platform (docs.x.com/x-api/getting-started/pricing), 2026-11-24 확인
- **X 수익화**: Creator Revenue Sharing 2026-09 종료 → Original Content Rewards. 조건(보도): 18세 이상, Premium·Premium+·Premium Business, 인증 팔로워 500, 최근 90일 인증 사용자 홈 타임라인 노출 50만. 복사·최소 수정·타 플랫폼 재업로드·관점 없는 모음은 제외.
  **Source:** "X Details Eligibility Rules For New Original Content Rewards Program", Net Influencer, 2026-09-03 (X 도움말 인용 2차 보도, help.x.com은 403으로 직접 확인 못 함) #confidence:medium
- **X 자동화 규칙**: 일반 자동 게시 허용, 키워드 검색 기반 자동 답글·자동 팔로우/언팔로우·자동 좋아요 금지, 자동화 계정은 운영 사실 표시 권장.
  **Source:** Automation rules, X Help Center (help.x.com/en/rules-and-policies/x-automation), 검색 결과 요약으로 확인 #confidence:medium
- **피드·API 응답 (직접 호출)**: hnrss.org, The Verge, Ars Technica, MIT TR, OpenAI News, Google AI Blog(새 주소 blog.google/innovation-and-ai/technology/ai/rss/), Hugging Face, GeekNews(feedburner로 리디렉션), 전자신문 200. TechCrunch 403. 유튜브 채널 RSS 200. OpenDART list.json 잘못된 키 → status 010 "등록되지 않은 인증키입니다."

## 결정

1. **실행 기본값은 내 Mac + launchd + codex exec.** ChatGPT Pro 구독 안에서 API 비용 없이 돌고, 잠자기 중 놓친 실행을 깨어날 때 돌려 줌(cron은 건너뜀). 데스크톱 앱 예약 작업과 GitHub Actions는 대안으로 안내.
2. **인터넷이 필요한 일은 codex exec 밖에서.** 수집·발송 스크립트는 run.sh에서 직접 실행하고, codex exec는 로컬 파일만 읽고 쓰게 해 샌드박스 네트워크 설정이 필요 없게 함.
3. **X는 반자동.** 원본성 조건과 자동화 규칙 때문에 "관점 한 줄은 사람, 게시는 승인 후". API 없이 웹 예약으로 가는 0원 경로도 둠.
4. **메일 비서는 발송 코드 없음.** 초안을 IMAP APPEND로 임시보관함에만. 프롬프트 인젝션 시험(E07) 포함.
5. **시험 자료로 채점하는 방식은 v2에서 유지.** 5개 프로젝트에 정답 있는 시험 자료.
