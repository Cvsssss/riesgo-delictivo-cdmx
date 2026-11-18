"""Descarga un CSV oficial y conserva el original en la capa bronze."""

import hashlib
import os
import tempfile
from datetime import datetime, timezone
from urllib.parse import urlparse
from urllib.request import Request, urlopen


def descargar(url, destino, limite_bytes):
	"""Descarga por bloques para no cargar todo el archivo en memoria."""
	digest = hashlib.sha256()
	total = 0
	peticion = Request(url, headers={"User-Agent": "DataBloom-CDMX-MVP/1.0"})
	with urlopen(peticion, timeout=45) as respuesta, open(destino, "wb") as archivo:
		while True:
			bloque = respuesta.read(1024 * 1024)
			if not bloque:
				break
			total += len(bloque)
			if total > limite_bytes:
				raise ValueError("El archivo supera el limite de descarga configurado")
			digest.update(bloque)
			archivo.write(bloque)
	if total == 0:
		raise ValueError("La fuente devolvio un archivo vacio")
	return digest.hexdigest(), total


def lambda_handler(event, context):
	import boto3
	from botocore.exceptions import ClientError

	url = os.environ.get("SOURCE_URL", "").strip()
	if not url:
		return {"estado": "sin_fuente", "detalle": "Configurar SOURCE_URL antes de activar el calendario"}
	if urlparse(url).scheme != "https":
		raise ValueError("SOURCE_URL debe utilizar HTTPS")

	bucket = os.environ["DATA_BUCKET"]
	limite = int(os.environ.get("MAX_SOURCE_BYTES", "100000000"))
	s3 = boto3.client("s3")
	with tempfile.TemporaryDirectory() as directorio:
		ruta = os.path.join(directorio, "fuente.csv")
		huella, bytes_descargados = descargar(url, ruta, limite)
		clave = f"bronze/fgj/{huella}.csv"
		try:
			s3.head_object(Bucket=bucket, Key=clave)
			return {"estado": "sin_cambios", "clave": clave, "bytes": bytes_descargados}
		except ClientError as error:
			if error.response["Error"]["Code"] not in ("404", "NoSuchKey", "NotFound"):
				raise
		s3.upload_file(
			ruta, bucket, clave,
			ExtraArgs={
				"ContentType": "text/csv",
				"Metadata": {
					"sha256": huella,
					"ingestado-en": datetime.now(timezone.utc).isoformat(),
					"origen": "fgj-cdmx",
				},
			},
		)
	return {"estado": "ingestado", "clave": clave, "bytes": bytes_descargados}
