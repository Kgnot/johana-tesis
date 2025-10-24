import flet as ft


class ImageCard(ft.Container):
    def __init__(self, image_src: str, width: int = 350, height: int = 220):
        super().__init__(
            content=ft.Image(
                src=image_src,
                width=width,
                height=height,
                fit=ft.ImageFit.CONTAIN,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.border_radius.all(10),
            ),
            # bgcolor="#f3f3f3",
            # padding=10
        )
        # self.update()
