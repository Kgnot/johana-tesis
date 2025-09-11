import numpy as np
import pytest
import matplotlib
matplotlib.use('Agg')
from logic.estudio_seniales.caracteristica_aceleracion import (
    calcular_caracteristicas, generar_tiempo, graficar_jerk, featuresac
)


def test_generar_tiempo():
    tiempo, duracion = generar_tiempo(100)
    assert len(tiempo) == 100
    assert np.isclose(duracion, 1.0)  # 100 muestras -> 1.0s


def test_generar_tiempo_edge_cases():
    # Test con n = 1
    tiempo, duracion = generar_tiempo(1)
    assert len(tiempo) == 1
    assert np.isclose(duracion, 0.01)

    # Test con n inválido
    with pytest.raises(ValueError):
        generar_tiempo(0)


def test_calcular_caracteristicas_senoidal():
    n = 100
    tiempo, _ = generar_tiempo(n)
    senal = np.sin(2 * np.pi * tiempo)
    features = calcular_caracteristicas(senal, tiempo)

    assert "RMS" in features
    assert "Jerk" in features
    assert isinstance(features["Jerk"], np.ndarray)
    # Para una senoidal, el RMS debería estar cerca de 1/sqrt(2)
    assert np.isclose(features["RMS"], 1 / np.sqrt(2), atol=0.1)


def test_calcular_caracteristicas_constante():
    """Test con señal constante"""
    n = 50
    tiempo = np.linspace(0, 1, n)
    senal = np.ones(n) * 5.0

    features = calcular_caracteristicas(senal, tiempo)

    assert np.isclose(features["RMS"], 5.0)
    assert np.isclose(features["Valor Mínimo"], 5.0)
    assert np.isclose(features["Valor Máximo"], 5.0)
    assert np.isclose(features["Rango Aceleraciones"], 0.0)
    # Jerk de señal constante debería ser ~0
    assert np.allclose(features["Jerk"], 0, atol=1e-10)


def test_calcular_caracteristicas_dimensiones_incorrectas():
    """Test manejo de errores en dimensiones"""
    with pytest.raises(ValueError):
        calcular_caracteristicas(np.array([1, 2, 3]), np.array([1, 2]))

    with pytest.raises(ValueError):
        calcular_caracteristicas(np.array([]), np.array([]))


def test_graficar_jerk():
    tiempo = np.linspace(0, 1, 10)
    jerk = np.random.randn(10)
    fig = graficar_jerk(tiempo, jerk, 1, "Test")
    assert fig is not None

    # Test dimensiones incorrectas
    with pytest.raises(ValueError):
        graficar_jerk(tiempo, jerk[:-1], 1, "Test")


def test_featuresac_multicolumna():
    """Test con datos multicolumna"""
    t = np.linspace(0, 2 * np.pi, 100)
    datos = np.column_stack([
        np.sin(t),  # Columna X
        np.cos(t),  # Columna Y
        np.sin(2 * t)  # Columna Z
    ])
    resultados, graficos = featuresac(datos, etiquetas=["X", "Y", "Z"])
    assert len(resultados) == 3
    assert len(graficos) == 3
    assert all("RMS" in r for r in resultados)
    assert all("Tiempo de la Prueba (s)" in r for r in resultados)


def test_featuresac_columna_unica():
    """Test con datos de una sola columna"""
    datos = np.sin(np.linspace(0, 4 * np.pi, 100))
    resultados, graficos = featuresac(datos)

    assert len(resultados) == 1
    assert len(graficos) == 1
    assert "RMS" in resultados[0]


def test_featuresac_etiquetas_incorrectas():
    """Test con número incorrecto de etiquetas"""
    datos = np.random.randn(50, 2)

    with pytest.raises(ValueError):
        featuresac(datos, etiquetas=["X", "Y", "Z"])  # 3 etiquetas para 2 columnas


def test_featuresac_datos_pequenos():
    """Test con pocos datos (no debería generar gráfico)"""
    datos = np.array([[1], [2], [3]])  # Solo 3 puntos
    resultados, graficos = featuresac(datos)

    assert len(resultados) == 1
    assert len(graficos) == 0  # No debe generar gráfico con <= 5 puntos


def test_featuresac_entrada_invalida():
    """Test con entrada inválida"""
    with pytest.raises(ValueError):
        featuresac("not_an_array")

    with pytest.raises(ValueError):
        featuresac(np.random.randn(10, 5, 3))  # 3D array


def test_valores_fisica():
    """Test con valores que tengan sentido físico"""
    # Simular aceleración gravitacional constante
    tiempo = np.linspace(0, 1, 100)
    aceleracion_z = np.ones(100) * 9.81  # gravedad

    features = calcular_caracteristicas(aceleracion_z, tiempo)

    assert np.isclose(features["RMS"], 9.81)
    assert np.isclose(features["Energía"], 9.81 ** 2 * 100, rtol=1e-3)
    assert np.isclose(features["Potencia"], 9.81 ** 2, rtol=1e-3)


def test_numpy_formula_potencia():
    columna = np.array([1, 2, 3, 4, 5])
    cuadrados = columna ** 2
    suma = np.sum(cuadrados)
    potencia_manual = suma / len(columna)
    potencia_automatica = np.mean(columna ** 2)
    assert potencia_manual == potencia_automatica
