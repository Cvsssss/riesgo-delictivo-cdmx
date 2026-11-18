-- Seleccionar la base de datos riesgo_cdmx_dev y el workgroup creado por CloudFormation.

SELECT alcaldia, mes, total_delitos, puntaje_ponderado, nivel_incidencia
FROM indicadores
ORDER BY mes DESC, puntaje_ponderado DESC;

-- Muestra solo niveles altos del indicador historico exploratorio.
SELECT alcaldia, mes, total_delitos, nivel_incidencia
FROM indicadores
WHERE nivel_incidencia = 'ALTO'
ORDER BY mes DESC, puntaje_ponderado DESC;
