SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-b3-2"
WHERE value IS NOT NULL
