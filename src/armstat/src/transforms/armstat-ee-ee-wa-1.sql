SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-ee-wa-1"
WHERE value IS NOT NULL
