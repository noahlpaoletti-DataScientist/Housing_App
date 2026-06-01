from app.formulas.valuation_formula import calculate_valuation


def test_calculate_valuation_returns_component_breakdown():
    result = calculate_valuation(
        {
            "comparable_sales": 435000,
            "price_per_sqft": 418000,
            "assessed_value": 390000,
            "last_sale_adjusted": 430000,
        },
        market_trend_adjustment=5000,
    )

    assert result["estimated_value"] > 400000
    assert len(result["components"]) == 4
    assert result["adjusted_weights"]["comparable_sales"] == 0.4


def test_missing_data_redistributes_weights():
    result = calculate_valuation(
        {
            "comparable_sales": 435000,
            "price_per_sqft": None,
            "assessed_value": 390000,
            "last_sale_adjusted": None,
        }
    )

    assert result["adjusted_weights"]["comparable_sales"] == 0.7273
    assert result["adjusted_weights"]["assessed_value"] == 0.2727
