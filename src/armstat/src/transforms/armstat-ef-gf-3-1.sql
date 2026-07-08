SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-gf-3-1"
WHERE value IS NOT NULL
