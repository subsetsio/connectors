SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-hs-bn19"
WHERE value IS NOT NULL
