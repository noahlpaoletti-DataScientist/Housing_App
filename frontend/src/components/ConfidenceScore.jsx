export default function ConfidenceScore({ score, explanation }) {
  if (score == null) {
    return null;
  }

  return (
    <section className="card confidence-card">
      <div>
        <span className="eyebrow">Confidence score</span>
        <h2>{score}/100</h2>
        <p>{explanation}</p>
      </div>
      <div className="confidence-meter">
        <div className="confidence-fill" style={{ width: `${score}%` }} />
      </div>
    </section>
  );
}
