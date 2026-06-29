import { Resend } from "resend";
import type { Draft } from "./types";

// Send an approved report to the CEO via Resend. This is the real, unattended
// send path (the claude.ai Gmail connector only drafts; a deployed app needs a
// mail API). Requires RESEND_API_KEY, REPORT_FROM_EMAIL, CEO_EMAIL.
export async function sendToCeo(draft: Draft): Promise<{ id: string; simulated: boolean }> {
  const apiKey = process.env.RESEND_API_KEY;
  const from = process.env.REPORT_FROM_EMAIL;
  const to = process.env.CEO_EMAIL;
  if (!apiKey || !from || !to) {
    // Demo mode: don't break the flow — report a simulated (non-sent) success,
    // clearly flagged so the UI can label it. Real sending requires the env vars.
    if (process.env.DEMO_SEED === "1") {
      return { id: "demo-not-sent", simulated: true };
    }
    throw new Error(
      "Email not configured: set RESEND_API_KEY, REPORT_FROM_EMAIL, CEO_EMAIL",
    );
  }
  const resend = new Resend(apiKey);
  const { data, error } = await resend.emails.send({
    from,
    to,
    subject: draft.subject,
    html: draft.html,
  });
  if (error) throw new Error(`Resend error: ${error.message}`);
  return { id: data?.id ?? "sent", simulated: false };
}
