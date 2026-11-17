# ADR 0002 — AWS Lambda frente a AWS Glue

**Estado:** vamos a usar Lambda en la primera versión (17/11/2026).

## Contexto

Estuvimos considerando Lambda y Glue para procesar los archivos. Por ahora solo necesitamos descargar un CSV, limpiar sus datos y hacer un resumen. Lambda nos permite separar esas tareas en funciones pequeñas y ejecutar la siguiente cuando S3 reciba un archivo. Glue también serviría, pero sería más trabajo configurarlo para esta primera prueba.

## Decisión del MVP

Elegimos **tres Lambdas**: una para descargar, otra para limpiar y otra para calcular los indicadores. Dejamos un límite de descarga de **100 MB** (`MaxSourceBytes`) que podemos cambiar si hace falta. Usaremos Glue únicamente como catálogo de tablas para Athena, no para ejecutar transformaciones.

| Criterio | Lambda (elegida) | Glue ETL (alternativa) |
| --- | --- | --- |
| Cómo se ejecuta | EventBridge Scheduler y eventos S3 | Jobs de Glue |
| Qué tenemos que configurar | Tres funciones pequeñas | Un trabajo de procesamiento |
| Cómo se cobra | Invocaciones, tiempo y memoria | Capacidad de cómputo y tiempo |
| Límite que nos importa | 15 minutos por ejecución | Puede trabajar con procesos más grandes |
| Para nuestros primeros archivos | Nos parece suficiente | Lo dejamos como alternativa |

## Números y comparación

Todavía **no hemos medido una ejecución en AWS**. Nuestro archivo de prueba tiene **456 bytes y 12 registros** (sin contar el encabezado), pero es un archivo inventado para probar el programa, no el tamaño real de la base de FGJ. Cuando hagamos la primera ejecución anotaremos el tamaño del archivo, las filas, los segundos, la memoria, los reintentos y el costo estimado.

Para hacer una comparación, supongamos un archivo de **10 MB** y que las tres Lambdas tardan **10 segundos cada una**, con **512 MB** de memoria. Es un ejemplo, no una prueba que ya hayamos corrido:

- Lambda: 3 × 10 × 0.5 = **15 GB-s**. A una tarifa de referencia de 0.0000166667 USD/GB-s, más las solicitudes, serían unos **0.000251 USD por lote**.
- Glue: si un trabajo usara **2 DPU durante 1 minuto**, con la tarifa de referencia de 0.44 USD/DPU-h, serían unos **0.0147 USD por lote**.
- Si repitiéramos esas condiciones durante 30 días, el cómputo saldría aproximadamente en **0.0075 USD con Lambda** o **0.44 USD con Glue**.

Estos números solo comparan el cómputo bajo los supuestos indicados. Faltan S3, consultas de Athena y otros posibles cargos, además de confirmar precios y tiempos reales en nuestra región.

Fuentes de consulta de tarifas: [AWS Lambda](https://aws.amazon.com/es/lambda/pricing/) y [AWS Glue](https://aws.amazon.com/glue/pricing/).

Cambiaríamos a Glue si vemos que pasa alguna de estas cosas varias veces:

- Alguna Lambda tarda **12 minutos o más**.
- Una Lambda usa más del **80 % de la memoria** que le asignamos.
- Los archivos superan el tamaño que podemos procesar cómodamente o necesitamos repartir el trabajo.
- Al comparar ejecuciones reales, Glue resulta más conveniente en tiempo o costo.

Por eso, antes de activar las descargas automáticas, tenemos que comprobar cuánto pesa el archivo oficial. Si es demasiado grande, ajustaremos el proceso o volveremos a evaluar Glue.
