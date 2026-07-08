SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-cpi-mi5"
WHERE value IS NOT NULL
