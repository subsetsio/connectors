SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-li-cej01"
WHERE value IS NOT NULL
