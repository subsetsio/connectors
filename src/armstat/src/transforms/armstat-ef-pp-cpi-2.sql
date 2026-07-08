SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-pp-cpi-2"
WHERE value IS NOT NULL
