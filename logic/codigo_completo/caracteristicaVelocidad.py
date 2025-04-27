import numpy as np
from matplotlib import pyplot as plt
from tabulate import tabulate


def featuresvel(senial,datosfinal_total):
    # Inicializa listas para almacenar las características
    rms_list = []
    potencia_list = []
    energia_list = []
    minimo_list = []
    maximo_list = []
    rango_list = []
    tiempot = []

    # Asegúrate de que la señal sea un array de NumPy
    señalf = np.array(senial)

    # Verifica que la señal tenga al menos 2 dimensiones
    if señalf.ndim < 2:
        print("Error: La señal debe tener al menos 2 dimensiones.")
        return None
    lab = ['Acc_X', 'Acc_Y', 'Acc_Z']
    nc = señalf.shape[1]
    print(nc)  # Número de columnas en la señal
    for i in range(nc):
        columna = señalf[:, i]  # Selecciona la columna i
        # Cálculo de las características
        li = len(señalf[:, i]) / 100
        lo = len(señalf[:, i])
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
        lab = ['V.Angular_x', 'Ve.Angular_y', 'V.angular_z']
        headers = ["Características"] + [f"Persona {i + 1}" for i in range(len(datosfinal_total))]
        caracteristicas = ["RMS", "Tiempo de la Prueba", "Potencia", "Energía", "Valor Máximo", "Valor Mínimo",
                           "Rango Velocidades"]
        data = [
            [caracteristicas[0], rms_list[i]],
            [caracteristicas[1], tiempot[i]],
            [caracteristicas[2], potencia_list[i]],
            [caracteristicas[3], energia_list[i]],
            [caracteristicas[4], maximo_list[i]],
            [caracteristicas[5], minimo_list[i]],
            [caracteristicas[6], rango_list[i]],
        ]

        # Número de la tabla

        # Imprimir la tabla
        print(f"Tabla {lab[i]}. Resultados por sujeto\n")
        print(tabulate(data, headers=headers, tablefmt="fancy_grid"))