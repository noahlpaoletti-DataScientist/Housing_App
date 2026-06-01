from __future__ import annotations

from datetime import date

from app.formulas.confidence_formula import calculate_confidence_score


def score_estimate(property_payload: dict, comparables: list[dict], market_trend: dict) -> dict:
    key_fields = [
        "square_feet",
        "bedrooms",
        "bathrooms",
        "lot_size_sqft",
        "year_built",
        "assessed_value",
        "last_sale_price",
        "local_price_per_sqft",
        "annual_market_growth_rate",
    ]
    populated_fields = sum(1 for field in key_fields if property_payload.get(field) is not None)
    data_completeness_score = (populated_fields / len(key_fields)) * 100

    comparable_quality_score = (
        sum(comp["similarity_score"] for comp in comparables) / len(comparables) if comparables else 35
    )
    market_data_score = 100 if market_trend.get("zip_code") else 45

    if comparables:
        most_recent_sale = max(date.fromisoformat(comp["sale_date"]) for comp in comparables)
        recency_days = (date.today() - most_recent_sale).days
        recency_score = max(35, 100 - (recency_days / 6))
    else:
        recency_score = 40

    return calculate_confidence_score(
        data_completeness_score=data_completeness_score,
        comparable_quality_score=comparable_quality_score,
        market_data_score=market_data_score,
        recency_score=recency_score,
    )
