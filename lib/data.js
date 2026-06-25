import seed from "@/data/snapshots.json";

// The dashboard reads its daily history from the Google Sheet data store when a
// published-CSV URL is provided via SHEET_CSV_URL. Otherwise it falls back to the
// committed snapshot (data/snapshots.json), which is seeded with real GCAD data so
// the dashboard always renders even before the live Sheet is wired up.
//
// To go fully live: in Google Sheets choose File → Share → Publish to web → CSV,
// then set SHEET_CSV_URL in Vercel to that link. The daily refresh job appends one
// row per day to that same Sheet.

function parseCsv(text) {
  const lines = text.trim().split(/\r?\n/);
  const header = lines[0].split(",").map((h) => h.trim());
  return lines.slice(1).map((line) => {
    const cells = line.split(",");
    const row = {};
    header.forEach((h, i) => (row[h] = (cells[i] ?? "").trim()));
    return row;
  });
}

function num(v) {
  const n = parseFloat(v);
  return Number.isFinite(n) ? n : 0;
}

// Map a raw Sheet row into the daily shape the UI expects.
function mapSheetRow(r) {
  return {
    date: r.date,
    googleSpend: num(r.google_spend),
    googleClicks: num(r.google_clicks),
    googleLeads: num(r.google_leads),
    metaSpend: num(r.meta_spend),
    metaClicks: num(r.meta_link_clicks),
    metaLeads: num(r.meta_messaging_leads),
  };
}

export async function getDashboardData() {
  const url = process.env.SHEET_CSV_URL;
  if (!url) return seed;

  try {
    const res = await fetch(url, { next: { revalidate: 1800 } });
    if (!res.ok) throw new Error(`Sheet fetch ${res.status}`);
    const rows = parseCsv(await res.text());
    const daily = rows.filter((r) => r.date).map(mapSheetRow);
    if (!daily.length) return seed;
    // Keep the seed's analysis/summary/campaign blocks; refresh the daily trend
    // from the live Sheet so the chart always reflects the newest rows.
    return { ...seed, daily: daily.slice(-14), liveSource: "google-sheet" };
  } catch (e) {
    return { ...seed, sheetError: String(e) };
  }
}
