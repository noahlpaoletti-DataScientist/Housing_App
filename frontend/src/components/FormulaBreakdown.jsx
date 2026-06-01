function formatCurrency(value) {
  return value.toLocaleString("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  });
}

export default function FormulaBreakdown({ components = [], weights = {}, explanation = "" }) {
  return (
    <section className="card">
      <div className="section-heading">
        <h2>Formula breakdown</h2>
        <p>{explanation}</p>
      </div>
      <div className="table-wrap">
        <table>
          <thead>
            <tr>
              <th>Signal</th>
              <th>Raw value</th>
              <th>Weight</th>
              <th>Weighted impact</th>
            </tr>
          </thead>
          <tbody>
            {components.map((component) => (
              <tr key={component.component_name}>
                <td>{component.component_name.replaceAll("_", " ")}</td>
                <td>{formatCurrency(component.component_value)}</td>
                <td>{Math.round((weights[component.component_name] || component.component_weight) * 100)}%</td>
                <td>{formatCurrency(component.weighted_value)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
