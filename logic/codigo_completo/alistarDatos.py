import os

import pandas as pd

## defino que necesito un int y que devuelve un str, se puede quitar
import os
import pandas as pd


def datosProcesar(dat: int) -> list:
    # Variables que usaremos en el filtro Butterworth
    senalesgenerales = []
    senalespasos = []

    # Carpeta base
    carpeta2_datos: str = "../../data/Tdatos"

    # Corrigiendo los if
    if dat == 1:
        carpeta2_datos = os.path.join(carpeta2_datos, "apriori", "Control")
    elif dat == 2:
        carpeta2_datos = os.path.join(carpeta2_datos, "apriori", "Experimental")
    elif dat == 3:
        carpeta2_datos = os.path.join(carpeta2_datos, "POSTERIORI", "Control")
    elif dat == 4:
        carpeta2_datos = os.path.join(carpeta2_datos, "POSTERIORI", "Experimental")
    else:
        raise ValueError("El valor de 'dat' debe ser 1, 2, 3 o 4.")

    # Luego de los if:
    data = os.listdir(carpeta2_datos)
    for archivo in data:
        archivo_csv = os.path.join(carpeta2_datos, archivo)

        # Verificamos que sea un archivo y termine en .csv
        if os.path.isfile(archivo_csv) and archivo_csv.endswith('.csv'):
            df = pd.read_csv(archivo_csv, delim_whitespace=True, skiprows=12)
            columnas = ['Acc_X', 'Acc_Y', 'Acc_Z', 'VelInc_X', 'VelInc_Y', 'VelInc_Z']
            df_selected = df[columnas]
            # Normalización Min-Max por columna
            df_normalizado = (df_selected - df_selected.min()) / (df_selected.max() - df_selected.min())
            señal = df_normalizado.values
            senalesgenerales.append(señal)

    return senalesgenerales
