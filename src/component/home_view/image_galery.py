import flet as ft
from .image_card import ImageCard
from src.component.utils import GenericText


class ImageGallery(ft.Column):
    def __init__(self):
        super().__init__(
            controls=[
                GenericText("Ejemplo de análisis visual de movimiento:", size=20, weight=ft.FontWeight.W_100),
                ft.Column(
                    [
                        ImageCard("/img/iTUG.jpg",400,300),
                        ImageCard("/img/mototiles.jpg",400,300)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                )
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
