import flet as ft
from src.app.model_app import ModelApp

def main(page: ft.Page):
    app = ModelApp(page)   # cada usuario tiene SU instancia de ModelApp
    app.run()

# Arranque web
if __name__ == "__main__":
    ft.app(target=main, port=9000, view=ft.WEB_BROWSER, assets_dir="assets")
