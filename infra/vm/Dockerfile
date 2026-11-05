# Image des « VM » de Kelvia : Python sert le dossier /srv en HTTP sur le port 8000.
# Python sert aussi à Ansible, qui s'y connecte pour déposer la page /srv/index.html.
FROM python:3.12-slim
COPY index.html /srv/index.html
EXPOSE 8000
# SIGINT : la « VM » s'arrête tout de suite (sinon Docker attend 10 s avant de la tuer).
STOPSIGNAL SIGINT
CMD ["python", "-m", "http.server", "8000", "--directory", "/srv"]
