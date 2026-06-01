import { useState } from "react";
import { analyzeInvestment } from "../api/client";
import InvestmentSummary from "../components/InvestmentSummary";

const defaults = {
  purchase_price: 425000,
  down_payment_percent: 0.2,
  loan_interest_rate: 0.068,
  loan_term_years: 30,
  renovation_budget: 35000,
  expected_monthly_rent: 2950,
  annual_property_taxes: 5200,
  annual_insurance: 1800,
  monthly_maintenance: 225,
  holding_period_months: 24,
  selling_cost_percent: 0.07,
  expected_appreciation_rate: 0.045,
};

export default function InvestorCalculator() {
  const [form, setForm] = useState(defaults);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  function setField(name, value) {
    setForm((current) => ({ ...current, [name]: Number(value) }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    try {
      const result = await analyzeInvestment(form);
      setSummary(result);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="stack-layout">
      <section className="card">
        <span className="eyebrow">Investor analysis</span>
        <h1>Model rental and flip economics in one pass.</h1>
      </section>

      <form className="card stack-form" onSubmit={handleSubmit}>
        <div className="form-grid">
          {Object.entries(form).map(([key, value]) => (
            <label key={key}>
              {key.replaceAll("_", " ")}
              <input type="number" step="0.01" value={value} onChange={(event) => setField(key, event.target.value)} />
            </label>
          ))}
        </div>
        <button type="submit" disabled={loading}>
          {loading ? "Analyzing..." : "Run scenario"}
        </button>
      </form>

      <InvestmentSummary summary={summary} />
    </div>
  );
}
