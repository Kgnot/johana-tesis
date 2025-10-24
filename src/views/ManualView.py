import flet as ft

from src.component.utils import (
    PDFEmbed,
    GenericText,
    VideoEmbed)


class ManualView(ft.Container):
    def __init__(self, pdf_url, video_url):
        super().__init__(
            expand=True,
            padding=20,
            bgcolor="white",
            content=
            ft.Column(
                [
                    GenericText("Manual de Usuario", weight="bold"),
                    ft.Divider(),
                    ft.Row([
                        PDFEmbed(pdf_url),
                        # VideoEmbed(video_url) 
                    ])
                ],
                alignment=ft.MainAxisAlignment.START,  # Lo hace al inicio
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,  # lo ubica central
                spacing=20,  # El gap o espacio entre componentes
                scroll=ft.ScrollMode.AUTO  # scrolling

            )
        )
