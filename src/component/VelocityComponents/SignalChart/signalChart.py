import base64
import io
import flet as ft


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
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK12)
        )

    def build(self):
        return self.clickable_image

    def plot_to_image(self, fig):
        try:
            import matplotlib.pyplot as plt

            fig.tight_layout()
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=100, bbox_inches='tight', pad_inches=0.1)
            buf.seek(0)

            img_base64 = base64.b64encode(buf.read()).decode('utf-8')
            buf.close()

            if self.page is not None:  # Asegúrate de que la página esté asignada
                self.image.src_base64 = img_base64
                self.dialog_image.src_base64 = img_base64
                self.update()

        except Exception as e:
            print(f"Error al convertir figura: {e}")
        finally:
            plt.close(fig)

    def update_image(self, pil_image):
        if pil_image:
            img_bytes = io.BytesIO()
            pil_image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            img_base64 = base64.b64encode(img_bytes.getvalue()).decode('utf-8')

            if self.page is not None:  # Asegúrate de que la página esté asignada
                self.image.src_base64 = img_base64
                self.dialog_image.src_base64 = img_base64
                self.update()

    def open_dialog(self, e):
        self.dialog.open = True
        self.page.dialog = self.dialog
        self.page.update()

    def close_dialog(self, e):
        self.dialog.open = False
        self.page.update()
