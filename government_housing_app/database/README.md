# Database

This folder is the canonical home for the database-first version of the project.

We are starting with `SQLite` so we can finalize the data model for address lookup, price signals, and renovation signals before building the app UI.

## Goals

- define a stable v1 schema for address-driven housing lookups
- store cached API results instead of re-fetching everything repeatedly
- support price-focused data first, with renovation evidence layered in
- keep the structure easy to migrate later to PostgreSQL or BigQuery-backed analytics

## Layout

```text
database/
  README.md
  docs/
    data_model.md
  raw_json/
    census_geocoder/
    census_acs/
  schema/
    sqlite/
      001_price_renovation_core.sql
  scripts/
    init_sqlite.py
    batch_import_addresses.py
    store_test_lookup.py
  storage/
```

## What Belongs Here

- `schema/`
  Versioned SQL files that define the database structure.
- `scripts/`
  Utility scripts for creating and migrating the local database.
- `raw_json/`
  Raw API responses stored as JSON so we keep the original source payloads.
- `storage/`
  Local SQLite database files. These are ignored by git.
- `docs/`
  Notes on what each table means and how the data flows through the project.

## V1 Database Scope

The first version of the schema is designed around one flow:

`address -> geocode -> tract -> price metrics -> renovation signals -> cached report`

The key tables are:

- `addresses`
- `geocode_results`
- `tract_metrics_acs`
- `tract_price_trends_fhfa`
- `lookup_cache`
- `permit_records`
- `local_property_records`
- `api_runs`

The raw source payloads also live on disk under:

- `raw_json/census_geocoder/`
- `raw_json/census_acs/`

## Initialize The Local Database

From the `government_housing_app` folder:

```powershell
.\.venv\Scripts\python.exe .\database\scripts\init_sqlite.py
```

This will create:

`database\storage\housing_app.db`

## Store A Test Lookup

From the `government_housing_app` folder:

```powershell
.\.venv\Scripts\python.exe .\database\scripts\store_test_lookup.py "4059 Mt Lee Dr, Hollywood, CA 90068"
```

This will:

- save the raw Census Geocoder JSON
- save the raw ACS JSON
- normalize key fields into SQLite
- print friendly labels when ACS values are unavailable for a tract

## Batch Import Addresses

You can import multiple addresses at once either directly or from a text file.

Directly:

```powershell
.\.venv\Scripts\python.exe .\database\scripts\batch_import_addresses.py "1600 Pennsylvania Ave NW, Washington, DC 20500" "350 5th Ave, New York, NY 10118"
```

From a file:

```powershell
.\.venv\Scripts\python.exe .\database\scripts\batch_import_addresses.py --file .\database\sample_addresses.txt
```

The text file format is simple:

```text
# one address per line
1600 Pennsylvania Ave NW, Washington, DC 20500
350 5th Ave, New York, NY 10118
```
