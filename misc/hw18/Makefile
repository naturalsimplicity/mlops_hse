.PHONY: dev.install db.migration.new db.migrate db.rollback db.up db.down db.status

dev.install:
	python -m venv venv
	. venv/bin/activate && pip install --upgrade pip
	. venv/bin/activate && pip install -r requirements.txt
	@echo "✅ Зависимости установлены. Активируйте окружение: source venv/bin/activate"

db.migration.new:
	@if [ -z "$(name)" ]; then \
		echo "Ошибка: необходимо указать имя миграции"; \
		echo "Использование: make db.migration.new name=\"описание миграции\""; \
		exit 1; \
	fi
	yoyo new ./migrations -m "$(name)"

db.migrate:
	yoyo apply --database $$(grep DATABASE_URL .env | cut -d '=' -f2) ./migrations

db.rollback:
	yoyo rollback --database $$(grep DATABASE_URL .env | cut -d '=' -f2) ./migrations

db.status:
	yoyo list --database $$(grep DATABASE_URL .env | cut -d '=' -f2) ./migrations

db.up:
	docker compose up -d db
	@echo "Ожидание готовности базы данных..."
	@sleep 5
	@echo "База данных запущена"

db.down:
	docker compose down

db.connect:
	docker compose exec db psql -U $$(grep POSTGRES_USER .env | cut -d '=' -f2) -d $$(grep POSTGRES_DB .env | cut -d '=' -f2)
