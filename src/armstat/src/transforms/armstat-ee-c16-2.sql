SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-c16-2"
WHERE value IS NOT NULL
