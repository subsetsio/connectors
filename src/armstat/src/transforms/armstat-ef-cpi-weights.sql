SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-cpi-weights"
WHERE value IS NOT NULL
