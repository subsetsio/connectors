SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-ee-wa-5"
WHERE value IS NOT NULL
