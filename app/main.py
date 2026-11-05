"""Billetterie en ligne de Kelvia pour festivals de musique (cas fictif, exercice pédagogique)."""
import asyncio
import random
from html import escape

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Nom du festival affiché sur la page d'accueil.
FESTIVAL = "Festival des Lucioles"

# Nombre maximal de billets par commande.
QUANTITE_MAX = 4

# Catégories de billets, en mémoire : le stock repart de sa valeur initiale à chaque redémarrage.
CATEGORIES = [
    {"id": "pass-1-jour", "nom": "Pass 1 jour", "prix": 59, "stock": 5000},
    {"id": "pass-3-jours", "nom": "Pass 3 jours", "prix": 149, "stock": 2000},
    {"id": "camping", "nom": "Camping", "prix": 25, "stock": 1000},
]

app = FastAPI(title="Kelvia")

# TP 4 : décommentez les deux lignes suivantes pour exposer /metrics.
# from prometheus_fastapi_instrumentator import Instrumentator
# Instrumentator().instrument(app, latency_lowr_buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1)).expose(app)


class Commande(BaseModel):
    categorie: str
    quantite: int
    nom: str


def verifier_quantite(quantite: int) -> int:
    """Règle métier : une commande compte de 1 à QUANTITE_MAX billets."""
    if quantite < 1 or quantite > QUANTITE_MAX:
        raise ValueError(f"une commande compte de 1 à {QUANTITE_MAX} billets")
    return quantite


def valider_nom(nom: str) -> str:
    """Refuse un nom d'acheteur vide ou fait seulement d'espaces."""
    if not nom.strip():
        raise ValueError("le nom de l'acheteur ne peut pas être vide")
    return nom


# Simulation pédagogique : un vrai site ralentit quand beaucoup de clients arrivent en même temps.
# Ici, chaque requête sur /billets attend quelques millisecondes de plus par requête déjà en cours :
# quelques millisecondes au repos, quelques centaines pendant « ./charge.sh rush », jamais plus de 0,9 s.
requetes_en_cours = 0


async def latence_simulee():
    global requetes_en_cours
    requetes_en_cours += 1
    try:
        attente = 0.003 + 0.018 * (requetes_en_cours - 1) * random.uniform(0.4, 1.6)
        await asyncio.sleep(min(attente, 0.9))
    finally:
        requetes_en_cours -= 1


def trouver_categorie(identifiant: str) -> dict:
    for categorie in CATEGORIES:
        if categorie["id"] == identifiant:
            return categorie
    raise HTTPException(status_code=404, detail="catégorie inconnue")


@app.get("/", response_class=HTMLResponse)
def page_billetterie():
    lignes = "".join(
        f"<tr><td>{escape(c['nom'])}</td><td>{c['prix']} €</td><td>{c['stock']}</td></tr>"
        for c in CATEGORIES
    )
    return f"""<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>{escape(FESTIVAL)} — billetterie Kelvia</title>
  <style>
    body {{ font-family: sans-serif; max-width: 40em; margin: 2em auto; }}
    table {{ border-collapse: collapse; width: 100%; }}
    th, td {{ border: 1px solid #ccc; padding: 0.5em; text-align: left; }}
  </style>
</head>
<body>
  <h1>{escape(FESTIVAL)}</h1>
  <p>Billetterie en ligne Kelvia. Jusqu'à {QUANTITE_MAX} billets par commande.</p>
  <table>
    <tr><th>Catégorie</th><th>Prix</th><th>Places restantes</th></tr>
    {lignes}
  </table>
  <p><small>Cas fictif, exercice pédagogique.</small></p>
</body>
</html>
"""


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/billets")
async def lister_billets():
    await latence_simulee()
    return CATEGORIES


@app.post("/billets", status_code=201)
async def commander(commande: Commande):
    await latence_simulee()
    categorie = trouver_categorie(commande.categorie)
    try:
        quantite = verifier_quantite(commande.quantite)
        nom = valider_nom(commande.nom)
    except ValueError as erreur:
        raise HTTPException(status_code=422, detail=str(erreur))
    if quantite > categorie["stock"]:
        raise HTTPException(status_code=409, detail="stock insuffisant")
    categorie["stock"] -= quantite
    return {"categorie": categorie["id"], "quantite": quantite, "nom": nom, "total": quantite * categorie["prix"]}
