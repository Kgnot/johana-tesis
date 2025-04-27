#  Tesis de Johana
Esta es una pequeña documentación de todo lo utilizado, y de como iniciar.

El proyecto esta creado en Python 3.8.20 , instalaro de ser necesario.


Para iniciar primero es necesario clonar el proyecto: 
```Bash
git clone https://github.com/Kgnot/johana-tesis 
```
Después de clonar el proyecto, toca instalar la data que se  usará directamente
ubicandonos en la raiz del proyecto vamos a crear la carpeta data
```Bash
mkdir data
cd ./data
```
Una vez dentros de la carpeta `` Data`` necesitamos clonar los siguientes proyectos: 
```Bash
git clone https://github.com/opensim-org/opensim-models#
```
---
Una vez clonado y puesto eso en marcha. Debemos añadir todas las dependencias usadas que se
encuentran en ``requeriments.txt``. Para inicializarlas usamos el siguiente comando: 
```Bash
pip install -r requeriments.txt
```
Si por alguna razón no se tiene ``pip`` instalado podemos instalarlo usando: 
```Bash
python -m ensurepip --upgrade
```

---
## Dependencias instaladas con `pip`

> **numpy**: Librería fundamental para cálculos numéricos y matrices multidimensionales.
> 
> **plotly**: Herramienta de visualización interactiva en el navegador.
> 
> **sklearn** (o `scikit-learn`): Librería de machine learning con algoritmos de clasificación, regresión, clustering, etc.
> 
> **pandas**: Manipulación y análisis de estructuras de datos en forma de tablas.
> 
> **pyvirtualdisplay**: Crea un servidor X virtual para que aplicaciones gráficas se ejecuten "sin pantalla" (útil en servidores o WSL).
> 
> **c3d**: Lectura y manipulación de archivos de captura de movimiento en formato `.c3d`.
> 
> **ipython** / **ipykernel**: Soporte para notebooks, ejecución interactiva y desarrollo en Jupyter.
> 
> **tensorflow**: Framework de machine learning de alto rendimiento (usado si hay redes neuronales involucradas).
> 
> **svgutils**: Manipulación de archivos SVG como imágenes vectoriales.
> 
> **pywt** (PyWavelets): Análisis de señales usando transformadas wavelet.
> 
> **opensim**: [Esta dependencia debe instalarse aparte] — Interfaz de Python para usar el motor de simulación biomecánica OpenSim.
> 
> **flet** / **flet-cli** / **flet-desktop** / **flet-web**: Framework para construir aplicaciones visuales y multiplataforma con Python.
> 
> **pyinstaller**: Convierte scripts Python en ejecutables (.exe o binarios).
> 
> **gaitmap** / **gaitmap_mad**: Librerías para análisis de marcha (gait analysis), especialmente usando sensores o archivos de movimiento.
> 
> **scipy**: Complemento de `numpy` para cálculos científicos avanzados (integración, estadística, álgebra lineal, etc).
> 
> **Tabulate**: 
---
También se instalaron dependencias con conda, pero no se que tan necesarias son, sin embargo:
```Bash
conda activate opensim_env
# Apartado de conda: 
conda install -c ember123 opencolab 
conda install -c plotly plotly-orca 
```
También un apartado para WSL: 
```Bash
sudo apt-get update -y
sudo apt-get install -y x11-apps mesa-utils xvfb x11-utils libadolc2 coinor-libipopt-dev
```
## Dependencias instaladas con `conda`

> **opencolab** _(canal ember123)_: Herramientas relacionadas con biomecánica y OpenSim (usualmente con visualización remota en notebooks).
> 
> **plotly-orca** _(canal plotly)_: Renderizado de gráficos `plotly` en modo offline o como imágenes estáticas (útil para exportar PNG, PDF, etc).

---
## Para finalizar: 

Se inicia, desde el archivo raíz con: 
```bash
python main.py
```
