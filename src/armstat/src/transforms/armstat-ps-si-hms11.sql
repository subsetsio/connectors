SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-si-hms11"
WHERE value IS NOT NULL
