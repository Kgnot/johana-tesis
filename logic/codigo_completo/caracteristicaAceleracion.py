import io

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from tabulate import tabulate


## Aqui tenemos que guardar dos respuestas, graficos y tabla
def featuresac(senial):
    # Inicializa listas para almacenar las características
    rms_list = []
    potencia_list = []
    energia_list = []
    minimo_list = []
    maximo_list = []
    rango_list = []
    jerkl = []
    jerkmin = []
    jerkmax = []
    jerkrms = []
    jerkmedia = []
    tiempot = []
    jerk_graficos = []

    # Asegúrate de que la señal sea un array de NumPy
    senialf = np.array(senial)

    lab = ['Acc_X', 'Acc_Y', 'Acc_Z']
    nc = senialf.shape[1]
    for y in range(nc):
        columna = senialf[:, y]
        li = len(columna) / 100
        lo = len(columna)
        tiempot.append(li)
        tm = np.random.uniform(0, li, lo)
        tiempo = np.sort(tm)

        rms = np.sqrt(np.mean(columna ** 2))
        rms_list.append(rms)
        potencia = np.sqrt((sum(columna)) ** 2)
        potencia_list.append(potencia)
        energia = (sum(columna)) ** 2
        energia_list.append(energia)
        mini = np.min(columna)
        minimo_list.append(mini)
        maxi = np.max(columna)
        maximo_list.append(maxi)
        rango = maxi - mini
        rango_list.append(rango)

        jerk = np.gradient(columna, tiempo)
        jerkl.append(jerk)
        jerkma = np.max(jerk)
        jerkmax.append(jerkma)
        jerkmi = np.min(jerk)
        jerkmin.append(jerkmi)
        jerkr = np.sqrt(np.mean(jerk ** 2))
        jerkrms.append(jerkr)
        jerkmed = np.mean(jerk)
        jerkmedia.append(jerkmed)

        # Crear y guardar gráfico
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(tiempo, jerk)
        ax.set_title(f"Jerk vs Tiempo {lab[y]}")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Jerk (m/s³)")
        ax.grid(True)

        jerk_graficos.append(fig)

        #plt.close(fig)  # Cierra cada figura inmediatamente

    # Crear tabla de características
    headers = ["Características", "Persona 1"]
    caracteristicas = ["RMS", "Tiempo de la Prueba", "Potencia", "Energía", "Valor Máximo", "Valor Mínimo",
                       "Rango Aceleraciones", "Jerk Máximo (m/s³)", "Jerk Mínimo (m/s³)", "Jerk Medio (m/s³)",
                       "Jerk RMS (m/s³)"]
    total_data = []
    for y in range(nc):
        data = [
            [caracteristicas[0], rms_list[y]],
            [caracteristicas[1], tiempot[y]],
            [caracteristicas[2], potencia_list[y]],
            [caracteristicas[3], energia_list[y]],
            [caracteristicas[4], maximo_list[y]],
            [caracteristicas[5], minimo_list[y]],
            [caracteristicas[6], rango_list[y]],
            [caracteristicas[7], jerkmax[y]],
            [caracteristicas[8], jerkmin[y]],
            [caracteristicas[9], jerkmedia[y]],
            [caracteristicas[10], jerkrms[y]]
        ]
        total_data.append(data)
        # Imprimir la tabla
    # print(f"Tabla {lab[y]}. Resultados por sujeto")
    # print(tabulate(data, headers=headers, tablefmt="fancy_grid"))
    plt.close('all')

    print("total_data: ", total_data)

    return total_data, jerk_graficos
