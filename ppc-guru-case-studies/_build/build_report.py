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
import json, sys, os, html, math, io, base64

def make_qr_datauri(url):
    try:
        import qrcode
        qr = qrcode.QRCode(version=None, box_size=10, border=1,
                           error_correction=qrcode.constants.ERROR_CORRECT_M)
        qr.add_data(url); qr.make(fit=True)
        img = qr.make_image(fill_color="#12294a", back_color="white")
        buf = io.BytesIO(); img.save(buf, format="PNG")
        return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()
    except Exception:
        return ""

PUBLISH_DATE = "2026-07-31"

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

COMPACT_CSS = f"""
:root{{--navy:{NAVY};--blue:{BLUE};--green:{GREEN};--grey:{GREY};--ink:{INK};--border:{BORDER};--lgrey:{LGREY};}}
*{{box-sizing:border-box;}}
@page{{size:A4;margin:11mm 12mm;}}
html,body{{margin:0;padding:0;}}
body{{font-family:-apple-system,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;color:var(--ink);font-size:10.2pt;line-height:1.45;}}
h1,h2,h3{{color:var(--navy);margin:0;}}
p{{margin:0 0 6px;}}
.wrap{{max-width:820px;margin:0 auto;}}
/* header band */
.hdr{{background:linear-gradient(120deg,var(--navy),#1c3a63 62%,#215891);color:#fff;border-radius:12px;padding:20px 22px;}}
.hdr .top{{display:flex;justify-content:space-between;align-items:center;font-size:9pt;}}
.hdr .brand{{display:flex;align-items:center;gap:8px;font-weight:800;font-size:13pt;letter-spacing:.2px;}}
.hdr .dot{{width:18px;height:18px;border-radius:5px;background:var(--blue);display:inline-block;}}
.hdr .tag{{background:rgba(255,255,255,.15);border:1px solid rgba(255,255,255,.3);padding:3px 10px;border-radius:999px;
  text-transform:uppercase;letter-spacing:.5px;font-weight:600;font-size:8pt;}}
.hdr .client{{color:#8fc4ff;font-size:12.5pt;font-weight:800;letter-spacing:.2px;margin-top:13px;}}
.hdr h1{{color:#fff;font-size:17.5pt;line-height:1.16;margin:3px 0 6px;font-weight:800;letter-spacing:-.2px;}}
.hdr .sub{{color:#cfe0f4;font-size:9.5pt;}}
.method{{font-size:7.6pt;color:#9aa4b2;font-style:italic;margin-top:7px;}}
/* kpi tiles */
.kpis{{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:12px 0;}}
.kpi{{background:#fff;border:1px solid var(--border);border-top:3px solid var(--green);border-radius:10px;padding:11px 13px;}}
.kpi .v{{font-size:20pt;font-weight:800;color:var(--navy);line-height:1;}}
.kpi .l{{font-size:8.6pt;color:var(--grey);text-transform:uppercase;letter-spacing:.4px;margin-top:5px;font-weight:600;}}
.kpi .n{{font-size:8.4pt;color:var(--green);font-weight:700;margin-top:3px;}}
/* section headers */
h2.s{{font-size:11.5pt;font-weight:800;margin:13px 0 6px;display:flex;align-items:center;gap:8px;}}
h2.s:before{{content:"";width:5px;height:15px;background:var(--blue);border-radius:2px;display:inline-block;}}
.lead{{color:var(--ink);}}
/* two-col */
.cols{{display:grid;grid-template-columns:1.15fr .85fr;gap:14px;align-items:start;}}
/* changes table */
table.chg{{border-collapse:collapse;width:100%;font-size:9.4pt;}}
table.chg td{{padding:6px 8px;border-bottom:1px solid var(--border);vertical-align:top;}}
table.chg td.w{{font-weight:700;color:var(--navy);white-space:nowrap;width:1%;padding-right:12px;}}
table.chg td.y{{color:#3a4658;}}
/* under the hood */
.hood{{background:var(--lgrey);border:1px solid var(--border);border-radius:10px;padding:12px 14px;}}
.hood h3{{font-size:9.5pt;text-transform:uppercase;letter-spacing:.5px;color:var(--blue);margin-bottom:8px;}}
.hood .row{{display:flex;justify-content:space-between;gap:10px;padding:4px 0;border-bottom:1px dotted var(--border);font-size:9.2pt;}}
.hood .row:last-child{{border-bottom:none;}}
.hood .k{{color:var(--grey);}}
.hood .val{{font-weight:600;text-align:right;color:var(--ink);}}
/* results */
table.cmp{{border-collapse:collapse;width:100%;font-size:9.6pt;margin:4px 0;}}
table.cmp th,table.cmp td{{padding:7px 9px;text-align:right;border-bottom:1px solid var(--border);}}
table.cmp th{{background:var(--navy);color:#fff;font-weight:700;font-size:9pt;}}
table.cmp th.m,table.cmp td.m{{text-align:left;}}
table.cmp tbody tr:nth-child(even){{background:var(--lgrey);}}
table.cmp td.m{{font-weight:600;}}
.up{{color:var(--green);font-weight:800;}}.neu{{color:var(--grey);font-weight:700;}}
.chartbox{{margin:8px 0 2px;border:1px solid var(--border);border-radius:10px;padding:10px 12px 6px;}}
.chart-title{{font-weight:700;color:var(--navy);font-size:9.6pt;margin-bottom:2px;}}
.chart-cap{{font-size:8pt;color:var(--grey);}}
.charts-2{{display:grid;grid-template-columns:1fr 1fr;gap:12px;align-items:start;}}
.quality{{background:#eaf7f0;border:1px solid #bfe6d0;border-left:4px solid var(--green);border-radius:8px;
  padding:8px 12px;font-size:9.4pt;margin:8px 0 2px;color:#14603a;}}
.quality b{{color:#0f5c37;}}
.timeline{{margin:6px 0 2px;border-left:2px solid var(--border);padding-left:18px;}}
.tl-item{{position:relative;padding:5px 0;font-size:9.6pt;}}
.tl-item:before{{content:"";position:absolute;left:-25px;top:8px;width:9px;height:9px;border-radius:50%;
  background:var(--blue);box-shadow:0 0 0 3px #fff,0 0 0 4px var(--blue);}}
.tl-when{{font-weight:800;color:var(--navy);margin-right:10px;}}
.tl-what{{color:#3a4658;}}
.spotlight{{background:#eef4fd;border:1px solid #cddffb;border-left:4px solid var(--blue);border-radius:9px;
  padding:11px 14px;margin:8px 0;}}
.spotlight h3{{font-size:10pt;color:var(--blue);margin-bottom:4px;}}
.spotlight p{{margin:0;font-size:9.5pt;color:#26405f;}}
ol.lessons{{margin:4px 0;padding-left:0;list-style:none;counter-reset:l;}}
ol.lessons li{{position:relative;padding:5px 0 5px 32px;font-size:9.6pt;counter-increment:l;border-bottom:1px solid var(--border);}}
ol.lessons li:last-child{{border-bottom:none;}}
ol.lessons li:before{{content:counter(l);position:absolute;left:0;top:5px;width:21px;height:21px;background:var(--navy);
  color:#fff;border-radius:50%;font-size:9pt;font-weight:700;text-align:center;line-height:21px;}}
ul.why{{margin:4px 0;padding-left:0;list-style:none;}}
ul.why li{{position:relative;padding:4px 0 4px 22px;font-size:9.6pt;}}
ul.why li:before{{content:"✔";position:absolute;left:2px;top:4px;color:var(--green);font-weight:800;}}
.bench{{font-size:8.8pt;color:var(--grey);font-style:italic;margin-top:4px;}}
.cta{{background:linear-gradient(120deg,var(--navy),#215891);color:#fff;border-radius:11px;padding:13px 16px;margin-top:12px;display:flex;justify-content:space-between;align-items:center;gap:16px;}}
.cta b{{font-size:11pt;}}.cta p{{margin:2px 0 0;color:#dbe7f8;font-size:9pt;}}
.cta .qr{{display:flex;flex-direction:column;align-items:center;gap:3px;background:#fff;border-radius:8px;padding:6px 6px 4px;}}
.cta .qr img{{width:62px;height:62px;display:block;}}
.cta .qr span{{font-size:6.8pt;color:var(--navy);font-weight:800;letter-spacing:.2px;}}
.disc{{margin-top:9px;font-size:7.4pt;color:#9aa4b2;border-top:1px solid var(--border);padding-top:6px;}}
.foot{{margin-top:6px;font-size:8pt;color:var(--grey);display:flex;justify-content:space-between;}}
.avoid{{break-inside:avoid;}}
"""

def _hood_panel(items):
    if not items:
        return ""
    rows = "".join(f'<div class="row"><span class="k">{esc(i.get("label",""))}</span>'
                   f'<span class="val">{esc(i.get("value",""))}</span></div>' for i in items)
    return f'<div class="hood"><h3>Under the Hood</h3>{rows}</div>'

def _changes_table(items):
    if not items:
        return ""
    body = "".join(f'<tr><td class="w">{esc(i.get("change",""))}</td><td class="y">{esc(i.get("why",""))}</td></tr>' for i in items)
    return f'<table class="chg"><tbody>{body}</tbody></table>'

def _kpi_band(items):
    if not items:
        return ""
    cells = "".join(f'<div class="kpi"><div class="v">{esc(i.get("value",""))}</div>'
                    f'<div class="l">{esc(i.get("label",""))}</div>'
                    f'<div class="n">{esc(i.get("note",""))}</div></div>' for i in items[:3])
    return f'<div class="kpis">{cells}</div>'

def _cmp_compact(cmp):
    if not cmp or not cmp.get("rows"):
        return ""
    head = (f'<tr><th class="m">Metric</th><th>{esc(cmp.get("col_before","Before"))}</th>'
            f'<th>{esc(cmp.get("col_after","After"))}</th><th>Change</th></tr>')
    body = []
    for r in cmp["rows"]:
        d = r.get("dir", "neutral")
        cls = "up" if d in ("up", "down-good") else "neu"
        arrow = "▲ " if d == "up" else ("▼ " if d == "down-good" else "")
        body.append(f'<tr><td class="m">{esc(r.get("metric",""))}</td><td>{esc(r.get("before",""))}</td>'
                    f'<td>{esc(r.get("after",""))}</td><td class="{cls}">{arrow}{esc(r.get("change",""))}</td></tr>')
    return f'<table class="cmp"><thead>{head}</thead><tbody>{"".join(body)}</tbody></table>'

def build_compact(folder, d, m):
    charts = d.get("charts", [])
    rendered = [render_chart(c) for c in charts[:2]]
    rendered = [r for r in rendered if r]
    if len(rendered) == 2:
        chart_html = f'<div class="charts-2">{rendered[0]}{rendered[1]}</div>'
    else:
        chart_html = "".join(rendered)
    why = "".join(f"<li>{esc(w)}</li>" for w in d.get("why_it_worked", [])[:4])
    bench = f'<div class="bench">{esc(d.get("benchmark",""))}</div>' if d.get("benchmark") else ""
    quality = f'<div class="quality"><b>Lead quality:</b> {esc(d.get("lead_quality",""))}</div>' if d.get("lead_quality") else ""
    # About the client
    client_ctx = f'<h2 class="s">About the Client</h2>{para(d.get("client_context",""))}' if d.get("client_context") else ""
    # Engagement timeline (as indexable text)
    tl = d.get("timeline", [])
    timeline_html = ""
    if tl:
        items = "".join(f'<div class="tl-item"><span class="tl-when">{esc(i.get("when",""))}</span>'
                        f'<span class="tl-what">{esc(i.get("what",""))}</span></div>' for i in tl)
        timeline_html = f'<h2 class="s">{esc(d.get("timeline_title","Engagement Timeline"))}</h2><div class="timeline">{items}</div>'
    # Spotlight callout (e.g. why the integration matters)
    sp = d.get("spotlight")
    spotlight_html = (f'<div class="spotlight"><h3>{esc(sp.get("title",""))}</h3>{para(sp.get("body",""))}</div>'
                      if sp and sp.get("body") else "")
    # Lessons for owners
    lessons = d.get("lessons", [])
    lessons_html = ""
    if lessons:
        li = "".join(f"<li>{esc(x)}</li>" for x in lessons)
        lessons_html = f'<h2 class="s">{esc(d.get("lessons_title","Lessons for Business Owners"))}</h2><ol class="lessons">{li}</ol>'
    # --- detailed narrative sections (all optional) ---
    background = f'<h2 class="s">How the Account Came to PPC Guru</h2>{para(d.get("background",""))}' if d.get("background") else ""
    analysis = ""
    if d.get("analysis") or d.get("analysis_points"):
        ap = bullet_list(d.get("analysis_points", [])) if d.get("analysis_points") else ""
        analysis = f'<h2 class="s">What We Analyzed &amp; Planned</h2>{para(d.get("analysis",""))}{ap}'
    early = ""
    if d.get("early_stage"):
        es = d["early_stage"]
        early = (f'<h2 class="s">{esc(es.get("title","The First Month & Early Results"))}</h2>'
                 f'{para(es.get("intro",""))}{simple_table(es)}')
    # chart placement: in detailed mode put the trend chart under "Gradual Improvement", the summary chart under Results
    first_chart = rendered[0] if rendered else ""
    second_chart = rendered[1] if len(rendered) > 1 else ""
    gradual_html = ""
    if d.get("gradual"):
        gradual_html = (f'<h2 class="s">Gradual Improvement, Month by Month</h2>{para(d.get("gradual",""))}'
                        f'<div class="avoid">{first_chart}</div>')
        results_chart = f'<div class="avoid">{second_chart}</div>' if second_chart else ""
    else:
        results_chart = f'<div class="avoid">{chart_html}</div>'
    # QR code CTA -> tracked contact link
    slug_tail = (m.get("slug", "") or "").rstrip("/").split("/")[-1] or "case-study"
    qr_url = f'https://ppcguru.ca/contact?utm_source=case_study&utm_medium=pdf&utm_campaign={slug_tail}'
    qr = make_qr_datauri(qr_url)
    qr_html = (f'<div class="qr"><img src="{qr}" alt="Scan to book a strategy call"><span>SCAN TO BOOK</span></div>' if qr else "")
    # JSON-LD for SEO / AI search
    ld = {"@context": "https://schema.org", "@type": "Article",
          "headline": d.get("headline", ""), "description": m.get("meta_description", ""),
          "about": m.get("industry", ""), "keywords": ", ".join([m.get("primary_keyword","")] + m.get("secondary_keywords", [])),
          "datePublished": PUBLISH_DATE, "inLanguage": "en-CA",
          "author": {"@type": "Organization", "name": "PPC Guru", "url": "https://ppcguru.ca"},
          "publisher": {"@type": "Organization", "name": "PPC Guru", "url": "https://ppcguru.ca"}}
    jsonld = f'<script type="application/ld+json">{json.dumps(ld)}</script>'
    parts = [f'<div class="wrap">']
    sub_bits = [b for b in [m.get("industry",""), m.get("market",""),
                (f"Managed since {m.get('managed_since','')}" if m.get("managed_since") else m.get("reporting_period",""))] if b]
    parts.append(f'''<div class="hdr"><div class="top"><div class="brand"><span class="dot"></span>PPC&nbsp;Guru</div>
      <div class="tag">{esc(m.get("platform",""))} Case Study</div></div>
      <div class="client">{esc(m.get("client_display",""))}</div>
      <h1>{esc(d.get("headline",""))}</h1>
      <div class="sub">{esc(" · ".join(sub_bits))}</div></div>''')
    parts.append(_kpi_band(d.get("kpis", [])))
    parts.append(f'<div class="lead">{esc(d.get("summary_line",""))}</div>')
    parts.append(client_ctx)
    parts.append(background)
    parts.append(f'<h2 class="s">{esc(d.get("challenge_title","The Challenge"))}</h2><p>{esc(d.get("challenge",""))}</p>')
    parts.append(analysis)
    parts.append('<div class="cols avoid">')
    parts.append(f'<div><h2 class="s">What PPC Guru Did &amp; Why</h2>{_changes_table(d.get("changes",[]))}</div>')
    parts.append(f'<div>{_hood_panel(d.get("technical",[]))}</div>')
    parts.append('</div>')
    parts.append(timeline_html)
    parts.append(early)
    parts.append(gradual_html)
    parts.append(f'<h2 class="s">Results</h2>{_cmp_compact(d.get("comparison"))}{bench}{quality}{results_chart}')
    parts.append(f'<h2 class="s">Why It Worked</h2><ul class="why">{why}</ul>')
    parts.append(spotlight_html)
    parts.append(lessons_html)
    parts.append(f'<h2 class="s">{esc(d.get("outcome_title","The Outcome"))}</h2><p>{esc(d.get("outcome",""))}</p>')
    parts.append(f'''<div class="cta"><div><b>Want results like these?</b><p>{esc(d.get("cta",""))}</p></div>
      {qr_html}</div>''')
    disc = ("Advertising results vary based on industry, market conditions, competition, budget, campaign history, offer, "
            "website experience, conversion tracking, and other factors. The results reflect the specific account and "
            "reporting periods shown and do not guarantee future performance.")
    method = d.get("methodology", "")
    if method:
        parts.append(f'<div class="method">{esc(method)}</div>')
    parts.append(f'<div class="disc">{esc(disc)}</div>')
    parts.append(f'<div class="foot"><span>© PPC Guru — Canadian Digital Marketing Agency</span><span>ppcguru.ca</span></div>')
    parts.append('</div>')
    doc = (f'<!doctype html><html lang="en-CA"><head><meta charset="utf-8">'
           f'<meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>{esc(m.get("seo_title",""))}</title>'
           f'<meta name="description" content="{esc(m.get("meta_description",""))}">'
           f'{jsonld}<style>{COMPACT_CSS}</style></head><body>{"".join(parts)}</body></html>')
    out = os.path.join(folder, "case-study.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    # teaser for email / WhatsApp
    teaser = d.get("teaser", "")
    if not teaser and d.get("kpis"):
        k = d["kpis"][0]
        teaser = f'{m.get("industry","")} · {m.get("platform","")}: {d.get("summary_line","")}'
    if teaser:
        with open(os.path.join(folder, "teaser.txt"), "w", encoding="utf-8") as f:
            f.write(teaser.strip() + "\n\nRead the full case study: https://ppcguru.ca" + (m.get("slug","") or "") + "\n")
    return out

def build(folder):
    with open(os.path.join(folder, "case-study.json"), encoding="utf-8") as f:
        d = json.load(f)
    m = d.get("meta", {})
    if m.get("layout") == "compact":
        return build_compact(folder, d, m)

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
