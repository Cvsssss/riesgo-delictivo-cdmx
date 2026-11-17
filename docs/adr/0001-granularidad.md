# ADR 0001 — Granularidad del indicador

**Estado:** decisión del equipo para la primera versión (17/11/2026).

## Contexto

Una de las primeras cosas que tuvimos que decidir fue qué tan específica debía ser la información. La base de la FGJ puede tener alcaldía, colonia, fecha y tipo de delito. Si empezamos por colonia, nos podemos encontrar con nombres diferentes, campos vacíos y zonas con muy pocos registros. Para esta entrega queremos algo que podamos revisar y explicar bien.

## Decisión

- Vamos a juntar los registros por **alcaldía y mes** (`YYYY-MM`).
- Un registro debe tener fecha válida, una de las 16 alcaldías y una categoría de delito. Si falta algo, lo contamos en el reporte de calidad.
- Calculamos cuántos delitos hay y un puntaje de ejemplo según la categoría.
- Comparamos los puntajes dentro del mes para mostrar BAJO, MEDIO o ALTO. Si todos son iguales, no forzamos una diferencia.
- El resultado sirve para observar **denuncias registradas**; no es una predicción de delitos.

## Consecuencias y pendientes

Con alcaldía y mes podemos terminar la primera versión sin complicarnos tanto. La desventaja es que perdemos el detalle de cada colonia. Además, no estamos dividiendo los casos entre la población, así que un puntaje alto no significa por sí solo que una alcaldía sea más peligrosa. Para la entrega completa nos faltará revisar duplicados, agregar población, definir cuándo hay datos suficientes y validar la fórmula. Tampoco debemos comparar directamente los niveles de lotes distintos sin revisar qué periodos contienen.
