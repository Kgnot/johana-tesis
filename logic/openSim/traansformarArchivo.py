import pandas as pd

# Ruta del archivo original
txt_file = "../../data/control/aposteriori/tug_1/60/MT_01200A8F-000-000_00B4578B.txt"
mot_file = "output.mot"

# Leer el archivo, ignorando las líneas de metadatos
data = pd.read_csv(txt_file, delim_whitespace=True, skiprows=12)

# Crear columna de tiempo
data.insert(0, "Tiempo", [i * 0.01 for i in range(len(data))])  # Suponiendo 100 Hz

# Seleccionar solo columnas relevantes para OpenSim
columnas_relevantes = ["Tiempo", "Acc_X", "Acc_Y", "Acc_Z", "VelInc_X", "VelInc_Y", "VelInc_Z"]
data = data[columnas_relevantes]

# Guardar en formato .mot
with open(mot_file, "w") as f:
    f.write("name: output\n")
    f.write(f"datacolumns: {len(columnas_relevantes)}\n")
    f.write(f"datarows: {len(data)}\n")
    f.write(f"range: {data['Tiempo'].iloc[0]} {data['Tiempo'].iloc[-1]}\n")
    f.write("endheader\n")
    data.to_csv(f, sep="\t", index=False)

print(f"Archivo .mot generado: {mot_file}")
