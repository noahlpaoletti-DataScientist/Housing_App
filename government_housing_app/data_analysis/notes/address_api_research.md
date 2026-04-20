# Address API Research

## Short Answer

Yes, it is possible to start from a street address and pull useful housing information with APIs, but there is an important limitation:

- National federal APIs usually do **not** expose rich public housing facts for a specific private address.
- They **do** support a strong workflow where we geocode an address and then fetch housing data for the surrounding Census geography, especially the tract or block group.

That means the best first version is:

`street address -> Census geocoder -> tract/county/state FIPS -> ACS/HUD area data -> database`

## What We Can Reliably Do

### 1. Convert a street address into Census geography

Use the Census Geocoder API.

What it gives us:

- matched address
- latitude / longitude
- Census block
- Census tract
- county FIPS
- state FIPS

This is the key bridge from an individual address to the government datasets that are published by geography.

Official sources:

- Census Geocoder overview: https://www.census.gov/data/developers/data-sets/Geocoding-services.html
- Census Geocoder documentation: https://www.census.gov/programs-surveys/geography/technical-documentation/complete-technical-documentation/census-geocoder.html
- Geocoder API reference: https://geocoding.geo.census.gov/geocoder/Geocoding_Services_API.html

### 2. Pull tract or block-group housing data

Use the Census ACS 5-year API after geocoding.

Good examples of tract-level housing metrics:

- median home value
- median gross rent
- owner vs renter occupancy
- median year built
- plumbing and kitchen deficiency proxies

Official source:

- ACS 5-year API: https://www.census.gov/data/developers/data-sets/acs-5year.html

### 3. Add HUD neighborhood / affordability datasets

HUD exposes some housing datasets through APIs and downloadable datasets, often keyed by tract, ZIP, county, or other geography rather than exact address.

Useful options:

- CHAS API for affordability context
- HUD-USPS crosswalk APIs for ZIP and tract relationships

Official sources:

- CHAS dataset overview: https://www.huduser.gov/portal/datasets/cp.html
- CHAS API docs: https://www.huduser.gov/portal/dataset/chas-api.html
- HUD-USPS ZIP Crosswalk: https://www.huduser.gov/portal/datasets/usps_crosswalk.html
- HUD-USPS Tract Crosswalk: https://www.huduser.gov/portal/datasets/census_tract_crosswalk.html

## What We Usually Cannot Get Nationally From One Federal API

For a single exact address, federal APIs generally do not give a clean national property record with fields like:

- parcel ID
- exact assessed value
- exact sale history
- exact permit / renovation history
- exact year built for that specific parcel

Those are usually maintained by:

- county assessor offices
- city open data portals
- local permit systems
- state property / recorder systems

So if the goal is "tell me about 123 Main St specifically," we will probably need a hybrid strategy:

1. federal APIs for geography and neighborhood context
2. local property or permit APIs for parcel-level facts where available

## Best Architecture for Our App

### Phase 1: National address-driven neighborhood lookup

Input:

- street address

Pipeline:

1. geocode address with Census Geocoder
2. save geocode result
3. fetch ACS tract-level housing metrics
4. optionally fetch HUD tract-level metrics
5. store all results in SQLite

Output:

- address match details
- tract / county / state identifiers
- neighborhood housing metrics around that address

### Phase 2: Parcel-level enrichment

Add connectors for local sources:

- county parcel APIs
- permit APIs
- assessor data exports

Output:

- property-specific year built
- assessed value
- recent permits
- renovation signals based on permit history

## Database Recommendation

Yes, we should store this in a database.

Best first choice:

- SQLite

Why:

- built into Python
- easy local development
- great for research and app prototypes
- enough for cached API responses and analysis tables

Suggested tables:

- `addresses`
- `geocode_results`
- `tract_housing_metrics`
- `api_runs`

If the app grows into multi-user or cloud deployment, we can move to:

- PostgreSQL

## Recommendation

The answer is "yes, with a nuance":

- We can absolutely build address-based lookup using official APIs.
- The first reliable national version should return **geography-based housing information around the address**, not promise exact parcel facts for every address in America.
- A database-backed design is a good fit from day one.
