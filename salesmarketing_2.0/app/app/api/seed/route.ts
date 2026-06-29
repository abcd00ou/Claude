import { NextResponse } from "next/server";
import { setDraft } from "@/lib/store";
import { DEMO_CONTENT } from "@/lib/demoSeed";
import { renderEmailHtml } from "@/lib/emailTemplate";
import { TEAMS, TEAM_IDS } from "@/lib/teams";

export const runtime = "nodejs";

// Demo only (DEMO_SEED=1): load the sample structured reports + render the branded
// SK hynix email so the UI can be shown without spending Anthropic credits.
export async function POST() {
  if (process.env.DEMO_SEED !== "1") {
    return NextResponse.json({ error: "not found" }, { status: 404 });
  }
  const q = `${new Date().getUTCFullYear()}Q${Math.floor(new Date().getUTCMonth() / 3) + 1}`;
  for (const id of TEAM_IDS) {
    const content = DEMO_CONTENT[id];
    await setDraft({
      team: id,
      subject: `[${TEAMS[id].subjectPrefix}] — CEO 데일리 브리핑 ${q}`,
      content,
      html: renderEmailHtml(TEAMS[id], content),
      status: "ready",
      generatedAt: new Date().toISOString(),
    });
  }
  return NextResponse.json({ seeded: TEAM_IDS });
}
