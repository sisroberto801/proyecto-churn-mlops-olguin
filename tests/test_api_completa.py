import json

import requests

BASE_URL = "http://localhost:8000"


def test_endpoints_basicos():
    print("=== PRUEBAS DE ENDPOINTS BÁSICOS ===")

    response = requests.get(f"{BASE_URL}/")
    print(f"GET /: {response.status_code} - {response.json()}")
    assert response.status_code == 200

    response = requests.get(f"{BASE_URL}/health")
    print(f"GET /health: {response.status_code} - {response.json()}")
    assert response.status_code == 200

    response = requests.get(f"{BASE_URL}/info")
    print(f"GET /info: {response.status_code} - {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200


def test_caso_valido():
    print("\n=== PRUEBA DE CASO VÁLIDO ===")

    datos_validos = {
        "antiguedad": 12,
        "cargo_mensual": 95.5,
        "reclamos": 3
    }

    response = requests.post(f"{BASE_URL}/predict", json=datos_validos)
    print(f"Caso válido: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200

    respuesta = response.json()
    assert "prediccion" in respuesta
    assert "probabilidad" in respuesta
    assert "version_modelo" in respuesta
    assert "autor" in respuesta


def test_campo_faltante():
    print("\n=== PRUEBA DE CAMPO FALTANTE ===")

    datos_incompletos = {
        "antiguedad": 12,
        "cargo_mensual": 95.5
    }

    response = requests.post(f"{BASE_URL}/predict", json=datos_incompletos)
    print(f"Campo faltante: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 422


def test_tipo_dato_incorrecto():
    print("\n=== PRUEBA DE TIPO DE DATO INCORRECTO ===")

    datos_tipo_erroneo = {
        "antiguedad": "doce",
        "cargo_mensual": 95.5,
        "reclamos": 3
    }

    response = requests.post(f"{BASE_URL}/predict", json=datos_tipo_erroneo)
    print(f"Tipo incorrecto: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 422


def test_valor_fuera_de_rango():
    print("\n=== PRUEBA DE VALOR FUERA DE RANGO ===")

    datos_antiguedad_invalida = {
        "antiguedad": 150,
        "cargo_mensual": 95.5,
        "reclamos": 3
    }

    response = requests.post(f"{BASE_URL}/predict", json=datos_antiguedad_invalida)
    print(f"Antigüedad fuera de rango: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 422

    datos_cargo_invalido = {
        "antiguedad": 12,
        "cargo_mensual": 2000,
        "reclamos": 3
    }

    response = requests.post(f"{BASE_URL}/predict", json=datos_cargo_invalido)
    print(f"Cargo mensual fuera de rango: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 422


def test_valores_negativos():
    print("\n=== PRUEBA DE VALORES NEGATIVOS ===")

    datos_negativos = {
        "antiguedad": -5,
        "cargo_mensual": -100,
        "reclamos": 3
    }

    response = requests.post(f"{BASE_URL}/predict", json=datos_negativos)
    print(f"Valores negativos: {response.status_code}")
    print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 422


def test_varios_casos_validos():
    print("\n=== PRUEBA DE MÚLTIPLES CASOS VÁLIDOS ===")

    casos = [
        {
            "nombre": "Cliente nuevo, bajo cargo",
            "datos": {
                "antiguedad": 6,
                "cargo_mensual": 50.0,
                "reclamos": 0
            }
        },
        {
            "nombre": "Cliente estable, cargo moderado",
            "datos": {
                "antiguedad": 24,
                "cargo_mensual": 150.0,
                "reclamos": 1
            }
        },
        {
            "nombre": "Cliente antiguo, alto cargo, muchos reclamos",
            "datos": {
                "antiguedad": 60,
                "cargo_mensual": 500.0,
                "reclamos": 8
            }
        }
    ]

    for caso in casos:
        response = requests.post(f"{BASE_URL}/predict", json=caso["datos"])
        print(f"\n{caso['nombre']}: {response.status_code}")
        print(f"Respuesta: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200


if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBAS COMPLETAS DE API")
    print("=" * 50)

    try:
        test_endpoints_basicos()
        test_caso_valido()
        test_campo_faltante()
        test_tipo_dato_incorrecto()
        test_valor_fuera_de_rango()
        test_valores_negativos()
        test_varios_casos_validos()

        print("\n" + "=" * 50)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS EXITOSAMENTE")
        print("✅ API lista para producción")

    except Exception as e:
        print(f"\n❌ ERROR EN PRUEBAS: {e}")
        print("Asegúrate de que la API esté corriendo en http://localhost:8000")
