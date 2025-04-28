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
                GenericText("Estudio de Señales Biomecánicas", weight=ft.FontWeight.BOLD, size=28),
                GenericText(
                    "Analice datos de aceleración y velocidad para comprender patrones de movimiento.",
                    size=16,
                    color=ft.colors.GREY_700
                ),
                ft.Row([
                    ft.Icon(ft.icons.ANALYTICS, size=60, color=ft.colors.GREY_700),
                    ft.Container(
                        content=GenericText(
                            "Compare distintas fases del movimiento para detectar anomalías o evaluar mejoras.",
                            size=16,
                            color=ft.colors.GREY_700
                        ),
                        padding=10,
                        width=500
                    )
                ], alignment=ft.MainAxisAlignment.CENTER),
                ft.Container(
                    content=ft.Column([
                        GenericText("Configuración de análisis", weight=ft.FontWeight.BOLD, color=ft.colors.BLUE_GREY_900),
                        row,
                    ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                    padding=ft.Padding(20, 20, 20, 20),
                    border_radius=10,
                    bgcolor=ft.colors.WHITE,
                    shadow=ft.BoxShadow(
                        spread_radius=1,
                        blur_radius=15,
                        color=ft.colors.with_opacity(0.2, ft.colors.BLUE_GREY_900),
                        offset=ft.Offset(0, 4)
                    )
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
            padding=30,
            bgcolor=ft.colors.WHITE,
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
            visible=False,
            spacing=8
        )
        self.intro_section = IntroSection(ft.Row([
            self.type_dropdown,
            self.data_input,
            self.process_button
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, spacing=15))

        # Contenedor final donde se mete el desplazamiento y el contenido
        self.content = ft.Container(
            content=ft.Column(
                controls=[
                    self.intro_section,
                    self.actions_accordion
                ],
                spacing=25,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ScrollMode.ALWAYS,
                on_scroll_interval=0,
                on_scroll=self.myscroll
            ),
            expand=True,
        )

    def myscroll(self, e: OnScrollEvent):
        pass

    def build(self):
        return ft.Column(
            controls=[
                self.intro_section,
                self.actions_accordion
            ],
            spacing=25,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def on_process_click(self, e):
        # Guardar el tipo de medición para uso en los análisis
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
                header=ft.Container(
                    content=ft.Text(f"Analizar {action}", weight=ft.FontWeight.W_500),
                    padding=12
                ),
                content=section,
                bgcolor=ft.colors.WHITE
            )
            self.actions_accordion.controls.append(item)

        self.actions_accordion.visible = True
        self.update()

        # Mostrar mensaje de éxito
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(
                f"Datos listos para análisis - Tipo: {self.type_dropdown.value}, Conjunto: {self.data_input.value}",
                color=ft.colors.WHITE
            ),
            bgcolor=ft.colors.AMBER_400,
            #action=ft.SnackBarAction("OK", lambda e: setattr(self.page.snack_bar, "open", False))
        )
        self.page.snack_bar.open = True
        self.page.update()