"""Calcula indicadores historicos exploratorios por alcaldia y mes."""

import csv
import io
import os
from collections import defaultdict
from datetime import datetime, timezone
from urllib.parse import unquote_plus


VERSION = "mvp-1"
LIMITACIONES = "Indicador historico de denuncias sin ajuste por poblacion; no predice delitos"


def peso(categoria):
	texto = categoria.upper()
	if "HOMICIDIO" in texto:
		return 5
	if "ROBO" in texto:
		return 3
	if "LESION" in texto:
		return 2
	return 1


def calcular_indicadores(filas, fecha_proceso=None):
	fecha_proceso = fecha_proceso or datetime.now(timezone.utc).date().isoformat()
	agregados = defaultdict(lambda: {"total": 0, "puntaje": 0})
	for fila in filas:
		llave = (fila["fecha"][:7], fila["alcaldia"])
		agregados[llave]["total"] += 1
		agregados[llave]["puntaje"] += peso(fila["categoria"])
	por_mes = defaultdict(list)
	for (mes, alcaldia), datos in agregados.items():
		por_mes[mes].append((alcaldia, datos))
	salida = []
	for mes, zonas in sorted(por_mes.items()):
		puntajes = sorted(datos["puntaje"] for _, datos in zonas)
		inferior = puntajes[(len(puntajes) - 1) // 3]
		superior = puntajes[2 * (len(puntajes) - 1) // 3]
		for alcaldia, datos in sorted(zonas):
			if inferior == superior:
				nivel = "SIN DIFERENCIA SUFICIENTE"
			elif datos["puntaje"] <= inferior:
				nivel = "BAJO"
			elif datos["puntaje"] <= superior:
				nivel = "MEDIO"
			else:
				nivel = "ALTO"
			salida.append({
				"alcaldia": alcaldia,
				"mes": mes,
				"total_delitos": datos["total"],
				"puntaje_ponderado": datos["puntaje"],
				"nivel_incidencia": nivel,
				"version_metodologia": VERSION,
				"fecha_proceso": fecha_proceso,
				"limitaciones": LIMITACIONES,
			})
	return salida


def lambda_handler(event, context):
	import boto3

	bucket = os.environ["DATA_BUCKET"]
	s3 = boto3.client("s3")
	procesados = []
	for elemento in event.get("Records", []):
		clave = unquote_plus(elemento["s3"]["object"]["key"])
		if not clave.startswith("silver/datos/") or not clave.endswith(".csv"):
			continue
		respuesta = s3.get_object(Bucket=bucket, Key=clave)
		with io.TextIOWrapper(respuesta["Body"], encoding="utf-8-sig", newline="") as archivo:
			filas = csv.DictReader(archivo)
			indicadores = calcular_indicadores(filas)
		if not indicadores:
			raise ValueError("Silver no contiene registros para calcular indicadores")
		salida = io.StringIO()
		escritor = csv.DictWriter(salida, fieldnames=indicadores[0].keys(), lineterminator="\n")
		escritor.writeheader()
		escritor.writerows(indicadores)
		s3.put_object(
			Bucket=bucket,
			Key="gold/indicadores/indicadores.csv",
			Body=salida.getvalue().encode("utf-8"),
			ContentType="text/csv",
		)
		procesados.append({"archivo": clave, "indicadores": len(indicadores)})
	return {"procesados": procesados}
