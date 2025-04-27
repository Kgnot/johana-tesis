from gaitmap.preprocessing.sensor_alignment import PcaAlignment
import pandas as pd
import numpy as np
from gaitmap.preprocessing import align_dataset_to_gravity
import matplotlib.pyplot as plt
import pywt
from sklearn.decomposition import FastICA

# Define the path to your text file
file_path ='../../data/control/aposteriori/tug_1/60/MT_01200A8F-000-000_00B457A5.txt'
# Read the first 6 lines separately
with open(file_path, 'r') as file:
    first_six_lines = [next(file).strip().split() for _ in range(28)]
data= pd.read_csv(file_path, delim_whitespace=True, skiprows=12)
DT=data.squeeze()
Df=DT[['Acc_X', 'Acc_Y', 'Acc_Z', 'VelInc_X','VelInc_Y','VelInc_Z']]
sensor = "right_sensor"

df = Df.rename(columns={
    "Acc_X": "acc_x",
    "Acc_Y": "acc_y",
    "Acc_Z": "acc_z",
    "VelInc_X": "gyr_x",
    "VelInc_Y": "gyr_y",
    "VelInc_Z": "gyr_z",
})


gravity_aligned_data = align_dataset_to_gravity(df, sampling_rate_hz=100, window_length_s=0.1, static_signal_th=15)

pca_alignment = PcaAlignment(target_axis="y", pca_plane_axis=("gyr_x", "gyr_y"))
pca_alignment = pca_alignment.align(gravity_aligned_data)
Final = pca_alignment.aligned_data_


# wavelet = 'coif17'
wavelet = 'db38'

# Listas de señales y nombres
signals = ['acc_x', 'acc_y', 'acc_z']
sigvel = ['gyr_x', 'gyr_y', 'gyr_z']
icasac = []
icasvel = []

# Iterar sobre cada señal de aceleración
for signal in signals:
    # Descomposición Wavelet
    coeffsac = pywt.wavedec(Final[signal], wavelet, level=6)
    (_, Da6, Da5, Da4, Da3, Da2, Da1) = coeffsac

    # Verificar las longitudes de los coeficientes y obtener la mínima
    lengthsa = [len(Da6), len(Da5), len(Da4), len(Da3), len(Da2), len(Da1)]
    min_length = min(lengthsa)

    # Recortar todos los coeficientes a la longitud mínima
    Da6_trimmed = Da6[:min_length]
    Da5_trimmed = Da5[:min_length]
    Da4_trimmed = Da4[:min_length]
    Da3_trimmed = Da3[:min_length]
    Da2_trimmed = Da2[:min_length]
    Da1_trimmed = Da1[:min_length]

    # Preparar los coeficientes de detalle para ICA
    coeffs_trimmedac = np.vstack((Da6_trimmed, Da5_trimmed, Da4_trimmed, Da3_trimmed, Da2_trimmed, Da1_trimmed)).T

    # Aplicar ICA
    icaa = FastICA(n_components=6)
    ica_transformedac = icaa.fit_transform(coeffs_trimmedac)

    # Guardar el resultado
    icasac.append(ica_transformedac)

# Iterar sobre cada señal de velocidad
for signal in sigvel:
    # Descomposición Wavelet
    coeffs = pywt.wavedec(Final[signal], wavelet, level=6)
    (_, D6, D5, D4, D3, D2, D1) = coeffs

    # Verificar las longitudes de los coeficientes y obtener la mínima
    lengths = [len(D6), len(D5), len(D4), len(D3)]
    min_lengthv = min(lengths)

    # Recortar todos los coeficientes a la longitud mínima
    D6_trimmed = D6[:min_lengthv]
    D5_trimmed = D5[:min_lengthv]
    D4_trimmed = D4[:min_lengthv]
    D3_trimmed = D3[:min_lengthv]


    # Preparar los coeficientes de detalle para ICA
    coeffs_trimmed = np.vstack((D6_trimmed, D5_trimmed, D4_trimmed, D3_trimmed)).T

    # Aplicar ICA
    icav = FastICA(n_components=4)
    ica_transformed = icav.fit_transform(coeffs_trimmed)

    # Guardar el resultado
    icasvel.append(ica_transformed)



titlesac = ['ICA - Acc_X', 'ICA - Acc_Y', 'ICA - Acc_Z']
titlesvel= ['ICA - Vel_X', 'ICA - Vel_Y', 'ICA - Vel_Z']


for i, ica_result in enumerate(icasac):
    plt.figure(figsize=(12, 8))
    for j in range(ica_result.shape[1]):
        plt.subplot(6, 1, j + 1)
        plt.plot(ica_result[:, j])
        plt.title(f'{titlesac[i]} - Componente {j + 1}')
        plt.xlabel('Tiempo')
        plt.ylabel('Amplitud')
    plt.tight_layout()
    plt.show()

for i, ica_result in enumerate(icasvel):
    plt.figure(figsize=(12, 8))
    for j in range(ica_result.shape[1]):
        plt.subplot(6, 1, j + 1)
        plt.plot(ica_result[:, j])
        plt.title(f'{titlesvel[i]} - Componente {j + 1}')
        plt.xlabel('Tiempo')
        plt.ylabel('Amplitud')
    plt.tight_layout()
    plt.show()


transformac=np.array(icasac)
transformac=np.hstack((transformac[0],transformac[1],transformac[2]))
transformve=np.array(icasvel)
transformve=np.hstack((transformve[0],transformve[1],transformve[2]))
