from __future__ import annotations

from pathlib import Path
import numpy as np
from fastapi import FastAPI
from pydantic import BaseModel, Field

import mlflow.sklearn


class DiabetesFeatures(BaseModel):
    # 10 признаков из sklearn.datasets.load_diabetes (feature_names)
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
        # Модель кладём в mlapp/model (формат MLflow)
        model_dir = Path(__file__).resolve().parent / "model"
        if not model_dir.exists():
            raise RuntimeError(
                f"Model directory not found: {model_dir}. "
                "Train and export model into mlapp/model first."
            )

        # load_model умеет грузить и по URI, и с локального пути
        app.state.model = mlflow.sklearn.load_model(str(model_dir))

    @app.post("/api/v1/predict")
    def predict(payload: DiabetesFeatures) -> dict:
        x = np.array([[
            payload.age, payload.sex, payload.bmi, payload.bp, payload.s1,
            payload.s2, payload.s3, payload.s4, payload.s5, payload.s6
        ]], dtype=float)

        y_pred = float(app.state.model.predict(x)[0])
        return {"predict": y_pred}

    return app


app = create_app()
