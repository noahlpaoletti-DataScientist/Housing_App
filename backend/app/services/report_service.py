from __future__ import annotations

from sqlalchemy.orm import Session

from app.services.investment_service import analyze_investment
from app.services.property_lookup_service import serialize_property
from app.services.renovation_service import create_renovation_estimate
from app.services.valuation_service import build_property_valuation


def build_property_report(db: Session, property_record) -> dict:
    valuation = build_property_valuation(db, property_record)

    kitchen = create_renovation_estimate(
        db,
        "kitchen",
        {"kitchen_square_feet": 180, "cabinet_linear_feet": 24},
        property_id=property_record.id,
    )
    bathroom = create_renovation_estimate(
        db,
        "bathroom",
        {"bathroom_square_feet": 72, "fixture_count": 5},
        property_id=property_record.id,
    )
    investment = analyze_investment(
        db,
        {
            "purchase_price": valuation["estimated_value"] * 0.94,
            "down_payment_percent": 0.20,
            "loan_interest_rate": 0.068,
            "loan_term_years": 30,
            "renovation_budget": kitchen["total_cost"] * 0.4,
            "expected_monthly_rent": round(valuation["estimated_value"] * 0.0065, 2),
            "annual_property_taxes": valuation["estimated_value"] * 0.011,
            "annual_insurance": 1800,
            "monthly_maintenance": 225,
            "holding_period_months": 24,
            "selling_cost_percent": 0.07,
            "expected_appreciation_rate": property_record.annual_market_growth_rate or 0.04,
        },
        property_id=property_record.id,
    )

    return {
        "input_address": property_record.address,
        "matched_property": serialize_property(property_record),
        "estimated_value": valuation["estimated_value"],
        "low_estimate": valuation["low_estimate"],
        "high_estimate": valuation["high_estimate"],
        "confidence_score": valuation["confidence_score"],
        "confidence_explanation": valuation["confidence_explanation"],
        "valuation_breakdown": valuation["valuation_breakdown"],
        "formula_explanation": valuation["formula_explanation"],
        "comparable_sales": valuation["comparable_sales"],
        "renovation_scenarios": [kitchen, bathroom],
        "investment_summary": investment,
        "market_trends": valuation["market_trends"],
        "data_sources_used": valuation["data_sources_used"],
        "valuation_components": valuation["components"],
    }
