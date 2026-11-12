# SOW: Pipeline batch de cálculo de riesgo delictivo en la CDMX

**Consultora:** Data Bloom
**Cliente:** SAFEZONE MÉXICO (Área de Inteligencia de Datos)
**Respuesta al RFP del:** 6 de octubre de 2026
**Versión:** 1.1
**Equipo:**
- Amir Cuevas Quintana — Ing. en Computación — Líder de proyecto y arquitecto de datos
- Uriel Ivan Guerrero Lopez — Ing. en Computación — Ingeniero de datos (ingesta y orquestación)
- Axel Alejandro Quintos Delgadillo — Ing. en Computación — Ingeniero de datos (calidad y modelo de datos)
- Aaron Rodrigo Leon Pérez — Ing. en Computación — Científico de datos
- Eduardo Antonio Estrada Luna — Ing. en Computación — DevOps, pruebas y documentación

---

## 1. Resumen ejecutivo

SAFEZONE elabora mapas de riesgo delictivo y necesita datos públicos de delitos en la CDMX que estén actualizados y sean confiables. Para eso construiremos un proceso automático que todos los días descargue los datos abiertos de carpetas de investigación de la FGJ-CDMX (apoyados con datos de INEGI), los limpie, los guarde con su historial y calcule un nivel de riesgo por zona y mes.
Los resultados quedarán disponibles en tablas consultables con SQL y en archivos listos para sus herramientas de visualización, siempre con su fecha, origen y limitaciones.
Entregamos en 8 semanas (6 hitos), con capacitación y 30 días de soporte posterior.
Los honorarios son de **$1,186,800 MXN + IVA** ($1,376,688 con IVA). El costo de AWS lo paga SAFEZONE directo en su cuenta: se estima en **~$3,000 MXN** durante el proyecto y en **~$600 MXN al mes** de operación. Ambas cifras quedan por debajo de los límites del RFP.

## 2. Alcance

**Dentro de alcance:**
- Ingesta automatizada de una fuente principal: los datos abiertos de carpetas de investigación de la FGJ-CDMX. En el Hito 0 se confirma que el conjunto siga publicado, su frecuencia real de actualización y su licencia de uso. Como apoyo se usan datos de INEGI (por ejemplo, población para normalizar y catálogos) y, si aportan algo, del SESNSP. Siempre se guarda una copia del dato original sin modificar.
- Limpieza, normalización y validación de fecha, categoría delictiva y ubicación, con reporte de calidad por lote.
- Cálculo de riesgo por colonia o alcaldía y mes, con una fórmula simple, parámetros configurables y metodología documentada.
- Histórico en S3 (Parquet) con registros procesados, indicadores y bitácora de ejecuciones, consultable con Athena.
- Proceso batch programado (mínimo una vez al día), con alertas, registro de errores y reintentos sin duplicar registros.
- Entrega de resultados mediante tablas en Athena y exportación de archivos estructurados (CSV y Parquet).
- Infraestructura en AWS definida como código (CloudFormation), en una cuenta propiedad del cliente.
- Manual técnico y operativo, documentación de arquitectura, decisiones técnicas (ADR) y metodología.
- Sesión de transferencia de conocimiento y capacitación remota.
- 30 días naturales de soporte posterior a la puesta en producción para corrección de defectos.

**Fuera de alcance:**
- Otras ciudades o estados: el proyecto cubre solo la CDMX.
- API REST con autenticación por cliente: el RFP (N5) acepta archivos estructurados, así que la API queda como mejora futura.
- Modelos de riesgo avanzados (cuadrícula hexagonal, ajustes estadísticos para zonas con pocos casos, tendencias con rango de incertidumbre): quedan como mejora futura sobre la fórmula base.
- Aplicación móvil o página web para usuarios finales: el RFP lo excluye; entregamos datos listos para las herramientas de visualización que ya usa SAFEZONE.
- Cámaras, sensores, GPS o infraestructura física: el proyecto trabaja solo con datos ya publicados.
- Bases policiales restringidas, expedientes judiciales o datos personales: el RFP lo prohíbe y no aportan a un indicador agregado por zona.
- Identificación de personas o predicción de delitos individuales: el resultado es un nivel de riesgo agregado por zona y periodo, no una predicción sobre personas.
- Respuesta policial, despacho de emergencias o intervención en campo: no es un servicio tecnológico de datos.
- Sesiones presenciales: el trabajo es remoto; si se requieren, se cotizan aparte (ver sección 10).
- Fuentes de paga o que requieran convenio: solo se integran fuentes públicas cuyas condiciones de uso lo permitan.

## 3. Entregables y criterios de aceptación

| # | Entregable | Criterio de aceptación | Hito |
|---|---|---|---|
| E1 | Documento de arranque: fuente principal confirmada (publicación vigente, frecuencia real de actualización, licencia y campos), nivel geográfico, reglas de "registro válido" y "zona con información suficiente", ADRs iniciales | Documento firmado por el responsable del cliente | 0 |
| E2 | Pipeline de ingesta con zona de datos originales (inmutable) | Al menos 90% de los registros válidos de cada lote se procesa con éxito en 3 lotes consecutivos (N1); el dato original de cada lote queda guardado y es recuperable | 1 |
| E3 | Proceso de limpieza, normalización y validación + reporte de calidad por lote | Al menos 95% de los registros utilizables tiene fecha, categoría y ubicación normalizadas (N2); cada lote genera su reporte de calidad con registros rechazados y motivo | 2 |
| E4 | Motor de cálculo de riesgo (etapa separada del pipeline) con parámetros configurables y metodología documentada | Se generan indicadores para al menos 85% de las zonas con información suficiente (N3); cambiar un peso o un umbral no requiere modificar código; metodología revisada por el cliente | 3 |
| E5 | Histórico en S3 (Parquet) y tablas en Athena (registros, indicadores, bitácora de lotes) | El 100% de los lotes registra fuente, fecha de actualización, versión de metodología y estado (N6) | 4 |
| E6 | Orquestación batch programada con reintentos | 3 días consecutivos de ejecución diaria automática; en una prueba de falla forzada el reintento termina sin registros duplicados (mismo conteo antes y después) (N4) | 4 |
| E7 | Tablas de consulta en Athena y exportación de archivos (CSV y Parquet) | Consulta por zona y rango de fechas; los archivos se cargan sin ajustes en la herramienta de visualización indicada por el cliente; cada resultado incluye fecha de actualización y limitaciones (N5) | 4 |
| E8 | Plan y reporte de pruebas (calidad, batch, rendimiento, recuperación, validación de resultados) | Todas las pruebas críticas pasan; reporte firmado por el cliente | 5 |
| E9 | Manual técnico y operativo, documentación de arquitectura y ADRs | El equipo del cliente ejecuta, reintenta y agrega una fuente siguiendo solo el manual, sin apoyo del proveedor | 5 |


## 4. Trazabilidad con el RFP

| Necesidad del RFP | Entregable(s) que la cubre(n) | Estado |
|---|---|---|
| N1 Integración automatizada de fuentes públicas | E1, E2 | Cubierta |
| N2 Limpieza y estandarización | E3 | Cubierta |
| N3 Cálculo de riesgo por zona y fecha | E1, E4 | Cubierta (la definición de "información suficiente" se acuerda en E1) |
| N4 Automatización por lotes | E6 | Cubierta |
| N5 Consulta de resultados | E7 | Cubierta |
| N6 Trazabilidad y confiabilidad | E2, E5 | Cubierta |

## 5. Enfoque técnico (alto nivel)

```
                       AWS (cuenta de SAFEZONE)
                      ┌──────────────────────────────────────────────────────────────────────────┐
                      │  EventBridge Scheduler (diario)                                          │
                      │          │                                                               │
                      │          ▼                                                               │
Datos abiertos FGJ ──►│  Lambda: descarga ──► S3 /crudo        (original sin tocar, versionado)  │
                      │          │                                                               │
                      │          ▼                                                               │
                      │  Lambda: limpieza y validación ──► S3 /limpio   (Parquet, por fecha)     │
                      │          │                                                               │
                      │          ▼                                                               │
                      │  Athena (SQL): cálculo de riesgo ──► S3 /resultados + tablas Athena      │
                      │                                                                          │
                      │  SNS + CloudWatch Logs: alertas y bitácora de cada lote                  │
                      │  Todo definido con CloudFormation                                        │
                      └──────────────────────────────────────────────────────────────────────────┘
                           │
                           ▼
                       Herramientas de visualización del cliente
```

Decisiones clave:
- **Cómputo sin servidores** (Lambda + EventBridge Scheduler): el proceso es diario y corto, así que no pagamos servidores encendidos todo el día y casi todo cabe en la capa gratuita de AWS. Si el volumen supera los límites de Lambda, se evalúa Glue cuidando el costo (se documenta en un ADR). Esto mantiene la operación muy por debajo de $25,500 MXN.
- **Parquet en S3 + Athena**: consultas SQL sin servidor, con pago por consulta. No hay base de datos encendida que administrar ni credenciales que guardar, porque las fuentes son públicas.
- **Dato original intocable**: cada descarga se guarda tal cual en S3 con versionado; si cambia la metodología, se puede recalcular todo el histórico.
- **Reintentos sin duplicados**: cada lote tiene un identificador y cada registro una huella (hash); al reintentar, el lote se reescribe completo en su propia partición y se descartan las huellas repetidas, así que nunca se duplica. Esto también cubre las correcciones retroactivas que la fuente pueda hacer a datos históricos.
- **Unidad geográfica**: colonia o alcaldía, unidas con un catálogo oficial. No se requiere base de datos geoespacial. El nivel exacto se decide en el Hito 0 según la población disponible para normalizar.
- **Metodología de riesgo explicable**: conteo de delitos ponderado por tipo, dividido entre la población, por colonia o alcaldía y mes, convertido en nivel bajo, medio o alto con umbrales configurables. Resultado: nivel, puntaje y nota de limitaciones. El cálculo vive en una etapa separada para poder cambiarlo sin tocar la ingesta.
- **Infraestructura como código** (CloudFormation, plantillas YAML) y todo el código en Git del cliente, para que no dependa de nosotros al terminar.

## 6. Plan por hitos

Fechas calculadas suponiendo firma del contrato el lunes 9 de noviembre de 2026.

| Hito | Qué se entrega | Evidencia | Fecha | Horas |
|---|---|---|---|---|
| 0 Arranque | E1: fuente confirmada, nivel geográfico, reglas de validación, cuenta AWS lista, ADRs iniciales | Documento de arranque firmado | Semana 1 — 13 nov 2026 | 120 |
| 1 Ingesta y datos originales | E2: descarga automática de la fuente y almacenamiento crudo | Demo de 3 lotes con métricas de procesamiento ≥ 90% | Semana 3 — 27 nov 2026 | 280 |
| 2 Limpieza y calidad | E3: normalización, validación y reportes de calidad | Reporte de calidad con ≥ 95% de registros normalizados | Semana 4 — 4 dic 2026 | 280 |
| 3 Motor de riesgo | E4: cálculo por zona y periodo, parámetros configurables, metodología | Indicadores en ≥ 85% de zonas con información suficiente; revisión metodológica con el cliente | Semana 6 — 18 dic 2026 | 300 |
| 4 Batch, histórico y consulta | E5, E6, E7: orquestación diaria, reintentos, bitácora, tablas de consulta y archivos | Bitácora de 3 días de ejecución, prueba de falla y reintento, demo de consulta en Athena y archivos | Semana 7 — 23 dic 2026 | 260 |
| 5 Pruebas, documentación y producción | E8, E9: pruebas finales, manuales, capacitación y salida a producción | Reporte de pruebas firmado, sesión grabada, sistema en producción | Semana 8 — 31 dic 2026 | 160 |
| **Total** | | | | **1,400** |

Revisión con el cliente cada semana y demo al cierre de cada hito. El soporte de 30 días inicia al aceptar el Hito 5.

**Calendario de E6:** la programación diaria se activa a más tardar el viernes 18 de diciembre, al cierre del Hito 3. Así, del 19 al 22 de diciembre se acumulan los 3 días consecutivos de bitácora que se muestran en la demo del Hito 4 (23 de diciembre).

## 7. Equipo y responsabilidades

| Rol | Nombre | Responsabilidad principal | Reporta a |
|---|---|---|---|
| Líder de proyecto y arquitecto de datos | Amir Cuevas Quintana | Plan, arquitectura, ADRs, relación con el cliente, control de cambios | Responsable del proyecto en SAFEZONE |
| Ingeniero de datos (ingesta y orquestación) | Uriel Ivan Guerrero Lopez | Conectores a la fuente, almacenamiento crudo, EventBridge Scheduler y Lambda, reintentos y bitácora de lotes | Líder de proyecto |
| Ingeniero de datos (calidad y modelo de datos) | Axel Alejandro Quintos Delgadillo | Reglas de limpieza y validación, modelo de datos (tablas Athena), reportes de calidad | Líder de proyecto |
| Científico de datos | Aaron Rodrigo Leon Pérez | Unidad geográfica, metodología de riesgo, validación de resultados y limitaciones | Líder de proyecto |
| DevOps, pruebas y documentación | Eduardo Antonio Estrada Luna | CloudFormation, CI/CD, monitoreo, plan de pruebas, manuales y capacitación | Líder de proyecto |

## 8. Supuestos y dependencias del cliente

**Supuestos:**
- Las fuentes públicas (datos abiertos de la FGJ-CDMX como fuente principal; INEGI como apoyo) siguen disponibles y permiten su uso para este fin.
- SAFEZONE aporta o autoriza una cuenta de AWS a su nombre; los costos de nube se facturan directo al cliente.
- Los precios son en MXN y antes de IVA.
- Las sesiones de trabajo y capacitación son remotas.
- Tipo de cambio de referencia para estimar AWS: $19 MXN por dólar.

**Datos que no cuadran (y cómo los resolvemos):**
- **Ejecución diaria vs. frecuencia de la fuente:** la frecuencia real de actualización de los datos de la FGJ-CDMX se confirma en el Hito 0, y las fuentes de apoyo como el SESNSP publican de forma mensual. El batch correrá todos los días como pide N4, pero solo recalculará cuando detecte datos nuevos; el riesgo se calcula por mes y se actualiza para el mes en curso cuando llegan datos más recientes.
- **"Predictivo" vs. "sin predicción determinista":** entregamos un nivel de riesgo calculado con datos históricos por zona y mes, no predicciones de delitos concretos. La tendencia con rango de incertidumbre queda como mejora futura.
- **Términos sin definir en N1 y N3:** "registro válido" y "zona con información suficiente" se definen y firman en el Hito 0; sin eso no se pueden medir los porcentajes.
- **Nivel geográfico abierto:** colonia o alcaldía depende de la población disponible para normalizar; se decide en el Hito 0.
- **Cifra negra:** los registros oficiales no incluyen delitos no denunciados; cada indicador lo dirá en su nota de limitaciones.
- **Plazo con temporada decembrina:** las semanas 7 y 8 caen en fiestas; por eso concentramos el trabajo pesado antes del 18 de diciembre.

**Dependencias del cliente:**
- Un responsable del proyecto con autoridad para aprobar hitos y cambios.
- Respuesta a validaciones en un máximo de 3 días hábiles.
- Acceso a la cuenta de AWS en la semana 1.
- Nombre y formato de la herramienta de visualización destino antes del Hito 3.
- Aprobación de la metodología de riesgo en el Hito 3.
- Disponibilidad del equipo de ingeniería y analítica para la capacitación en la semana 8.

## 9. Riesgos

| Riesgo | Probabilidad | Impacto | Qué haremos |
|---|---|---|---|
| Cambia el formato o la URL de la fuente pública | Media | Alto | Validación de estructura antes de procesar; el lote falla de forma controlada, alerta al equipo y no contamina el histórico; conector separado por fuente |
| La fuente deja de publicarse o se retrasa | Media | Medio | Indicadores muestran la fecha del último dato; se marca la zona como "desactualizada" en lugar de inventar valores |
| Calidad baja de datos (ubicaciones vacías o colonias mal escritas) | Alta | Alto | Catálogos oficiales de alcaldías y colonias para normalizar, reglas de corrección documentadas y reporte de registros rechazados con su motivo |
| Sesgo por zonas con más denuncias o más cobertura | Alta | Alto | Regla de "información suficiente": las zonas con pocos casos se marcan sin calificar en lugar de ajustarse; nota de limitaciones en cada indicador; revisión de resultados con analistas del cliente |
| Interpretación errónea del indicador por clientes corporativos | Media | Alto | Cada resultado incluye fecha, versión de metodología y limitaciones; guía breve de interpretación en el manual |
| Retraso en definiciones del Hito 0 (fuente, nivel geográfico) | Media | Alto | Propuesta inicial preparada por nosotros para que el cliente solo valide; cualquier retraso mayor a 3 días hábiles se trata por control de cambios |
| Costos de nube por encima de lo estimado | Baja | Medio | Presupuesto en AWS Budgets con alerta por correo desde el primer día (al 50%, 80% y 100% del presupuesto mensual acordado en el Hito 0); cómputo sin servidores y sin NAT Gateway |
| Ausencias por temporada decembrina | Media | Medio | Trabajo crítico terminado antes del 18 de diciembre; fechas de revisión acordadas desde el arranque |
| Uso de una fuente fuera de sus condiciones de uso | Baja | Alto | Revisión de términos y licencia de cada fuente en el Hito 0; registro de licencia por fuente en la bitácora |

## 10. Presupuesto

| Concepto | Horas | Tarifa MXN/h | Subtotal MXN |
|---|---|---|---|
| Líder de proyecto y arquitecto de datos | 240 | 900 | 216,000 |
| Ingeniero de datos (ingesta y orquestación) | 320 | 700 | 224,000 |
| Ingeniero de datos (calidad y modelo) | 320 | 700 | 224,000 |
| Científico de datos | 280 | 800 | 224,000 |
| DevOps, pruebas y documentación | 240 | 600 | 144,000 |
| Colchón de imprevistos (15%) | | | 154,800 |
| **Total de honorarios** | **1,400** | | **1,186,800** |

- **Comparación contra el RFP:** los honorarios son de $1,186,800 MXN + IVA ($1,376,688 MXN con IVA), por debajo del máximo de $1,500,000 MXN en ambos casos. Aun sumando el costo estimado de AWS, el total sigue por debajo del máximo.
- **AWS no forma parte de los honorarios:** se paga directo en la cuenta del cliente. Durante las 8 semanas del proyecto (desarrollo, pruebas y producción) se estima en ~$3,000 MXN.
- El colchón cubre también los 30 días de soporte posterior. Si no se usa, no se cobra.
- **Sesión presencial opcional** (no incluida): $15,000 MXN por sesión en la CDMX, solo si el cliente la solicita.

**Costo mensual estimado de operación (después de la entrega):**

| Servicio AWS | MXN/mes |
|---|---|
| S3 (datos originales, limpios y resultados, con versionado) | 50 |
| Lambda (descarga y limpieza diarias) | 50 |
| Athena (consultas SQL y cálculo de riesgo) | 150 |
| EventBridge Scheduler y catálogo de tablas | 0 (capa gratuita) |
| CloudWatch Logs y SNS (bitácoras y alertas) | 150 |
| Transferencia de datos y otros | 50 |
| Margen de seguridad (30%) | 135 |
| **Total estimado** | **~600** |

Equivale a cerca del 2% del límite de $25,500 MXN; la cifra se valida con la calculadora de AWS en el Hito 0.

## 11. Control de cambios y comunicación

- **Pedir algo nuevo:** el cliente envía una solicitud de cambio por correo al líder de proyecto, indicando qué necesita y por qué.
- **Evaluación:** en 2 días hábiles respondemos con el impacto en horas, costo, fechas y riesgos.
- **Aprobación:** el cambio solo entra si lo firman el responsable de SAFEZONE y nuestro líder de proyecto. Lo no aprobado no se trabaja.
- **Registro:** todos los cambios quedan en una bitácora compartida con número, fecha y estado.
- **Revisión semanal:** reunión virtual de 45 minutos cada martes con avance, riesgos y pendientes del cliente.
- **Demo por hito:** sesión al cierre de cada hito para revisar la evidencia de aceptación.
- **Reporte semanal:** resumen por correo cada viernes. Canal de chat compartido para dudas del día a día; las decisiones formales siempre por correo.

## 12. Aceptación y pagos

- Un hito se da por terminado cuando el cliente firma el acta de aceptación con base en los criterios de la sección 3.
- El cliente tiene 5 días hábiles para revisar. Si hay observaciones, las corregimos en un máximo de 5 días hábiles y se vuelve a revisar solo lo observado.
- Si pasan 5 días hábiles sin respuesta ni observaciones, el hito se considera aceptado.
- El costo de AWS durante el proyecto se paga directo en la cuenta del cliente y no forma parte de estos pagos.

| Hito | % de honorarios | Monto MXN (antes de IVA) |
|---|---|---|
| 0 Arranque | 10% | 118,680 |
| 1 Ingesta y datos originales | 15% | 178,020 |
| 2 Limpieza y calidad | 15% | 178,020 |
| 3 Motor de riesgo | 20% | 237,360 |
| 4 Batch, histórico y consulta | 20% | 237,360 |
| 5 Pruebas, documentación y producción | 20% | 237,360 |
| **Total honorarios** | **100%** | **1,186,800** |

Los porcentajes se aplican a los honorarios ($1,186,800 MXN = horas + colchón), que son el total que cobra Data Bloom. Los ~$3,000 MXN estimados de AWS los paga SAFEZONE directo en su cuenta y no se suman a este total.
