# Kelvia — API de réservation de salles

> Cas fictif, exercice pédagogique. Module DevOps.

Kelvia est une entreprise fictive. Ses équipes réservent des salles de réunion avec une petite API web.
Les développeurs livrent d'un côté, les administrateurs exploitent de l'autre, et chaque mise en production fait peur.
Vous êtes la nouvelle équipe DevOps : ce dépôt est votre point de départ pour tous les TP.

## Contenu du dépôt

| Chemin | Rôle |
|---|---|
| `app/main.py` | L'API : `GET /health`, `GET /salles`, `POST /salles` |
| `tests/` | Tests pytest de l'API |
| `.devcontainer/devcontainer.json` | L'environnement de travail, décrit en code |
| `compose.yaml`, `monitoring/` | Prometheus et Grafana, avec le tableau de bord « Kelvia » |
| `charge.sh` | Envoie du trafic sur `/salles` (TP 4) |
| `infra/` | L'infrastructure de Kelvia en code : Terraform et Ansible (TP 3) |
| `exemples/` | Exemples de livrables, sur un autre cas fictif (la pizzeria Nova) |
| `docs/` | Vos captures d'écran |

## Règle métier

Une salle ne peut pas avoir une capacité négative. Cette règle est écrite dans la fonction
`verifier_capacite` de `app/main.py` : `POST /salles` avec une capacité négative est refusé avec le code 422.

## Lancer le codespace

1. Sur la page du dépôt : **Code → Codespaces → Create codespace on main**.
2. Attendre la fin de la création : la commande `postCreateCommand` de `.devcontainer/devcontainer.json`
   installe les dépendances Python, Ansible et la collection `community.docker`.
3. Dans le terminal, vérifier les outils :

```bash
docker version
terraform version
ansible --version
```

Après une modification de `.devcontainer/devcontainer.json` : palette de commandes (Ctrl+Maj+P),
**Codespaces: Rebuild Container**.

Arrêtez votre codespace en fin de journée (**Code → Codespaces → … → Stop codespace**) : il consomme votre quota tant qu'il tourne.

## Commandes utiles

```bash
pytest                                       # lancer les tests
uvicorn app.main:app --reload                # lancer l'API sur le port 8000
docker compose up -d                         # démarrer les services de compose.yaml
docker compose ps                            # état des services
docker compose down                          # arrêter et supprimer les services
./charge.sh                                  # envoyer du trafic sur /salles (Ctrl+C pour arrêter)
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

Un commit par TP, sur `main` (par pull request à partir du TP 2).

| TP | Livrable | Modèle de format |
|---|---|---|
| TP 1 | `DIAGNOSTIC.md` à la racine (dans le dépôt de l'un des deux) | `exemples/diagnostic-nova.md` |
| TP 2 | `CHANGELOG.md` : section v1.0.0 au-dessus de v0.1.0 | section v0.1.0 déjà présente |
| TP 3 | `IDEMPOTENCE.md` à la racine | `exemples/idempotence-nova.md` |
| TP 4 | `SLO.md` et `CHAOS.md` à la racine ; tests dans `tests/` | `exemples/slo-nova.md`, `exemples/chaos-nova.md`, `tests/test_refus.py` |
| TP 5 | `MIGRATION.md` à la racine (dans le dépôt de l'un des deux) | `exemples/migration-nova.md` |

Captures d'écran : dans `docs/`, nommées `tpN-sujet.png` (exemple : `docs/tp2-ruleset.png`).

Les fichiers de `exemples/` portent sur la pizzeria Nova : reprenez leur forme, pas leur contenu.

## Repartir d'un point de reprise

Si vous êtes en retard, le formateur peut vous donner le nom d'un point de reprise (`<tag>`).
Dans le terminal du codespace, à la racine du dépôt, remplacez `<tag>` par ce nom :

```bash
git fetch https://github.com/YaelGj/kelvia-api <tag>
git checkout FETCH_HEAD -- .
git commit -m "Reprise <tag>"
git push
```

Les fichiers du point de reprise remplacent les vôtres. Un fichier que vous avez créé et qui n'existe pas
dans le point de reprise est conservé tel quel. Si `main` est protégée par un ruleset,
faites ces commandes sur une branche et passez par une pull request.

## Problèmes fréquents

**Le port 8000 est déjà pris.** Un conteneur lancé à la main (`docker run -p 8000:8000 ...`) occupe encore le port.
Arrêtez-le (Ctrl+C dans son terminal, ou `docker ps` puis `docker stop <id>`) avant `docker compose up -d`.

**Visibilité des ports.** Laissez les ports en **Private** dans l'onglet Ports. Un port public exposerait
Grafana à tout Internet. Pour montrer votre écran, utilisez le partage d'écran.

**Première connexion à Grafana.** Port 3000, identifiant `admin`, mot de passe `admin`. Grafana demande ensuite
de choisir un nouveau mot de passe. Le tableau de bord « Kelvia » est dans **Dashboards**.
