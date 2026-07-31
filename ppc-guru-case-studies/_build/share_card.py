#!/usr/bin/env python3
"""Generate a 1200x630 social share card (share-card.html) from case-study.json.
build_all.sh screenshots it to share-card.png. Usage: python3 share_card.py <folder> [...]"""
import json, sys, os, html
NAVY="#12294a"; BLUE="#1f6feb"; GREEN="#1a9e5f"
def esc(s): return html.escape(str(s)) if s is not None else ""

def build(folder):
    d = json.load(open(os.path.join(folder, "case-study.json"), encoding="utf-8"))
    m = d.get("meta", {})
    kpis = d.get("kpis", [])[:3]
    tiles = "".join(
        f'<div class="t"><div class="v">{esc(k.get("value",""))}</div>'
        f'<div class="l">{esc(k.get("label",""))}</div></div>' for k in kpis)
    css = f"""
    *{{margin:0;box-sizing:border-box;}}
    html,body{{margin:0;padding:0;}}
    .card{{position:absolute;top:0;left:0;width:1200px;height:630px;overflow:hidden;
      font-family:-apple-system,'Segoe UI',Roboto,Arial,sans-serif;
      background:linear-gradient(125deg,{NAVY} 0%,#1c3a63 55%,#215891 100%);color:#fff;padding:50px 60px;
      display:flex;flex-direction:column;justify-content:space-between;}}
    .top{{display:flex;justify-content:space-between;align-items:center;}}
    .brand{{display:flex;align-items:center;gap:12px;font-weight:800;font-size:30px;}}
    .dot{{width:30px;height:30px;border-radius:8px;background:{BLUE};display:inline-block;}}
    .tag{{border:1px solid rgba(255,255,255,.35);border-radius:999px;padding:8px 18px;font-size:15px;
      text-transform:uppercase;letter-spacing:1px;font-weight:700;color:#cfe0f4;}}
    .mid .client{{color:#8fc4ff;font-weight:800;font-size:24px;}}
    h1{{font-size:42px;line-height:1.13;font-weight:800;margin-top:10px;max-width:1040px;letter-spacing:-.5px;}}
    .bottom{{display:flex;justify-content:space-between;align-items:flex-end;}}
    .tiles{{display:flex;gap:22px;}}
    .t{{background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.16);border-top:4px solid {GREEN};
      border-radius:14px;padding:14px 22px;min-width:180px;}}
    .t .v{{font-size:38px;font-weight:800;line-height:1;}}
    .t .l{{font-size:13.5px;color:#bcd4ef;margin-top:7px;text-transform:uppercase;letter-spacing:.5px;font-weight:600;}}
    .site{{color:#bcd4ef;font-size:20px;font-weight:700;padding-bottom:6px;}}
    """
    body = (f'<div class="top"><div class="brand"><span class="dot"></span>PPC&nbsp;Guru</div>'
            f'<div class="tag">{esc(m.get("platform",""))} Case Study</div></div>'
            f'<div class="mid"><div class="client">{esc(m.get("client_display",""))} · {esc(m.get("industry",""))}</div>'
            f'<h1>{esc(d.get("headline",""))}</h1></div>'
            f'<div class="bottom"><div class="tiles">{tiles}</div><div class="site">ppcguru.ca</div></div>')
    doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body><div class="card">{body}</div></body></html>'
    out = os.path.join(folder, "share-card.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(doc)
    return out

if __name__ == "__main__":
    for folder in sys.argv[1:]:
        print("wrote:", build(folder))
