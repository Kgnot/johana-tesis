import flet as ft

from src.component.home_view import HomeHeader, ImageGallery


class HomeView(ft.Container):
    def __init__(self):
        super().__init__(
            expand=True,
            padding=20,
            bgcolor="white",
            content=ft.Column(
                [
                    HomeHeader(),
                    ft.Divider(),
                    ImageGallery()
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20
            )
        )
