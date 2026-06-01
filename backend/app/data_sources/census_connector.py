def fetch_census_context(zip_code: str) -> dict:
    return {
        "zip_code": zip_code,
        "status": "placeholder",
        "message": "Census integration is designed but mocked for MVP use.",
    }
