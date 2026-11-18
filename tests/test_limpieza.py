import importlib.util
import io
import pathlib
import unittest


RUTA = pathlib.Path(__file__).resolve().parents[1] / "src" / "silver" / "handler.py"
spec = importlib.util.spec_from_file_location("silver_handler", RUTA)
silver = importlib.util.module_from_spec(spec)
spec.loader.exec_module(silver)


class PruebasLimpieza(unittest.TestCase):
	def test_normaliza_acento_y_fecha(self):
		entrada = {"fecha_inicio": "2026-10-12", "alcaldia_catalogo": "álvaro obregón", "categoria_delito": "Robo"}
		registro, motivo = silver.normalizar_registro(entrada)
		self.assertIsNone(motivo)
		self.assertEqual(registro, {"fecha": "2026-10-12", "alcaldia": "ALVARO OBREGON", "categoria": "ROBO"})

	def test_rechaza_datos_incompletos(self):
		registro, motivo = silver.normalizar_registro({"fecha_inicio": "2026-10-12", "alcaldia_catalogo": "", "categoria_delito": "Robo"})
		self.assertIsNone(registro)
		self.assertEqual(motivo, "alcaldia_invalida")

	def test_reporte_y_salida_sin_duplicaciones(self):
		entrada = io.StringIO("fecha_inicio,alcaldia_catalogo,categoria_delito\n2026-10-12,Coyoacán,ROBO\n2026-10-13,Sin alcaldia,ROBO\n")
		salida = io.StringIO()
		resumen = silver.procesar_filas(entrada, salida)
		self.assertEqual(resumen["validos"], 1)
		self.assertEqual(resumen["rechazados"], {"alcaldia_invalida": 1})
		self.assertEqual(len(salida.getvalue().splitlines()), 2)


if __name__ == "__main__":
	unittest.main()
