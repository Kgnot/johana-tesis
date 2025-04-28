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
                label=f"Tiempo inicial para {action_name}",
                width=200,
                keyboard_type=ft.KeyboardType.NUMBER,
                suffix_text="seg"
            ),
            ft.TextField(
                label=f"Tiempo final para {action_name}",
                width=200,
                keyboard_type=ft.KeyboardType.NUMBER,
                suffix_text="seg"
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)

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
        self.chartsXYZ.visible = False
        self.chartsJerk.visible = False
        self.chartsAngle.visible = False
        # Progress indicator durante el análisis
        self.progress = ft.ProgressRing(width=20, height=20, visible=False)

    def build(self):
        self.clear_charts()
        return ft.Container(
            content=ft.Column([
                GenericText(f"Análisis de {self.action_name}", weight="bold", size=20),
                ft.Row([
                    self.time_inputs,
                    self.analyze_button,
                    self.progress
                ], alignment=ft.MainAxisAlignment.CENTER),
                self.chartsXYZ,
                self.chartsJerk,
                self.chartsAngle,
                self.result_card,
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            border_radius=10,
            border=ft.border.all(2, ft.colors.BLUE_200)
        )

    def on_analyze_click(self, e):
        try:
            # Mostrar progreso
            self.progress.visible = True
            self.analyze_button.disabled = True
            self.update()

            # Ejecutar análisis en un hilo separado para no bloquear la UI
            # threading.Thread(target=self.run_analysis, daemon=True).start()
            self.run_analysis()

        except Exception as ex:
            print(f"Error al iniciar análisis desde signal: {ex}")
            self.progress.visible = False
            self.analyze_button.disabled = False
            self.update()

    def run_analysis(self):
        # Validar inputs
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
        # Obtener datos segmentados
        result = segmul(
            med=self.page.data.get('med_type'),
            datosProcesar=int(self.page.data.get('datosProcesar')),
            Ti=ti,
            Tf=tf,
            accion=self.action_name
        )

        # limpiar graficos actuales
        self.clear_charts()

        # Actualizar gráficos XYZ
        chartsXYZ = result.get('gráficos', [])
        for i in range(min(len(chartsXYZ), 3)):
            self.chartsXYZ.controls[i].plot_to_image(chartsXYZ[i])
        # Actualizar gráficos Jerk
        chartsJerk = result.get('graficos_Jerk', [])
        for i in range(min(len(chartsJerk), 3)):
            self.chartsJerk.controls[i].plot_to_image(chartsJerk[i])
        # Actualizar gráficos de Ángulos
        chartsAngle = result.get('angulos_graficos', [])
        for i in range(min(len(chartsAngle), 2)):
            self.chartsAngle.controls[i].plot_to_image(chartsAngle[i])

        self.init_result_card(result.get('características'), result.get('angulos'))

        self.chartsXYZ.visible = True
        self.chartsJerk.visible = True
        self.chartsAngle.visible = True

        self.chartsXYZ.update()
        self.chartsJerk.update()
        self.chartsAngle.update()
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
        self.page.snack_bar = ft.SnackBar(content=ft.Text(message))
        self.page.snack_bar.open = True
        # self.reset_ui()

