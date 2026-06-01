from app.formulas.comp_adjustment_formula import adjust_comparable


def test_adjust_comparable_returns_similarity_and_adjusted_value():
    subject = {
        "square_feet": 1800,
        "bedrooms": 3,
        "bathrooms": 2.0,
        "lot_size_sqft": 6000,
        "year_built": 1998,
        "property_type": "single_family",
        "local_price_per_sqft": 220,
        "annual_market_growth_rate": 0.05,
    }
    comp = {
        "id": 1,
        "address": "12 Main Street",
        "sale_price": 400000,
        "sale_date": "2025-01-01",
        "square_feet": 1750,
        "bedrooms": 3,
        "bathrooms": 2.0,
        "lot_size_sqft": 5900,
        "year_built": 2000,
        "property_type": "single_family",
        "distance_miles": 0.5,
    }

    result = adjust_comparable(subject, comp)

    assert result["adjusted_value"] > 400000
    assert 0 < result["similarity_score"] <= 100
