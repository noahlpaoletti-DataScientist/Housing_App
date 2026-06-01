export default function PropertySummary({ property }) {
  if (!property) {
    return null;
  }

  const items = [
    ["Address", property.address],
    ["Type", property.property_type?.replace("_", " ")],
    ["Beds / Baths", `${property.bedrooms} / ${property.bathrooms}`],
    ["Size", `${property.square_feet?.toLocaleString()} sqft`],
    ["Lot", `${property.lot_size_sqft?.toLocaleString()} sqft`],
    ["Built", property.year_built],
  ];

  return (
    <section className="card">
      <div className="section-heading">
        <h2>Property facts</h2>
        <p>{property.city}, {property.state} {property.zip_code}</p>
      </div>
      <div className="stats-grid">
        {items.map(([label, value]) => (
          <div key={label} className="stat-card">
            <span>{label}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>
    </section>
  );
}
