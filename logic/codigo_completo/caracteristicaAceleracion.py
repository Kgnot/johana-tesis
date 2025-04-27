import numpy as np
from matplotlib import pyplot as plt
from tabulate import tabulate


def featuresac(señal):
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

    # Asegúrate de que la señal sea un array de NumPy
    señalf = np.array(señal)

    lab = ['Acc_X', 'Acc_Y', 'Acc_Z']
    nc = señalf.shape[1]
    print(nc)
    for y in range(nc):
        columna = señalf[:, y]  # Selecciona la columna i
        # Cálculo de las características
        li = len(señalf[:, y]) / 100
        lo = len(señalf[:, y])
        tiempot.append(li)
        tm = np.random.uniform(0, li, lo)
        tiempo = np.sort(tm)
        rms = np.sqrt(np.mean(columna ** 2))  # Cálculo del RMS
        rms_list.append(rms)
        potencia = np.sqrt((sum(columna)) ** 2)  # Media
        potencia_list.append(potencia)
        energia = (sum(columna)) ** 2  # Desviación estándar
        energia_list.append(energia)
        mini = np.min(columna)  # Mínimo
        minimo_list.append(mini)
        maxi = np.max(columna)  # Máximo
        maximo_list.append(maxi)
        rango = maxi - mini  # Rango
        rango_list.append(rango)
        jerk = np.gradient(señalf[:, y], tiempo)
        jerkl.append(jerk)
        jerkma = np.max(jerk)
        jerkmax.append(jerkma)
        jerkmi = np.min(jerk)
        jerkmin.append(jerkmi)
        jerkr = np.sqrt(np.mean(jerk ** 2))
        jerkrms.append(jerkr)
        jerkmed = np.mean(jerk)
        jerkmedia.append(jerkmed)
        plt.plot(tiempo, jerk)
        plt.title(f"Jerk vs Tiempo {lab[y]}")
        plt.xlabel("Tiempo (s)")
        plt.ylabel("Jerk (m/s³)")
        plt.grid(True)
        plt.show()
        lab = ['Acc_x', 'Acc_y', 'Acc_z']
        # headers = ["Características"] + [f"Persona {i+1}" for i in range(len(datosfinal_total))]
        headers = ["Características", "Persona 1"]
        caracteristicas = ["RMS", "Tiempo de la Prueba", "Potencia", "Energía", "Valor Máximo", "Valor Mínimo",
                           "Rango Aceleraciones", "Jerk Máximo (m/s³)", "Jerk Mínimo (m/s³)", "Jerk Medio (m/s³)",
                           "Jerk RMS (m/s³)"]
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

        # Número de la tabla

        # Imprimir la tabla
        print(f"Tabla {lab[y]}. Resultados por sujeto")
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))