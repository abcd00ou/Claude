const { chromium } = require('playwright');
const { execSync } = require('child_process');
const fs = require('fs');

const TITLE = '삼성 T9 SSD 실측 속도 테스트 — USB 3.2 Gen 2×2, 실제로 얼마나 빠를까?';
const CONTENT = `외장 SSD를 고를 때 스펙표의 숫자만 믿기엔 불안한 분들 많으시죠?
저도 그런 분들 중 하나였습니다.

삼성전자 T9은 공식 스펙상 최대 읽기 2,000 MB/s를 지원한다고 명시되어 있는데, 실제로 내 PC에서도 그 속도가 나오는지 직접 측정해 봤습니다.

테스트는 CrystalDiskMark 벤치마크와 4K 영상 파일 실전 전송, 두 가지 방식으로 진행했습니다. 수치 중심으로 최대한 담백하게 정리해 드리겠습니다.


■ 테스트 환경 먼저 공개합니다

벤치마크 결과는 환경에 따라 크게 달라지기 때문에 조건을 먼저 밝히겠습니다.

- OS: Windows 11 (23H2)
- 연결 포트: USB 3.2 Gen 2×2 지원 Type-C 포트 (메인보드 후면)
- 케이블: 동봉 USB-C to C 케이블 사용 (0.5m)
- 측정 도구: CrystalDiskMark 8.0.4

포트 조건이 맞지 않으면 속도가 절반 이하로 떨어질 수 있어서, 반드시 Gen 2×2 지원 포트를 확인하시길 권장합니다.


■ CrystalDiskMark 실측값 — 순차 읽기·쓰기

테스트는 3회 반복 후 평균값을 사용했습니다.

순차 읽기 (SEQ1M Q8T1): 1,981 MB/s
순차 쓰기 (SEQ1M Q8T1): 1,847 MB/s
4K 랜덤 읽기 (Q32T16): 71.2 MB/s
4K 랜덤 쓰기 (Q32T16): 163.4 MB/s

순차 읽기는 공식 스펙(2,000 MB/s)에 근접한 수치가 확인됐습니다.
일반적인 USB 3.2 Gen 2 (10Gbps) 외장 SSD 대비 약 1.8배 수준입니다.


■ 4K 영상 10GB 실전 전송 — 실제로 몇 분 걸렸나

- 파일: 4K RAW 영상 10.2GB (단일 파일)
- 전송 방향: 내장 NVMe → T9
- 소요 시간: 약 58초
- 평균 전송 속도: 약 1,750 MB/s

10GB 넘는 파일이 1분 안에 전송되는 건 포터블 SSD로는 꽤 만족스러운 결과입니다.


■ 발열 및 SLC 캐시 이후 지속 속도 확인

- 초반 0~15GB 구간: 평균 1,700~1,800 MB/s 유지
- 15GB 이후 구간: 약 1,100~1,300 MB/s 수준으로 안정화
- 본체 표면 온도: 최대 약 42°C (실내 23°C 기준)
- 드라이브 온도: 최대 56°C

SLC 캐시 영역을 넘어서도 속도가 급격히 떨어지지 않고 안정적인 범위를 유지했습니다.


■ 수치 한눈에 정리

CrystalDiskMark 순차 읽기: 1,981 MB/s
CrystalDiskMark 순차 쓰기: 1,847 MB/s
10GB 파일 실전 전송 시간: 약 58초
연속 대용량 전송 후 속도: 1,100~1,300 MB/s
최대 본체 표면 온도: 약 42°C


▣ 오늘 내용 요약

1. 삼성 T9은 USB 3.2 Gen 2×2 환경에서 순차 읽기 약 1,981 MB/s, 쓰기 약 1,847 MB/s 실측 확인됐습니다.
2. 4K 영상 10GB 파일을 약 58초에 전송했으며, 대용량 연속 전송 후에도 1,100 MB/s 이상 유지했습니다.
3. 발열은 최대 표면 42°C 수준으로 관리되어 안정적인 동작이 확인됐습니다.


스펙과 가격, 용량별 옵션은 삼성전자 공식 스마트스토어에서 바로 확인하실 수 있습니다.
▶ 삼성전자 공식 스마트스토어에서 T9 SSD 보러 가기


여러분은 외장 SSD를 주로 어떤 용도로 활용하고 계신가요?
영상 편집 소스 보관인지, 게임 설치용인지, 아니면 단순 백업용인지 댓글로 알려주시면 다음 콘텐츠 기획에 참고하겠습니다!

#삼성T9SSD #삼성SSD속도 #외장SSD추천 #포터블SSD #USB32Gen2x2 #SSD속도테스트 #외장SSD실측 #삼성전자T9 #4K영상편집 #CrystalDiskMark`;

const SIGNAL_FILE = '/tmp/blog_continue';
const STATUS_FILE = '/tmp/blog_status.txt';

// 상태 파일에 메시지 기록
function setStatus(msg) {
  fs.writeFileSync(STATUS_FILE, msg, 'utf8');
  console.log(msg);
}

// 사용자가 해결하고 신호 파일 생성할 때까지 대기
async function waitForUser(instruction) {
  if (fs.existsSync(SIGNAL_FILE)) fs.unlinkSync(SIGNAL_FILE);
  setStatus(`\n⏸️  [일시정지] ${instruction}\n   → 해결 후 Claude에게 "계속해줘" 라고 말해주세요.`);
  while (!fs.existsSync(SIGNAL_FILE)) {
    await new Promise(r => setTimeout(r, 500));
  }
  fs.unlinkSync(SIGNAL_FILE);
  console.log('▶️  재개합니다...');
}

function copyToClipboard(text) {
  const tmp = '/tmp/naver_content.txt';
  fs.writeFileSync(tmp, text, 'utf8');
  execSync(`pbcopy < ${tmp}`);
}

(async () => {
  console.log('🚀 브라우저를 시작합니다...');
  const browser = await chromium.launch({ headless: false, args: ['--start-maximized'] });
  const context = await browser.newContext({ viewport: null, locale: 'ko-KR' });
  let page = await context.newPage();

  // ── STEP 1: 로그인 ──
  await page.goto('https://nid.naver.com/nidlogin.login', { waitUntil: 'domcontentloaded' });
  console.log('⏳ 로그인 완료를 자동 감지 중...');

  let loggedIn = false;
  for (let i = 0; i < 120; i++) {
    await page.waitForTimeout(1000);
    if (!page.url().includes('nidlogin') && !page.url().includes('nid.naver.com')) {
      loggedIn = true; break;
    }
  }
  if (!loggedIn) {
    setStatus('❌ 로그인 타임아웃');
    await browser.close(); return;
  }
  console.log('✅ 로그인 감지!');
  await page.waitForTimeout(1000);

  // ── STEP 2: 블로그 메인 이동 ──
  await page.goto('https://blog.naver.com', { waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(3000);

  // ── STEP 3: 글쓰기 버튼 → 새 탭 감지 ──
  console.log('🖱️  글쓰기 버튼 클릭 중...');

  // 새 탭을 기다리면서 클릭
  const [newPage] = await Promise.all([
    context.waitForEvent('page', { timeout: 10000 }).catch(() => null),
    (async () => {
      const btn = await page.$('a:has-text("글쓰기")') ||
                  await page.$('button:has-text("글쓰기")');
      if (btn) await btn.click();
      else console.log('⚠️  글쓰기 버튼을 못 찾았습니다.');
    })()
  ]);

  // 새 탭이 열렸으면 그쪽으로 전환
  if (newPage) {
    page = newPage;
    console.log('✅ 새 탭 감지 — 에디터 탭으로 전환');
  } else {
    console.log('   새 탭 없음 — 현재 페이지 유지');
  }

  console.log(`   현재 URL: ${page.url()}`);
  console.log('⏳ 에디터 로딩 대기 중 (8초)...');
  await page.waitForTimeout(8000);
  console.log(`   에디터 URL: ${page.url()}`);

  // ── STEP 4: 도움말 오버레이 닫기 ──
  console.log('🔍 도움말 오버레이 닫기 시도...');
  const overlaySelectors = [
    '.se-help-panel .close_button',
    '.se_help_layer .btn_close',
    'button[data-v-*].close',
    '[class*="help"][class*="close"]',
    '[class*="tooltip"] button',
    '.btn_close',
    'button[aria-label="닫기"]',
  ];
  let overlayClosed = false;
  for (const sel of overlaySelectors) {
    try {
      const el = await page.$(sel);
      if (el && await el.isVisible()) {
        await el.click();
        overlayClosed = true;
        console.log(`   ✅ 오버레이 닫기 (${sel})`);
        await page.waitForTimeout(600);
      }
    } catch (_) {}
  }
  await page.keyboard.press('Escape');
  await page.waitForTimeout(500);

  if (!overlayClosed) {
    setStatus('⚠️  [확인 필요] 도움말 팝업이 자동으로 닫히지 않았습니다.\n   → 브라우저에서 도움말/팝업을 직접 닫아주세요.');
    await waitForUser('도움말/팝업을 브라우저에서 직접 닫아주세요.');
  }

  // ── STEP 5: 제목 입력 ──
  console.log('\n✏️  제목 입력 시도...');
  const frames = [page, ...page.frames()];
  const titleSelectors = [
    '.se-title-text',
    '.se-title-text p',
    'div.se-title-text[contenteditable]',
    'p[contenteditable="true"]',
    'div[contenteditable="true"]',
    'input#subject',
  ];

  let titleDone = false;
  for (const frame of frames) {
    for (const sel of titleSelectors) {
      try {
        const el = await frame.$(sel);
        if (el && await el.isVisible()) {
          await el.click();
          await page.waitForTimeout(400);
          await page.keyboard.press('Meta+a');
          await page.waitForTimeout(200);
          await page.keyboard.type(TITLE, { delay: 10 });
          titleDone = true;
          console.log(`   ✅ 제목 입력 완료 (${sel})`);
          break;
        }
      } catch (_) {}
    }
    if (titleDone) break;
  }

  if (!titleDone) {
    setStatus('⚠️  [확인 필요] 제목 자동 입력 실패!\n   → 브라우저에서 제목 입력란을 클릭하고 아래 제목을 직접 입력해주세요:\n   ' + TITLE);
    await waitForUser('제목을 직접 입력해주세요.');
  }

  await page.waitForTimeout(800);

  // ── STEP 6: 본문 붙여넣기 ──
  console.log('\n📋 본문 클립보드 복사 + 붙여넣기 시도...');
  copyToClipboard(CONTENT);
  console.log('   ✅ 클립보드 복사 완료');

  const bodySelectors = [
    '.se-text-paragraph p',
    '.se-main-container',
    '.se-content-container',
    '.se2_inputarea',
  ];

  let bodyDone = false;
  for (const frame of frames) {
    for (const sel of bodySelectors) {
      try {
        const el = await frame.$(sel);
        if (el && await el.isVisible()) {
          await el.click();
          await page.waitForTimeout(600);
          await page.keyboard.press('Meta+v');
          await page.waitForTimeout(2000);
          bodyDone = true;
          console.log(`   ✅ 본문 붙여넣기 완료 (${sel})`);
          break;
        }
      } catch (_) {}
    }
    if (bodyDone) break;
  }

  if (!bodyDone) {
    setStatus('⚠️  [확인 필요] 본문 자동 입력 실패!\n   → 브라우저에서 본문 영역을 클릭한 후 Cmd+V 로 붙여넣기 해주세요.\n   (클립보드에 이미 본문이 복사되어 있습니다)');
    await waitForUser('본문 영역 클릭 후 Cmd+V 로 붙여넣기 해주세요.');
  }

  // ── STEP 7: 완료 ──
  setStatus(`\n🎉 자동 입력 완료!\n\n📌 남은 작업 (직접 해주세요):\n   1. 태그 추가:\n      삼성T9SSD / 외장SSD추천 / 포터블SSD / USB32Gen2x2\n      SSD속도테스트 / 외장SSD실측 / 삼성전자T9\n      4K영상편집 / CrystalDiskMark / 삼성SSD속도\n   2. 카테고리 설정\n   3. 발행 버튼 클릭`);

  await page.waitForTimeout(600000);
  await browser.close();
})();
