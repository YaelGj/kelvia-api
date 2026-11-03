#!/usr/bin/env bash
# Appelle /salles environ 5 fois par seconde et affiche le code HTTP de chaque réponse.
# 200 : la requête a réussi. 000 : l'API n'a pas répondu.
# Arrêt : Ctrl+C.
while true; do
  code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 1 http://localhost:8000/salles)
  if [ "$code" = "200" ]; then
    echo "$(date +%H:%M:%S) /salles $code"
  else
    echo "$(date +%H:%M:%S) /salles $code ÉCHEC"
  fi
  sleep 0.2
done
