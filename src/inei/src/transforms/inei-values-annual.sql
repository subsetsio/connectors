SELECT indicador_id, anio AS year, value
FROM (
    SELECT indicador_id, anio, valor AS value
    FROM "inei-values-annual"
) AS a
WHERE value IS NOT NULL
  AND anio IS NOT NULL
  AND value NOT BETWEEN -10000000000.0 AND -9999999999.0 AND value NOT BETWEEN -8888888889.0 AND -8888888888.0
