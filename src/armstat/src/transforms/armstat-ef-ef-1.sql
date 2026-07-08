SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-ef-1"
WHERE value IS NOT NULL
