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
            "https://uc723e15ed308fee84b26d31e83c.dl.dropboxusercontent.com/cd/0/inline2/Cz3K9nP1X3g4R67QnoIxD14RqnYTR3dHTY3YU9H0Q4u7taVMuiWQ6LtMiFgOU6DqRe7SMmz-YobboWJH9EGy6dwyNdXIc20eTcuKxY6AXZV-2YQoCgzg_Y5cP4UK39_AlW21oH7IFioHVw5c9MD70ld5pHzkVcSK1OGWzK6thCUOng4xxwhGqyFcNjJ7oJd777JX8yDBaP0vNo-sy4zdt4hShtAJ2aHnFmFbTBVqtYz18XqD79RQbBzRFPKE6MmRJeoKqSQlYG20tx9dxewXYdDSaqeUFaXhfKbHdVDEIJ57tQC0uZ-y0P1TtmkyAmwaL7V3aZInHO6LXWrZVHINJ8byCUV8o6QTOo6WyRGm2Z6bMmPbXLMcSO6t5swrLC9rXVM/file",
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
