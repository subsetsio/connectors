SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-i1-2"
WHERE value IS NOT NULL
