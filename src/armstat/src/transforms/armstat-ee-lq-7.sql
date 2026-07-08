SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-lq-7"
WHERE value IS NOT NULL
