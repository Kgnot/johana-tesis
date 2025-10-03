import flet as ft
import io
import base64
import matplotlib.pyplot as plt



class SignalChart(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.dialog_image = ft.Image(
            width=650,
            height=550,
            fit=ft.ImageFit.CONTAIN
        )
        self.dialog = ft.AlertDialog(
            modal=True,
            content=self.dialog_image,
            actions=[ft.TextButton("Cerrar", on_click=self.close_dialog)],
            actions_alignment=ft.MainAxisAlignment.END
        )
        self.image = ft.Image(
            width=400,
            height=300,
            fit=ft.ImageFit.CONTAIN,
            border_radius=ft.border_radius.all(8)
        )
        self.clickable_image = ft.Container(
            content=self.image,
            on_click=self.open_dialog,
            border_radius=10,
            padding=10,
            bgcolor=ft.Colors.WHITE,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.BLACK12)
        )

    def build(self):
        return self.clickable_image

    def plot_to_image(self, fig):
        try:
            # Asegúrate de que la figura tenga un layout ajustado
            fig.tight_layout()

            # Guarda la figura en un buffer de bytes
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', pad_inches=0.1)
            buf.seek(0)

            # Convierte los bytes a base64
            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()

            # Actualiza las imágenes si la página está disponible
            if hasattr(self, 'page') and self.page is not None:
                self.image.src_base64 = img_base64
                self.dialog_image.src_base64 = img_base64
                self.update()

            return True
        except Exception as e:
            print(f"Error al convertir figura: {e}")
            return False
        finally:
            plt.close(fig)  # Asegúrate de cerrar la figura para liberar memoria

    def update_image(self, img_source):
        if img_source is None:
            # Limpiar la imagen
            if hasattr(self, 'page') and self.page is not None:
                self.image.src_base64 = None
                self.dialog_image.src_base64 = None
                self.update()
            return None

        # Si es una figura de matplotlib
        if hasattr(img_source, 'savefig'):
            return self.plot_to_image(img_source)

        # Si es una imagen PIL
        try:
            img_bytes = io.BytesIO()
            img_source.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

            if hasattr(self, 'page') and self.page is not None:
                self.image.src_base64 = img_base64
                self.dialog_image.src_base64 = img_base64
                self.update()
            return True
        except Exception as e:
            print(f"Error al actualizar imagen: {e}")
            return False

    def open_dialog(self, e):
        if hasattr(self, 'page') and self.page is not None:
            self.dialog.open = True
            self.page.dialog = self.dialog
            self.page.update()

    def close_dialog(self, e):
        self.dialog.open = False
        self.page.update()