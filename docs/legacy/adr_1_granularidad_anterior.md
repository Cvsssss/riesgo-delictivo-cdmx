# ADR 0001: Granularidad del cálculo de riesgo

- **Estado:** propuesta
- **Fecha:** 2026-11-12
- **Decide:** equipo Data Bloom 

## Contexto

El pipeline calcula un nivel de riesgo delictivo (bajo, medio o alto) por zona y periodo. Hay que decidir qué es una "zona" (alcaldía o colonia) y qué es un "periodo" (mes, día u hora) **antes de construir la transformación hacia las Capas Silver**, porque esta decisión define:

- las columnas y la partición de las tablas de la Capa Silver,
- la fórmula de riesgo,
- qué población se necesita para normalizar, y a qué nivel geográfico existe.

Los orígenes son la API de INEGI y la API de PGR. La ejecución es semanal.

## Datos disponibles en los orígenes

Llenar al revisar los archivos Excel:

| Campo | INEGI | PGR |
|---|---|---|
| Fecha del delito | Si | Si |
| Hora del delito | No | Si |
| Alcaldía | Si | Si |
| Colonia | Si | Si |

## Opciones

| Opción | Zona | Periodo | Las fuentes traen los campos | Casos por celda (zona y periodo)
|---|---|---|---|---|---|
| A | Alcaldía | Mes | Si | 1,000
| B | Colonia | Mes | Si | 9
| C | Colonia | Día | Si | 0.3
| D | Colonia | Hora | No | 0.01

## Decisión

Punto de partida del SOW: colonia o alcaldía por mes.

## Consecuencias

- Las tablas de la Capa Silver se diseñan con esta unidad de zona y periodo.
- La población para normalizar debe existir a ese mismo nivel; si solo existe por alcaldía, la zona no puede ser colonia sin otra fuente.
- Si se necesita una granularidad más fina, se registra como solicitud de cambio.
