SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-si-nrdp06"
WHERE value IS NOT NULL
