function formatCurrency(value) {
  return typeof value === "number"
    ? value.toLocaleString("en-US", { style: "currency", currency: "USD", maximumFractionDigits: 0 })
    : "N/A";
}

export default function ValueEstimateCard({ estimatedValue, lowEstimate, highEstimate }) {
  return (
    <section className="hero-card">
      <div>
        <span className="eyebrow">Explainable valuation</span>
        <h1>{formatCurrency(estimatedValue)}</h1>
        <p>Range: {formatCurrency(lowEstimate)} to {formatCurrency(highEstimate)}</p>
      </div>
      <div className="mini-grid">
        <div>
          <span>Low</span>
          <strong>{formatCurrency(lowEstimate)}</strong>
        </div>
        <div>
          <span>High</span>
          <strong>{formatCurrency(highEstimate)}</strong>
        </div>
      </div>
    </section>
  );
}
