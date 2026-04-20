# Government Housing App

A Python app for exploring official U.S. government housing data, starting with the U.S. Census Bureau ACS API.

## Project Layout

```text
government_housing_app/
  app.py
  requirements.txt
  README.md
  database/
    README.md
    docs/
    schema/
    scripts/
    storage/
  data/
    raw/
    processed/
  src/
    gov_housing_app/
      __init__.py
      explorer.py
  tests/
```

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

## Example Commands

```bash
python app.py
python app.py --sort-by median_gross_rent_usd
python app.py --geography county --state-fips 06 --top 20
```

## Notes

- Current data source: U.S. Census Bureau ACS 5-year API
- Current focus: housing prices, rents, age of housing stock, owner/renter mix, and renovation-related proxy signals
- Next natural upgrade: add building permits, maps, and a web UI
- Database-first work now lives under `database/`, with SQLite as the v1 storage target
