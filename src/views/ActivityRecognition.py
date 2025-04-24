import flet as ft

from src.component.text.GenericText import GenericText


class ActivityRecognition(ft.Container):
    def __init__(self):
        super().__init__(
            expand=True,
            padding=20,
            bgcolor="white",
            content=ft.Column(
                [
                    GenericText("Reconocimiento de Actividades",weight="bold"),
                    GenericText(
                        "El reconocimiento de actividades permite diferenciar entre distintas acciones mediante datos "
                        "capturados en tiempo real.",
                        size=16
                    ),
                    ft.Image(src="/path/to/image5.jpg", width=400, height=250, fit=ft.ImageFit.COVER),
                    GenericText(
                        "A través de sensores, se pueden identificar patrones de movimiento específicos como caminar, correr "
                        "o estar en reposo.",
                        size=16
                    ),
                    ft.Row(
                        [
                            ft.Image(src="/path/to/image6.jpg", width=250, height=150, fit=ft.ImageFit.COVER),
                            ft.Image(src="/path/to/image7.jpg", width=250, height=150, fit=ft.ImageFit.COVER),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER
                    ),
                    GenericText(
                        "Esta tecnología tiene aplicaciones en salud, deportes y ergonomía laboral.",
                        size=16
                    )
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )
