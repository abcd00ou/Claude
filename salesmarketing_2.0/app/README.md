# CEO Daily Brief — Human-in-the-Loop Web App

Next.js app (Vercel) for the 9am leader-review flow. Each morning a cron generates 3 team
drafts; the 3 leaders review them in 3 tabs and either **approve & send to the CEO** or
**regenerate / request a data update**.

```
  09:00 KST  ─ Vercel Cron ─▶ /api/cron ─▶ generate 3 drafts (Claude + web search) ─▶ store
                                                                                       │
   leader opens app ─▶ 3 tabs (Sales · Marketing · Product Planning)                   │
        ├─ Approve & send to CEO ─▶ /api/approve ─▶ Resend ─▶ abcd00ou@gmail.com        │
        ├─ Regenerate (+ feedback) ─▶ /api/generate                                     │
        └─ Request data update      ─▶ /api/generate (fresh web search)  ◀──────────────┘
```

## What each draft contains

A C-level HTML email body: `[REAL]` web-sourced signals (cited) + `[SIM]` simulated internal
SK hynix stand-ins (clearly labeled). The trust rule holds: a simulated number can never read
as real, and the gap section lists what needs human confirmation.

## Prerequisites (you provide)

- **Anthropic API key** — generation + web search (`ANTHROPIC_API_KEY`). Model defaults to
  `claude-opus-4-8`; set `ANTHROPIC_MODEL=claude-sonnet-4-6` to cut cost.
- **Resend** — `RESEND_API_KEY` + a verified `REPORT_FROM_EMAIL`, and `CEO_EMAIL` (the recipient).
- **Vercel account** — to deploy.
- **Vercel KV** (recommended) — so drafts survive between the 9am cron and review. Without it,
  drafts live in memory and won't persist across serverless invocations.

## Local dev

```bash
cd salesmarketing_2.0/app
npm install
npm install @anthropic-ai/sdk@latest   # ensure the current API surface (adaptive thinking, web_search_20260209)
cp .env.example .env.local              # fill in keys
npm run dev                             # http://localhost:3000
```

Generate a draft from the UI (the "Generate" button) — no cron needed locally.

## Deploy to Vercel

1. Push this repo; in Vercel, **import the project with root directory `salesmarketing_2.0/app`**.
2. Add env vars (Settings → Environment Variables): `ANTHROPIC_API_KEY`, `RESEND_API_KEY`,
   `REPORT_FROM_EMAIL`, `CEO_EMAIL`, `CRON_SECRET`. Add the **Vercel KV** integration (sets
   `KV_REST_API_URL` / `KV_REST_API_TOKEN`).
3. `vercel.json` registers the daily cron at `0 0 * * *` (**00:00 UTC = 09:00 KST**). Vercel
   Cron runs in UTC and attaches `CRON_SECRET` automatically.
4. Deploy.

## Honest limitations

- **Plan limits:** generation does web search + Opus, which can exceed **Hobby's 60s function
  cap** — use Vercel **Pro** (`maxDuration` is set to 300s). Hobby Cron also runs once/day max,
  which fits the 9am job.
- **Email deliverability:** Resend needs a verified sender domain or the mail may land in spam.
- **Simulated internal data:** `[SIM]` signals are illustrative, not real SK hynix data. The app
  is honest about this; do not treat `[SIM]` numbers as fact in a real decision.
- **Cost:** 3 Opus + web-search generations/day, plus any regenerations. Switch `ANTHROPIC_MODEL`
  to Sonnet to reduce it.

## Files

```
app/
├── vercel.json                 cron schedule (9am KST)
├── lib/
│   ├── teams.ts                3 team configs (focus + signal categories)
│   ├── anthropic.ts            generate(team, feedback?) — Claude + web search, pause_turn loop
│   ├── email.ts                sendToCeo() — Resend
│   ├── store.ts                Vercel KV (or in-memory fallback)
│   └── types.ts
└── app/
    ├── page.tsx                3-tab review UI (approve / regenerate / request update)
    └── api/{cron,generate,approve,drafts}/route.ts
```
