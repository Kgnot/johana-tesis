import flet as ft
from src.component.sidebar.NavigationComponent import NavigationComponent


#Esta es una clase que es el compomente de navegacion de python .
class NavigationBar(ft.NavigationRail):
    #Se inicializa con super y una función cuyo nombre es on_change
    def __init__(self, on_change,color="white"):
        super().__init__(
            #el index es el elemento a elegir
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            #group_alignment=-0.9,
            bgcolor="#ffffff",
            expand=True, # se expande en el componente que hace parte
            #las diferentes destinos de cada uno y sus nombres con sus iconos :D
            destinations=[
                NavigationComponent(ft.icons.RECORD_VOICE_OVER, "Inicio"),  # Icono de voz para la prueba
                NavigationComponent(ft.icons.TRENDING_UP, "Estudio de señales"),  # Representa incremento de velocidad
                NavigationComponent(ft.icons.ACCESSIBLE_ROUNDED,"Parametros de la marcha"),
                NavigationComponent(ft.icons.RUN_CIRCLE, "Reconocimiento/Actividades"),
                NavigationComponent(ft.icons.MENU_BOOK, "Manual"),  # Representa un manual o documentación
                NavigationComponent(ft.icons.MODEL_TRAINING, "Modelo"),  # Representa el modelo en entrenamiento
            ],
            on_change=on_change
        )
