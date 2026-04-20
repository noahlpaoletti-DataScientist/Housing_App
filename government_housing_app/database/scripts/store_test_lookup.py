from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from pathlib import Path
from typing import Any, Dict

import requests


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
DATABASE_DIR = PROJECT_ROOT / "database"
DB_PATH = DATABASE_DIR / "storage" / "housing_app.db"
RAW_JSON_DIR = DATABASE_DIR / "raw_json"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from gov_housing_app.census import ACS_YEAR, HOUSING_VARIABLES


ACS_API_ROOT = f"https://api.census.gov/data/{ACS_YEAR}/acs/acs5"
GEOCODER_URL = "https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress"
MISSING_SENTINELS = {"-666666666", "-222222222", "-333333333", "-555555555", "-888888888", "-999999999"}


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower()).strip("_")
    return slug or "lookup"


def save_json(payload: Any, folder: Path, stem: str) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{stem}.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def to_float(value: Any) -> float | None:
    if value is None:
        return None
    text = str(value)
    if text in MISSING_SENTINELS:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def normalize_address(address: str) -> str:
    return " ".join(address.upper().split())


def geocode_with_raw(address: str) -> tuple[Dict[str, Any], Dict[str, Any]]:
    params = {
        "address": address,
        "benchmark": "Public_AR_Current",
        "vintage": "Current_Current",
        "format": "json",
    }
    response = requests.get(GEOCODER_URL, params=params, timeout=60)
    response.raise_for_status()
    payload = response.json()

    matches = payload["result"]["addressMatches"]
    if not matches:
        raise ValueError(f"No Census geocoder match found for address: {address}")

    match = matches[0]
    geographies = match["geographies"]
    census_blocks = geographies.get("2020 Census Blocks") or geographies.get("Census Blocks")
    if not census_blocks:
        raise ValueError("Geocoder response did not include Census block geography")

    block = census_blocks[0]
    coordinates = match["coordinates"]
    normalized = {
        "input_address": address,
        "normalized_address": normalize_address(address),
        "matched_address": match["matchedAddress"],
        "longitude": coordinates["x"],
        "latitude": coordinates["y"],
        "state_fips": block["STATE"],
        "county_fips": block["COUNTY"],
        "tract_code": block["TRACT"],
        "block_code": block["BLOCK"],
        "geoid_tract": f'{block["STATE"]}{block["COUNTY"]}{block["TRACT"]}',
        "geoid_block": f'{block["STATE"]}{block["COUNTY"]}{block["TRACT"]}{block["BLOCK"]}',
    }
    return normalized, payload


def fetch_acs_with_raw(state_fips: str, county_fips: str, tract_code: str) -> tuple[Dict[str, Any], list[Any]]:
    params = {
        "get": ",".join(HOUSING_VARIABLES.keys()),
        "for": f"tract:{tract_code}",
        "in": f"state:{state_fips} county:{county_fips}",
    }
    response = requests.get(ACS_API_ROOT, params=params, timeout=60)
    response.raise_for_status()
    payload = response.json()

    header, row = payload[0], payload[1]
    raw = dict(zip(header, row))

    median_year_built = to_float(raw.get("B25035_001E"))
    occupied_units = to_float(raw.get("B25003_001E"))
    owner_occupied_units = to_float(raw.get("B25003_002E"))
    renter_occupied_units = to_float(raw.get("B25003_003E"))
    plumbing_total = to_float(raw.get("B25047_001E"))
    lacking_plumbing = to_float(raw.get("B25047_003E"))
    kitchen_total = to_float(raw.get("B25051_001E"))
    lacking_kitchen = to_float(raw.get("B25051_003E"))

    owner_share_pct = (
        (owner_occupied_units / occupied_units) * 100
        if occupied_units not in (None, 0) and owner_occupied_units is not None
        else None
    )
    renter_share_pct = (
        (renter_occupied_units / occupied_units) * 100
        if occupied_units not in (None, 0) and renter_occupied_units is not None
        else None
    )
    lack_plumbing_pct = (
        (lacking_plumbing / plumbing_total) * 100
        if plumbing_total not in (None, 0) and lacking_plumbing is not None
        else None
    )
    lack_kitchen_pct = (
        (lacking_kitchen / kitchen_total) * 100
        if kitchen_total not in (None, 0) and lacking_kitchen is not None
        else None
    )
    housing_age_years = ACS_YEAR - median_year_built if median_year_built is not None else None
    renovation_signal = (
        (housing_age_years or 0)
        + 40 * (lack_plumbing_pct or 0)
        + 40 * (lack_kitchen_pct or 0)
        if any(value is not None for value in (housing_age_years, lack_plumbing_pct, lack_kitchen_pct))
        else None
    )

    normalized = {
        "name": raw["NAME"],
        "state_fips": raw["state"],
        "county_fips": raw["county"],
        "tract_code": raw["tract"],
        "median_home_value_usd": to_float(raw.get("B25077_001E")),
        "median_gross_rent_usd": to_float(raw.get("B25064_001E")),
        "median_year_built": median_year_built,
        "housing_age_years": housing_age_years,
        "occupied_units": occupied_units,
        "owner_occupied_units": owner_occupied_units,
        "renter_occupied_units": renter_occupied_units,
        "owner_share_pct": owner_share_pct,
        "renter_share_pct": renter_share_pct,
        "lack_plumbing_pct": lack_plumbing_pct,
        "lack_kitchen_pct": lack_kitchen_pct,
        "renovation_signal": renovation_signal,
    }
    return normalized, payload


def init_db(conn: sqlite3.Connection) -> None:
    conn.execute("PRAGMA foreign_keys = ON;")
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            filename TEXT PRIMARY KEY,
            applied_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.commit()


def ensure_database_ready() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        init_db(conn)


def upsert_lookup(
    conn: sqlite3.Connection,
    geocode_result: Dict[str, Any],
    tract_metrics: Dict[str, Any],
) -> Dict[str, int]:
    cursor = conn.execute(
        """
        INSERT INTO addresses (input_address, normalized_address)
        VALUES (?, ?)
        """,
        (geocode_result["input_address"], geocode_result["normalized_address"]),
    )
    address_id = cursor.lastrowid

    cursor = conn.execute(
        """
        INSERT INTO geocode_results (
            address_id,
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
            address_id,
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
    geocode_result_id = cursor.lastrowid

    conn.execute(
        """
        INSERT INTO tract_metrics_acs (
            geoid_tract,
            acs_year,
            name,
            median_home_value_usd,
            median_gross_rent_usd,
            median_year_built,
            housing_age_years,
            occupied_units,
            owner_occupied_units,
            renter_occupied_units,
            owner_share_pct,
            renter_share_pct,
            lack_plumbing_pct,
            lack_kitchen_pct,
            renovation_signal
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(geoid_tract, acs_year) DO UPDATE SET
            name=excluded.name,
            median_home_value_usd=excluded.median_home_value_usd,
            median_gross_rent_usd=excluded.median_gross_rent_usd,
            median_year_built=excluded.median_year_built,
            housing_age_years=excluded.housing_age_years,
            occupied_units=excluded.occupied_units,
            owner_occupied_units=excluded.owner_occupied_units,
            renter_occupied_units=excluded.renter_occupied_units,
            owner_share_pct=excluded.owner_share_pct,
            renter_share_pct=excluded.renter_share_pct,
            lack_plumbing_pct=excluded.lack_plumbing_pct,
            lack_kitchen_pct=excluded.lack_kitchen_pct,
            renovation_signal=excluded.renovation_signal
        """,
        (
            geocode_result["geoid_tract"],
            ACS_YEAR,
            tract_metrics["name"],
            tract_metrics["median_home_value_usd"],
            tract_metrics["median_gross_rent_usd"],
            tract_metrics["median_year_built"],
            tract_metrics["housing_age_years"],
            tract_metrics["occupied_units"],
            tract_metrics["owner_occupied_units"],
            tract_metrics["renter_occupied_units"],
            tract_metrics["owner_share_pct"],
            tract_metrics["renter_share_pct"],
            tract_metrics["lack_plumbing_pct"],
            tract_metrics["lack_kitchen_pct"],
            tract_metrics["renovation_signal"],
        ),
    )

    acs_metric_id = conn.execute(
        """
        SELECT id
        FROM tract_metrics_acs
        WHERE geoid_tract = ? AND acs_year = ?
        """,
        (geocode_result["geoid_tract"], ACS_YEAR),
    ).fetchone()[0]

    cache_key = geocode_result["normalized_address"]
    conn.execute(
        """
        INSERT INTO lookup_cache (
            cache_key,
            address_id,
            geocode_result_id,
            acs_metric_id
        ) VALUES (?, ?, ?, ?)
        ON CONFLICT(cache_key) DO UPDATE SET
            address_id=excluded.address_id,
            geocode_result_id=excluded.geocode_result_id,
            acs_metric_id=excluded.acs_metric_id,
            is_stale=0,
            refreshed_at=CURRENT_TIMESTAMP
        """,
        (cache_key, address_id, geocode_result_id, acs_metric_id),
    )
    conn.commit()

    return {
        "address_id": address_id,
        "geocode_result_id": geocode_result_id,
        "acs_metric_id": acs_metric_id,
    }


def store_lookup(address: str) -> Dict[str, Any]:
    geocode_result, geocoder_payload = geocode_with_raw(address)
    tract_metrics, acs_payload = fetch_acs_with_raw(
        state_fips=geocode_result["state_fips"],
        county_fips=geocode_result["county_fips"],
        tract_code=geocode_result["tract_code"],
    )

    file_stem = slugify(geocode_result["normalized_address"])
    geocoder_path = save_json(
        geocoder_payload,
        RAW_JSON_DIR / "census_geocoder",
        f"{file_stem}_geocoder",
    )
    acs_path = save_json(
        acs_payload,
        RAW_JSON_DIR / "census_acs",
        f"{file_stem}_acs_tract",
    )

    with sqlite3.connect(DB_PATH) as conn:
        init_db(conn)
        ids = upsert_lookup(conn, geocode_result, tract_metrics)

    return {
        "geocode_result": geocode_result,
        "tract_metrics": tract_metrics,
        "geocoder_path": geocoder_path,
        "acs_path": acs_path,
        "ids": ids,
        "database_path": DB_PATH,
    }


def format_metric(value: Any, kind: str = "plain") -> str:
    if value is None:
        return "data unavailable for this tract"
    if kind == "currency":
        return f"${value:,.0f}"
    if kind == "pct":
        return f"{value:.1f}%"
    if kind == "years":
        return f"{value:.0f}"
    return str(value)


def print_lookup_summary(result: Dict[str, Any]) -> None:
    geocode_result = result["geocode_result"]
    tract_metrics = result["tract_metrics"]
    ids = result["ids"]

    print("Stored test lookup")
    print(f"  input_address: {geocode_result['input_address']}")
    print(f"  matched_address: {geocode_result['matched_address']}")
    print(f"  geoid_tract: {geocode_result['geoid_tract']}")
    print(f"  address_id: {ids['address_id']}")
    print(f"  geocode_result_id: {ids['geocode_result_id']}")
    print(f"  acs_metric_id: {ids['acs_metric_id']}")
    print(f"  geocoder_json: {result['geocoder_path']}")
    print(f"  acs_json: {result['acs_path']}")
    print(f"  database: {result['database_path']}")
    print()
    print("ACS tract metrics")
    print(f"  median_home_value_usd: {format_metric(tract_metrics['median_home_value_usd'], 'currency')}")
    print(f"  median_gross_rent_usd: {format_metric(tract_metrics['median_gross_rent_usd'], 'currency')}")
    print(f"  median_year_built: {format_metric(tract_metrics['median_year_built'], 'years')}")
    print(f"  housing_age_years: {format_metric(tract_metrics['housing_age_years'], 'years')}")
    print(f"  owner_share_pct: {format_metric(tract_metrics['owner_share_pct'], 'pct')}")
    print(f"  renter_share_pct: {format_metric(tract_metrics['renter_share_pct'], 'pct')}")
    print(f"  lack_plumbing_pct: {format_metric(tract_metrics['lack_plumbing_pct'], 'pct')}")
    print(f"  lack_kitchen_pct: {format_metric(tract_metrics['lack_kitchen_pct'], 'pct')}")
    print(f"  renovation_signal: {format_metric(tract_metrics['renovation_signal'])}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Store a test address lookup as raw JSON plus normalized SQLite rows."
    )
    parser.add_argument(
        "address",
        nargs="?",
        default="4059 Mt Lee Dr, Hollywood, CA 90068",
        help='Example: "4059 Mt Lee Dr, Hollywood, CA 90068"',
    )
    args = parser.parse_args()

    ensure_database_ready()
    result = store_lookup(args.address)
    print_lookup_summary(result)


if __name__ == "__main__":
    main()
