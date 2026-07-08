SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-tt-tr-rt2"
WHERE value IS NOT NULL
