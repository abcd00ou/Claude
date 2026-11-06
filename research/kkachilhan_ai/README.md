# 까칠한 AI (황현태) 유튜브 분석

- **대상:** https://www.youtube.com/@kkachilhan-ai 본편 21개 (2026-02-23 ~ 2026-11-05)
- **작성일:** 2026-11-02 (2026-11-06 갱신: 11월 영상 2개 추가, 프로필 자료 추가)
- **목적:** 시간에 따른 화자의 인사이트를 정리합니다 (AI 발전, 엔터프라이즈 AX, 한국 FDE, 국가 AI 정책).

## 파일

| 파일 | 내용 |
|---|---|
| [insights.md](insights.md) | 시기 구분, 주제별 변화, FDE 정리, 정책 제안, 개념 사전 |
| [timeline.md](timeline.md) | 영상 21개 요약 (최신순) |
| [index.html](index.html) | 위 내용을 보기 좋게 만든 웹페이지 |
| [profile.md](profile.md) / [.html](profile.html) | 황현태 대표 소개 자료 (공개 기사·인터뷰와 영상 속 본인 발언 기준, 출처 표기) |
| [fde_curriculum.md](fde_curriculum.md) / [.html](fde_curriculum.html) | 분석 내용을 바탕으로 설계한 12주 FDE 양성 과정 |
| [fde_lab/](fde_lab/README.md) | 12주 실습 자료와 예상 산출물 (가상 제조사 케이스, 1인 FDE 목표) |
| `transcripts/` | 영상별 자막 전문 (`YYYY-MM-DD_<videoId>.md`). **로컬 전용, git 제외** |
| `raw_vtt/` | yt-dlp 원본 자막(.vtt)과 메타데이터(.info.json). **로컬 전용, git 제외** |

## 수집 방법
1. `yt-dlp --flat-playlist`로 채널의 `/videos` 탭 목록을 가져왔습니다 (2026-11-06 기준 21개).
2. `yt-dlp --skip-download --write-subs --write-auto-subs --sub-langs ko`로 한국어 자막과 메타데이터를 받았습니다.
3. VTT의 타임스탬프와 중복 줄을 정리해 약 350자 단위 문단으로 묶었습니다 (`[mm:ss]` 표시).
4. 자막 전문을 읽고 요약했습니다.

## 주의
- 자동 자막이 섞여 있어 고유명사 오기가 있습니다 (안묵지 → 암묵지, 스페이스와 → 스페이스와이 등). 일부 파일 끝에는 자동 자막의 파편이 중복되어 있습니다.
- 자막 전문은 저작권 문제로 원격 저장소에 올리지 않았습니다 (`.gitignore`).
- 요약 속 수치와 기업 사례는 화자 발언 기준이며 검증하지 않았습니다.
- 다시 수집하려면 위 2번 명령을 같은 출력 경로로 실행하면 됩니다 (yt-dlp는 별도 venv에 설치되어 있습니다).
