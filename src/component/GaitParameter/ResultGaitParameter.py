import flet as ft
from flet.core.alignment import Alignment
from flet.core.scrollable_control import OnScrollEvent
from flet.core.types import ScrollMode

from logic.parametros_marcha.ParametrosMarcha import marcha
from src.component.SignalChart.signalChart import SignalChart
from src.component.text.GenericText import GenericText


class ResultGaitParameter(ft.Container):
    def __init__(self):
        # Gráficas
        self.chart_senial_normalizada = SignalChart()
        self.chart_velocidad = SignalChart()
        self.chart_distancia = SignalChart()

        # Filas con texto + imagen
        self.content_senial_normalizada = ft.Column([
            GenericText("Señal normalizada: ", 22),
            self.chart_senial_normalizada
        ], alignment=ft.MainAxisAlignment.CENTER, expand=True)

        self.content_velocidad = ft.Column([
            GenericText("Velocidad: ", 22),
            self.chart_velocidad
        ], alignment=ft.MainAxisAlignment.CENTER, expand=True)

        self.content_distancia = ft.Column([
            GenericText("Distancia: ", 22),
            self.chart_distancia
        ], alignment=ft.MainAxisAlignment.CENTER, expand=True)

        # Contenedor para los datos tabulares
        self.data_table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Características")),
                ft.DataColumn(ft.Text("Persona"))
            ],
            rows=[]
        )

        self.table_container = ft.Container(
            content=self.data_table,
            padding=10,
            margin=ft.margin.only(top=20),
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(blur_radius=2, color=ft.colors.BLACK12)
        )

        # Llamada al constructor padre con content ya definido
        super().__init__(
            content=self.build(),
            alignment=ft.alignment.center,
            expand=True,
            padding=20
        )

    def build(self):
        return ft.Column(
            controls=[
                ft.Text("Parámetros de la Marcha", size=24, weight=ft.FontWeight.BOLD),
                ft.Row(
                    [
                        self.content_senial_normalizada,
                        self.content_velocidad,
                        self.content_distancia,
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.CENTER

                ),

                self.table_container
            ],
            scroll=ft.ScrollMode.AUTO,
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            expand=True
        )

    def init_charts(self, dato_procesar, Ti, Tf):
        # Limpiar gráficas antes de iniciar
        self.clear_charts()

        # Mostrar un indicador de carga (opcional)
        # self.update() si quieres actualizar la UI antes de procesar

        try:
            # Obtener los datos de marcha
            response_marcha = marcha(dato_procesar, Ti, Tf)

            if not response_marcha:
                print("No se pudo obtener marcha.")
                return False

            # Verificar que todas las gráficas estén presentes
            required_keys = ['grafica_normalizada', 'grafica_velocidad', 'grafica_distancia']
            if not all(key in response_marcha for key in required_keys):
                print(f"Faltan gráficas en la respuesta: {[k for k in required_keys if k not in response_marcha]}")
                return False

            # Asignar las gráficas a los componentes
            self.chart_senial_normalizada.plot_to_image(response_marcha['grafica_normalizada'])
            self.chart_velocidad.plot_to_image(response_marcha['grafica_velocidad'])
            self.chart_distancia.plot_to_image(response_marcha['grafica_distancia'])

            # Actualizar la tabla de datos
            if 'data' in response_marcha and 'headers' in response_marcha:
                self.update_data_table(response_marcha['headers'], response_marcha['data'])

            # Actualizar UI
            self.update()
            return True

        except Exception as e:
            print(f"Error al inicializar gráficas: {e}")
            import traceback
            traceback.print_exc()
            return False

    def update_data_table(self, headers, data):
        # Limpiar filas existentes
        self.data_table.rows.clear()

        # Actualizar encabezados si es necesario
        if len(self.data_table.columns) != len(headers):
            self.data_table.columns = [ft.DataColumn(ft.Text(h)) for h in headers]

        # Llenar con nuevos datos
        for row_data in data:
            self.data_table.rows.append(
                ft.DataRow(
                    cells=[ft.DataCell(ft.Text(str(cell))) for cell in row_data]
                )
            )

    def clear_charts(self):
        self.chart_senial_normalizada.update_image(None)
        self.chart_velocidad.update_image(None)
        self.chart_distancia.update_image(None)
        self.data_table.rows.clear()
        self.update()
