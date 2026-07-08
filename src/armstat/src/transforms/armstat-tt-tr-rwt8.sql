SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-tt-tr-rwt8"
WHERE value IS NOT NULL
