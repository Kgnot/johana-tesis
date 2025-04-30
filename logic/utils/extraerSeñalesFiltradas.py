import numpy as np

from logic.estudio_seniales.filtroButterworth import filtroButterworth_DatosFinalTotal

def procesar_datos(datos_array):
    DT = np.array(datos_array)
    # Separar aceleraciones y velocidades
    da = DT[:, 0:3]
    dv = DT[:, 3:6]
    da = (da - da.min(axis=0)) / (da.max(axis=0) - da.min(axis=0))
    DT = np.hstack((da, dv))
    # Crear diccionario de señales
    seniales = {
        'señalac': [DT[:, 0:3]],  # Aceleraciones
        'señalve': [DT[:, 3:6]],  # Velocidades
        'DT': DT  # Datos completos
    }

    return DT, seniales

def extraer_seniales_filtradas(datosProcesar: int):
    datosfinal_total = filtroButterworth_DatosFinalTotal(datosProcesar)
    ultimoDatoFinal_total = datosfinal_total[-1]
    # Escojemos el último
    DT, seniales = procesar_datos(ultimoDatoFinal_total)
    return DT, seniales, datosfinal_total
