import threading
import flet as ft
from logic.codigo_completo.exportacion_codigo_completo import segmul
from src.component.VelocityComponents.ResultCard.resultCard import ResultCard
from src.component.VelocityComponents.SignalChart.signalChart import SignalChart
from src.component.VelocityComponents.processButton.ProcessButton import ProcessButton
from src.component.text.GenericText import GenericText


class SignalAnalysisSection(ft.UserControl):
    def __init__(self, action_name):
        super().__init__()
        self.action_name = action_name

        self.time_inputs = ft.Row([
            ft.TextField(
                label=f"Tiempo inicial",
                width=180,
                keyboard_type=ft.KeyboardType.NUMBER,
                suffix_text="seg",
                border_radius=8,
                filled=True,
                bgcolor=ft.colors.with_opacity(0.04, ft.colors.BLACK),
                hint_text="0.0"
            ),
            ft.TextField(
                label=f"Tiempo final",
                width=180,
                keyboard_type=ft.KeyboardType.NUMBER,
                suffix_text="seg",
                border_radius=8,
                filled=True,
                bgcolor=ft.colors.with_opacity(0.04, ft.colors.BLACK),
                hint_text="0.0"
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)

        self.analyze_button = ProcessButton(
            on_click=self.on_analyze_click,
            txt=f"Analizar {action_name}"
        )

        self.chartsXYZ = ft.Row([
            SignalChart() for _ in range(3)  # X, Y, Z charts
        ], wrap=True, alignment=ft.MainAxisAlignment.CENTER)
        self.chartsJerk = ft.Row([
            SignalChart() for _ in range(3)
        ], wrap=True, alignment=ft.MainAxisAlignment.CENTER)
        self.chartsAngle = ft.Row([
            SignalChart() for _ in range(2)  # X y Y
        ], wrap=True, alignment=ft.MainAxisAlignment.CENTER)
        # Aqui los resultcard:
        self.result_card = ResultCard(f"Resultados de {action_name} ")
        self.result_card.visible = False
        self.chartsXYZ.visible = True
        self.chartsJerk.visible = False
        self.chartsAngle.visible = False

        ## Aqui iran los contenedores:
        self.chartsXYZ_container = ft.Container(
            content=ft.Column([
                GenericText("Componentes X, Y, Z", weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_900, size=18),
                self.chartsXYZ,
            ], spacing=12),
        )
        self.chartsJerk_container = ft.Container(
            content=ft.Column([
                GenericText("Análisis Jerk", weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_900, size=18),
                self.chartsJerk,
            ], spacing=12),
        )
        self.chartsAngle_container = ft.Container(
            content=ft.Column([
                GenericText("Análisis de Ángulos", weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_900, size=18),
                self.chartsAngle,
            ], spacing=12),
        )
        self.chartsXYZ_container.visible = False
        self.chartsJerk_container.visible = False
        self.chartsAngle_container.visible = False
        # Progress indicator during analysis
        self.progress = ft.ProgressRing(
            width=24,
            height=24,
            visible=False,
            stroke_width=2,
            color=ft.colors.BLUE_600
        )

    def build(self):
        self.clear_charts()
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    self.time_inputs,
                    self.analyze_button,
                    self.progress
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=16),

                # Charts sections with labels
                self.chartsXYZ_container,
                self.chartsJerk_container,
                self.chartsAngle_container,
                self.result_card,
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
        try:
            # Show progress
            self.progress.visible = True
            self.analyze_button.disabled = True
            self.update()

            # Run analysis in a separate thread to avoid UI blocking
            # threading.Thread(target=self.run_analysis, daemon=True).start()
            self.run_analysis()

        except Exception as ex:
            print(f"Error al iniciar análisis desde signal: {ex} ")
            self.progress.visible = False
            self.analyze_button.disabled = False
            self.update()

    def run_analysis(self):
        # Validate inputs
        ti_str = self.time_inputs.controls[0].value
        tf_str = self.time_inputs.controls[1].value

        if not ti_str or not tf_str:
            self.show_error("Ingrese tiempos válidos.")
            return

        if 'med_type' not in self.page.data or 'datosProcesar' not in self.page.data:
            self.show_error("Datos de análisis no disponibles.")
            return

        ti = float(ti_str)
        tf = float(tf_str)
        # Get segmented data
        result = segmul(
            med=self.page.data.get('med_type'),
            datosProcesar=int(self.page.data.get('datosProcesar')),
            Ti=ti,
            Tf=tf,
            accion=self.action_name
        )

        # Clear current charts
        self.clear_charts()

        # Update XYZ charts
        chartsXYZ = result.get('gráficos', [])
        for i in range(min(len(chartsXYZ), 3)):
            self.chartsXYZ.controls[i].plot_to_image(chartsXYZ[i])

        # Update Jerk charts
        chartsJerk = result.get('graficos_Jerk', [])
        for i in range(min(len(chartsJerk), 3)):
            self.chartsJerk.controls[i].plot_to_image(chartsJerk[i])

        # Update Angle charts
        chartsAngle = result.get('angulos_graficos', [])
        for i in range(min(len(chartsAngle), 2)):
            self.chartsAngle.controls[i].plot_to_image(chartsAngle[i])

        self.init_result_card(result.get('características'), result.get('angulos'))

        self.chartsXYZ_container.visible = True
        self.chartsJerk_container.visible = True
        self.chartsAngle_container.visible = True

        self.chartsXYZ.visible = True
        self.chartsJerk.visible = True
        self.chartsAngle.visible = True

        self.chartsXYZ.update()
        self.chartsJerk.update()
        self.chartsAngle.update()
        self.chartsXYZ_container.update()
        self.chartsJerk_container.update()
        self.chartsAngle_container.update()
        self.page.update()
        self.reset_ui()

    def clear_charts(self):
        for chart in self.chartsXYZ.controls:
            chart.update_image(None)
        for chart in self.chartsJerk.controls:
            chart.update_image(None)
        for chart in self.chartsAngle.controls:
            chart.update_image(None)

    def init_result_card(self, characteristics, angles):
        # self.result_card.update_characteristics(characteristics)
        self.result_card.update_angles(angles)
        print(f" Caracteristicas: {characteristics} \n Angles: {angles}")
        self.result_card.visible = True
        self.result_card.update()
        self.reset_ui()

    def reset_ui(self):
        print("entre a reset ui de signalAnalysis")
        self.progress.visible = False
        self.analyze_button.disabled = False
        self.analyze_button.update()
        self.update()
        self.page.update()

    def show_error(self, message):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(message, color=ft.colors.WHITE),
            bgcolor=ft.colors.RED_600,
            action=ft.SnackBarAction("OK", lambda e: setattr(self.page.snack_bar, "open", False))
        )
        self.page.snack_bar.open = True
        self.page.update()
        self.reset_ui()
