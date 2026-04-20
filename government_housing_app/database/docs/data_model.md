# V1 Data Model

The database is designed for a database-first housing project focused on `price` and `renovation`.

## Core Flow

1. User enters an address.
2. We store the raw address request.
3. We geocode the address to Census geography.
4. We fetch tract-level housing metrics.
5. We fetch tract/county-level price trends.
6. We optionally attach parcel or permit evidence.
7. We cache a combined lookup result for fast reuse.

## Table Roles

### addresses

Stores what the user searched for.

Important fields:

- `input_address`
- `normalized_address`

### geocode_results

Stores the matched address and geographies returned by the Census geocoder.

Important fields:

- `matched_address`
- `latitude`
- `longitude`
- `state_fips`
- `county_fips`
- `tract_code`
- `block_code`
- `geoid_tract`
- `geoid_block`

### tract_metrics_acs

Stores tract-level snapshot metrics from ACS.

Important fields:

- `median_home_value_usd`
- `median_gross_rent_usd`
- `median_year_built`
- `housing_age_years`
- `owner_share_pct`
- `renter_share_pct`
- `lack_plumbing_pct`
- `lack_kitchen_pct`
- `renovation_signal`

### tract_price_trends_fhfa

Stores tract- or county-level price trend metrics from FHFA.

Important fields:

- `geography_type`
- `geography_id`
- `hpi_value`
- `hpi_1yr_change_pct`
- `hpi_5yr_change_pct`
- `as_of_date`

### lookup_cache

Stores the combined report returned to the app, keyed by address and freshness.

Important fields:

- `address_id`
- `geocode_result_id`
- `acs_metric_id`
- `fhfa_trend_id`
- `cache_key`
- `is_stale`
- `refreshed_at`

### local_property_records

Future-ready table for assessor or parcel-level property data.

### permit_records

Future-ready table for local permit history and renovation activity.

## Why This Shape

This structure gives us:

- repeatable address lookups
- cached tract-level housing context
- room for local renovation evidence
- a clean upgrade path to PostgreSQL later
