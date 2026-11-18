import csv
import importlib.util
import io
import pathlib
import unittest


RAIZ = pathlib.Path(__file__).resolve().parents[1]


def cargar_modulo(nombre, ruta):
	especificacion = importlib.util.spec_from_file_location(nombre, RAIZ / ruta)
	modulo = importlib.util.module_from_spec(especificacion)
	especificacion.loader.exec_module(modulo)
	return modulo


silver = cargar_modulo("silver_local", "src/silver/handler.py")
gold = cargar_modulo("gold_local", "src/gold/handler.py")


class PruebaPipelineLocal(unittest.TestCase):
	def test_csv_sintetico_pasa_de_bronze_a_gold(self):
		muestra = RAIZ / "tests" / "fixtures" / "muestra_fgj.csv"
		limpio = io.StringIO()
		with muestra.open(encoding="utf-8", newline="") as entrada:
			reporte = silver.procesar_filas(entrada, limpio)
		self.assertEqual(reporte["total"], 12)
		self.assertEqual(reporte["validos"], 10)
		self.assertEqual(reporte["rechazados"], {"fecha_invalida": 1, "alcaldia_invalida": 1})
		limpio.seek(0)
		indicadores = gold.calcular_indicadores(csv.DictReader(limpio), fecha_proceso="2026-11-17")
		self.assertEqual(sum(fila["total_delitos"] for fila in indicadores), 10)
		self.assertEqual(len(indicadores), 6)
		coyoacan_octubre = next(fila for fila in indicadores if fila["alcaldia"] == "COYOACAN" and fila["mes"] == "2026-10")
		self.assertEqual(coyoacan_octubre["total_delitos"], 4)
		self.assertEqual(coyoacan_octubre["puntaje_ponderado"], 11)


if __name__ == "__main__":
	unittest.main()
