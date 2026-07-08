SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-si-no01"
WHERE value IS NOT NULL
