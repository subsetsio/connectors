SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-pp-cpi-1"
WHERE value IS NOT NULL
