from scipy.signal import butter, filtfilt
import numpy as np
import matplotlib.pyplot as plt
from logic.codigo_completo.alistarDatos import datosProcesar


def filtroButterworth_DatosFinalTotal(datTatosProcesar: int) -> list:
    # Llamamos a senalesgenerales:
    senalesgenerales = datosProcesar(datTatosProcesar)

    # Lista para almacenar los datos filtrados de todas las señales
    datosfinal_total = []

    # Parámetros del filtro
    orden = 4  # Orden del filtro
    fc = 10  # Frecuencia de corte en Hz
    fs = 100  # Frecuencia de muestreo en Hz

    # Nombres de las variables
    Listado = ['Aceleración X', 'Aceleración Y', 'Aceleración Z', 'V. Angular X', 'V. Angular Y', 'V. Angular Z']

    # Filtro Butterworth y filtrado de señales
    for l in range(len(senalesgenerales)):
        # Leer los datos
        señal_original = np.array(senalesgenerales[l])
        b, a = butter(orden, fc / (fs / 2), btype='low', analog=False)

        datosfinal = []  # Para almacenar los datos filtrados de la señal actual

        for m in range(6):  # Cada columna
            señal_filtrada = filtfilt(b, a, señal_original[:, m])
            datosfinal.append(señal_filtrada)

        datosfinal = np.array(datosfinal).T  # Transponemos para que quede igual que original
        datosfinal_total.append(datosfinal)

        # Graficamos la señal original y la señal filtrada de la primer componente
        plt.figure(figsize=(10, 5))
        plt.plot(señal_original[:, 0], label="Señal Original")
        plt.plot(datosfinal[:, 0], label="Señal Filtrada", linestyle='--')
        plt.title(f"Comparación de Señales {Listado[0]} (Señal {l + 1})")
        plt.xlabel("Tiempo (muestras)")
        plt.ylabel("Amplitud (normalizada)")
        plt.legend()
        plt.grid(True)
        plt.show()

    return datosfinal_total
