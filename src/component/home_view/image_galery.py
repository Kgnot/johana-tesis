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
                        ImageCard("https://moto-tiles.com/site_pr/img_pr/03.jpg"),
                        ImageCard("https://ars.els-cdn.com/content/image/1-s2.0-S0196070924003223-gr1.jpg")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20
                )
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
