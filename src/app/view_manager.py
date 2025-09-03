import flet as ft
from src.views.ActivityRecognition import ActivityRecognition
from src.views.GaitParameters import GaitParameters
from src.views.HomeView import HomeView
from src.views.ManualView import ManualView
from src.views.BiomechanicalAnalysisView import BiomechanicalAnalysisView


def _initialize_views():
    return {
        0: HomeView(),
        1: BiomechanicalAnalysisView(),
        2: GaitParameters(),
        3: ActivityRecognition(),
        4: ManualView(
            "https://bibliotecadigital.ilce.edu.mx/Colecciones/CuentosMas/Cenicienta.pdf",
            "https://www.youtube.com/watch?v=QB0tJajDvMw"
        )
    }


class ViewManager:
    """ Responsable de gestionar las vistas """

    def __init__(self):
        self.view = _initialize_views()

    """ Función encargada de obtener una vista"""

    def get_view(self, index: int) -> ft.Container:
        return self.view.get(index)
