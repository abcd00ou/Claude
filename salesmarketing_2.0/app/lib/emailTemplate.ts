import { BRAND } from "./brand";
import type { EmailBlock, ReportContent } from "./types";
import type { TeamConfig as TC } from "./teams";

// Render a natural, SK hynix-branded executive email from ordered content blocks.
// Reads like a morning note: prose commentary, a table where numbers belong, and a
// simple CSS bar chart (email-safe — no images/JS, renders in Gmail/Outlook).

function esc(s: string): string {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function currentQuarter(d = new Date()): string {
  return `${d.getUTCFullYear()}Q${Math.floor(d.getUTCMonth() / 3) + 1}`;
}

function renderText(text: string): string {
  return `<p style="margin:0 0 13px;font-size:14px;line-height:1.62;color:${BRAND.ink}">${esc(text)}</p>`;
}

function renderTable(b: Extract<EmailBlock, { type: "table" }>): string {
  const head = b.columns
    .map(
      (c, i) =>
        `<th style="text-align:${i === 0 ? "left" : "right"};font-size:11px;letter-spacing:.03em;text-transform:uppercase;color:#fff;background:${BRAND.red};padding:7px 10px;font-weight:700">${esc(c)}</th>`,
    )
    .join("");
  const body = b.rows
    .map(
      (r, ri) =>
        `<tr style="background:${ri % 2 ? "#faf7f6" : "#fff"}">${r
          .map(
            (cell, ci) =>
              `<td style="text-align:${ci === 0 ? "left" : "right"};font-size:13px;color:${BRAND.ink};padding:7px 10px;border-bottom:1px solid ${BRAND.line}">${esc(cell)}</td>`,
          )
          .join("")}</tr>`,
    )
    .join("");
  return `<div style="margin:6px 0 16px">
    ${b.title ? `<div style="font-size:12px;font-weight:700;color:${BRAND.ink};margin:0 0 6px">${esc(b.title)}</div>` : ""}
    <table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="border-collapse:collapse;border:1px solid ${BRAND.line};border-radius:8px;overflow:hidden">
      <thead><tr>${head}</tr></thead><tbody>${body}</tbody>
    </table>
  </div>`;
}

function renderChart(b: Extract<EmailBlock, { type: "chart" }>): string {
  const max = Math.max(...b.bars.map((x) => Math.abs(x.value)), 1);
  const rows = b.bars
    .map((bar) => {
      const w = Math.max(2, Math.round((Math.abs(bar.value) / max) * 100));
      const color = bar.tag === "SIM" ? BRAND.orange : BRAND.red;
      const val = b.unit ? `${bar.value}${b.unit.startsWith("%") ? "%" : " " + b.unit}` : String(bar.value);
      return `<tr>
        <td style="font-size:12px;color:#374151;padding:4px 10px 4px 0;white-space:nowrap;width:34%">${esc(bar.label)}</td>
        <td style="padding:4px 0;width:66%">
          <table cellpadding="0" cellspacing="0" role="presentation" style="width:100%"><tr>
            <td style="width:${w}%"><div style="background:${color};height:13px;border-radius:3px">&nbsp;</div></td>
            <td style="padding-left:8px;font-size:11px;color:${BRAND.muted};white-space:nowrap">${esc(val)}</td>
          </tr></table>
        </td>
      </tr>`;
    })
    .join("");
  return `<div style="margin:8px 0 16px;background:#fafbfc;border:1px solid ${BRAND.line};border-radius:8px;padding:12px 14px">
    ${b.title ? `<div style="font-size:12px;font-weight:700;color:${BRAND.ink};margin:0 0 8px">${esc(b.title)}${b.unit ? ` <span style="color:${BRAND.muted};font-weight:400">(${esc(b.unit)})</span>` : ""}</div>` : ""}
    <table width="100%" cellpadding="0" cellspacing="0" role="presentation">${rows}</table>
  </div>`;
}

function renderBlock(b: EmailBlock): string {
  if (b.type === "text") return renderText(b.text);
  if (b.type === "table") return renderTable(b);
  if (b.type === "chart") return renderChart(b);
  return "";
}

export function renderEmailHtml(team: TC, content: ReportContent): string {
  const q = currentQuarter();
  const date = new Date().toLocaleDateString("ko-KR", { year: "numeric", month: "long", day: "numeric" });
  const body = content.emailBlocks.map(renderBlock).join("\n");

  return `<div style="background:${BRAND.bg};padding:24px 0;font-family:Georgia,'Times New Roman',serif">
  <table align="center" width="660" cellpadding="0" cellspacing="0" role="presentation" style="max-width:660px;margin:0 auto;background:${BRAND.card};border:1px solid ${BRAND.line};border-radius:10px;overflow:hidden">
    <tr><td style="background:${BRAND.red};padding:13px 30px">
      <table width="100%" role="presentation"><tr>
        <td style="font-family:Arial,sans-serif;font-size:19px;font-weight:800;color:#fff;letter-spacing:-.02em">SK<span style="color:#ffd9c2"> hynix</span></td>
        <td align="right" style="font-family:Arial,sans-serif;font-size:10px;color:#ffd9c2;letter-spacing:.1em">대외비</td>
      </tr></table>
    </td></tr>
    <tr><td style="padding:24px 30px 18px">
      <div style="font-family:Arial,sans-serif;font-size:12px;color:${BRAND.muted};margin:0 0 16px">${date} · ${q} · ${esc(team.label)}팀</div>
      ${body}
      <div style="border-top:1px solid ${BRAND.line};margin-top:18px;padding-top:12px;font-family:Arial,sans-serif;font-size:11px;color:${BRAND.muted};line-height:1.6">
        공개 출처가 표기된 수치는 확인된 값이며, “내부 추정” 표기 수치는 확인 전 당분기 작업 추정치입니다. SK hynix — 내부 대외비.
      </div>
    </td></tr>
  </table>
</div>`;
}
