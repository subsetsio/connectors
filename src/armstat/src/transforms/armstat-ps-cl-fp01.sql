SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-cl-fp01"
WHERE value IS NOT NULL
