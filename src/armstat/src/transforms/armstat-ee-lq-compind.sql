SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ee-lq-compind"
WHERE value IS NOT NULL
