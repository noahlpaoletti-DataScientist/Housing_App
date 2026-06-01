function Row({ label, value, suffix = "" }) {
  return (
    <div className="stat-card">
      <span>{label}</span>
      <strong>
        {typeof value === "number" ? value.toLocaleString("en-US", { maximumFractionDigits: 2 }) : value}
        {suffix}
      </strong>
    </div>
  );
}

export default function InvestmentSummary({ summary }) {
  if (!summary || Object.keys(summary).length === 0) {
    return null;
  }

  return (
    <section className="card">
      <div className="section-heading">
        <h2>Investment summary</h2>
        <p>Rental and flip metrics derived from the current assumptions.</p>
      </div>
      <div className="stats-grid">
        <Row label="Monthly payment" value={`$${summary.monthly_payment?.toLocaleString()}`} />
        <Row label="Monthly cash flow" value={`$${summary.monthly_cash_flow?.toLocaleString()}`} />
        <Row label="Annual cash flow" value={`$${summary.annual_cash_flow?.toLocaleString()}`} />
        <Row label="Cap rate" value={summary.cap_rate} suffix="%" />
        <Row label="Cash-on-cash" value={summary.cash_on_cash_return} suffix="%" />
        <Row label="Resale value" value={`$${summary.estimated_resale_value?.toLocaleString()}`} />
        <Row label="Project cost" value={`$${summary.total_project_cost?.toLocaleString()}`} />
        <Row label="Flip profit" value={`$${summary.estimated_flip_profit?.toLocaleString()}`} />
      </div>
    </section>
  );
}
