# Migration vers le cloud — pizzeria Nova (exemple)

Binôme : Léa et Hugo

> Exemple de format sur un composant qui n'existe pas chez Kelvia : le registre d'images de Nova.

## Stratégies

| Composant | Stratégie (7 R) | Justification |
|---|---|---|
| Registre d'images Docker, installé à la main sur un serveur loué | Replatform | On garde les mêmes images, mais le registre devient un service managé. |

## Services équivalents

| Composant | AWS | GCP | Azure |
|---|---|---|---|
| Registre d'images | [Amazon Elastic Container Registry](https://docs.aws.amazon.com/AmazonECR/latest/userguide/what-is-ecr.html) | [Artifact Registry](https://docs.cloud.google.com/artifact-registry/docs/overview) | [Azure Container Registry](https://learn.microsoft.com/en-us/azure/container-registry/container-registry-intro) |

## Risques

| Risque | Mesure qui le réduit |
|---|---|
| Une image oubliée pendant la copie : un déploiement échoue après la bascule | Lister les images utilisées en production et vérifier leur présence dans le nouveau registre avant d'arrêter l'ancien. |
