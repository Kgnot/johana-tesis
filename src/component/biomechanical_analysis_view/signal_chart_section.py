from typing import cast
import flet as ft
from src.component.utils import (
    SignalChart,
    GenericText)


class SignalChartSection(ft.Container):
    def __init__(self, title: str, chart_count: int):
        self.charts = ft.Row([
            SignalChart() for _ in range(chart_count)
        ], wrap=True, alignment=ft.MainAxisAlignment.CENTER)

        super().__init__(
            content=ft.Column([
                GenericText(title, weight=ft.FontWeight.W_500,
                            color=ft.colors.BLUE_GREY_900, size=18),
                self.charts,
            ], spacing=12),
            visible=False
        )

    def update_charts(self, chart_data_list):
        """Actualiza los charts con nuevos datos"""
        for i in range(min(len(chart_data_list), len(self.charts.controls))):
            chart = cast(SignalChart, self.charts.controls[i])
            chart.plot_to_image(chart_data_list[i])

    def clear_charts(self):
        """Limpia todos los charts"""
        for chart in self.charts.controls:
            item = cast(SignalChart, chart)
            item.update_image(None)
