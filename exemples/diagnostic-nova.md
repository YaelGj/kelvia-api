# Diagnostic — pizzeria Nova (exemple)

Binôme : Léa et Hugo

> Exemple de format sur un autre cas que Kelvia. Les chiffres viennent des données de Nova ci-dessous, pas de celles de Kelvia.

Données de Nova (mars 2026) : 12 déploiements ; 3 annulés en urgence, rétablis en 1 h, 2 h et 6 h ; changements commités les 2, 4 et 9 mars, tous déployés le 12 mars ; 1 déploiement non planifié après une panne du paiement.

## 1. Métriques DORA

| Métrique | Calcul | Résultat |
|---|---|---|
| Deployment frequency | 12 déploiements sur 1 mois | 12 par mois |
| Change lead time moyen | (10 + 8 + 3) / 3 jours | 7 jours |
| Change fail rate | 3 / 12 | 25 % |
| Failed deployment recovery time moyen | (1 + 2 + 6) / 3 heures | 3 h |

## 2. Frictions et enjeux métier

| Friction (citation) | Enjeu métier |
|---|---|
| Karim (cuisine) : « On découvre les nouvelles recettes sur le site le jour même. » | Image auprès des clients : une pizza affichée mais pas encore préparable. |

## 3. Rôles

Un seul responsable par tâche.

| Tâche | Responsable | Participants |
|---|---|---|
| Renouveler le certificat HTTPS du site | SysOps | DevOps |
| Supprimer les comptes des anciens stagiaires | DevSecOps | SysOps |

## 4. Contrôle décalé à gauche

| Contrôle | Moment du cycle |
|---|---|
| Recherche de secrets dans le code | Au moment du push, avant que le commit n'arrive sur GitHub |

## 5. Prolongement

Deployment rework rate : 1 déploiement non planifié sur 12, soit environ 8 %. Un déploiement sur douze sert à réparer une panne.
