from __future__ import annotations

import os
import pickle
from pathlib import Path
from typing import Any

import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field


API_DIR = Path(__file__).resolve().parent


def _default_column_paths() -> list[Path]:
    return [
        API_DIR / "models" / "column" / "pretrained_model.pkl",
        API_DIR / "models" / "column" / "model.txt",
    ]


def _default_wall_paths() -> list[Path]:
    return [
        API_DIR / "models" / "wall" / "pretrained_model.pkl",
        API_DIR / "models" / "wall" / "model.txt",
    ]


def _path_from_env(name: str, defaults: list[Path]) -> list[Path]:
    value = os.getenv(name, "").strip()
    if not value:
        return defaults
    parts = [v.strip() for v in value.split(";") if v.strip()]
    resolved: list[Path] = []
    for part in parts:
        p = Path(part)
        if not p.is_absolute():
            p = (API_DIR.parent / p).resolve()
        resolved.append(p)
    return resolved or defaults


def _load_model(paths: list[Path]) -> Any:
    for p in paths:
        if not p.exists():
            continue
        if p.suffix.lower() in {".pkl", ".pickle"}:
            with p.open("rb") as fh:
                return pickle.load(fh)

        if p.suffix.lower() in {".txt", ".model"}:
            try:
                import lightgbm as lgb
            except Exception as exc:  # pragma: no cover
                raise RuntimeError("lightgbm is required to load .txt model files") from exc
            return lgb.Booster(model_file=str(p))

    expected = "\n".join(str(p) for p in paths)
    raise FileNotFoundError(
        "No model file found. Place an exact Colab model file at one of:\n" + expected
    )


class ColumnInput(BaseModel):
    a: float = Field(..., gt=0)
    d: float = Field(..., gt=0)
    s: float = Field(..., gt=0)
    fc: float = Field(..., gt=0)
    fyl: float = Field(..., gt=0)
    fyt: float = Field(..., gt=0)
    rhol: float = Field(..., ge=0)
    rhot: float = Field(..., ge=0)
    v: float = Field(..., ge=0)
    lbd: float = Field(..., gt=0)


class WallInput(BaseModel):
    fc: float = Field(..., gt=0)
    Lw: float = Field(..., gt=0)
    t: float = Field(..., gt=0)
    h: float = Field(..., gt=0)
    s: float = Field(..., gt=0)
    rholb: float = Field(..., ge=0)
    rhotb: float = Field(..., ge=0)
    Fy: float = Field(..., gt=0)
    ALR: float = Field(..., ge=0)


app = FastAPI(title="Liam Pledger Model API", version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


_column_model_error: str | None = None
_wall_model_error: str | None = None
_column_model: Any | None = None
_wall_model: Any | None = None


def _unwrap_model(obj: Any) -> Any:
    if isinstance(obj, dict):
        for key in ("model", "booster", "bst", "estimator"):
            candidate = obj.get(key)
            if candidate is not None:
                return candidate
    return obj


def _predict_model(model: Any, x: np.ndarray) -> float:
    target = _unwrap_model(model)
    if not hasattr(target, "predict"):
        raise RuntimeError("Loaded model does not provide a predict() method.")

    y = target.predict(x)
    arr = np.asarray(y, dtype=float).reshape(-1)
    if arr.size == 0:
        raise RuntimeError("Model returned an empty prediction.")
    return float(arr[0])


def _safe_load_models() -> None:
    global _column_model, _wall_model, _column_model_error, _wall_model_error

    column_paths = _path_from_env("COLUMN_MODEL_PATHS", _default_column_paths())
    wall_paths = _path_from_env("WALL_MODEL_PATHS", _default_wall_paths())

    try:
        _column_model = _load_model(column_paths)
        _column_model_error = None
    except Exception as exc:
        _column_model = None
        _column_model_error = str(exc)

    try:
        _wall_model = _load_model(wall_paths)
        _wall_model_error = None
    except Exception as exc:
        _wall_model = None
        _wall_model_error = str(exc)


@app.on_event("startup")
def _startup() -> None:
    _safe_load_models()


@app.get("/health")
def health() -> dict[str, Any]:
    return {
        "ok": True,
        "column_model_loaded": _column_model is not None,
        "wall_model_loaded": _wall_model is not None,
        "column_model_error": _column_model_error,
        "wall_model_error": _wall_model_error,
    }


@app.post("/reload-models")
def reload_models() -> dict[str, Any]:
    _safe_load_models()
    return health()


@app.post("/predict/column")
def predict_column(payload: ColumnInput) -> dict[str, float]:
    if _column_model is None:
        raise HTTPException(status_code=503, detail=_column_model_error or "Column model not loaded")

    # Exact feature order used in the Colab inference function:
    # [a, a/d, fyt, s/d, fc, v, s/lbd, a/s, rhol*fyl, rhot*fyt]
    x = np.array(
        [[
            payload.a,
            payload.a / payload.d,
            payload.fyt,
            payload.s / payload.d,
            payload.fc,
            payload.v,
            payload.s / payload.lbd,
            payload.a / payload.s,
            payload.rhol * payload.fyl,
            payload.rhot * payload.fyt,
        ]],
        dtype=float,
    )
    y_pred = _predict_model(_column_model, x)
    return {"drift_capacity": y_pred}


@app.post("/predict/wall")
def predict_wall(payload: WallInput) -> dict[str, float]:
    if _wall_model is None:
        raise HTTPException(status_code=503, detail=_wall_model_error or "Wall model not loaded")

    # Exact feature order used in the Colab inference function:
    # [h/Lw, Lw/t, fc, t/h, s/h, rholb*Fy, rhotb*Fy, ALR]
    x = np.array(
        [[
            payload.h / payload.Lw,
            payload.Lw / payload.t,
            payload.fc,
            payload.t / payload.h,
            payload.s / payload.h,
            payload.rholb * payload.Fy,
            payload.rhotb * payload.Fy,
            payload.ALR,
        ]],
        dtype=float,
    )
    y_pred = _predict_model(_wall_model, x)
    return {"drift_capacity": y_pred}
