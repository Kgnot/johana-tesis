import flet as ft

from src.component.text.GenericText import GenericText


class VelocityView(ft.Container):
    def __init__(self):
        super().__init__(
            expand=True,
            padding=20,
            bgcolor="white",
            content=ft.Column(
                [
                    GenericText("Estudio de Velocidades",weight="bold"),
                    GenericText(
                        "El estudio de la velocidad en el movimiento humano es crucial para la evaluación de desempeño "
                        "y la prevención de lesiones.",
                        size=16
                    ),
                    ft.Row(
                        [
                            ft.Image(src="/path/to/image4.jpg", width=300, height=200, fit=ft.ImageFit.COVER),
                            ft.Container(
                                content=GenericText(
                                    "Comparando distintas velocidades a lo largo de una actividad, se pueden detectar "
                                    "anomalías o mejoras en la técnica de una persona.",
                                    size=16
                                ),
                                padding=10
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    GenericText(
                        "Los datos obtenidos ayudan a construir modelos predictivos y a mejorar la eficiencia del movimiento.",
                        size=16
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )