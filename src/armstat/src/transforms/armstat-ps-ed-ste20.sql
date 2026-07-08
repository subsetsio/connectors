SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-ed-ste20"
WHERE value IS NOT NULL
