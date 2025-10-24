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
            "https://uc724cfcf2f20a747d5dade91a95.dl.dropboxusercontent.com/cd/0/inline2/Cz3xj2jXMEawPEucRyL-_NJJ6VsFzXTb71HcMiFP3dN8V4sCEeCteKypER-PNzE11ZDXNK6RAcer7seifs7G8wKamvuSlvSIEvD7zM9Z8_oimTFB1N4hzoWiXKAEklMoE-dYsSapv1W4WJJULzicDj_d1mKSLKg8b-hWB82lAf3DyD6gNxmG86QwBIHBppc5zyDwNG5pV_zHGpu8JuWtUqV7ovP2NL1rwKtRwvSMWht_FngpBVkfSfJlCvF2Qt8cXBxKiws0SAoqb6E4LiVg_SBz18LfAzH8GDBp6bddGoDtahss1sIPT_JvePIHy1tt1uUlS2dSN7ZkdJf91LpjxzvIPGfJClQksfhnMUHJBorVFKgRTgWhXBRFFxTPtcFODFc/file",
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
