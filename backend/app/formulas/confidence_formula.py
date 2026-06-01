from __future__ import annotations


def calculate_confidence_score(
    data_completeness_score: float,
    comparable_quality_score: float,
    market_data_score: float,
    recency_score: float,
) -> dict[str, float | str]:
    score = (
        data_completeness_score * 0.40
        + comparable_quality_score * 0.35
        + market_data_score * 0.15
        + recency_score * 0.10
    )
    score = round(max(0.0, min(score, 100.0)), 2)

    if score >= 80:
        explanation = "High confidence because parcel data is complete and comparable support is strong."
    elif score >= 60:
        explanation = "Moderate confidence because the estimate has decent source coverage but some signals are weaker."
    else:
        explanation = "Lower confidence because the estimate relies on limited or aging comparable and market signals."

    return {"score": score, "explanation": explanation}
