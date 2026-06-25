import { getDashboardData } from "@/lib/data";
import TrendChart from "@/components/TrendChart";

export const dynamic = "force-dynamic";

function money(n, c = "CAD") {
  if (n == null) return "—";
  return new Intl.NumberFormat("en-CA", { style: "currency", currency: c, maximumFractionDigits: 0 }).format(n);
}
function money2(n, c = "CAD") {
  if (n == null) return "—";
  return new Intl.NumberFormat("en-CA", { style: "currency", currency: c, minimumFractionDigits: 2 }).format(n);
}

function Delta({ current, prior, goodIsUp = true }) {
  if (prior == null || prior === 0) return <span className="delta flat">—</span>;
  const pct = ((current - prior) / Math.abs(prior)) * 100;
  const up = pct >= 0;
  const good = goodIsUp ? up : !up;
  const cls = Math.abs(pct) < 0.5 ? "flat" : good ? "up" : "down";
  const arrow = Math.abs(pct) < 0.5 ? "→" : up ? "▲" : "▼";
  return (
    <span className={`delta ${cls}`}>
      {arrow} {Math.abs(pct).toFixed(0)}%
    </span>
  );
}

export default async function Page() {
  const data = await getDashboardData();
  const c = data.currency;
  const s = data.summary;
  const live = data.liveSource === "google-sheet";

  return (
    <main className="wrap">
      <div className="topbar">
        <div className="brand">
          <h1>{data.client}</h1>
          <span className="by">Ads Performance · by PPC Guru</span>
        </div>
        <div style={{ textAlign: "right" }}>
          <span className={`pill ${live ? "live" : "seed"}`}>
            {live ? "Live · Google Sheet" : "Seeded snapshot"}
          </span>
          <div className="meta-line">
            Updated {data.lastUpdated} · {s.combined.spend.current && money(s.combined.spend.current, c)} spend ·{" "}
            {data.periods.current.label}
          </div>
        </div>
      </div>

      {/* Headline KPIs — optimizing for LEAD VOLUME */}
      <div className="grid kpis">
        <div className="card hero kpi">
          <div className="label">Total Leads <span className="tag">(both platforms)</span></div>
          <div className="value">
            {s.combined.leads.current}
            <Delta current={s.combined.leads.current} prior={s.combined.leads.prior} goodIsUp />
          </div>
          <div className="sub">vs {s.combined.leads.prior} prior 30 days</div>
        </div>
        <div className="card kpi">
          <div className="label">Blended Cost / Lead</div>
          <div className="value">
            {money(s.combined.costPerLead.current, c)}
            <Delta current={s.combined.costPerLead.current} prior={s.combined.costPerLead.prior} goodIsUp={false} />
          </div>
          <div className="sub">total spend ÷ total leads</div>
        </div>
        <div className="card kpi">
          <div className="label">Meta Leads <span className="tag">(Messenger)</span></div>
          <div className="value">
            {s.meta.leads.current}
            <Delta current={s.meta.leads.current} prior={s.meta.leads.prior} goodIsUp />
          </div>
          <div className="sub">{money2(s.meta.costPerLead.current, c)} / lead</div>
        </div>
        <div className="card kpi">
          <div className="label">Google Leads <span className="tag">(calls + conv.)</span></div>
          <div className="value">
            {s.google.leads.current}
            <Delta current={s.google.leads.current} prior={s.google.leads.prior} goodIsUp />
          </div>
          <div className="sub">{s.google.conversions.current} conv · {s.google.phoneCalls.current} calls</div>
        </div>
      </div>

      {/* Daily trend */}
      <div className="section-title">Daily trend · last 14 days</div>
      <div className="card">
        <div className="chart-head">
          <h3>Leads &amp; spend per day</h3>
          <div className="legend">
            <span><i className="dot" style={{ background: "#4f8cff" }} /> Leads</span>
            <span><i className="dot" style={{ background: "#34d399" }} /> Spend</span>
          </div>
        </div>
        <TrendChart daily={data.daily} currency={c} />
      </div>

      {/* Platform breakdown */}
      <div className="section-title">Platform breakdown · {data.periods.current.label}</div>
      <div className="grid cols-2">
        <div className="card">
          <div className="chart-head"><h3>🔵 Google Ads</h3><span className="tag">{money(s.google.spend.current, c)}</span></div>
          <table>
            <tbody>
              <Row k="Leads" v={s.google.leads.current} />
              <Row k="Conversions" v={s.google.conversions.current} />
              <Row k="Phone calls" v={s.google.phoneCalls.current} />
              <Row k="Clicks" v={s.google.clicks.current} />
              <Row k="Impressions" v={s.google.impressions.current.toLocaleString()} />
              <Row k="Cost / lead" v={money2(s.google.costPerLead.current, c)} />
            </tbody>
          </table>
        </div>
        <div className="card">
          <div className="chart-head"><h3>🟠 Meta Ads</h3><span className="tag">{money(s.meta.spend.current, c)}</span></div>
          <table>
            <tbody>
              <Row k="Leads (Messenger)" v={s.meta.leads.current} />
              <Row k="Link clicks" v={s.meta.linkClicks.current} />
              <Row k="Impressions" v={s.meta.impressions.current.toLocaleString()} />
              <Row k="Reach" v={s.meta.reach.current.toLocaleString()} />
              <Row k="Cost / lead" v={money2(s.meta.costPerLead.current, c)} />
            </tbody>
          </table>
        </div>
      </div>

      {/* Campaign tables */}
      <div className="section-title">Google campaigns</div>
      <div className="card">
        <table>
          <thead>
            <tr><th>Campaign</th><th>Spend</th><th>Clicks</th><th>CTR</th><th>Conv.</th><th>CPA</th><th>Impr. share</th><th>Lost (budget)</th></tr>
          </thead>
          <tbody>
            {data.campaigns.google.map((g) => (
              <tr key={g.name}>
                <td>{g.name}<div className="tag">{g.type} · {money(g.dailyBudget, c)}/day</div></td>
                <td>{money2(g.spend, c)}</td>
                <td>{g.clicks}</td>
                <td>{g.ctr}%</td>
                <td>{g.conversions}</td>
                <td>{money(g.cpa, c)}</td>
                <td>{g.impressionShare}%</td>
                <td>{g.budgetLostIS}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="section-title">Meta campaigns</div>
      <div className="card">
        <table>
          <thead>
            <tr><th>Campaign</th><th>Spend</th><th>Link clicks</th><th>Link CTR</th><th>CPM</th><th>Leads</th><th>Cost / lead</th></tr>
          </thead>
          <tbody>
            {data.campaigns.meta.map((m) => (
              <tr key={m.name}>
                <td>{m.name}</td>
                <td>{money2(m.spend, c)}</td>
                <td>{m.linkClicks}</td>
                <td>{m.linkCtr}%</td>
                <td>{money2(m.cpm, c)}</td>
                <td>{m.leads}</td>
                <td>{m.costPerLead == null ? "—" : money2(m.costPerLead, c)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Auto insights */}
      <div className="section-title">Today's actionable insights</div>
      <div className="card">
        {data.insights.map((it, i) => (
          <div className="insight" key={i}>
            <div className={`sev ${it.severity}`} />
            <div>
              <div className={`sev-label ${it.severity}`}>{it.severity} priority</div>
              <h4>{it.title}</h4>
              <p>{it.detail}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="foot">
        Data source: {live ? "live Google Sheet" : "seeded snapshot"} · pulled via Adzviser (Google &amp; Meta).{" "}
        Data store:{" "}
        <a href={data.sheet.url} target="_blank" rel="noreferrer">Google Sheet ↗</a>.<br />
        To go fully live, publish the Sheet to web as CSV and set <code>SHEET_CSV_URL</code> in Vercel. A daily job appends one row per day.
        {data.sheetError && <div style={{ color: "var(--bad)", marginTop: 8 }}>Sheet read fell back to seed: {data.sheetError}</div>}
      </div>
    </main>
  );
}

function Row({ k, v }) {
  return (
    <tr>
      <td>{k}</td>
      <td>{v}</td>
    </tr>
  );
}
