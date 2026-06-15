# Instrucciones de ejecución

## 1. Entrar al proyecto

```bash
cd proyecto_churn_mlops
```

## 2. Instalar librerías

```bash
python -m pip install -r requirements.txt
```

## 3. Ejecutar preparación de datos

```bash
python src/preparar_datos.py
```

## 4. Entrenar el modelo

```bash
python src/entrenar_modelo.py
```

## 5. Evaluar el modelo

```bash
python src/evaluar_modelo.py
```

## 6. Ejecutar la API

```bash
uvicorn api.main:app --reload
```

Abrir en el navegador:

```text
http://127.0.0.1:8000
```

Documentación automática:

```text
http://127.0.0.1:8000/docs
```

## 7. Probar la API

En Swagger, usar el endpoint:

```text
POST /predict
```

Ejemplo de entrada:

```json
{
  "edad": 28,
  "antiguedad_meses": 8,
  "saldo_promedio": 1200,
  "reclamos": 3,
  "usa_app": 0
}
```

## 8. Ejecutar pruebas

Detener la API con `Ctrl + C` y ejecutar:

```bash
pytest
```

Resultado esperado:

```text
2 passed
```
## 9. Limpiar caché del proyecto (opcional)

Para limpiar archivos de caché de Python:

```bash
find . -type d -name "__pycache__" -exec rm -rf {} + && find . -name "*.pyc" -delete && find . -name "*.pyo" -delete
```

## 10. Nota sobre trazabilidad

Cada cambio importante del proyecto debe registrarse mediante commits claros y descriptivos.

Esto permite conocer la evolución del código, la documentación, las pruebas y la configuración del proyecto.

## 11. Solución de problemas comunes

### Error: FileNotFoundError al evaluar el modelo

Si aparece el error "No se encontró el modelo entrenado", asegúrate de ejecutar los scripts en orden:
1. `python src/preparar_datos.py`
2. `python src/entrenar_modelo.py`
3. `python src/evaluar_modelo.py`

### Error: X has N features, but StandardScaler is expecting M features

Este error fue corregido. El script de evaluación ahora mapea automáticamente las características del dataset a las que el modelo espera.
