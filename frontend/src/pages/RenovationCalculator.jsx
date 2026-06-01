import RenovationEstimator from "../components/RenovationEstimator";

export default function RenovationCalculator() {
  return (
    <div className="stack-layout">
      <section className="card">
        <span className="eyebrow">Renovation planning</span>
        <h1>Estimate project cost and value lift.</h1>
        <p>
          This calculator supports remodel and construction scenarios with visible materials, labor,
          overhead, contingency, and ROI assumptions.
        </p>
      </section>
      <RenovationEstimator />
    </div>
  );
}
