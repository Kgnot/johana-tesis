import os
import pandas as pd
import pytest

from logic.estudio_seniales.alistar_datos import obtener_carpeta, leer_csv, normalizar_dataframe


def test_obtener_carpeta_valida():
    base = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "Tdatos"))
    assert obtener_carpeta(1).endswith(os.path.join("apriori", "Control"))
    assert obtener_carpeta(4).endswith(os.path.join("POSTERIORI", "Experimental"))


def test_leer_csv(tmp_path):
    # CSV Falso
    contenido = """Header info line
Otra linea
Otra
Otra
Otra
Otra
Otra
Otra
Otra
Otra
Otra
Otra
0.1 0.2 0.3 1.0 2.0 3.0
0.2 0.3 0.4 1.5 2.5 3.5
"""
    archivo = tmp_path / "test.csv"
    archivo.write_text(contenido)

    df = leer_csv(archivo)
    assert list(df.columns) == ['Acc_X', 'Acc_Y', 'Acc_Z', 'VelInc_X', 'VelInc_Y', 'VelInc_Z']
    assert len(df) == 2


def test_normalizar_dataframe():
    df = pd.DataFrame({"A": [1, 2, 3], "B": [10, 20, 30]})
    df_norm = normalizar_dataframe(df)
    assert df_norm.min().min() == 0
    assert df_norm.max().max() == 1
