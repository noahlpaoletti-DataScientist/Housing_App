# API Documentation

## Health

- `GET /health`

## Property

- `GET /api/property/lookup?address=...`
- `GET /api/property/{property_id}/comparables`

## Valuation

- `GET /api/property/{property_id}/valuation`
- `GET /api/property/{property_id}/formula`

## Renovation

- `POST /api/renovation/estimate`

Request body:

```json
{
  "property_id": 1,
  "renovation_type": "kitchen",
  "inputs": {
    "kitchen_square_feet": 180,
    "cabinet_linear_feet": 24
  }
}
```

## Investment

- `POST /api/investment/analyze`

## Market

- `GET /api/market/trends?zip_code=28203`

## Report

- `GET /api/report/property/{property_id}`
