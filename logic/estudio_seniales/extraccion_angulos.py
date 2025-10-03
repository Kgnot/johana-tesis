import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


def artan(senial, longitud_filtro=31, figsize=(8, 4)):
    """
    Calcula ángulos de inclinación a partir de señales 3D y genera estadísticas y gráficos.

    Args:
        senial: Array o lista con 3 componentes (X, Y, Z)
        longitud_filtro: Longitud del filtro de suavizado (debe ser impar)
        figsize: Tamaño de las figuras

    Returns:
        estadisticas: DataFrame con estadísticas de los ángulos
        graficos: Lista de figuras de matplotlib
    """
    # Convertir a array numpy y validar
    senial_array = np.array(senial)

    # Validar dimensiones
    if senial_array.size == 0:
        raise ValueError("La señal no puede estar vacía")

    # Asegurar que tenga forma (3, n_muestras)
    if senial_array.ndim == 1:
        if len(senial_array) != 3:
            raise ValueError("La señal 1D debe tener exactamente 3 componentes")
        senial_array = senial_array.reshape(3, 1)
    elif senial_array.ndim == 2:
        if senial_array.shape[0] != 3 and senial_array.shape[1] == 3:
            # Transponer si está en formato (n_muestras, 3)
            senial_array = senial_array.T
        if senial_array.shape[0] != 3:
            raise ValueError("La señal debe tener exactamente 3 componentes (X, Y, Z)")
    else:
        raise ValueError("La señal debe ser 1D o 2D")

    # Evitar división por cero en componente Z
    z_component = senial_array[2].copy()
    z_component[np.abs(z_component) < 1e-10] = 1e-10 * np.sign(z_component[np.abs(z_component) < 1e-10])

    # Calcular ángulos vectorizadamente
    angulos_x = np.arctan(senial_array[1] / z_component)  # atan(Y/Z)
    angulos_y = np.arctan(senial_array[0] / z_component)  # atan(X/Z)

    # Calcular estadísticas
    estadisticas = _calcular_estadisticas(angulos_x, angulos_y)

    # Aplicar suavizado
    angulos_x_suave, angulos_y_suave = _aplicar_suavizado(
        angulos_x, angulos_y, longitud_filtro
    )

    # Generar gráficos
    graficos = _generar_graficos(angulos_x_suave, angulos_y_suave, figsize)

    return estadisticas, graficos

def _calcular_estadisticas(angulos_x, angulos_y):
    """Calcula estadísticas básicas de los ángulos"""
    # Convertir a grados para mejor interpretación
    angulos_x_deg = np.degrees(angulos_x)
    angulos_y_deg = np.degrees(angulos_y)

    datos = [
        {
            'Ángulo': 'X',
            'Ángulo mínimo': np.min(angulos_x_deg),
            'Ángulo máximo': np.max(angulos_x_deg),
            'Rango': np.ptp(angulos_x_deg)
        },
        {
            'Ángulo': 'Y',
            'Ángulo mínimo': np.min(angulos_y_deg),
            'Ángulo máximo': np.max(angulos_y_deg),
            'Rango': np.ptp(angulos_y_deg)
        }
    ]

    return pd.DataFrame(datos)

def _aplicar_suavizado(angulos_x, angulos_y, longitud_filtro):
    """Aplica filtro de suavizado a los ángulos"""
    if longitud_filtro <= 1 or len(angulos_x) <= longitud_filtro:
        return angulos_x, angulos_y

    # Asegurar que la longitud del filtro sea impar
    if longitud_filtro % 2 == 0:
        longitud_filtro += 1

    try:
        # Usar Savitzky-Golay filter para mejor suavizado
        from scipy.signal import savgol_filter
        x_suave = savgol_filter(angulos_x, longitud_filtro, 3)
        y_suave = savgol_filter(angulos_y, longitud_filtro, 3)
        return x_suave, y_suave
    except ImportError:
        # Fallback a media móvil simple
        kernel = np.ones(longitud_filtro) / longitud_filtro
        x_suave = np.convolve(angulos_x, kernel, mode='same')
        y_suave = np.convolve(angulos_y, kernel, mode='same')
        return x_suave, y_suave

def _generar_graficos(angulos_x_suave, angulos_y_suave, figsize):
    """Genera los gráficos de los ángulos."""
    respuesta_graficos = []

    # Gráfico para ángulo X
    fig_x = _crear_grafico_individual(
        angulos_x_suave,
        'Ángulo de inclinación en X',
        'Tiempo (muestras)',
        'Ángulo (radianes)',
        figsize
    )
    respuesta_graficos.append(fig_x)

    # Gráfico para ángulo Y
    fig_y = _crear_grafico_individual(
        angulos_y_suave,
        'Ángulo de inclinación en Y',
        'Tiempo (muestras)',
        'Ángulo (radianes)',
        figsize
    )
    respuesta_graficos.append(fig_y)

    return respuesta_graficos

def _crear_grafico_individual(datos, titulo, xlabel, ylabel, figsize):
    """Crea un gráfico individual con la configuración dada"""
    fig, ax = plt.subplots(figsize=figsize)
    ax.plot(datos)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.grid(True)
    plt.tight_layout()  # Mejorar espaciado
    return fig