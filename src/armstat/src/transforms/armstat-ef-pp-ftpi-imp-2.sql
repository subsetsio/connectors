SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-pp-ftpi-imp-2"
WHERE value IS NOT NULL
