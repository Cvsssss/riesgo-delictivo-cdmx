# riesgo-delictivo-cdmx

Pipeline de datos en AWS que toma archivos de la FGJ-CDMX y del INEGI sobre delitos y población en la Ciudad de México, los transforma y calcula un nivel de riesgo delictivo por zona (cuadrícula de 1 km) y época del año.

Proyecto del equipo **Data Bloom** para un cliente, **SAFEZONE MÉXICO**, una empresa que elabora mapas de riesgo.

![Arquitectura](docs/consultoria/riesgo-delictivo-cdmx.png)

## Qué problema resuelve

Los datos públicos de delitos llegan en archivos grandes, con errores de captura (alcaldías mal escritas, ubicaciones vacías, saltos de línea dentro de campos). Quien hace mapas de riesgo tiene que limpiarlos y recalcularlos a mano cada vez.

Este proyecto automatiza ese trabajo: los archivos se guardan sin modificar, y cada lunes a las 9:00 am (hora de la CDMX) se transforman y se calcula el riesgo. Los resultados quedan listos para consultarse con SQL en Athena.

## Qué pregunta contesta

> ¿Qué nivel de riesgo delictivo (bajo, medio o alto) tiene cada celda de 1 km de la CDMX en cada mes o semana del año, con datos abiertos y trazables?

Además da la tasa ponderada de delitos por 100,000 habitantes de cada alcaldía. La granularidad está justificada en el [ADR 0001](docs/adr/0001-granularidad-del-calculo.md).

## Cómo funciona

| Componente | Qué hace |
|---|---|
| **Orígenes de datos** | CSV acumulado de carpetas de investigación de la FGJ-CDMX (2,098,743 registros, 2016 a enero de 2025) y Censo de Población y Vivienda 2020 del INEGI (población por alcaldía). |
| **S3 · bronze** | El dato original, sin modificar y con versionado. Se puede recalcular todo desde aquí. |
| **EventBridge Scheduler** | Cada lunes a las 9:00 (America/Mexico_City) lanza la Lambda de transformación. |
| **Lambda de transformación** | Python, sin dependencias. Lee bronze en streaming, valida y escribe las dos Capas Silver. Tarda 69.8 s y usa 149 MB ([ADR 0002](docs/adr/0002-lambda-contra-glue.md)). |
| **Capa Silver 1 (limpia)** | Conteos por celda, periodo y categoría de delito, más `calidad.json` con el balance de registros descartados. |
| **Capa Silver 2 (consultable)** | `indice_celda` e `indice_alcaldia`, las tablas que consultan los usuarios. |
| **Athena** | SQL sobre la Silver consultable, con un grupo de trabajo que corta consultas que escaneen más de 2 GB. |
| **IAM Role** | Da a los usuarios acceso solo a Athena y a la Silver consultable; no pueden leer bronze. |
| **CloudWatch** | Alarmas de errores y duración, aviso por correo con SNS y un tablero. |
| **CloudFormation** | Toda la infraestructura como código (`infra/01` a `08`). |

Decisiones de diseño:

- Índice = promedio anual de delitos ponderados por tipo (de 0 a 10) en cada celda y periodo, convertido a percentil frente a las demás celdas del mismo periodo: alto ≥ 80, medio ≥ 50, bajo el resto. Es relativo, no absoluto.
- Las celdas con menos de 10 registros se marcan "SIN INFORMACION SUFICIENTE" en lugar de calificarse.
- La Silver 1 guarda conteos por categoría: cambiar los pesos o umbrales no obliga a releer el archivo original.
- El volumen es pequeño: Lambda basta, y el [ADR 0002](docs/adr/0002-lambda-contra-glue.md) da el umbral para pasar a Glue.

## Fuentes de datos

- **FGJ-CDMX**, carpetas de investigación (CSV acumulado, CC BY 4.0), datos abiertos de la CDMX.
- **INEGI**, Censo de Población y Vivienda 2020 (ITER, CSV).

Se confirmó que ambas están publicadas, su formato y sus campos. La FGJ no actualiza el acumulado con frecuenci.


## Resultados

Primera corrida real: 2,098,743 registros leídos, 57,152 filas en `indice_celda`, 893 celdas con datos. El rol de consulta puede usar Athena y se le niega bronze; la alarma de CloudWatch envió el correo de prueba.

## Limitaciones

- Los registros oficiales no incluyen los delitos que no se denuncian (cifra negra).
- Las zonas con más denuncias pueden parecer más riesgosas; las de pocos casos se marcan "sin información suficiente".
- El índice por celda es relativo (percentil), por lo que la cantidad de celdas por nivel casi no cambia entre épocas.
- Los pesos por tipo de delito son un supuesto del equipo, sin validación estadística.
- Los datos llegan hasta enero de 2025 y la carga es manual.
- El resultado es un nivel de riesgo histórico agregado. **No** es una predicción de delitos ni identifica personas.

## Documentación

- [RFP](docs/consultoria/rfp.md): necesidades del cliente.
- [SOW](docs/consultoria/sow.md): alcance, entregables, calendario y presupuesto.
- [ADR 0001](docs/adr/0001-granularidad-del-calculo.md): granularidad del cálculo.
- [ADR 0002](docs/adr/0002-lambda-contra-glue.md): Lambda o Glue.

## Equipo

Data Bloom: Amir Cuevas Quintana, Uriel Ivan Guerrero Lopez, Axel Alejandro Quintos Delgadillo, Aaron Rodrigo Leon Pérez y Eduardo Antonio Estrada Luna.

## Licencia

GPL-3.0. Consulta el archivo [LICENSE](LICENSE).
