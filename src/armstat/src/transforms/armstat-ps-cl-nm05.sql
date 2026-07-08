SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-cl-nm05"
WHERE value IS NOT NULL
