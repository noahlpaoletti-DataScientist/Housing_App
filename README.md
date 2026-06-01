# Real Estate Intelligence Platform

Transparent real estate valuation, renovation-cost, and investment-analysis MVP built with FastAPI, React, SQLite, and mock data. The product is designed to show users not only an estimated value, but why the estimate exists through auditable formula components, assumptions, confidence scoring, and source provenance.

## What the app does

- Looks up a property by address using seeded mock data.
- Calculates an explainable home value estimate.
- Shows comparable-sale adjustments and component weights.
- Estimates renovation costs and renovation ROI.
- Runs investor scenarios for rental and flip analysis.
- Surfaces a confidence score and market-trend context.

## Product positioning

This app is intentionally not a black-box AVM clone. It is a transparent property intelligence platform for brokerages, investors, lenders, insurers, builders, contractors, and homeowners who need an estimate they can explain in plain English.

## Stack

- Backend: FastAPI, SQLAlchemy, SQLite, Pydantic
- Frontend: React + Vite
- Testing: pytest
- Containers: Docker + docker-compose
- Data: seeded mock property, comps, market, and material-cost datasets

## Project structure

```text
HousingApp/
├── backend/
├── frontend/
├── data/
├── docs/
├── notebooks/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── requirements.txt
```

## Local setup

### Backend

1. Create a virtual environment with Python 3.11+.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the API:

```bash
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000
```

Windows PowerShell helper:

```powershell
.\scripts\start-backend.ps1
```

Optional dev mode with auto-reload:

```powershell
.\scripts\start-backend-dev.ps1
```

Windows batch launcher:

```bat
start-backend.bat
```

### Frontend

1. Install Node.js 20+.
2. Install packages:

```bash
cd frontend
npm install
```

3. Start the frontend:

```bash
npm run dev -- --host 0.0.0.0 --port 5173
```

Windows PowerShell helper:

```powershell
.\scripts\start-frontend.ps1
```

Windows batch launcher:

```bat
start-frontend.bat
```

To launch both in separate windows:

```bat
start-all.bat
```

## Docker

Run the full stack with:

```bash
docker-compose up --build
```

- Backend: `http://localhost:8000`
- Swagger docs: `http://localhost:8000/docs`
- Frontend: `http://localhost:5173`

## Testing

```bash
pytest
```

Windows PowerShell helper:

```powershell
.\scripts\run-tests.ps1
```

## Formula overview

### Valuation

Estimated value is built from:

- Comparable-sales value
- Price-per-square-foot value
- Assessed-value signal
- Last-sale-adjusted signal
- Market-trend adjustment
- Optional renovation value add

If a source is missing, the default source weights are redistributed across the available sources and returned to the client.

### Renovation

Renovation totals use material, labor, permit, disposal, overhead, and contingency components. Specialized formulas are included for kitchen, bathroom, and new construction.

### Investment

Investor analysis returns mortgage payment, cash flow, cap rate, cash-on-cash return, estimated resale value, project cost, flip profit, and break-even price.

## Mock data and future integrations

The MVP uses sample data only and does not scrape proprietary listing sources. The codebase is structured so county parcel, assessor, FHFA, Census, permit, rental, and licensed MLS connectors can be added later without rewriting the core formulas.

## Legal/data note

This repository is intentionally designed around mock and future public/licensed connectors. Proprietary real estate sites should not be scraped without the proper data rights.
