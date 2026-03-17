# Создать виртуальное окружение
python -m venv venv

# Активировать виртуальное окружение
source venv/bin/activate

# Установить зависимости
make dev.install

# Или вручную:
pip install -r requirements.txt

# Запустить PostgreSQL в Docker
make db.up

# Или вручную:
docker compose up -d db

# Проверить статус
docker compose ps

# Проверить статус миграций
make db.status

# Применить миграции
make db.migrate

# Откатить последнюю миграцию
make db.rollback

# Применить снова
make db.migrate

# Подключиться к базе данных
make db.connect

# Или вручную:
docker compose exec db psql -U testuser -d testdb

