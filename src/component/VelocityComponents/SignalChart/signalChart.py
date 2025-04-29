import base64
import io

import flet as ft


class SignalChart(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.image = ft.Image(
            width=400,
            height=300,
            fit=ft.ImageFit.CONTAIN,
            border_radius=ft.border_radius.all(8)
        )

    def build(self):
        return ft.Container(
            content=self.image,
            padding=10,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK12)
        )

    def plot_to_image(self, fig):
        """Convierte una figura matplotlib directamente a imagen para Flet"""
        try:
            import io
            import base64
            import matplotlib.pyplot as plt

            # Configuración para mejor calidad
            fig.tight_layout()

            # Convertir a PNG en memoria
            buf = io.BytesIO()
            fig.savefig(buf, format='png',
                        dpi=100,  # Ajusta según necesidad
                        bbox_inches='tight',
                        pad_inches=0.1)
            buf.seek(0)

            # Codificar como base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()

            # Actualizar la imagen
            self.image.src_base64 = img_base64
            self.update()

        except Exception as e:
            print(f"Error al convertir figura: {e}")
        finally:
            plt.close(fig)  # Cierra la figura para liberar memoria

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
