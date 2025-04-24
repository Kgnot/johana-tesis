import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fftpack import fft

# Ruta del archivo
pelvis = "../../data/control/aposteriori/tug_1/60/MT_01200A8F-000-000_00B4578C.txt"

# Leer el archivo y seleccionar columnas relevantes
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

# Separar aceleraciones y velocidades
aceleraciones = ["acc_x", "acc_y", "acc_z"]
velocidades = ["gyr_x", "gyr_y", "gyr_z"]

# Frecuencia de muestreo
fs = 100

fig, axes = plt.subplots(2, 1, figsize=(10, 8))

for columna in aceleraciones:
    señal = df[columna].values
    N = len(señal)

    fft_result = fft(señal)
    fft_magnitude = np.abs(fft_result)
    frequencies = np.fft.fftfreq(N, 1/fs)
    axes[0].plot(frequencies[:N//2], fft_magnitude[:N//2], label=columna)

axes[0].set_title("Espectro de Frecuencia - Aceleraciones (Filtradas)")
axes[0].set_xlabel("Frecuencia (Hz)")
axes[0].set_ylabel("Amplitud")
axes[0].legend()
axes[0].grid()
axes[0].set_xlim(0, fs/2)
axes[0].set_ylim(0, 1500)

for columna in velocidades:
    señal = df[columna].values
    N = len(señal)

    fft_result = fft(señal)
    fft_magnitude = np.abs(fft_result)
    frequencies = np.fft.fftfreq(N, 1/fs)
    axes[1].plot(frequencies[:N//2], fft_magnitude[:N//2], label=columna)

axes[1].set_title("Espectro de Frecuencia - Velocidades Angulares (Filtradas)")
axes[1].set_xlabel("Frecuencia (Hz)")
axes[1].set_ylabel("Amplitud")
axes[1].legend()
axes[1].grid()
axes[1].set_xlim(0, fs/2)
axes[1].set_ylim(0, 14)

#plt.show()

plt.savefig("grafica.png", dpi=300, bbox_inches="tight")
