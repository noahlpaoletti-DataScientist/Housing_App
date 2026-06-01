def build_feature_row(property_payload: dict) -> dict:
    return {
        "square_feet": property_payload.get("square_feet", 0),
        "bedrooms": property_payload.get("bedrooms", 0),
        "bathrooms": property_payload.get("bathrooms", 0),
        "lot_size_sqft": property_payload.get("lot_size_sqft", 0),
        "year_built": property_payload.get("year_built", 0),
        "local_price_per_sqft": property_payload.get("local_price_per_sqft", 0),
    }
