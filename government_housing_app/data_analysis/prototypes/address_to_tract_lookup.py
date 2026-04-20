"""
Prototype: address -> Census geocoder -> tract-level ACS housing metrics -> SQLite

This is a research script, not main app code yet.

Official sources used:
  - Census Geocoder API
    https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html
  - ACS 5-Year API
    https://www.census.gov/data/developers/data-sets/acs-5year.html
"""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
DEFAULT_DB = Path(__file__).resolve().parents[1] / "outputs" / "housing_research.db"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gov_housing_app.census import ACS_YEAR, fetch_acs_record, geocode_address


ACS_VARIABLES = {
    "NAME": "name",
    "B25077_001E": "median_home_value_usd",
    "B25064_001E": "median_gross_rent_usd",
    "B25035_001E": "median_year_built",
    "B25003_002E": "owner_occupied_units",
    "B25003_003E": "renter_occupied_units",
}


def fetch_tract_housing_metrics(state_fips: str, county_fips: str, tract_code: str) -> Dict[str, Any]:
    raw = fetch_acs_record(
        variables=ACS_VARIABLES,
        geography="tract",
        state_fips=state_fips,
        county_fips=county_fips,
        tract_code=tract_code,
    )
    return {
        "name": raw["name"],
        "median_home_value_usd": raw["median_home_value_usd"],
        "median_gross_rent_usd": raw["median_gross_rent_usd"],
        "median_year_built": raw["median_year_built"],
        "owner_occupied_units": raw["owner_occupied_units"],
        "renter_occupied_units": raw["renter_occupied_units"],
        "state_fips": raw["state"],
        "county_fips": raw["county"],
        "tract_code": raw["tract"],
    }


def init_db(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS addresses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            input_address TEXT NOT NULL,
            matched_address TEXT,
            latitude REAL,
            longitude REAL,
            state_fips TEXT,
            county_fips TEXT,
            tract_code TEXT,
            block_code TEXT,
            geoid_tract TEXT,
            geoid_block TEXT,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS tract_housing_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            geoid_tract TEXT NOT NULL,
            acs_year INTEGER NOT NULL,
            name TEXT,
            median_home_value_usd REAL,
            median_gross_rent_usd REAL,
            median_year_built REAL,
            owner_occupied_units REAL,
            renter_occupied_units REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            UNIQUE (geoid_tract, acs_year)
        );
        """
    )
    conn.commit()


def save_results(
    conn: sqlite3.Connection,
    geocode_result: Dict[str, Any],
    tract_metrics: Dict[str, Any],
) -> None:
    conn.execute(
        """
        INSERT INTO addresses (
            input_address,
            matched_address,
            latitude,
            longitude,
            state_fips,
            county_fips,
            tract_code,
            block_code,
            geoid_tract,
            geoid_block
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            geocode_result["input_address"],
            geocode_result["matched_address"],
            geocode_result["latitude"],
            geocode_result["longitude"],
            geocode_result["state_fips"],
            geocode_result["county_fips"],
            geocode_result["tract_code"],
            geocode_result["block_code"],
            geocode_result["geoid_tract"],
            geocode_result["geoid_block"],
        ),
    )

    conn.execute(
        """
        INSERT OR REPLACE INTO tract_housing_metrics (
            geoid_tract,
            acs_year,
            name,
            median_home_value_usd,
            median_gross_rent_usd,
            median_year_built,
            owner_occupied_units,
            renter_occupied_units
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            geocode_result["geoid_tract"],
            ACS_YEAR,
            tract_metrics["name"],
            tract_metrics["median_home_value_usd"],
            tract_metrics["median_gross_rent_usd"],
            tract_metrics["median_year_built"],
            tract_metrics["owner_occupied_units"],
            tract_metrics["renter_occupied_units"],
        ),
    )
    conn.commit()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Prototype address-based housing lookup using official Census APIs."
    )
    parser.add_argument("address", help='Example: "1600 Pennsylvania Ave NW, Washington, DC 20500"')
    parser.add_argument(
        "--db",
        default=str(DEFAULT_DB),
        help="SQLite database path for storing address and tract results.",
    )
    args = parser.parse_args()

    db_path = Path(args.db).expanduser().resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    geocode_result = geocode_address(args.address)
    tract_metrics = fetch_tract_housing_metrics(
        state_fips=geocode_result["state_fips"],
        county_fips=geocode_result["county_fips"],
        tract_code=geocode_result["tract_code"],
    )

    with sqlite3.connect(db_path) as conn:
        init_db(conn)
        save_results(conn, geocode_result, tract_metrics)

    print("Matched address:")
    print(f'  {geocode_result["matched_address"]}')
    print()
    print("Census geography:")
    print(f'  tract GEOID: {geocode_result["geoid_tract"]}')
    print(f'  block GEOID: {geocode_result["geoid_block"]}')
    print()
    print("Tract-level housing metrics:")
    for key, value in tract_metrics.items():
        if key not in {"state_fips", "county_fips", "tract_code"}:
            print(f"  {key}: {value}")
    print()
    print(f"Saved results to {db_path}")


if __name__ == "__main__":
    main()
