# Data Analysis

This folder is for research, experiments, and early-stage analysis before we turn ideas into the main app.

## Purpose

- research which official APIs can support address-based housing lookups
- prototype data pipelines
- define database storage before wiring it into the main app

## Layout

```text
data_analysis/
  README.md
  notes/
    address_api_research.md
  prototypes/
    address_to_tract_lookup.py
  sql/
    sqlite_schema.sql
  outputs/
```

## Current Research Direction

For a national app, the most realistic government-backed flow is:

1. Take a street address.
2. Geocode it with the U.S. Census Geocoder.
3. Extract tract / county / state FIPS.
4. Pull area-level housing metrics from ACS or HUD APIs.
5. Store the address, geocode result, and retrieved metrics in a database.

This gives us address-driven lookup, but not always true parcel-level housing facts. For property-level details such as tax assessment, year built for a specific parcel, or permit history for one house, we will usually need county or city assessor / permit data sources in addition to federal APIs.
