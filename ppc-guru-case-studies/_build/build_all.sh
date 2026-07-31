#!/usr/bin/env bash
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHROME="$(ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1)"
mapfile -t FOLDERS < <(find "$ROOT/google-ads" "$ROOT/meta-ads" -maxdepth 1 -mindepth 1 -type d | sort)
built=0; pdfs=0; cards=0
for f in "${FOLDERS[@]}"; do
  [ -f "$f/case-study.json" ] || { echo "skip (no json): $f"; continue; }
  python3 "$ROOT/_build/build_report.py" "$f" >/dev/null 2>&1 || { echo "HTML FAIL: $f"; continue; }
  python3 "$ROOT/_build/md_from_json.py" "$f" >/dev/null 2>&1
  python3 "$ROOT/_build/share_card.py" "$f" >/dev/null 2>&1
  built=$((built+1))
  fname=$(python3 -c "import json;print(json.load(open('$f/case-study.json'))['meta']['pdf_filename'])")
  "$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer --print-to-pdf="$f/$fname" "$f/case-study.html" >/dev/null 2>&1
  [ -f "$f/$fname" ] && { pdfs=$((pdfs+1)); cp "$f/$fname" "$f/case-study.pdf"; } || echo "PDF FAIL: $f"
  if [ -f "$f/share-card.html" ]; then
    "$CHROME" --headless --no-sandbox --disable-gpu --hide-scrollbars --force-device-scale-factor=1 --window-size=1200,820 --screenshot="$f/charts/_sc_tall.png" "$f/share-card.html" >/dev/null 2>&1
    if [ -f "$f/charts/_sc_tall.png" ]; then
      python3 -c "from PIL import Image;Image.open('$f/charts/_sc_tall.png').crop((0,0,1200,630)).save('$f/charts/share-card.png')" 2>/dev/null
      rm -f "$f/charts/_sc_tall.png"
      [ -f "$f/charts/share-card.png" ] && cards=$((cards+1))
    fi
  fi
done
echo "HTML: $built | PDFs: $pdfs | Share cards: $cards"
