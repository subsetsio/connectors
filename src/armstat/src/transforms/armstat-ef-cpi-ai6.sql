SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-cpi-ai6"
WHERE value IS NOT NULL
