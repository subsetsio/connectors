SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-hs-ws01"
WHERE value IS NOT NULL
