import numpy as np
import matplotlib.pyplot as plt
import io
from PIL import Image
from tabulate import tabulate


def featuresvel(senial, datosfinal_total):
    # Inicializa listas para almacenar las características
    rms_list = []
    potencia_list = []
    energia_list = []
    minimo_list = []
    maximo_list = []
    rango_list = []
    tiempot = []
    respuesta_graficos = []

    # Asegúrate de que la señal sea un array de NumPy
    senialf = np.array(senial)

    # Verifica que la señal tenga al menos 2 dimensiones
    if senialf.ndim < 2:
        print("Error: La señal debe tener al menos 2 dimensiones.")
        return None, None  # Retorna None si la señal no es válida

    lab = ['V.Angular_x', 'Ve.Angular_y', 'V.angular_z']
    nc = senialf.shape[1]
    print(nc)  # Número de columnas en la señal
    for i in range(nc):
        columna = senialf[:, i]  # Selecciona la columna i
        # Cálculo de las características
        li = len(senialf[:, i]) / 100
        lo = len(senialf[:, i])
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

        # Crear la figura para graficar la velocidad angular vs tiempo
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.plot(tiempo, columna)
        ax.set_title(f"Velocidad Angular vs Tiempo {lab[i]}")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Velocidad Angular (rad/s)")
        ax.grid(True)

        # Agregar la imagen a la lista de gráficos
        respuesta_graficos.append(fig)

        # Limpiar la figura después de usarla para evitar que se acumulen recursos
        #plt.close(fig)

    # Definir las características para la tabla
    caracteristicas = ["RMS", "Tiempo de la Prueba", "Potencia", "Energía", "Valor Máximo", "Valor Mínimo",
                       "Rango Velocidades"]

    # Crear los datos para la tabla
    data = []
    for i in range(nc):
        data.append([
            [caracteristicas[0], rms_list[i]],
            [caracteristicas[1], tiempot[i]],
            [caracteristicas[2], potencia_list[i]],
            [caracteristicas[3], energia_list[i]],
            [caracteristicas[4], maximo_list[i]],
            [caracteristicas[5], minimo_list[i]],
            [caracteristicas[6], rango_list[i]],
        ])

        # Imprimir la tabla
        print(f"Tabla {lab[i]}. Resultados por sujeto\n")
        print(tabulate(data[i], headers=["Características", f"Persona {i + 1}"], tablefmt="fancy_grid"))

    # Retornar las características y los gráficos guardados
    return data, respuesta_graficos
