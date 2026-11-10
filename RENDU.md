# RENDU — Kelvia

Binôme (TP 1) : Camille et Léo
Remplacez seulement les `___` : une valeur lue à l'écran, ou un mot de la liste proposée.

## TP 1 — Diagnostic

Données : slide « TP 1 · données : Kelvia, six derniers mois ».

### 1. Métriques DORA

| Métrique | Calcul | Résultat |
|---|---|---|
| Deployment frequency | 7 déploiements sur 6 mois | 1,2 par mois |
| Change lead time moyen | (26 + 19 + 12 + 5) / 4 jours | 15,5 jours |
| Change fail rate | 2 / 7 | 29 % |
| Failed deployment recovery time moyen | (5 + 9) / 2 heures | 7 h |

### 2. Frictions et enjeux métier (2 lignes)

Pour au moins 2 lignes, choisissez l'enjeu : délai, coût ou image auprès des clients.

| Friction (citation) | Enjeu métier |
|---|---|
| Marc (exploitation) : « On reçoit le code le vendredi. » | délai |
| Sofia (développeuse) : « Je ne sais pas quand mon code part. » | délai |
| Thomas (CTO) : « Le jour de l'ouverture des ventes, ce sont les festivaliers qui nous ont prévenus de la panne. » | image auprès des clients |

### 3. Rôles : un seul responsable par tâche (SysOps, DevOps ou DevSecOps)

| Tâche | Responsable |
|---|---|
| 1 Écrire les tests de l'API | DevOps |
| 2 Mettre à jour le système des serveurs | SysOps |
| 3 Analyser les dépendances vulnérables | DevSecOps |
| 4 Écrire le pipeline d'intégration continue | DevOps |
| 5 Sauvegarder la base de données | SysOps |
| 6 Définir l'alerte de disponibilité | SysOps |
| 7 Stocker le mot de passe de la base | DevSecOps |
| 8 Revoir les droits d'accès à la production | DevSecOps |

### 4. Un contrôle de sécurité décalé à gauche

Contrôle, au choix : analyse des dépendances (pip-audit), protection au push des secrets, tests dans le pipeline.
Moment, au choix : à chaque push, à chaque pull request, avant la mise en production.

| Contrôle | Moment du cycle |
|---|---|
| analyse des dépendances (pip-audit) | à chaque pull request |

## TP 4 — SLO (Service Level Objective)

### SLI

Latence de /billets au 95e centile, lue sur le panneau « Latence 95e centile /billets ».
Valeur relevée sous `./charge.sh` : 0,005 s. Valeur relevée sous `./charge.sh rush` : 0,49 s.

### SLO

SLI sous 500 ms pendant 99,5 % du temps, sur 30 jours glissants.

### Error budget sur 30 jours

30 jours = 43 200 min.
0,5 % de 43 200 min = 216 min au-dessus de 500 ms.

### Quand le budget est épuisé

Au choix : on livre plus vite, on fige les nouveautés et on fiabilise, on baisse la cible.
L'équipe : on fige les nouveautés et on fiabilise

## TP 4 — Expérience de chaos
Remplissez « Avant l'expérience » avant d'arrêter quoi que ce soit.

### Avant l'expérience

**Steady state** : /billets répond à environ 5 requêtes par seconde, latence au 95e centile sous 500 ms (panneaux « Requêtes par seconde /billets » et « Latence 95e centile /billets »).

**Hypothèse** : si l'API s'arrête 2 minutes, la page devient indisponible (disponible ou indisponible) et la panne est visible sur le tableau de bord en moins de 30 secondes.

**Variable** : `docker compose stop api` pendant 2 minutes, puis `docker compose start api`.

**Critère d'arrêt** : si la panne dure plus de 5 minutes, relancer l'API (`docker compose start api`).

### Après l'expérience

**Ce qui s'est passé** : la page est devenue indisponible (disponible ou indisponible) ; les panneaux de trafic et de latence ont montré un trou (un trou ou des erreurs) ; « API joignable » est passé à 0.

**Délai de détection** : 8 secondes, sur le panneau « API joignable ».

**Écart avec l'hypothèse** : hypothèse confirmée (confirmée ou infirmée).

**Action d'amélioration**, au choix : une alerte sur « API joignable », une deuxième copie de l'API, les deux.
Votre choix : une alerte sur « API joignable »
