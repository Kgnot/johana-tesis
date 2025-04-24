import flet as ft

def main(page: ft.Page):
    page.title = "Data Analysis Dashboard"
    page.theme_mode = "light"
    page.bgcolor = "#f8f9fa"
    page.padding = 0

    # ---- Contenedor donde cambia el contenido ----
    content_container = ft.Container(expand=True, padding=20)

    # ---- Función para actualizar solo el contenido ----
    def change_page(index):
        views = [
            home_view(),
            data_analysis_view(),
            performance_metrics_view(),
            report_generation_view(),
            charts_view(),
            statistics_view()
        ]
        content_container.content = views[index]  # Cambia solo el contenido
        page.update()

    # ---- Sidebar (Menú de navegación) ----
    sidebar = ft.Container(
        width=220,
        bgcolor="white",
        content=ft.Column(
            [
                ft.Text("📊 Data Dashboard", size=20, weight="bold"),
                ft.Divider(),
                ft.NavigationRail(
                    selected_index=0,
                    label_type=ft.NavigationRailLabelType.ALL,
                    expand=True,  # 🔥 SOLUCIÓN: Asegura que tenga tamaño
                    destinations=[
                        ft.NavigationRailDestination(icon=ft.icons.HOME, label="Home"),
                        ft.NavigationRailDestination(icon=ft.icons.BAR_CHART, label="Data Analysis"),
                        ft.NavigationRailDestination(icon=ft.icons.SHOW_CHART, label="Performance Metrics"),
                        ft.NavigationRailDestination(icon=ft.icons.DESCRIPTION, label="Report Generation"),
                        ft.NavigationRailDestination(icon=ft.icons.INSERT_CHART, label="Charts"),
                        ft.NavigationRailDestination(icon=ft.icons.ANALYTICS, label="Statistics"),
                    ],
                    on_change=lambda e: change_page(e.control.selected_index),
                ),
            ],
            expand=True
        )
    )

    # ---- Páginas ----
    def home_view():
        return ft.Column([
            ft.Text("Data Analysis Dashboard", size=30, weight="bold"),
            ft.Text("Welcome to the interactive data analysis dashboard.", size=14, color="gray"),
        ])

    def data_analysis_view():
        return ft.Column([
            ft.Text("📊 Data Analysis", size=30, weight="bold"),
            ft.Text("Analyze trends, patterns, and insights from your datasets.", size=14, color="gray"),
        ])

    def performance_metrics_view():
        return ft.Column([
            ft.Text("📈 Performance Metrics", size=30, weight="bold"),
            ft.Text("Track key performance indicators and monitor performance.", size=14, color="gray"),
        ])

    def report_generation_view():
        return ft.Column([
            ft.Text("📄 Report Generation", size=30, weight="bold"),
            ft.Text("Create and export reports from your data.", size=14, color="gray"),
        ])

    def charts_view():
        return ft.Column([
            ft.Text("📊 Charts", size=30, weight="bold"),
            ft.Text("View and analyze different types of charts.", size=14, color="gray"),
        ])

    def statistics_view():
        return ft.Column([
            ft.Text("📊 Statistics", size=30, weight="bold"),
            ft.Text("Get statistical insights from your data.", size=14, color="gray"),
        ])

    # ---- Contenido inicial ----
    content_container.content = home_view()

    # ---- Estructura Principal ----
    page.add(ft.Row([sidebar, content_container], expand=True))

ft.app(target=main)

