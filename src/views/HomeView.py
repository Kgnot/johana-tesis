import flet as ft

from src.component.text.GenericText import GenericText


class HomeView(ft.Container):
    def __init__(self):
        super().__init__(
            expand=True,
            padding=20,
            bgcolor="white",
            content=ft.Column(
                [
                    GenericText("Tesis en Bioingeniería", size=28,weight="bold"),
                    GenericText(
                        "Este proyecto tiene como objetivo analizar el movimiento humano utilizando sensores "
                        "de aceleración y modelos biomecánicos avanzados. A través de este estudio, buscamos "
                        "comprender mejor la cinemática del cuerpo y desarrollar herramientas para mejorar "
                        "la rehabilitación y el rendimiento deportivo.",
                        size=16
                    ),
                    GenericText(
                        "Utilizamos software especializado para procesar los datos obtenidos de los sensores, "
                        "permitiendo la visualización de patrones de movimiento en distintas actividades. "
                        "Estos análisis pueden aplicarse en diversas áreas como la fisioterapia, la ergonomía "
                        "y el diseño de dispositivos médicos.",
                        size=16
                    ),
                    ft.Divider(),
                    GenericText("Ejemplo de análisis visual de movimiento:", size=18),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Image(src="/path/to/image1.jpg", width=350, height=220, fit=ft.ImageFit.COVER),
                                border_radius=10,
                                bgcolor="#f2f2f2",
                                padding=10
                            ),
                            ft.Container(
                                content=ft.Image(src="/path/to/image2.jpg", width=350, height=220, fit=ft.ImageFit.COVER),
                                border_radius=10,
                                bgcolor="#f2f2f2",
                                padding=10
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )
