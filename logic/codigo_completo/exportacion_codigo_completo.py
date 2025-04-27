import numpy as np
from matplotlib import pyplot as plt

from logic.codigo_completo.caracteristicaAceleracion import featuresac
from logic.codigo_completo.extraccionAngulos import artan
from logic.codigo_completo.filtroButterworth import filtroButterworth_DatosFinalTotal
#from logic.codigo_completo.espectroFrecuencias import DT

def extraclaims(datTatosProcesar:int):
    datosfinal_total = filtroButterworth_DatosFinalTotal(datTatosProcesar)

    for x in range(len(datosfinal_total)):
        DT = datosfinal_total[x]
        DT = np.array(DT)
        da = DT[:, 0:3]
        dv = DT[:, 3:6]
        da = (da - da.min(axis=0)) / (da.max(axis=0) - da.min(axis=0))
        DT = np.hstack((da, dv))
        DT = np.array(DT)


def segmulac(med:str,datTatosProcesar:int):
    ###



    # En todos los ejes de aceleración senial es = senialac = [DT[:,0:3]]
    senial = [DT[:0, 3]] # Asi estaba

    senialr = np.array(senial)
    # Este seg son las cosas que se desean como pararse etc
    seg1 = ['Pararse',
            'Primer Giro',
            'Giro para sentarse',
            'Sentarse']
    med1 = med # Este apartado puede ser Velocidad o Aceleración , lo pasaremos como parametro xd

    for k in range(0, len(senialr)):
        for i, accion in enumerate(seg1):
            Ti = float(input(f"Ingresa el tiempo inicial deseado para {accion}: "))
            Tf = float(input(f"Ingresa el tiempo final deseado para {accion}: "))

            To = int(Ti * 100)
            Te = int(Tf * 100)
            Tt = Te - To

            if To < 0 or Te > senialr.shape[1] or To >= Te:
                print("Error: Los tiempos ingresados están fuera de rango o son inválidos.")
                return

                # Extraer la parte de la senial correspondiente
            senial = senialr[k]
            senial = senial[To:Te]
            fig, axs = plt.subplots(3, 1, figsize=(20, 10))

            new_xticks = np.linspace(0, Tt, 26)
            new_xticklabels = [f"{(i / 100) + Ti:.2f}" for i in new_xticks]

            axs[0].plot(senial[:, 0])
            axs[0].set_title(f"{accion} {med1} X")
            axs[0].set_xticks(new_xticks, new_xticklabels)
            axs[0].set_xlabel('Tiempo')
            axs[0].set_ylabel('Amplitud')
            axs[0].grid()

            axs[1].plot(senial[:, 1])
            axs[1].set_title(f"{accion} {med1} Y")
            axs[1].set_xticks(new_xticks, new_xticklabels)
            axs[1].set_xlabel('Tiempo')
            axs[1].set_ylabel('Amplitud')
            axs[1].grid()

            axs[2].plot(senial[:, 2])
            axs[2].set_title(f"{accion} {med1} Z")
            axs[2].set_xticks(new_xticks, new_xticklabels)
            axs[2].set_xlabel('Tiempo')
            axs[2].set_ylabel('Amplitud')
            axs[2].grid()

            plt.subplots_adjust(hspace=0.5)
            artan(senial)
            print("\n")
            car = None
            if med == "Acc":
                car = featuresac(senial)
            elif med == "Velocidad":
                car = featuresac(senial)

            if car is not None:
                print("Características de la senial:")
                for key, value in car.items():
                    print(f"{key}: {value}")

        plt.show()

segmulac("Acc",1)
