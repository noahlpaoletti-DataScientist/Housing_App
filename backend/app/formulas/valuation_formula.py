from __future__ import annotations

from typing import Any

DEFAULT_WEIGHTS = {
    "comparable_sales": 0.40,
    "price_per_sqft": 0.25,
    "assessed_value": 0.15,
    "last_sale_adjusted": 0.20,
}


def redistribute_weights(values: dict[str, float | None]) -> dict[str, float]:
    available = {key: weight for key, weight in DEFAULT_WEIGHTS.items() if values.get(key) is not None}
    if not available:
        return {key: 0.0 for key in DEFAULT_WEIGHTS}

    total = sum(available.values())
    return {
        key: round((weight / total), 4) if key in available else 0.0
        for key, weight in DEFAULT_WEIGHTS.items()
    }


def calculate_valuation(
    values: dict[str, float | None],
    market_trend_adjustment: float = 0.0,
    renovation_value_added: float = 0.0,
) -> dict[str, Any]:
    weights = redistribute_weights(values)
    components = []
    estimate = 0.0

    explanations = {
        "comparable_sales": "Derived from adjusted comparable sale prices weighted by similarity.",
        "price_per_sqft": "Computed from subject square footage multiplied by local average price per square foot.",
        "assessed_value": "Local assessed value signal included as a secondary anchor.",
        "last_sale_adjusted": "Previous sale price adjusted by annual market growth over time.",
    }

    for name, value in values.items():
        if value is None:
            continue
        weighted_value = round(value * weights[name], 2)
        estimate += weighted_value
        components.append(
            {
                "component_name": name,
                "component_value": round(value, 2),
                "component_weight": weights[name],
                "weighted_value": weighted_value,
                "explanation": explanations[name],
            }
        )

    estimate += market_trend_adjustment + renovation_value_added
    estimate = round(estimate, 2)

    if components:
        explanation_bits = [
            f"{component['component_name'].replace('_', ' ')} suggests ${component['component_value']:,.0f}"
            for component in components
        ]
        explanation = (
            f"This property is estimated at ${estimate:,.0f} because "
            + ", ".join(explanation_bits[:-1])
            + (", and " if len(explanation_bits) > 1 else "")
            + explanation_bits[-1]
            + f". Market trend adjustment contributes ${market_trend_adjustment:,.0f} and renovation value add contributes ${renovation_value_added:,.0f}."
        )
    else:
        explanation = "No valuation inputs were available."

    return {
        "estimated_value": estimate,
        "components": components,
        "adjusted_weights": weights,
        "formula_explanation": explanation,
    }
