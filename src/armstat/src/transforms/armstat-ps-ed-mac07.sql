SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-ed-mac07"
WHERE value IS NOT NULL
