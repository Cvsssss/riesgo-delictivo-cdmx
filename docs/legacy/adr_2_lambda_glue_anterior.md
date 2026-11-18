# ADR 0002: Lambda o Glue para la transformación de bronze a silver

- **Estado:** propuesta
- **Fecha:** 2026-11-12
- **Decide:** equipo Data Bloom

## Contexto

La segunda Lambda del pipeline lee los archivos de bronze, los transforma y valida, y escribe en las dos Capas Silver. Hay que decidir si esa transformación corre en AWS Lambda o en AWS Glue.

El proceso corre una vez por semana y procesa archivos Excel de INEGI y PGR.

## Mediciones

| Dato | Valor |
|---|---|
| Tamaño de los archivos por corrida (MB) | [medir] |
| Filas por corrida | [medir] |
| Crecimiento esperado (por semana o por mes) | [estimar] |
| Tiempo de ejecución en Lambda | [medir] |
| Memoria usada | [medir] |
| Ejecuciones por mes | 4 o 5 (una cada lunes) |

## Límites de Lambda a considerar

| Límite | Valor |
|---|---|
| Tiempo máximo por ejecución | 15 minutos |
| Memoria máxima | 128 MB a 10,240 MB |
| Almacenamiento temporal | Entre 512 MB y 10,240 MB |
| Tamaño del paquete de despliegue | Paquete .zip: 50 MB comprimido y 250 MB descomprimido. Imagen de contenedor: hasta 10 GB |

## Opciones

| | Lambda | Glue |
|---|---|---|
| Cómo corre | Función bajo demanda | Trabajo administrado (puede usar Spark) |
| Tiempo de ejecución estimado | [de la tabla de mediciones] | [estimar] |
| Costo por corrida | $0 (dentro del free tier mensual de Lambda) | ≈ $0.07 (Spark, 2 DPU, 5 min, estimado) |
| Costo mensual | $0 | ≈ $0.37 (5 corridas, estimado sin medir) |
| Complejidad de desarrollo y despliegue | Baja: una función dentro de la plantilla de CloudFormation, empaquetar la librería para leer Excel dentro de los límites del paquete | hay que definir el trabajo en la plantilla y probar el arranque |
| Cabe en los límites con el volumen actual | [pendiente de medir] | [verificar timeout configurado del trabajo] |
## Decisión

## Umbral de cambio

Se cambia a Glue cuando ocurra **cualquiera** de estas condiciones.

- Una corrida tarda más de [ej.: 10] minutos en Lambda.
- La memoria usada supera [ej.: 80%] de la configurada.
- El volumen por corrida crece [ej.: 100 veces] respecto al actual.
- Se necesita Spark o procesamiento distribuido.

## Consecuencias

- Si se elige Lambda: el costo se mantiene muy por debajo del límite de $25,500 MXN al mes del RFP y el despliegue queda en la plantilla de CloudFormation.
- Se vigila el tiempo y la memoria de cada corrida en CloudWatch para detectar cuándo se acerca el umbral.
- Si se cruza el umbral, se escribe un nuevo ADR que reemplaza a este.
