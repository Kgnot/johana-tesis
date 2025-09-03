import flet as ft


class BlueProgressRing(ft.ProgressRing):
    def __init__(self):
        super().__init__(
            width=24,
            height=24,
            visible=False,
            stroke_width=2,
            color=ft.colors.BLUE_600
        )
