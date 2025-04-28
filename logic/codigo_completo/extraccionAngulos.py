import io

import numpy as np
import pandas as pd
import math

from PIL import Image
from matplotlib import pyplot as plt


########Extracción de angulos:
def artan(senial):
    respuesta_graficos = []
    seniala = np.squeeze(np.array(senial)).T
    X = []
    Y = []
    for i in range(len(seniala[0])):
        anguloX = math.atan(seniala[1][i] / seniala[2][i])
        anguloY = math.atan(seniala[0][i] / seniala[2][i])
        X.append(anguloX)
        Y.append(anguloY)

    # Calcular características
    minax = np.min(X)
    maxax = np.max(X)
    rangox = maxax - minax
    minay = np.min(Y)
    maxay = np.max(Y)
    rangoy = maxay - minay

    # Suavizado simple
    long = 31
    coefi = np.ones(long)
    b = coefi / long
    anx = np.array(X)
    any = np.array(Y)
    X_suave = np.convolve(anx, b, mode='same')
    Y_suave = np.convolve(any, b, mode='same')

    # --- Figura para Ángulo X ---
    figX, axX = plt.subplots(figsize=(8, 4))
    axX.plot(X_suave)
    axX.set_title('Ángulo de inclinación en X')
    axX.set_xlabel('Tiempo')
    axX.set_ylabel('Ángulo (radianes)')
    axX.grid(True)
    respuesta_graficos.append(figX)

    # --- Figura para Ángulo Y ---
    figY, axY = plt.subplots(figsize=(8, 4))
    axY.plot(Y_suave)
    axY.set_title('Ángulo de inclinación en Y')
    axY.set_xlabel('Tiempo')
    axY.set_ylabel('Ángulo (radianes)')
    axY.grid(True)
    respuesta_graficos.append(figY)

    # Características de los ángulos
    datos = [["X", minax, maxax, rangox], ["Y", minay, maxay, rangoy]]
    angulos = pd.DataFrame(datos, columns=['Ángulo', 'Ángulo mínimo', 'Ángulo máximo', 'Rango'])

    return angulos, respuesta_graficos