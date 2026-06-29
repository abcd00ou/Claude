import { NextRequest, NextResponse } from "next/server";
import { getDraft, setDraft } from "@/lib/store";
import { sendToCeo } from "@/lib/email";
import type { TeamId } from "@/lib/types";

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
  const body = await req.json().catch(() => ({}));
  const draft = await getDraft(body.team as TeamId);
  if (!draft || draft.status !== "ready") {
    return NextResponse.json({ error: "no ready draft to send" }, { status: 400 });
  }
  try {
    const res = await sendToCeo(draft);
    const sent = { ...draft, status: "sent" as const, sentAt: new Date().toISOString(), sentSimulated: res.simulated };
    await setDraft(sent);
    return NextResponse.json({ draft: sent });
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    return NextResponse.json({ error: msg }, { status: 500 });
  }
}
