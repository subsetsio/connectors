SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-li-gei17"
WHERE value IS NOT NULL
