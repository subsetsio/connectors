SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ic-tr-5-2024"
WHERE value IS NOT NULL
