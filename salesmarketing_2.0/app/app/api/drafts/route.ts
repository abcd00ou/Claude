import { NextResponse } from "next/server";
import { getDraft } from "@/lib/store";
import { TEAM_IDS } from "@/lib/teams";

export const runtime = "nodejs";

export async function GET() {
  const drafts = await Promise.all(TEAM_IDS.map((t) => getDraft(t)));
  return NextResponse.json({ drafts: drafts.filter(Boolean) });
}
