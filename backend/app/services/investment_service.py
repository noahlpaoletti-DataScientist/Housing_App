from __future__ import annotations

from math import pow

from sqlalchemy.orm import Session

from app.db.models import InvestmentScenario


def _monthly_payment(loan_amount: float, annual_interest_rate: float, loan_term_years: int) -> float:
    monthly_rate = annual_interest_rate / 12
    payments = loan_term_years * 12
    if monthly_rate == 0:
        return loan_amount / payments
    return loan_amount * (monthly_rate * pow(1 + monthly_rate, payments)) / (
        pow(1 + monthly_rate, payments) - 1
    )


def analyze_investment(
    db: Session, inputs: dict, property_id: int | None = None, persist: bool = False
) -> dict:
    purchase_price = inputs["purchase_price"]
    down_payment_percent = inputs["down_payment_percent"]
    renovation_budget = inputs["renovation_budget"]
    loan_amount = purchase_price * (1 - down_payment_percent)
    monthly_payment = _monthly_payment(
        loan_amount,
        inputs["loan_interest_rate"],
        int(inputs["loan_term_years"]),
    )

    monthly_operating_costs = (
        inputs["annual_property_taxes"] / 12
        + inputs["annual_insurance"] / 12
        + inputs["monthly_maintenance"]
    )
    monthly_cash_flow = inputs["expected_monthly_rent"] - monthly_payment - monthly_operating_costs
    annual_cash_flow = monthly_cash_flow * 12

    total_project_cost = purchase_price + renovation_budget
    noi = (inputs["expected_monthly_rent"] * 12) - (monthly_operating_costs * 12)
    cap_rate = (noi / total_project_cost) * 100 if total_project_cost else 0
    cash_invested = purchase_price * down_payment_percent + renovation_budget
    cash_on_cash_return = (annual_cash_flow / cash_invested) * 100 if cash_invested else 0

    resale_value = purchase_price * ((1 + inputs["expected_appreciation_rate"]) ** (inputs["holding_period_months"] / 12))
    selling_costs = resale_value * inputs["selling_cost_percent"]
    estimated_flip_profit = resale_value - selling_costs - total_project_cost
    break_even_price = total_project_cost / (1 - inputs["selling_cost_percent"])

    result = {
        "monthly_payment": round(monthly_payment, 2),
        "monthly_cash_flow": round(monthly_cash_flow, 2),
        "annual_cash_flow": round(annual_cash_flow, 2),
        "cap_rate": round(cap_rate, 2),
        "cash_on_cash_return": round(cash_on_cash_return, 2),
        "estimated_resale_value": round(resale_value, 2),
        "total_project_cost": round(total_project_cost, 2),
        "estimated_flip_profit": round(estimated_flip_profit, 2),
        "break_even_price": round(break_even_price, 2),
    }

    if persist:
        scenario = InvestmentScenario(
            property_id=property_id,
            scenario_name="default-analysis",
            purchase_price=purchase_price,
            total_project_cost=result["total_project_cost"],
            monthly_cash_flow=result["monthly_cash_flow"],
            cap_rate=result["cap_rate"],
            cash_on_cash_return=result["cash_on_cash_return"],
            estimated_flip_profit=result["estimated_flip_profit"],
        )
        db.add(scenario)
        db.commit()

    return result
