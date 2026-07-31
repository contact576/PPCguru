#!/usr/bin/env python3
"""Scan all client folders and emit case-study-index.csv + project-summary.md."""
import json, os, csv, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COLS = ["Client Name", "Platform", "Industry", "PPC Guru Start Date", "Comparison Period",
        "Main Metric", "Previous Result", "New Result", "Percentage Improvement",
        "PDF File Path", "Status", "Data Confidence", "Notes"]

EXPECTED = {
    "google-ads": ["rehab-clinic", "rj-cad-solutions", "westway-immigration", "jk-appliance-repair",
                   "therapy-villa", "northyork-healthcare-associates", "palmdale-health-center",
                   "true-life-wellness-physio", "rehab2go", "bindra-world-immigration-terminal",
                   "ecocare-home-comfort", "blockline-physiotherapy-wellness", "apexshine-cleaning",
                   "vin-engineering"],
    "meta-ads": ["gcad-construction", "projects-pioneer", "ppc-guru", "ecocare",
                 "true-life-wellness-physio", "lavish-artigiano", "soldbykaushik", "ace-equity", "muydor"],
}

def load(folder):
    p = os.path.join(folder, "case-study.json")
    if not os.path.exists(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None

def row_for(platform_dir, slug):
    folder = os.path.join(ROOT, platform_dir, slug)
    d = load(folder)
    if not d:
        return {"Client Name": slug, "Platform": platform_dir, "Industry": "", "PPC Guru Start Date": "",
                "Comparison Period": "", "Main Metric": "", "Previous Result": "", "New Result": "",
                "Percentage Improvement": "", "PDF File Path": "", "Status": "Missing",
                "Data Confidence": "Low", "Notes": "case-study.json not found"}
    m = d.get("meta", {})
    cmp = (d.get("comparison") or {}).get("rows") or []
    main = cmp[0] if cmp else {}
    pdf = m.get("pdf_filename", "")
    pdf_path = f"{platform_dir}/{slug}/{pdf}" if pdf else ""
    return {"Client Name": m.get("client_display", slug), "Platform": m.get("platform", platform_dir),
            "Industry": m.get("industry", ""), "PPC Guru Start Date": m.get("managed_since", ""),
            "Comparison Period": m.get("comparison_period", ""),
            "Main Metric": main.get("metric", (d.get("kpis") or [{}])[0].get("label", "")),
            "Previous Result": main.get("before", ""), "New Result": main.get("after", ""),
            "Percentage Improvement": main.get("change", ""), "PDF File Path": pdf_path,
            "Status": m.get("status", "Needs Review"), "Data Confidence": m.get("confidence", ""),
            "Notes": (m.get("comparison_period", "") or "")[:80]}

def main():
    rows = []
    for pd, slugs in EXPECTED.items():
        for s in slugs:
            rows.append(row_for(pd, s))
    # write CSV
    with open(os.path.join(ROOT, "case-study-index.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    # summary
    total = len(rows)
    g = sum(1 for r in rows if "google" in r["Platform"].lower() or r["Platform"] == "google-ads")
    done = [r for r in rows if r["Status"] == "Completed"]
    review = [r for r in rows if r["Status"] in ("Needs Review", "Insufficient Data")]
    missing = [r for r in rows if r["Status"] in ("Missing", "Account Not Found", "MCP Access Error")]
    lines = []
    lines.append("# PPC Guru Case Studies — Project Summary\n")
    lines.append(f"- Total clients requested: {total}")
    lines.append(f"- Google Ads accounts: {sum(1 for r in rows if r['Platform']=='Google Ads' or 'google' in r['Platform'].lower())}")
    lines.append(f"- Meta Ads accounts: {sum(1 for r in rows if 'meta' in r['Platform'].lower())}")
    lines.append(f"- Completed case studies: {len(done)}")
    lines.append(f"- Needs review / insufficient data: {len(review)}")
    lines.append(f"- Missing / not found / MCP error: {len(missing)}\n")
    lines.append("## Status by client\n")
    lines.append("| Client | Platform | Industry | Main metric | Before | After | Change | Status | Confidence |")
    lines.append("|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        lines.append(f"| {r['Client Name']} | {r['Platform']} | {r['Industry']} | {r['Main Metric']} | "
                     f"{r['Previous Result']} | {r['New Result']} | {r['Percentage Improvement']} | "
                     f"{r['Status']} | {r['Data Confidence']} |")
    lines.append("\n## Generated PDFs\n")
    for r in rows:
        if r["PDF File Path"]:
            lines.append(f"- `{r['PDF File Path']}`")
    if review:
        lines.append("\n## Needs manual review\n")
        for r in review:
            lines.append(f"- {r['Client Name']} ({r['Status']}) — {r['Notes']}")
    if missing:
        lines.append("\n## Missing / errors\n")
        for r in missing:
            lines.append(f"- {r['Client Name']} — {r['Notes']}")
    with open(os.path.join(ROOT, "project-summary.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"index: {total} rows | completed {len(done)} | review {len(review)} | missing {len(missing)}")

if __name__ == "__main__":
    main()
