SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-hs-sc06"
WHERE value IS NOT NULL
