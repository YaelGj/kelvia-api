from fastapi.testclient import TestClient

from app.main import app


def test_health():
    client = TestClient(app)
    reponse = client.get("/health")
    assert reponse.status_code == 200
