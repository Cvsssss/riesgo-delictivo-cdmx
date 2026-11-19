
import csv
import datetime
import io
import json
import os
import time
import unicodedata
from bisect import bisect_left
from collections import defaultdict

LAT0, LON0, PASO = 19.0, -99.4, 0.01          
LAT_MAX, LON_MAX = 19.6, -98.9                
ANIO_MIN, ANIO_MAX = 2016, 2025
PESOS = {                                   
    "HOMICIDIO DOLOSO": 10, "FEMINICIDIO": 10, "SECUESTRO": 10,
    "PLAGIO O SECUESTRO": 10,
    "VIOLACION": 8, "LESIONES DOLOSAS POR DISPARO DE ARMA DE FUEGO": 8,
    "ROBO A CASA HABITACION CON VIOLENCIA": 5,
    "ROBO A CUENTAHABIENTE SALIENDO DEL CAJERO CON VIOLENCIA": 5,
    "ROBO A PASAJERO A BORDO DE TAXI CON VIOLENCIA": 5,
    "ROBO A TRANSPORTISTA CON Y SIN VIOLENCIA": 5,
    "ROBO A TRANSEUNTE EN VIA PUBLICA CON Y SIN VIOLENCIA": 3,
    "ROBO DE VEHICULO CON Y SIN VIOLENCIA": 3,
    "ROBO A NEGOCIO CON VIOLENCIA": 3,
    "ROBO A REPARTIDOR CON Y SIN VIOLENCIA": 3,
    "ROBO A PASAJERO A BORDO DEL METRO CON Y SIN VIOLENCIA": 3,
    "ROBO A PASAJERO A BORDO DE MICROBUS CON Y SIN VIOLENCIA": 3,
    "DELITO DE BAJO IMPACTO": 1,
    "HECHO NO DELICTIVO": 0,               
}
PESO_DEFECTO = 1
CATEGORIAS = list(PESOS) + ["OTRA"]
CAT_ID = {c: i for i, c in enumerate(CATEGORIAS)}


def norm(txt):
    """Mayusculas, sin acentos y sin espacios sobrantes."""
    txt = unicodedata.normalize("NFD", (txt or "").strip().upper())
    return "".join(c for c in txt if unicodedata.category(c) != "Mn")


def leer_poblacion(lineas):
    """Poblacion por alcaldia (filas del ITER con LOC = 0000)."""
    r = csv.reader(lineas)
    enc = [c.lstrip("﻿").strip().upper() for c in next(r)]
    i_mun, i_nom, i_loc, i_pob = (enc.index(c) for c in ("MUN", "NOM_MUN", "LOC", "POBTOT"))
    pob = {}
    for f in r:
        if len(f) > i_pob and f[i_loc] == "0000" and f[i_mun] != "000":
            pob[norm(f[i_nom])] = int(f[i_pob])
    return pob


def semana_del_anio(fecha):
    d = fecha.timetuple().tm_yday
    return min((d - 1) // 7 + 1, 52)          


def procesar(lineas_fgj, poblacion, salida, min_registros=10,
             p_alto=80.0, p_medio=50.0, version="v1-2026-11"):
    """Procesa el CSV de la FGJ y escribe los archivos en la carpeta `salida`."""
    csv.field_size_limit(10_000_000)
    r = csv.reader(lineas_fgj)
    enc = [c.lstrip("﻿").strip().lower() for c in next(r)]
    ix = {c: enc.index(c) for c in
          ("fecha_hecho", "fecha_inicio", "categoria_delito", "alcaldia_hecho", "latitud", "longitud")}
    necesarias = max(ix.values()) + 1

    q = defaultdict(int)                     
    alc_w = defaultdict(float)                 
    celda_alc = defaultdict(lambda: defaultdict(int))
    anios_p = {(t, p): set() for t in (0, 1) for p in range(1, 53)}
    cache_fecha = {}
    cal = defaultdict(int)

    for f in r:
        cal["registros_leidos"] += 1
        if len(f) < necesarias:
            cal["descartado_fila_corta"] += 1
            continue
        parte = None
        for campo in (f[ix["fecha_hecho"]], f[ix["fecha_inicio"]]):
            clave = campo[:10]
            if clave not in cache_fecha:
                try:
                    d = datetime.date(int(clave[:4]), int(clave[5:7]), int(clave[8:10]))
                    cache_fecha[clave] = (d.year, d.month, semana_del_anio(d))
                except ValueError:
                    cache_fecha[clave] = None
            parte = cache_fecha[clave]
            if parte:
                break
        if not parte:
            cal["descartado_sin_fecha"] += 1
            continue
        anio, mes, sem = parte
        if anio < ANIO_MIN or anio > ANIO_MAX:
            cal["descartado_fuera_de_2016_2025"] += 1
            continue
        cat = norm(f[ix["categoria_delito"]])
        if cat not in PESOS:
            cal["categoria_desconocida_peso_1"] += 1
        peso = PESOS.get(cat, PESO_DEFECTO)
        if peso == 0:
            cal["excluido_hecho_no_delictivo"] += 1
            continue
        cid = CAT_ID.get(cat, CAT_ID["OTRA"])
        alc = norm(f[ix["alcaldia_hecho"]])
        alc_ok = alc in poblacion
        if alc_ok:
            alc_w[(alc, 1, mes)] += peso
        else:
            cal["alcaldia_no_valida"] += 1
        try:
            lat = float(f[ix["latitud"]])
            lon = float(f[ix["longitud"]])
        except ValueError:
            cal["descartado_sin_coordenadas"] += 1
            continue
        if not (LAT0 <= lat < LAT_MAX and LON0 <= lon < LON_MAX):
            cal["descartado_coordenadas_fuera_de_cdmx"] += 1
            continue
        celda = int((lat - LAT0) / PASO) * 100 + int((lon - LON0) / PASO)
        q[((celda * 2 + 0) * 64 + sem) * 32 + cid] += 1
        q[((celda * 2 + 1) * 64 + mes) * 32 + cid] += 1
        anios_p[(0, sem)].add(anio)
        anios_p[(1, mes)].add(anio)
        if alc_ok:
            celda_alc[celda][alc] += 1
        cal["usado_en_el_mapa"] += 1

    def centro(celda):
        return round(LAT0 + (celda // 100 + 0.5) * PASO, 5), round(LON0 + (celda % 100 + 0.5) * PASO, 5)

    w = {}                                    
    ruta1 = os.path.join(salida, "conteos_celda.csv")
    with open(ruta1, "w", newline="", encoding="utf-8") as fh:
        s1 = csv.writer(fh)
        s1.writerow(["celda_id", "lat", "lon", "tipo_periodo", "periodo", "categoria", "registros"])
        for k in sorted(q):
            cid = k % 32
            resto = k // 32
            periodo = resto % 64
            resto //= 64
            tipo, celda = resto % 2, resto // 2
            lat, lon = centro(celda)
            s1.writerow([celda, lat, lon, "semana" if tipo == 0 else "mes", periodo, CATEGORIAS[cid], q[k]])
            a = w.setdefault(celda, ({}, {}))[tipo]
            par = a.setdefault(periodo, [0.0, 0])
            par[0] += PESOS.get(CATEGORIAS[cid], PESO_DEFECTO) * q[k]
            par[1] += q[k]

    n_anios = {(t, p): max(len(s), 1) for (t, p), s in anios_p.items()}
    filas = []                                 
    for celda, par in w.items():
        for tipo, nper in ((1, 12), (0, 52)):
            datos = par[tipo]
            prom = {p: datos.get(p, [0.0, 0])[0] / n_anios[(tipo, p)] for p in range(1, nper + 1)}
            regs = {p: datos.get(p, [0.0, 0])[1] for p in range(1, nper + 1)}
            for p in range(1, nper + 1):
                if tipo == 0:                 
                    vec = [(p - 2) % 52 + 1, p, p % 52 + 1]
                    v = sum(prom[x] for x in vec) / 3
                    n = sum(regs[x] for x in vec)
                else:
                    v, n = prom[p], regs[p]
                filas.append((celda, tipo, p, v, n, n >= min_registros))
    por_periodo = defaultdict(list)
    for celda, tipo, p, v, n, ok in filas:
        if ok:
            por_periodo[(tipo, p)].append(v)
    for lst in por_periodo.values():
        lst.sort()

    def nivel(pct):
        return "ALTO" if pct >= p_alto else ("MEDIO" if pct >= p_medio else "BAJO")

    hoy = datetime.date.today().isoformat()
    ruta2 = os.path.join(salida, "indice_celda.csv")
    with open(ruta2, "w", newline="", encoding="utf-8") as fh:
        s2 = csv.writer(fh)
        s2.writerow(["celda_id", "lat", "lon", "alcaldia", "tipo_periodo", "periodo",
                     "delitos_ponderados_prom_anual", "registros", "puntaje", "nivel",
                     "version_metodologia", "actualizado"])
        for celda, tipo, p, v, n, ok in sorted(filas):
            lat, lon = centro(celda)
            a = celda_alc.get(celda)
            alcaldia = max(a, key=a.get) if a else ""
            if ok:
                lst = por_periodo[(tipo, p)]
                pct = round(bisect_left(lst, v) / len(lst) * 100, 1)
                niv = nivel(pct)
            else:
                pct, niv = "", "SIN INFORMACION SUFICIENTE"
            s2.writerow([celda, lat, lon, alcaldia, "semana" if tipo == 0 else "mes", p,
                         round(v, 4), n, pct, niv, version, hoy])

    tasas = []                                 
    for alc, pob in poblacion.items():
        prom_mes = {m: alc_w.get((alc, 1, m), 0.0) / n_anios[(1, m)] for m in range(1, 13)}
        for m in range(1, 13):
            tasas.append((alc, "mes", m, prom_mes[m] / pob * 100000))
        tasas.append((alc, "anio", 0, sum(prom_mes.values()) / pob * 100000))
    grupos = defaultdict(list)
    for alc, t, p, tasa in tasas:
        grupos[(t, p)].append(tasa)
    for lst in grupos.values():
        lst.sort()
    ruta3 = os.path.join(salida, "indice_alcaldia.csv")
    with open(ruta3, "w", newline="", encoding="utf-8") as fh:
        s3 = csv.writer(fh)
        s3.writerow(["alcaldia", "poblacion_2020", "tipo_periodo", "periodo",
                     "tasa_ponderada_por_100k", "puntaje", "nivel", "version_metodologia", "actualizado"])
        for alc, t, p, tasa in sorted(tasas):
            lst = grupos[(t, p)]
            pct = round(bisect_left(lst, tasa) / len(lst) * 100, 1)
            s3.writerow([alc, poblacion[alc], t, p, round(tasa, 2), pct, nivel(pct), version, hoy])

    cal["celdas_con_datos"] = len(w)
    cal["filas_indice_celda"] = len(filas)
    ruta4 = os.path.join(salida, "calidad.json")
    with open(ruta4, "w", encoding="utf-8") as fh:
        json.dump(dict(cal), fh, indent=2, ensure_ascii=False)
    return dict(cal), {"conteos_celda": ruta1, "indice_celda": ruta2,
                       "indice_alcaldia": ruta3, "calidad": ruta4}


def _lineas(cuerpo):
    for ln in cuerpo.iter_lines(chunk_size=1 << 20, keepends=True):
        yield ln.decode("utf-8", errors="replace")


def handler(event, context):
    import boto3                          
    s3 = boto3.client("s3")
    origen, destino = os.environ["BRONZE_BUCKET"], os.environ["SILVER_BUCKET"]
    inicio = time.time()
    poblacion = leer_poblacion(_lineas(s3.get_object(
        Bucket=origen, Key=os.environ.get("INEGI_KEY", "inegi/conjunto_de_datos_iter_09CSV20.csv"))["Body"]))
    cuerpo = s3.get_object(Bucket=origen, Key="fgj/carpetas_acumulado.csv")["Body"]
    cal, rutas = procesar(_lineas(cuerpo), poblacion, "/tmp",
                          min_registros=int(os.environ.get("MIN_REGISTROS", "10")),
                          version=os.environ.get("METODOLOGIA_VERSION", "v1-2026-11"))
    destinos = {"conteos_celda": "limpio/conteos_celda/conteos_celda.csv",
                "calidad": "limpio/calidad/calidad.json",
                "indice_celda": "consultable/indice_celda/indice_celda.csv",
                "indice_alcaldia": "consultable/indice_alcaldia/indice_alcaldia.csv"}
    for nombre, clave in destinos.items():
        s3.upload_file(rutas[nombre], destino, clave)
    resultado = {"segundos": round(time.time() - inicio, 1), "calidad": cal}
    print(json.dumps(resultado, ensure_ascii=False))
    return resultado
