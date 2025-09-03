import flet as ft
from logic.openSim.openSim import execModelo
from .view_manager import ViewManager


class NavigationController:
    """Responsable de manejar la navegación"""

    def __init__(self, view_manager:ViewManager, content_container):
        self.view_manager = view_manager
        self.content_container = content_container
    """Encargado de cambiar la pagina"""

    def navigate_to(self, index):
        if index == 5:
            execModelo()
            return
        new_view:ft.Container = self.view_manager.get_view(index)
        if new_view:
            self.content_container.content = new_view
            self.content_container.update()
