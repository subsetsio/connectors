SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-eu-23-2024"
WHERE value IS NOT NULL
