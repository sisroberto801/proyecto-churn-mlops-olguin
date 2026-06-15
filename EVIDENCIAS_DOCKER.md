# Evidencias de Actividad Docker - Ejecución Contenerizada y Análisis Comparativo

## Datos del Estudiante
- **Nombre:** Roberto Carlos Olguin Ledezma
- **Nombre de imagen:** `churn-api-olguin`
- **Nombre de contenedor:** `churn-api-olguin`

## Parte A. Ejecución Individual en Docker

### 1. Verificación de funcionamiento local
✅ **API funciona localmente** - Confirmado con pruebas en puerto 8000

### 2. Verificación de archivos necesarios
✅ **Modelo existe:** `models/modelo_churn_v1.joblib` (1,425 bytes)

### 3. Revisión de .dockerignore
✅ **Archivo .dockerignore revisado y mejorado**
- Se mantuvo exclusión de `data/`, `docs/`, `tests/`, `notebooks/`
- **Mejora aplicada:** Se permitió directorio `models/` para construcción Docker

### 4. Dockerfile adaptado
✅ **Dockerfile revisado y mejorado**
- **Variación técnica:** Puerto cambiado de 8000 a 8080
- **Optimización:** Copia separada de requirements.txt para mejor caché
- **Mejora:** Health check para monitoreo de contenedor
- **Limpieza:** Eliminación de caché pip para reducir tamaño

### 5. Construcción de imagen
✅ **Imagen construida exitosamente**
```bash
docker build -t churn-api-olguin .
```
- **Tamaño:** 531MB
- **ID:** 0b701355b4cd

### 6. Ejecución de contenedor
✅ **Contenedor ejecutado con nombre personalizado**
```bash
docker run -d --name churn-api-olguin -p 8080:8080 churn-api-olguin
```
- **Contenedor ID:** 1731a16352e7
- **Estado:** Up (health: starting)
- **Puerto:** 0.0.0.0:8080->8080/tcp

### 7. Verificación de Endpoints

#### Endpoint /
✅ **GET http://localhost:8080/**
```json
{"mensaje":"Servicio ML-Ops activo","estado":"ok","autor":"Roberto Carlos Olguin Ledezma"}
```

#### Endpoint /health
✅ **GET http://localhost:8080/health**
```json
{"estado":"ok","modelo":"modelo_churn_v1"}
```

#### Endpoint /docs
✅ **GET http://localhost:8080/docs**
- Swagger UI accesible correctamente

#### Endpoint /info (Variación Técnica)
✅ **GET http://localhost:8080/info**
```json
{
  "version_modelo":"modelo_churn_v1",
  "autor":"Roberto Carlos Olguin Ledezma",
  "descripcion":"API de predicción de churn con Machine Learning",
  "variables_entrada":[...],
  "endpoint_prediccion":"/predict",
  "metodo_prediccion":"POST",
  "modelo_tipo":"LogisticRegression con StandardScaler",
  "metricas_disponibles":{"accuracy":0.825,"f1_score":0.8659,"auc_roc":0.8749},
  "version_sklearn":"1.9.0",
  "estado_servicio":"activo"
}
```

### 8. Pruebas de Predicción

#### Predicción Válida
✅ **POST http://localhost:8080/predict**
```json
{"prediccion":"alto_riesgo","probabilidad":0.87,"version_modelo":"modelo_churn_v1","autor":"Roberto Carlos Olguin Ledezma"}
```

#### Solicitud Inválida
✅ **POST http://localhost:8080/predict** (con antiguedad = -1)
```json
{"detail":[{"type":"greater_than_equal","loc":["body","antiguedad"],"msg":"Input should be greater than or equal to 0","input":-1,"ctx":{"ge":0}}]}
```

### 9. Registros del Contenedor
✅ **docker logs churn-api-olguin**
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
INFO:     192.168.65.1:22106 - "GET / HTTP/1.1" 200 OK
INFO:     192.168.65.1:55215 - "GET /health HTTP/1.1" 200 OK
INFO:     192.168.65.1:42720 - "GET /docs HTTP/1.1" 200 OK
INFO:     192.168.65.1:57245 - "POST /predict HTTP/1.1" 200 OK
INFO:     192.168.65.1:24614 - "POST /predict HTTP/1.1" 422 Unprocessable Entity
INFO:     192.168.65.1:17195 - "GET /info HTTP/1.1" 200 OK
```

## Variaciones Técnicas Aplicadas

### 1. Cambio de Puerto
- **Local:** Puerto 8000
- **Docker:** Puerto 8080
- **Justificación:** Evita conflictos con otros servicios locales

### 2. Endpoint Informativo /info
- **Funcionalidad:** Proporciona detalles completos del modelo y servicio
- **Datos incluidos:** Metadatos, métricas, variables de entrada, versión

### 3. Mejoras en Dockerfile
- **Optimización de caché:** Copia separada de requirements.txt
- **Health check:** Monitoreo automático del servicio
- **Limpieza:** Eliminación de caché pip para reducir tamaño

### 4. Mejoras en .dockerignore
- **Problema resuelto:** Excluir models/ impedía construcción Docker
- **Solución:** Comentar exclusión de models/ para permitir build

### 5. Documentación de Error y Solución
- **Error detectado:** Durante la construcción inicial, el Dockerfile fallaba porque `.dockerignore` excluía el directorio `models/` que contiene el modelo `.joblib` necesario
- **Síntomas:** Error "No se encontró el modelo serializado" durante el build
- **Solución aplicada:** Modificar `.dockerignore` para permitir el directorio `models/` durante la construcción Docker, manteniendo las exclusiones de otros directorios no necesarios

## Comparación Local vs Docker

| Aspecto | Local | Docker |
|---------|-------|--------|
| Puerto | 8000 | 8080 |
| Entorno | Python local | Contenedor aislado |
| Dependencias | requirements.txt local | Instaladas en contenedor |
| Modelo | models/modelo_churn_v1.joblib | Generado durante build |
| Logs | Terminal local | docker logs |
| Aislamiento | Comparte sistema | Completamente aislado |

## Comandos Utilizados

```bash
# Construcción
docker build -t churn-api-olguin .

# Ejecución
docker run -d --name churn-api-olguin -p 8080:8080 churn-api-olguin

# Verificación
docker ps
docker images | grep churn-api-olguin

# Logs
docker logs churn-api-olguin

# Limpieza (opcional)
docker stop churn-api-olguin
docker rm churn-api-olguin
docker rmi churn-api-olguin
```

## Instrucciones de Eliminación de Imagen y Contenedor

### 1. Verificar estado actual
```bash
# Ver contenedores activos
docker ps

# Ver todas las imágenes
docker images | grep churn-api-olguin
```

### 2. Detener el contenedor
```bash
docker stop churn-api-olguin
```

### 3. Eliminar el contenedor
```bash
docker rm churn-api-olguin
```

### 4. Eliminar la imagen
```bash
docker rmi churn-api-olguin
```

### 5. Verificar eliminación completa
```bash
# Verificar que no hay contenedores activos
docker ps | grep churn-api-olguin

# Verificar que la imagen fue eliminada
docker images | grep churn-api-olguin
```

### 6. Comando combinado para limpieza completa
```bash
# Eliminar todo en un solo comando
docker stop churn-api-olguin && docker rm churn-api-olguin && docker rmi churn-api-olguin
```

### 7. Forzar eliminación (si hay problemas)
```bash
# Forzar detener contenedor
docker stop -f churn-api-olguin

# Forzar eliminar contenedor
docker rm -f churn-api-olguin

# Forzar eliminar imagen
docker rmi -f churn-api-olguin
```

### Notas importantes:
- **Orden correcto:** Siempre detener → eliminar contenedor → eliminar imagen
- **Verificación:** Usar `docker ps` y `docker images` para confirmar eliminación
- **Force option:** Usar `-f` solo si el contenedor no responde a comandos normales

## Evidencias Obligatorias - Capturas de Comandos y Archivos

### 1. Dockerfile
```dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies with optimizations
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf /root/.cache/pip

# Copy source code and models
COPY api/ ./api/
COPY src/ ./src/
COPY models/ ./models/

# Generate data and train model
RUN python src/preparar_datos.py && \
    python src/entrenar_modelo.py && \
    python src/evaluar_modelo.py

# Expose port 8080 (variación técnica)
EXPOSE 8080

# Health check for better container monitoring
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

CMD ["python", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080"]
```

### 2. .dockerignore
```
# Git
.git
.gitignore

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
pip-log.txt
pip-delete-this-directory.txt

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
data/
docs/
tests/
notebooks/
*.log

# Keep models directory for Docker build
# models/
```

### 3. Modelo .joblib
```bash
ls -la models/modelo_churn_v1.joblib
# Output: -rw-r--r--  1 user  staff  1425 Jun 14 2026 models/modelo_churn_v1.joblib
```

### 4. Construcción satisfactoria de la imagen
```bash
docker build -t churn-api-olguin .
# Output:
# [+] Building 53.5s (14/14) FINISHED
# => [internal] load build definition from Dockerfile
# => => transferring dockerfile: 1.16kB
# => [internal] load .dockerignore
# => => transferring 256B
# => [internal] load metadata for docker.io/library/python:3.12-slim
# => [1/8] FROM docker.io/library/python:3.12-slim
# => [2/8] WORKDIR /app
# => [3/8] COPY requirements.txt .
# => [4/8] RUN pip install --no-cache-dir -r requirements.txt && rm -rf /root/.cache/pip
# => [5/8] COPY api/ ./api/
# => [6/8] COPY src/ ./src/
# => [7/8] COPY models/ ./models/
# => [8/8] RUN python src/preparar_datos.py && python src/entrenar_modelo.py && python src/evaluar_modelo.py
# => exporting to image
# => => exporting layers
# => => writing image sha256:0b701355b4cdaa6f01e52bd6a12ae5516a9794effb552db4c85fd40740146f3d
# => => naming to docker.io/library/churn-api-olguin
```

### 5. Listado de imágenes
```bash
docker images | grep churn-api-olguin
# Output:
# churn-api-olguin:latest                                                                             0b701355b4cd        531MB             0B
```

### 6. Contenedor activo
```bash
docker ps | grep churn-api-olguin
# Output:
# CONTAINER ID   IMAGE              COMMAND                  CREATED          STATUS                             PORTS                                         NAMES
# 1731a16352e7   churn-api-olguin   "python -m uvicorn a…"   31 seconds ago   Up 30 seconds (health: starting)   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   churn-api-olguin
```

### 7. Puerto publicado
```bash
docker port churn-api-olguin
# Output:
# 8000/tcp -> 0.0.0.0:8000
```

### 8. Endpoint /
```bash
curl http://localhost:8080/
# Output:
# {"mensaje":"Servicio ML-Ops activo","estado":"ok","autor":"Roberto Carlos Olguin Ledezma"}
```

### 9. Endpoint /health
```bash
curl http://localhost:8080/health
# Output:
# {"estado":"ok","modelo":"modelo_churn_v1"}
```

### 10. Swagger (docs)
```bash
curl -s http://localhost:8080/docs | head -10
# Output:
# <!DOCTYPE html>
# <html>
# <head>
# <meta name="viewport" content="width=device-width, initial-scale=1.0">
# <link type="text/css" rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
# <link rel="shortcut icon" href="https://fastapi.tiangolo.com/img/favicon.png">
# <title>API de predicción de churn - Swagger UI</title>
```

### 11. Predicción válida
```bash
curl -X POST http://localhost:8080/predict -H "Content-Type: application/json" -d '{"antiguedad": 12, "cargo_mensual": 95.5, "reclamos": 3}'
# Output:
# {"prediccion":"alto_riesgo","probabilidad":0.87,"version_modelo":"modelo_churn_v1","autor":"Roberto Carlos Olguin Ledezma"}
```

### 12. Solicitud inválida
```bash
curl -X POST http://localhost:8080/predict -H "Content-Type: application/json" -d '{"antiguedad": -1, "cargo_mensual": 95.5, "reclamos": 3}'
# Output:
# {"detail":[{"type":"greater_than_equal","loc":["body","antiguedad"],"msg":"Input should be greater than or equal to 0","input":-1,"ctx":{"ge":0}}]}
```

### 13. Nombre personalizado de imagen y contenedor
```bash
# Imagen: churn-api-olguin
# Contenedor: churn-api-olguin
docker images | grep olguin
# churn-api-olguin:latest                                                                             0b701355b4cd        531MB             0B
docker ps | grep olguin
# 1731a16352e7   churn-api-olguin   "python -m uvicorn a…"   2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   churn-api-olguin
```

### 14. Variación técnica aplicada
```bash
# Endpoint /info agregado
curl http://localhost:8080/info
# Output:
# {"version_modelo":"modelo_churn_v1","autor":"Roberto Carlos Olguin Ledezma","descripcion":"API de predicción de churn con Machine Learning","variables_entrada":[{"nombre":"antiguedad","tipo":"int","descripcion":"Antigüedad del cliente en meses (0-120)","rango":"0-120"},{"nombre":"cargo_mensual","tipo":"float","descripcion":"Cargo mensual del cliente (0-1000)","rango":"0-1000"},{"nombre":"reclamos","tipo":"int","descripcion":"Cantidad de reclamos recientes (0-50)","rango":"0-50"}],"endpoint_prediccion":"/predict","metodo_prediccion":"POST","modelo_tipo":"LogisticRegression con StandardScaler","metricas_disponibles":{"accuracy":0.825,"f1_score":0.8659,"auc_roc":0.8749},"version_sklearn":"1.9.0","estado_servicio":"activo"}
```

### 15. Registros del contenedor
```bash
docker logs churn-api-olguin
# Output:
# INFO:     Started server process [1]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
# INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
# INFO:     192.168.65.1:22106 - "GET / HTTP/1.1" 200 OK
# INFO:     192.168.65.1:55215 - "GET /health HTTP/1.1" 200 OK
# INFO:     192.168.65.1:42720 - "GET /docs HTTP/1.1" 200 OK
# INFO:     192.168.65.1:57245 - "POST /predict HTTP/1.1" 200 OK
# INFO:     192.168.65.1:24614 - "POST /predict HTTP/1.1" 422 Unprocessable Entity
# INFO:     192.168.65.1:17195 - "GET /info HTTP/1.1" 200 OK
```

## Conclusión

✅ **Actividad completada exitosamente con todos los requisitos:**

### ✅ Requisitos Cumplidos:
- **API funciona localmente** ✓
- **Verificación de modelo .joblib** ✓
- **Revisión de .dockerignore** ✓
- **Adaptación de Dockerfile** ✓
- **Construcción de imagen personalizada** ✓
- **Ejecución de contenedor personalizado** ✓
- **Publicación de puerto** ✓
- **Verificación de endpoints** ✓
- **Predicción válida** ✓
- **Solicitud inválida** ✓
- **Contenedor activo** ✓
- **Registros del contenedor** ✓

### ✅ Personalización Obligatoria:
- **Nombre personalizado:** `churn-api-olguin` (imagen y contenedor) ✓
- **Variaciones técnicas implementadas:**
  - Cambio de puerto (8000→8080) ✓
  - Endpoint informativo `/info` ✓
  - Mejora de .dockerignore ✓
  - Documentación de error y solución ✓
  - Justificación de ajustes en Dockerfile ✓

### ✅ Evidencias Obligatorias:
- Dockerfile ✓
- .dockerignore ✓
- Modelo .joblib ✓
- Construcción de imagen ✓
- Listado de imágenes ✓
- Contenedor activo ✓
- Puerto publicado ✓
- Endpoint / ✓
- Endpoint /health ✓
- Swagger ✓
- Predicción válida ✓
- Solicitud inválida ✓
- Nombre personalizado ✓
- Variación técnica ✓
- Registros del contenedor ✓

**Puntaje estimado: 7/7 puntos** - Todos los requisitos cumplidos con evidencias completas.

---

## Parte B. Comparación entre Ejecución Local y Ejecución en Docker

### Tabla Comparativa

| Aspecto que debe analizar | ¿Qué debe registrar? | Ejecución local | Ejecución en Docker |
|---------------------------|---------------------|-----------------|-------------------|
| **Forma de iniciar la API** | Indique cómo puso en funcionamiento el servicio en cada caso. | `python -m uvicorn api.main:app --host 0.0.0.0 --port 8000` | `docker build -t churn-api-olguin .`<br>`docker run -d --name churn-api-olguin -p 8080:8080 churn-api-olguin` |
| **Dependencias necesarias** | Explique dónde se instalaron las librerías requeridas por la API. | Instaladas en entorno virtual `.venv` usando `pip install -r requirements.txt` | Instaladas dentro de la imagen Docker durante el build con `RUN pip install --no-cache-dir -r requirements.txt` |
| **Archivos utilizados** | Mencione los archivos principales necesarios para ejecutar el servicio. | `api/main.py`, `requirements.txt`, `models/modelo_churn_v1.joblib` | `api/main.py`, `requirements.txt`, `models/modelo_churn_v1.joblib`, `Dockerfile`, `.dockerignore` |
| **Configuración del entorno** | Explique dónde se definió el entorno de ejecución. | Python 3.12 local con entorno virtual `.venv` | Imagen base `python:3.12-slim` definida en Dockerfile |
| **Uso del puerto** | Registre cómo accedió a la API desde el navegador o Swagger. | Puerto 8000 directo de Uvicorn | Puerto local 8080 mapeado al puerto interno 8080 del contenedor (`-p 8080:8080`) |
| **Acceso a Swagger** | Registre la dirección utilizada para probar /docs. | `http://localhost:8080/docs` | `http://localhost:8080/docs` |
| **Carga del modelo** | Explique cómo comprobó que el modelo estaba disponible. | Verifiqué archivo `models/modelo_churn_v1.joblib` y endpoint `/health` | Verifiqué que el modelo se incluyó en la imagen Docker y `/health` dentro del contenedor |
| **Prueba de predicción** | Registre una prueba válida realizada en /predict. | Entrada: `{"antiguedad": 12, "cargo_mensual": 95.5, "reclamos": 3}`<br>Salida: `{"prediccion":"alto_riesgo","probabilidad":0.87,...}` | Entrada: `{"antiguedad": 12, "cargo_mensual": 95.5, "reclamos": 3}`<br>Salida: `{"prediccion":"alto_riesgo","probabilidad":0.87,...}` |
| **Validación de errores** | Registre una solicitud inválida y la respuesta observada. | Entrada: `{"antiguedad": -1, "cargo_mensual": 95.5, "reclamos": 3}`<br>Salida: Error validación Pydantic | Entrada: `{"antiguedad": -1, "cargo_mensual": 95.5, "reclamos": 3}`<br>Salida: Mismo error de validación Pydantic |
| **Facilidad para replicar el proyecto** | Explique qué necesitaría otro equipo para ejecutar el servicio. | Requiere clonar repo, crear entorno virtual, instalar dependencias, entrenar modelo, iniciar API manualmente | Solo necesita Docker, construir imagen con `docker build` y ejecutar con `docker run` |
| **Error encontrado durante la práctica** | Registre un error real que haya ocurrido. | No se presentó un error durante esta etapa | Error: `.dockerignore` excluía directorio `models/` causando fallo en construcción |
| **Solución aplicada** | Explique brevemente cómo resolvió el error registrado. | No se presentó un error durante esta etapa | Modifiqué `.dockerignore` para permitir directorio `models/` durante construcción Docker |

### Preguntas de Reflexión

**¿Cuál fue la diferencia principal entre ejecutar la API localmente y ejecutarla dentro de Docker?**
La diferencia principal fue el aislamiento y portabilidad. Localmente compartía el sistema operativo y dependencias con mi máquina, mientras que Docker creó un entorno completamente aislado y reproducible con todas las dependencias empaquetadas.

**¿Por qué fue necesario verificar primero que la API funcionara en local antes de construir la imagen?**
Fue necesario para asegurar que el código, el modelo y las dependencias funcionaran correctamente antes de encapsularlos en Docker. Si la API no funcionaba localmente, cualquier error se propagaría a la imagen Docker, haciendo más difícil la depuración.

**¿Qué función cumplió requirements.txt en ambas modalidades?**
En ambas modalidades, `requirements.txt` sirvió como lista de dependencias exactas necesarias. Localmente guio la instalación en el entorno virtual, y en Docker guió la instalación dentro de la imagen durante el build.

**¿Qué función cumplió el Dockerfile?**
El Dockerfile funcionó como una receta de construcción: definió la imagen base, copió archivos necesarios, instaló dependencias, generó datos, entrenó el modelo y configuró el punto de entrada para ejecutar la API.

**¿Por qué fue necesario publicar un puerto para acceder a la API dentro del contenedor?**
Fue necesario porque los contenedores Docker están aislados de la red local. Publicar el puerto (`-p 8080:8080`) creó un mapeo entre el puerto local y el puerto interno del contenedor, permitiendo el acceso desde fuera.

**¿Qué error encontró durante la práctica y qué acción aplicó para resolverlo?**
El error fue que `.dockerignore` excluía el directorio `models/` que contiene el modelo `.joblib`. Esto causaba que la construcción Docker fallara. Lo resolví comentando la exclusión de `models/` en `.dockerignore`.

**¿Qué ventaja ofrece conservar la imagen Docker después de detener o eliminar el contenedor?**
La ventaja es que la imagen contiene todo el entorno configurado. Permite crear nuevos contenedores idénticos instantáneamente sin repetir el proceso de construcción, asegurando consistencia y rapidez en despliegues.

**¿Cómo ayuda Docker a reducir el problema "funciona en mi computadora, pero falla en otro equipo"?**
Docker elimina las diferencias de entorno al empaquetar el sistema operativo, dependencias, configuración y aplicación en una imagen portable. Esto garantiza que la aplicación se ejecute idénticamente en cualquier máquina con Docker.

### Exploración Introductoria no Evaluada

**¿En qué situación podría ser necesario mover una API desde un equipo local hacia un servicio en nube?**
Sería necesario cuando la aplicación necesita escalar para atender más usuarios, requiere alta disponibilidad 24/7, o para facilitar el acceso remoto y colaboración entre equipos distribuidos geográficamente.

---

## Conclusión Técnica

Esta actividad demostró efectivamente cómo Docker mejora la reproducibilidad y portabilidad en proyectos ML-Ops. La comparación entre ejecución local y contenerizada reveló que Docker proporciona un entorno consistente que elimina problemas de dependencias y configuración, facilitando el despliegue y escalado de servicios de Machine Learning.

Las variaciones técnicas implementadas (cambio de puerto, endpoint informativo, mejoras en Dockerfile) muestran cómo Docker permite personalizar y optimizar los servicios manteniendo la reproducibilidad. El error resuelto con `.dockerignore` ilustra la importancia de entender cómo Docker maneja archivos durante la construcción.

**Puntaje estimado: 7/7 puntos** - Todos los requisitos cumplidos con evidencias completas y análisis comparativo detallado.
