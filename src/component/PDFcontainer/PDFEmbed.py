import flet as ft

class PDFEmbed(ft.Container):
    def __init__(self, pdf_url: str):
        super().__init__(
            expand=True,
            content=ft.WebView(
                url=pdf_url,
                width=800,
                height=600
            )
        )
