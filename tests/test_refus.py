"""Modèles pour tester un refus (chapitre 7).

Ces deux tests portent sur d'autres règles que celle du TP 4 partie 3 :
reprenez leur forme, pas leur contenu.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app, valider_nom


def test_nom_vide_refuse_unitaire():
    # Le test réussit seulement si valider_nom lève ValueError.
    with pytest.raises(ValueError):
        valider_nom("")


def test_route_inconnue_integration():
    client = TestClient(app)
    reponse = client.get("/route-inconnue")
    assert reponse.status_code == 404
