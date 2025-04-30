import flet as ft


def Error(text):
    return ft.SnackBar(
        content=ft.Text(
            text,
            color=ft.colors.WHITE
        ),
        bgcolor=ft.colors.AMBER_400,
    )
