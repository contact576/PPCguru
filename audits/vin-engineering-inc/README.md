# Vin Engineering INC — Google Ads Audit

Full performance audit of the **Vin Engineering INC** Google Ads account (566-536-4039, CAD),
produced for PPC Guru. Data pulled live via the **PPC Guru Google Ads MCP** for the
**last 30 days: Jun 23 – Jul 22, 2026**.

## Files

| File | What it is |
|------|-----------|
| `Vin_Engineering_Google_Ads_Audit.pdf` | 13-page client-facing audit (the deliverable) |
| `Vin_Engineering_Negative_Keywords.csv` | 76 categorized negative keywords, ready to import |
| `vin_audit_source.html` | HTML source of the PDF (re-render with WeasyPrint) |

Re-render the PDF:

```bash
pip install weasyprint
python3 -c "from weasyprint import HTML; HTML('vin_audit_source.html').write_pdf('Vin_Engineering_Google_Ads_Audit.pdf')"
```

## Headline numbers (last 30 days)

| Metric | Value |
|---|---|
| Spend | CAD $1,472.35 |
| Impressions | 3,188 |
| Clicks | 198 |
| CTR | 6.21% |
| Avg CPC | $7.44 |
| Leads (conversions) | 13 (9 form fills + 4 calls) |
| Cost / lead | $113.26 |
| Search impression share | 34.0% |
| Impr. share lost to rank | 43.8% |
| Impr. share lost to budget | 22.2% |
| Optimization score | 55.5% |

## Diagnosis in one line

A young, single-campaign account with good fundamentals (clean Search-only setup, disciplined
phrase/exact match types, real lead tracking, strong ad copy) held back chiefly by a
**weak landing page** — Google rates post-click (landing-page) Quality Score `BELOW_AVERAGE`
on nearly every keyword, which inflates CPCs to $7.44 and loses 43.8% of impressions to Ad Rank.

## Top areas requiring optimization (full list in the PDF)

1. **Landing page** — rebuild to message-match the ads (Critical)
2. **Quality Score** — outcome of the landing page + ad-group split (Critical)
3. **Negative keywords** — import the CSV (government/portal, DIY, wrong-service, out-of-area) (High)
4. **Account structure** — split the single ad group into 3–4 themed ad groups (High)
5. **Conversion tracking** — verify firing/dedup, resolve double-counted calls, import booked jobs (High)
6. **"building permit" close variants** — contain the top-spending, zero-lead broad query (High)
7. **Geo targeting** — remove the mistakenly-targeted **Cambridge, England (UK)** (Medium)
8. **Bidding guardrail** — add a Target CPA to Maximize Conversions (Medium)
9. **Ad creative** — add a 2nd RSA + ad assets per group (Medium)
10. **Prune** zero-traffic / off-core keywords (Medium)
11–14. Watch-list: underperforming relevant keywords, budget scaling, device bids, ad schedule

## Method & limitations

- Every figure is pulled live from the Google Ads API — nothing is estimated.
- Conversion tag firing, de-duplication and attribution settings are **not** readable via the
  API and require a manual in-platform check.
- Search-term dollar figures reflect only the ~34% of spend Google itemizes above its privacy
  threshold, so true wasted spend is somewhat higher than the visible figures.
- Cost verdicts assume a lead→job close rate to be confirmed with the client.
