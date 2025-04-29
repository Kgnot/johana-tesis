import os

import numpy as np
import pywt
from matplotlib import pyplot as plt
from sklearn.decomposition import FastICA


def wavelet():
    señalw = señalwa
    columns = ['acc_x', 'acc_y', 'acc_z', 'gyr_x', 'gyr_y', 'gyr_z']
    col_idx = {name: i for i, name in enumerate(columns)}

    wavelet = 'db38'
    signals = ['acc_x', 'acc_y', 'acc_z']
    sigvel = ['gyr_x', 'gyr_y', 'gyr_z']

    icasac = []
    icasvel = []

    # Procesamiento de aceleración
    for signal in signals:
        signal_data = señalw[:, col_idx[signal]]
        coeffsac = pywt.wavedec(signal_data, wavelet, level=6)
        (_, Da6, Da5, Da4, Da3, Da2, Da1) = coeffsac

        lengthsa = [len(Da6), len(Da5), len(Da4), len(Da3), len(Da2), len(Da1)]
        min_length = min(lengthsa)

        coeffs_trimmedac = np.vstack([
            Da6[:min_length],
            Da5[:min_length],
            Da4[:min_length],
            Da3[:min_length],
            Da2[:min_length],
            Da1[:min_length]
        ]).T

        icaa = FastICA(n_components=6)
        ica_transformedac = icaa.fit_transform(coeffs_trimmedac)
        icasac.append(ica_transformedac)

    # Procesamiento de velocidad angular
    for signal in sigvel:
        signal_data = señalw[:, col_idx[signal]]
        coeffs = pywt.wavedec(signal_data, wavelet, level=6)
        (_, D6, D5, D4, D3, D2, D1) = coeffs

        lengths = [len(D6), len(D5), len(D4), len(D3), len(D2), len(D1)]
        min_lengthv = min(lengths)

        coeffs_trimmed = np.vstack([
            D6[:min_lengthv],
            D5[:min_lengthv],
            D4[:min_lengthv],
            D3[:min_lengthv],
            D2[:min_lengthv],
            D1[:min_lengthv]
        ]).T

        icav = FastICA(n_components=6)
        ica_transformed = icav.fit_transform(coeffs_trimmed)
        icasvel.append(ica_transformed)

    # Graficar resultados ICA
    titlesac = ['ICA - Acc_X', 'ICA - Acc_Y', 'ICA - Acc_Z']
    titlesvel = ['ICA - Vel_X', 'ICA - Vel_Y', 'ICA - Vel_Z']

    for i, ica_result in enumerate(icasac):
        plt.figure(figsize=(12, 8))
        for j in range(ica_result.shape[1]):
            plt.subplot(6, 1, j + 1)
            plt.plot(ica_result[:, j])
            plt.title(f'{titlesac[i]} - Componente {j + 1}')
            plt.xlabel('Tiempo')
            plt.ylabel('Amplitud')
        plt.tight_layout()
        filename = f"{titlesac[i].replace(' ', '_')}_ICA.png"
        filepath = os.path.join(carpetafinal, filename)
        plt.savefig(filepath)

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
        # Guardar la figura como archivo PNG en Drive
        filename = f"{titlesvel[i].replace(' ', '_')}_ICA.png"
        filepath = os.path.join(carpetafinal, filename)
        plt.savefig(filepath)
        plt.show()

    # Transformaciones combinadas
    transformac = np.hstack([icasac[0], icasac[1], icasac[2]])
    transformve = np.hstack([icasvel[0], icasvel[1], icasvel[2]])

    # Reconstrucción
    reconstructed_signals_ac = []
    reconstructed_signals_vel = []

    def resize_coeffs(original_coeffs, transformed_coeffs):
        resized_coeffs = []
        for orig, trans in zip(original_coeffs, transformed_coeffs.T):
            if len(orig) != len(trans):
                trans = np.interp(np.linspace(0, 1, len(orig)), np.linspace(0, 1, len(trans)), trans)
            resized_coeffs.append(trans)
        return resized_coeffs

    # Reconstrucción aceleración
    for i, ica_result in enumerate(icasac):
        signal_data = señalw[:, col_idx[signals[i]]]
        coeffsac = pywt.wavedec(signal_data, wavelet, level=6)
        approx_coeff = coeffsac[0]
        transformed_coeffs = resize_coeffs(coeffsac[1:], ica_result)
        final_coeffs = [approx_coeff] + transformed_coeffs
        reconstructed_signal1 = pywt.waverec(final_coeffs, wavelet)
        long = 27
        coefi = np.ones(long)
        b = coefi / long
        ace = np.array(reconstructed_signal1)
        reconstructed_signal = np.convolve(ace, b)
        reconstructed_signals_ac.append(reconstructed_signal)

    # Reconstrucción velocidad
    for i, ica_result in enumerate(icasvel):
        signal_data = señalw[:, col_idx[sigvel[i]]]
        coeffs = pywt.wavedec(signal_data, wavelet, level=6)
        approx_coeff = coeffs[0]
        transformed_coeffs = resize_coeffs(coeffs[1:], ica_result)
        final_coeffs = [approx_coeff] + transformed_coeffs
        reconstructed_signal1 = pywt.waverec(final_coeffs, wavelet)
        long = 27
        coefi = np.ones(long)
        b = coefi / long
        vel = np.array(reconstructed_signal1)
        reconstructed_signal = np.convolve(vel, b)
        reconstructed_signals_vel.append(reconstructed_signal)

    # Graficar señales reconstruidas
    titlesac = ['Reconstrucción Acc_X', 'Reconstrucción Acc_Y', 'Reconstrucción Acc_Z']
    titlesvel = ['Reconstrucción Vel_X', 'Reconstrucción Vel_Y', 'Reconstrucción Vel_Z']

    for i, rec_signal in enumerate(reconstructed_signals_ac):
        plt.figure(figsize=(12, 4))
        plt.plot(rec_signal, label=titlesac[i])
        plt.title(titlesac[i])
        plt.xlabel("Tiempo")
        plt.ylabel("Amplitud")
        plt.legend()
        filename = f"{titlesac[i].replace(' ', '_')}_Reconstruida.png"
        filepath = os.path.join(carpetafinal, filename)
        plt.savefig(filepath)
        plt.show()

    for i, rec_signal in enumerate(reconstructed_signals_vel):
        plt.figure(figsize=(12, 4))
        plt.plot(rec_signal, label=titlesvel[i])
        plt.title(titlesvel[i])
        plt.xlabel("Tiempo")
        plt.ylabel("Amplitud")
        plt.legend()
        filename = f"{titlesvel[i].replace(' ', '_')}_Reconstruida.png"
        filepath = os.path.join(carpetafinal, filename)
        plt.savefig(filepath)
        plt.show()
