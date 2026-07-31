#!/usr/bin/env bash
# Render every case-study.json -> case-study.html -> case-study.pdf
set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHROME="$(ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1)"
mapfile -t FOLDERS < <(find "$ROOT/google-ads" "$ROOT/meta-ads" -maxdepth 1 -mindepth 1 -type d | sort)
built=0; pdfs=0
for f in "${FOLDERS[@]}"; do
  [ -f "$f/case-study.json" ] || { echo "skip (no json): $f"; continue; }
  python3 "$ROOT/_build/build_report.py" "$f" >/dev/null || { echo "HTML FAIL: $f"; continue; }
  built=$((built+1))
  fname=$(python3 -c "import json,sys;print(json.load(open('$f/case-study.json'))['meta']['pdf_filename'])")
  "$CHROME" --headless --no-sandbox --disable-gpu --no-pdf-header-footer \
     --print-to-pdf="$f/$fname" "$f/case-study.html" >/dev/null 2>&1
  if [ -f "$f/$fname" ]; then pdfs=$((pdfs+1)); cp "$f/$fname" "$f/case-study.pdf"; else echo "PDF FAIL: $f"; fi
done
echo "HTML built: $built | PDFs: $pdfs"
