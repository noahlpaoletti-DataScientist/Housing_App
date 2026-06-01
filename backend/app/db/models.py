from __future__ import annotations

from datetime import date, datetime

from sqlalchemy import Boolean, Date, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(255))


class Property(TimestampMixin, Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    address: Mapped[str] = mapped_column(String(255))
    normalized_address: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    city: Mapped[str] = mapped_column(String(120))
    state: Mapped[str] = mapped_column(String(2))
    zip_code: Mapped[str] = mapped_column(String(10), index=True)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    square_feet: Mapped[int] = mapped_column(Integer)
    bedrooms: Mapped[int] = mapped_column(Integer)
    bathrooms: Mapped[float] = mapped_column(Float)
    lot_size_sqft: Mapped[int] = mapped_column(Integer)
    year_built: Mapped[int] = mapped_column(Integer)
    property_type: Mapped[str] = mapped_column(String(50))
    assessed_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    last_sale_price: Mapped[float | None] = mapped_column(Float, nullable=True)
    last_sale_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    local_price_per_sqft: Mapped[float | None] = mapped_column(Float, nullable=True)
    annual_market_growth_rate: Mapped[float | None] = mapped_column(Float, nullable=True)

    features: Mapped[list[PropertyFeature]] = relationship(back_populates="property")
    valuations: Mapped[list[PropertyValuation]] = relationship(back_populates="property")


class PropertyFeature(TimestampMixin, Base):
    __tablename__ = "property_features"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    feature_name: Mapped[str] = mapped_column(String(100))
    feature_value: Mapped[str] = mapped_column(String(255))

    property: Mapped[Property] = relationship(back_populates="features")


class PropertyValuation(TimestampMixin, Base):
    __tablename__ = "property_valuations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    estimated_value: Mapped[float] = mapped_column(Float)
    low_estimate: Mapped[float] = mapped_column(Float)
    high_estimate: Mapped[float] = mapped_column(Float)
    confidence_score: Mapped[float] = mapped_column(Float)
    formula_explanation: Mapped[str] = mapped_column(Text)

    property: Mapped[Property] = relationship(back_populates="valuations")
    components: Mapped[list[ValuationComponent]] = relationship(back_populates="valuation")


class ValuationComponent(TimestampMixin, Base):
    __tablename__ = "valuation_components"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    valuation_id: Mapped[int] = mapped_column(ForeignKey("property_valuations.id"))
    component_name: Mapped[str] = mapped_column(String(100))
    component_value: Mapped[float] = mapped_column(Float)
    component_weight: Mapped[float] = mapped_column(Float)
    weighted_value: Mapped[float] = mapped_column(Float)
    explanation: Mapped[str] = mapped_column(Text)

    valuation: Mapped[PropertyValuation] = relationship(back_populates="components")


class ComparableSale(TimestampMixin, Base):
    __tablename__ = "comparable_sales"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"), index=True)
    address: Mapped[str] = mapped_column(String(255))
    sale_price: Mapped[float] = mapped_column(Float)
    sale_date: Mapped[date] = mapped_column(Date)
    square_feet: Mapped[int] = mapped_column(Integer)
    bedrooms: Mapped[int] = mapped_column(Integer)
    bathrooms: Mapped[float] = mapped_column(Float)
    lot_size_sqft: Mapped[int] = mapped_column(Integer)
    year_built: Mapped[int] = mapped_column(Integer)
    property_type: Mapped[str] = mapped_column(String(50))
    distance_miles: Mapped[float] = mapped_column(Float)
    adjusted_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    similarity_score: Mapped[float | None] = mapped_column(Float, nullable=True)


class RenovationEstimate(TimestampMixin, Base):
    __tablename__ = "renovation_estimates"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_id: Mapped[int | None] = mapped_column(ForeignKey("properties.id"), nullable=True)
    renovation_type: Mapped[str] = mapped_column(String(100))
    total_cost: Mapped[float] = mapped_column(Float)
    value_added: Mapped[float] = mapped_column(Float)
    roi_percent: Mapped[float] = mapped_column(Float)
    assumptions_json: Mapped[str] = mapped_column(Text)


class RenovationComponent(TimestampMixin, Base):
    __tablename__ = "renovation_components"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    estimate_id: Mapped[int] = mapped_column(ForeignKey("renovation_estimates.id"))
    component_name: Mapped[str] = mapped_column(String(100))
    component_cost: Mapped[float] = mapped_column(Float)
    explanation: Mapped[str] = mapped_column(Text)


class MarketTrend(TimestampMixin, Base):
    __tablename__ = "market_trends"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    zip_code: Mapped[str] = mapped_column(String(10), index=True)
    annual_growth_rate: Mapped[float] = mapped_column(Float)
    six_month_trend: Mapped[float] = mapped_column(Float)
    average_days_on_market: Mapped[int] = mapped_column(Integer)
    inventory_index: Mapped[float] = mapped_column(Float)
    trend_summary: Mapped[str] = mapped_column(Text)


class InvestmentScenario(TimestampMixin, Base):
    __tablename__ = "investment_scenarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_id: Mapped[int | None] = mapped_column(ForeignKey("properties.id"), nullable=True)
    scenario_name: Mapped[str] = mapped_column(String(120))
    purchase_price: Mapped[float] = mapped_column(Float)
    total_project_cost: Mapped[float] = mapped_column(Float)
    monthly_cash_flow: Mapped[float] = mapped_column(Float)
    cap_rate: Mapped[float] = mapped_column(Float)
    cash_on_cash_return: Mapped[float] = mapped_column(Float)
    estimated_flip_profit: Mapped[float] = mapped_column(Float)


class DataSource(TimestampMixin, Base):
    __tablename__ = "data_sources"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True)
    source_type: Mapped[str] = mapped_column(String(50))
    status: Mapped[str] = mapped_column(String(50))
    provenance_url: Mapped[str] = mapped_column(String(255))
    last_updated_label: Mapped[str] = mapped_column(String(120))


class LookupHistory(TimestampMixin, Base):
    __tablename__ = "lookup_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    input_address: Mapped[str] = mapped_column(String(255))
    normalized_address: Mapped[str] = mapped_column(String(255))
    property_id: Mapped[int | None] = mapped_column(ForeignKey("properties.id"), nullable=True)
    matched: Mapped[bool] = mapped_column(Boolean, default=False)


class ModelPrediction(TimestampMixin, Base):
    __tablename__ = "model_predictions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    model_name: Mapped[str] = mapped_column(String(120))
    prediction_value: Mapped[float] = mapped_column(Float)
    confidence_score: Mapped[float] = mapped_column(Float)


class SavedProperty(TimestampMixin, Base):
    __tablename__ = "saved_properties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    property_id: Mapped[int] = mapped_column(ForeignKey("properties.id"))
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
