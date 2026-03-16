## Airflow

Запуск

```shell
# без выдачи прав миграции не пройдут
sudo chmod -R 777 dags logs plugins
echo -e "AIRFLOW_UID=$(id -u)" > .env

docker compose up -d db
docker compose run --rm airflow.db.init
docker compose run --rm airflow.db.migrate
docker compose up -d airflow.webserver airflow.scheduler airflow.triggerer
```

Создание суперпользователя

```shell
docker compose exec -it airflow.webserver bash
airflow users create \
  --username admin \
  --firstname Matvey \
  --lastname Vasheka \
  --role Admin \
  --email vasheka@matvey.com \
  --password change_me
```
