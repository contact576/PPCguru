# SEO Automation Tool — Concept & Execution Plan

Internal agency tool for running end-to-end SEO programs for clients across the
USA, Canada, UK, Australia, and Europe — covering both classic search engine
ranking (Google/Bing) and visibility in LLM answers (ChatGPT, Claude, Gemini).

Pilot client: **Therapy Villa** — therapy practice, Canada, target market Toronto.

---

## 1. What the tool is (and is not)

**It is:** a config-driven pipeline. Each client gets a profile (business,
vertical, country, city, services, site URL, competitors). Modules run against
that profile on a schedule and produce actionable outputs: prioritized fix
lists, content briefs/drafts, keyword maps, and tracking reports.

**It is not:** a magic "rank on ChatGPT" button. No tool can directly place a
business in LLM answers. LLMs cite businesses that have strong entity signals,
authoritative mentions, structured/quotable content, and good classic SEO —
the tool's job is to *systematize* those fundamentals and *measure* AI
visibility so we know what's working.

---

## 2. Module map

### M1. Client profile (the contract every module reads)
YAML/JSON per client: business name, vertical, site URL, country + target
locations, services, competitors, languages/locale (en-CA vs en-US vs en-GB),
brand voice notes, GSC/GBP/GA4 credentials.

### M2. Keyword research (geo-aware)
- Seed expansion from services + locations (service x location matrix:
  "couples therapy Toronto", "anxiety therapist near me").
- Volume/difficulty/CPC from DataForSEO Keyword Data API with country +
  city-level location codes.
- Competitor keyword gap (keywords competitors rank for, client doesn't).
- Intent classification (informational / commercial / transactional / local)
  and clustering into topic clusters via Claude API.
- Output: keyword map — every cluster assigned to an existing URL or flagged
  as a new-page opportunity.

### M3. SERP & competitor analysis (per target country/city)
- Geo-located SERP snapshots (DataForSEO SERP API, e.g. location=Toronto,
  language=en, google.ca).
- For each priority keyword: top-10 analysis — content type, word count,
  heading structure, schema in use, People Also Ask, local pack presence,
  AI Overview presence and who it cites.
- Output per keyword: "what it takes to win" brief input.

### M4. Technical SEO audit ← **first build**
Crawler + API checks producing a scored, prioritized fix list:
- Indexability: robots.txt, meta robots, canonicals, sitemap coverage,
  status codes, redirect chains, orphan pages, crawl depth.
- Performance: Core Web Vitals via PageSpeed Insights API (free), mobile.
- International: hreflang correctness for multi-country clients.
- Structured data: validation + missing-schema opportunities
  (LocalBusiness / MedicalBusiness, FAQPage, Service, Person for clinicians).
- AI-crawler readiness: GPTBot/ClaudeBot/Google-Extended access in robots.txt,
  llms.txt, server-side rendered content (LLM crawlers execute little JS).

### M5. On-page audit & optimization ← **first build**
Per-page scoring against the keyword map:
- Title/meta/H1 vs target cluster; heading hierarchy; content depth vs the
  current top-10 (from M3); image alts; internal link suggestions.
- E-E-A-T checks (critical for YMYL verticals like therapy): author
  credentials, reviewed-by blocks, citations to authoritative sources,
  about/contact/policy pages.
- Output: per-page fix list with ready-to-paste replacements (new title tag,
  new meta description, schema JSON-LD blocks), ranked by impact x effort.

### M6. Content engine
- Briefs generated from M2 clusters + M3 SERP analysis: entities to cover,
  heading outline, PAA-derived FAQ, target length, internal links, schema.
- Drafts via Claude API with locale enforcement (en-CA spelling, local
  references, local stats) and E-E-A-T scaffolding (author bio, citations).
- Human review gate before anything publishes. Never auto-publish YMYL content.

### M7. AEO/GEO — LLM visibility (the differentiator)
Two halves:
1. **Measure:** a fixed prompt panel per client (~20-30 buyer-intent prompts:
   "best therapist in Toronto", "affordable couples counselling Toronto",
   "online therapy covered by insurance Canada") run weekly against the
   ChatGPT, Claude, and Gemini APIs (web search enabled where available).
   Log: is the client mentioned? cited? which sources does the answer pull
   from? Track share-of-voice vs competitors over time.
2. **Act:** the sources LLM answers cite for a niche become the target list —
   directories (Psychology Today for therapy), review platforms, local press,
   Reddit/Quora threads, "best X in Y" listicles. The tool surfaces *where to
   earn mentions*; outreach stays human.

### M8. Rank tracking & reporting
- Geo-located rank checks via DataForSEO (city-level, per device).
- GSC API for real impressions/clicks/queries.
- AI mention trend from M7.
- Weekly per-client report: movements, completed fixes, content shipped,
  AI share-of-voice. Markdown/HTML first; dashboard later if needed.

---

## 3. Architecture

- **Backend:** Python (FastAPI later; plain CLI pipeline first), Postgres,
  job scheduler (cron → Celery/RQ when needed).
- **Crawler:** httpx + selectolax for speed, Playwright fallback for
  JS-rendered pages.
- **External APIs:** DataForSEO (SERP, keywords, rank — ~$50-100/mo at this
  scale), PageSpeed Insights (free), Google Search Console API (free),
  Google Business Profile API (free), Claude API (analysis + generation),
  OpenAI + Gemini APIs (prompt panel only).
- **Outputs:** versioned markdown/HTML reports per client per run, stored in
  Postgres + flat files. No UI until the engine proves out.
- **Multi-country:** locale is a first-class field on every request —
  search engine domain (google.ca/.co.uk/.com.au), location code, language,
  spelling variant — never an afterthought.

## 4. Execution roadmap

| Phase | Scope | Duration |
|-------|-------|----------|
| 0 | Manual validation: run the full methodology by hand for Therapy Villa (keyword map, audit, prompt panel) to lock the report formats before automating | ~1 week |
| 1 | M1 + M4 + M5: client config, crawler, technical + on-page audit engine with prioritized fix-list output | 2-3 weeks |
| 2 | M2 + M3: DataForSEO integration, keyword map, SERP analysis (feeds better targets into M5) | 2 weeks |
| 3 | M7 measurement + M8: prompt panel, rank tracking, weekly report | 2 weeks |
| 4 | M6: content briefs + drafts with review workflow | 2 weeks |
| 5 | Second/third client onboarded purely via config — the real test | ongoing |

## 5. Expert caveats (so we don't overpromise to clients)

- **Therapy = YMYL.** Google holds health-adjacent content to higher E-E-A-T
  standards. Credentialed authors and clinical review notes are not optional.
- **Local SEO is half the battle for Therapy Villa.** Google Business Profile
  optimization, reviews velocity, and citation consistency (NAP) often move
  the local pack more than on-site changes. The tool audits these; some
  execution (review generation, outreach) stays human.
- **LLM visibility lags.** Models retrain and search indexes refresh on their
  own schedules; expect 2-6 months before AI mention metrics move. Set client
  expectations accordingly.
- **Don't scrape Google directly.** DataForSEO/serp APIs exist precisely
  because direct scraping is fragile and ToS-hostile.
- **Never auto-publish.** Drafts always pass a human gate, especially YMYL.

## 6. Open questions

- Does the tool live in this repo or a new `seo-engine` repo? (This repo is
  the PPC Guru site; recommend a separate repo once we start Phase 1.)
- Which Therapy Villa competitors to seed the gap analysis with?
- Access available? GSC, GBP, GA4 for Therapy Villa.
