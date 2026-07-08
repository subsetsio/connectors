SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-li-sca01"
WHERE value IS NOT NULL
