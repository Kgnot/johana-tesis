import flet as ft

#es el componente es decir, el elemento que se elije
class NavigationComponent(ft.NavigationRailDestination):
    def __init__(self, icon, label):
        super().__init__(
            icon=ft.Icon(icon),
            label_content=ft.Text(
                label,
                text_align=ft.TextAlign.CENTER,
                size=12,
                weight=ft.FontWeight.W_500
            )
        )