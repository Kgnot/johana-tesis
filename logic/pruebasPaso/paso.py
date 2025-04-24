import pandas as pd
import numpy as np
# def analizarGait(data_list, ruta, nummaxcost):
piede='../../data/control/aposteriori/tug_1/60/MT_01200A8F-000-000_00B4578C.txt'
pieiz='../../data/control/aposteriori/tug_1/60/MT_01200A8F-000-000_00B4578D.txt'

piede = pd.read_csv(piede, delim_whitespace=True, skiprows=12)
pieiz = pd.read_csv(pieiz, delim_whitespace=True, skiprows=12)

data = pd.concat([pieiz[['Acc_X','Acc_Y','Acc_Z']], piede[['Acc_X','Acc_Y','Acc_Z']]], axis=1)
 # Assign values to the DataFrame


# Definir la acción
señal=data.to_numpy()
# Función para extraer segmentos de la señal

def extraer_segmento(señal):
  segmentos = []
  for i in range(0,2):
    Ti = float(input(f"Ingresa el tiempo inicial deseado para segmento{i+1}: "))
    Tf = float(input(f"Ingresa el tiempo final deseado para {i+1}: "))

    # Convertir los tiempos a enteros
    To = int(Ti * 100)
    Te = int(Tf * 100)
    Tt=Te-To

    if To < 0 or Te > señal.shape[0] or To >= Te:
        print("Error: Los tiempos ingresados están fuera de rango o son inválidos.")
        return
    segmento = señal[To:Te, :]  # Extraer todas las columnas
    segmentos.append(segmento)
  return segmentos

datos=extraer_segmento(señal)
datos=np.vstack((datos[0],datos[1]))
datac=pd.DataFrame(datos)

print(datac)