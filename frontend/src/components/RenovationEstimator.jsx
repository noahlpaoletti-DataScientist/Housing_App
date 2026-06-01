import { useState } from "react";
import { estimateRenovation } from "../api/client";

const defaults = {
  kitchen_square_feet: 180,
  bathroom_square_feet: 75,
  building_square_feet: 2400,
  cabinet_linear_feet: 24,
  fixture_count: 5,
  quantity: 1,
  labor_hours: 40,
  permit_cost: 850,
  disposal_cost: 500,
};

export default function RenovationEstimator({ onResult }) {
  const [renovationType, setRenovationType] = useState("kitchen");
  const [inputs, setInputs] = useState(defaults);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  function updateField(name, value) {
    setInputs((current) => ({ ...current, [name]: Number(value) }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    try {
      const payload = { renovation_type: renovationType, inputs };
      const response = await estimateRenovation(payload);
      setResult(response);
      onResult?.(response);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="card">
      <div className="section-heading">
        <h2>Renovation estimator</h2>
        <p>Run kitchen, bathroom, generic repair, or new-build scenarios with auditable cost components.</p>
      </div>
      <form className="stack-form" onSubmit={handleSubmit}>
        <label>
          Renovation type
          <select value={renovationType} onChange={(event) => setRenovationType(event.target.value)}>
            <option value="kitchen">Kitchen remodel</option>
            <option value="bathroom">Bathroom remodel</option>
            <option value="roof">Roof replacement</option>
            <option value="paint">Interior paint</option>
            <option value="new_build">New construction</option>
          </select>
        </label>
        <div className="form-grid">
          <label>
            Kitchen sqft
            <input type="number" value={inputs.kitchen_square_feet} onChange={(event) => updateField("kitchen_square_feet", event.target.value)} />
          </label>
          <label>
            Bathroom sqft
            <input type="number" value={inputs.bathroom_square_feet} onChange={(event) => updateField("bathroom_square_feet", event.target.value)} />
          </label>
          <label>
            Building sqft
            <input type="number" value={inputs.building_square_feet} onChange={(event) => updateField("building_square_feet", event.target.value)} />
          </label>
          <label>
            Cabinet feet
            <input type="number" value={inputs.cabinet_linear_feet} onChange={(event) => updateField("cabinet_linear_feet", event.target.value)} />
          </label>
          <label>
            Fixture count
            <input type="number" value={inputs.fixture_count} onChange={(event) => updateField("fixture_count", event.target.value)} />
          </label>
          <label>
            Labor hours
            <input type="number" value={inputs.labor_hours} onChange={(event) => updateField("labor_hours", event.target.value)} />
          </label>
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Estimating..." : "Estimate renovation"}
        </button>
      </form>

      {result && (
        <div className="results-grid">
          <div className="stat-card">
            <span>Total cost</span>
            <strong>${result.total_cost.toLocaleString()}</strong>
          </div>
          <div className="stat-card">
            <span>Value added</span>
            <strong>${result.value_added.toLocaleString()}</strong>
          </div>
          <div className="stat-card">
            <span>ROI</span>
            <strong>{result.roi_percent}%</strong>
          </div>
        </div>
      )}
    </section>
  );
}
