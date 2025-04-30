from scipy.signal import butter, filtfilt
import numpy as np
import matplotlib.pyplot as plt
from logic.estudio_seniales.alistarDatos import datosProcesar


def filtroButterworth_DatosFinalTotal(datProc: int) -> list:
    # Llamamos a senialesgenerales:
    senalesgenerales = datosProcesar(datProc)
    #print("Señales generales:",senalesgenerales)
    # Lista para almacenar los datos filtrados de todas las señales
    datosfinal_total = []

    # Parámetros del filtro
    orden = 4  # Orden del filtro
    fc = 10  # Frecuencia de corte en Hz
    fs = 100  # Frecuencia de muestreo en Hz

    # Nombres de las variables
    # Listado = ['Aceleración X', 'Aceleración Y', 'Aceleración Z', 'V. Angular X', 'V. Angular Y', 'V. Angular Z']

    # Filtro Butterworth y filtrado de señales
    for l in range(len(senalesgenerales)):
        # Leer los datos
        senial_original = np.array(senalesgenerales[l])
        b, a = butter(orden, fc / (fs / 2), btype='low', analog=False)

        datosfinal = []  # Para almacenar los datos filtrados de la señal actual

        for m in range(6):  # Cada columna
            senial_filtrada = filtfilt(b, a, senial_original[:, m])
            datosfinal.append(senial_filtrada)

        datosfinal = np.array(datosfinal).T  # Transponemos para que quede igual que original
        datosfinal_total.append(datosfinal)

    return datosfinal_total
