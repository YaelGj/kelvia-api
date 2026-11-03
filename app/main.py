"""API de réservation de salles de Kelvia (cas fictif, exercice pédagogique)."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Kelvia")

# TP 4 partie 2 : décommentez les deux lignes suivantes pour exposer /metrics.
# from prometheus_fastapi_instrumentator import Instrumentator
# Instrumentator().instrument(app).expose(app)

# Données en mémoire : elles repartent de zéro à chaque redémarrage.
SALLES = [
    {"id": 1, "nom": "Atlas", "capacite": 12},
    {"id": 2, "nom": "Boréal", "capacite": 6},
    {"id": 3, "nom": "Cassiopée", "capacite": 20},
]


class NouvelleSalle(BaseModel):
    nom: str
    capacite: int


def verifier_capacite(capacite: int) -> int:
    """Règle métier : une salle ne peut pas avoir une capacité négative."""
    if capacite < 0:
        raise ValueError("la capacité d'une salle ne peut pas être négative")
    return capacite


def valider_nom(nom: str) -> str:
    """Refuse un nom de salle vide ou fait seulement d'espaces."""
    if not nom.strip():
        raise ValueError("le nom d'une salle ne peut pas être vide")
    return nom


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/salles")
def lister_salles():
    return SALLES


@app.post("/salles", status_code=201)
def creer_salle(salle: NouvelleSalle):
    try:
        capacite = verifier_capacite(salle.capacite)
    except ValueError as erreur:
        raise HTTPException(status_code=422, detail=str(erreur))
    nouvelle = {"id": len(SALLES) + 1, "nom": salle.nom, "capacite": capacite}
    SALLES.append(nouvelle)
    return nouvelle
