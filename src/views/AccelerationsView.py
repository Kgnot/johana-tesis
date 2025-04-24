import flet as ft

from src.component.text.GenericText import GenericText


class AccelerationsView(ft.Container):
    def __init__(self):
        super().__init__(
            expand=True,
            padding=20,
            bgcolor="white",
            content=ft.Column(
                [
                    GenericText("Análisis de Aceleraciones",weight="bold"),
                    ft.Image(src="/path/to/image1.jpg", width=400, height=250, fit=ft.ImageFit.COVER),
                    GenericText(
                        "El análisis de aceleraciones permite comprender mejor el movimiento en diversas actividades, "
                        "lo cual es fundamental en estudios biomecánicos y de rendimiento deportivo.",
                        size=16
                    ),
                    GenericText(
                        "Al examinar los cambios de velocidad en el tiempo, se pueden identificar patrones clave en "
                        "la marcha humana y en otras actividades físicas.",
                        size=16
                    ),
                    ft.Row(
                        [
                            ft.Image(src="/path/to/image2.jpg", width=250, height=150, fit=ft.ImageFit.COVER),
                            ft.Image(src="/path/to/image3.jpg", width=250, height=150, fit=ft.ImageFit.COVER),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )