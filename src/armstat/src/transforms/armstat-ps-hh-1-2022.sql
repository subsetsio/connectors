SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-hh-1-2022"
WHERE value IS NOT NULL
