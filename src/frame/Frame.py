import flet as ft

class Frame:

    def __init__(self,page:ft.Page):
        self.page = page
        self.page.title = "Tesis Bioingenieria"
        self.page.padding = 0
        self.page.bgcolor = "#d6dbdf"
        self.page.theme_mode = "light"

    def add(self,component1,component2):
        self.page.add(
            ft.Row(
                [
                    ft.Container(component1, width=200, expand=False),  #no se expande si no tiene un ancho fijo
                    ft.Container(component2, expand=True)   # Se expande lo que quedá
                ],
                expand=True
            ))