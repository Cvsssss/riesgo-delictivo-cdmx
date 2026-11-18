import importlib.util
import pathlib
import unittest


RUTA = pathlib.Path(__file__).resolve().parents[1] / "src" / "gold" / "handler.py"
spec = importlib.util.spec_from_file_location("gold_handler", RUTA)
gold = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gold)


class PruebasIndicadores(unittest.TestCase):
	def test_agrupa_por_alcaldia_y_mes(self):
		filas = [
			{"fecha": "2026-10-01", "alcaldia": "COYOACAN", "categoria": "ROBO"},
			{"fecha": "2026-10-03", "alcaldia": "COYOACAN", "categoria": "LESIONES"},
			{"fecha": "2026-11-01", "alcaldia": "COYOACAN", "categoria": "OTROS"},
		]
		filas_resultado = gold.calcular_indicadores(filas, fecha_proceso="2026-11-17")
		self.assertEqual(len(filas_resultado), 2)
		self.assertEqual(filas_resultado[0]["total_delitos"], 2)
		self.assertEqual(filas_resultado[0]["puntaje_ponderado"], 5)
		self.assertEqual(filas_resultado[1]["mes"], "2026-11")

	def test_una_sola_zona_no_se_califica_como_riesgo_real(self):
		filas = [{"fecha": "2026-10-01", "alcaldia": "COYOACAN", "categoria": "ROBO"}]
		indicadores = gold.calcular_indicadores(filas, fecha_proceso="2026-11-17")
		self.assertEqual(indicadores[0]["nivel_incidencia"], "SIN DIFERENCIA SUFICIENTE")
		self.assertIn("no predice", indicadores[0]["limitaciones"])


if __name__ == "__main__":
	unittest.main()
