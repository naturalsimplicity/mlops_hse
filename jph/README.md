# Генерация JUPYTERHUB_CRYPT_KEY
openssl rand -hex 32

# Генерация JUPYTERHUB_COOKIE_SECRET
openssl rand -hex 32

# Сборка образа
docker compose build

# Запуск сервисов
docker compose up -d

# Просмотр логов
docker compose logs -f

# Логи JupyterHub
docker compose logs jupyterhub

# Логи PostgreSQL
docker compose logs postgres
