export default function DataSourceProvenance({ sources = [] }) {
  return (
    <section className="card">
      <div className="section-heading">
        <h2>Data provenance</h2>
        <p>This MVP uses mock data and public-data connector placeholders by design.</p>
      </div>
      <div className="pill-row">
        {sources.map((source) => (
          <span key={source} className="pill">
            {source}
          </span>
        ))}
      </div>
    </section>
  );
}
