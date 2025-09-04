import flet as ft

from logic.recon.ReconocimientoActividades import wavelet
from src.component.utils import (
    SignalChart,
    GenericText)


class ResultActivityRecognition(ft.Container):
    def __init__(self):
        super().__init__()
        # Primero creamos los gráficos base
        self.chartICA_ac = ft.Row([
            SignalChart() for _ in range(3)
        ], wrap=True, alignment=ft.MainAxisAlignment.CENTER)
        self.chartICA_vel = ft.Row([
            SignalChart() for _ in range(3)
        ], wrap=True, alignment=ft.MainAxisAlignment.CENTER)
        self.chartREC_ac = ft.Row([
            SignalChart() for _ in range(3)
        ], wrap=True, alignment=ft.MainAxisAlignment.CENTER)
        self.chartREC_vel = ft.Row([
            SignalChart() for _ in range(3)
        ], wrap=True, alignment=ft.MainAxisAlignment.CENTER)

        # Ahora los contenedores:
        self.ChartICA_ac_Container = ft.Column([
            GenericText("Gráficos de aceleración ICA", size=20),
            self.chartICA_ac
        ])
        self.ChartICA_vel_Container = ft.Column([
            GenericText("Gráficos de velocidad ICA", size=20),
            self.chartICA_vel
        ])
        self.ChartREC_ac_Container = ft.Column([
            GenericText("Reconstrucción aceleración", size=20),
            self.chartREC_ac
        ])
        self.ChartREC_vel_Container = ft.Column([
            GenericText("Reconstrucción velocidad", size=20),
            self.chartREC_vel
        ])

        # Finalmente, construimos el contenido
        self.content = self.build()
        self.content.alignment = ft.MainAxisAlignment.CENTER
        self.content.scroll = ft.ScrollMode.AUTO
        self.content.expand = True
        self.content.wrap = True
        self.content.spacing = 20
        self.content.run_spacing = 20

    def build(self):
        return ft.Column([
            self.ChartICA_ac_Container,
            self.ChartICA_vel_Container,
            self.ChartREC_ac_Container,
            self.ChartREC_vel_Container
        ])

    def init_charts(self):
        if 'med_type_recognition' not in self.page.data:
            print("Datos de análisis no disponibles.")
            return

        self.clear_charts()
        response_wavelet = wavelet(int(self.page.data['med_type_recognition']))

        chartICA_ac = response_wavelet.get('graficos_ica_ac', [])
        chartICA_vel = response_wavelet.get('graficos_ica_vel', [])
        chartREC_ac = response_wavelet.get('graficos_reconstruccion_ac', [])
        chartREC_vel = response_wavelet.get('graficos_reconstruccion_vel', [])

        # Asignamos los gráficos a los SignalChart correspondientes
        for i in range(min(len(chartICA_ac), 3)):
            self.chartICA_ac.controls[i].plot_to_image(chartICA_ac[i])

        for i in range(min(len(chartICA_vel), 3)):
            self.chartICA_vel.controls[i].plot_to_image(chartICA_vel[i])

        for i in range(min(len(chartREC_ac), 3)):
            self.chartREC_ac.controls[i].plot_to_image(chartREC_ac[i])

        for i in range(min(len(chartREC_vel), 3)):
            self.chartREC_vel.controls[i].plot_to_image(chartREC_vel[i])

    def clear_charts(self):
        for chart in self.chartICA_ac.controls:
            chart.update_image(None)
        for chart in self.chartICA_vel.controls:
            chart.update_image(None)
        for chart in self.chartREC_vel.controls:
            chart.update_image(None)
        for chart in self.chartREC_ac.controls:
            chart.update_image(None)
