# Jupyterhub

## Запуск сервисов
docker compose up -d
docker compose exec jupyterhub bash -c "echo 'admin:admin123' | chpasswd"

## Логи JupyterHub
docker compose logs jupyterhub
