import flet as ft

from src.component.biomechanical_analysis_view import (
    SignalChartSection,
    AnalysisController)
from src.component.utils import time_inputs,ProcessButton
from src.component.biomechanical_analysis_view.result_card.resultCard import ResultCard
from src.error.Error import Error


class SignalAnalysisSection(ft.UserControl):
    def __init__(self, action_name):
        super().__init__()
        self.action_name = action_name
        self.time_inputs = time_inputs()
        self.analyze_button = ProcessButton(
            on_click=self.on_analyze_click,
            txt=f"Analizar {action_name}"
        )

        # Usar los nuevos componentes
        self.xyz_section = SignalChartSection("Componentes X, Y, Z", 3)
        self.jerk_section = SignalChartSection("Análisis de Jerk", 3)
        self.angle_section = SignalChartSection("Análisis de Ángulos", 2)

        self.result_card = ResultCard(f"Resultados de {action_name}")
        self.result_card.visible = False

        self.progress = ft.ProgressRing(
            width=24, height=24, visible=False,
            stroke_width=2, color=ft.colors.BLUE_600
        )

        self.controller = AnalysisController(self)

    def build(self):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    self.time_inputs,
                    self.analyze_button,
                    self.progress
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=16),

                self.xyz_section,
                self.jerk_section,
                self.angle_section,

                ft.Column([self.result_card], alignment=ft.MainAxisAlignment.CENTER)
            ], spacing=24, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=ft.Padding(24, 24, 24, 24),
            border_radius=12,
            border=ft.Border(
                bottom=ft.BorderSide(2, ft.colors.GREY_300),
                right=ft.BorderSide(1, ft.colors.GREY_300),
                left=ft.BorderSide(1, ft.colors.GREY_300),
                top=ft.BorderSide(1, ft.colors.GREY_300),
            )
        )

    def on_analyze_click(self, e):
        """Maneja el click del botón de análisis"""
        self.set_loading_state(True)
        self.controller.perform_analysis(
            self.time_inputs.controls[0].value,
            self.time_inputs.controls[1].value
        )

    def set_loading_state(self, loading: bool):
        """Establece el estado de carga"""
        self.progress.visible = loading
        self.analyze_button.disabled = loading
        self.update()

    def update_with_result(self, result):
        """Actualiza la vista con los resultados del análisis"""
        # Actualizar charts
        self.xyz_section.update_charts(result.get('gráficos', []))
        self.jerk_section.update_charts(result.get('graficos_Jerk', []))
        self.angle_section.update_charts(result.get('angulos_graficos', []))

        # Mostrar secciones
        self.xyz_section.visible = True
        self.jerk_section.visible = True
        self.angle_section.visible = True

        # Actualizar result card
        self.result_card.update_characteristics(result.get('características', {}))
        self.result_card.update_angles(result.get('angulos', {}))
        self.result_card.visible = True

        # Resetear UI
        self.set_loading_state(False)
        self.update_all()

    def show_error(self, message):
        """Muestra un mensaje de error"""
        self.page.snack_bar = Error(message)
        self.page.snack_bar.open = True
        self.set_loading_state(False)
        self.page.update()

    def update_all(self):
        """Actualiza todos los componentes"""
        self.xyz_section.update()
        self.jerk_section.update()
        self.angle_section.update()
        self.result_card.update()
        self.update()
