from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from sqlalchemy.orm import Session

from app.db.models import ComparableSale, DataSource, MarketTrend, Property
from app.db.session import SessionLocal
from app.utils.normalization import normalize_address

DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def _load_json(name: str) -> list[dict]:
    with (DATA_DIR / name).open("r", encoding="utf-8") as file:
        return json.load(file)


def seed_database() -> None:
    db: Session = SessionLocal()
    try:
        if not db.query(Property).first():
            for record in _load_json("sample_properties.json"):
                db.add(
                    Property(
                        id=record["id"],
                        address=record["address"],
                        normalized_address=normalize_address(record["address"]),
                        city=record["city"],
                        state=record["state"],
                        zip_code=record["zip_code"],
                        latitude=record["latitude"],
                        longitude=record["longitude"],
                        square_feet=record["square_feet"],
                        bedrooms=record["bedrooms"],
                        bathrooms=record["bathrooms"],
                        lot_size_sqft=record["lot_size_sqft"],
                        year_built=record["year_built"],
                        property_type=record["property_type"],
                        assessed_value=record.get("assessed_value"),
                        last_sale_price=record.get("last_sale_price"),
                        last_sale_date=date.fromisoformat(record["last_sale_date"])
                        if record.get("last_sale_date")
                        else None,
                        local_price_per_sqft=record.get("local_price_per_sqft"),
                        annual_market_growth_rate=record.get("annual_market_growth_rate"),
                    )
                )

        if not db.query(ComparableSale).first():
            for record in _load_json("sample_comps.json"):
                db.add(
                    ComparableSale(
                        **{
                            **record,
                            "sale_date": date.fromisoformat(record["sale_date"]),
                        }
                    )
                )

        if not db.query(MarketTrend).first():
            for record in _load_json("sample_market_trends.json"):
                db.add(MarketTrend(**record))

        if not db.query(DataSource).first():
            db.add_all(
                [
                    DataSource(
                        name="Mock Property Registry",
                        source_type="mock",
                        status="active",
                        provenance_url="local://backend/app/data/sample_properties.json",
                        last_updated_label="Seeded at app startup",
                    ),
                    DataSource(
                        name="Mock Comparable Sales",
                        source_type="mock",
                        status="active",
                        provenance_url="local://backend/app/data/sample_comps.json",
                        last_updated_label="Seeded at app startup",
                    ),
                    DataSource(
                        name="Mock Market Trends",
                        source_type="mock",
                        status="active",
                        provenance_url="local://backend/app/data/sample_market_trends.json",
                        last_updated_label="Seeded at app startup",
                    ),
                ]
            )

        db.commit()
    finally:
        db.close()
