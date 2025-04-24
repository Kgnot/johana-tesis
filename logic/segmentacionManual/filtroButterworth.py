from scipy.signal import butter, filtfilt, freqz
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def filtroButterworth()-> []:
    datosfinal=[]
    # Ruta del archivo
    pelvis = "../../data/control/aposteriori/tug_1/60/MT_01200A8F-000-000_00B4578C.txt"
    piede='../../data/control/aposteriori/tug_1/60/MT_01200A8F-000-000_00B4578C.txt'
    pieiz='../../data/control/aposteriori/tug_1/60/MT_01200A8F-000-000_00B4578D.txt'


    # Lista de archivos CSV que contienen las señales
    archivos = ['pelvis', 'piede', 'pieiz']  # Cambia estos nombres por los nombres de tus archivos
    datosfinal_total = []  # Lista para almacenar los datos filtrados de todas las señales

    # Definir parámetros del filtro
    orden = 3  # Orden del filtro
    fc = 10  # Frecuencia de corte en Hz
    fs = 100  # Frecuencia de muestreo en Hz

    for datos in archivos:
        # Leer los datos
        data = pd.read_csv(pelvis, delim_whitespace=True, skiprows=12)
        Df = data[['Acc_X', 'Acc_Y', 'Acc_Z', 'VelInc_X', 'VelInc_Y', 'VelInc_Z']]
        df = Df.rename(columns={
            "Acc_X": "acc_x",
            "Acc_Y": "acc_y",
            "Acc_Z": "acc_z",
            "VelInc_X": "gyr_x",
            "VelInc_Y": "gyr_y",
            "VelInc_Z": "gyr_z",
        })

        señal_original = df.to_numpy()
        b, a = butter(orden, fc / (fs / 2), btype='low', analog=False)

        datosfinal = []  # Lista para almacenar los datos filtrados de la señal actual

        for k in range(6):
            señal_filtrada = filtfilt(b, a, señal_original[:, k])
            datosfinal.append(señal_filtrada)

        datosfinal = np.array(datosfinal).T
        datosfinal_total.append(datosfinal)  # Almacenar los datos filtrados de la señal actual


        # Graficar las señales
        plt.figure(figsize=(10, 10))
        for k in range(6):
            plt.subplot(6, 1, k + 1)  # Crear subgráficas para cada canal
            plt.plot(señal_original[:, k], label="Señal Original")
            plt.plot(datosfinal[:, k], label="Señal Filtrada")
            plt.title(f"Comparación de Señales (Canal {k + 1}) - {datos}")
            plt.xlabel("Tiempo")
            plt.ylabel("Amplitud")
            plt.legend()  # Agregar leyenda para diferenciar señales
            plt.grid()

        plt.tight_layout()  # Ajustar el layout para que no se superpongan
        plt.show()

    datosfinal1=np.squeeze(np.array(datosfinal_total))
    piernaiz=datosfinal1[0]
    piernade=datosfinal1[1]
    pelvisf=datosfinal1[2]

    return datosfinal_total