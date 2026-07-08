SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-tt-tr-rwt3"
WHERE value IS NOT NULL
