SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-pp-ipppi-3"
WHERE value IS NOT NULL
