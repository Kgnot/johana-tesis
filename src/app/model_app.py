from typing import Optional
import flet as ft
from .navigation_controller import NavigationController
from .view_manager import ViewManager
from .app_builder import AppBuilder


class ModelApp:
    """Responsable principal de coordinar la aplicación"""

    def __init__(self):
        self.view_manager = ViewManager()  # Encargado de inicializar las vistas y manejarlas
        self.navigation_controller = None  # Controlador para navegar
        self.app_builder = None  # Construir UI

    def start(self):
        ft.app(target=self.run)

    def start_web(self):
        ft.app(target=self.run, port=9000, view=ft.WEB_BROWSER)

    def run(self, page: ft.Page):
        self.app_builder = AppBuilder(page)  # construimos la application con una pagina
        content_container: ft.Container = self.app_builder.build_ui(self.on_nav_change)  # Construimo el ui

        self.navigation_controller: NavigationController = NavigationController(
            self.view_manager, content_container
        )  # agregamos el controlador de navegación

    def on_nav_change(self, e):
        self.navigation_controller.navigate_to(e.control.selected_index)
