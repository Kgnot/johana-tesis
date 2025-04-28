import flet as ft

from src.component.text.GenericText import GenericText


class ResultCard(ft.UserControl):
    def __init__(self, title):
        super().__init__()
        self.title = title

        # Initialize components to display characteristics
        self.characteristics_tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[],
            expand=True
        )

        # Initialize table for angles
        self.angles_table = ft.DataTable(
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=8,
            vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_300),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_300),
            columns=[
                ft.DataColumn(GenericText("Ángulo", weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_900)),
                ft.DataColumn(GenericText("Mínimo", weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_900)),
                ft.DataColumn(GenericText("Máximo", weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_900)),
                ft.DataColumn(GenericText("Rango", weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_900))
            ],
            rows=[],
            heading_row_height=50,
            # data_row_height=45,
            heading_row_color=ft.colors.with_opacity(0.05, ft.colors.BLUE_GREY_800),
        )

    def build(self):
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.icons.ANALYTICS, color=ft.colors.BLUE_600),
                    GenericText(self.title, size=20, weight=ft.FontWeight.W_600, color=ft.colors.BLUE_GREY_700),
                ], spacing=10),
                ft.Divider(height=1, color=ft.colors.GREY_300),

                ft.Container(
                    content=ft.Column([
                        GenericText("Análisis de ángulos", weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_800),
                        self.angles_table
                    ], spacing=12),
                    padding=ft.Padding(0, 10, 0, 0)
                ),

                ft.Container(
                    content=ft.Column([
                        GenericText("Características por componente", weight=ft.FontWeight.W_500,
                                    color=ft.colors.BLUE_800),
                        self.characteristics_tabs
                    ], spacing=12),
                    padding=ft.Padding(0, 10, 0, 0)
                )
            ], spacing=16),
            padding=20,
            border_radius=12,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=12,
                color=ft.colors.with_opacity(0.15, ft.colors.GREY_800),
                offset=ft.Offset(0, 2)
            )
        )

    def update_angles(self, angles_df):
        """Actualiza la tabla de ángulos con los datos del DataFrame"""
        self.angles_table.rows.clear()
        print(f"Entre a resultCard y estos son los datos de la angulos petes: {angles_df}")

        if angles_df is None or angles_df.empty:
            return

        # Convert DataFrame to table rows
        try:
            for _, row in angles_df.iterrows():
                self.angles_table.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(GenericText(str(row['Ángulo']), weight=ft.FontWeight.W_500)),
                            ft.DataCell(GenericText(f"{row['Ángulo mínimo']:.4f}", color=ft.colors.BLUE_GREY_900)),
                            ft.DataCell(GenericText(f"{row['Ángulo máximo']:.4f}", color=ft.colors.BLUE_GREY_900)),
                            ft.DataCell(GenericText(f"{row['Rango']:.4f}", weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_900))
                        ],
                        on_select_changed=lambda e: self.highlight_row(e)
                    )
                )
        except Exception as e:
            print(f"Error al actualizar tabla de ángulos: {e}")

        # Update UI
        self.update()

    def highlight_row(self, e):
        """Highlight selected row when clicked (visual feedback)"""
        # This would need additional implementation for complete functionality
        pass

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

