import numpy as np
from matplotlib import pyplot as plt


## Aqui tenemos que guardar dos respuestas, graficos y tabla
def featuresac(senial):
    # Inicializa listas para almacenar las características
    rms_list = []
    potencia_list = []
    energia_list = []
    minimo_list = []
    maximo_list = []
    rango_list = []
    jerkl = []
    jerkmin = []
    jerkmax = []
    jerkrms = []
    jerkmedia = []
    tiempot = []
    jerk_graficos = []

    # Asegúrate de que la señal sea un array de NumPy
    senialf = np.array(senial)
    if senialf.ndim ==1 :
        senialf = senialf.reshape(-1,1)

    lab = ['Acc_X', 'Acc_Y', 'Acc_Z']
    nc = senialf.shape[1]

    for y in range(nc):
        columna = senialf[:, y]
        li = len(columna) / 100
        lo = len(columna)
        tiempot.append(li)
        tm = np.linspace(0, li, lo)
        tiempo = np.sort(tm)

        # Calucla las caracteristicas
        rms = np.sqrt(np.mean(columna ** 2))
        potencia = np.sqrt((np.sum(columna)) ** 2)
        energia = (np.sum(columna)) ** 2
        mini = np.min(columna)
        maxi = np.max(columna)
        rango = maxi - mini
        jerk = np.gradient(columna, tiempo)
        jerkma = np.max(jerk)
        jerkmi = np.min(jerk)
        jerkmed = np.mean(jerk)

        # Guardar
        rms_list.append(rms)
        potencia_list.append(potencia)
        energia_list.append(energia)
        minimo_list.append(mini)
        maximo_list.append(maxi)
        rango_list.append(rango)
        jerkmax.append(jerkma)
        jerkmin.append(jerkmi)
        jerkmedia.append(jerkmed)

        # Crear y guardar gráfico
        if len(columna) > 5 :
            fig, ax = plt.subplots(figsize=(8, 4))
            ax.plot(tiempo, jerk)
            ax.set_title(f"Jerk vs Tiempo {lab[y]}")
            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel("Jerk (m/s³)")
            ax.grid(True)
            jerk_graficos.append(fig)
        #plt.close(fig)  # Cierra cada figura inmediatamente
    caracteristicas = [
        "RMS", "Tiempo de la Prueba (s)", "Potencia", "Energía", "Valor Máximo",
        "Valor Mínimo", "Rango Aceleraciones", "Jerk Máximo", "Jerk Mínimo", "Jerk Medio"
    ]
    listas_por_caracteristica = [
        rms_list, tiempot, potencia_list, energia_list, maximo_list,
        minimo_list, rango_list, jerkmax, jerkmin, jerkmedia
    ]

    total_data = []
    data = []
    for i, nombre in enumerate(caracteristicas):
        fila = [nombre]
        valores = listas_por_caracteristica[i]
        for eje in range(nc):
            if eje < len(valores):
                fila.append(valores[eje])
            else:
                fila.append("N/A")
        data.append(fila)
        total_data.append(data)

    plt.close('all')
    return total_data, jerk_graficos
