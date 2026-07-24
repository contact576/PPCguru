# Meta Ads Performance Comparison and GCAD Cost‑Per‑Lead Improvement Plan
### Project Pioneer vs. GCAD Construction – New

| | |
|---|---|
| **Prepared for** | GCAD Construction |
| **Prepared by** | PPC Guru (Marketing Agency) |
| **Report date** | 24 July 2026 |
| **Currency** | All figures in **CAD** |
| **Benchmark account** | Project Pioneer (internal benchmark only — a related, more mature renovation account) |
| **Subject account** | GCAD Construction – New (Meta ad account `819921644385618`) |

**Reporting periods used in this report**

| View | Project Pioneer | GCAD Construction – New |
|---|---|---|
| Account lifetime available | 25 Feb 2026 → 24 Jul 2026 (≈5 months) | 22 Jun 2026 → 24 Jul 2026 (≈1 month / 33 days) |
| Same‑period head‑to‑head | 25 Jun → 24 Jul 2026 | 22 Jun → 24 Jul 2026 (its whole life) |
| Age‑matched | First 7 / 14 / 30 days from 25 Feb | First ~30 days = its whole life |

> **Data sources:** Project Pioneer was read through the **Adzviser** connector; GCAD‑New was read directly through the **Meta Ads API (MCP)**. Both are Meta's own reported numbers. Project Pioneer is currently not directly queryable through the Meta API (account status *unsettled*), which is why two connectors were used. See **Section 4** for the attribution and comparability caveats this creates.

---

## 1. Executive Summary

This report compares two renovation lead‑generation accounts on Meta. **Project Pioneer** is a more mature account that has been advertising since late February 2026. **GCAD Construction – New** is a **brand‑new ad account, roughly one month old**, created to run a cleaner, geographically‑restricted setup after the previous account attracted out‑of‑area enquiries.

**The headline difference (verified):** In the last ~30 days, Project Pioneer produced **WhatsApp conversations at about CA$55 each**, while GCAD‑New's blended WhatsApp cost was about **CA$74 each** — and over each account's *lifetime*, the gap is wider (Pioneer ≈ **CA$24** per conversation across 280 conversations vs GCAD‑New ≈ **CA$74** across 20). Project Pioneer is producing **more conversations at a lower cost**.

**Most important *verified* causes of the gap**

1. **Maturity and conversion volume.** Project Pioneer has ~5 months of history, **280 messaging conversations**, and a single consolidated campaign. GCAD‑New has ~1 month and **20 conversations spread across 7 ad sets** — too little signal for Meta to optimise efficiently. *(Confirmed by data.)*
2. **Budget concentration vs fragmentation.** Pioneer concentrates spend; GCAD‑New splits a small budget across 7 ad sets (several at $20/day, 1–9 conversations each). *(Confirmed by data.)*
3. **A saturated ad set.** GCAD‑New's largest early ad set ran to **frequency 4.80** (same people seeing the ad ~5×) at **$111 per conversation**. *(Confirmed by data.)*

**Most important *likely* causes (not yet proven)**

- **Audience saturation and seasonality** in the current summer window are depressing results for *both* accounts (Pioneer's own cost per conversation rose from ~$21 to ~$55 as it matured and as summer arrived).
- **Post‑click WhatsApp handling** (response speed, qualification) is not measured yet and may explain part of the quality/cost picture.
- **Lead quality** (in‑area, contactable, qualified) is **not tracked in any system today**, so no cost‑per‑*qualified*‑lead exists for either account yet.

**Actions already taken for GCAD‑New (by the agency)**

- Tightened the service area to **Toronto + specific GTA postal codes** and radius targeting on Toronto / Brampton / Mississauga / Vaughan.
- **Excluded ~69 non‑serviceable Ontario cities** (Ottawa, Hamilton, London, Kingston, Windsor, Barrie, Kitchener/Waterloo, Sudbury, etc.) plus **12–13 custom radius exclusions**, and switched Meta **geographic expansion OFF**.
- Launched a **second lead path — an Instant Form campaign** — with the goal of capturing service‑area and qualification information more reliably than a raw WhatsApp click.

> ⚠️ **The Instant Form campaign is 1 day old with $43.74 spend and 0 completed forms. It must NOT be judged yet.** It has nowhere near enough data to call good or bad.

**Top five recommended actions**

1. **Stand up a lead‑quality tracking sheet** (project postal code, in/out of area, contactable, qualified, appointment, sale) so we can finally measure **cost per qualified in‑area lead** — the metric that actually matters.
2. **Consolidate the 7 ad sets** into far fewer, better‑funded ad sets so Meta gets concentrated conversion signal.
3. **Protect and scale the winning WhatsApp structure** (the "V" concept at ~$45–54/conversation) and **rework or pause the saturated $111 ad set**.
4. **Add a short WhatsApp qualification opener** (city/postal code → project type → budget → timeline → ownership) and log response times.
5. **Let the Instant Form campaign gather 2–3 weeks of data** before comparing it to WhatsApp, and keep the two conversion types reported **separately**.

> **A note on expectations, in plain English:** improvement here comes from **controlled testing and enough data**, not a single switch. We are targeting a **lower cost per qualified in‑area lead over the next 6 weeks** — we are **not** promising GCAD‑New will match Project Pioneer's cost per lead, because the two accounts differ in age, history, and accumulated data.

---

## 2. Business and Campaign Context

Both businesses operate in the **construction / renovation** industry and both use **WhatsApp** as a primary lead destination. Their core objective is renovation lead generation (basements feature heavily in both).

| | Project Pioneer | GCAD Construction – New |
|---|---|---|
| Industry | Renovation / construction | Renovation / construction |
| Primary lead destination | WhatsApp messaging | WhatsApp messaging (+ new Instant Form) |
| Account first delivery | 25 Feb 2026 | 22 Jun 2026 |
| Account age (as of 24 Jul) | ~5 months | ~1 month |
| Lifetime spend (Meta) | CA$6,790.57 | CA$1,521.23 |
| Lifetime messaging conversations | 280 | 20 |
| Lifetime form leads | 14 (secondary) | 0 (form is 1 day old) |
| Service focus in ads | Basements, restaurant/commercial fit‑outs, healthcare clinic fit‑outs | Basement rental/income suites |
| Geographic approach | Multiple Ontario cities + creative self‑qualification ("GTA homeowners only", "across Ontario") | Tight GTA postal codes/radius + heavy exclusions |

**Why the comparison must be handled carefully**

- **Different maturity:** one account has 14× the conversation history of the other.
- **Different conversion actions:** Pioneer's "results" are almost entirely **WhatsApp conversations**; GCAD‑New now runs **both** WhatsApp conversations **and** Instant Form leads. *A WhatsApp conversation and a form submission are not the same action and are not combined into one blended cost per lead in this report.*
- **The geographic issue** on the older/original GCAD setup prompted a deliberate rebuild — GCAD‑**New** is that rebuild. Judging it against a 5‑month account on raw cost alone would be unfair; this report normalises the comparison (Section 5–6) and separates what is proven from what is plausible (Section 10).

---

## 3. Data Scope and Comparison Methodology

**Data available and used**

- Delivery, engagement, and conversion metrics at **account, campaign, ad‑set, and ad** level for both accounts.
- **Campaign objectives, optimisation goals, budgets, delivery status, creation/launch dates.**
- **Geographic targeting** (included cities, postal codes, radius, and exclusion lists) and **audience** settings (interests, behaviours, Advantage audience).
- **Creative** formats, primary text, headlines, and calls‑to‑action; **video** hook/hold metrics for Project Pioneer.
- **Placement** breakdown for Project Pioneer.

**Data NOT available (marked throughout as "Data not provided")**

- **CRM / offline outcomes for both accounts:** contactable leads, in‑area vs out‑of‑area confirmation, qualified renovation opportunities, consultation/estimate appointments, sales opportunities, and closed projects. **Neither account is connected to a CRM today.**
- **WhatsApp conversation content** (response times, qualification answers, spam/duplicate rate).
- **Instant Form question‑level configuration and conditional logic** (not retrievable through the current API; to be confirmed in Ads Manager).
- **Account change history / activity log for GCAD‑New** (the Meta activity‑log tool is not yet enabled for this ad account; launch dates are inferred from campaign/ad‑set creation timestamps instead).
- **Meaningful placement/age/gender splits for GCAD‑New:** with only 20 conversations, splitting them across ~10 placements or several age bands produces 0–3 conversions per cell — **too small to act on** (see Section 11).

**Comparability caveats**

- The two accounts were read through **different connectors** (Adzviser vs Meta API). Both report Meta's numbers, but **default attribution windows may differ slightly**. GCAD‑New's ad sets use **1‑day‑view / 7‑day‑click** attribution. Treat sub‑10% differences as noise, not signal.
- **Are the conversion actions directly comparable?** WhatsApp conversation ↔ WhatsApp conversation: **yes** (Comparison E). WhatsApp conversation ↔ Instant Form: **no** — reported separately.

---

## 4. Attribution, Conversion Definitions, and Comparability

| Item | Project Pioneer | GCAD Construction – New |
|---|---|---|
| Campaign objective | OUTCOME_LEADS | OUTCOME_LEADS (all 3 campaigns) |
| Primary result type | **Messaging conversations started** (WhatsApp) | **Messaging conversations started** (2 campaigns) + **Leads (form)** (1 campaign) |
| Ad‑set optimisation event | Messaging/WhatsApp conversations | **REPLIES** (WhatsApp ad sets) / **LEAD_GENERATION** (Instant Form ad sets) |
| CTA in creative | WHATSAPP_MESSAGE | WHATSAPP_MESSAGE (mostly); one video uses **GET_QUOTE** |
| Attribution setting | Adzviser default (Meta) | 1‑day view / 7‑day click |
| Currency | CAD | CAD |

> **Plain‑English callout — "lead" is not one thing.** Meta labels several different actions as a "result." In this report we keep them separate: a **WhatsApp conversation** (someone opened a chat) is *earlier and softer* than a **completed Instant Form** (someone answered qualifying questions), which is *earlier and softer* than a **qualified in‑area lead** (someone we confirmed is in our service area with a real project). We do **not** blend WhatsApp conversations and form completions into a single cost‑per‑lead.

---

## 5. Account‑Level Performance Scorecard

**Same recent window — WhatsApp / messaging only** (Pioneer 25 Jun–24 Jul; GCAD‑New 22 Jun–24 Jul, messaging campaigns only). This is the fairest apples‑to‑apples view.

| Metric | Project Pioneer | GCAD‑New (WhatsApp) | Difference | Interpretation | Confidence |
|---|---|---|---|---|---|
| Spend | $1,381.01 | $1,477.49 | +7% | Similar spend | High |
| Impressions | 78,075 | 74,977 | −4% | Similar reach of delivery | High |
| Reach | 30,231 | ~22,988 | −24% | GCAD‑New hits fewer unique people (tighter geo) | High |
| Frequency | 2.58 | up to **4.80** (S) | Higher on GCAD‑New | Saturation on one ad set | High |
| CPM | $17.69 | ~$20 | +~13% | Slightly higher — expected with tighter geo | Med |
| Link clicks | 407 | ~731 | +80% | GCAD‑New gets **more clicks** | High |
| CTR (link) | 0.52% | 0.81%–1.23% | Higher on GCAD‑New | **GCAD‑New creative earns attention** | High |
| CPC (link) | $3.39 | ~$1.91–2.14 | **Lower on GCAD‑New** | Cheaper clicks | High |
| **Messaging conversations** | **25** | **20** | −20% | Fewer conversations | High |
| **Cost / conversation** | **$55.24** | **$73.87** | **+34%** | **Core gap in this window** | High |

> **The most important line above:** GCAD‑New gets **more clicks at a lower CPC and a higher CTR**, but **fewer conversations at a higher cost per conversation**. The performance gap **is not at the top of the funnel (creative/clicks) — it opens up at the click‑to‑conversation step.** That points at conversion destination, WhatsApp flow, budget concentration, and optimisation maturity rather than "bad ads." (See Sections 9, 12.)

**Lifetime context** (not apples‑to‑apples — different ages)

| Metric | Project Pioneer (≈5 mo) | GCAD‑New (≈1 mo) |
|---|---|---|
| Spend | $6,790.57 | $1,521.23 |
| Messaging conversations | 280 | 20 |
| Cost / messaging conversation | **$24.25** | **$73.87** (WhatsApp only) |
| Form leads | 14 | 0 (form 1 day old) |

---

## 6. Funnel Comparison

Funnel per account (same recent window). Steps below the conversation line are **Data not provided** because no CRM/WhatsApp‑content tracking exists yet — closing that gap is Recommendation #1.

**Project Pioneer**

| Stage | Value | Step conversion |
|---|---|---|
| Impressions | 78,075 | — |
| Link clicks | 407 | 0.52% |
| WhatsApp conversations | 25 | 6.1% of clicks |
| Contactable leads | Data not provided | — |
| In‑area leads | Data not provided | — |
| Qualified leads | Data not provided | — |
| Appointments | Data not provided | — |
| Closed projects | Data not provided | — |

**GCAD Construction – New** (WhatsApp campaigns)

| Stage | Value | Step conversion |
|---|---|---|
| Impressions | ~74,977 | — |
| Link clicks | ~731 | ~0.98% |
| WhatsApp conversations | 20 | **2.7% of clicks** |
| Contactable leads | Data not provided | — |
| In‑area leads | Data not provided | — |
| Qualified leads | Data not provided | — |
| Appointments | Data not provided | — |
| Closed projects | Data not provided | — |

> **Where GCAD‑New loses the most ground vs Pioneer:** the **click → WhatsApp conversation** step (~2.7% vs ~6.1%). GCAD‑New actually **wins** the impression → click step (higher CTR, cheaper clicks). So more people are clicking, but proportionally fewer are starting a conversation. Likely contributors: the messaging ad sets optimise for **REPLIES** (not conversations) on very thin data, budget is fragmented, and the post‑click WhatsApp experience is unmeasured. **This is the single most important place to focus.**

---

## 7. Campaign‑Structure Comparison

**Project Pioneer** — one consolidated campaign, segmented by service vertical at the ad‑set level.

| Campaign | Objective | Destination | Ad sets | Result (recent 30d) | Cost/result | Status |
|---|---|---|---|---|---|---|
| PPC Guru All Services $2000 | OUTCOME_LEADS | WhatsApp | 3 (Restaurant, Healthcare, Home) @ ~$20/day each | 25 conversations | $55.24 | ACTIVE |

**GCAD Construction – New** — three campaigns, seven ad sets.

| Campaign | Objective | Destination | Opt. goal | Launched | Spend | Result | Cost/result | Status |
|---|---|---|---|---|---|---|---|---|
| Basement ($1500) – S | OUTCOME_LEADS | WhatsApp | REPLIES | 22 Jun | $777.87 | 7 conversations | **$111.12** | ACTIVE |
| Basement ($1500) – V | OUTCOME_LEADS | WhatsApp | REPLIES | 8 Jul | $699.62 | 13 conversations | **$53.82** | ACTIVE |
| Basement – IF ($1000) | OUTCOME_LEADS | **Instant Form** | LEAD_GENERATION | **23 Jul** | $43.74 | 0 forms | n/a (too new) | ACTIVE |

**GCAD‑New ad‑set detail** (note the fragmentation and churn):

| Ad set | Campaign | Opt. | Daily budget | Spend | Conversations | Cost/result | Freq | Notes |
|---|---|---|---|---|---|---|---|---|
| Basement – New | S ($1500) | REPLIES | (ad‑set) | $778.99 | 7 | $111.28 | **4.80** | Toronto + postal codes; 69 city + 12 custom exclusions; **saturated** |
| V3 – Old | V ($1500) | REPLIES | (ad‑set) | $405.86 | 9 | **$45.10** | 1.86 | **Best performer** |
| New | V ($1500) | REPLIES | (ad‑set) | $189.77 | 3 | $63.26 | 1.71 | Radius: Vaughan/Brampton/Mississauga/Toronto |
| V1 (paused) | V ($1500) | REPLIES | (ad‑set) | $108.15 | 1 | $108.15 | 1.41 | Paused |
| Basement – V | IF ($1000) | LEAD_GENERATION | $20 | $20.58 | 0 forms | n/a | 1.82 | 1 day old |
| Basement – S | IF ($1000) | LEAD_GENERATION | $20 | $24.71 | 0 forms | n/a | 1.83 | 1 day old |
| Basement – New July | S ($1500) | REPLIES | (ad‑set) | $0.16 | 0 | n/a | 1.09 | Created 24 Jul |

> **Key structural finding (Confirmed):** Project Pioneer gives Meta **one concentrated pool of conversion data**; GCAD‑New spreads a similar budget across **7 ad sets holding 0–9 conversions each**. Meta's optimisation works best with roughly **~50 conversion events per ad set per week** — every GCAD‑New ad set is far below that, so the system is effectively learning on a handful of data points.

---

## 8. Geographic and Lead‑Quality Analysis

**The original problem.** On the earlier GCAD setup, the client received enquiries from **outside the intended service area**. That is a real, business‑level quality problem (out‑of‑area leads waste sales time even when they're "cheap").

**What the agency has already changed in GCAD‑New (Confirmed in the account):**

- **Included** areas: **Toronto** plus a specific list of **GTA postal codes** (FSAs L4H–L7A, i.e. Brampton/Mississauga/Vaughan corridors), and on some ad sets **radius targeting** (10–11 miles) on Toronto, Brampton, Mississauga, Vaughan.
- **Excluded** areas: **~69 non‑serviceable Ontario cities** (Ottawa, Hamilton, London, Kingston, Windsor, Barrie, Kitchener, Waterloo, Cambridge, Guelph, Niagara Falls, Oshawa, Sudbury, Thunder Bay, and many more) **plus 12–13 custom radius exclusions**.
- **Meta geographic expansion is OFF** (`advantage_audience` geo automation = 0), so Meta will not silently broaden the area.
- **Service area is stated in the ad copy** ("Serving in Toronto, Brampton & Mississauga") and property type is pre‑qualified ("Own a detached or semi?").

> ✅ **Client‑facing message:** the geographic concern has been **actively and thoroughly addressed** — tighter inclusions, a long exclusion list, geo‑expansion disabled, and service‑area language in the creative and (now) an Instant Form path to capture location. These are the right moves.

**Remaining geographic risks (to watch, not alarms):**

1. **`location_types` still include `recent` and `frequently_in`,** not just `home`. This means people *recently* in the GTA (visitors, people passing through) can still be served and may enquire about a project **elsewhere**. Consider testing `home` only for the core ad set.
2. **Meta only reports delivery down to *province*.** GCAD‑New's delivery is **100% Ontario**, but Meta's breakdowns **cannot show city‑level leakage** inside Ontario. So we cannot prove from delivery data whether any conversations are still out‑of‑area.
3. **The four location layers are not the same thing** and none is captured today: *Meta delivery location ≠ the lead's current location ≠ the project property's location ≠ the desired service location.* Someone standing in Toronto can ask for a basement in Barrie.
4. **Inconsistent geo setup across ad sets** (some use postal codes + a 69‑city exclusion list; others use radius + custom exclusions only). Standardising this will make results easier to trust.

> **The fix that actually resolves this:** capture the **project's postal code** at the very start of every WhatsApp chat and inside the Instant Form's conditional logic, then record in/out‑of‑area on the tracking sheet. **That — not more exclusions — is what will let us prove and price in‑area lead quality.**

**How we will measure it:** every lead tagged with project postal code → in‑area / out‑of‑area → cost per **in‑area** conversation reported weekly, per campaign.

---

## 9. Creative and Offer Comparison

**Project Pioneer creative (recent 30 days)** — segmented by vertical, static + video, all WhatsApp CTA.

| Creative | Concept | Format | Hook / offer | CTR | CPC | Conv. | Cost/conv. |
|---|---|---|---|---|---|---|---|
| Restaurant‑2 | Commercial fit‑out, proof | Static | "15+ Years of Proven Execution" | 0.50% | $2.57 | 6 | **$37.7** |
| Home‑1 | Basement, price anchor | Static | "Finished Basement From $47,990 — Turnkey" | 0.62% | $3.84 | 5 | $55.3 |
| Restaurant‑1 | Commercial fit‑out | Static | Proven process / on‑time | 0.61% | $2.29 | 4 | $57.9 |
| Healthcare‑V | Clinic fit‑outs | Video | "Healthcare Clinic Fit‑Outs Across Ontario" (AODA, code‑compliant) | 0.47% | $3.83 | 7 | $64.6 |
| Home‑2 | Basement, price anchor | Static | "Transform Your Basement — Starting at $47,990" | 0.42% | $5.31 | 2 | $69.1 |
| Home‑V | Basement | Video | Turnkey basement, free quote | 0.23% | $23.54 | 1 | $47.1 |

**Project Pioneer's proven creative principles (the transferable part):**

- **Specific price anchor** ("From $47,990 — Turnkey") removes friction and self‑qualifies budget.
- **Proof and credibility** ("15+ Years of Proven Execution", "permits pulled in‑house", "AODA compliant", "Ontario Building Code").
- **Geographic self‑qualification inside the ad** ("GTA homeowners only", "across Ontario") — the ad *pre‑screens* who bothers to message.
- **One crew / no subcontractors / no surprises** — trust and risk‑reversal.
- **Vertical‑specific angles** (restaurant, healthcare, home) with matching decision‑maker audiences.
- **Both static and video**, with video carrying real hold (Healthcare‑V: 717 people watched to 25%, 137 to 100%).

**GCAD Construction – New creative** — actually **strong and on‑strategy already**:

| Creative | Concept | Format | Hook / offer | CTA |
|---|---|---|---|---|
| "Serving in Toronto, Brampton & Mississauga" | Legal rental suite, ROI | Static | "$46,500 fully legal 2‑bedroom suite… pays for itself in ~2 years… Own a detached or semi?" | WhatsApp |
| "Your Basement Can Pay Your Bills 💰" | Rental income | Video | Same $46,500 anchor, GTA rents | WhatsApp |
| "From Empty Space to Income Space" | Legal/fear angle | Video | "Renting illegally can get you fined… we build fully legal suites" | **GET_QUOTE** |
| "{{product.name}}" | — | Static | **Unrendered dynamic placeholder** | — |

> **Fair, important finding:** GCAD‑New's creative is **not the problem.** It already uses a price anchor ($46,500), ROI framing, a legal/trust angle, property‑type qualification ("detached or semi"), and **service‑area language** — the very principles that work for Pioneer. GCAD‑New even earns a **higher CTR at a lower CPC** than Pioneer right now.

**Two creative issues to fix (low effort):**

1. **Mixed CTA/destination:** one video uses **GET_QUOTE** while the rest use **WHATSAPP_MESSAGE**. Keep one clear destination per ad set so Meta optimises cleanly.
2. **`{{product.name}}` placeholder ads** are showing an unrendered token instead of a headline — either fix the dynamic feed or replace with written headlines.

**Do not copy Pioneer's ads verbatim** — adapt the *principles* to GCAD's brand, photography, offer ($46,500 legal suite), and service area.

---

## 10. Why the Results Are Different

Each factor is rated for **Impact** (performance effect), **Evidence** (how sure we are), and **Controllability** (how much we can change it).

### A. Confirmed differences (supported by data)

| Factor | What the data shows | Impact | Evidence | Control |
|---|---|---|---|---|
| Conversion **volume / history** | 280 vs 20 lifetime conversations | High | Strong | Medium |
| **Budget fragmentation** | 7 ad sets, 0–9 conversions each vs 1 concentrated campaign | High | Strong | High |
| **Ad‑set saturation** | $111 ad set at frequency 4.80 | Medium | Strong | High |
| **Optimisation maturity** | Each GCAD‑New ad set far below ~50 conv/wk | High | Strong | Medium |
| **Higher CTR / lower CPC on GCAD‑New** | 0.8–1.2% CTR, ~$2 CPC | (Positive for GCAD) | Strong | — |

### B. Highly probable contributing factors

| Factor | Reasoning | Impact | Evidence | Control |
|---|---|---|---|---|
| **Optimising for REPLIES on thin data** | Messaging ad sets optimise for replies with <10 events each | Medium | Moderate | High |
| **Click→conversation drop‑off** | 2.7% vs 6.1% — softer post‑click step | High | Moderate | High |
| **Seasonality** | Pioneer's own cost rose to ~$55 this summer; GCAD‑New launched into the same summer auction | Medium | Moderate | Low |
| **Mixed CTA/destination & placeholder ads** | Splits optimisation signal | Low‑Med | Moderate | High |

### C. Factors requiring additional data (cannot conclude yet)

| Factor | Why we can't conclude | What we need |
|---|---|---|
| **Lead quality / in‑area rate** | No CRM or postal‑code capture | Tracking sheet + WhatsApp opener |
| **WhatsApp response/qualification** | Conversation content not measured | Response‑time log, qualification answers |
| **Instant Form performance** | 1 day old, $43, 0 forms | 2–3 weeks of spend |
| **Placement/demographic efficiency (GCAD‑New)** | 20 conversations is too few to split | More volume |

### D. Factors unlikely to explain the gap

| Factor | Why it's unlikely to be the main cause |
|---|---|
| **"Bad creative"** | GCAD‑New's CTR is *higher* and CPC *lower* than Pioneer's. |
| **"The account is just new"** | True but insufficient — the **age‑matched** view (Section labelled Comparison B) shows Pioneer's *own first 30 days* were stronger (45 conv @ ~$22). Newness alone is not a complete explanation, and we do **not** attribute the gap to account age by itself. |
| **Geographic targeting being "too broad"** | It's now **tightly restricted** — if anything the risk is over‑restriction raising CPM, not breadth. |

---

## Normalised Comparisons (A–E)

**Comparison A — Same calendar period** (≈22/25 Jun → 24 Jul): Pioneer **25 conv @ $55.24** vs GCAD‑New **20 conv @ $73.87** (WhatsApp only). Gap ≈ **+34%**. *Confidence: high on numbers; medium on cause.*

**Comparison B — Account‑age‑matched** (first 7 / 14 / 30 days):

| Window | Project Pioneer | GCAD‑New |
|---|---|---|
| First 7 days | 17 conv @ **$12.41** | — |
| First 14 days | 25 conv @ **$16.74** | — |
| First 30 days | 45 conv @ **$21.80** | ~20 conv @ ~**$74** (≈ whole life, mixed structure) |

> **Read this carefully:** Pioneer's *own* first month was strong (45 conversations at ~$22). GCAD‑New's first month is weaker (20 at ~$74). **So the gap is not purely "GCAD is new."** *Important caveat:* the two first‑months fell in **different seasons** (Pioneer: late‑Feb→Mar; GCAD‑New: summer) and used different structures, so this is **strong evidence, moderate certainty** — not proof of a single cause.

**Comparison C — Equal spend (~CA$1,500):** GCAD‑New at $1,521 → **20** conversations. Pioneer reached ~$1,500 cumulative around its first ~40–45 days with roughly **60+** conversations. At comparable early spend, **Pioneer produced ~3× the conversation volume** (approximate; seasonality caveat applies).

**Comparison D — Current structure:** covered in Section 7. Pioneer = 1 campaign / 3 ad sets; GCAD‑New = 3 campaigns / 7 ad sets after geo restriction + Instant Form launch.

**Comparison E — Conversion destination:**

| Destination | Project Pioneer | GCAD‑New |
|---|---|---|
| WhatsApp ↔ WhatsApp | $55.24 / conversation | $73.87 / conversation (best ad set $45.10) |
| Instant Form ↔ Instant Form | No dedicated form campaign (14 form leads lifetime, incidental) | $43.74 spend, **0 forms, 1 day old — not comparable yet** |
| Qualified ↔ Qualified | **Data not provided (neither account)** | **Data not provided** |

---

## 11. Placement and Device Analysis

**Project Pioneer placement efficiency (recent 30 days)** — useful directional benchmark:

| Placement | Spend | CTR | Conv. | Cost/conv. |
|---|---|---|---|---|
| Instagram Stories | $142.36 | **1.56%** | 6 | **$23.73** |
| Facebook Reels overlay | $41.81 | 0.53% | 2 | $20.90 |
| Facebook Instream video | $58.41 | 0.28% | 2 | $29.20 |
| Facebook Search | $15.09 | 1.29% | 1 | $15.09 |
| Facebook Feed | $484.38 | 0.56% | 7 | $69.20 |
| Facebook Reels | $179.94 | 0.31% | 3 | $59.98 |
| Instagram Reels | $168.50 | 0.44% | 2 | $84.25 |
| Instagram Feed | $267.29 | 0.41% | 2 | **$133.65** |

> **Directional read (medium confidence — small per‑placement counts):** for Pioneer, **Instagram Stories** and **Facebook Reels overlay** are the most efficient; **Instagram Feed** is the most expensive per conversation. This is a **hypothesis to test on GCAD‑New**, not a rule to copy.

**GCAD Construction – New:** with only **20 conversations**, splitting by placement, device, age, or gender yields **0–3 conversions per cell**. Per the data‑integrity rules, **we will not cut placements or demographics on such small samples.** We will revisit once GCAD‑New has accumulated more conversions.

---

## 12. Auction and Efficiency Diagnostic — Where the Gap Begins

Using the diagnostic framework on GCAD‑New's numbers:

| Symptom | GCAD‑New reading | Diagnosis |
|---|---|---|
| CPM | ~$20 (normal), Pioneer $17.69 | **Not the problem.** Slightly higher, expected with tighter geo. |
| CTR | 0.8%–1.2% (good, > Pioneer) | **Not the problem** — creative earns clicks. |
| CPC | ~$1.91–2.14 (low, < Pioneer) | **Not the problem** — clicks are cheap. |
| Click → conversation | **2.7% (vs Pioneer 6.1%)** | **This is where the gap begins.** |
| Cost per conversation | $73.87 blended (best $45.10) | Symptom of the drop‑off + fragmentation + saturation. |
| Cost per **qualified** in‑area lead | **Data not provided** | Cannot yet judge true efficiency. |

> **Conclusion:** GCAD‑New has a **good top of funnel and a soft middle.** The evidence points to **conversion destination, WhatsApp flow, optimisation concentration, and (one ad set) frequency** — *not* creative, CPM, or clicks. That is a **good** place to be, because those middle‑funnel levers are highly controllable.

**Low lead volume across many ad sets** = classic **budget fragmentation / insufficient conversion concentration** → addressed by consolidation (Section 13).

---

## 13. GCAD Cost‑Per‑Lead Reduction Plan (Phased)

### Phase 1 — Measurement & Stabilisation (Days 1–7)
- Confirm equivalent **conversion definitions** and keep WhatsApp vs Instant Form **reported separately**.
- Audit each campaign's **objective, optimisation event, attribution** (messaging = REPLIES; consider testing a conversations‑optimised messaging goal once volume allows).
- **Verify geographic inclusions/exclusions** and standardise them across ad sets; test `home`‑only location type on the core ad set.
- **Validate the Instant Form's conditional logic** (service area, renovation type, ownership, timeline, budget) in Ads Manager.
- **Implement the lead‑quality tracking sheet** (record project postal code; tag in/out‑of‑area; separate WhatsApp vs form).
- **Avoid unnecessary major edits** — let the current winners keep learning; **consolidate the fragmented ad sets** (below).

### Phase 2 — Controlled Testing (Days 8–21)
- Launch **adapted** versions of Pioneer's winning principles (price anchor, proof, geo self‑qualification) — **not copies**.
- Test creative concepts one variable at a time: **before/after transformation**, **completed‑project proof**, **trust/credibility**, **offer‑led** ($46,500 legal suite).
- Run **WhatsApp vs Instant Form as separate campaigns** and compare only like‑for‑like.
- Keep a clear **control** (V concept @ ~$45–54) and **challengers**; change **one major variable at a time**.

### Phase 3 — Optimisation & Scaling (Days 22–45)
- Shift budget toward the **lowest cost‑per‑qualified‑lead** campaigns (once the sheet has data), not the lowest raw CPL.
- **Pause consistently weak creatives/ad sets only after sufficient data.**
- Expand winning concepts; build **retargeting** only if audience size supports it (Section labelled "Recommended Architecture").
- Where technically possible, **feed qualified‑lead outcomes back to Meta** (offline conversions / lead‑quality signals).
- Scale **gradually** (≤20–30% budget steps) and keep tracking **cost per qualified in‑area lead**, not just Meta CPL.

> **We will not simply "increase the budget."** More budget on a fragmented, unmeasured funnel buys more of the same. Consolidation + measurement first; then scale what proves out.

---

## 14. Recommended Campaign Architecture

Given the current ~$50–75/day spend level, **fewer, better‑funded ad sets** will beat many thin ones.

**Campaign 1 — GCAD WhatsApp Lead Acquisition**
- Objective: Leads · Destination: WhatsApp/messaging · Goal: messaging conversations (test replies vs conversations).
- **One consolidated GTA service‑area ad set** (merge the current 4–5 WhatsApp ad sets), standardised geo (postal codes **or** radius, plus the exclusion list — pick one method).
- **3–5 ads** using clearly different concepts (income/ROI, before‑after, trust/proof).

**Campaign 2 — GCAD Instant Form Lead Qualification**
- Objective: Leads · Destination: Instant Form · Higher‑intent form with **conditional service‑area qualification**.
- **One consolidated ad set**, 3–5 creative variations.
- Let it run **2–3 weeks** before comparing to WhatsApp.

**Campaign 3 — Retargeting (only when audience is large enough)**
- Candidate pools: Instagram/Facebook engagers, video viewers, **form openers who didn't submit**, website visitors (if pixel tracking exists).
- **Recommendation: hold for now** — GCAD‑New's ~21,700 reached users is borderline; revisit at higher volume.

> **CBO vs ABO:** with a small budget and a **testing** objective, use **Ad‑Set Budget Optimisation (ABO)** while consolidating and learning (so each test gets guaranteed spend). Move to **Campaign Budget Optimisation (CBO)** once you have 2–3 proven ad sets and want Meta to allocate between winners.

---

## 15. Testing Matrix

| # | Hypothesis | Variable | Control | Challenger | Budget | Primary KPI | Secondary KPI | Min. evidence | Decision rule | Next action |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Consolidation lowers cost/conv | Ad‑set count | 7 ad sets | 1–2 consolidated | 60% | Cost/in‑area conv | Cost/conv | ~50 conv or 2 wks | If ≥15% better → keep | Merge ad sets |
| 2 | Instant Form yields better in‑area quality | Destination | WhatsApp | Instant Form | 20% | Cost/qualified in‑area lead | Form completion rate | 2–3 wks / ~$300+ | Compare qualified CPL | Keep both, report separately |
| 3 | `home`‑only cuts out‑of‑area | Location type | home+recent+freq | home only | 10% | Out‑of‑area rate | Cost/conv | ~30 leads tagged | If out‑of‑area drops, no CPL spike → adopt | Duplicate core ad set |
| 4 | Fixing CTA/placeholder lifts conv rate | Creative hygiene | Mixed CTA / `{{product.name}}` | Single CTA / real headline | 10% | Click→conv rate | CTR | ~2 wks | If conv rate up → standardise | Edit creatives |

**Rule:** test **one major variable at a time**; keep control and challenger clearly labelled.

---

## 16. KPI Framework

**Primary KPI:** **Cost per qualified in‑area lead** *(requires the tracking sheet — not yet measurable; standing up that measurement is the #1 action).*

**Secondary KPIs (report weekly):** total qualified leads · in‑area lead rate · contact rate · appointment rate · qualified‑lead rate · Meta CPL (by conversion type) · CTR · CPC · CPM · form completion rate · WhatsApp qualification rate.

> **We will not chase a lower raw CPL if it lowers lead quality.** A $30 out‑of‑area WhatsApp click is worse than a $90 in‑area, contactable, qualified conversation. The whole point of the tracking sheet and Instant Form is to optimise toward **qualified in‑area** leads, not vanity cost.

---

## 17. Final Findings Table — *Exactly What Makes the Two Accounts Different*

| Area | Project Pioneer | GCAD Construction – New | Performance effect | Evidence | Recommended GCAD action | Priority |
|---|---|---|---|---|---|---|
| Account maturity | ~5 months | ~1 month | Higher (Pioneer) | Confirmed | Allow ramp; don't over‑edit | — |
| Conversion history | 280 conversations | 20 conversations | Higher | Confirmed | Consolidate to build signal | High |
| Campaign objective | OUTCOME_LEADS | OUTCOME_LEADS | Neutral | Confirmed | Keep | — |
| Optimisation goal | Messaging conversations | REPLIES (WA) / LEAD_GEN (form) | Possible drag on thin data | Data‑supported | Test conversations goal at volume | Med |
| Campaign structure | 1 campaign / 3 ad sets | 3 campaigns / 7 ad sets | Fragmentation hurts GCAD | Confirmed | Consolidate | High |
| Budget concentration | Concentrated | Fragmented ($20/day cells) | Weak signal | Confirmed | Fund fewer ad sets | High |
| Geographic targeting | Multi‑city + creative qualify | Tight GTA + exclusions | Quality‑focused (good) | Confirmed | Standardise method | Med |
| Geographic exclusions | ~14 custom (Home) | ~69 cities + 12 custom | Strong control | Confirmed | Maintain; test home‑only | Med |
| Audience size | Broader | Tighter (~22k reach) | Slightly higher CPM | Confirmed | Monitor CPM vs quality | Low |
| Creative quality | Strong, varied | **Strong already** | GCAD CTR higher | Confirmed | Keep; adapt Pioneer principles | Med |
| Creative volume | 6+ live, static+video | Several + dynamic | Adequate | Confirmed | Fix CTA/placeholder | Med |
| Offer | $47,990 turnkey + proof | $46,500 legal suite + ROI | Comparable | Confirmed | Keep, add proof | Low |
| Social proof | "15+ years", AODA, code | Legal/inspection angle | Pioneer richer | Data‑supported | Add reviews/portfolio | Med |
| WhatsApp setup | Not measured | Not measured | Unknown | Data not provided | Add qualification opener + log | High |
| Response process | Not measured | Not measured | Unknown | Data not provided | Track response time | High |
| Instant Form qualification | None dedicated | New, conditional logic | Promising, unproven | Data not provided | Validate logic; gather data | High |
| Qualified‑lead tracking | None | None | Can't price quality | Data not provided | **Build tracking sheet** | **Critical** |
| CRM / offline feedback | None | None | No return signal | Data not provided | Connect CRM/offline events | High |
| Testing history | Vertical tests, video | Rapid ad‑set churn | Churn wastes learning | Data‑supported | Structured one‑variable tests | Med |

---

## 18. Final Action Checklist — *What We Will Implement in GCAD to Lower Cost per Qualified Lead*

| Action | Reason | Owner | Start | Review | KPI | Priority | Status |
|---|---|---|---|---|---|---|---|
| Stand up lead‑quality tracking sheet (postal code, in/out area, contact, qualified, appt, sale) | Enables the primary KPI | Agency + Client | Day 1 | Day 7 | Cost/qualified in‑area lead | **Critical** | Not started |
| Add WhatsApp qualification opener (5 questions) | Screen area/intent, capture project location | Agency + Client | Day 1 | Day 10 | WhatsApp qualification rate | High | Not started |
| Consolidate 7 ad sets → 1–2 funded ad sets | Concentrate conversion signal | Agency | Day 3 | Day 17 | Cost/conversation | High | Not started |
| Rework/pause the $111 saturated ad set (freq 4.80) | Stop overspending on fatigued audience | Agency | Day 3 | Day 10 | Frequency, cost/conv | High | Not started |
| Fix mixed CTA + `{{product.name}}` placeholder ads | Clean optimisation signal | Agency | Day 2 | Day 9 | Click→conv rate | Med | Not started |
| Validate Instant Form conditional logic (area/type/ownership/timeline/budget) | Ensure it truly qualifies | Agency | Day 2 | Day 9 | Form completion rate | High | Not started |
| Standardise geo method + test `home`‑only | Reduce out‑of‑area risk | Agency | Day 5 | Day 21 | Out‑of‑area rate | Med | Not started |
| Let Instant Form gather 2–3 weeks data | Avoid premature judgement | Agency | Day 1 | Day 21 | Cost/qualified in‑area lead | High | In progress |
| Adapt Pioneer creative principles (proof, price, geo‑qualify) | Transfer what works | Agency | Day 8 | Day 21 | Cost/conv, CTR | Med | Not started |
| Weekly reporting split by conversion type + qualified in‑area | Optimise to quality not vanity CPL | Agency | Day 7 | Weekly | All secondary KPIs | High | Not started |
| Explore CRM / offline conversion feedback to Meta | Teach Meta what a good lead is | Agency + Client | Day 22 | Day 45 | Qualified‑lead rate | Med | Not started |

---

## Additional Data Required

To move from **cost per conversation** to the real goal — **cost per qualified in‑area lead** — we need, from the client or a connected system:

1. **Project postal code** for each enquiry (WhatsApp + form) → in/out‑of‑area tagging.
2. **Contactable / qualified / appointment / sale** outcomes per lead (a simple shared sheet or CRM).
3. **WhatsApp response times** and qualification answers.
4. **Instant Form question set and conditional‑logic rules** (screenshot from Ads Manager).
5. Any **offer, promotion, or availability** changes over the period.

Until these exist, all quality‑, appointment‑, and sale‑level metrics are marked **"Data not provided"** and no cost‑per‑qualified‑lead is claimed for either account.

---

## The 10 Questions, Answered in Plain Language

1. **Why is Project Pioneer performing better?** More history and conversation volume, a single concentrated campaign, and 5 months of accumulated optimisation — plus a strong start of its own. It produces conversations at ~$55 now (~$24 lifetime) vs GCAD‑New's ~$74.
2. **Why is GCAD currently more expensive?** A ~1‑month‑old account with only 20 conversations spread across 7 thin ad sets, one saturated ad set at $111, and a softer click‑to‑conversation step — while measurement of true lead quality doesn't exist yet.
3. **Which differences are proven?** Maturity/volume, budget fragmentation, ad‑set saturation, and GCAD‑New's *higher* CTR / *lower* CPC (Section 10A, 5, 7).
4. **Which are only possible explanations?** Seasonality, WhatsApp‑flow handling, REPLIES‑optimisation on thin data, and any remaining out‑of‑area leakage (Section 10B–C).
5. **What has already been corrected?** Service‑area tightened to GTA postal codes/radius, ~69 cities + custom areas excluded, geo‑expansion off, service area stated in creative, and a new Instant Form path launched.
6. **What should be implemented next?** Tracking sheet + WhatsApp qualification opener, ad‑set consolidation, fix the saturated ad set, validate the form (Section 18).
7. **What should be transferred from Pioneer?** Creative *principles* (price anchor, proof, geo self‑qualification), budget concentration, and structured one‑variable testing.
8. **What should not be copied blindly?** Pioneer's exact ads, its broad multi‑city geo, and any placement cuts based on small samples.
9. **How will we reduce GCAD's cost per qualified lead?** Concentrate signal, measure quality, keep WhatsApp and form separate, optimise to **qualified in‑area** leads — not raw CPL.
10. **How and when will we know it worked?** Weekly review of cost per qualified in‑area lead and the secondary KPIs, with clear decision rules at Day 7, 21, and 45 (Sections 13, 15).

> **Closing note:** GCAD Construction – New is a **healthy young account with good creative and a corrected geographic setup**. The remaining work is **measurement and concentration**, not reinvention. With the tracking and consolidation steps above, we expect a **lower cost per qualified in‑area lead over the next six weeks** — measured honestly, and reported with WhatsApp and Instant Form kept separate.

---

*Prepared by PPC Guru · 24 July 2026 · Figures are Meta‑reported (Project Pioneer via Adzviser; GCAD‑New via Meta Ads API). Quality‑, appointment‑, and sale‑level outcomes are not yet tracked and are marked "Data not provided."*
