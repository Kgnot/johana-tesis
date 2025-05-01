import flet as ft

from src.component.text.GenericText import GenericText


class ResultCard(ft.UserControl):
    def __init__(self, title):
        super().__init__()
        self.title = title

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

        # Initialize tables for characteristics (one for each component)
        self.characteristics_tables = {
            "X": self._create_characteristics_table("X"),
            "Y": self._create_characteristics_table("Y"),
            "Z": self._create_characteristics_table("Z")
        }

    def _create_characteristics_table(self, component):
        """Crea una tabla de características para un componente específico"""
        return ft.DataTable(
            border=ft.border.all(1, ft.colors.GREY_300),
            border_radius=8,
            vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_300),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_300),
            columns=[
                ft.DataColumn(GenericText("Característica", weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_900)),
                ft.DataColumn(GenericText("Valor", weight=ft.FontWeight.W_500, color=ft.colors.BLUE_GREY_900)),
            ],
            rows=[],
            heading_row_height=40,
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

                ft.Divider(height=1, color=ft.colors.GREY_300),
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Column([
                                GenericText("Características - Componente X", weight=ft.FontWeight.W_500,
                                            color=ft.colors.BLUE_800),
                                self.characteristics_tables["X"]
                            ], spacing=12),
                            padding=ft.Padding(0, 10, 0, 0)
                        ),
                        # Componente Y
                        ft.Container(
                            content=ft.Column([
                                GenericText("Características - Componente Y", weight=ft.FontWeight.W_500,
                                            color=ft.colors.BLUE_800),
                                self.characteristics_tables["Y"]
                            ], spacing=12),
                            padding=ft.Padding(0, 10, 0, 0)
                        ),

                        # Componente Z
                        ft.Container(
                            content=ft.Column([
                                GenericText("Características - Componente Z", weight=ft.FontWeight.W_500,
                                            color=ft.colors.BLUE_800),
                                self.characteristics_tables["Z"]
                            ], spacing=12),
                            padding=ft.Padding(0, 10, 0, 0)
                        )
                    ],
                        wrap=True
                    )
                ),
                # Componente X

            ], spacing=16, scroll=ft.ScrollMode.AUTO),
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

    def update_characteristics(self, total_data):
        # Nombres de componentes
        component_names = ["X", "Y", "Z"]

        # Actualizar cada tabla de componentes
        for idx, component_data in enumerate(total_data):
            if idx >= len(component_names):
                break

            component_name = component_names[idx]

            # Limpiar filas existentes
            self.characteristics_tables[component_name].rows.clear()

            # Llenar la tabla con los datos de este componente
            for item in component_data:
                # Formatear el valor según su tipo
                value = item[1]
                formatted_value = f"{value:.4f}" if isinstance(value, float) else str(value)

                # Agregar fila a la tabla
                self.characteristics_tables[component_name].rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(GenericText(item[0], color=ft.colors.BLUE_GREY_800)),
                            ft.DataCell(GenericText(formatted_value, color=ft.colors.BLUE_GREY_800)),
                        ]
                    )
                )

            # Actualizar la tabla de este componente
            self.characteristics_tables[component_name].update()

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
                            ft.DataCell(GenericText(f"{row['Rango']:.4f}", weight=ft.FontWeight.W_500,
                                                    color=ft.colors.BLUE_GREY_900))
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
