def fetch_fhfa_index(zip_code: str) -> dict:
    return {
        "zip_code": zip_code,
        "status": "placeholder",
        "message": "FHFA HPI connector reserved for a later ingestion phase.",
    }
