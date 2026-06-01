from __future__ import annotations

from sqlalchemy.orm import Session

from app.db.models import LookupHistory, Property
from app.utils.normalization import normalize_address


def get_property_by_address(db: Session, address: str, record_history: bool = False) -> Property | None:
    normalized = normalize_address(address)
    property_record = (
        db.query(Property).filter(Property.normalized_address == normalized).one_or_none()
    )

    if property_record is None:
        property_record = (
            db.query(Property)
            .filter(Property.normalized_address.contains(normalized.split(" ")[0]))
            .first()
        )

    if record_history:
        db.add(
            LookupHistory(
                input_address=address,
                normalized_address=normalized,
                property_id=property_record.id if property_record else None,
                matched=property_record is not None,
            )
        )
        db.commit()
    return property_record


def serialize_property(property_record: Property) -> dict:
    return {
        "id": property_record.id,
        "address": property_record.address,
        "city": property_record.city,
        "state": property_record.state,
        "zip_code": property_record.zip_code,
        "latitude": property_record.latitude,
        "longitude": property_record.longitude,
        "square_feet": property_record.square_feet,
        "bedrooms": property_record.bedrooms,
        "bathrooms": property_record.bathrooms,
        "lot_size_sqft": property_record.lot_size_sqft,
        "year_built": property_record.year_built,
        "property_type": property_record.property_type,
        "assessed_value": property_record.assessed_value,
        "last_sale_price": property_record.last_sale_price,
        "last_sale_date": property_record.last_sale_date.isoformat()
        if property_record.last_sale_date
        else None,
        "local_price_per_sqft": property_record.local_price_per_sqft,
        "annual_market_growth_rate": property_record.annual_market_growth_rate,
    }
