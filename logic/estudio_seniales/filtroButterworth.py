from scipy.signal import butter, filtfilt
import numpy as np
from logic.estudio_seniales.alistar_datos import procesar_archivos


def filtroButterworth_DatosFinalTotal(datos_procesar: int) -> list:
    # Llamamos a senialesgenerales:
    senalesgenerales = procesar_archivos(datos_procesar)
    # Lista para almacenar los datos filtrados de todas las señales
    datosfinal_total = []

    # Parámetros del filtro
    orden = 4  # Orden del filtro
    fc = 10  # Frecuencia de corte en Hz
    fs = 100  # Frecuencia de muestreo en Hz

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
