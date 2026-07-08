SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ef-na-08qe05"
WHERE value IS NOT NULL
