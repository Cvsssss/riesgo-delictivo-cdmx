RFP: Sistema de Mapeo y Cálculo Predictivo de Riesgo Delictivo por Lotes (Batch Processing)

**Cliente:** SAFEZONE MÉXICO

**Contacto:** safezone_contacto@sz.mx

**Equipo redactor:** Área de Inteligencia de Datos de SAFEZONE MÉXICO

**Fecha de publicación:** 2026-10-06


## 1. Quiénes somos

Somos una empresa de tecnología aplicada a la seguridad privada en México que provee herramientas analíticas y mapas de riesgo para corporativos y ciudadanos. Consolidamos grandes volúmenes de información geoespacial para transformar datos públicos en decisiones accionables de prevención. Contamos con un equipo de 30 personas distribuidas entre ingeniería de datos, analítica geográfica, desarrollo web y atención a clientes corporativos.


## 2. El problema

Actualmente, la información sobre incidentes delictivos se encuentra distribuida en diferentes fuentes públicas y presenta diferencias en formatos, fechas y ubicaciones geográficas. Esto dificulta identificar patrones históricos y evaluar cómo cambia el riesgo delictivo entre distintas zonas y periodos.

Necesitamos automatizar la integración, limpieza y procesamiento de estos datos para calcular indicadores de riesgo por zona geográfica y fecha. La falta de una solución automatizada retrasa la actualización de nuestros mapas, limita la capacidad de detectar tendencias y dificulta que nuestros clientes tomen decisiones preventivas basadas en información actualizada y confiable.


## 3. Qué necesitamos lograr

| # | Necesidad | Cómo sabremos que se cumplió (medible) |
|---|---|---|
| N1 | Integración automatizada de información delictiva de fuentes públicas. | Procesamiento exitoso de al menos el 90% de los registros válidos recibidos en cada lote. |
| N2 | Limpieza y estandarización de los datos. | Al menos el 95% de los registros utilizables deberán contar con fecha, categoría y ubicación normalizadas. |
| N3 | Cálculo del nivel de riesgo por zona y fecha. | Generación de indicadores para al menos el 85% de las zonas que cuenten con información suficiente. |
| N4 | Automatización del procesamiento por lotes. | Ejecución programada al menos una vez al día, con registro de errores y posibilidad de reintentar procesos fallidos. |
| N5 | Consulta de los resultados. | Disponibilidad de los resultados procesados mediante un servicio de consulta o archivos estructurados para su integración con herramientas de visualización. |
| N6 | Trazabilidad y confiabilidad de la información. | Registro del origen de los datos, fecha de actualización, versión de la metodología y estado del 100% de los lotes ejecutados. |


## 4. Qué NO queremos en este proyecto

No incluye el desarrollo completo ni el rediseño visual de una aplicación móvil o página web para usuarios finales.

No contempla la instalación de cámaras, sensores, dispositivos GPS ni infraestructura física de vigilancia.

No incluye la integración con bases de datos policiales restringidas, expedientes judiciales privados o información personal sin autorización.

No contempla la identificación de personas como posibles delincuentes ni la predicción determinista de delitos individuales.

No incluye servicios de respuesta policial, despacho de emergencias ni intervención física en las zonas analizadas.


## 5. Datos que tenemos y datos que faltan

Datos que tenemos: Registros históricos de incidentes delictivos provenientes de fuentes públicas, cuando estén disponibles. Estos registros pueden incluir fecha, tipo de incidente, municipio, colonia, coordenadas geográficas y número de eventos reportados. La disponibilidad y calidad de estos campos dependerán de cada fuente.

Datos externos identificados: Bases de datos y conjuntos de información publicados por instituciones oficiales mexicanas, como el Secretariado Ejecutivo del Sistema Nacional de Seguridad Pública (SESNSP) y el Instituto Nacional de Estadística y Geografía (INEGI). Se evaluarán las condiciones de acceso, periodicidad, cobertura y uso de cada conjunto de datos.

Datos que faltan / dudas: Es necesario definir las fuentes definitivas, el nivel geográfico de análisis (colonia, cuadrícula o municipio), el periodo histórico disponible y la frecuencia de actualización. También se requiere establecer la fórmula de cálculo del riesgo, las variables que se utilizarán y los criterios para validar los resultados. Deberá considerarse que los registros oficiales no necesariamente representan la totalidad de los delitos ocurridos.


## 6. Restricciones

Presupuesto máximo: $1,500,000 MXN para el desarrollo e implementación de la solución completa.

Plazo: Entrega final y puesta en producción en un máximo de 8 semanas naturales a partir de la firma del contrato.

Costo de operación mensual máximo: $25,500 MXN mensuales para infraestructura de procesamiento, almacenamiento y servicios de consulta.

Seguridad y privacidad: Las credenciales y accesos a las fuentes de datos deberán almacenarse de forma segura. Se deberán respetar las condiciones de uso de las fuentes consultadas y evitar la exposición de información personal o restringida. Los resultados se presentarán de forma agregada por zona y periodo.

Quién lo va a usar: El equipo interno de ingeniería de datos y analítica geográfica, así como clientes corporativos que consultarán los resultados a través de los mecanismos autorizados.

Infraestructura: Se priorizarán servicios y tecnologías que permitan ejecutar procesos por lotes de manera programada, controlando los costos de operación.

Interpretación de resultados: Los indicadores deberán incluir su fecha de actualización, metodología general y limitaciones para evitar interpretaciones erróneas o conclusiones que no estén respaldadas por los datos.


## 7. Qué esperamos recibir

Pipeline de datos automatizado que obtenga información de fuentes públicas autorizadas, almacene los datos originales y los prepare para su análisis.

Proceso de limpieza, normalización y validación de registros, con reportes de calidad y manejo de datos incompletos.

Motor de cálculo de riesgo delictivo por zona y fecha, con metodología documentada y parámetros configurables.

Base de datos histórica con registros procesados, indicadores de riesgo, fechas de actualización y trazabilidad de las ejecuciones.

Proceso batch programado que genere nuevos resultados y permita reintentar ejecuciones fallidas sin duplicar registros.

Servicio de consulta documentado o archivos estructurados que permitan integrar los resultados con herramientas de visualización existentes.

Manual técnico y operativo, documentación de la arquitectura y sesión de transferencia de conocimiento para el equipo interno.

Capacitación: Se requiere una sesión de capacitación para el equipo de ingeniería de datos y analítica geográfica sobre la ejecución de procesos, revisión de errores, actualización de fuentes e interpretación de resultados.

Modalidad de trabajo: El trabajo podrá realizarse de forma remota, con reuniones virtuales de seguimiento. Las sesiones presenciales, si fueran necesarias, deberán acordarse previamente y especificarse en la propuesta económica.


## 8. Cómo evaluaremos las propuestas

| Criterio | Peso |
|---|---:|
| Robustez de la arquitectura de datos y confiabilidad del procesamiento por lotes | 30% |
| Claridad del plan de trabajo, cronograma y viabilidad del plazo | 15% |
| Cumplimiento del presupuesto y costo mensual de infraestructura | 20% |
| Experiencia en ingeniería de datos, análisis geoespacial y procesamiento de información | 20% |
| Gestión de riesgos, documentación, capacitación y soporte posterior al lanzamiento | 15% |
| Total | 100% |


## 9. Qué debe incluir su propuesta

Statement of Work (SOW): Alcance detallado, entregables, supuestos, exclusiones y criterios de aceptación.

Arquitectura de solución: Diagrama conceptual del flujo de datos, tecnologías propuestas y justificación de los componentes de ingesta, almacenamiento, procesamiento por lotes y consulta.

Metodología de cálculo: Explicación del enfoque estadístico o predictivo, variables utilizadas, definición de zonas y fechas, estrategia de validación y limitaciones.

Cronograma: Desglose semanal de actividades, hitos, revisiones y fechas de entrega.

Equipo de trabajo: Perfiles, responsabilidades y experiencia de los profesionales asignados al proyecto.

Matriz de riesgos: Identificación de riesgos relacionados con la disponibilidad de fuentes, calidad de datos, sesgos, confiabilidad de los indicadores y costos operativos, junto con sus medidas de mitigación.

Propuesta económica: Desglose de honorarios de desarrollo, implementación, capacitación y estimación mensual de costos de infraestructura.

Plan de pruebas y aceptación: Pruebas de calidad de datos, funcionamiento del procesamiento por lotes, rendimiento, recuperación ante fallos y validación de resultados.


## 10. Calendario del proceso

Fecha límite para preguntas y aclaraciones: 23 de octubre de 2026.

Fecha límite para entregar propuestas: 30 de octubre de 2026, hasta las 18:00 horas (CST).

Fecha de decisión y adjudicación: 6 de noviembre de 2026.

Las preguntas deberán enviarse al contacto oficial de SAFEZONE MÉXICO. Las propuestas deberán cumplir con los requisitos de alcance, presupuesto, calendario y documentación establecidos en este RFP.
 
