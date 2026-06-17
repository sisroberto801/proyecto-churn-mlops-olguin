# Ficha Técnica de Monitoreo - API Predictiva de Churn

**Autor:** Roberto Carlos Olguin Ledezma  
**Proyecto:** API de predicción de churn con ML-Ops  
**Fecha:** 17/06/2026

## Matriz de Monitoreo

| Métrica seleccionada | Tipo | Señal de alerta | Acción propuesta |
|---------------------|------|----------------|-----------------|
| Estado de /health | Técnica | Endpoint no responde o timeout > 5s | Revisar estado del contenedor Docker y logs del servicio |
| Latencia de /predict | Técnica | Latencia > 1000ms sostenida por 5 minutos | Revisar consumo de CPU/memoria y escalar recursos si es necesario |
| Errores 422 | Técnica | Más del 10% de las solicitudes con error 422 en última hora | Revisar integración del cliente y validar formato de datos enviados |
| Proporción de alto riesgo | Modelo | Más del 80% de predicciones como "alto_riesgo" sostenido 2 horas | Evaluar posible data drift y considerar reentrenamiento |
| Probabilidad promedio | Modelo | Variación > 25% en probabilidad promedio respecto a baseline | Analizar distribución de datos recientes y validar calidad |
| F1-score en producción | Modelo | Disminución sostenida > 15% en métricas de validación | Ejecutar evaluación completa y programar reentrenamiento |

## Descripción de Métricas

### Métricas Técnicas

**1. Estado de /health**
- **Fuente:** Endpoint GET /health
- **Frecuencia:** Cada 30 segundos (health check Docker)
- **Umbral crítico:** Sin respuesta por más de 5 segundos
- **Impacto:** Indisponibilidad total del servicio

**2. Latencia de /predict**
- **Fuente:** Middleware de medición en API
- **Frecuencia:** Por cada solicitud
- **Umbral crítico:** > 1000ms sostenido
- **Impacto:** Degradación del用户体验 y posible sobrecarga

**3. Errores 422**
- **Fuente:** Contador de errores de validación
- **Frecuencia:** Monitoreo continuo
- **Umbral crítico:** > 10% del total de solicitudes
- **Impacto:** Problemas en integración cliente-servidor

### Métricas del Modelo

**4. Proporción de alto riesgo**
- **Fuente:** Contador de predicciones en /metrics
- **Frecuencia:** Acumulado cada hora
- **Umbral crítico:** > 80% sostenido por 2 horas
- **Impacto:** Posible cambio en comportamiento de datos (drift)

**5. Probabilidad promedio**
- **Fuente:** Promedio de probabilidades en predicciones
- **Frecuencia:** Comparación con baseline cada 4 horas
- **Umbral crítico:** Variación > 25%
- **Impacto:** Cambio en distribución de características

**6. F1-score en producción**
- **Fuente:** Evaluación periódica con datos validados
- **Frecuencia:** Diaria con muestra reciente
- **Umbral crítico:** Disminución > 15% vs baseline
- **Impacto:** Degradación del rendimiento predictivo

## Sistema de Alertas

### Niveles de Severidad

**🔴 Crítico (1-5 minutos)**
- /health no responde
- Latencia > 5000ms
- Errores 500 > 5%

**🟡 Advertencia (1 hora)**
- Errores 422 > 10%
- Latencia > 1000ms sostenido
- Proporción alto riesgo > 80%

**🔵 Informativo (24 horas)**
- Variación en probabilidades
- Tendencias en métricas

### Canales de Notificación

1. **Logs estructurados:** `logs/monitor_api.log`
2. **Endpoint /metrics:** Consulta en tiempo real
3. **Health check Docker:** Monitoreo automático
4. **Alertas en logs:** Mensajes WARNING y ERROR

## Acciones de Respuesta

### Respuesta Inmediata (Crítico)

1. **Verificar contenedor:**
   ```bash
   docker ps | grep churn-api-olguin
   docker logs churn-api-olguin --tail 50
   ```

2. **Reiniciar servicio:**
   ```bash
   docker restart churn-api-olguin
   ```

3. **Validar endpoints:**
   ```bash
   curl http://localhost:8080/health
   curl http://localhost:8080/metrics
   ```

### Respuesta Coordinada (Advertencia)

1. **Analizar logs:**
   ```bash
   grep "WARNING\|ERROR" logs/monitor_api.log --tail 100
   ```

2. **Revisar métricas:**
   ```bash
   curl http://localhost:8080/metrics | jq .
   ```

3. **Evaluar drift:**
   - Comparar distribución actual vs histórica
   - Analizar variables fuera de rango

### Respuesta Programada (Informativo)

1. **Reporte diario:**
   - Resumen de métricas
   - Tendencias observadas
   - Recomendaciones

2. **Mantenimiento preventivo:**
   - Limpieza de logs
   - Actualización de dependencias
   - Reentrenamiento programado

## Herramientas de Monitoreo

### Disponibles en el Proyecto

1. **FastAPI Middleware:** Medición automática de latencia
2. **Logging estructurado:** Registro de eventos y errores
3. **Endpoint /metrics:** Resumen acumulado en tiempo real
4. **Health check Docker:** Verificación automática cada 30s
5. **Detección de anomalías:** Alertas por valores fuera de rango histórico

### Integración Sugerida

Para producción, se recomienda integrar con:
- **Prometheus:** Exportación de métricas
- **Grafana:** Visualización de dashboards
- **Alertmanager:** Gestión de alertas
- **ELK Stack:** Análisis avanzado de logs

## Métricas de Baseline

### Valores de Referencia (Entrenamiento)

- **Accuracy:** 0.825
- **F1-score:** 0.8659
- **AUC-ROC:** 0.8749
- **Latencia promedio:** < 100ms
- **Tasa de error 422:** < 5%
- **Proporción alto riesgo:** ~45%

### Objetivos Operativos

- **Disponibilidad:** > 99.5%
- **Latencia:** < 500ms (percentil 95)
- **Tasa de error:** < 1%
- **Tiempo de detección:** < 5 minutos
- **Tiempo de respuesta:** < 15 minutos

## Procedimientos de Escalamiento

### Nivel 1: Operación Automática
- Health checks y reinicios automáticos
- Rotación de logs y limpieza temporal
- Monitoreo básico con /metrics

### Nivel 2: Respuesta Manual
- Análisis de logs y métricas
- Ajustes de configuración
- Escalado horizontal si es necesario

### Nivel 3: Intervención Especializada
- Reentrenamiento del modelo
- Análisis de drift profundo
- Mejoras arquitectónicas

---

**Estado actual:** Implementado y funcional  
**Próxima revisión:** 17/07/2026  
**Vigencia:** 6 meses
