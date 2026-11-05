# Preuve d'idempotence — pizzeria Nova (exemple)

<!-- Yaël : remplacer les deux blocs par les sorties réelles du second passage sur le dépôt Nova, copiées depuis un codespace. Ne rien réécrire à la main. -->

## Second `terraform apply`

```text
À REMPLACER : sortie réelle du second terraform apply sur Nova
```

Ce qui prouve l'idempotence : aucune ressource ajoutée, modifiée ni détruite.

## Second `ansible-playbook -i inventaire.yaml site.yaml`

```text
À REMPLACER : sortie réelle du second ansible-playbook sur Nova, PLAY RECAP compris
```

Ce qui prouve l'idempotence : dans le PLAY RECAP, `changed=0` pour chaque machine.
