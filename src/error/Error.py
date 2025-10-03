import flet as ft


def Error(text):
    return ft.SnackBar(
        content=ft.Text(
            text,
            color=ft.Colors.WHITE
        ),
        bgcolor=ft.Colors.AMBER_400,
    )
