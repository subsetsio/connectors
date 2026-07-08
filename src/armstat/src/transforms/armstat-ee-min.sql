SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-min"
WHERE value IS NOT NULL
