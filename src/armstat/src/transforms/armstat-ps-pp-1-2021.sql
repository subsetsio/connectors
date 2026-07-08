SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-pp-1-2021"
WHERE value IS NOT NULL
