FROM python:3.14-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Установка configurable-http-proxy
RUN npm install -g configurable-http-proxy

# Установка JupyterHub и необходимых пакетов
RUN pip install --no-cache-dir \
    jupyterhub \
    jupyterlab \
    notebook \
    dockerspawner \
    psycopg2-binary

# Создание директорий
RUN mkdir -p /srv/jupyterhub

# Установка рабочей директории
WORKDIR /srv/jupyterhub

# Открытие портов
EXPOSE 8000 8081

# Команда запуска
CMD ["jupyterhub", "-f", "/srv/jupyterhub/jupyterhub_config.py"]
