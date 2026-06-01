import { useNavigate } from "react-router-dom";
import AddressSearch from "../components/AddressSearch";

export default function Home() {
  const navigate = useNavigate();

  function handleSearch(address) {
    navigate(`/report?address=${encodeURIComponent(address)}`);
  }

  return (
    <div className="stack-layout">
      <section className="landing-hero">
        <div>
          <span className="eyebrow">Transparent real estate intelligence</span>
          <h1>Understand what a property might be worth and why.</h1>
          <p>
            PropLens combines address lookup, valuation formulas, comparable logic, renovation ROI,
            investor analysis, and confidence scoring into one explainable report.
          </p>
        </div>
        <AddressSearch onSearch={handleSearch} />
      </section>

      <section className="feature-grid">
        <article className="feature-card">
          <h2>Explainable valuation</h2>
          <p>Every estimate includes source weights, formula components, and plain-English reasoning.</p>
        </article>
        <article className="feature-card">
          <h2>Renovation ROI</h2>
          <p>Estimate kitchen, bathroom, roof, paint, or new-build scenarios with visible assumptions.</p>
        </article>
        <article className="feature-card">
          <h2>Investor workflow</h2>
          <p>Model cash flow, cap rate, cash-on-cash return, resale value, and break-even targets.</p>
        </article>
      </section>
    </div>
  );
}
