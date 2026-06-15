# Proyecto Churn MLOps

Proyecto académico de MLOps para predicción de abandono de clientes (churn) utilizando FastAPI y scikit-learn.

**Autor:** Roberto Carlos Olguin Ledezma

**Repositorio GitHub:** https://github.com/sisroberto801/proyecto_churn_mlops.git

## Descripción

Este proyecto implementa un pipeline completo de Machine Learning para predecir el riesgo de abandono de clientes. Incluye:

- Preparación y procesamiento de datos
- Entrenamiento de modelo con LogisticRegression
- Evaluación de métricas de rendimiento
- API REST para predicciones en tiempo real
- Pruebas automatizadas
- Documentación técnica

## Características

- **Modelo**: Regresión Logística con escalado StandardScaler
- **API**: FastAPI con documentación Swagger automática
- **Variables**: antigüedad, cargo_mensual, reclamos
- **Métricas**: Accuracy, Precision, Recall, F1-score
- **Testing**: Pruebas unitarias con pytest
- **Container**: Soporte Docker incluido

## Problema del proyecto

Se trabajará con un caso simplificado de predicción de abandono de clientes, conocido como churn.

El modelo intentará predecir si un cliente podría abandonar un servicio, utilizando variables como edad, antigüedad, saldo promedio, reclamos y uso de aplicación móvil.

## Arquitectura del proyecto

```text
proyecto_churn_mlops/
├── api/
│   ├── __init__.py
│   └── main.py              # API FastAPI con endpoints /predict, /health
├── data/
│   ├── churn_clientes.csv   # Dataset de demostración
│   ├── train.csv           # Datos de entrenamiento
│   ├── test.csv            # Datos de prueba
│   └── descripcion_dataset.md
├── docs/
│   └── metricas_modelo.md   # Métricas de evaluación
├── models/
│   ├── modelo_churn_v1.joblib     # Modelo serializado
│   └── modelo_churn_v1_metadata.json
├── src/
│   ├── preparar_datos.py   # Generación y preparación de datos
│   ├── entrenar_modelo.py  # Entrenamiento del modelo
│   └── evaluar_modelo.py   # Evaluación y métricas
├── tests/
│   ├── test_api.py
│   ├── test_api_completa.py
│   └── test_api_nueva.py
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
├── README.md
└── INSTRUCCIONES_EJECUCION.md
```

## Componentes principales

### Scripts de ML (`src/`)
- **`preparar_datos.py`**: Crea dataset sintético y divide en train/test
- **`entrenar_modelo.py`**: Entrena LogisticRegression con Pipeline
- **`evaluar_modelo.py`**: Evalúa modelo y genera métricas

### API REST (`api/`)
- **`main.py`**: FastAPI con validación Pydantic
- **Endpoints**: `/`, `/health`, `/predict`
- **Documentación**: Swagger en `/docs`

### Testing (`tests/`)
- Pruebas unitarias para endpoints de API
- Validación de respuestas y códigos de estado

### Modelo (`models/`)
- **`modelo_churn_v1.joblib`**: Modelo serializado con Pipeline completo
- **`modelo_churn_v1_metadata.json`**: Metadatos del modelo

## Flujo de ejecución

1. **Preparar datos**: `python src/preparar_datos.py`
2. **Entrenar modelo**: `python src/entrenar_modelo.py`
3. **Evaluar modelo**: `python src/evaluar_modelo.py`
4. **Iniciar API**: `uvicorn api.main:app --reload`
5. **Probar API**: Acceder a `http://127.0.0.1:8000/docs`
6. **Ejecutar pruebas**: `python tests/test_api_completa.py` (requiere API corriendo)
7. **Pruebas unitarias**: `pytest`

## Modelo de predicción

### Variables de entrada
- **antiguedad** (int): Meses como cliente (0-120)
- **cargo_mensual** (float): Monto mensual pagado (0-1000)
- **reclamos** (int): Cantidad de reclamos recientes (0-50)

### Salida
- **prediccion**: "alto_riesgo" o "bajo_riesgo"
- **probabilidad**: Score de probabilidad (0.0-1.0)
- **version_modelo**: Identificador del modelo
- **autor**: Roberto Carlos Olguin Ledezma

### Métricas de rendimiento
Las métricas se generan automáticamente y se guardan en `docs/metricas_modelo.md`:
- Accuracy
- Precision  
- Recall
- F1-score

## Tecnologías

- **Python 3.12+**: Lenguaje principal
- **FastAPI**: Framework API con validación automática
- **scikit-learn**: Biblioteca de Machine Learning
- **pandas**: Manipulación de datos
- **pytest**: Framework de testing
- **Docker**: Contenerización

## Requisitos

Ver `requirements.txt` para las dependencias completas:
```bash
fastapi[standard]
uvicorn
pandas
scikit-learn
joblib
pydantic
pytest
httpx
```

## Control de versiones

Este proyecto utiliza Git para control de versiones y GitHub para respaldo en la nube.

Los commits mantienen trazabilidad sobre:
- Cambios en el código fuente
- Actualizaciones de documentación
- Modificaciones en la estructura del proyecto
- Mejoras en el modelo y API
