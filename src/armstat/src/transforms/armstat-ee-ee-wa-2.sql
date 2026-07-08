SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-ee-wa-2"
WHERE value IS NOT NULL
