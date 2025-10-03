import math

import numpy as np
import pandas as pd

from logic.estudio_seniales.extraccion_angulos import artan


def test_funcionamiento_basico():
    """Test 1: Verifica el funcionamiento básico de artan."""
    print("🧪 Test 1: Funcionamiento básico")

    senial_test = np.random.rand(3, 100)  # Señal 3D con 100 muestras
    senial_test[2] = np.abs(senial_test[2]) + 0.1  # Evitar división por cero

    estadisticas, graficos = artan(senial_test)

    print(f"   - DataFrame generado: {estadisticas.shape}")
    print(f"   - Gráficos generados: {len(graficos)}")
    print(f"   - Columnas: {list(estadisticas.columns)}")

    assert len(graficos) == 2, "Deben generarse exactamente 2 gráficos"
    assert estadisticas.shape == (2, 4), "DataFrame debe tener 2 filas y 4 columnas"
    assert list(estadisticas.columns) == ['Ángulo', 'Ángulo mínimo', 'Ángulo máximo', 'Rango']

    print("   ✓ Test funcionamiento básico pasado")

def test_validacion_entrada():
    """Test 2: Verifica que se valide correctamente la entrada."""
    # Test con dimensiones incorrectas
    senial_invalida = np.random.rand(2, 100)  # Solo 2 componentes
    try:
        estadisticas, graficos = artan(senial_invalida)
        raise AssertionError("Debería haber lanzado un ValueError")
    except ValueError as e:
        print(e)
    try:
        senial_vacia = np.array([]).reshape(3, 0)
        estadisticas, graficos = artan(senial_vacia)
    except Exception as e:
        print(e)

def test_formatos_entrada():
    """Test 3: Verifica diferentes formatos de entrada."""
    # Lista de listas
    senial_lista = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    estadisticas1, graficos1 = artan(senial_lista)
    # Array numpy 2D
    senial_numpy = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
    estadisticas2, graficos2 = artan(senial_numpy)
    # Verificar que ambos formatos dan el mismo resultado
    pd.testing.assert_frame_equal(estadisticas1, estadisticas2)

def test_parametros_opcionales():
    """Test 4: Verifica parámetros opcionales."""
    senial_test = np.random.rand(3, 50)
    senial_test[2] = np.abs(senial_test[2]) + 0.1
    # Sin suavizado
    estadisticas1, graficos1 = artan(senial_test, longitud_filtro=0)
    # Con suavizado diferente
    estadisticas2, graficos2 = artan(senial_test, longitud_filtro=21)
    # Tamaño de figura personalizado
    estadisticas3, graficos3 = artan(senial_test, figsize=(10, 6))
    # Verificar que las estadísticas son consistentes
    assert estadisticas1.shape == estadisticas2.shape == estadisticas3.shape

def test_validacion_contenido():
    """Test 5: Verifica la correctitud de los cálculos."""
    # Señal conocida para verificar cálculos
    senial_conocida = np.array([
        [0, 1, 2],  # X
        [0, 0, 0],  # Y
        [1, 1, 1]  # Z
    ])

    estadisticas, graficos = artan(senial_conocida, longitud_filtro=1)

    # Verificar ángulos X (atan(Y/Z) = atan(0/1) = 0)
    angulo_x_min = estadisticas.loc[0, 'Ángulo mínimo']
    angulo_x_max = estadisticas.loc[0, 'Ángulo máximo']

    # Los ángulos están en grados, convertir a radianes para comparar
    angulo_x_min_rad = math.radians(angulo_x_min)
    angulo_x_max_rad = math.radians(angulo_x_max)

    assert abs(angulo_x_min_rad) < 1e-10, f"Ángulo X mínimo debería ser ~0, got {angulo_x_min_rad}"
    assert abs(angulo_x_max_rad) < 1e-10, f"Ángulo X máximo debería ser ~0, got {angulo_x_max_rad}"

    # Verificar ángulos Y (atan(X/Z) = atan([0,1,2]/1) = [0, π/4, atan(2)])
    angulo_y_min = estadisticas.loc[1, 'Ángulo mínimo']
    angulo_y_max = estadisticas.loc[1, 'Ángulo máximo']

    # Convertir a radianes para comparar
    angulo_y_min_rad = math.radians(angulo_y_min)
    angulo_y_max_rad = math.radians(angulo_y_max)

    expected_y_min = 0
    expected_y_max = math.atan(2)  # Esto está en radianes

    assert abs(angulo_y_min_rad - expected_y_min) < 1e-10, f"Ángulo Y mínimo incorrecto: {angulo_y_min_rad} vs {expected_y_min}"
    assert abs(angulo_y_max_rad - expected_y_max) < 1e-6, f"Ángulo Y máximo incorrecto: {angulo_y_max_rad} vs {expected_y_max}"

def test_casos_borde():
    """Test 6: Casos borde y situaciones especiales."""
    # Señal con un solo punto
    senial_un_punto = np.array([[1], [2], [3]])
    try:
        estadisticas, graficos = artan(senial_un_punto)
    except Exception as e:
        print(e)

    # Señal con valores muy pequeños en Z (cerca de cero)
    senial_z_pequena = np.random.rand(3, 10)
    senial_z_pequena[2] = 1e-10  # Valores muy pequeños
    try:
        estadisticas, graficos = artan(senial_z_pequena)
    except Exception as e:
        print(e)