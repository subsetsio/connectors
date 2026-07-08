SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-cl-nso08"
WHERE value IS NOT NULL
