SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-pp-ftpi-exp-2"
WHERE value IS NOT NULL
