import numpy as np
import matplotlib.pyplot as plt

from logic.estudio_seniales.estudio_senales_cod import graficosXYZ_segmento


def test_graficosXYZ_segmento_basico():
    # Datos falsos: 100 muestras con 3 columnas (X, Y, Z)
    segmento = np.random.randn(100, 3)
    accion = "Correr"
    tipo_medicion = "Acelerómetro"
    tiempo_inicial = 0
    duracion_total = 100

    graficos = graficosXYZ_segmento(segmento, accion, tipo_medicion, tiempo_inicial, duracion_total)

    # --- Validaciones ---
    # Deben ser 3 figuras
    assert len(graficos) == 3

    for i, eje in enumerate(['X', 'Y', 'Z']):
        fig = graficos[i]
        ax = fig.axes[0]  # Cada figura tiene un solo Axes

        # Chequear título
        assert ax.get_title() == f"{accion} {tipo_medicion} {eje}"

        # Chequear labels de ejes
        assert ax.get_xlabel() == "Tiempo (s)"
        assert ax.get_ylabel() == "Amplitud"

        # Chequear que se hayan seteado xticks
        xticks = ax.get_xticks()
        xticklabels = [t.get_text() for t in ax.get_xticklabels()]
        assert len(xticks) == len(xticklabels) == 26

    # Cerrar figuras al final para evitar warnings
    plt.close("all")
