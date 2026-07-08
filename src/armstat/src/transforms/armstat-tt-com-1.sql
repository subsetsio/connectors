SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-tt-com-1"
WHERE value IS NOT NULL
