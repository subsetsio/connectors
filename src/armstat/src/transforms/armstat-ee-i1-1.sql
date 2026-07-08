SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-i1-1"
WHERE value IS NOT NULL
