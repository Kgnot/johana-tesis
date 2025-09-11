from typing import Tuple

import numpy as np
from matplotlib import pyplot as plt
from numpy import ndarray

"""
    Pasamos la columna, el tiempo y generamos un mapa con las característica
"""


def calcular_caracteristicas(columna: np.ndarray, tiempo: np.ndarray) -> dict:
    # Validar datos de entrada
    if len(columna) == 0:
        raise ValueError("La columna no puede estar vacía")
    if len(tiempo) != len(columna):
        raise ValueError("Tiempo y columna deben tener la misma longitud")
    if len(columna) == 1:
        # Manejar caso de un solo punto
        jerk = np.array([0.0])  # Jerk cero para un solo punto
    else:
        jerk = np.gradient(columna, tiempo)

    rms = np.sqrt(np.mean(columna ** 2))
    potencia = np.mean(columna ** 2)  # np.sqrt((np.sum(columna)) ** 2)
    energia = np.sum(columna ** 2)  # (np.sum(columna)) ** 2
    mini = np.min(columna)
    maxi = np.max(columna)
    rango = maxi - mini
    jerk = np.gradient(columna, tiempo)

    return {
        "RMS": rms,
        "Potencia": potencia,
        "Energía": energia,
        "Valor Mínimo": mini,
        "Valor Máximo": maxi,
        "Rango Aceleraciones": rango,
        "Jerk": jerk,
        "Jerk Máximo": np.max(jerk),
        "Jerk Mínimo": np.min(jerk),
        "Jerk Medio": np.mean(jerk)
    }


"""
    n es la longitud de la columna que se pasa.
    Y con linspace sacamos puntos intermedios entre 0 y la duración.
    Devolvemos una tupla entre dicho linspace y la duración
"""


def generar_tiempo(n: int) -> Tuple[ndarray, float]:
    if n <= 0:
        raise ValueError("n debe ser un número positivo mayor que 0")

    duracion = n / 100.0
    return np.linspace(0, duracion, n), duracion


def graficar_jerk(tiempo: np.ndarray, jerk: np.ndarray, i: int, etiqueta: str = None):
    """Genera un gráfico de jerk vs. tiempo."""
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(tiempo, jerk)
    lab = ['Acc_X', 'Acc_Y', 'Acc_Z']
    ax.set_title(f"Jerk vs Tiempo {lab[i]}")
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Jerk (m/s³)")
    ax.grid(True)
    return fig


""" 
    La función principal aqui se basa en optener una señal, y devolvemos los resultados y un grafico_jerk
    Agregamos un etiquetas=None para facilitar el testing.
"""


def featuresac(senial: np.ndarray, etiquetas=None):
    if not isinstance(senial, np.ndarray):
        raise ValueError("La señal debe ser un array de numpy")

    senialf = np.array(senial)
    # la señal debe ser array de numpy
    if senialf.ndim > 2:
        raise ValueError("La señal debe ser 1D o 2D")

    if senialf.ndim == 1:
        senialf = senialf.reshape(-1, 1)
    ## Miramos la cantidad de columnas
    n_columnas = senialf.shape[1]
    # hacemos validación.
    if etiquetas is None:
        etiquetas = [f"Col_{i}" for i in range(senialf.shape[1])]
    elif len(etiquetas) != n_columnas:
        raise ValueError("El número de etiquetas no coincide con el número de columnas")

    resultados = []
    jerk_graficos = []
    nc = senialf.shape[1]

    for y in range(nc):
        columna = senialf[:, y]
        tiempo, duracion = generar_tiempo(len(columna))
        caracteristicas = calcular_caracteristicas(columna, tiempo)
        caracteristicas["Tiempo de la Prueba (s)"] = duracion  # añade un elemento al diccionario
        resultados.append(caracteristicas)

        # Crear y guardar gráfico
        if len(columna) > 5:
            jerk_graficos.append(graficar_jerk(tiempo, caracteristicas["Jerk"], y, etiquetas[y]))

    return resultados, jerk_graficos
