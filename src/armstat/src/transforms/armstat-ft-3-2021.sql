SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ft-3-2021"
WHERE value IS NOT NULL
