SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-ee-wa-4"
WHERE value IS NOT NULL
