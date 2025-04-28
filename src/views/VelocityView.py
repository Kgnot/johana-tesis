import flet as ft
from flet.core.scrollable_control import OnScrollEvent
from flet.core.types import ScrollMode

from src.component.VelocityComponents.dropdown.genericDropdown import GenericDropdown, DropType
from src.component.VelocityComponents.signalAnalysisSection.signalAnalysisSection import SignalAnalysisSection
from src.component.VelocityComponents.processButton.ProcessButton import ProcessButton
from src.component.text.GenericText import GenericText


class IntroSection(ft.Column):
    def __init__(self, row: ft.Row):
        super().__init__(
            controls=[
                GenericText("Estudio de Señales Biomecánicas", weight="bold", size=24),
                GenericText(
                    "Analice datos de aceleración y velocidad para comprender patrones de movimiento.",
                    size=16
                ),
                ft.Row([
                    ft.Image(
                        src="/icons/motion_analysis.png",
                        width=80,
                        height=80,
                        fit=ft.ImageFit.CONTAIN
                    ) if False else ft.Icon(ft.icons.ANALYTICS, size=60, color=ft.colors.BLUE),
                    ft.Container(
                        content=GenericText(
                            "Compare distintas fases del movimiento para detectar anomalías o evaluar mejoras.",
                            size=16
                        ),
                        padding=10,
                        width=500
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Card(
                    content=ft.Container(
                        padding=10,
                        content=ft.Column([
                            GenericText("Configuración de análisis", weight="bold"),
                            row,
                        ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ),
                    elevation=5
                )
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

    def on_process_click(self, e):
        pass


class VelocityView(ft.Container):
    def __init__(self):
        super().__init__(
            expand=True,
            padding=20,
            bgcolor="white",
        )
        # Opciones:
        type_options = [
            DropType("Acc", "Aceleración"),
            DropType("Velocidad", "Velocidad")
        ]
        data_options = [
            DropType("1", "Conjunto 1"),
            DropType("2", "Conjunto 2"),
            DropType("3", "Conjunto 3"),
            DropType("4", "Conjunto 4"),
        ]

        # Instancia de cada clase
        self.process_button = ProcessButton(self.on_process_click)
        self.type_dropdown = GenericDropdown("Tipo medición", type_options, "Acc")
        self.data_input = GenericDropdown("Conjunto de datos", data_options, "1")
        self.actions_accordion = ft.ExpansionPanelList(
            expand=True,
            visible=False
        )
        self.intro_section = IntroSection(ft.Row([
            self.type_dropdown,
            self.data_input,
            self.process_button
        ], alignment=ft.MainAxisAlignment.CENTER))

        # Contenedor final donde se mete el desplazamiento y el contenido
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    self.intro_section,
                    self.actions_accordion
                ],
                spacing=20,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ScrollMode.ALWAYS,
                on_scroll_interval=0,
                on_scroll=self.myscroll
            ),
            expand=True,
        )

    def myscroll(self, e: OnScrollEvent):
        #print(e)
        pass

    def build(self):
        return ft.Column(
            controls=[
                self.intro_section,
                self.actions_accordion
            ],
            spacing=20,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def on_process_click(self, e):
        #Guardar el tipo de medición para uso en los análisis
        if not hasattr(self.page, 'data') or self.page.data is None:
            self.page.data = {}
        self.page.data['med_type'] = self.type_dropdown.value
        self.page.data['datosProcesar'] = self.data_input.value
        # Limpiar el acordeón actual
        self.actions_accordion.controls.clear()

        # Crear secciones para cada acción
        actions = ['Pararse', 'Primer Giro', 'Giro para sentarse', 'Sentarse']
        for action in actions:
            section = SignalAnalysisSection(action)
            item = ft.ExpansionPanel(
                header=ft.Text(f"Analizar {action}"),
                content=section,
                bgcolor=ft.colors.BLUE_50
            )
            self.actions_accordion.controls.append(item)

        self.actions_accordion.visible = True
        self.update()

        # Mostrar mensaje de éxito
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(
                f"Datos listos para análisis - Tipo: {self.type_dropdown.value}, Conjunto: {self.data_input.value}")
        )
        self.page.snack_bar.open = True
        self.page.update()
