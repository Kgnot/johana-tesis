import flet as ft
from .image_card import ImageCard
from src.component.utils import GenericText


class ImageGallery(ft.Column):
    def __init__(self):
        super().__init__(
            controls=[
                GenericText("Ejemplo de análisis visual de movimiento:", size=18),
                ft.Row(
                    [
                        ImageCard("/path/to/image1.jpg"),
                        ImageCard("/path/to/image2.jpg"),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                )
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
