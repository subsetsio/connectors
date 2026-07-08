SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-pp-ipppi-4"
WHERE value IS NOT NULL
