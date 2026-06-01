function formatCurrency(value) {
  return value.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  });
}

export default function RenovationScenarios({ scenarios = [] }) {
  if (!scenarios.length) {
    return null;
  }

  return (
    <section className="card">
      <div className="section-heading">
        <h2>Renovation scenarios</h2>
        <p>Sample value-add scenarios generated alongside the valuation report.</p>
      </div>
      <div className="stats-grid">
        {scenarios.map((scenario) => (
          <div className="stat-card" key={`${scenario.renovation_type}-${scenario.total_cost}`}>
            <span>{scenario.renovation_type.replaceAll("_", " ")}</span>
            <strong>{formatCurrency(scenario.total_cost)}</strong>
            <span>Value add: {formatCurrency(scenario.value_added)}</span>
            <span>ROI: {scenario.roi_percent}%</span>
          </div>
        ))}
      </div>
    </section>
  );
}
