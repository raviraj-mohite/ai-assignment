from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    res = client.get("/health")
    assert res.status_code == 200

def test_validation_fail():
    res = client.post("/validate", json={})
    assert res.status_code == 422