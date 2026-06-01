from __future__ import annotations

from datetime import date

from sqlalchemy.orm import Session

from app.db.models import Property
from app.formulas.valuation_formula import calculate_valuation
from app.services.comparable_service import get_adjusted_comparables
from app.services.market_service import get_market_trend, serialize_market_trend
from app.services.property_lookup_service import serialize_property
from app.services.scoring_service import score_estimate


def _last_sale_adjusted(property_record: Property) -> float | None:
    if property_record.last_sale_price is None or property_record.last_sale_date is None:
        return None
    years_since_sale = max((date.today() - property_record.last_sale_date).days / 365, 0)
    growth_rate = property_record.annual_market_growth_rate or 0
    return round(property_record.last_sale_price * ((1 + growth_rate) ** years_since_sale), 2)


def build_property_valuation(db: Session, property_record: Property) -> dict:
    comparable_payload = get_adjusted_comparables(db, property_record)
    comparables = comparable_payload["comparables"]
    comparable_value = comparable_payload["comparable_value"]

    market_trend = serialize_market_trend(get_market_trend(db, property_record.zip_code))
    price_per_sqft_value = (
        round(property_record.square_feet * property_record.local_price_per_sqft, 2)
        if property_record.local_price_per_sqft is not None
        else None
    )
    assessed_value = property_record.assessed_value
    last_sale_adjusted = _last_sale_adjusted(property_record)

    base_for_market_adjustment = comparable_value or price_per_sqft_value or assessed_value or 0
    market_trend_adjustment = round(base_for_market_adjustment * market_trend["six_month_trend"] * 0.12, 2)

    valuation_result = calculate_valuation(
        values={
            "comparable_sales": comparable_value,
            "price_per_sqft": price_per_sqft_value,
            "assessed_value": assessed_value,
            "last_sale_adjusted": last_sale_adjusted,
        },
        market_trend_adjustment=market_trend_adjustment,
        renovation_value_added=0.0,
    )

    confidence = score_estimate(serialize_property(property_record), comparables, market_trend)
    confidence_score = confidence["score"]

    spread = max(0.04, (100 - confidence_score) / 200)
    low_estimate = round(valuation_result["estimated_value"] * (1 - spread), 2)
    high_estimate = round(valuation_result["estimated_value"] * (1 + spread), 2)

    return {
        "property_id": property_record.id,
        "estimated_value": valuation_result["estimated_value"],
        "low_estimate": low_estimate,
        "high_estimate": high_estimate,
        "confidence_score": confidence_score,
        "confidence_explanation": confidence["explanation"],
        "formula_explanation": valuation_result["formula_explanation"],
        "valuation_breakdown": valuation_result["adjusted_weights"],
        "components": valuation_result["components"],
        "comparable_sales": comparables,
        "market_trends": market_trend,
        "data_sources_used": [
            "Mock Property Registry",
            "Mock Comparable Sales",
            "Mock Market Trends",
        ],
    }


def get_latest_valuation(db: Session, property_record: Property) -> dict:
    return build_property_valuation(db, property_record)
