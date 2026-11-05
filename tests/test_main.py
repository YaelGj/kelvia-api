from fastapi.testclient import TestClient

from app.main import app


def test_health():
    client = TestClient(app)
    reponse = client.get("/health")
    assert reponse.status_code == 200


def test_prix_pass_1_jour():
    client = TestClient(app)
    categories = client.get("/billets").json()
    pass_1_jour = next(c for c in categories if c["nom"] == "Pass 1 jour")
    assert pass_1_jour["prix"] == 59
