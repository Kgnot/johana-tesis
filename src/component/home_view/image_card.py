import flet as ft

class ImageCard(ft.Container):
    def __init__(self, image_src: str, width: int = 350, height: int = 220):
        super().__init__(
            content=ft.Image(
                src=image_src
                width=width,
                height=height,
                fit=ft.ImageFit.COVER
            ),
            border_radius=10,
            bgcolor="#f2f2f2",
            padding=10
        )
