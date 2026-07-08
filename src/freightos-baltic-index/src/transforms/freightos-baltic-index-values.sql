SELECT DISTINCT
    CAST(date AS DATE)    AS date,
    index_code,
    CAST(value AS DOUBLE) AS value
FROM "freightos-baltic-index-values"
WHERE value IS NOT NULL
  AND date IS NOT NULL
  AND index_code IS NOT NULL
