import numpy as np
from matplotlib import pyplot as plt

from logic.estudio_seniales.caracteristica_aceleracion import featuresac
from logic.estudio_seniales.caracteristica_velocidad import featuresvel
from logic.estudio_seniales.extraccion_angulos import artan
from logic.utils.extraerSeñalesFiltradas import extraer_seniales_filtradas


"""
    segumul es quien nos otorga el análisis de señales deseado.
    Obtenemos si es Aceleración o Velocidad dependiendo de "med"
    Luego cuales son los datos a procesar
    Tiempo inicial y tiempo final
    El tipo de acción a obtener
"""
def segmul(med: str, datos_procesar: int, ti, tf, accion):
    DT, seniales, datosfinal_total = extraer_seniales_filtradas(datos_procesar) # Función ya testeada
    # Seleccionar señal según el tipo de medición
    if med == "Acc":
        senial = seniales['señalac']
    elif med == "Velocidad":
        senial = seniales['señalve']
    else:
        print(f"Tipo de medición '{med}' no reconocido. Use 'Acc' o 'Velocidad'.")
        return None

    senialr = np.array(senial)
    To = int(ti * 100)
    Te = int(tf * 100)
    Tt = Te - To
    # Validar rango de tiempo
    if To < 0 or Te > senialr[-1].shape[0] or To >= Te:
        raise Exception("Error: Los tiempos ingresados están fuera de rango o son inválidos.")
    # Aqui elegimos el -1 para evaluar
    segmento = senialr[-1][To:Te]
    # Visualizar resultados XYZ
    graficosXYZ = graficosXYZ_segmento(segmento, accion, med, ti, Tt)  # Aquí me agrega todas las graficas XYZ, y ya fué testeada
    # Analizar señal angulos
    angulos, graficos_angulos = artan(segmento)  # Devuelve: angulos,respuesta_graficos . angulos es un pd.Dataframe
    # Extraer características según tipo de medición
    data, jerk_graficos = None, None
    if med == "Acc":
        data, jerk_graficos = featuresac(segmento)  # Función ya probada
    elif med == "Velocidad":
        data, jerk_graficos = featuresvel(segmento, datosfinal_total)  # Función ya probada

    return {
        "gráficos": graficosXYZ,
        "graficos_Jerk": jerk_graficos,
        "angulos_graficos": graficos_angulos,
        "angulos": angulos,
        "características": data,
    }


def graficosXYZ_segmento(segmento, accion, tipo_medicion, tiempo_inicial, duracion_total):
    graficos_XYZ = []

    # Cálculo de ticks y etiquetas
    new_xticks = np.linspace(0, duracion_total, 26)
    new_xticklabels = [f"{(i / 100) + tiempo_inicial:.2f}" for i in new_xticks]

    # Crear un gráfico individual para cada eje
    for i, eje in enumerate(['X', 'Y', 'Z']):
        fig, ax = plt.subplots(figsize=(8, 4))  # Tamaño manejable
        ax.plot(segmento[:, i])
        ax.set_title(f"{accion} {tipo_medicion} {eje}")
        ax.set_xticks(new_xticks)
        ax.set_xticklabels(new_xticklabels, rotation=45)
        ax.set_xlabel('Tiempo (s)')
        ax.set_ylabel('Amplitud')
        ax.grid(True)

        graficos_XYZ.append(fig)

    return graficos_XYZ
