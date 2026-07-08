SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-li-cej02"
WHERE value IS NOT NULL
