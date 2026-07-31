#!/usr/bin/env python3
"""Generate case-study.md from case-study.json so markdown always matches the PDF.
Usage: python3 md_from_json.py <client-folder> [...]"""
import json, sys, os

DISCLAIMER = ("Advertising results vary based on industry, market conditions, competition, budget, campaign history, "
              "offer, website experience, conversion tracking, and other factors. The results presented in this case "
              "study reflect the specific account and reporting periods shown and do not guarantee future performance.")

def md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "| " + " | ".join(["---"] * len(headers)) + " |"]
    for r in rows:
        out.append("| " + " | ".join(str(c) for c in r) + " |")
    return "\n".join(out)

def build_compact_md(folder, d, m):
    L = []
    L.append(f"# {m.get('industry','')} {m.get('platform','')} Case Study — {m.get('client_display','')}\n")
    L.append("## SEO")
    L.append(f"- **Title:** {m.get('seo_title','')}")
    L.append(f"- **Meta description:** {m.get('meta_description','')}")
    L.append(f"- **Slug:** `{m.get('slug','')}`")
    L.append(f"- **Primary keyword:** {m.get('primary_keyword','')}")
    L.append(f"- **Secondary keywords:** {', '.join(m.get('secondary_keywords',[]))}")
    L.append(f"- **Confidence:** {m.get('confidence','')} | **Status:** {m.get('status','')}\n")
    L.append(f"## {d.get('headline','')}\n")
    if d.get("kpis"):
        L.append("**Headline results:** " + " · ".join(f"{k.get('value','')} {k.get('label','')}" for k in d["kpis"]) + "\n")
    L.append(d.get("summary_line", "") + "\n")
    if d.get("client_context"):
        L.append("### About the Client")
        L.append(d["client_context"] + "\n")
    if d.get("background"):
        L.append("### How the Account Came to PPC Guru")
        L.append(d["background"] + "\n")
    L.append(f"### {d.get('challenge_title','The Challenge')}")
    L.append(d.get("challenge", "") + "\n")
    if d.get("analysis") or d.get("analysis_points"):
        L.append("### What We Analyzed & Planned")
        if d.get("analysis"):
            L.append(d["analysis"] + "\n")
        for p in d.get("analysis_points", []):
            L.append(f"- {p}")
        L.append("")
    if d.get("timeline"):
        L.append(f"### {d.get('timeline_title','Engagement Timeline')}")
        for i in d["timeline"]:
            L.append(f"- **{i.get('when','')}:** {i.get('what','')}")
        L.append("")
    L.append("### What PPC Guru Did & Why")
    if d.get("changes"):
        L.append(md_table(["Change", "Why"], [[c.get("change",""), c.get("why","")] for c in d["changes"]]))
    L.append("")
    if d.get("technical"):
        L.append("### Under the Hood (account configuration)")
        for t in d["technical"]:
            L.append(f"- **{t.get('label','')}:** {t.get('value','')}")
        L.append("")
    if d.get("early_stage"):
        es = d["early_stage"]
        L.append(f"### {es.get('title','The First Month & Early Results')}")
        if es.get("intro"):
            L.append(es["intro"] + "\n")
        if es.get("rows"):
            L.append(md_table(es.get("headers", []), es["rows"]))
        L.append("")
    if d.get("gradual"):
        L.append("### Gradual Improvement, Month by Month")
        L.append(d["gradual"] + "\n")
    L.append("### Results")
    cmp = d.get("comparison", {})
    if cmp.get("rows"):
        rows = [[r.get("metric",""), r.get("before",""), r.get("after",""), r.get("change","")] for r in cmp["rows"]]
        L.append(md_table(["Metric", cmp.get("col_before","Before"), cmp.get("col_after","After"), "Change"], rows))
    if d.get("benchmark"):
        L.append(f"\n_{d['benchmark']}_")
    if d.get("lead_quality"):
        L.append(f"\n**Lead quality:** {d['lead_quality']}")
    L.append("")
    if d.get("spotlight") and d["spotlight"].get("body"):
        L.append(f"### {d['spotlight'].get('title','Why It Matters')}")
        L.append(d["spotlight"]["body"] + "\n")
    if d.get("lessons"):
        L.append(f"### {d.get('lessons_title','Lessons for Business Owners')}")
        for i, x in enumerate(d["lessons"], 1):
            L.append(f"{i}. {x}")
        L.append("")
    L.append("### Why It Worked")
    for w in d.get("why_it_worked", []):
        L.append(f"- {w}")
    L.append("")
    L.append(f"### {d.get('outcome_title','The Outcome')}")
    L.append(d.get("outcome", "") + "\n")
    L.append("### Get in touch")
    L.append(d.get("cta", "") + "\n")
    L.append("---")
    L.append(f"*{DISCLAIMER}*\n")
    out = os.path.join(folder, "case-study.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out

def build(folder):
    d = json.load(open(os.path.join(folder, "case-study.json"), encoding="utf-8"))
    m = d.get("meta", {})
    if m.get("layout") == "compact":
        return build_compact_md(folder, d, m)
    L = []
    L.append(f"# {m.get('industry','')} {m.get('platform','')} Case Study — {m.get('client_display','')}\n")
    L.append("## 1. SEO Meta Information")
    L.append(f"- **SEO Title:** {m.get('seo_title','')}")
    L.append(f"- **Meta Description:** {m.get('meta_description','')}")
    L.append(f"- **Suggested URL Slug:** `{m.get('slug','')}`")
    L.append(f"- **Primary Keyword:** {m.get('primary_keyword','')}")
    L.append(f"- **Secondary Keywords:** {', '.join(m.get('secondary_keywords',[]))}")
    L.append(f"- **Platform:** {m.get('platform','')} | **Data confidence:** {m.get('confidence','')} | **Status:** {m.get('status','')}\n")
    L.append("## 2. Headline")
    L.append(f"**{d.get('headline','')}**\n")
    L.append("## 3. Executive Summary")
    L.append(d.get("executive_summary", "") + "\n")
    L.append("## 4. Client Overview")
    for i in d.get("client_overview", []):
        L.append(f"- **{i.get('label','')}:** {i.get('value','')}")
    L.append("")
    L.append("## 5. The Opportunity")
    L.append(d.get("opportunity", "") + "\n")
    L.append("## 6. PPC Guru's Strategy")
    if d.get("strategy_intro"):
        L.append(d["strategy_intro"] + "\n")
    for b in d.get("strategy_bullets", []):
        L.append(f"- {b}")
    L.append("")
    L.append("## 7. Performance Comparison")
    cmp = d.get("comparison", {})
    if cmp.get("rows"):
        rows = [[r.get("metric",""), r.get("before",""), r.get("after",""), r.get("change","")] for r in cmp["rows"]]
        L.append(md_table(["Metric", cmp.get("col_before","Before"), cmp.get("col_after","After"), "Change"], rows))
    L.append("")
    L.append("## 8. Key Results")
    for k in d.get("key_results", []):
        L.append(f"- {k}")
    L.append("")
    if d.get("early_stage"):
        es = d["early_stage"]
        L.append("## 9. First-Month & Early-Stage Results")
        if es.get("intro"):
            L.append(es["intro"] + "\n")
        if es.get("rows"):
            L.append(md_table(es.get("headers", []), es["rows"]))
        L.append("")
    L.append("## 10. Business Impact")
    L.append(d.get("business_impact", "") + "\n")
    L.append("## 11. Why the Campaign Worked")
    for w in d.get("why_it_worked", []):
        L.append(f"- {w}")
    L.append("")
    L.append("## 12. Conclusion")
    L.append(d.get("conclusion", "") + "\n")
    L.append("## 13. Call to Action")
    L.append(d.get("cta", "") + "\n")
    L.append("## 14. Disclaimer")
    L.append(f"*{DISCLAIMER}*\n")
    out = os.path.join(folder, "case-study.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    return out

if __name__ == "__main__":
    for folder in sys.argv[1:]:
        print("wrote:", build(folder))
