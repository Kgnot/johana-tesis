import flet as ft

from src.component.text.GenericText import GenericText


class ResultCard(ft.UserControl):
    def __init__(self, title):
        super().__init__()
        self.title = title

        # Inicializar componentes para mostrar características
        self.characteristics_tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[],
            expand=True
        )

        # Inicializar tabla para ángulos
        self.angles_table = ft.DataTable(
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
            columns=[
                ft.DataColumn(GenericText("Ángulo")),
                ft.DataColumn(GenericText("Mínimo")),
                ft.DataColumn(GenericText("Máximo")),
                ft.DataColumn(GenericText("Rango"))
            ],
            rows=[]
        )

    def build(self):
        return ft.Card(
            content=ft.Container(
                content=ft.Column([
                    GenericText(self.title, size=20, weight=ft.FontWeight.BOLD),
                    ft.Divider(),
                    GenericText("Características por componente:", weight=ft.FontWeight.BOLD),
                    self.characteristics_tabs,
                    ft.Divider(),
                    GenericText("Análisis de ángulos:", weight=ft.FontWeight.BOLD),
                    self.angles_table
                ], spacing=10),
                padding=20
            ),
            elevation=4
        )

    def update_characteristics(self, characteristics_data):
        self.characteristics_tabs.tabs.clear()
        print(f"Entre a resultCard y estos son los datos de la caracteristicas: {characteristics_data}")
        if not characteristics_data:
            return

        # Verificar si los datos son para múltiples componentes (X, Y, Z)
        is_multi_component = isinstance(characteristics_data[0], list) and isinstance(characteristics_data[0][0], list)

        if is_multi_component:
            # Datos para múltiples componentes (X, Y, Z)
            labels = ['Componente X', 'Componente Y', 'Componente Z']

            for i, component_data in enumerate(characteristics_data):
                if i >= len(labels):
                    break

                # Crear tabla para este componente
                table = ft.DataTable(
                    border=ft.border.all(1, ft.colors.GREY_400),
                    border_radius=10,
                    vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
                    horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
                    columns=[
                        ft.DataColumn(GenericText("Característica")),
                        ft.DataColumn(GenericText("Valor"))
                    ],
                    rows=[]
                )

                # Añadir filas a la tabla
                for feature, value in component_data:
                    try:
                        formatted_value = f"{float(value):.4f}"
                    except (ValueError, TypeError):
                        formatted_value = str(value)

                    table.rows.append(
                        ft.DataRow(cells=[
                            ft.DataCell(GenericText(feature)),
                            ft.DataCell(GenericText(formatted_value))
                        ])
                    )

                # Añadir pestaña para este componente
                self.characteristics_tabs.tabs.append(
                    ft.Tab(
                        text=labels[i],
                        content=ft.Container(
                            content=table,
                            padding=10
                        )
                    )
                )
        else:
            # Datos para un solo componente (formato antiguo)
            table = ft.DataTable(
                border=ft.border.all(1, ft.colors.GREY_400),
                border_radius=10,
                vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
                horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
                columns=[
                    ft.DataColumn(GenericText("Característica")),
                    ft.DataColumn(GenericText("Valor"))
                ],
                rows=[]
            )

            for feature, value in characteristics_data:
                try:
                    formatted_value = f"{float(value):.4f}"
                except (ValueError, TypeError):
                    formatted_value = str(value)

                table.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(GenericText(feature)),
                        ft.DataCell(GenericText(formatted_value))
                    ])
                )

            self.characteristics_tabs.tabs.append(
                ft.Tab(
                    text="Características",
                    content=ft.Container(
                        content=table,
                        padding=10
                    )
                )
            )

        self.update()

    def update_angles(self, angles_df):
        """Actualiza la tabla de ángulos con los datos del DataFrame"""
        self.angles_table.rows.clear()
        print(f"Entre a resultCard y estos son los datos de la angulos petes: {angles_df}")

        if angles_df is None or angles_df.empty:
            return

        # Convertir DataFrame a filas de la tabla
        try:
            for _, row in angles_df.iterrows():
                self.angles_table.rows.append(
                    ft.DataRow(cells=[
                        ft.DataCell(GenericText(str(row['Ángulo']))),
                        ft.DataCell(GenericText(f"{row['Ángulo mínimo']:.4f}")),
                        ft.DataCell(GenericText(f"{row['Ángulo máximo']:.4f}")),
                        ft.DataCell(GenericText(f"{row['Rango']:.4f}"))
                    ])
                )
        except Exception as e:
            print(f"Error al actualizar tabla de ángulos: {e}")

        # Actualizar UI
        self.update()