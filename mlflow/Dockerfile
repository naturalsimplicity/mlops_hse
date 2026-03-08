FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir \
    mlflow==2.12.2 \
    psycopg2-binary==2.9.9

EXPOSE 5000
