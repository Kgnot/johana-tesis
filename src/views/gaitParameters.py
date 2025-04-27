import flet as ft

from src.component.text.GenericText import GenericText


class GaitParameters(ft.Component):
    def __init__(self):
        super().__init__(
            expand=True,
            padding=20,
            bgcolor="white",
            content = ft.Column(
                [
                    GenericText("Parametros de la marcha", size=28,weight="bold"),
                    GenericText(
                        "Aqui van los parametros de la marcha xd",
                        size=16
                    ),
                    GenericText(
                        "Vamos a mirar todo ",
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