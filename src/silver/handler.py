"""Convierte las carpetas de investigacion a registros normalizados."""

import csv
import io
import json
import os
import tempfile
import unicodedata
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import unquote_plus


ALCALDIAS = (
	"ALVARO OBREGON", "AZCAPOTZALCO", "BENITO JUAREZ", "COYOACAN",
	"CUAJIMALPA DE MORELOS", "CUAUHTEMOC", "GUSTAVO A MADERO", "IZTACALCO",
	"IZTAPALAPA", "LA MAGDALENA CONTRERAS", "MIGUEL HIDALGO", "MILPA ALTA",
	"TLAHUAC", "TLALPAN", "VENUSTIANO CARRANZA", "XOCHIMILCO",
)


def limpiar_texto(valor):
	valor = unicodedata.normalize("NFKD", str(valor or "").strip().upper())
	return " ".join("".join(letra for letra in valor if not unicodedata.combining(letra)).replace(".", " ").split())


def primer_valor(fila, campos):
	for campo in campos:
		valor = fila.get(campo)
		if valor is not None and str(valor).strip():
			return str(valor).strip()
	return ""


def fecha_iso(valor):
	valor = valor.strip()
	for formato in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d"):
		try:
			return datetime.strptime(valor[:10], formato).strftime("%Y-%m-%d")
		except ValueError:
			continue
	return ""


def normalizar_registro(fila):
	"""Devuelve un registro valido o (None, motivo de rechazo)."""
	fila = {limpiar_texto(campo).lower().replace(" ", "_"): valor for campo, valor in fila.items() if campo}
	fecha = fecha_iso(primer_valor(fila, ("fecha_hecho", "fecha_inicio", "fecha_delito", "fecha")))
	if not fecha:
		return None, "fecha_invalida"
	alcaldia = limpiar_texto(primer_valor(fila, ("alcaldia_catalogo", "alcaldia_hecho", "alcaldia", "alcaldiahechos")))
	if alcaldia not in ALCALDIAS:
		return None, "alcaldia_invalida"
	categoria = limpiar_texto(primer_valor(fila, ("categoria_delito", "categoria", "delito")))
	if not categoria:
		return None, "categoria_vacia"
	return {"fecha": fecha, "alcaldia": alcaldia, "categoria": categoria}, None


def procesar_filas(entrada, salida):
	lector = csv.DictReader(entrada)
	if not lector.fieldnames:
		raise ValueError("El CSV no contiene encabezados")
	escritor = csv.DictWriter(salida, fieldnames=("fecha", "alcaldia", "categoria"))
	escritor.writeheader()
	rechazados = Counter()
	validos = 0
	for fila in lector:
		registro, motivo = normalizar_registro(fila)
		if motivo:
			rechazados[motivo] += 1
		else:
			escritor.writerow(registro)
			validos += 1
	return {"validos": validos, "rechazados": dict(rechazados), "total": validos + sum(rechazados.values())}


def lambda_handler(event, context):
	import boto3

	s3 = boto3.client("s3")
	bucket = os.environ["DATA_BUCKET"]
	resultados = []
	for elemento in event.get("Records", []):
		clave = unquote_plus(elemento["s3"]["object"]["key"])
		if not clave.startswith("bronze/") or not clave.endswith(".csv"):
			continue
		respuesta = s3.get_object(Bucket=bucket, Key=clave)
		with tempfile.TemporaryDirectory() as temporal:
			ruta = os.path.join(temporal, "delitos_limpios.csv")
			with io.TextIOWrapper(respuesta["Body"], encoding="utf-8-sig", errors="replace", newline="") as entrada:
				with open(ruta, "w", encoding="utf-8", newline="") as salida:
					resumen = procesar_filas(entrada, salida)
			if resumen["validos"] == 0:
				raise ValueError("No hay registros validos para generar silver")
			s3.upload_file(ruta, bucket, "silver/datos/delitos_limpios.csv", ExtraArgs={"ContentType": "text/csv"})
		resumen.update({"archivo_origen": clave, "procesado_en": datetime.now(timezone.utc).isoformat()})
		identificador = clave.rsplit("/", 1)[-1].rsplit(".", 1)[0]
		s3.put_object(Bucket=bucket, Key=f"silver/reportes/{identificador}.json", Body=json.dumps(resumen).encode("utf-8"), ContentType="application/json")
		resultados.append(resumen)
	return {"lotes": resultados}
