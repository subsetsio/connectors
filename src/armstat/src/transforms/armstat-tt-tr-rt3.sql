SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-tt-tr-rt3"
WHERE value IS NOT NULL
