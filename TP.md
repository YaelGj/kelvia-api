# TP — Kelvia, billetterie en ligne (cas fictif, exercice pédagogique)

Vous êtes la nouvelle équipe DevOps de Kelvia. Chaque étape se termine par **Vous devez voir** : si vous ne le voyez pas, ne passez pas à la suite, relisez l'étape ou demandez à votre binôme.

**Point d'étape** : toutes les 20 minutes, une ligne dans le chat : le TP, le numéro de l'étape, et « OK » ou « bloqué ».

**En retard ?** Voir la section « Repartir d'un point de reprise » du README, quand le formateur vous le propose.

**Après le TP 2, étape 2** : `main` est protégée. Partout où ce fichier dit « Commit, push », travaillez sur une branche, poussez-la, ouvrez une pull request et fusionnez quand le check `tests` est vert.

**Bloqué par un message d'erreur ?** Voir « Erreurs fréquentes » à la fin de ce fichier.

---

## TP 0 — Votre billetterie en ligne (30 min)

À faire avant le cours (J-2) : créer votre dépôt public avec « Use this template » sur le dépôt modèle, sur votre compte personnel, puis créer son codespace (Code → Codespaces). Dans le terminal du codespace, lancer une fois `docker compose pull` : les images seront déjà téléchargées le jour du TP 4.

1. Dans le terminal du codespace : `uvicorn app.main:app --reload`. Ouvrez le port 8000 (onglet Ports), en visibilité Private.
   **Vous devez voir** : la page de billetterie de Kelvia.
2. Dans `app/main.py`, remplacez la valeur de `FESTIVAL` par le nom de votre choix et enregistrez.
   **Vous devez voir** : le nouveau nom après rechargement de la page.
3. Invitez votre binôme comme collaborateur (Settings → Collaborators) et activez la protection au push des secrets dans les réglages de sécurité du dépôt.
4. Remplissez `EQUIPE.md` (prénom seulement), puis :
   ```
   git add -A
   git commit -m "TP 0 : mon festival"
   git push
   ```
   **Vous devez voir** : votre commit sur la page GitHub du dépôt. Collez le lien du dépôt dans le chat.

---

## TP 1 — Étude de cas : diagnostic et rôles (50 min, en binôme)

Consignes et données : slides du TP 1. Format du fichier : `exemples/diagnostic-nova.md`.
Livrable : `DIAGNOSTIC.md` à la racine du dépôt de l'un des deux, avec vos deux prénoms.

---

## TP 2 — Du commit à la release (150 min)

Avant de commencer : arrêtez uvicorn (Ctrl+C) si vous ne vous en servez plus.

### Étape 1 — Le pipeline vérifie chaque pull request
1. `git switch -c ajout-ci`
2. Écrivez `.github/workflows/ci.yml` en suivant la slide « Anatomie d'un workflow GitHub Actions » (le job s'appelle `tests`).
3. `git add -A`, `git commit -m "Ajout de la CI"`, `git push -u origin ajout-ci`, puis ouvrez une pull request sur GitHub.
4. Votre binôme commente au moins une ligne et approuve. Vous faites de même dans son dépôt. Si votre binôme est absent, fusionnez quand même : la relecture se fera plus tard.
   **Vous devez voir** : la pastille verte sur la pull request. Fusionnez.

### Étape 2 — main est protégée
1. Créez le ruleset de `main` (slide « Protéger main avec un ruleset ») : pull request obligatoire avec 0 approbation requise, check `tests` obligatoire.
2. `git switch main`, `git pull`, puis `git switch -c test-protection`.
3. Dans `app/main.py`, changez le prix d'un billet. Commit, push, pull request.
   **Vous devez voir** : la pastille rouge et le bouton de fusion bloqué.
4. Remettez le prix d'origine, commit, push.
   **Vous devez voir** : le retour au vert. Fusionnez. Faites une capture du ruleset et de la fusion bloquée dans `docs/`.

### Étape 3 — Livrer la v1.0.0
1. Dans `CHANGELOG.md`, ajoutez au-dessus de v0.1.0 une section v1.0.0 qui résume les TP 0 à 2 (format : slide « Livrer une version avec un tag »).
2. Créez `.github/workflows/livraison.yml` à partir de ce modèle et remplacez A, B, C et D (slide « Exercice : complétez le workflow »). Différence avec l'exercice : le jeton n'est donné qu'à la dernière étape, la seule qui en a besoin.
   ```yaml
   name: livraison
   on: {push: {___A___: ["v*"]}}
   permissions:
     contents: ___B___
   jobs:
     release:
       runs-on: ___C___
       steps:
         - uses: actions/checkout@v7
           with: {persist-credentials: false}
         - uses: actions/setup-python@v7
           with: {python-version: "3.12"}
         - run: pip install -r requirements.txt
         - run: pytest
         - run: gh release create "$GITHUB_REF_NAME" -F CHANGELOG.md
           env:
             ___D___: ${{ secrets.GITHUB_TOKEN }}
   ```
3. Passez par une pull request, fusionnez, puis :
   ```
   git switch main
   git pull
   git tag v1.0.0
   git push origin v1.0.0
   ```
   **Vous devez voir** : la release v1.0.0 dans l'onglet Releases, avec le texte de votre CHANGELOG.

**Prolongements** : badge d'état du workflow dans `README.md` ; tag `v1.0.1-test` posé sur des tests rouges : aucune release ne doit apparaître.

---

## TP 3 — L'infrastructure de Kelvia en code (60 min)

Tout se passe dans le dossier `infra/` : `cd infra`.

1. Complétez `main.tf` aux endroits marqués « À compléter » : un réseau `kelvia` et les conteneurs `vm-web-1` et `vm-web-2`, avec `image = docker_image.vm.image_id` et la page publiée sur les ports 8081 et 8082 (slide « Une ressource Terraform »). Puis :
   ```
   terraform init
   terraform plan
   terraform apply
   ```
   **Vous devez voir** : sur les ports 8081 et 8082, une page « Kelvia — machine en attente de configuration ».
2. Regardez `inventaire.yaml` (groupes `recette` et `production`) et le dossier `group_vars/`, puis lancez le playbook fourni :
   ```
   ansible-playbook -i inventaire.yaml site.yaml
   ```
   **Vous devez voir** : un bandeau RECETTE sur le port 8081 et un bandeau PRODUCTION sur le port 8082, produits par le même playbook.
3. Thomas veut mettre la production en maintenance avant l'ouverture des ventes. Dans `group_vars/production.yml`, passez `maintenance` à `true`, puis relancez la même commande.
   **Vous devez voir** : la page de production affiche « Maintenance en cours » ; la recette ne change pas.
   Remettez `maintenance: false` et relancez.
4. Relancez `terraform apply`, puis le playbook, sans rien changer.
   **Vous devez voir** : « No changes » et `changed=0`. Recopiez les deux sorties telles quelles dans `IDEMPOTENCE.md` à la racine (modèle : `exemples/idempotence-nova.md`). Commit, push.

**Prolongement** : passez le nombre de machines à 3 (une seule variable), `terraform apply`, décommentez `vm-web-3` dans le groupe `production` de `inventaire.yaml`, relancez le playbook : une troisième page de production apparaît sur le port 8083.

---

## TP 4, partie 1 — Conteneuriser l'API (50 min, à enchaîner avec le TP 3)

Avant de commencer : arrêtez uvicorn s'il tourne encore (le port 8000 doit être libre). Revenez à la racine du dépôt.

1. Écrivez le `Dockerfile` (slide « Une image se construit avec un Dockerfile »), puis :
   ```
   docker build -t kelvia .
   docker run --rm -p 8000:8000 kelvia
   ```
   **Vous devez voir** : la page de billetterie sur le port 8000. Arrêtez le conteneur avec Ctrl+C.
2. Ajoutez le service `api` à `compose.yaml`, avec sa vérification de santé (slide « Plusieurs conteneurs avec Docker Compose »), puis :
   ```
   docker compose up -d
   docker compose ps
   ```
   **Vous devez voir** : `api` en `healthy` (patientez quelques secondes).
3. Changez un texte de la page dans `app/main.py`, puis `docker compose up -d --build`.
   **Vous devez voir** : la modification sur le port 8000. Commit, push (avec une capture de `docker compose ps`).

**Prolongement** : un job du pipeline qui construit l'image à chaque pull request.

---

## TP 4, parties 2 et 3 — Observer Kelvia et provoquer une panne (70 min)

1. Dans `app/main.py`, décommentez le bloc d'instrumentation (lignes marquées « TP 4 »), puis `docker compose up -d --build`. Ouvrez Grafana (port 3000, identifiant et mot de passe initiaux `admin`), tableau de bord « Kelvia ». Dans un second terminal : `./charge.sh`.
   **Vous devez voir** : les courbes de `/billets` monter. Puis arrêtez (Ctrl+C) et lancez `./charge.sh rush`.
   **Vous devez voir** : le pic d'ouverture des ventes sur les deux panneaux : le trafic et la latence montent.
2. Rédigez `SLO.md` à la racine (modèle : `exemples/slo-nova.md`) : le SLI lu sur le panneau de latence, la cible, l'error budget sur 30 jours en minutes.
3. La règle « une commande compte de 1 à 4 billets » est dans `app/main.py` (fonction citée dans le README). Écrivez dans `tests/` un test unitaire et un test d'intégration de cette règle (slide « Un test unitaire et un test d'intégration », modèle de refus : `tests/test_refus.py`). Lancez `pytest`.
   Passez la limite à 6 dans `app/main.py`, relancez `pytest`.
   **Vous devez voir** : votre test au rouge. Remettez 4 : tout repasse au vert. Commit, push : le pipeline doit être vert.
4. Rédigez la première partie de `CHAOS.md` (modèle : `exemples/chaos-nova.md`) : steady state, hypothèse, variable, critère d'arrêt. Avec `./charge.sh` qui tourne :
   ```
   docker compose stop api
   ```
   Attendez 2 minutes, puis :
   ```
   docker compose start api
   ```
   **Vous devez voir** : la page indisponible, des échecs dans `charge.sh`, « API joignable » à 0, puis tout revenir. Complétez `CHAOS.md` : ce qui s'est passé, délai de détection, écart avec l'hypothèse, une action d'amélioration. Commit, push, avec une capture du tableau de bord pendant l'expérience.

---

## TP 5 — Préparer la migration de Kelvia (25 min, en binôme)

Consignes et données : slides du TP 5. Format : `exemples/migration-nova.md`.
Livrable : `MIGRATION.md` à la racine du dépôt de l'un des deux, avec vos deux prénoms.

---

## Erreurs fréquentes

Copiez le message exact avant de demander de l'aide. Ce tableau dit où regarder, pas quoi taper.

| Message ou symptôme | Où regarder |
|---|---|
| `push declined due to repository rule violations` | `main` est protégée depuis le TP 2 : relisez l'encadré en tête de ce fichier. |
| `fatal: couldn't find remote ref …` ou `invalid reference: FETCH_HEAD` | Le nom du point de reprise, lettre par lettre. |
| `pytest` échoue juste après une reprise | Vos propres fichiers de test, conservés par la reprise. |
| `Interrupted: 1 error during collection` | `pytest.ini` est-il toujours à la racine du dépôt ? |
| `StarletteDeprecationWarning` | Un avertissement, pas une erreur : les tests passent-ils ? |
| Cible Prometheus en erreur (`no such host`), « API joignable » à 0 | Le service `api` existe-t-il dans `compose.yaml` ? (TP 4, partie 1) |
| Panneaux de requêtes et de latence vides pendant l'arrêt de l'API | Sans réponse, pas de mesure. Quel panneau mesure, lui, la disponibilité ? |
| `vm-web-3` garde la page « en attente de configuration » | Le fichier d'inventaire. |
| `timeout while waiting for state to become 'removed'` | Les lignes `-/+` du plan : une ressource remplacée est-elle encore utilisée par une autre ? |
| `env: 'bash\r': No such file or directory` ou `detected dubious ownership` | Vous travaillez hors de Codespaces : repassez sur votre codespace. |

---

N'oubliez pas d'arrêter votre codespace à la fin de chaque journée.
