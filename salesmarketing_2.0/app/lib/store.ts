import type { Draft, TeamId } from "./types";

// Draft store. Uses Vercel KV when configured (survives between the 9am cron run
// and the leader opening the app later). Falls back to an in-memory map for local
// dev / when KV isn't set up — note in-memory does NOT persist across serverless
// invocations, so production needs KV.

const KEY = (team: TeamId) => `draft:${team}`;
const useKv = !!process.env.KV_REST_API_URL && !!process.env.KV_REST_API_TOKEN;

const mem = new Map<string, Draft>();

export async function getDraft(team: TeamId): Promise<Draft | null> {
  if (useKv) {
    const { kv } = await import("@vercel/kv");
    return (await kv.get<Draft>(KEY(team))) ?? null;
  }
  return mem.get(KEY(team)) ?? null;
}

export async function setDraft(draft: Draft): Promise<void> {
  if (useKv) {
    const { kv } = await import("@vercel/kv");
    await kv.set(KEY(draft.team), draft);
    return;
  }
  mem.set(KEY(draft.team), draft);
}
