"""Shared Census API helpers for the housing app."""

from __future__ import annotations

from typing import Any, Dict

import pandas as pd
import requests


ACS_YEAR = 2024
ACS_DATASET = "acs/acs5"
ACS_API_ROOT = f"https://api.census.gov/data/{ACS_YEAR}/{ACS_DATASET}"
GEOCODER_URL = "https://geocoding.geo.census.gov/geocoder/geographies/onelineaddress"


HOUSING_VARIABLES: Dict[str, str] = {
    "NAME": "name",
    "B25077_001E": "median_home_value_usd",
    "B25064_001E": "median_gross_rent_usd",
    "B25035_001E": "median_year_built",
    "B25003_001E": "occupied_units",
    "B25003_002E": "owner_occupied_units",
    "B25003_003E": "renter_occupied_units",
    "B25047_001E": "housing_units_plumbing_total",
    "B25047_003E": "housing_units_lacking_complete_plumbing",
    "B25051_001E": "housing_units_kitchen_total",
    "B25051_003E": "housing_units_lacking_complete_kitchen",
}


def build_acs_params(variables: Dict[str, str], geography: str, **geo_parts: str | None) -> Dict[str, str]:
    params = {"get": ",".join(variables.keys())}

    if geography == "state":
        params["for"] = "state:*"
    elif geography == "county":
        state_fips = geo_parts.get("state_fips")
        if not state_fips:
            raise ValueError("--state-fips is required when geography=county")
        params["for"] = "county:*"
        params["in"] = f"state:{state_fips}"
    elif geography == "tract":
        state_fips = geo_parts.get("state_fips")
        county_fips = geo_parts.get("county_fips")
        tract_code = geo_parts.get("tract_code")
        if not state_fips or not county_fips or not tract_code:
            raise ValueError("state_fips, county_fips, and tract_code are required for tract lookups")
        params["for"] = f"tract:{tract_code}"
        params["in"] = f"state:{state_fips} county:{county_fips}"
    else:
        raise ValueError(f"Unsupported geography: {geography}")

    return params


def fetch_acs_dataframe(
    variables: Dict[str, str],
    geography: str,
    **geo_parts: str | None,
) -> pd.DataFrame:
    params = build_acs_params(variables=variables, geography=geography, **geo_parts)
    response = requests.get(ACS_API_ROOT, params=params, timeout=60)
    response.raise_for_status()

    payload = response.json()
    header, rows = payload[0], payload[1:]
    return pd.DataFrame(rows, columns=header).rename(columns=variables)


def fetch_acs_record(
    variables: Dict[str, str],
    geography: str,
    **geo_parts: str | None,
) -> Dict[str, Any]:
    df = fetch_acs_dataframe(variables=variables, geography=geography, **geo_parts)
    if df.empty:
        raise ValueError("Census ACS response returned no rows")
    return df.iloc[0].to_dict()


def geocode_address(address: str) -> Dict[str, Any]:
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

    return {
        "input_address": address,
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
