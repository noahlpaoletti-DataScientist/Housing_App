from fastapi.testclient import TestClient

from app.main import app


def test_health_check():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


def test_property_lookup_api():
    with TestClient(app) as client:
        response = client.get("/api/property/lookup", params={"address": "101 Cedar Elm Street"})
        assert response.status_code == 200
        payload = response.json()
        assert payload["matched_property"]["address"] == "101 Cedar Elm Street"
        assert payload["estimated_value"] > 0
