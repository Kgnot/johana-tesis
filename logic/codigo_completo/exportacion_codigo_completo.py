import numpy as np
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
    # Normalizar aceleraciones
    da = (da - da.min(axis=0)) / (da.max(axis=0) - da.min(axis=0))
    # Combinar datos normalizados
    DT = np.hstack((da, dv))

    # Crear diccionario de señales
    seniales = {
        'señalac': [DT[:, 0:3]],  # Aceleraciones
        'señalve': [DT[:, 3:6]],  # Velocidades
        'señalax': [DT[:, 0]],  # Acc_X
        'señalay': [DT[:, 1]],  # Acc_Y
        'señalaz': [DT[:, 2]],  # Acc_Z
        'señalvx': [DT[:, 3]],  # Vel_x
        'señalvy': [DT[:, 4]],  # Vel_Y
        'señalvz': [DT[:, 5]],  # Vel_Z
        'DT': DT  # Datos completos
    }

    return DT, seniales

def extraclaims(datosProcesar:int):
    datosfinal_total = filtroButterworth_DatosFinalTotal(datosProcesar)
    resultados = []
    for datos in datosfinal_total:
        DT, seniales = procesar_datos(datos)
        resultados.append((DT, seniales))

    return resultados , datosfinal_total

#Este va por segulac y segmulvel
def segmul(med:str, datosProcesar:int):
    ###
    resultados,datosfinal_total = extraclaims(datosProcesar)
    if not resultados:
        print("No se encontraron datos para procesar")
        return
    seg1 = ['Pararse',
            'Primer Giro',
            'Giro para sentarse',
            'Sentarse']
    # Con cada conjunto de datos que procesamos
    for DT, seniales in resultados:
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
            # Para cada acción a segmentar
            for i, accion in enumerate(seg1):
                # input de los tiempos:
                Ti = float(input(f"Ingresa el tiempo inicial deseado para {accion}: "))
                Tf = float(input(f"Ingresa el tiempo final deseado para {accion}: "))

                # Convertir a índices
                To = int(Ti * 100)
                Te = int(Tf * 100)
                Tt = Te - To

                # Validar rango de tiempo
                if To < 0 or Te > senialr[k].shape[0] or To >= Te: # Este es uno de los cambios que hizo, analizar el cambio: | señalr.shape[1] por senialr[k].shape[0]
                    '''
                    Dijo:
                    Validación de tiempo mejorada:
                        Cambié senialr.shape[1] a senialr[k].shape[0] porque estamos comprobando el límite de tiempo (que es la dimensión 0 de la señal), no el número de canales.

                    '''

                    print("Error: Los tiempos ingresados están fuera de rango o son inválidos.")
                    continue

                # Extraer segmento de señal Aqui hay cambio esto es segun la IA pero no se, toca evaluar
                #Antes:
                #senial = senialr[k]
                #senial = senial[To:Te]
                segmento = senialr[k][To:Te]

                # Visualizar resultados
                visualizar_segmento(segmento, accion, med, Ti, Tt)

                # Analizar señal
                artan(segmento)
                print("\n")

                # Extraer características según tipo de medición
                caracteristicas = None
                if med == "Acc":
                    caracteristicas = featuresac(segmento)
                elif med == "Velocidad":
                    caracteristicas = featuresvel(segmento,datosfinal_total)  # Usando featuresvel para velocidades

                if caracteristicas:
                    print("Características de la señal:")
                    for key, value in caracteristicas.items():
                        print(f"{key}: {value}")

def visualizar_segmento(segmento, accion, tipo_medicion, tiempo_inicial, duracion_total):
    fig, axs = plt.subplots(3, 1, figsize=(20, 10))

    # Crear etiquetas de tiempo adecuadas
    new_xticks = np.linspace(0, duracion_total, 26)
    new_xticklabels = [f"{(i / 100) + tiempo_inicial:.2f}" for i in new_xticks]

    # Configurar gráficos para cada eje
    for i in range(3):
        axs[i].plot(segmento[:, i])
        axs[i].set_title(f"{accion} {tipo_medicion} {['X', 'Y', 'Z'][i]}")
        axs[i].set_xticks(new_xticks, new_xticklabels)
        axs[i].set_xlabel('Tiempo')
        axs[i].set_ylabel('Amplitud')
        axs[i].grid()

    plt.subplots_adjust(hspace=0.5)
    plt.show()

segmul("Acc", 1)
