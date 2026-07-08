SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-lq-12"
WHERE value IS NOT NULL
