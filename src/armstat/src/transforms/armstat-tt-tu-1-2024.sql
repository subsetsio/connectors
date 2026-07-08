SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-tt-tu-1-2024"
WHERE value IS NOT NULL
