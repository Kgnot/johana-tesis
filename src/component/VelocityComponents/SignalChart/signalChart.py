import base64
import io
from io import BytesIO

import flet as ft
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg



class SignalChart(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.image = ft.Image(
            width=400,
            height=300,
            fit=ft.ImageFit.CONTAIN
        )

    def build(self):
        return self.image

    def plot_to_image(self, fig):
        import io
        import base64

        buffer = io.BytesIO()
        fig.savefig(buffer, format="png")
        buffer.seek(0)
        img_bytes = buffer.read()
        buffer.close()

        self.image.src_base64 = base64.b64encode(img_bytes).decode("utf-8")
        self.image.update()

    def update_image(self, pil_image):
        """Actualiza la imagen del gráfico usando una imagen PIL"""
        if pil_image:
            # Convertir la imagen PIL a un formato que Flet pueda usar
            img_bytes = io.BytesIO()
            pil_image.save(img_bytes, format='PNG')
            img_bytes.seek(0)

            # Actualizar la imagen en la UI
            self.image.src_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')
            self.update()