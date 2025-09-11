from logic.estudio_seniales.EstudioSenalesCod import segmul


class AnalysisService:
    @staticmethod
    def validate_inputs(ti_str: str, tf_str: str) -> tuple:
        """Validamos los inputs de tiempo"""
        castNum1: int = int(ti_str)
        castNum2: int = int(tf_str)
        linealTimeAssert: bool = (castNum1 < castNum2)
        if not ti_str or not tf_str or not linealTimeAssert:
            raise ValueError("Ingrese tiempos válidos.")
        return float(ti_str), float(tf_str)

    @staticmethod
    def validate_page_data(page_data: dict):
        """Validamos que los datos necesarios estén presentes"""
        if 'med_type' not in page_data or 'datosProcesar' not in page_data:
            raise ValueError("Datos de análisis no disponibles.")

    @staticmethod
    def execute_analysis(page_data: dict, ti: float, tf: float, action_name: str):
        """Ejecuta el análisis y retorna resultados"""
        return segmul(
            med=page_data.get('med_type'),
            datosProcesar=int(page_data.get('datosProcesar')), # Obetenemos el valor en del dict
            Ti=ti,
            Tf=tf,
            accion=action_name
        )
