import numpy as np
from matplotlib import pyplot as plt
from scipy.signal import find_peaks

from logic.utils.extraerSeñalesFiltradas import extraer_seniales_filtradas


# cuando estamos en marcha señal = señalz que se ubica con el DT como:
# señalaz=[DT[:,2]] #Acc_Z
def marcha(dato_procesar: int,Ti,Tf):

    print("Datos desde marcha funcion : ", dato_procesar, " - ", Ti, " - ",Tf)

    final_data = {}
    DT, seniales, datosfinal_total = extraer_seniales_filtradas(dato_procesar)
    senial = [DT[:, 2]]  # ACC_Z
    seniall = np.array(senial).T
    fs = 100
    longitud = int(0.38 * fs)
    datos = seniall
    duracion_total = len(datos) / fs
    segmentos = []

    ###
    graficas_segmentos = []

    for l in range(0, 2):
        print(f"\n--- Segmento {l + 1} ---")
        print(f"La duración de la señal es de {duracion_total:.2f} segundos.")
        To = int(Ti * fs)
        Te = int(Tf * fs)
        if To < 0 or Te > len(datos) or To >= Te:
            print("Error: Los tiempos ingresados están fuera de rango o son inválidos.")
            return
        if datos.ndim == 1:
            segmento = datos[To:Te]
        else:
            segmento = datos[To:Te, 0]

        segmentos.append(segmento)

    # Unir y normalizar los segmentos
    if len(segmentos) < 2:
        print("No se obtuvieron dos segmentos válidos.")
        return final_data
    else:
        señal_completa = np.concatenate(segmentos)

        # Normalización Min-Max
        min_val = np.min(señal_completa)
        max_val = np.max(señal_completa)
        if max_val - min_val == 0:
            print("Advertencia: la señal es constante, no se puede normalizar.")
            señal_normalizada = señal_completa  # evitar división por cero
        else:
            señal_normalizada = (señal_completa - min_val) / (max_val - min_val)

        t = np.arange(len(señal_normalizada)) / fs
        tiempot = len(t) / 100
        amplitud = 0.6  # umbral sobre la señal normalizada

        peaks, _ = find_peaks(señal_normalizada, height=amplitud, distance=longitud)
        print("\n")

        v = np.array([np.trapz(señal_normalizada[:i + 1], t[:i + 1]) for i in range(len(t))])
        d = np.array([np.trapz(v[:i + 1], t[:i + 1]) for i in range(len(t))])

        npasos = len(peaks)
        distancia_total = d[-1]
        velocidad = distancia_total / tiempot
        tpaso = tiempot / npasos
        cadencia = (npasos / tiempot) * 60
        longitudpaso = distancia_total / npasos
        tzancada = 120 / cadencia
        czancadas = int(npasos / 2)
        longitudzan = velocidad * tzancada
        mini = np.min(señal_normalizada)  # Mínimo
        maxi = np.max(señal_normalizada)  # Máximo
        rango = maxi - mini  # Rango
        jerk = np.gradient(señal_normalizada, 1 / 100)
## Aqui extraemos la figura
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(t, señal_normalizada, label="Señal Normalizada")
        ax.plot(t[peaks], señal_normalizada[peaks], "rx", label="Picos")
        ax.set_title("Señal Normalizada - Picos Detectados")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")
        ax.legend()
        ax.grid(True)
        fig.tight_layout()
        graficas_segmentos.append(fig)
        ## otro plot:
        fig2, ax2 = plt.subplots(figsize=(12, 6))
        ax2.plot(t, v, label="Velocidad", color="green")
        ax2.set_title("Velocidad de la marcha")
        ax2.set_xlabel("Tiempo (s)")
        ax2.set_ylabel("Velocidad (u.a.)")
        ax2.grid(True)
        fig2.tight_layout()
        graficas_segmentos.append(fig2)
        ## Tercer plot:
        fig3, ax3 = plt.subplots(figsize=(12, 6))
        ax3.plot(t, d, label="Distancia", color="purple")
        ax3.set_title("Distancia")
        ax3.set_xlabel("Tiempo (s)")
        ax3.set_ylabel("Distancia (u.a.)")
        ax3.grid(True)
        fig3.tight_layout()
        graficas_segmentos.append(fig3)
        nc = 0
        headers = ["Características", f"Persona"]
        caracteristicas = ["Distancia (m)", "Velocidad promedio (m/s)", "Cantidad de pasos", "Tiempo del paso (s)",
                           "Longitud del paso (m) ", "Cadencia (pasos/min)", "Cantidad de zancadas",
                           "Longitud de la Zancada (m)", "Tiempo de la zancada (s)"]
        data = [
            [caracteristicas[0], distancia_total],
            [caracteristicas[1], velocidad],
            [caracteristicas[2], npasos],
            [caracteristicas[3], tpaso],
            [caracteristicas[4], longitudpaso],
            [caracteristicas[5], cadencia],
            [caracteristicas[6], czancadas],
            [caracteristicas[7], npasos],
            [caracteristicas[8], longitudzan]
        ]
        final_data = {
            "headers": headers,
            "data":data,
            "graficas_segmentos":graficas_segmentos,
            "grafica_normalizada":fig,
            "grafica_velocidad":fig2,
            "grafica_distancia":fig3,
        }
        print("Data final be like: ",final_data)
        return final_data

#marcha(1,1,3)