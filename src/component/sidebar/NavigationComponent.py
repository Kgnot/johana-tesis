import flet as ft

#es el componente es decir, el elemento que se elije
class NavigationComponent(ft.NavigationRailDestination):
    def __init__(self, icon, label):
        super().__init__(icon=ft.Icon(icon), label=label)
