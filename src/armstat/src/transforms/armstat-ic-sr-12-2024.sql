SELECT * EXCLUDE (value), CAST(value AS DOUBLE) AS value
FROM "armstat-ic-sr-12-2024"
WHERE value IS NOT NULL
