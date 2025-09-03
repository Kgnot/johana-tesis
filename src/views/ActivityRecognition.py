import flet as ft
from flet.core.scrollable_control import OnScrollEvent
from flet.core.types import ScrollMode
from src.component.activity_recognition.ResultActivityRecognition import ResultActivityRecognition

from ..component.utils import (
    DropType,
    GenericDropdown,
    ProcessButton,
    GenericText)


class ActivityRecognition(ft.Container):
    def __init__(self):
        super().__init__(
            expand=True,
            padding=30,
            bgcolor=ft.colors.WHITE,
        )
        data_options = [
            DropType("1", "Conjunto 1"),
            DropType("2", "Conjunto 2"),
            DropType("3", "Conjunto 3"),
            DropType("4", "Conjunto 4"),
        ]
        self.data_input = GenericDropdown("Conjunto de datos", data_options, "1")
        self.process_button = ProcessButton(self.on_process_click)
        self.resultActivity = ResultActivityRecognition()
        self.progress = ft.ProgressRing(
            width=24,
            height=24,
            visible=False,
            stroke_width=2,
            color=ft.colors.BLUE_600
        )
        self.content = self.build()
        self.resultActivity.visible = False

    def build(self):
        return ft.Column(
            controls=[
                GenericText("Reconocimiento de Actividades", weight="bold"),
                GenericText(
                    "El reconocimiento de actividades permite diferenciar entre distintas acciones mediante datos "
                    "capturados en tiempo real.",
                    size=16
                ),
                GenericText(
                    "A través de sensores, se pueden identificar patrones de movimiento específicos como caminar, correr "
                    "o estar en reposo.",
                    size=16
                ),
                ft.Row([
                    self.data_input,
                    self.process_button,
                    self.progress

                ],
                    spacing=15,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                self.resultActivity
            ],
            spacing=25,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ScrollMode.ALWAYS,
            on_scroll_interval=0,
            on_scroll=self.myscroll
        )

    def myscroll(self, e: OnScrollEvent):
        pass

    def on_process_click(self, e):
        if not hasattr(self.page, 'data_activity') or self.page.data is None:
            self.page.data = {}
        self.progress.visible = True
        self.process_button.disabled = True
        self.update()
        # Apartado
        self.page.data['med_type_recognition'] = self.data_input.value
        self.resultActivity.init_charts()
        self.resultActivity.visible = True
        self.progress.visible = False
        self.process_button.disabled = False
        self.resultActivity.update()
        self.page.update()
