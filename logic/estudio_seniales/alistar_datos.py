import os
import pandas as pd

"""
    Obtenemos la ruta
"""


def obtener_ruta() -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(script_dir, "..", "..", "data", "Tdatos"))


"""
    Obtenemos la carpeta
"""


def obtener_carpeta(dat: int) -> str:
    carpeta_datos = obtener_ruta()
    opciones = {
        1: ("apriori", "Control"),
        2: ("apriori", "Experimental"),
        3: ("POSTERIORI", "Control"),
        4: ("POSTERIORI", "Experimental"),
    }

    if dat not in opciones:
        raise Exception("Dat no existe")
    return os.path.join(carpeta_datos,
                        *opciones[dat])  # El * desempaqueta y pasa los valores de la lista como argumentos
    # os.path.join(carpeta2_datos, "apriori", "Control") # pe


"""
    Leemos el archivo csv con las columnas
"""


def leer_csv(archivo_csv: str) -> pd.DataFrame:
    columnas = ['Acc_X', 'Acc_Y', 'Acc_Z', 'VelInc_X', 'VelInc_Y', 'VelInc_Z']
    skip_header: int = 12  # El header es de 12 filas, lo cual saltaremos
    df = pd.read_csv(archivo_csv, delim_whitespace=True, skiprows=skip_header)
    return df[columnas]


""" 
    Normalizamos por cada columna
"""


def normalizar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    return (df - df.min()) / (df.max() - df.min())


"""
    Procesamos los archivos [flujo completo] dados por dat y 
    retornamos las señales normalizadas
"""

# PRINCIPAL
def procesar_archivos(dat: int):
    carpeta = obtener_carpeta(dat)
    senales = []
    for archivo in carpeta:
        archivo_csv = os.path.join(carpeta, archivo)
        df = leer_csv(archivo_csv)
        df_normalizado = normalizar_dataframe(df)
        senales.append(df_normalizado)

    return senales
