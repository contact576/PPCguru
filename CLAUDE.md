# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A single-screen, always-on **ads performance dashboard** (Next.js 14 App Router, plain JavaScript)
that unifies **Google Ads + Meta Ads** into one view for a PPC Guru client. It currently ships for
**GCAD Construction** but is intentionally built to be multi-client: a new client is a new data
config + Google Sheet tab, not a rebuild (a client-switcher dropdown is the planned next step).
The headline metric everywhere is **lead volume**, with blended cost-per-lead as the efficiency KPI.

Deployed on **Vercel** (project `gcad-ads-dashboard`).

## Commands

```bash
npm install
npm run dev      # dev server → http://localhost:3000
npm run build    # production build
npm start        # serve the production build
npm run lint     # next lint
```

There is **no test setup** in this repo (no test script, no test deps) — don't invent one; add a
framework deliberately if tests are needed.

## Architecture — the parts that matter

The whole UI is driven by **one data object** with a fixed shape. Understanding that object and how
it's assembled is 90% of understanding the app.

- **`data/snapshots.json` is the canonical data contract and the always-render seed.** It is
  committed with real client data so the dashboard renders even with no live source. Its top-level
  shape — `client, currency, lastUpdated, periods{current,prior}, summary{combined,google,meta},
  daily[], campaigns{google[],meta[]}, insights[]` — is what every component in `app/page.js`
  reads. Change this shape and you must update the consumers in `app/page.js` too.

- **`lib/data.js › getDashboardData()` is the single data entry point, and its merge behavior is
  non-obvious:** if `SHEET_CSV_URL` is set it fetches the published Google-Sheet CSV (ISR
  `revalidate: 1800`), but it **only refreshes the `daily` trend from the Sheet** — `summary`,
  `campaigns`, and `insights` **always come from the committed seed**. With no env var (or on fetch
  error) it returns the seed as-is (adding `sheetError` on failure). So editing numbers in
  `snapshots.json` is how you change everything except the live daily chart.

- **CSV ↔ app field mapping lives in `mapSheetRow` (lib/data.js).** The Sheet uses snake_case
  columns (`google_spend`, `meta_messaging_leads`, …); the app uses camelCase daily fields
  (`googleSpend`, `metaLeads`, …). If you change the `daily` shape, update **all three**:
  `mapSheetRow` (column names), the `daily` seed rows, and the consumers (`TrendChart`, `page.js`).

- **`app/page.js` is one async React Server Component** (`export const dynamic = "force-dynamic"`)
  rendering the entire page: KPI cards, trend chart, per-platform breakdown, Google + Meta campaign
  tables, and the auto-insights panel. There is no client-side state or routing.

- **Zero UI/chart dependencies by design.** The only runtime deps are `next`, `react`, `react-dom`.
  Styling is hand-written CSS in `app/globals.css` (no Tailwind, no CSS-in-JS). The trend chart
  (`components/TrendChart.js`) is a **dependency-free hand-rolled SVG** (lead bars + spend line).
  Prefer this house style — reach for a library only with a clear reason.

- **No TypeScript.** Plain JS with the `@/*` path alias → repo root (`jsconfig.json`).

## Domain semantics (baked into the code — get these right)

"Leads" is a **blended, cross-platform** definition, not a single ad-platform metric:
- **Google leads = conversions + phone calls.**
- **Meta leads = new Messenger conversations** (this account runs messaging objectives, not lead forms).
- **Blended cost / lead = total spend ÷ total leads** across both platforms.

Metric direction matters in the UI: the `Delta` component in `page.js` takes `goodIsUp` — **cost
metrics are good when they go down** (`goodIsUp={false}`), volume metrics good when up. Keep that
correct when adding KPIs.

## Data pipeline (context, not in this repo)

The daily refresh is **not** a serverless cron here: an agent/Claude job pulls yesterday's numbers
via MCP (Adzviser for Google + Meta; Meta Ads MCP) and appends one row per day to the client's
Google Sheet. To go fully live, publish that Sheet to web as CSV and set `SHEET_CSV_URL` in Vercel —
the header pill flips "Seeded snapshot" → "Live · Google Sheet". See `README.md` for the step-by-step
and the current known gaps (no CRM close-rate; no Google conversion value, so ROAS is unavailable).

## Don't-trip-on-these

- **`index.html`** at the repo root is a stray static "Welcome to PPC Guru" placeholder — it is **not**
  the app entry point (Next serves from `app/`). Don't wire features into it.
- **`Ecocare_Meta_Ads_Audit/`** is generated client-audit output (Markdown / DOCX / CSV / HTML
  deliverables), **not application code** — don't treat it as part of the dashboard.
