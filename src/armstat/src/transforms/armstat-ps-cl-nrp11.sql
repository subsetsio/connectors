SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-cl-nrp11"
WHERE value IS NOT NULL
