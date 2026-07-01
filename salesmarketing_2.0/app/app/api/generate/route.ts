import { NextRequest, NextResponse } from "next/server";
import { TEAMS } from "@/lib/teams";
import { generateDraft } from "@/lib/anthropic";
import { setDraft } from "@/lib/store";
import { DEMO_CONTENT, regenerateDemo } from "@/lib/demoSeed";
import { renderEmailHtml } from "@/lib/emailTemplate";
import type { TeamId } from "@/lib/types";

export const runtime = "nodejs";
export const maxDuration = 300; // web search + opus can be slow; Vercel Pro allows 300s (Hobby caps at 60s)

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => ({}));
  const team = body.team as TeamId;
  const cfg = TEAMS[team];
  if (!cfg) return NextResponse.json({ error: "unknown team" }, { status: 400 });

  try {
    const { subject, html, content } = await generateDraft(cfg, {
      feedback: body.feedback || undefined,
      requestDataUpdate: !!body.requestUpdate,
    });
    const draft = {
      team: cfg.id,
      subject,
      content,
      html,
      status: "ready" as const,
      generatedAt: new Date().toISOString(),
      lastFeedback: body.feedback || undefined,
    };
    await setDraft(draft);
    return NextResponse.json({ draft });
  } catch (e) {
    const raw = e instanceof Error ? e.message : String(e);

    // Demo mode (DEMO_SEED=1): generation isn't available (no Anthropic key/credits),
    // so serve the seeded sample report instead of failing — same graceful path the
    // send button uses. Clearly still demo content.
    if (process.env.DEMO_SEED === "1") {
      const content = regenerateDemo(DEMO_CONTENT[cfg.id], {
        feedback: body.feedback || undefined,
        requestDataUpdate: !!body.requestUpdate,
      });
      const q = `${new Date().getUTCFullYear()}Q${Math.floor(new Date().getUTCMonth() / 3) + 1}`;
      const draft = {
        team: cfg.id,
        subject: `[${cfg.subjectPrefix}] — CEO 데일리 브리핑 ${q}`,
        content,
        html: renderEmailHtml(cfg, content),
        status: "ready" as const,
        generatedAt: new Date().toISOString(),
        lastFeedback: body.feedback || undefined,
      };
      await setDraft(draft);
      return NextResponse.json({ draft });
    }

    // Real path: turn the raw Anthropic billing error into a clear message.
    const msg = /credit balance is too low|Plans & Billing|insufficient_quota/i.test(raw)
      ? "Anthropic API 크레딧이 부족합니다. Plans & Billing에서 크레딧을 충전한 뒤 다시 시도해 주세요. (원본: " + raw.slice(0, 120) + ")"
      : raw;
    await setDraft({
      team: cfg.id,
      subject: cfg.subjectPrefix,
      content: null,
      html: "",
      status: "error",
      generatedAt: new Date().toISOString(),
      error: msg,
    });
    return NextResponse.json({ error: msg }, { status: 500 });
  }
}
