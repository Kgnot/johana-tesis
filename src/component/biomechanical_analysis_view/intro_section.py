import flet as ft
from src.component.utils import GenericText


def _create_icon_row() -> ft.Row:
    return ft.Row([
        ft.Icon(ft.Icons.ANALYTICS, size=60, color=ft.Colors.GREY_700),
        ft.Container(
            content=GenericText(
                "Compare distintas fases del movimiento para detectar anomalías o evaluar mejoras.",
                size=16,
                color=ft.Colors.GREY_700
            ),
            padding=10,
            width=500
        )
    ], alignment=ft.MainAxisAlignment.CENTER)


def _create_configuration_card(configuration_row: ft.Row) -> ft.Container:
    return ft.Container(
        content=ft.Column([
            GenericText("Configuración de análisis",
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_GREY_900),
            configuration_row,
        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding(20, 20, 20, 20),
        border_radius=10,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=15,
            color=ft.Colors.with_opacity(0.2, ft.Colors.BLUE_GREY_900),
            offset=ft.Offset(0, 4)
        )
    )


class IntroSection(ft.Column):
    def __init__(self, configuration_row: ft.Row):
        super().__init__(
            controls=[
                GenericText("Estudio de Señales Biomecánicas",
                            weight=ft.FontWeight.BOLD,
                            size=28),
                GenericText(
                    "Analice datos de aceleración y velocidad para comprender patrones de movimiento.",
                    size=16,
                    color=ft.Colors.GREY_700
                ),
                _create_icon_row(),
                _create_configuration_card(configuration_row)
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20
        )

