import matplotlib
import numpy as np
import pytest
import matplotlib.pyplot as plt
matplotlib.use('Agg')

# Importar las funciones del módulo de velocidad
from logic.estudio_seniales.caracteristica_velocidad import (
    calcular_caracteristicas, generar_tiempo, grafico, featuresvel
)


def test_generar_tiempo():
    """Test de generación de tiempo"""
    tiempo, duracion = generar_tiempo(100)
    assert len(tiempo) == 100
    assert np.isclose(duracion, 1.0)  # 100 muestras -> 1.0s


def test_generar_tiempo_edge_cases():
    """Test casos edge de generación de tiempo"""
    # Test con n = 1
    tiempo, duracion = generar_tiempo(1)
    assert len(tiempo) == 1
    assert np.isclose(duracion, 0.01)

    # Test con n inválido
    with pytest.raises(ValueError):
        generar_tiempo(0)


def test_calcular_caracteristicas_senoidal():
    """Test con señal senoidal"""
    n = 100
    tiempo, _ = generar_tiempo(n)
    senal = np.sin(2 * np.pi * tiempo)
    features = calcular_caracteristicas(senal, tiempo)

    assert "RMS" in features
    assert "Potencia" in features
    assert "Energía" in features
    assert "Valor Máximo" in features
    assert "Valor Mínimo" in features
    assert "Rango Velocidades" in features


def test_calcular_caracteristicas_constante():
    """Test con señal constante"""
    n = 50
    tiempo = np.linspace(0, 1, n)
    senal = np.ones(n) * 5.0

    features = calcular_caracteristicas(senal, tiempo)

    assert np.isclose(features["RMS"], 5.0)
    assert np.isclose(features["Valor Mínimo"], 5.0)
    assert np.isclose(features["Valor Máximo"], 5.0)
    assert np.isclose(features["Rango Velocidades"], 0.0)
    # Para señal constante, potencia y energía tienen valores específicos
    assert np.isclose(features["Potencia"], abs(5.0 * n))
    assert np.isclose(features["Energía"], (5.0 * n) ** 2)


def test_calcular_caracteristicas_vacia():
    """Test con array vacío"""
    with pytest.raises(Exception):  # Debería lanzar alguna excepción
        calcular_caracteristicas(np.array([]), np.array([]))


def test_grafico():
    """Test de generación de gráfico"""
    tiempo = np.linspace(0, 1, 10)
    velocidad = np.random.randn(10)
    fig = grafico(velocidad, tiempo, 0)

    assert fig is not None
    assert isinstance(fig, plt.Figure)


def test_grafico_indice_invalido():
    """Test con índice inválido para etiquetas"""
    tiempo = np.linspace(0, 1, 10)
    velocidad = np.random.randn(10)

    # Debería manejar índices fuera de rango
    fig = grafico(velocidad, tiempo, 5)  # Índice fuera de [0,2]
    assert fig is not None


def test_featuresvel_multicolumna():
    """Test con datos multicolumna"""
    t = np.linspace(0, 2 * np.pi, 100)
    datos = np.column_stack([
        np.sin(t),  # Columna X
        np.cos(t),  # Columna Y
        np.sin(2 * t)  # Columna Z
    ])

    # Mock de datosfinal_total (aunque no se usa)
    datosfinal_total = None

    resultados, graficos = featuresvel(datos, datosfinal_total, etiquetas=["X", "Y", "Z"])

    assert len(resultados) == 3
    assert len(graficos) == 3
    assert all("RMS" in r for r in resultados)
    assert all("Tiempo de la Prueba (s)" in r for r in resultados)


def test_featuresvel_columna_unica():
    """Test con datos de una sola columna"""
    datos = np.sin(np.linspace(0, 4 * np.pi, 100))
    datosfinal_total = None

    resultados, graficos = featuresvel(datos, datosfinal_total)

    assert len(resultados) == 1
    assert len(graficos) == 1
    assert "RMS" in resultados[0]


def test_featuresvel_etiquetas_incorrectas():
    """Test con número incorrecto de etiquetas"""
    datos = np.random.randn(50, 2)
    datosfinal_total = None

    with pytest.raises(ValueError):
        featuresvel(datos, datosfinal_total, etiquetas=["X", "Y", "Z"])  # 3 etiquetas para 2 columnas


def test_featuresvel_datos_pequenos():
    """Test con pocos datos"""
    datos = np.array([[1], [2], [3]])  # Solo 3 puntos
    datosfinal_total = None

    resultados, graficos = featuresvel(datos, datosfinal_total)

    assert len(resultados) == 1
    assert len(graficos) == 1  # Debería generar gráfico igualmente


def test_featuresvel_entrada_invalida():
    """Test con entrada inválida"""
    datosfinal_total = None

    with pytest.raises(ValueError):
        featuresvel("not_an_array", datosfinal_total)

    with pytest.raises(ValueError):
        featuresvel(np.random.randn(10, 5, 3), datosfinal_total)  # 3D array


def test_featuresvel_sin_datosfinal_total():
    """Test sin pasar datosfinal_total"""
    datos = np.random.randn(50, 2)

    # Debería funcionar aunque no se pase el parámetro
    resultados, graficos = featuresvel(datos, None)
    assert len(resultados) == 2


def test_valores_velocidad():
    """Test con valores de velocidad específicos"""
    tiempo = np.linspace(0, 1, 100)
    velocidad = np.ones(100) * 10.0  # velocidad constante de 10 rad/s

    features = calcular_caracteristicas(velocidad, tiempo)

    # Verificar cálculos específicos
    assert np.isclose(features["RMS"], 10.0)
    assert np.isclose(features["Potencia"], abs(10.0 * 100))  # |∑vᵢ|
    assert np.isclose(features["Energía"], (10.0 * 100) ** 2)  # (∑vᵢ)²


def test_formulas_consistencia():
    """Test de consistencia en las fórmulas"""
    columna = np.array([1, 2, 3, 4, 5])
    tiempo = np.linspace(0, 1, 5)

    features = calcular_caracteristicas(columna, tiempo)

    # Verificar cálculos manuales
    suma = np.sum(columna)
    assert np.isclose(features["Potencia"], abs(suma))
    assert np.isclose(features["Energía"], suma ** 2)
    assert np.isclose(features["RMS"], np.sqrt(np.mean(columna ** 2)))