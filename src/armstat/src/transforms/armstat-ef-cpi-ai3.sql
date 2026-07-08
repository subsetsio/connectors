SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-cpi-ai3"
WHERE value IS NOT NULL
