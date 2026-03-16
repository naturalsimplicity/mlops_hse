import os
import time
from pathlib import Path

import numpy as np
import mlflow
import mlflow.sklearn
from fastapi import FastAPI, Response
from pydantic import BaseModel, Field
from prometheus_client import (
    Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
)


REQUEST_COUNT = Counter(
    "mlservice_requests_total",
    "Number of requests to the ML model",
    ["endpoint"]
)

PREDICTION_TIME = Histogram(
    "mlservice_prediction_seconds",
    "Time spent on prediction",
    buckets=(0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 2)
)


class DiabetesFeatures(BaseModel):
    age: float = Field(..., description="age")
    sex: float = Field(..., description="sex")
    bmi: float = Field(..., description="bmi")
    bp: float = Field(..., description="bp")
    s1: float = Field(..., description="s1")
    s2: float = Field(..., description="s2")
    s3: float = Field(..., description="s3")
    s4: float = Field(..., description="s4")
    s5: float = Field(..., description="s5")
    s6: float = Field(..., description="s6")


def create_app() -> FastAPI:
    app = FastAPI(title="Diabetes ML Service", version="1.0.0")

    @app.on_event("startup")
    def _load_model() -> None:
        model_dir = Path(__file__).resolve().parent / "model"
        model_dir.mkdir(exist_ok=True)

        mlflow_tracking_uri = os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000")
        model_name = os.getenv("MLFLOW_MODEL_NAME", "diabets")
        model_version = os.getenv("MLFLOW_MODEL_VERSION", "1")

        mlflow.set_tracking_uri(mlflow_tracking_uri)

        model_uri = f"models:/{model_name}/{model_version}"

        if not (model_dir / "MLmodel").exists():
            model = mlflow.sklearn.load_model(model_uri, dst_path=str(model_dir))

        app.state.model = mlflow.sklearn.load_model(str(model_dir))

    @app.post("/api/v1/predict")
    def predict(payload: DiabetesFeatures) -> dict:
        start_time = time.perf_counter()
        REQUEST_COUNT.labels(endpoint="/api/v1/predict").inc()

        x = np.array([[
            payload.age, payload.sex, payload.bmi, payload.bp,
            payload.s1, payload.s2, payload.s3, payload.s4,
            payload.s5, payload.s6
        ]], dtype=float)

        y_pred = float(app.state.model.predict(x)[0])

        duration = time.perf_counter() - start_time
        PREDICTION_TIME.observe(duration)

        return {"predict": y_pred}

    @app.get("/metrics")
    def get_metrics() -> Response:
        """
        Экспорт метрик для Prometheus
        """
        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    return app


app = create_app()
