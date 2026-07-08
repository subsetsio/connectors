SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-lq-10"
WHERE value IS NOT NULL
