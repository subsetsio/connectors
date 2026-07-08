SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-si-nrdp08"
WHERE value IS NOT NULL
