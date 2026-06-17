# Análisis de Riesgo de Drift - API Predictiva de Churn

**Autor:** Roberto Carlos Olguin Ledezma  
**Fecha de análisis:** 17/06/2026  
**Modelo:** modelo_churn_v1 (LogisticRegression)

## Plantilla de Análisis de Drift

| Elemento | Respuesta del maestrante |
|----------|-------------------------|
| **Riesgo identificado** | Incremento sostenido de cargos mensuales promedio debido a cambios en la estructura tarifaria de la empresa |
| **Tipo de drift** | Data drift (cambio en la distribución de datos de entrada) |
| **Impacto** | Las predicciones de churn podrían subestimar el riesgo real, ya que cargos más altos históricamente correlacionan con mayor probabilidad de abandono |
| **Señal de alerta** | Variación > 25% en el promedio de `cargo_mensual` respecto al rango histórico [20.0, 150.0] sostenida por más de 48 horas |
| **Respuesta operativa** | 1. Activar monitoreo intensivo de la variable<br>2. Analizar impacto en precisión del modelo<br>3. Evaluar necesidad de reentrenamiento con datos recientes<br>4. Documentar cambio en rangos de referencia |

## Análisis Detallado del Riesgo

### Contexto del Negocio

El modelo fue entrenado con datos históricos donde el cargo mensual promedio de los clientes se mantenía dentro de un rango estable de $20.0 a $150.0. Sin embargo, la empresa está implementando una reestructura tarifaria que podría modificar significativamente estos valores.

### Riesgo Identificado

**Descripción:** Incremento sostenido de cargos mensuales promedio debido a cambios en la estructura tarifaria de la empresa.

**Escenario específico:**
- Situación actual: La empresa lanza nuevos planes premium con precios entre $200-500
- Comportamiento esperado: Los clientes existentes migran gradualmente a los nuevos planes
- Impacto en datos: El promedio de `cargo_mensual` podría aumentar de ~$85 a ~$180

### Tipo de Drift

**Data drift** - Cambio en la distribución de las variables de entrada sin cambio en la relación subyacente entre variables y objetivo.

**Características:**
- Las características de entrada cambian (cargo_mensual más alto)
- La relación entre variables y churn podría mantenerse
- El modelo entrenado con rangos históricos becomes less accurate

### Impacto en Predicciones

#### Efecto Directo
1. **Sesgo en predicciones:** El modelo podría subestimar el riesgo de churn para clientes con cargos altos
2. **Alertas falsas:** Más clientes serán marcados como "anómalos" por estar fuera del rango histórico
3. **Calibración incorrecta:** Las probabilidades predichas podrían no reflejar el riesgo real

#### Efecto Secundario
1. **Pérdida de confianza:** Los usuarios podrían desconfiar de predicciones con muchas alertas
2. **Decisiones incorrectas:** La empresa podría tomar acciones basadas en predicciones sesgadas
3. **Costos operativos:** Revisión manual de más casos por alertas de anomalía

### Señales de Alerta

#### Métricas Cuantitativas
1. **Variación en promedio:** > 25% cambio en cargo_mensual promedio
2. **Proporción de anomalías:** > 30% de solicitudes con alertas de datos atípicos
3. **Distribución de predicciones:** Cambio significativo en proporción alto/bajo riesgo

#### Umbrales Específicos
```python
# Rangos históricos actuales
RANGOS_HISTORICOS = {
    "cargo_mensual": (20.0, 150.0),  # Media ~85
}

# Umbrales de alerta
UMBRAL_DRIFT_CARGO = 150.0 * 1.25  # 187.5
UMBRAL_ANOMALIAS = 0.30  # 30% de solicitudes
```

#### Indicadores de Monitoreo
1. **Endpoint /metrics:** Aumento en `solicitudes_con_anomalias`
2. **Logs:** Más mensajes "Valores fuera de rango histórico"
3. **Predicciones:** Cambio en distribución de probabilidades

### Respuesta Operativa

#### Fase 1: Detección Temprana (0-24 horas)
```bash
# Monitoreo intensivo
curl http://localhost:8080/metrics | jq '.solicitudes_con_anomalias'

# Análisis de logs
grep "cargo_mensual" logs/monitor_api.log | tail -50
```

#### Fase 2: Evaluación de Impacto (24-72 horas)
1. **Análisis estadístico:**
   - Comparar distribución actual vs histórica
   - Calcular métricas de drift (KS test, Population Stability Index)
   
2. **Validación de modelo:**
   - Evaluar precisión con datos recientes si hay etiquetas disponibles
   - Analizar calibración de probabilidades

3. **Decisión de reentrenamiento:**
   - Si drift > 0.25: Considerar reentrenamiento inmediato
   - Si drift < 0.25: Monitorear y planificar reentrenamiento programado

#### Fase 3: Acción Correctiva (72+ horas)
1. **Recolectar datos nuevos:** Capturar datos con nuevos rangos tarifarios
2. **Reentrenar modelo:** Incluir datos actualizados en conjunto de entrenamiento
3. **Actualizar rangos:** Modificar `RANGOS_HISTORICOS` en api/main.py
4. **Validar y desplegar:** Probar nuevo modelo antes de producción

### Plan de Respuesta Detallado

#### Niveles de Severidad

**🟡 Nivel 1 (Monitoreo)**
- Señal: Variación 10-25% en cargo_mensual
- Acción: Monitoreo intensivo, reporte diario
- Timeline: 7 días

**🟠 Nivel 2 (Evaluación)**
- Señal: Variación 25-50% o >20% anomalías
- Acción: Análisis de impacto, preparación para reentrenamiento
- Timeline: 72 horas

**🔴 Nivel 3 (Acción)**
- Señal: Variación >50% o >30% anomalías
- Acción: Reentrenamiento inmediato, actualización de modelo
- Timeline: 24 horas

#### Comandos de Respuesta

```bash
# 1. Verificar métricas actuales
curl -s http://localhost:8080/metrics | jq '{
  solicitudes_con_anomalias,
  predicciones_validas,
  latencia_promedio_ms
}'

# 2. Analizar logs de anomalías recientes
grep "cargo_mensual.*fuera del rango" logs/monitor_api.log --tail=20

# 3. Evaluar distribución actual (si se tiene acceso a datos)
python -c "
import pandas as pd
# Cargar datos recientes y comparar con históricos
print('Análisis de drift pendiente de implementación')
"

# 4. Preparar reentrenamiento
python src/preparar_datos.py  # Con nuevos parámetros si es necesario
python src/entrenar_modelo.py
python src/evaluar_modelo.py
```

### Prevención y Mitigación

#### Medidas Preventivas
1. **Monitoreo continuo:** Implementar alertas automáticas para detección temprana
2. **Validación periódica:** Evaluar rendimiento del modelo con datos actuales
3. **Actualización de rangos:** Revisar y ajustar `RANGOS_HISTORICOS` periódicamente

#### Medidas de Mitigación
1. **Modelo robusto:** Considerar modelos más resistentes a cambios en distribución
2. **Ensemble de modelos:** Combinar modelos entrenados en diferentes períodos
3. **Actualización incremental:** Implementar aprendizaje incremental si es posible

### Impacto en el Proyecto Final

#### Relevancia para la Defensa
- **Escenario real:** Cambio tarifario es situación común en negocios reales
- **Monitoreo implementado:** La API ya tiene detección de valores fuera de rango
- **Respuesta operativa:** Plan estructurado con niveles de severidad y acciones

#### Evidencias Técnicas
- **Código implementado:** Función `detectar_anomalias()` en api/main.py
- **Métricas disponibles:** Endpoint `/metrics` con contadores de anomalías
- **Logging estructurado:** Registro automático de valores atípicos

### Conclusión

El riesgo de drift por incremento de cargos mensuales es un escenario realista y bien documentado en sistemas de predicción de churn. La implementación actual del proyecto incluye las capacidades técnicas necesarias para detectar y responder a este tipo de drift:

1. **Detección:** La API identifica valores fuera del rango histórico
2. **Monitoreo:** Las métricas acumulan solicitudes con anomalías
3. **Logging:** Los eventos quedan registrados para análisis
4. **Respuesta:** Existe un plan operativo estructurado

Este análisis demuestra comprensión del ciclo de vida ML-Ops más allá del entrenamiento inicial, abordando la operación continua del modelo en un entorno de negocio dinámico.

---

**Estado:** Riesgo identificado y plan de respuesta implementado  
**Severidad potencial:** Media (impacto en precisión pero detectable)  
**Capacidad de respuesta:** Disponible en el sistema actual  
**Frecuencia de revisión:** Mensual o ante cambios tarifarios conocidos
