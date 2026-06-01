from app.db.models import Property


def geocode_property(property_record: Property) -> dict[str, float]:
    return {"latitude": property_record.latitude, "longitude": property_record.longitude}
