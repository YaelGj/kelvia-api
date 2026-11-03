# SLO de /commandes — pizzeria Nova (exemple)

> Exemple de format. Les valeurs de Nova (800 ms, 99 %) ne sont pas celles attendues pour Kelvia.

## SLI

Latence de /commandes au 95e centile, lue sur le panneau « Latence 95e centile /commandes ».

Valeur relevée sous charge : 0,31 s.

## SLO

SLI sous 800 ms pendant 99 % du temps, sur 30 jours glissants.

## Error budget sur 30 jours

30 jours = 43 200 min.
1 % de 43 200 min = 432 min, soit 7 h 12 au-dessus de 800 ms.

## Quand le budget est épuisé

L'équipe fige les nouvelles fonctionnalités et ne livre que des corrections de fiabilité jusqu'à ce que le budget se reconstitue.
