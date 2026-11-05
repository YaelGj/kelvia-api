# Kelvia — billetterie en ligne de festivals

> Cas fictif, exercice pédagogique. Module DevOps.

Kelvia est une entreprise fictive qui vend en ligne les billets de festivals de musique.
Les développeurs livrent d'un côté, les administrateurs exploitent de l'autre, et chaque mise en production fait peur,
surtout la veille d'une ouverture des ventes. Vous êtes la nouvelle équipe DevOps : ce dépôt est votre point de départ pour tous les TP.

**Consignes des TP : [TP.md](TP.md).**

## Contenu du dépôt

| Chemin | Rôle |
|---|---|
| `app/main.py` | L'API : page de billetterie `GET /`, `GET /health`, `GET /billets`, `POST /billets` |
| `tests/` | Tests pytest de l'API |
| `.devcontainer/` | L'environnement de travail, décrit en code |
| `compose.yaml`, `monitoring/` | Prometheus et Grafana, avec le tableau de bord « Kelvia » |
| `charge.sh` | Envoie du trafic sur `/billets` (TP 4) |
| `infra/` | L'infrastructure de Kelvia en code : Terraform et Ansible (TP 3) |
| `exemples/` | Exemples de livrables, sur un autre cas fictif (la pizzeria Nova) |
| `docs/` | Vos captures d'écran |

## Règle métier

Une commande compte de 1 à 4 billets. Cette règle est écrite dans la fonction `verifier_quantite` de `app/main.py`
(limite : `QUANTITE_MAX`) : `POST /billets` avec une quantité hors de cet intervalle est refusé avec le code 422.

## Lancer le codespace

1. Sur la page du dépôt : **Code → Codespaces → Create codespace on main**.
2. Attendre la fin de la création : `.devcontainer/post-create.sh` installe les dépendances Python,
   Ansible et la collection `community.docker`.
3. Dans le terminal, vérifier les outils :

```bash
docker version
terraform version
ansible --version
```

Arrêtez votre codespace en fin de journée (**Code → Codespaces → … → Stop codespace**) : il consomme votre quota tant qu'il tourne.

## Commandes utiles

```bash
pytest                                       # lancer les tests
uvicorn app.main:app --reload                # lancer l'API sur le port 8000
docker compose up -d                         # démarrer les services de compose.yaml
docker compose ps                            # état des services
docker compose down                          # arrêter et supprimer les services
./charge.sh                                  # environ 5 requêtes par seconde sur /billets (Ctrl+C pour arrêter)
./charge.sh rush                             # ouverture des ventes : un pic de trafic d'une minute
```

Infrastructure (depuis le dossier `infra/`) :

```bash
cd infra
terraform init
terraform plan
terraform apply
ansible-playbook -i inventaire.yaml site.yaml
```

Ports transférés par le codespace : 8000 (API), 3000 (Grafana), 9090 (Prometheus). Onglet **Ports** de l'éditeur.

## Livrables : format et emplacement

Consignes détaillées de chaque TP : `TP.md`. Un commit par étape livrée, sur `main` (par pull request à partir du TP 2).

| TP | Livrable | Modèle de format |
|---|---|---|
| TP 1 | `DIAGNOSTIC.md` à la racine (dans le dépôt de l'un des deux) | `exemples/diagnostic-nova.md` |
| TP 2 | `.github/workflows/ci.yml`, `.github/workflows/livraison.yml`, `CHANGELOG.md` : section v1.0.0 au-dessus de v0.1.0 | section v0.1.0 déjà présente ; modèle à trous de livraison.yml dans `TP.md` |
| TP 3 | `IDEMPOTENCE.md` à la racine | `exemples/idempotence-nova.md` |
| TP 4 | `SLO.md` et `CHAOS.md` à la racine ; tests dans `tests/` | `exemples/slo-nova.md`, `exemples/chaos-nova.md`, `tests/test_refus.py` |
| TP 5 | `MIGRATION.md` à la racine (dans le dépôt de l'un des deux) | `exemples/migration-nova.md` |

Captures d'écran : dans `docs/`, nommées `tpN-sujet.png` (exemple : `docs/tp2-ruleset.png`).

Les fichiers de `exemples/` portent sur la pizzeria Nova : reprenez leur forme, pas leur contenu.

## Repartir d'un point de reprise

Seulement quand le formateur vous le propose : il vous donne le nom du point de reprise, noté `<tag>` ci-dessous.
Enregistrez d'abord votre travail en cours (commit), puis, dans le terminal du codespace :

```
git switch main
git pull
git switch -c rattrapage-<tag>
git fetch https://github.com/YaelGj/kelvia-api <tag>
git checkout FETCH_HEAD -- . ':!EQUIPE.md'
git commit -m "Reprise <tag>"
git push -u origin rattrapage-<tag>
```

Ouvrez ensuite une pull request vers `main` et fusionnez quand le check `tests` est vert : depuis le TP 2, `main` n'accepte plus de push direct.

Ce que fait la reprise : les fichiers du point de reprise remplacent les vôtres ; vos fichiers qui n'y figurent pas sont conservés ; `EQUIPE.md` n'est jamais touché.
**Vous devez voir** : la pull request au vert. Si `pytest` échoue, regardez d'abord vos propres fichiers de test conservés.

## Problèmes fréquents

**Le port 8000 est déjà pris.** Un autre programme l'occupe encore : l'API lancée avec `uvicorn` au TP 0
(Ctrl+C dans son terminal) ou un conteneur lancé à la main avec `docker run -p 8000:8000 …`
(Ctrl+C dans son terminal, ou `docker ps` puis `docker stop <id>`). Libérez-le avant `docker compose up -d`.

**Visibilité des ports.** Laissez les ports en **Private** dans l'onglet Ports. Un port public exposerait
Grafana à tout Internet. Pour montrer votre écran, utilisez le partage d'écran.

**Première connexion à Grafana.** Port 3000, identifiant `admin`, mot de passe `admin`. Grafana propose ensuite
de choisir un nouveau mot de passe. Le tableau de bord « Kelvia » est dans **Dashboards**.
