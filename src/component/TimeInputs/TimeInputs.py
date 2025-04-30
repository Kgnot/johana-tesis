import flet as ft


def timeImputs():
    return ft.Row([
        ft.TextField(
            label=f"Tiempo inicial",
            width=180,
            keyboard_type=ft.KeyboardType.NUMBER,
            suffix_text="seg",
            border_radius=8,
            filled=True,
            bgcolor=ft.colors.with_opacity(0.04, ft.colors.BLACK),
            hint_text="0.0"
        ),
        ft.TextField(
            label=f"Tiempo final",
            width=180,
            keyboard_type=ft.KeyboardType.NUMBER,
            suffix_text="seg",
            border_radius=8,
            filled=True,
            bgcolor=ft.colors.with_opacity(0.04, ft.colors.BLACK),
            hint_text="0.0"
        ),
    ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
