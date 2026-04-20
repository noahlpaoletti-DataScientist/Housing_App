-- Research database schema for address-driven housing analysis.
-- This is meant for SQLite and can later be adapted to PostgreSQL.

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

CREATE TABLE IF NOT EXISTS local_property_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address_id INTEGER,
    source_name TEXT NOT NULL,
    parcel_id TEXT,
    assessed_value REAL,
    market_value REAL,
    year_built INTEGER,
    last_sale_date TEXT,
    last_sale_price REAL,
    raw_payload TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (address_id) REFERENCES addresses(id)
);

CREATE TABLE IF NOT EXISTS permit_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address_id INTEGER,
    source_name TEXT NOT NULL,
    permit_number TEXT,
    permit_type TEXT,
    permit_status TEXT,
    issue_date TEXT,
    description TEXT,
    valuation REAL,
    raw_payload TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (address_id) REFERENCES addresses(id)
);
