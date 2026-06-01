from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ComparableResponse(BaseModel):
    id: int
    address: str
    sale_price: float
    sale_date: str
    square_feet: int
    bedrooms: int
    bathrooms: float
    lot_size_sqft: int
    year_built: int
    property_type: str
    distance_miles: float
    adjusted_value: float
    similarity_score: float
    adjustments: dict[str, float]


class ValuationComponentResponse(BaseModel):
    component_name: str
    component_value: float
    component_weight: float
    weighted_value: float
    explanation: str


class PropertyLookupResponse(BaseModel):
    input_address: str
    matched_property: dict[str, Any] | None
    estimated_value: float | None = None
    low_estimate: float | None = None
    high_estimate: float | None = None
    confidence_score: float | None = None
    confidence_explanation: str | None = None
    valuation_breakdown: dict[str, float] = Field(default_factory=dict)
    formula_explanation: str | None = None
    comparable_sales: list[ComparableResponse] = Field(default_factory=list)
    renovation_scenarios: list[dict[str, Any]] = Field(default_factory=list)
    investment_summary: dict[str, Any] = Field(default_factory=dict)
    market_trends: dict[str, Any] = Field(default_factory=dict)
    data_sources_used: list[str] = Field(default_factory=list)
    valuation_components: list[ValuationComponentResponse] = Field(default_factory=list)


class RenovationEstimateRequest(BaseModel):
    property_id: int | None = None
    renovation_type: str
    inputs: dict[str, float] = Field(default_factory=dict)


class RenovationEstimateResponse(BaseModel):
    renovation_type: str
    total_cost: float
    value_added: float
    roi_percent: float
    value_multiplier: float
    components: dict[str, float]


class InvestmentAnalysisRequest(BaseModel):
    property_id: int | None = None
    purchase_price: float
    down_payment_percent: float
    loan_interest_rate: float
    loan_term_years: int
    renovation_budget: float
    expected_monthly_rent: float
    annual_property_taxes: float
    annual_insurance: float
    monthly_maintenance: float
    holding_period_months: int
    selling_cost_percent: float
    expected_appreciation_rate: float


class InvestmentAnalysisResponse(BaseModel):
    monthly_payment: float
    monthly_cash_flow: float
    annual_cash_flow: float
    cap_rate: float
    cash_on_cash_return: float
    estimated_resale_value: float
    total_project_cost: float
    estimated_flip_profit: float
    break_even_price: float


class MarketTrendResponse(BaseModel):
    zip_code: str | None
    annual_growth_rate: float
    six_month_trend: float
    average_days_on_market: int | None
    inventory_index: float | None
    trend_summary: str


class FormulaResponse(BaseModel):
    property_id: int
    adjusted_weights: dict[str, float]
    components: list[ValuationComponentResponse]
    formula_explanation: str


class BasicPropertyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    address: str
    city: str
    state: str
    zip_code: str
