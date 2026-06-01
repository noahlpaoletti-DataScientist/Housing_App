function formatCurrency(value) {
  return value.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  });
}

export default function ComparableSalesTable({ comparables = [] }) {
  return (
    <section className="card">
      <div className="section-heading">
        <h2>Comparable sales</h2>
        <p>Adjusted by square footage, bedrooms, bathrooms, lot size, age, and market timing.</p>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Address</th>
              <th>Sale price</th>
              <th>Adjusted value</th>
              <th>Distance</th>
              <th>Similarity</th>
            </tr>
          </thead>
          <tbody>
            {comparables.map((comp) => (
              <tr key={comp.id}>
                <td>{comp.address}</td>
                <td>{formatCurrency(comp.sale_price)}</td>
                <td>{formatCurrency(comp.adjusted_value)}</td>
                <td>{comp.distance_miles} mi</td>
                <td>{comp.similarity_score}%</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
