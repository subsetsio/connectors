SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-hh-5-2022"
WHERE value IS NOT NULL
