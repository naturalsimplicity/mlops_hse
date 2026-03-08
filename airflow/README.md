## Airflow

Запуск

```shell
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
  --firstname Admin \
  --lastname User \
  --role Admin \
  --email admin@example.com \
  --password admin
exit
```
