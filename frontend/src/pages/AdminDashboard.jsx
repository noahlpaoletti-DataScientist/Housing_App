import { useEffect, useState } from "react";
import { getHealth, getMarketTrend } from "../api/client";

export default function AdminDashboard() {
  const [health, setHealth] = useState(null);
  const [trend, setTrend] = useState(null);

  useEffect(() => {
    async function load() {
      const [healthPayload, trendPayload] = await Promise.all([
        getHealth(),
        getMarketTrend("28203"),
      ]);
      setHealth(healthPayload);
      setTrend(trendPayload);
    }

    load().catch(() => {
      setHealth({ status: "offline" });
    });
  }, []);

  return (
    <div className="stack-layout">
      <section className="card">
        <span className="eyebrow">System overview</span>
        <h1>MVP admin dashboard</h1>
        <p>
          This view is meant for product and data operators who need a quick read on API health,
          seeded-market readiness, and connector strategy.
        </p>
      </section>

      <div className="stats-grid">
        <div className="stat-card">
          <span>API status</span>
          <strong>{health?.status || "checking"}</strong>
        </div>
        <div className="stat-card">
          <span>Primary market</span>
          <strong>{trend?.zip_code || "mock data"}</strong>
        </div>
        <div className="stat-card">
          <span>Connector mode</span>
          <strong>Mock + future public/licensed</strong>
        </div>
      </div>

      <section className="card">
        <h2>Designed connectors</h2>
        <div className="pill-row">
          <span className="pill">County parcel APIs</span>
          <span className="pill">Local assessor data</span>
          <span className="pill">Census</span>
          <span className="pill">FHFA</span>
          <span className="pill">Permit data</span>
          <span className="pill">Licensed MLS data</span>
        </div>
      </section>
    </div>
  );
}
