import { NextRequest, NextResponse } from "next/server";
import { TEAMS, TEAM_IDS } from "@/lib/teams";
import { generateDraft } from "@/lib/anthropic";
import { setDraft } from "@/lib/store";

export const runtime = "nodejs";
export const maxDuration = 300;

// Fired daily at 09:00 KST (00:00 UTC) by Vercel Cron — see vercel.json.
// Generates all 3 leader drafts so they're waiting when the leaders open the app.
// Does NOT send — sending is the human leader's approve action.
export async function GET(req: NextRequest) {
  // Vercel Cron attaches `Authorization: Bearer $CRON_SECRET` automatically when CRON_SECRET is set.
  const secret = process.env.CRON_SECRET;
  if (secret && req.headers.get("authorization") !== `Bearer ${secret}`) {
    return NextResponse.json({ error: "unauthorized" }, { status: 401 });
  }

  const results: Record<string, string> = {};
  for (const id of TEAM_IDS) {
    try {
      const { subject, html, content } = await generateDraft(TEAMS[id]);
      await setDraft({
        team: id,
        subject,
        content,
        html,
        status: "ready",
        generatedAt: new Date().toISOString(),
      });
      results[id] = "ready";
    } catch (e) {
      const msg = e instanceof Error ? e.message : String(e);
      await setDraft({
        team: id,
        subject: TEAMS[id].subjectPrefix,
        content: null,
        html: "",
        status: "error",
        generatedAt: new Date().toISOString(),
        error: msg,
      });
      results[id] = `error: ${msg}`;
    }
  }
  return NextResponse.json({ ranAt: new Date().toISOString(), results });
}
