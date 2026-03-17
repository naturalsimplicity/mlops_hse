FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -r mlflow && useradd -r -g mlflow mlflow

WORKDIR /mlflow

RUN pip install --no-cache-dir \
    mlflow==3.10.1 \
    psycopg2-binary==2.9.9 \
    boto3==1.35.0

RUN mkdir -p /mlflow/artifacts && \
    chown -R mlflow:mlflow /mlflow && \
    chmod -R 755 /mlflow

USER mlflow

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

CMD mlflow server \
    --host 0.0.0.0 \
    --port 5000 \
    --backend-store-uri postgresql://${MLFLOW_DB_USER}:${MLFLOW_DB_PASSWORD}@${MLFLOW_DB_HOST}:${MLFLOW_DB_PORT}/${MLFLOW_DB_NAME} \
    --default-artifact-root ${MLFLOW_ARTIFACT_ROOT} \
    --serve-artifacts \
    --allowed-hosts ${MLFLOW_ALLOWED_HOSTS} \
    --dev
