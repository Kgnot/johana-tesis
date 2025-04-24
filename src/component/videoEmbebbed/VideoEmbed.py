import flet as ft

class VideoEmbed(ft.Container):
    def __init__(self, video_url: str):
        embed_url = video_url.replace("watch?v=", "embed/")  # Convierte la URL de YouTube a formato embed
        super().__init__(
            expand=True,
            content=ft.WebView(
                url=embed_url,
                width=800,
                height=450
            )
        )
