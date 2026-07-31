#!/usr/bin/env python3
"""
PPC Guru — Case Study report builder.

Reads a per-client `case-study.json` and renders a branded, A4, print-ready
`case-study.html`. A separate step (build_all.sh) rasterises each HTML to PDF
via headless Chromium. Charts are emitted as inline SVG so the PDF stays
selectable / searchable and needs no external assets.

Usage:  python3 build_report.py <path-to-client-folder>
The folder must contain case-study.json; outputs case-study.html beside it.
"""
import json, sys, os, html, math

# ---------- brand ----------
NAVY   = "#12294a"   # deep navy
BLUE   = "#1f6feb"   # PPC Guru brand blue
GREEN  = "#1a9e5f"   # positive performance
GREEN_D= "#127a48"
GREY   = "#5b6675"   # neutral text
LGREY  = "#eef2f7"   # light table background
BORDER = "#d9e1ec"
INK    = "#1b2431"

def esc(s):
    return html.escape(str(s)) if s is not None else ""

def para(text):
    """Split double-newlines into <p> blocks; keep single text as one <p>."""
    if not text:
        return ""
    blocks = [b.strip() for b in str(text).split("\n\n") if b.strip()]
    return "".join(f"<p>{esc(b)}</p>" for b in blocks)

# ---------- charts (inline SVG) ----------
def _nice_max(v):
    if v <= 0:
        return 1
    mag = 10 ** math.floor(math.log10(v))
    for m in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if m * mag >= v:
            return m * mag
    return 10 * mag

def line_chart(ch):
    """ch: {title, period, x:[labels], series:[{name,values,color}]}"""
    W, H = 720, 300
    padL, padR, padT, padB = 54, 20, 28, 54
    x = ch.get("x", [])
    series = ch.get("series", [])
    n = len(x)
    if n < 2:
        return ""
    allv = [v for s in series for v in s["values"] if v is not None]
    ymax = _nice_max(max(allv) if allv else 1)
    def px(i):
        return padL + (W - padL - padR) * (i / (n - 1))
    def py(v):
        return H - padB - (H - padT - padB) * (v / ymax)
    parts = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{esc(ch.get("title",""))}" class="chart">']
    # gridlines + y labels
    for g in range(5):
        v = ymax * g / 4
        yy = py(v)
        parts.append(f'<line x1="{padL}" y1="{yy:.1f}" x2="{W-padR}" y2="{yy:.1f}" stroke="{BORDER}" stroke-width="1"/>')
        parts.append(f'<text x="{padL-8}" y="{yy+4:.1f}" text-anchor="end" font-size="12" fill="{GREY}">{_fmt_num(v)}</text>')
    # x labels (thin out if many)
    step = max(1, n // 12)
    for i, lab in enumerate(x):
        if i % step == 0 or i == n - 1:
            parts.append(f'<text x="{px(i):.1f}" y="{H-padB+20:.1f}" text-anchor="middle" font-size="11" fill="{GREY}">{esc(lab)}</text>')
    # series
    palette = {"green": GREEN, "blue": BLUE, "navy": NAVY, "grey": GREY}
    for s in series:
        col = palette.get(s.get("color", "blue"), s.get("color", BLUE))
        pts = [f"{px(i):.1f},{py(v):.1f}" for i, v in enumerate(s["values"]) if v is not None]
        parts.append(f'<polyline fill="none" stroke="{col}" stroke-width="2.6" points="{" ".join(pts)}" stroke-linejoin="round"/>')
        for i, v in enumerate(s["values"]):
            if v is not None:
                parts.append(f'<circle cx="{px(i):.1f}" cy="{py(v):.1f}" r="2.6" fill="{col}"/>')
    # legend
    lx = padL
    for s in series:
        col = palette.get(s.get("color", "blue"), s.get("color", BLUE))
        parts.append(f'<rect x="{lx}" y="6" width="12" height="12" rx="2" fill="{col}"/>')
        parts.append(f'<text x="{lx+17}" y="16" font-size="12" fill="{INK}">{esc(s.get("name",""))}</text>')
        lx += 22 + 8 * len(s.get("name", ""))
    parts.append("</svg>")
    return _chart_wrap(ch, "".join(parts))

def bar_chart(ch):
    """ch: {title, period, labels:[..], values:[..], colors:[..]?, unit?}"""
    labels = ch.get("labels", [])
    values = ch.get("values", [])
    n = len(labels)
    if n == 0:
        return ""
    W, H = 720, 300
    padL, padR, padT, padB = 60, 20, 28, 50
    ymax = _nice_max(max(values) if values else 1)
    bw = (W - padL - padR) / n * 0.55
    gap = (W - padL - padR) / n
    def py(v):
        return H - padB - (H - padT - padB) * (v / ymax)
    palette = {"green": GREEN, "blue": BLUE, "navy": NAVY, "grey": GREY}
    colors = ch.get("colors", ["navy", "green"] * n)
    parts = [f'<svg viewBox="0 0 {W} {H}" width="100%" role="img" aria-label="{esc(ch.get("title",""))}" class="chart">']
    for g in range(5):
        v = ymax * g / 4
        yy = py(v)
        parts.append(f'<line x1="{padL}" y1="{yy:.1f}" x2="{W-padR}" y2="{yy:.1f}" stroke="{BORDER}" stroke-width="1"/>')
        parts.append(f'<text x="{padL-8}" y="{yy+4:.1f}" text-anchor="end" font-size="12" fill="{GREY}">{_fmt_num(v)}</text>')
    for i, (lab, v) in enumerate(zip(labels, values)):
        cx = padL + gap * i + gap / 2
        col = palette.get(colors[i] if i < len(colors) else "navy", "navy")
        yy = py(v)
        parts.append(f'<rect x="{cx-bw/2:.1f}" y="{yy:.1f}" width="{bw:.1f}" height="{H-padB-yy:.1f}" rx="4" fill="{col}"/>')
        parts.append(f'<text x="{cx:.1f}" y="{yy-8:.1f}" text-anchor="middle" font-size="13" font-weight="700" fill="{INK}">{_fmt_num(v)}</text>')
        parts.append(f'<text x="{cx:.1f}" y="{H-padB+20:.1f}" text-anchor="middle" font-size="12" fill="{GREY}">{esc(lab)}</text>')
    parts.append("</svg>")
    return _chart_wrap(ch, "".join(parts))

def _fmt_num(v):
    if v is None:
        return ""
    if abs(v) >= 1000:
        return f"{v:,.0f}"
    if v == int(v):
        return f"{int(v)}"
    return f"{v:,.1f}"

def _chart_wrap(ch, svg):
    cap = esc(ch.get("period", ""))
    cap_html = f'<div class="chart-cap">{cap}</div>' if cap else ""
    return (f'<figure class="chartbox"><figcaption class="chart-title">{esc(ch.get("title",""))}</figcaption>'
            f'{svg}{cap_html}</figure>')

def render_chart(ch):
    t = ch.get("type", "line")
    if t == "line":
        return line_chart(ch)
    if t in ("bar", "bar_compare"):
        return bar_chart(ch)
    return ""

# ---------- table ----------
def comparison_table(cmp):
    if not cmp or not cmp.get("rows"):
        return ""
    cb = esc(cmp.get("col_before", "Before PPC Guru"))
    ca = esc(cmp.get("col_after", "After PPC Guru"))
    head = (f'<tr><th class="mcol">Metric</th><th class="ncol">{cb}</th>'
            f'<th class="ncol">{ca}</th><th class="ccol">Change</th></tr>')
    body = []
    for r in cmp["rows"]:
        d = r.get("dir", "neutral")
        cls = {"up": "chg-up", "down-good": "chg-up", "neutral": "chg-neu"}.get(d, "chg-neu")
        arrow = "▲ " if d == "up" else ("▼ " if d == "down-good" else "")
        body.append(f'<tr><td class="mcol">{esc(r.get("metric",""))}</td>'
                     f'<td class="ncol">{esc(r.get("before",""))}</td>'
                     f'<td class="ncol">{esc(r.get("after",""))}</td>'
                     f'<td class="ccol {cls}">{arrow}{esc(r.get("change",""))}</td></tr>')
    return f'<table class="cmp"><thead>{head}</thead><tbody>{"".join(body)}</tbody></table>'

def simple_table(tbl):
    if not tbl or not tbl.get("rows"):
        return ""
    heads = "".join(f"<th>{esc(h)}</th>" for h in tbl.get("headers", []))
    rows = "".join("<tr>" + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for r in tbl["rows"])
    return f'<table class="simple"><thead><tr>{heads}</tr></thead><tbody>{rows}</tbody></table>'

def kv_grid(items):
    if not items:
        return ""
    cells = "".join(f'<div class="kv"><span class="kv-l">{esc(i.get("label",""))}</span>'
                    f'<span class="kv-v">{esc(i.get("value",""))}</span></div>' for i in items)
    return f'<div class="kvgrid">{cells}</div>'

def bullet_list(items, cls="bul"):
    if not items:
        return ""
    return f'<ul class="{cls}">' + "".join(f"<li>{esc(i)}</li>" for i in items) + "</ul>"

# ---------- page ----------
CSS = f"""
:root{{--navy:{NAVY};--blue:{BLUE};--green:{GREEN};--grey:{GREY};--ink:{INK};--border:{BORDER};--lgrey:{LGREY};}}
*{{box-sizing:border-box;}}
@page{{size:A4;margin:14mm 15mm;}}
html,body{{margin:0;padding:0;}}
body{{font-family:-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:var(--ink);font-size:11pt;line-height:1.5;}}
h1,h2,h3{{color:var(--navy);margin:0;}}
p{{margin:0 0 8px;}}
.small{{font-size:9.5pt;color:var(--grey);}}
.wrap{{max-width:800px;margin:0 auto;}}

/* cover */
.cover{{background:linear-gradient(135deg,var(--navy),#1c3a63 60%,#20558f);color:#fff;border-radius:14px;padding:34px 34px 30px;margin-bottom:20px;}}
.cover .brand{{display:flex;align-items:center;gap:10px;font-weight:800;letter-spacing:.3px;font-size:15pt;}}
.cover .dot{{width:22px;height:22px;border-radius:6px;background:var(--blue);display:inline-block;}}
.cover .tag{{display:inline-block;margin-top:22px;background:rgba(255,255,255,.14);border:1px solid rgba(255,255,255,.28);
  padding:5px 12px;border-radius:999px;font-size:9.5pt;font-weight:600;letter-spacing:.4px;text-transform:uppercase;}}
.cover h1{{color:#fff;font-size:24pt;line-height:1.18;margin:14px 0 0;font-weight:800;letter-spacing:-.3px;}}
.cover .sub{{color:#cdddf2;margin-top:12px;font-size:11pt;}}
.cover .meta-row{{display:flex;gap:26px;flex-wrap:wrap;margin-top:20px;font-size:9.5pt;}}
.cover .meta-row div span{{display:block;color:#9fc0e6;text-transform:uppercase;letter-spacing:.5px;font-size:8pt;}}
.cover .meta-row div b{{font-size:11pt;color:#fff;font-weight:700;}}

section{{margin:0 0 16px;}}
h2.sec{{font-size:13.5pt;font-weight:800;margin:20px 0 8px;padding-bottom:5px;border-bottom:2px solid var(--border);}}
h2.sec .n{{color:var(--blue);font-weight:800;margin-right:8px;}}

.exec{{background:var(--lgrey);border-left:4px solid var(--blue);border-radius:8px;padding:14px 16px;}}
.exec p{{margin:0;}}

.kvgrid{{display:grid;grid-template-columns:1fr 1fr;gap:6px 22px;}}
.kv{{display:flex;justify-content:space-between;gap:12px;border-bottom:1px dotted var(--border);padding:4px 0;}}
.kv-l{{color:var(--grey);}}
.kv-v{{font-weight:600;text-align:right;}}

ul.bul{{margin:4px 0 8px;padding-left:0;list-style:none;}}
ul.bul li{{position:relative;padding:3px 0 3px 20px;}}
ul.bul li:before{{content:"";position:absolute;left:2px;top:9px;width:7px;height:7px;border-radius:2px;background:var(--blue);}}
ul.res{{margin:4px 0;padding-left:0;list-style:none;}}
ul.res li{{position:relative;padding:6px 0 6px 26px;border-bottom:1px solid var(--border);font-weight:600;}}
ul.res li:before{{content:"✔";position:absolute;left:2px;top:6px;color:var(--green);font-weight:800;}}

table{{border-collapse:collapse;width:100%;font-size:10pt;margin:6px 0;}}
table.cmp th,table.cmp td{{padding:8px 10px;text-align:right;border-bottom:1px solid var(--border);}}
table.cmp th{{background:var(--navy);color:#fff;font-weight:700;font-size:9.5pt;}}
table.cmp th.mcol,table.cmp td.mcol{{text-align:left;}}
table.cmp tbody tr:nth-child(even){{background:var(--lgrey);}}
table.cmp td.mcol{{font-weight:600;color:var(--ink);}}
.chg-up{{color:var(--green);font-weight:800;}}
.chg-neu{{color:var(--grey);font-weight:700;}}
table.simple th{{background:var(--lgrey);color:var(--navy);text-align:right;padding:7px 10px;border-bottom:2px solid var(--border);font-size:9.5pt;}}
table.simple th:first-child,table.simple td:first-child{{text-align:left;}}
table.simple td{{padding:7px 10px;text-align:right;border-bottom:1px solid var(--border);}}

.chartbox{{margin:10px 0 6px;border:1px solid var(--border);border-radius:10px;padding:12px 14px 8px;background:#fff;}}
.chart-title{{font-weight:700;color:var(--navy);font-size:10.5pt;margin-bottom:4px;}}
.chart-cap{{font-size:8.5pt;color:var(--grey);margin-top:2px;}}
.charts-2{{display:grid;grid-template-columns:1fr 1fr;gap:12px;}}
@media print{{.charts-2{{grid-template-columns:1fr 1fr;}}}}

.cta{{background:linear-gradient(135deg,var(--navy),#20558f);color:#fff;border-radius:12px;padding:18px 20px;margin-top:18px;}}
.cta h3{{color:#fff;margin:0 0 6px;font-size:13pt;}}
.cta p{{margin:0;color:#e6eefb;}}
.disclaimer{{margin-top:16px;font-size:8pt;color:#8a94a3;border-top:1px solid var(--border);padding-top:8px;}}
.foot{{margin-top:10px;font-size:8.5pt;color:var(--grey);display:flex;justify-content:space-between;}}
.kw{{font-size:8.5pt;color:var(--grey);margin-top:4px;}}
.avoid-break{{break-inside:avoid;}}
"""

def build(folder):
    with open(os.path.join(folder, "case-study.json"), encoding="utf-8") as f:
        d = json.load(f)
    m = d.get("meta", {})

    charts_html = ""
    charts = d.get("charts", [])
    if charts:
        rendered = [render_chart(c) for c in charts]
        rendered = [r for r in rendered if r]
        if len(rendered) == 2:
            charts_html = f'<div class="charts-2">{rendered[0]}{rendered[1]}</div>'
        else:
            charts_html = "".join(rendered)

    early = ""
    if d.get("early_stage"):
        early = (f'<section class="avoid-break"><h2 class="sec"><span class="n">09</span>First-Month &amp; Early-Stage Results</h2>'
                 f'{para(d["early_stage"].get("intro",""))}{simple_table(d["early_stage"])}</section>')

    parts = []
    parts.append(f'<div class="wrap">')
    # cover
    parts.append(f'''<div class="cover">
      <div class="brand"><span class="dot"></span> PPC&nbsp;Guru</div>
      <div class="tag">Client Case Study · {esc(m.get("platform",""))}</div>
      <h1>{esc(d.get("headline",""))}</h1>
      <div class="sub">{esc(m.get("industry",""))} · {esc(m.get("platform",""))}</div>
      <div class="meta-row">
        <div><span>Reporting Period</span><b>{esc(m.get("reporting_period",""))}</b></div>
        <div><span>Platform</span><b>{esc(m.get("platform",""))}</b></div>
        <div><span>Comparison</span><b>{esc(m.get("comparison_period",""))}</b></div>
      </div>
    </div>''')
    # exec summary
    parts.append(f'<section class="avoid-break"><h2 class="sec"><span class="n">01</span>Executive Summary</h2>'
                 f'<div class="exec">{para(d.get("executive_summary",""))}</div></section>')
    # client overview
    parts.append(f'<section class="avoid-break"><h2 class="sec"><span class="n">02</span>Client Overview</h2>'
                 f'{kv_grid(d.get("client_overview",[]))}</section>')
    # opportunity
    parts.append(f'<section><h2 class="sec"><span class="n">03</span>The Opportunity</h2>{para(d.get("opportunity",""))}</section>')
    # strategy
    parts.append(f'<section><h2 class="sec"><span class="n">04</span>PPC Guru’s Strategy</h2>'
                 f'{para(d.get("strategy_intro",""))}{bullet_list(d.get("strategy_bullets",[]))}</section>')
    # performance comparison + charts
    parts.append(f'<section class="avoid-break"><h2 class="sec"><span class="n">05</span>Performance Comparison</h2>'
                 f'{comparison_table(d.get("comparison"))}{charts_html}</section>')
    # key results
    parts.append(f'<section class="avoid-break"><h2 class="sec"><span class="n">06</span>Key Results</h2>'
                 f'{bullet_list(d.get("key_results",[]),"res")}</section>')
    # early stage (optional)
    parts.append(early)
    # business impact
    parts.append(f'<section><h2 class="sec"><span class="n">07</span>Business Impact</h2>{para(d.get("business_impact",""))}</section>')
    # why it worked
    parts.append(f'<section class="avoid-break"><h2 class="sec"><span class="n">08</span>Why the Campaign Worked</h2>'
                 f'{bullet_list(d.get("why_it_worked",[]))}</section>')
    # conclusion
    parts.append(f'<section><h2 class="sec"><span class="n">10</span>Conclusion</h2>{para(d.get("conclusion",""))}</section>')
    # CTA
    parts.append(f'<div class="cta"><h3>Ready to grow with measurable advertising?</h3><p>{esc(d.get("cta",""))}</p></div>')
    # disclaimer
    disc = ("Advertising results vary based on industry, market conditions, competition, budget, campaign history, "
            "offer, website experience, conversion tracking, and other factors. The results presented in this case "
            "study reflect the specific account and reporting periods shown and do not guarantee future performance.")
    parts.append(f'<div class="disclaimer">{esc(disc)}</div>')
    kws = ", ".join([m.get("primary_keyword","")] + m.get("secondary_keywords",[]))
    parts.append(f'<div class="foot"><span>© PPC Guru — Canadian Digital Marketing Agency</span><span>ppcguru.ca</span></div>')
    parts.append(f'<div class="kw">Topics: {esc(kws)}</div>')
    parts.append("</div>")

    doc = (f'<!doctype html><html lang="en-CA"><head><meta charset="utf-8">'
           f'<meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>{esc(m.get("seo_title",""))}</title>'
           f'<meta name="description" content="{esc(m.get("meta_description",""))}">'
           f'<style>{CSS}</style></head><body>{"".join(parts)}</body></html>')
    out = os.path.join(folder, "case-study.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    return out

if __name__ == "__main__":
    for folder in sys.argv[1:]:
        try:
            print("built:", build(folder))
        except Exception as e:
            print("ERROR", folder, e, file=sys.stderr)
            raise
