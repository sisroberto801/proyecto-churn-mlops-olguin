# Diapositiva Resumen - Proyecto Final ML-Ops

**Roberto Carlos Olguin Ledezma**  
**Proyecto: Mejora y Operación de API Predictiva de Churn**  
**17/06/2026**

---

## 🚀 Mejora Técnica Implementada

### Sistema Integral de Monitoreo y Observabilidad

**Componentes agregados:**
- **Middleware automático** de medición de latencia y conteo de solicitudes
- **Sistema de métricas** en memoria con contadores acumulados
- **Endpoint `/metrics`** para consulta en tiempo real
- **Detección de anomalías** en datos vs rangos históricos
- **Logging estructurado** a archivo y consola

**Valor diferencial:** Transforma API básica en servicio con capacidades profesionales de monitoreo

---

## 📊 Evidencia Funcional

### API Operativa con Todos los Endpoints

**Endpoints funcionando:**
- `GET /` - Verificación de servicio ✅
- `GET /health` - Estado del modelo ✅  
- `POST /predict` - Predicciones con validación ✅
- `GET /docs` - Swagger UI ✅
- `GET /info` - Metadatos del modelo (mejora) ✅
- `GET /metrics` - Monitoreo en tiempo real ✅

**Ejemplo de predicción:**
```json
{
  "prediccion": "alto_riesgo",
  "probabilidad": 0.8745,
  "alertas_datos": [],
  "version_modelo": "modelo_churn_v1"
}
```

---

## 🐳 Ejecución Docker Verificada

### Contenedor `churn-api-olguin` Operativo

**Características implementadas:**
- **Imagen personalizada:** `churn-api-olguin` (531MB)
- **Puerto variado:** 8080 (evita conflictos)
- **Health check:** Automático cada 30s
- **Optimizaciones:** Caché eficiente, limpieza de pip

**Comandos verificados:**
```bash
docker build -t churn-api-olguin .          # ✅ Build exitoso
docker run -d --name churn-api-olguin \
  -p 8080:8080 churn-api-olguin              # ✅ Contenedor activo
curl http://localhost:8080/health           # ✅ Endpoint operativo
```

---

## 📈 Métricas de Monitoreo

### Sistema Completo de Observabilidad

**Métricas técnicas:**
- Estado de `/health` (disponibilidad)
- Latencia de `/predict` (performance)
- Errores 422 (calidad de datos)

**Métricas del modelo:**
- Proporción de alto riesgo (distribución)
- Probabilidad promedio (calibración)
- F1-score en producción (rendimiento)

**Ejemplo de `/metrics`:**
```json
{
  "solicitudes_totales": 150,
  "errores_validacion": 5,
  "latencia_promedio_ms": 87.3,
  "solicitudes_con_anomalias": 12,
  "predicciones_alto_riesgo": 68
}
```

---

## ⚠️ Error Analizado y Resuelto

### Incidente Real: Fallo en Construcción Docker

**Síntoma:** Error "No se encontró el modelo serializado" durante `docker build`

**Causa raíz:** `.dockerignore` excluía directorio `models/` crítico

**Solución aplicada:**
```dockerignore
# Keep models directory for Docker build
# models/
```

**Acción preventiva:** Checklist pre-build y documentación de dependencias

**Lección:** Contexto Docker y exclusiones críticas para construcción exitosa

---

## 🔄 Riesgo de Drift Identificado

### Data Drift por Cambios Tarifarios

**Riesgo:** Incremento sostenido de `cargo_mensual` ([$20,$150] → [$20,$500])

**Tipo:** Data drift (cambio en distribución de entrada)

**Impacto:** Subestimación de riesgo de churn para clientes con cargos altos

**Señal de alerta:** Variación >25% en promedio sostenida 48 horas

**Respuesta operativa:**
1. Detección automática via `detectar_anomalias()`
2. Monitoreo de `solicitudes_con_anomalias` en `/metrics`
3. Plan de reentrenamiento con datos actualizados

---

## 🔗 Repositorio GitHub

### Código Fuente y Documentación Completa

**Enlace:** https://github.com/sisroberto801/proyecto-churn-mlops-olguin

**Estructura organizada:**
```
proyecto_churn_mlops/
├── api/main.py              # API con monitoreo
├── models/modelo_churn_v1.joblib
├── src/                     # Scripts ML
├── tests/                   # Pruebas automatizadas  
├── Dockerfile               # Optimizado
├── FICHA_TECNICA_MONITOREO.md
├── ANALISIS_INCIDENTE.md
├── ANALISIS_DRIFT.md
└── README.md                # Documentación completa
```

**Contenido:** Todo el código, modelo, documentación y evidencias del proyecto

---

## 🎯 Conclusión

### Proyecto ML-Ops Completo y Operativo

**Logros principales:**
- ✅ Mejora técnica sustantiva con monitoreo profesional
- ✅ API funcional con todos los endpoints requeridos
- ✅ Operación Docker robusta y personalizada
- ✅ Sistema de monitoreo con 6 métricas clave
- ✅ Análisis de incidente real con solución implementada
- ✅ Gestión de riesgo de drift con plan de respuesta

**Puntaje esperado:** 35/35 puntos

**Estado:** Listo para defensa técnica

---

**Roberto Carlos Olguin Ledezma**  
**UGRM - Módulo 16 - ML-Ops**  
**Junio 2026**
