# Cargar el modelo
def execModelo():
    import os
    os.add_dll_directory("C:/OpenSim 4.5/bin")
    import opensim as osim

    # Configurar rutas de búsqueda de geometría ANTES de cargar el modelo
    osim.ModelVisualizer.addDirToGeometrySearchPaths("C:/OpenSim 4.5/Geometry")
    ruta_base = os.path.dirname(os.path.abspath(__file__))
    ruta_modelo = os.path.join(ruta_base, "../../data/opensim-models/Models/Gait2354_Simbody/gait2354_simbody.osim")

    modelo = osim.Model(ruta_modelo)
    modelo.setUseVisualizer(True)

    # Imprimir información básica del modelo
    print("Nombre del modelo:", modelo.getName())

    # Inicializar el sistema del modelo
    modelo.initSystem()

    # Intentar visualizar el modelo
    state = modelo.initializeState()

    modelo.getVisualizer().show(state)

# import os
# import sys
# import opensim as osim
#
# # Configurar OpenSim
# os.add_dll_directory("C:/OpenSim 4.5/bin")
# osim.ModelVisualizer.addDirToGeometrySearchPaths("C:/OpenSim 4.5/Geometry")
#
#
# def execModelo():
#     os.add_dll_directory("C:/OpenSim 4.5/bin")
#
#     # 🔥 Detectar si el script está empaquetado en un .exe
#     if getattr(sys, 'frozen', False):
#         ruta_base = sys._MEIPASS  # PyInstaller usa esta carpeta temporal
#     else:
#         ruta_base = os.path.dirname(os.path.abspath(__file__))
#
#     # Construir ruta del modelo
#     ruta_modelo = os.path.join(ruta_base, "data/opensim-models/Models/Gait2354_Simbody/gait2354_simbody.osim")
#
#     # Verificar si el archivo existe
#     if not os.path.exists(ruta_modelo):
#         print(f"⚠ ERROR: No se encontró el archivo: {ruta_modelo}")
#         return
#
#     # Cargar el modelo
#     modelo = osim.Model(ruta_modelo)
#     modelo.setUseVisualizer(True)
#
#     modelo.initSystem()
#     state = modelo.initializeState()
#     modelo.getVisualizer().show(state)
