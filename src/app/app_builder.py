import flet as ft

from src.component.utils.sidebar.Sidebar import Sidebar
from src.component.utils import ContentContainer
from src.frame.Frame import Frame


class AppBuilder:
    """ Responsable de construir la interfaz del usuario"""

    def __init__(self, page: ft.Page):
        self.page = page
        self.frame = Frame(page)
        self.content_container = ContentContainer()

    def build_ui(self, navigation_callback) -> ft.Container:
        sidebar = Sidebar(w=200, color="white", on_change=navigation_callback)
        content_container: ft.Container = self.content_container
        self.frame.add(sidebar, content_container)
        return content_container
