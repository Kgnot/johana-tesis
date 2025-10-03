import flet as ft
from .navigation_controller import NavigationController
from .view_manager import ViewManager
from .app_builder import AppBuilder


class ModelApp:
    """Responsable principal de coordinar la aplicación"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.view_manager = ViewManager()
        self.app_builder = AppBuilder(page)
        self.navigation_controller = None

    def run(self):
        content_container: ft.Container = self.app_builder.build_ui(self.on_nav_change)
        self.navigation_controller = NavigationController(
            self.view_manager, content_container
        )

    def on_nav_change(self, e):
        self.navigation_controller.navigate_to(e.control.selected_index)
