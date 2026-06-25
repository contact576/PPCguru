# GCAD Construction — Ads Performance Dashboard

A one-screen, always-on dashboard for a single PPC Guru client (**GCAD Construction**),
unifying **Google Ads** and **Meta Ads** into one view. Built to scale to more clients later.

Headline KPI: **total lead volume** across both platforms (Meta Messenger conversations +
Google calls/conversions), with blended cost-per-lead, daily trend, campaign tables, and an
auto-generated **actionable insights** panel.

## How the data flows

```
 Adzviser MCP (Google Ads) ─┐
 Adzviser MCP (Meta Ads)   ─┼─► daily pull (Claude/agent) ─► Google Sheet (data store) ─► this Next.js app ─► Vercel
 Meta Ads MCP              ─┘
```

- **Data store:** a Google Sheet — one row per day per client.
  Current store: `GCAD Construction — Ads Daily Snapshots` (see `data/snapshots.json → sheet.url`).
- **Daily refresh:** a scheduled job pulls yesterday's numbers from Adzviser and appends a
  row to the Sheet. (Runs from the agent environment via MCP; to make it fully serverless,
  swap in direct Adzviser/Google/Meta API keys.)
- **The app** reads the Sheet's published CSV when `SHEET_CSV_URL` is set; otherwise it falls
  back to `data/snapshots.json`, which is **seeded with real GCAD data** so it always renders.

## Run locally

```bash
npm install
npm run dev      # http://localhost:3000
npm run build && npm start
```

## Go fully live (Sheet → dashboard)

1. In the Google Sheet: **File → Share → Publish to web → CSV**.
2. In Vercel: set env var `SHEET_CSV_URL` to that published CSV link.
3. Redeploy. The header pill flips from "Seeded snapshot" to "Live · Google Sheet".

## Data definitions

- **Google leads** = conversion actions + phone calls.
- **Meta leads** = new Messenger conversations (this account runs messaging objectives, not lead forms).
- **Blended cost / lead** = total spend ÷ total leads, across both platforms.

## Adding the next client

Each client = one Adzviser workspace (Google) + one (Meta) + one Sheet tab. The dashboard
shape is identical, so a new client is a config entry, not a rebuild. A client switcher
dropdown is the next planned addition.

## What this is NOT (yet)

- Not wired to a CRM, so "lead → booked job" close rate isn't tracked. That's the natural
  next step once lead quality matters.
- Conversion **value** isn't set in the Google account, so ROAS can't be computed until that's
  fixed in Google Ads (flagged in the dashboard's insights panel).
