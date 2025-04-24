import numpy as np

# Leer los datos del archivo
data = np.loadtxt("output.mot", skiprows=7)  # Saltar las primeras 7 líneas (encabezado)
time = data[:, 0]  # Columna de tiempo
acc_x = data[:, 1]  # Aceleración en X
acc_y = data[:, 2]  # Aceleración en Y
acc_z = data[:, 3]  # Aceleración en Z

# Parámetros
dt = time[1] - time[0]  # Intervalo de tiempo entre muestras

# Integrar aceleraciones para obtener velocidades
vel_x = np.cumsum(acc_x) * dt
vel_y = np.cumsum(acc_y) * dt
vel_z = np.cumsum(acc_z) * dt

# Integrar velocidades para obtener posiciones
pos_x = np.cumsum(vel_x) * dt
pos_y = np.cumsum(vel_y) * dt
pos_z = np.cumsum(vel_z) * dt

# Guardar las posiciones como marcadores virtuales
with open("processed_markers.mot", "w") as file:
    # Encabezado
    file.write("Markers\n")
    file.write("version=1\n")
    file.write(f"nRows={len(time)}\n")
    file.write("nColumns=4\n")
    file.write("inDegrees=no\n")
    file.write("Units are meters.\n\n")
    file.write("Time\tMarker_X\tMarker_Y\tMarker_Z\n")

    # Datos
    for t, x, y, z in zip(time, pos_x, pos_y, pos_z):
        file.write(f"{t}\t{x}\t{y}\t{z}\n")

print("Archivo de marcadores procesado correctamente.")