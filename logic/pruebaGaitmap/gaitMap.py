import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from gaitmap.preprocessing.sensor_alignment import PcaAlignment, align_dataset_to_gravity
from gaitmap.stride_segmentation import BarthOriginalTemplate
from gaitmap.utils.coordinate_conversion import convert_to_fbf
from gaitmap.stride_segmentation import BarthDtw

# def analizarGait(data_list, ruta, nummaxcost):
# piede='../../data/control/aposteriori/tug_1/60/MT_01200A8F-000-000_00B4578C.txt'
# pieiz='../../data/control/aposteriori/tug_1/60/MT_01200A8F-000-000_00B4578D.txt'
pieiz='../../data/control/aposteriori/tug_1/60/MT_01200A8F-000-000_00B457A5.txt'

# piede = pd.read_csv(pi15ede, delim_whitespace=True, skiprows=12)1
pieiz = pd.read_csv(pieiz, delim_whitespace=True, skiprows=12)

data =pieiz[['Acc_X','Acc_Y','Acc_Z','Acc_X','Acc_Y','Acc_Z']]
 # Assign values to the DataFrame


# Definir la acción
señal=data.to_numpy()
# Función para extraer segmentos de la señal
def extraer_segmento(señal):
  segmentos = []
  for i in range(0,2):
    Ti = float(input(f"Ingresa el tiempo inicial deseado para segmento{i+1}: "))
    Tf = float(input(f"Ingresa el tiempo final deseado para {i+1}: "))

    # Convertir los tiempos a enteros
    To = int(Ti * 100)
    Te = int(Tf * 100)
    Tt=Te-To

    if To < 0 or Te > señal.shape[0] or To >= Te:
        print("Error: Los tiempos ingresados están fuera de rango o son inválidos.")
        return
    segmento = señal[To:Te, :]  # Extraer todas las columnas
    segmentos.append(segmento)
  return segmentos

datos=extraer_segmento(señal)
datos=np.vstack((datos[0],datos[1]))
datac=pd.DataFrame(datos)

  # Define headers
header0 = ['pelvis_sensor', 'pelvis_sensor', 'pelvis_sensor','pelvis_sensor', 'pelvis_sensor','pelvis_sensor']
header1 = ['acc_x', 'acc_y', 'acc_z', 'gyr_x', 'gyr_y', 'gyr_z']

datac.columns = pd.MultiIndex.from_arrays([header0, header1], names=['sensor', 'axis'])

gravity_aligned_data = align_dataset_to_gravity(datac, sampling_rate_hz=100, window_length_s=0.1, static_signal_th=15)

pca_alignment = PcaAlignment(target_axis="y", pca_plane_axis=("gyr_x", "gyr_y"))
pca_alignment = pca_alignment.align(gravity_aligned_data)
Final = pca_alignment.aligned_data_
# forward_aligned_data = (ForwardDirectionSignAlignment().align(Final, sampling_rate_hz=100).aligned_data_)

# _, axs = plt.subplots(2, 2, figsize=(13, 6))
# axs[0, 0].plot(rotated_dataset[sensor].iloc[:1000][SF_ACC])
# axs[0, 1].plot(forward_aligned_data[sensor].iloc[:1000][SF_ACC])
# for ax in axs[0]:

#   ax.grid("on")
# axs[1, 0].plot(rotated_dataset[sensor].iloc[:1000][SF_GYR])
# axs[1, 1].plot(forward_aligned_data[sensor].iloc[:1000][SF_GYR])
# for ax in axs[1]:

#   ax.grid("on")

# axs[0, 0].set_title("Acceleration - pelvis")
# axs[1, 0].set_title("Gyroscope - pelvis")
# axs[0, 1].set_title("Acceleration - rotated pelvis")
# axs[1, 1].set_title("Gyroscope - rotated pelvis")

# plt.tight_layout()
# plt.show()


template = BarthOriginalTemplate()

bf_data = convert_to_fbf(Final, left_like="pelvis_")
# bf_data = convert_to_fbf(forward_aligned_data, left_like="pelvis_")

nummaxcost=4.751418

dtw = BarthDtw(template=template, max_cost=nummaxcost)

dtw = dtw.segment(data=bf_data, sampling_rate_hz=100)

stride_list_left = dtw.stride_list_["pelvis_sensor"]
steps_left = len(stride_list_left)


total = steps_left

sensor = "pelvis_sensor"
fig, axs = plt.subplots(nrows=3, sharex=True, figsize=(10, 5))
dtw.data[sensor]["gyr_ml"].reset_index(drop=True).plot(ax=axs[0])
axs[0].set_ylabel("gyro [deg/s]")
axs[1].plot(dtw.cost_function_[sensor])
axs[1].set_ylabel("dtw cost [a.u.]")
axs[1].axhline(dtw.max_cost, color="k", linestyle="--")
axs[2].imshow(dtw.acc_cost_mat_[sensor], aspect="auto")
axs[2].set_ylabel("template position [#]")
for p in dtw.paths_[sensor]:
  axs[2].plot(p.T[1], p.T[0])
for s in dtw.matches_start_end_original_[sensor]:
  axs[1].axvspan(*s, alpha=0.3, color="g")
for _, s in dtw.stride_list_[sensor][["start", "end"]].iterrows():
  axs[0].axvspan(*s, alpha=0.3, color="g")
axs[0].set_xlabel("time [#]")
fig.tight_layout()
plt.show()

print(total)