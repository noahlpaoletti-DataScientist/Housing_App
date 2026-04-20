#!/usr/bin/env python3
"""
Explore official U.S. government housing data with Python.

Primary source:
  - U.S. Census Bureau ACS 5-Year API
    https://www.census.gov/data/developers/data-sets/acs-5year.html

This module focuses on variables that are easy to retrieve nationally and
useful for housing-price / rent / housing-condition exploration.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, Iterable, List

import pandas as pd

from gov_housing_app.census import ACS_YEAR, HOUSING_VARIABLES, fetch_acs_dataframe


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT = PROJECT_ROOT / "data" / "processed" / "housing_data.csv"


STATE_FIPS_TO_ABBR: Dict[str, str] = {
    "01": "AL",
    "02": "AK",
    "04": "AZ",
    "05": "AR",
    "06": "CA",
    "08": "CO",
    "09": "CT",
    "10": "DE",
    "11": "DC",
    "12": "FL",
    "13": "GA",
    "15": "HI",
    "16": "ID",
    "17": "IL",
    "18": "IN",
    "19": "IA",
    "20": "KS",
    "21": "KY",
    "22": "LA",
    "23": "ME",
    "24": "MD",
    "25": "MA",
    "26": "MI",
    "27": "MN",
    "28": "MS",
    "29": "MO",
    "30": "MT",
    "31": "NE",
    "32": "NV",
    "33": "NH",
    "34": "NJ",
    "35": "NM",
    "36": "NY",
    "37": "NC",
    "38": "ND",
    "39": "OH",
    "40": "OK",
    "41": "OR",
    "42": "PA",
    "44": "RI",
    "45": "SC",
    "46": "SD",
    "47": "TN",
    "48": "TX",
    "49": "UT",
    "50": "VT",
    "51": "VA",
    "53": "WA",
    "54": "WV",
    "55": "WI",
    "56": "WY",
    "72": "PR",
}


def fetch_acs(geography: str, state_fips: str | None) -> pd.DataFrame:
    return fetch_acs_dataframe(
        variables=HOUSING_VARIABLES,
        geography=geography,
        state_fips=state_fips,
    )


def numeric_columns(df: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors="coerce")
    return df


def enrich(df: pd.DataFrame) -> pd.DataFrame:
    numeric_cols: List[str] = [
        "median_home_value_usd",
        "median_gross_rent_usd",
        "median_year_built",
        "occupied_units",
        "owner_occupied_units",
        "renter_occupied_units",
        "housing_units_plumbing_total",
        "housing_units_lacking_complete_plumbing",
        "housing_units_kitchen_total",
        "housing_units_lacking_complete_kitchen",
    ]
    df = numeric_columns(df, numeric_cols)

    if "state" in df.columns:
        df["state_abbr"] = df["state"].map(STATE_FIPS_TO_ABBR)

    df["owner_share_pct"] = 100 * df["owner_occupied_units"] / df["occupied_units"]
    df["renter_share_pct"] = 100 * df["renter_occupied_units"] / df["occupied_units"]
    df["housing_age_years"] = ACS_YEAR - df["median_year_built"]
    df["lack_plumbing_pct"] = (
        100
        * df["housing_units_lacking_complete_plumbing"]
        / df["housing_units_plumbing_total"]
    )
    df["lack_kitchen_pct"] = (
        100
        * df["housing_units_lacking_complete_kitchen"]
        / df["housing_units_kitchen_total"]
    )

    # Practical renovation proxy: older stock + basic housing deficiencies.
    df["renovation_signal"] = (
        df["housing_age_years"].fillna(0)
        + 40 * df["lack_plumbing_pct"].fillna(0)
        + 40 * df["lack_kitchen_pct"].fillna(0)
    )

    ordered_columns = [
        "name",
        "state_abbr" if "state_abbr" in df.columns else None,
        "state" if "state" in df.columns else None,
        "county" if "county" in df.columns else None,
        "median_home_value_usd",
        "median_gross_rent_usd",
        "median_year_built",
        "housing_age_years",
        "occupied_units",
        "owner_occupied_units",
        "renter_occupied_units",
        "owner_share_pct",
        "renter_share_pct",
        "housing_units_lacking_complete_plumbing",
        "lack_plumbing_pct",
        "housing_units_lacking_complete_kitchen",
        "lack_kitchen_pct",
        "renovation_signal",
    ]
    ordered_columns = [col for col in ordered_columns if col is not None and col in df.columns]

    return df[ordered_columns].sort_values("median_home_value_usd", ascending=False)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Download and explore official U.S. government housing data."
    )
    parser.add_argument(
        "--geography",
        choices=["state", "county"],
        default="state",
        help="Pull state-level or county-level ACS results.",
    )
    parser.add_argument(
        "--state-fips",
        help="Required for county mode, e.g. 06 for California or 36 for New York.",
    )
    parser.add_argument(
        "--sort-by",
        default="median_home_value_usd",
        help="Column to sort by in the final output.",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        help="How many rows to print to the console.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="CSV path to write the final table.",
    )
    args = parser.parse_args()

    df = fetch_acs(geography=args.geography, state_fips=args.state_fips)
    result = enrich(df)

    if args.sort_by not in result.columns:
        raise SystemExit(
            f"Unknown sort column '{args.sort_by}'. Available columns: "
            + ", ".join(result.columns)
        )

    result = result.sort_values(args.sort_by, ascending=False)

    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result.to_csv(output_path, index=False)

    preview = result.head(args.top).copy()
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 180)

    print(f"Saved {len(result):,} rows to {output_path}")
    print()
    print(preview.to_string(index=False))
    print()
    print("Notes:")
    print(f"- Source: U.S. Census Bureau ACS {ACS_YEAR} 5-year estimates")
    print("- Renovation is approximated here using housing age and basic housing-condition signals.")
    print("- For deeper renovation data, add the American Housing Survey and building permits data.")


if __name__ == "__main__":
    main()
