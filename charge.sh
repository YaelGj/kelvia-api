#!/usr/bin/env bash
# Envoie du trafic sur /billets et affiche le code HTTP de chaque réponse.
#   ./charge.sh        environ 5 requêtes par seconde
#   ./charge.sh rush   ouverture des ventes : 60 s de trafic bien plus fort, puis retour au rythme normal
# 200 : la requête a réussi. 000 : l'API n'a pas répondu (ÉCHEC).
# Arrêt : Ctrl+C.

appeler() {
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 2 http://localhost:8000/billets)
  if [ "$code" = "200" ]; then
    echo "$(date +%H:%M:%S) /billets $code"
  else
    echo "$(date +%H:%M:%S) /billets $code ÉCHEC"
  fi
}

if [ "${1:-}" = "rush" ]; then
  # Ctrl+C arrête aussi les clients lancés en parallèle.
  trap 'kill $(jobs -p) 2>/dev/null; exit 130' INT TERM
  echo "Ouverture des ventes : 20 clients en parallèle pendant 60 s."
  fin=$(( $(date +%s) + 60 ))
  for client in $(seq 20); do
    while [ "$(date +%s)" -lt "$fin" ]; do appeler; done &
  done
  wait
  echo "Fin du pic : retour au rythme normal."
fi

while true; do
  appeler
  sleep 0.2
done
