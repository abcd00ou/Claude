import { NextRequest, NextResponse } from "next/server";
import { TEAMS } from "@/lib/teams";
import { generateDraft } from "@/lib/anthropic";
import { setDraft } from "@/lib/store";
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
    const msg = e instanceof Error ? e.message : String(e);
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
