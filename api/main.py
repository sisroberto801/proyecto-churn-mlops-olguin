"""
API de predicción de churn con FastAPI.

La API carga un modelo serializado, valida los datos de entrada
y devuelve una predicción junto con su probabilidad.
"""

from pathlib import Path

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = PROJECT_ROOT / "models" / "modelo_churn_v1.joblib"

VERSION_MODELO = "modelo_churn_v1"
AUTOR = "Roberto Carlos Olguin Ledezma"

if not MODEL_PATH.exists():
    raise RuntimeError(
        "No se encontró el modelo serializado. "
        "Ejecute primero: python src\\entrenar_modelo.py"
    )

modelo = joblib.load(MODEL_PATH)


class ClienteEntrada(BaseModel):
    antiguedad: int = Field(
        ...,
        ge=0,
        le=120,
        description="Antigüedad del cliente expresada en meses",
        examples=[12],
    )
    cargo_mensual: float = Field(
        ...,
        ge=0,
        le=1000,
        description="Cargo mensual del cliente",
        examples=[95.5],
    )
    reclamos: int = Field(
        ...,
        ge=0,
        le=50,
        description="Cantidad de reclamos recientes",
        examples=[3],
    )


class PrediccionSalida(BaseModel):
    prediccion: str
    probabilidad: float
    version_modelo: str
    autor: str


app = FastAPI(
    title="API de predicción de churn",
    description="Servicio académico ML-Ops para estimar riesgo de abandono.",
    version="1.0.0",
)


@app.get("/")
def inicio() -> dict[str, str]:
    return {
        "mensaje": "Servicio ML-Ops activo",
        "estado": "ok",
        "autor": "Roberto Carlos Olguin Ledezma",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "estado": "ok",
        "modelo": VERSION_MODELO,
    }


@app.get("/info")
def info() -> dict[str, object]:
    """Endpoint informativo con detalles del modelo y servicio."""
    import json
    from pathlib import Path

    metadata_path = Path(__file__).resolve().parents[1] / "models" / "modelo_churn_v1_metadata.json"

    # Cargar metadatos si existen
    metadata = {}
    if metadata_path.exists():
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

    return {
        "version_modelo": VERSION_MODELO,
        "autor": AUTOR,
        "descripcion": "API de predicción de churn con Machine Learning",
        "variables_entrada": [
            {
                "nombre": "antiguedad",
                "tipo": "int",
                "descripcion": "Antigüedad del cliente en meses (0-120)",
                "rango": "0-120"
            },
            {
                "nombre": "cargo_mensual",
                "tipo": "float",
                "descripcion": "Cargo mensual del cliente (0-1000)",
                "rango": "0-1000"
            },
            {
                "nombre": "reclamos",
                "tipo": "int",
                "descripcion": "Cantidad de reclamos recientes (0-50)",
                "rango": "0-50"
            }
        ],
        "endpoint_prediccion": "/predict",
        "metodo_prediccion": "POST",
        "modelo_tipo": "LogisticRegression con StandardScaler",
        "metricas_disponibles": metadata.get("metricas", {}),
        "version_sklearn": metadata.get("version_sklearn", "No disponible"),
        "estado_servicio": "activo"
    }


@app.post("/predict", response_model=PrediccionSalida)
def predict(datos: ClienteEntrada) -> PrediccionSalida:
    try:
        X = [[
            datos.antiguedad,
            datos.cargo_mensual,
            datos.reclamos,
        ]]

        probabilidad = float(modelo.predict_proba(X)[0][1])
        etiqueta = "alto_riesgo" if probabilidad >= 0.50 else "bajo_riesgo"

        return PrediccionSalida(
            prediccion=etiqueta,
            probabilidad=round(probabilidad, 4),
            version_modelo=VERSION_MODELO,
            autor=AUTOR,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="No fue posible generar la predicción.",
        ) from exc
