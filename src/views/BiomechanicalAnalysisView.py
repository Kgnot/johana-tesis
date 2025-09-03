import flet as ft
from flet.core.scrollable_control import OnScrollEvent
from flet.core.types import ScrollMode
from src.error.Error import Error
from src.component.biomechanical_analysis_view import IntroSection, SignalAnalysisSection
from src.component.utils import (
    ProcessButton,
    ChooseDataSetDropdown,
    DropType,
    GenericDropdown)


def _create_analysis_sections(actions: list) -> list:
    """Crea las secciones de análisis para cada acción"""
    sections = []
    for action in actions:
        section = SignalAnalysisSection(action)
        panel = ft.ExpansionPanel(
            header=ft.Container(
                content=ft.Text(f"Analizar {action}", weight=ft.FontWeight.W_500),
                padding=12
            ),
            content=section,
            bgcolor=ft.colors.WHITE
        )
        sections.append(panel)
    return sections


class BiomechanicalAnalysisView(ft.Container):
    STANDARD_ACTIONS = {
        'common': ['Pararse', 'Primer Giro', 'Giro para sentarse', 'Sentarse'],
        'acceleration': ['Caminata ida', 'Caminata vuelta']
    }

    def __init__(self):
        super().__init__(
            expand=True,
            padding=30,
            bgcolor=ft.colors.WHITE,
        )

        self._initialize_components()
        self.content = self._build_content()

    def _initialize_components(self):
        """Inicializa todos los componentes de la UI"""
        type_options = [
            DropType("Acc", "Aceleración"),
            DropType("Velocidad", "Velocidad")
        ]

        self.process_button = ProcessButton(self._handle_process_click)
        self.type_dropdown = GenericDropdown("Tipo medición", type_options, "Acc")
        self.data_input = ChooseDataSetDropdown()
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

    def _build_content(self):
        """Construye el layout principal"""
        return ft.Container(
            content=ft.Column(
                controls=[
                    self.intro_section,
                    self.actions_accordion
                ],
                spacing=25,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                scroll=ScrollMode.ALWAYS,
                on_scroll_interval=0,
                on_scroll=self._handle_scroll
            ),
            expand=True,
        )

    def _handle_scroll(self, e: OnScrollEvent):
        """Maneja eventos de scroll"""
        pass

    def _handle_process_click(self, e):
        """Coordina el proceso de análisis"""
        self._save_configuration()
        self._rebuild_analysis_sections()
        self._show_success_message()

    def _save_configuration(self):
        """Guarda la configuración en el contexto global"""
        if not hasattr(self.page, 'data') or self.page.data is None:
            self.page.data = {}

        self.page.data['med_type'] = self.type_dropdown.value
        self.page.data['datosProcesar'] = self.data_input.value

    def _rebuild_analysis_sections(self):
        """Reconstruye las secciones de análisis según la configuración"""
        med_type = self.page.data['med_type']
        # Limpiar y reconstruir
        self.actions_accordion.controls.clear()

        actions = self._get_actions_for_type(med_type)
        analysis_sections = _create_analysis_sections(actions)

        self.actions_accordion.controls.extend(analysis_sections)
        self.actions_accordion.visible = True
        self.update()

    def _show_success_message(self):
        """Muestra mensaje de éxito"""
        self.page.snack_bar = Error(
            f"Datos listos para análisis - Tipo: {self.type_dropdown.value}, Conjunto: {self.data_input.value}")
        self.page.snack_bar.open = True
        self.page.update()

    def _get_actions_for_type(self, measurement_type: str) -> list:
        """Devuelve las acciones correspondientes al tipo de medición"""
        common_actions = self.STANDARD_ACTIONS['common']

        if measurement_type == 'Acc':
            return common_actions + self.STANDARD_ACTIONS['acceleration']
        else:
            return common_actions
