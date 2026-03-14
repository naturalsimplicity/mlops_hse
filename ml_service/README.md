# ML service

## how to run Mlflow

```shell
mlflow server \
  --backend-store-uri sqlite:///mlflow.db \
  --default-artifact-root ./mlruns \
  --host 0.0.0.0 \
  --port 5000
```

## how to run service

```shell
docker compose up --build
```

## how to test

```shell
curl -s -X POST "http://127.0.0.1:8000/api/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "age": 59, "sex": 2, "bmi": 32.1, "bp": 101,
    "s1": 157, "s2": 93.2, "s3": 38, "s4": 4.1, "s5": 5.2, "s6": 87
  }'

```
