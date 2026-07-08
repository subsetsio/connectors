SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-lq-3"
WHERE value IS NOT NULL
