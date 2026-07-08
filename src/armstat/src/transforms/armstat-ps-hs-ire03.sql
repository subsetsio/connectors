SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-hs-ire03"
WHERE value IS NOT NULL
