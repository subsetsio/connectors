SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-c11-r7"
WHERE value IS NOT NULL
