SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-a1-1"
WHERE value IS NOT NULL
