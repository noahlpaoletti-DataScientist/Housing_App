from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import MarketTrend


def get_market_trend(db: Session, zip_code: str) -> MarketTrend | None:
    return db.query(MarketTrend).filter(MarketTrend.zip_code == zip_code).one_or_none()


def serialize_market_trend(trend: MarketTrend | None) -> dict:
    if trend is None:
        return {
            "zip_code": None,
            "annual_growth_rate": 0,
            "six_month_trend": 0,
            "average_days_on_market": None,
            "inventory_index": None,
            "trend_summary": "No market trend data available for this ZIP code.",
        }
    return {
        "zip_code": trend.zip_code,
        "annual_growth_rate": trend.annual_growth_rate,
        "six_month_trend": trend.six_month_trend,
        "average_days_on_market": trend.average_days_on_market,
        "inventory_index": trend.inventory_index,
        "trend_summary": trend.trend_summary,
    }
