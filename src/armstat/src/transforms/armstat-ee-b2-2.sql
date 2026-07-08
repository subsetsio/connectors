SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-b2-2"
WHERE value IS NOT NULL
