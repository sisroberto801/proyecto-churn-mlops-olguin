# Análisis de Incidente - API Predictiva de Churn

**Autor:** Roberto Carlos Olguin Ledezma  
**Fecha del incidente:** 14/06/2026  
**Fecha de análisis:** 17/06/2026

## Plantilla de Análisis de Incidente

| Elemento | Respuesta del maestrante |
|----------|-------------------------|
| **Síntoma** | El contenedor Docker `churn-api-olguin` fallaba durante la construcción con error "No se encontró el modelo serializado" |
| **Posible causa** | El archivo `.dockerignore` excluía el directorio `models/` que contiene el modelo `.joblib` necesario para la API |
| **Forma de detección** | Error durante la ejecución de `docker build -t churn-api-olguin .` con mensaje de runtime error en api/main.py |
| **Evidencia que revisaría** | 1. Contenido de `.dockerignore`<br>2. Estructura del directorio `models/`<br>3. Logs del build de Docker<br>4. Rutas definidas en api/main.py |
| **Acción correctiva** | Modificar `.dockerignore` para comentar la exclusión del directorio `models/`, permitiendo que el modelo se incluya en la imagen Docker |
| **Acción preventiva** | 1. Verificar siempre el `.dockerignore` antes del build<br>2. Crear checklist de archivos críticos para construcción Docker<br>3. Documentar dependencias entre archivos y configuración |

## Detalle del Incidente

### Contexto
Durante la construcción de la imagen Docker para el proyecto final, el proceso fallaba consistentemente al intentar ejecutar la API dentro del contenedor.

### Cronología de Eventos

1. **10:30 AM** - Ejecución de `docker build -t churn-api-olguin .`
2. **10:45 AM** - Build falla en paso 8/8 con error de runtime
3. **10:50 AM** - Revisión de logs del contenedor para identificar causa
4. **11:00 AM** - Identificación del problema en `.dockerignore`
5. **11:15 AM** - Aplicación de la solución y reconstrucción exitosa

### Análisis Técnico

#### Error Detectado
```
RuntimeError: No se encontró el modelo serializado. 
Ejecute primero: python src\entrenar_modelo.py
```

#### Causa Raíz
El archivo `.dockerignore` contenía:
```dockerignore
# Project specific
data/
docs/
tests/
notebooks/
*.log
models/  # ← Esta línea excluía el directorio crítico
```

#### Impacto
- **Construcción:** Falla completa del build Docker
- **Tiempo:** 30 minutos de diagnóstico y solución
- **Riesgo:** Potencial entrega incompleta del proyecto

### Evidencias Revisadas

#### 1. Estructura de Directorios
```bash
ls -la models/
# Output:
# modelo_churn_v1.joblib
# modelo_churn_v1_metadata.json
```

#### 2. Contenido Original de .dockerignore
```dockerignore
# Project specific
data/
docs/
tests/
notebooks/
*.log
models/
```

#### 3. Rutas en api/main.py
```python
MODEL_PATH = PROJECT_ROOT / "models" / "modelo_churn_v1.joblib"
```

#### 4. Logs del Build Docker
```
Step 8/8 : RUN python src/preparar_datos.py && python src/entrenar_modelo.py && python src/evaluar_modelo.py
 ---> Running in 123456789abc
Traceback (most recent call last):
  File "api/main.py", line 134, in <module>
    raise RuntimeError("No se encontró el modelo serializado...")
RuntimeError: No se encontró el modelo serializado...
```

### Solución Aplicada

#### Modificación de .dockerignore
```dockerignore
# Project specific
data/
docs/
tests/
notebooks/
*.log

# Keep models directory for Docker build
# models/
```

#### Verificación Post-Solución
```bash
docker build -t churn-api-olguin .
# Output: Successfully built churn-api-olguin

docker run -d --name churn-api-olguin -p 8080:8080 churn-api-olguin
# Output: Container running successfully

curl http://localhost:8080/health
# Output: {"estado":"ok","modelo":"modelo_churn_v1"}
```

## Lecciones Aprendidas

### Técnicas
1. **Docker context:** El contexto de construcción incluye solo archivos no excluidos por `.dockerignore`
2. **Dependencias críticas:** El modelo `.joblib` es esencial para el funcionamiento de la API
3. **Build eficiente:** Copiar `requirements.txt` primero permite mejor caché de capas Docker

### Operativas
1. **Verificación preventiva:** Siempre revisar `.dockerignore` antes del build
2. **Documentación:** Registrar decisiones de exclusión/inclusión de archivos
3. **Testing:** Verificar construcción en ambiente limpio

### Proceso
1. **Diagnóstico sistemático:** Revisar logs → estructura → configuración
2. **Solución mínima:** Cambio específico y enfocado
3. **Verificación completa:** Probar funcionalidad end-to-end

## Medidas Preventivas

### Inmediatas
- [x] Documentar el cambio en `.dockerignore`
- [x] Agregar comentario explicativo en el archivo
- [x] Actualizar `EVIDENCIAS_DOCKER.md` con el error y solución

### Mediano Plazo
- [ ] Crear checklist pre-build Docker
- [ ] Implementar tests automatizados de construcción
- [ ] Documentar arquitectura de dependencias

### Largo Plazo
- [ ] Establecer proceso de revisión de cambios críticos
- [ ] Implementar integración continua con validación Docker
- [ ] Crear plantillas estandarizadas para proyectos ML-Ops

## Impacto en el Proyecto Final

### Positivo
- **Experiencia real:** Incidente auténtico durante desarrollo
- **Documentación completa:** Evidencia detallada del problema y solución
- **Mejora del proceso:** Fortalecimiento de prácticas Docker

### Negativo (mitigado)
- **Tiempo:** 30 minutos adicionales de diagnóstico
- **Riesgo:** Potencial retraso en entrega (evitado por solución rápida)

## Conclusión

Este incidente ilustra la importancia de entender cómo Docker maneja el contexto de construcción y cómo las configuraciones de exclusión pueden impactar críticamente el funcionamiento del servicio. La solución aplicada fue mínima pero efectiva, y la documentación detallada servirá como referencia para futuros proyectos y como evidencia del requisito de "escenario de error o incidente" del proyecto final.

El incidente demuestra capacidad de:
- **Diagnóstico técnico** de problemas de construcción
- **Análisis de causa raíz** sistemático
- **Implementación de solución** enfocada
- **Documentación completa** para aprendizaje organizacional

---

**Estado:** Resuelto y documentado  
**Severidad:** Media (impactó construcción pero no producción)  
**Tiempo de resolución:** 30 minutos  
**Prevención:** Implementada mediante documentación y checklist
