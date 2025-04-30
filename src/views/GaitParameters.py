import flet as ft
from flet.core.scrollable_control import OnScrollEvent
from flet.core.types import ScrollMode

from src.component.GaitParameter.ResultGaitParameter import ResultGaitParameter
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
        self.progress = ft.ProgressRing(
            width=24,
            height=24,
            visible=False,
            stroke_width=2,
            color=ft.colors.BLUE_600
        )
        self.result_gait_parameter = ResultGaitParameter()
        self.result_gait_parameter.visible = False
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
                    self.progress
                ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER
                ),
                self.result_gait_parameter
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            scroll=ScrollMode.ALWAYS,
            on_scroll_interval=0,
            on_scroll=self.myscroll
        )

    def myscroll(self, e: OnScrollEvent):
        pass

    def on_process_click(self, e):
        self.progress.visible = True
        self.process_button.disabled = True
        dato = int(self.data_input.value)
        ti_str = float(self.time_inputs.controls[0].value)
        tf_str = float(self.time_inputs.controls[1].value)
        valor_bool = self.result_gait_parameter.init_charts(dato, ti_str, tf_str)
        if valor_bool:
            self.result_gait_parameter.visible = True
            self.progress.visible = False
            self.process_button.disabled = False
            self.result_gait_parameter.update()
            self.page.update()
        else:
            self.page.snack_bar = ft.SnackBar(
                content=ft.Text(
                    f"Los tiempos ingresados están fuera de rango o son inválidos.",
                    color=ft.colors.WHITE
                ),
                bgcolor=ft.colors.AMBER_400,
            )
            self.page.snack_bar.open = True
            self.progress.visible = False
            self.process_button.disabled = False
             
