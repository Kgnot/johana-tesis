import os

import numpy as np
import pywt
from matplotlib import pyplot as plt
from sklearn.decomposition import FastICA

from logic.estudio_seniales.EstudioSenalesCod import extraer_seniales_filtradas


## señalwa es el mismo DT
## Necesitamos un dato a procesar:
def wavelet(dato_procesar: int):
    # llamamos a extraclaims para DT:
    DT, seniales, datosfinal_total = extraer_seniales_filtradas(dato_procesar)
    senialw = DT
    columns = ['acc_x', 'acc_y', 'acc_z', 'gyr_x', 'gyr_y', 'gyr_z']
    col_idx = {name: i for i, name in enumerate(columns)}
    wavelet = 'db38'
    # Señales a procesar
    signals = ['acc_x', 'acc_y', 'acc_z']
    sigvel = ['gyr_x', 'gyr_y', 'gyr_z']

    icasac = []  #
    icasvel = []

    # Procesamiento de aceleración
    # Análisis de componentes independientes
    icasac:[] = procesar_ica(senialw, signals, col_idx, wavelet)
    icasvel:[] = procesar_ica(senialw, sigvel, col_idx, wavelet)
    # Graficar resultados ICA
    titlesac = ['ICA - Acc_X', 'ICA - Acc_Y', 'ICA - Acc_Z']
    titlesvel = ['ICA - Vel_X', 'ICA - Vel_Y', 'ICA - Vel_Z']
    figuras_aceleracion:[] = crear_grafico_icas(icasac, titlesac)
    figuras_velocidad:[] = crear_grafico_icas(icasvel, titlesvel)

    # Transformaciones combinadas -- Preguntar porque no se usan xd
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
        signal_data = senialw[:, col_idx[signals[i]]]
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
        signal_data = senialw[:, col_idx[sigvel[i]]]
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

    graficos_reconstruiccion_ac:[] = crear_grafico_recontruido(reconstructed_signals_ac, titlesac)
    graficos_reconstruiccion_vel:[] = crear_grafico_recontruido(reconstructed_signals_vel, titlesvel)

    resultados = {
        # 'ica_acc': resultados_ica_acc,
        # 'ica_vel': resultados_ica_vel,
        'graficos_ica_ac': figuras_aceleracion,
        'graficos_ica_vel': figuras_velocidad,
        # 'señales_reconstruidas_ac': reconstructed_signals_ac,
        # 'señales_reconstruidas_vel': reconstructed_signals_vel,
        'graficos_reconstruccion_ac': graficos_reconstruiccion_ac,
        'graficos_reconstruccion_vel': graficos_reconstruiccion_vel
    }

    return resultados

def crear_grafico_recontruido(reconstructed_signals, titles):
    figuras = []
    for i, rec_signal in enumerate(reconstructed_signals):
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(rec_signal, label=titles[i])
        ax.set_title(titles[i])
        ax.set_xlabel("Tiempo")
        ax.set_ylabel("Amplitud")
        fig.tight_layout()
        figuras.append(fig)
    return figuras

def crear_grafico_icas(icas, titles):  ## por icas
    figuras = []
    for i, ica_result in enumerate(icas):
        fig, ax = plt.subplots(figsize=(12, 8))

        for j in range(ica_result.shape[1]):
            ax = fig.add_subplot(6, 1, j + 1)
            ax.plot(ica_result[:, j])
            ax.set_title(f'{titles[i]} - Componente {j + 1}')
            ax.set_xlabel('Tiempo')
            ax.set_ylabel('Amplitud')
        # Ajustar layout
        fig.tight_layout()
        # Agregar figura a la lista
        figuras.append(fig)

    return figuras

def procesar_ica(datos, seniales, col_idx, wavelet, nivel=6):
    resultados_ica = []
    for senial in seniales:
        # Extraer datos de la señal
        datos_señal = datos[:, col_idx[senial]]
        # Descomponer señal con wavelet
        coeficientes = pywt.wavedec(datos_señal, wavelet, level=nivel)
        (_, *detalles) = coeficientes  # Separar aproximación de detalles

        # Encontrar la longitud mínima para los coeficientes
        longitudes = [len(d) for d in detalles]
        min_longitud = min(longitudes)

        # Recortar todos los coeficientes a la longitud mínima
        coeficientes_recortados = np.vstack([
            d[:min_longitud] for d in detalles
        ]).T

        # Aplicar ICA
        modelo_ica = FastICA(n_components=len(detalles))
        ica_transformada = modelo_ica.fit_transform(coeficientes_recortados)
        resultados_ica.append(ica_transformada)

    return resultados_ica

#wavelet(1)