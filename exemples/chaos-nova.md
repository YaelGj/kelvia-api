# Expérience de chaos — pizzeria Nova (exemple)

> Exemple de format sur une autre panne que celle du TP : ici, le service de paiement de Nova.

## Avant l'expérience

**Steady state** : /commandes répond à environ 5 requêtes par seconde, latence au 95e centile sous 800 ms (panneaux « Requêtes par seconde /commandes » et « Latence 95e centile /commandes »).

**Hypothèse** : si le service de paiement s'arrête 2 minutes, /commandes continue de répondre sous 800 ms et la panne est visible sur le tableau de bord en moins d'une minute.

**Variable** : `docker compose stop paiement` pendant 2 minutes, puis `docker compose start paiement`.

**Critère d'arrêt** : si /commandes ne répond plus pendant plus de 30 secondes, relancer le paiement tout de suite.

## Après l'expérience

**Ce qui s'est passé** : /commandes a continué de répondre ; les nouvelles commandes ont été refusées au moment du paiement.

**Délai de détection** : 50 secondes, en regardant le tableau de bord.

**Écart avec l'hypothèse** : confirmée pour la latence ; mais personne n'aurait vu la panne sans regarder l'écran.

**Action d'amélioration** : une alerte sur la part de paiements refusés.
