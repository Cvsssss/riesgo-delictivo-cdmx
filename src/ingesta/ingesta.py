
import os
import time
import urllib.request

import boto3
from boto3.s3.transfer import TransferConfig

s3 = boto3.client("s3")
BUCKET = os.environ["BRONZE_BUCKET"]
URL = os.environ["FGJ_URL"]
KEY = "fgj/carpetas_acumulado.csv"


def handler(event, context):
    inicio = time.time()
    req = urllib.request.Request(
        URL, headers={"User-Agent": "Mozilla/5.0 (data-bloom-ingesta)"}
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        esperado = r.headers.get("Content-Length")
        s3.upload_fileobj(
            r,
            BUCKET,
            KEY,
            ExtraArgs={"ContentType": "text/csv"},
            Config=TransferConfig(
                multipart_chunksize=16 * 1024 * 1024, max_concurrency=4
            ),
        )
    real = s3.head_object(Bucket=BUCKET, Key=KEY)["ContentLength"]
    if esperado and int(esperado) != real:
        raise RuntimeError(f"Tamano distinto: {esperado} vs {real}")
    resultado = {
        "bucket": BUCKET,
        "key": KEY,
        "mb": round(real / 1048576, 1),
        "segundos": round(time.time() - inicio, 1),
    }
    print(resultado)
    return resultado
