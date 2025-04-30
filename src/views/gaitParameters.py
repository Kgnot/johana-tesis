import flet as ft

from src.component.TimeInputs.TimeInputs import timeImputs
from src.component.dropdown.genericDropdown import DropType, GenericDropdown
from src.component.processButton.ProcessButton import ProcessButton
from src.component.text.GenericText import GenericText


class GaitParameters(ft.Container):
    def __init__(self):
        super().__init__(
            expand=True,
            padding=20,
            bgcolor="white",
        )
        data_options = [
            DropType("1", "Conjunto 1"),
            DropType("2", "Conjunto 2"),
            DropType("3", "Conjunto 3"),
            DropType("4", "Conjunto 4"),
        ]
        self.data_input = GenericDropdown("Conjunto de datos", data_options, "1")
        self.process_button = ProcessButton(self.on_process_click)
        ## Apartado de inputs:
        self.time_inputs = timeImputs()
        self.content = self.build()

    def build(self):
        return ft.Column(
            [
                GenericText("Parametros de la marcha", size=28, weight="bold"),
                GenericText(
                    "Aqui van los parametros de la marcha xd",
                    size=16
                ),
                GenericText(
                    "Vamos a mirar todo ",
                    size=16
                ),
                ft.Divider(),
                ft.Row([
                    self.data_input,
                    self.time_inputs,
                    self.process_button,
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

    def on_process_click(self,e):
        pass
