SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-li-gei06"
WHERE value IS NOT NULL
