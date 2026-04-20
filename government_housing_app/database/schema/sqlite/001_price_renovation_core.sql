PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS api_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_name TEXT NOT NULL,
    request_type TEXT NOT NULL,
    request_key TEXT,
    status_code INTEGER,
    requested_at TEXT DEFAULT CURRENT_TIMESTAMP,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS addresses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    input_address TEXT NOT NULL,
    normalized_address TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS geocode_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address_id INTEGER NOT NULL,
    matched_address TEXT NOT NULL,
    latitude REAL,
    longitude REAL,
    state_fips TEXT NOT NULL,
    county_fips TEXT NOT NULL,
    tract_code TEXT NOT NULL,
    block_code TEXT,
    geoid_tract TEXT NOT NULL,
    geoid_block TEXT,
    source_name TEXT NOT NULL DEFAULT 'census_geocoder',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (address_id) REFERENCES addresses(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS tract_metrics_acs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    geoid_tract TEXT NOT NULL,
    acs_year INTEGER NOT NULL,
    name TEXT,
    median_home_value_usd REAL,
    median_gross_rent_usd REAL,
    median_year_built REAL,
    housing_age_years REAL,
    occupied_units REAL,
    owner_occupied_units REAL,
    renter_occupied_units REAL,
    owner_share_pct REAL,
    renter_share_pct REAL,
    lack_plumbing_pct REAL,
    lack_kitchen_pct REAL,
    renovation_signal REAL,
    source_name TEXT NOT NULL DEFAULT 'census_acs5',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (geoid_tract, acs_year)
);

CREATE TABLE IF NOT EXISTS tract_price_trends_fhfa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    geography_type TEXT NOT NULL,
    geography_id TEXT NOT NULL,
    series_id TEXT,
    as_of_date TEXT NOT NULL,
    hpi_value REAL,
    hpi_1yr_change_pct REAL,
    hpi_5yr_change_pct REAL,
    source_name TEXT NOT NULL DEFAULT 'fhfa_hpi',
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (geography_type, geography_id, as_of_date)
);

CREATE TABLE IF NOT EXISTS local_property_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address_id INTEGER NOT NULL,
    source_name TEXT NOT NULL,
    parcel_id TEXT,
    assessed_value REAL,
    market_value REAL,
    year_built INTEGER,
    last_sale_date TEXT,
    last_sale_price REAL,
    raw_payload TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (address_id) REFERENCES addresses(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS permit_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address_id INTEGER NOT NULL,
    source_name TEXT NOT NULL,
    permit_number TEXT,
    permit_type TEXT,
    permit_status TEXT,
    issue_date TEXT,
    description TEXT,
    valuation REAL,
    raw_payload TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (address_id) REFERENCES addresses(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS lookup_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cache_key TEXT NOT NULL UNIQUE,
    address_id INTEGER NOT NULL,
    geocode_result_id INTEGER NOT NULL,
    acs_metric_id INTEGER,
    fhfa_trend_id INTEGER,
    local_property_record_id INTEGER,
    permit_summary TEXT,
    is_stale INTEGER NOT NULL DEFAULT 0,
    refreshed_at TEXT DEFAULT CURRENT_TIMESTAMP,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (address_id) REFERENCES addresses(id) ON DELETE CASCADE,
    FOREIGN KEY (geocode_result_id) REFERENCES geocode_results(id) ON DELETE CASCADE,
    FOREIGN KEY (acs_metric_id) REFERENCES tract_metrics_acs(id) ON DELETE SET NULL,
    FOREIGN KEY (fhfa_trend_id) REFERENCES tract_price_trends_fhfa(id) ON DELETE SET NULL,
    FOREIGN KEY (local_property_record_id) REFERENCES local_property_records(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_geocode_results_geoid_tract
    ON geocode_results (geoid_tract);

CREATE INDEX IF NOT EXISTS idx_tract_metrics_acs_geoid_tract
    ON tract_metrics_acs (geoid_tract);

CREATE INDEX IF NOT EXISTS idx_tract_price_trends_fhfa_geography
    ON tract_price_trends_fhfa (geography_type, geography_id);

CREATE INDEX IF NOT EXISTS idx_local_property_records_address_id
    ON local_property_records (address_id);

CREATE INDEX IF NOT EXISTS idx_permit_records_address_id
    ON permit_records (address_id);
