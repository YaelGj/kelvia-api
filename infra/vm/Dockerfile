# Image des « VM » de Kelvia : une Debian minimale avec Python,
# pour qu'Ansible puisse s'y connecter (python3-apt est exigé par le module apt).
FROM debian:13.7-slim
RUN apt-get update \
    && apt-get install -y --no-install-recommends python3 python3-apt \
    && rm -rf /var/lib/apt/lists/*
CMD ["sleep", "infinity"]
