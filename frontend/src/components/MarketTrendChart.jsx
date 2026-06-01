export default function MarketTrendChart({ trend }) {
  if (!trend?.zip_code) {
    return null;
  }

  return (
    <section className="card">
      <div className="section-heading">
        <h2>Market trend snapshot</h2>
        <p>{trend.trend_summary}</p>
      </div>
      <div className="trend-grid">
        <div>
          <span>Annual growth</span>
          <div className="trend-bar">
            <div style={{ width: `${trend.annual_growth_rate * 900}%` }} />
          </div>
          <strong>{(trend.annual_growth_rate * 100).toFixed(1)}%</strong>
        </div>
        <div>
          <span>6-month trend</span>
          <div className="trend-bar">
            <div style={{ width: `${trend.six_month_trend * 1800}%` }} />
          </div>
          <strong>{(trend.six_month_trend * 100).toFixed(1)}%</strong>
        </div>
        <div>
          <span>Days on market</span>
          <strong>{trend.average_days_on_market}</strong>
        </div>
        <div>
          <span>Inventory index</span>
          <strong>{trend.inventory_index}</strong>
        </div>
      </div>
    </section>
  );
}
