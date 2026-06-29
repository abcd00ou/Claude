import Anthropic from "@anthropic-ai/sdk";
import type { TeamConfig } from "./teams";
import type { EmailBlock, ReportContent, TaskUpdate } from "./types";
import { renderEmailHtml } from "./emailTemplate";

const MODEL = process.env.ANTHROPIC_MODEL || "claude-opus-4-8";

export interface GenerateOpts {
  feedback?: string;
  requestDataUpdate?: boolean;
}

function currentQuarter(d = new Date()): string {
  return `${d.getUTCFullYear()}Q${Math.floor(d.getUTCMonth() / 3) + 1}`;
}

function buildPrompt(team: TeamConfig, opts: GenerateOpts): string {
  const quarter = currentQuarter();
  const cats = team.categories.map((c) => `"${c}"`).join(", ");
  let preamble = "";
  if (opts.feedback) preamble += `\nThe leader was NOT satisfied with the previous draft. Feedback: "${opts.feedback}". Address it.\n`;
  if (opts.requestDataUpdate) preamble += `\nThe leader requested fresh data — search again for the very latest.\n`;

  return `You are the ${team.label} team leader at SK hynix (memory: DRAM/HBM/LPDDR/NAND), writing this morning's note to the CEO. Focus: ${team.focus}.

WRITE ALL CONTENT IN KOREAN (한국어) — every commentary paragraph, headline, detail, table title, column header, row text, and chart title must be Korean. Keep company names (NVIDIA, Samsung, Micron), product names (HBM3E-12hi, DDR5-6400), source names (TrendForce, Bloomberg, JEDEC), numbers, and units in their original form. The JSON keys and the tag values "REAL"/"SIM" stay in English.
${preamble}
Gather signals:
1. Web-search for REAL current public facts (earnings, filings, analyst notes, press, JEDEC, pricing indices). Each REAL fact has a source (publisher + month).
2. For SK hynix INTERNAL signals that are not public (yield, allocation quantities, CRM specifics, internal commitments), produce brief plausible ${quarter} estimates — these are simulated.

Return ONLY a JSON object (no prose, no markdown fences):
{
  "task_updates": [
    { "category": <one of [${cats}]>, "tag": "REAL"|"SIM", "headline": "one line", "detail": "supporting detail", "source": "publisher + month for REAL, else empty" }
  ],
  "email_blocks": [ ... ]
}

"task_updates" is the leader's raw categorized scan (5-9 items).

"email_blocks" is the ACTUAL EMAIL to the CEO — write it like a real person, not a template. Rules:
- It must READ like a natural morning email, not an AI report. NO "Executive Summary"/"Key Signals" headers, NO bullet-point dumps, NO status chips.
- Open with a short, human one-liner to the CEO and 1-2 sentences of context.
- Carry the story mostly in COMMENTARY: 3-4 short paragraphs of plain prose, in your own voice, explaining what's happening and what it means.
- Put NUMBERS in a table where a table genuinely helps (pricing, allocation, share, roadmap) — 1 or 2 tables max.
- Include exactly ONE simple bar chart for the single most important trend.
- Close with a brief "what I'm watching / what I'd ask of you" paragraph.
- Cite REAL facts inline in the prose/table ("(TrendForce, Mar)"). Mark simulated internal figures inline as "(internal est.)". Do not over-label.

email_blocks is an ordered array; each block is one of:
{ "type": "text", "text": "a paragraph of commentary" }
{ "type": "table", "title": "short title", "columns": ["Col A","Col B"], "rows": [["x","y"]] }
{ "type": "chart", "title": "short title", "unit": "% QoQ", "bars": [ { "label": "DDR5", "value": 45, "tag": "REAL" } ] }
Typical order: text (greeting+context) → text → table → text → chart → text (closing). Keep it tight — a CEO reads it in under a minute.`;
}

function asBlocks(raw: unknown): EmailBlock[] {
  if (!Array.isArray(raw)) return [];
  const out: EmailBlock[] = [];
  for (const b of raw as Record<string, unknown>[]) {
    if (b?.type === "text" && typeof b.text === "string") {
      out.push({ type: "text", text: b.text });
    } else if (b?.type === "table" && Array.isArray(b.columns) && Array.isArray(b.rows)) {
      out.push({
        type: "table",
        title: typeof b.title === "string" ? b.title : undefined,
        columns: (b.columns as unknown[]).map(String),
        rows: (b.rows as unknown[]).map((r) => (Array.isArray(r) ? r.map(String) : [String(r)])),
      });
    } else if (b?.type === "chart" && Array.isArray(b.bars)) {
      out.push({
        type: "chart",
        title: typeof b.title === "string" ? b.title : undefined,
        unit: typeof b.unit === "string" ? b.unit : undefined,
        bars: (b.bars as Record<string, unknown>[]).map((x) => ({
          label: String(x.label ?? ""),
          value: Number(x.value ?? 0),
          tag: x.tag === "SIM" ? "SIM" : x.tag === "REAL" ? "REAL" : undefined,
        })),
      });
    }
  }
  return out;
}

function parseContent(raw: string, categories: string[]): ReportContent {
  const start = raw.indexOf("{");
  const end = raw.lastIndexOf("}");
  if (start !== -1 && end > start) {
    try {
      const o = JSON.parse(raw.slice(start, end + 1));
      const taskUpdates: TaskUpdate[] = Array.isArray(o.task_updates)
        ? o.task_updates.map((u: Record<string, unknown>) => ({
            category: String(u.category ?? categories[0]),
            tag: u.tag === "REAL" ? "REAL" : "SIM",
            headline: String(u.headline ?? ""),
            detail: String(u.detail ?? ""),
            source: String(u.source ?? ""),
          }))
        : [];
      const emailBlocks = asBlocks(o.email_blocks);
      if (emailBlocks.length > 0 || taskUpdates.length > 0) return { taskUpdates, emailBlocks };
    } catch {
      /* fall through */
    }
  }
  return { taskUpdates: [], emailBlocks: [{ type: "text", text: raw.trim().slice(0, 1500) }] };
}

export async function generateDraft(
  team: TeamConfig,
  opts: GenerateOpts = {},
): Promise<{ subject: string; html: string; content: ReportContent }> {
  const client = new Anthropic();
  const messages: Anthropic.MessageParam[] = [{ role: "user", content: buildPrompt(team, opts) }];

  let final: Anthropic.Message | null = null;
  for (let i = 0; i < 6; i++) {
    const res = await client.messages.create({
      model: MODEL,
      max_tokens: 8000,
      thinking: { type: "adaptive" },
      output_config: { effort: "high" },
      tools: [{ type: "web_search_20260209", name: "web_search" }],
      messages,
    });
    if (res.stop_reason === "pause_turn") {
      messages.push({ role: "assistant", content: res.content });
      continue;
    }
    final = res;
    break;
  }
  if (!final) throw new Error("Generation did not converge (pause_turn loop)");

  const text = final.content
    .filter((b): b is Anthropic.TextBlock => b.type === "text")
    .map((b) => b.text)
    .join("\n");
  if (!text.trim()) throw new Error("Model returned no text content");

  const content = parseContent(text, team.categories);
  return {
    subject: `[${team.subjectPrefix}] — CEO 데일리 브리핑 ${currentQuarter()}`,
    html: renderEmailHtml(team, content),
    content,
  };
}
