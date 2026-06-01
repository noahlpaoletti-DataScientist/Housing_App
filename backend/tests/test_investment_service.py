from app.services.investment_service import analyze_investment


class DummySession:
    def add(self, _):
        return None

    def commit(self):
        return None


def test_investment_analysis_formulas():
    result = analyze_investment(
        DummySession(),
        {
            "purchase_price": 300000,
            "down_payment_percent": 0.2,
            "loan_interest_rate": 0.07,
            "loan_term_years": 30,
            "renovation_budget": 25000,
            "expected_monthly_rent": 2500,
            "annual_property_taxes": 3600,
            "annual_insurance": 1200,
            "monthly_maintenance": 150,
            "holding_period_months": 24,
            "selling_cost_percent": 0.07,
            "expected_appreciation_rate": 0.04,
        },
    )
    assert result["monthly_payment"] > 0
    assert "cap_rate" in result
