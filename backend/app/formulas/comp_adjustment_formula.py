from __future__ import annotations

from datetime import date

import numpy as np


def adjust_comparable(subject: dict, comp: dict) -> dict:
    price_per_sqft_adjustment = (subject["square_feet"] - comp["square_feet"]) * (
        subject["local_price_per_sqft"] * 0.30
    )
    bedroom_adjustment = (subject["bedrooms"] - comp["bedrooms"]) * 7_500
    bathroom_adjustment = (subject["bathrooms"] - comp["bathrooms"]) * 5_000
    lot_size_adjustment = (subject["lot_size_sqft"] - comp["lot_size_sqft"]) * 1.5
    age_adjustment = (comp["year_built"] - subject["year_built"]) * 1_200

    sale_date = date.fromisoformat(str(comp["sale_date"]))
    days_since_sale = max((date.today() - sale_date).days, 1)
    market_time_adjustment = comp["sale_price"] * subject["annual_market_growth_rate"] * (
        days_since_sale / 365
    )

    adjusted_value = (
        comp["sale_price"]
        + price_per_sqft_adjustment
        + bedroom_adjustment
        + bathroom_adjustment
        + lot_size_adjustment
        + age_adjustment
        + market_time_adjustment
    )

    recency_score = max(0.1, 1 - (days_since_sale / 730))
    distance_score = max(0.1, 1 - (comp["distance_miles"] / 5))
    sqft_score = max(0.1, 1 - abs(subject["square_feet"] - comp["square_feet"]) / subject["square_feet"])
    type_score = 1.0 if subject["property_type"] == comp["property_type"] else 0.6
    bed_bath_score = max(
        0.1,
        1
        - (
            abs(subject["bedrooms"] - comp["bedrooms"]) * 0.08
            + abs(subject["bathrooms"] - comp["bathrooms"]) * 0.06
        ),
    )
    year_score = max(0.1, 1 - abs(subject["year_built"] - comp["year_built"]) / 80)
    lot_score = max(0.1, 1 - abs(subject["lot_size_sqft"] - comp["lot_size_sqft"]) / 10_000)

    similarity_score = round(
        np.average(
            [distance_score, recency_score, sqft_score, type_score, bed_bath_score, year_score, lot_score],
            weights=[0.2, 0.2, 0.18, 0.1, 0.12, 0.1, 0.1],
        )
        * 100,
        2,
    )

    return {
        **comp,
        "adjustments": {
            "price_per_sqft_adjustment": round(price_per_sqft_adjustment, 2),
            "bedroom_adjustment": round(bedroom_adjustment, 2),
            "bathroom_adjustment": round(bathroom_adjustment, 2),
            "lot_size_adjustment": round(lot_size_adjustment, 2),
            "age_adjustment": round(age_adjustment, 2),
            "market_time_adjustment": round(market_time_adjustment, 2),
        },
        "adjusted_value": round(adjusted_value, 2),
        "similarity_score": similarity_score,
    }


def aggregate_comparable_value(adjusted_comps: list[dict]) -> float | None:
    if not adjusted_comps:
        return None

    weights = [
        max(0.01, comp["similarity_score"] / 100) * max(0.01, 1 / max(comp["distance_miles"], 0.1))
        for comp in adjusted_comps
    ]
    values = [comp["adjusted_value"] for comp in adjusted_comps]
    return round(float(np.average(values, weights=weights)), 2)
