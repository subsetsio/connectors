SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ps-eu-3-2024"
WHERE value IS NOT NULL
