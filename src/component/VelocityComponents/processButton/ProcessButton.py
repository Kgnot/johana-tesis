import flet as ft

class ProcessButton(ft.ElevatedButton):
    def __init__(self, on_click, txt = "Procesar Datos"):
        super().__init__(
            text=txt,
            on_click=on_click,
            bgcolor=ft.colors.BLUE_700,
            color=ft.colors.WHITE
        )
