SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-pp-api-proc-1"
WHERE value IS NOT NULL
