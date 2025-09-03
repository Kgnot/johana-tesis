import flet as ft

from src.component.utils.sidebar.NavigationBar import NavigationBar

class Sidebar(ft.Container):
    def __init__(self, w, color, on_change,h = None):
        super().__init__(
            width=w,
            height=h,
            bgcolor=color,
            padding=10,
            expand=True,
            content=self.build_content(on_change)  # Agregamos el contenido correctamente
        )
        self.column1 = None
        self.height = h

    def build_content(self, on_change) -> ft.Column:
        self.column1 =  ft.Column(
            [
                ft.Text("Dashboard", size=20, weight="bold",color=" #2e4053"),
                ft.Divider(),
                ft.Container(
                    NavigationBar(on_change),
                    bgcolor="#ffffff",
                    expand=True,
                )
            ],
            expand=True)
        return self.column1