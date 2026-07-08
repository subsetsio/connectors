SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ic-ind-m-01"
WHERE value IS NOT NULL
