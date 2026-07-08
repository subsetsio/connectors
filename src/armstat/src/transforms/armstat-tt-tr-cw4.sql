SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-tt-tr-cw4"
WHERE value IS NOT NULL
