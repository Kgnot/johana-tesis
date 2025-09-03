import flet as ft

from src.component.utils import GenericText


class HomeHeader(ft.Column):
    def __init__(self):
        super().__init__(
            controls=[
                GenericText("Tesis en Bioingeniería", size=28, weight="bold"),
                GenericText(
                    "Este proyecto tiene como objetivo analizar el movimiento humano utilizando sensores "
                    "de aceleración y modelos biomecánicos avanzados. A través de este estudio, buscamos "
                    "comprender mejor la cinemática del cuerpo y desarrollar herramientas para mejorar "
                    "la rehabilitación y el rendimiento deportivo.",
                    size=16
                ),
                GenericText(
                    "Utilizamos software especializado para procesar los datos obtenidos de los sensores, "
                    "permitiendo la visualización de patrones de movimiento en distintas actividades. "
                    "Estos análisis pueden aplicarse en diversas áreas como la fisioterapia, la ergonomía "
                    "y el diseño de dispositivos médicos.",
                    size=16
                )
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
