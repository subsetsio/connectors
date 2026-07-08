SELECT
    codigo_serie,
    frecuencia,
    CAST(date AS DATE)    AS date,
    CAST(value AS DOUBLE) AS value
FROM "central-bank-of-peru-values"
WHERE value IS NOT NULL
  AND codigo_serie IS NOT NULL
  AND date IS NOT NULL
