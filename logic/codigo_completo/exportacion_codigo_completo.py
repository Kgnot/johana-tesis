import io

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

from logic.codigo_completo.caracteristicaAceleracion import featuresac
from logic.codigo_completo.caracteristicaVelocidad import featuresvel
from logic.codigo_completo.extraccionAngulos import artan
from logic.codigo_completo.filtroButterworth import filtroButterworth_DatosFinalTotal


def procesar_datos(datos_array):
    DT = np.array(datos_array)
    # Separar aceleraciones y velocidades
    da = DT[:, 0:3]
    dv = DT[:, 3:6]
    da = (da - da.min(axis=0)) / (da.max(axis=0) - da.min(axis=0))
    DT = np.hstack((da, dv))
    # DT = np.array(DT) # Esto sobra son lo mismo xd
    # Crear diccionario de señales
    seniales = {
        'señalac': [DT[:, 0:3]],  # Aceleraciones
        'señalve': [DT[:, 3:6]],  # Velocidades
        # 'señalax': [DT[:, 0]],  # Acc_X
        # 'señalay': [DT[:, 1]],  # Acc_Y
        # 'señalaz': [DT[:, 2]],  # Acc_Z
        # 'señalvx': [DT[:, 3]],  # Vel_x
        # 'señalvy': [DT[:, 4]],  # Vel_Y
        # 'señalvz': [DT[:, 5]],  # Vel_Z
        'DT': DT  # Datos completos
    }

    return DT, seniales


def extraclaims(datosProcesar: int):
    datosfinal_total = filtroButterworth_DatosFinalTotal(datosProcesar)
    resultados = []
    ultimoDatoFinal_total = datosfinal_total[-1]
    DT = None
    # for datos in datosfinal_total:
    #     DT, seniales = procesar_datos(datos)
    #     # resultados.append((DT, seniales))
    #     resultados.append({
    #         'DT_procesado': DT,
    #         'seniales': seniales
    #     })
    # Escojemos el último
    DT,seniales = procesar_datos(ultimoDatoFinal_total)
    return DT,seniales, datosfinal_total


# Este va por segulac y segmulvel
def segmul(med: str, datosProcesar: int, Ti, Tf, accion):
    print(f"En segmul: datosProcesar: {med} \n {datosProcesar} \n {accion} ")
    datos_segmul = {}  ## Esto sseran todas las graficas y datos de retorno qu eharemos

    ###
    DT,seniales, datosfinal_total = extraclaims(datosProcesar)

    # Seleccionar señal según el tipo de medición
    if med == "Acc":
        senial = seniales['señalac']
    elif med == "Velocidad":
        senial = seniales['señalve']
    else:
        print(f"Tipo de medición '{med}' no reconocido. Use 'Acc' o 'Velocidad'.")
        return

    senialr = np.array(senial)

    # Para cada señal
    for k in range(len(senialr)):
        To = int(Ti * 100)
        Te = int(Tf * 100)
        Tt = Te - To
        # Validar rango de tiempo
        if To < 0 or Te > senialr[k].shape[
            0] or To >= Te:  # Este es uno de los cambios que hizo, analizar el cambio: | señalr.shape[1] por senialr[k].shape[0]
            '''
            Dijo:
            Validación de tiempo mejorada:
                Cambié senialr.shape[1] a senialr[k].shape[0] porque estamos comprobando el límite de tiempo (que es la dimensión 0 de la señal), no el número de canales.

            '''
            print("Error: Los tiempos ingresados están fuera de rango o son inválidos.")
            continue

        # Extraer segmento de señal Aqui hay cambio esto es segun la IA pero no se, toca evaluar
        # Antes:
        segmento = senialr[k][To:Te]

        # Visualizar resultados XYZ
        graficosXYZ = graficosXYZ_segmento(segmento, accion, med, Ti, Tt)  # Aqui me agrega todas las graficas XYZ
        # Analizar señal angulos
        angulos, graficos_angulos = artan(
            segmento)  # Devuelve: angulos,respuesta_graficos . angulos es un pd.Dataframe
        print("\n")
        # Extraer características según tipo de medición
        data, jerk_graficos = None, None
        if med == "Acc":
            data, jerk_graficos = featuresac(segmento)  # Esta guardando Los graficos y la tabla
        elif med == "Velocidad":
            data, jerk_graficos = featuresvel(segmento,
                                              datosfinal_total)  # Me genera lo mismo, graficos y una tabla,

        datos_segmul = {
            "acción": accion,
            "gráficos": graficosXYZ,
            "angulos": angulos,
            "angulos_graficos": graficos_angulos,
            "características": data,
            "graficos_Jerk": jerk_graficos
        }
    return datos_segmul


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


#segmul("Acc", 1, 3, 5, "Pararse")
