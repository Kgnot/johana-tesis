from src.service.analysis_signal_service import AnalysisService


class AnalysisController:
    def __init__(self, view):
        self.view = view
        self.analysis_service = AnalysisService()

    def perform_analysis(self, ti_str: str, tf_str: str):
        """Coordina el proceso completo de análisis"""
        try:
            # Validar inputs
            ti, tf = self.analysis_service.validate_inputs(ti_str, tf_str)

            # Validar datos de página
            self.analysis_service.validate_page_data(self.view.page.data)

            # Ejecutar análisis
            result = self.analysis_service.execute_analysis(
                self.view.page.data, ti, tf, self.view.action_name
            )

            # Actualizar vista
            self.view.update_with_result(result)

        except ValueError as e:
            self.view.show_error(str(e))
        except Exception as e:
            self.view.show_error(f"Error inesperado: {e}")