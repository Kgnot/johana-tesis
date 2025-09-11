import numpy as np
import matplotlib.pyplot as plt
from numpy import ndarray
from typing import Tuple


def calcular_caracteristicas(columna: np.ndarray, tiempo: np.ndarray) -> dict:
    # Validar datos de entrada
    if len(columna) == 0:
        raise ValueError("La columna no puede estar vacía")
    if len(tiempo) != len(columna):
        raise ValueError("Tiempo y columna deben tener la misma longitud")
    rms = np.sqrt(np.mean(columna ** 2))  # Cálculo del RMS
    potencia = np.sqrt((sum(columna)) ** 2)  # Media
    energia = (sum(columna)) ** 2  # Desviación estándar
    maxi = np.max(columna)  # Máximo
    mini = np.min(columna)  # Mínimo
    rango = maxi - mini  # Rango

    return {
        "RMS": rms,
        "Potencia": potencia,
        "Energía": energia,
        "Valor Máximo": maxi,
        "Valor Mínimo": mini,
        "Rango Velocidades": rango
    }


def generar_tiempo(n: int) -> Tuple[ndarray, float]:
    if n <= 0:
        raise ValueError("n debe ser un número positivo mayor que 0")

    duracion = n / 100.0
    return np.linspace(0, duracion, n), duracion


def grafico(columna: ndarray, tiempo: np.ndarray, i: int):
    lab = ['V.Angular_x', 'Ve.Angular_y', 'V.angular_z']
    if i < 0 or i >= len(lab):
        etiqueta = f"Columna_{i}"
    else:
        etiqueta = lab[i]
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(tiempo, columna)
    ax.set_title(f"Velocidad Angular vs Tiempo {etiqueta}")
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Velocidad Angular (rad/s)")
    ax.grid(True)
    return fig


def featuresvel(senial, datosfinal_total, etiquetas=None):
    if not isinstance(senial, np.ndarray):
        raise ValueError("La señal debe ser un array de numpy")

    senialf = np.array(senial)
    # la señal debe ser array de numpy
    if senialf.ndim > 2:
        raise ValueError("La señal debe ser 1D o 2D")

    if senialf.ndim == 1:
        senialf = senialf.reshape(-1, 1)
    nc = senialf.shape[1]
    # Inicializa listas para almacenar los resultados
    if etiquetas is None:
        etiquetas = [f"Col_{i}" for i in range(senialf.shape[1])]
    elif len(etiquetas) != nc:
        raise ValueError("El número de etiquetas no coincide con el número de columnas")

    resultados = []
    graficos = []
    for i in range(nc):
        columna = senialf[:, i]
        tiempo, duracion = generar_tiempo(len(columna))
        caracteristicas = calcular_caracteristicas(columna, tiempo)
        caracteristicas["Tiempo de la Prueba (s)"] = duracion
        resultados.append(caracteristicas)
        graficos.append(grafico(columna, tiempo, i))

    return resultados, graficos
