from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import ComparableSale, Property
from app.formulas.comp_adjustment_formula import adjust_comparable, aggregate_comparable_value


def get_adjusted_comparables(db: Session, property_record: Property) -> dict:
    comp_rows = db.query(ComparableSale).filter(ComparableSale.property_id == property_record.id).all()
    subject = {
        "square_feet": property_record.square_feet,
        "bedrooms": property_record.bedrooms,
        "bathrooms": property_record.bathrooms,
        "lot_size_sqft": property_record.lot_size_sqft,
        "year_built": property_record.year_built,
        "property_type": property_record.property_type,
        "local_price_per_sqft": property_record.local_price_per_sqft or 0,
        "annual_market_growth_rate": property_record.annual_market_growth_rate or 0,
    }

    adjusted = []
    for comp in comp_rows:
        adjusted_comp = adjust_comparable(
            subject,
            {
                "id": comp.id,
                "address": comp.address,
                "sale_price": comp.sale_price,
                "sale_date": comp.sale_date.isoformat(),
                "square_feet": comp.square_feet,
                "bedrooms": comp.bedrooms,
                "bathrooms": comp.bathrooms,
                "lot_size_sqft": comp.lot_size_sqft,
                "year_built": comp.year_built,
                "property_type": comp.property_type,
                "distance_miles": comp.distance_miles,
            },
        )
        adjusted.append(adjusted_comp)

    return {
        "comparables": adjusted,
        "comparable_value": aggregate_comparable_value(adjusted),
    }
