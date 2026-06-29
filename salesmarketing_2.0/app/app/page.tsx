"use client";

import { useEffect, useState } from "react";

type TeamId = "sales" | "marketing" | "product_planning";
interface TaskUpdate {
  category: string;
  tag: "REAL" | "SIM";
  headline: string;
  detail: string;
  source: string;
}
interface ReportContent {
  taskUpdates: TaskUpdate[];
  emailBlocks: unknown[];
}
interface Draft {
  team: TeamId;
  subject: string;
  content: ReportContent | null;
  html: string;
  status: "generating" | "ready" | "sent" | "error";
  generatedAt: string;
  sentAt?: string;
  sentSimulated?: boolean;
  error?: string;
}

const TABS: { id: TeamId; label: string }[] = [
  { id: "sales", label: "영업" },
  { id: "marketing", label: "마케팅" },
  { id: "product_planning", label: "제품기획" },
];

const STATUS_KO: Record<string, string> = {
  ready: "준비됨", sent: "전송됨", error: "오류", generating: "생성 중", none: "—",
};

function groupByCategory(updates: TaskUpdate[]): [string, TaskUpdate[]][] {
  const order: string[] = [];
  const map = new Map<string, TaskUpdate[]>();
  for (const u of updates) {
    if (!map.has(u.category)) { map.set(u.category, []); order.push(u.category); }
    map.get(u.category)!.push(u);
  }
  return order.map((c) => [c, map.get(c)!]);
}

export default function Home() {
  const [active, setActive] = useState<TeamId>("sales");
  const [drafts, setDrafts] = useState<Record<string, Draft>>({});
  const [busy, setBusy] = useState<string | null>(null);
  const [feedback, setFeedback] = useState("");
  const [err, setErr] = useState<string | null>(null);

  async function load() {
    const r = await fetch("/api/drafts");
    const j = await r.json();
    const map: Record<string, Draft> = {};
    for (const d of j.drafts as Draft[]) map[d.team] = d;
    setDrafts(map);
  }
  useEffect(() => { load(); }, []);

  const cur = drafts[active];
  const status = cur?.status ?? "none";
  const isBusy = busy === active;

  async function regenerate(useFeedback: boolean, requestUpdate: boolean) {
    setErr(null);
    setBusy(active);
    try {
      const r = await fetch("/api/generate", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ team: active, feedback: useFeedback ? feedback : undefined, requestUpdate }),
      });
      const j = await r.json();
      if (!r.ok) throw new Error(j.error || "생성 실패");
      setDrafts((d) => ({ ...d, [active]: j.draft }));
      setFeedback("");
    } catch (e) {
      setErr(e instanceof Error ? e.message : String(e));
    } finally { setBusy(null); }
  }

  async function approve() {
    setErr(null);
    setBusy(active);
    try {
      const r = await fetch("/api/approve", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ team: active }),
      });
      const j = await r.json();
      if (!r.ok) throw new Error(j.error || "전송 실패");
      setDrafts((d) => ({ ...d, [active]: j.draft }));
    } catch (e) {
      setErr(e instanceof Error ? e.message : String(e));
    } finally { setBusy(null); }
  }

  return (
    <>
      <div className="brandbar">
        <div className="wordmark">SK<span> hynix</span></div>
        <div className="sub">영업·마케팅 인텔리전스 · 대외비</div>
      </div>
      <header className="titlerow">
        <h1>CEO 데일리 브리핑 — 리더 검토</h1>
        <p>각 리더가 팀의 일일 업무 업데이트를 검토한 뒤 CEO에게 보고를 전송합니다 — 또는 다시 생성하거나 최신 데이터를 요청합니다.</p>
      </header>
      <main>
        <div className="tabs">
          {TABS.map((t) => (
            <button key={t.id} className={`tab ${active === t.id ? "active" : ""}`}
              onClick={() => { setActive(t.id); setErr(null); setFeedback(""); }}>
              {t.label}<span className="badge">{STATUS_KO[drafts[t.id]?.status ?? "none"]}</span>
            </button>
          ))}
        </div>

        <div className="panel">
          <div className="statusline">
            <span className={`pill ${status}`}>{STATUS_KO[status]}</span>
            {cur?.generatedAt && <span>갱신 {new Date(cur.generatedAt).toLocaleString("ko-KR")}</span>}
            {cur?.sentAt && <span>· CEO 전송 {new Date(cur.sentAt).toLocaleString("ko-KR")}{cur.sentSimulated ? " (시뮬레이션 · 미발송)" : ""}</span>}
          </div>

          {!cur && <div className="empty">아직 업데이트가 없습니다 — 오전 9시 작업이 생성합니다. 아래 “생성”으로 지금 만들 수 있습니다.</div>}
          {cur?.status === "error" && <div className="err">생성 오류: {cur.error}</div>}

          {cur?.content && (
            <>
              <div className="sectionhead">팀 일일 업무 업데이트</div>
              {groupByCategory(cur.content.taskUpdates).map(([cat, items]) => (
                <div className="cat" key={cat}>
                  <div className="cat-label">{cat}</div>
                  {items.map((u, i) => (
                    <div className="update" key={i}>
                      <div className="hl">
                        <span className={`chip ${u.tag === "REAL" ? "real" : "sim"}`}>{u.tag}</span>
                        <b>{u.headline}</b>
                      </div>
                      <div className="dt">{u.detail}</div>
                      {u.source && <div className="src">출처: {u.source}</div>}
                    </div>
                  ))}
                </div>
              ))}

              <div className="sectionhead" style={{ marginTop: 22 }}>CEO 보고 이메일</div>
              <div className="preview-wrap">
                <div className="preview-bar">
                  <b>받는 사람:</b> CEO &lt;abcd00ou@gmail.com&gt; &nbsp;·&nbsp; <b>제목:</b> {cur.subject}
                </div>
                <div className="preview-body" dangerouslySetInnerHTML={{ __html: cur.html }} />
              </div>
            </>
          )}

          <div className="actions">
            <button className="act send" disabled={isBusy || status !== "ready"} onClick={approve}>
              {status === "sent" ? (cur?.sentSimulated ? "전송됨 (시뮬레이션) ✓" : "전송됨 ✓") : "승인 후 CEO에게 전송"}
            </button>
            <button className="act regen" disabled={isBusy} onClick={() => regenerate(!!feedback, false)}>
              {cur ? "다시 생성" : "생성"}
            </button>
            <button className="act update" disabled={isBusy} onClick={() => regenerate(!!feedback, true)}>
              데이터 업데이트 요청
            </button>
          </div>
          <textarea rows={2} placeholder="선택: 무엇이 잘못됐는지 팀에 알려주세요 (다시 생성에 반영됩니다)…"
            value={feedback} onChange={(e) => setFeedback(e.target.value)} />
          {isBusy && <div className="note">작업 중… 웹 검색과 초안 작성에 최대 1분 정도 걸릴 수 있습니다.</div>}
          {err && <div className="err">{err}</div>}
        </div>
      </main>
    </>
  );
}
