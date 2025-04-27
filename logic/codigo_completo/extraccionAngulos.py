import numpy as np
import pandas as pd
import math
from matplotlib import pyplot as plt


########Extracción de angulos:
def artan(señal):
    señala=np.squeeze(np.array(señal)).T
    X=[]
    Y=[]
    for i in range(0,len(señala[0])):
      anguloX=math.atan((señala[1][i])/(señala[2][i]))
      anguloY=math.atan((señala[0][i])/(señala[2][i]))
      X.append(anguloX)
      Y.append(anguloY)
    minax= np.min(X)
    maxax= np.max(X)
    rangox=maxax-minax
    minay= np.min(Y)
    maxay= np.max(Y)
    rangoy=maxay-minay
    long=31
    coefi=np.ones(long)
    b=coefi/long
    anx=np.array(X)
    X = np.convolve(anx,b)
    any=np.array(X)
    Y = np.convolve(any,b)
    C1=0
    C2=0
    #plotear angulos
    while True:
      if (C1==0)and(C2==0):
        plt.figure()
        plt.plot(X)
        plt.title('Ángulos de inclinación en X')
        plt.figure()
        plt.plot(Y)
        plt.title('Ángulos de inclinación en Y')
        plt.show()
        C2=1
      elif(C1==0)and(C2==1):
        break

    #Mostrar resultados
    datos=[["X",minax,maxax,rangox],["Y",minay,maxay,rangoy]]
    angulos = pd.DataFrame(datos, columns=['Ángulo','Ángulo mínimo', 'Ángulo máximo', 'Rango'])
    print()
    print(angulos)

