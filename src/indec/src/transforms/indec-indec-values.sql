SELECT DISTINCT
    series_id,
    CAST(date AS DATE)    AS date,
    CAST(value AS DOUBLE) AS value
FROM "indec-indec-values"
WHERE value IS NOT NULL
  AND series_id IS NOT NULL
