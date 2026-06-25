// Dependency-free dual-line SVG chart: total leads (bars) + total spend (line).
export default function TrendChart({ daily, currency = "CAD" }) {
  const W = 1080;
  const H = 280;
  const padL = 44;
  const padR = 48;
  const padT = 16;
  const padB = 34;
  const n = daily.length;

  const leadsArr = daily.map((d) => (d.googleLeads || 0) + (d.metaLeads || 0));
  const spendArr = daily.map((d) => (d.googleSpend || 0) + (d.metaSpend || 0));
  const maxLeads = Math.max(4, ...leadsArr);
  const maxSpend = Math.max(10, ...spendArr) * 1.15;

  const plotW = W - padL - padR;
  const plotH = H - padT - padB;
  const x = (i) => padL + (n <= 1 ? plotW / 2 : (i * plotW) / (n - 1));
  const yLeads = (v) => padT + plotH - (v / maxLeads) * plotH;
  const ySpend = (v) => padT + plotH - (v / maxSpend) * plotH;

  const barW = Math.max(6, plotW / n - 12);
  const linePts = spendArr.map((v, i) => `${x(i)},${ySpend(v)}`).join(" ");

  const fmtDate = (s) => {
    const [, m, d] = s.split("-");
    return `${parseInt(m, 10)}/${parseInt(d, 10)}`;
  };

  return (
    <svg viewBox={`0 0 ${W} ${H}`} width="100%" role="img" aria-label="Daily leads and spend trend">
      {/* gridlines */}
      {[0, 0.25, 0.5, 0.75, 1].map((t, i) => {
        const yy = padT + plotH - t * plotH;
        return (
          <g key={i}>
            <line x1={padL} y1={yy} x2={W - padR} y2={yy} stroke="#263251" strokeWidth="1" />
            <text x={padL - 8} y={yy + 4} fill="#93a0bd" fontSize="11" textAnchor="end">
              {Math.round(t * maxLeads)}
            </text>
          </g>
        );
      })}

      {/* lead bars */}
      {leadsArr.map((v, i) => (
        <rect
          key={i}
          x={x(i) - barW / 2}
          y={yLeads(v)}
          width={barW}
          height={padT + plotH - yLeads(v)}
          rx="3"
          fill="#4f8cff"
          opacity="0.85"
        />
      ))}

      {/* spend line */}
      <polyline points={linePts} fill="none" stroke="#34d399" strokeWidth="2.5" />
      {spendArr.map((v, i) => (
        <circle key={i} cx={x(i)} cy={ySpend(v)} r="3" fill="#34d399" />
      ))}

      {/* x labels */}
      {daily.map((d, i) => (
        <text key={i} x={x(i)} y={H - 12} fill="#93a0bd" fontSize="10.5" textAnchor="middle">
          {fmtDate(d.date)}
        </text>
      ))}
    </svg>
  );
}
